# Optimized single-container Dockerfile for Render.com
# =======================================================

# Stage 1: Frontend Builder
# -------------------------
FROM node:18-alpine AS frontend-builder

# Set working directory
WORKDIR /app

# Copy package files first for optimal Docker layer caching
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies in a separate layer for better caching
RUN npm ci && npm cache clean --force

# Copy configuration files
COPY frontend/next.config.js ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./
COPY frontend/tsconfig.json ./
COPY frontend/next-env.d.ts ./

# Copy source code
COPY frontend/src ./src
COPY frontend/public ./public

# Build the application with error handling
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV CI=true
ENV NPM_CONFIG_LOGLEVEL=error
ENV NEXT_PUBLIC_API_URL=https://getyourmusicgear.com

# Clear any existing build cache and build with verbose output for debugging
RUN rm -rf .next && \
    npm run build && \
    echo "Frontend build completed successfully" && \
    ls -la .next/

# Stage 2: Production Runtime
# ---------------------------
FROM python:3.11-slim AS production

# Add metadata labels
LABEL maintainer="Musical Instruments Platform"
LABEL description="Single container with FastAPI backend and Next.js frontend"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Install system dependencies in a single layer
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        curl \
        ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Copy Python requirements first for better caching
COPY backend/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Install Node.js for serving frontend (if needed)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy backend application
COPY backend/app ./app
COPY backend/alembic.ini ./alembic.ini
COPY backend/alembic ./alembic

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/.next ./frontend/.next
COPY --from=frontend-builder /app/public ./frontend/public
COPY --from=frontend-builder /app/package.json ./frontend/package.json

# Create non-root user for security
RUN addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --shell /bin/bash appuser \
    && chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Expose port
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Starting Musical Instruments Platform..."\n\
echo "Running database migrations..."\n\
python -m alembic upgrade head || echo "Migrations failed, continuing..."\n\
echo "Starting application..."\n\
exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1\n\
' > /app/start.sh && chmod +x /app/start.sh

# Start the application
CMD ["/app/start.sh"]
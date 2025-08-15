# Optimized Dockerfile for Render.com deployment
FROM node:18-alpine AS frontend-builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Clear npm cache and install dependencies with better error handling
RUN npm cache clean --force && \
    npm install --production=false --no-audit --no-fund --legacy-peer-deps --verbose

# Copy frontend source
COPY frontend/ ./

# Clear Next.js cache and build with better error handling
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV CI=true

RUN rm -rf .next && \
    rm -rf node_modules/.cache && \
    npm run build || (echo "Build failed, trying with legacy peer deps" && npm install --legacy-peer-deps && npm run build)

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY backend/ ./backend/

# Copy built frontend (if it exists)
COPY --from=frontend-builder /app/.next ./frontend/.next 2>/dev/null || echo "Frontend build not available"
COPY --from=frontend-builder /app/public ./frontend/public 2>/dev/null || echo "Frontend public not available"
COPY --from=frontend-builder /app/package.json ./frontend/package.json 2>/dev/null || echo "Frontend package.json not available"

# Set environment
ENV PYTHONPATH=/app
ENV PORT=10000

EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Start command
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "10000"]
# Frontend build
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Final image
FROM python:3.11-slim
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    gcc build-essential libpq-dev nginx nodejs npm gettext-base \
    && rm -rf /var/lib/apt/lists/*

# Install backend deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY backend/ .

# Copy frontend build + install production deps
COPY --from=frontend-builder /app/frontend ./frontend
WORKDIR /app/frontend
RUN npm ci --only=production

# Copy nginx config & start script
WORKDIR /app
COPY nginx.conf /etc/nginx/nginx.conf
COPY start.sh ./start.sh
RUN chmod +x ./start.sh

EXPOSE $PORT
CMD ["./start.sh"]

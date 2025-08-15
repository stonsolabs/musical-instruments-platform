#!/bin/bash

set -e

# Set default port
export PORT=${PORT:-10000}

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Cleanup function
cleanup() {
    log "Shutting down services..."
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

log "Starting Musical Instruments Platform..."
log "Port: $PORT"
log "Environment: ${NODE_ENV:-development}"

# Wait for database to be ready (if DATABASE_URL is set)
if [ ! -z "$DATABASE_URL" ]; then
    log "Waiting for database..."
    python -c "
import asyncpg
import asyncio
import os
import time

async def wait_for_db():
    for i in range(30):
        try:
            conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
            await conn.close()
            print('Database is ready!')
            break
        except Exception as e:
            print(f'Waiting for database... ({i+1}/30)')
            time.sleep(2)
    else:
        print('Database not ready after 60 seconds')
        exit(1)

asyncio.run(wait_for_db())
"
fi

# Run database migrations
if [ ! -z "$DATABASE_URL" ]; then
    log "Running database migrations..."
    cd /app
    python -m alembic upgrade head || log "Migration failed, continuing..."
fi

# Start FastAPI backend
log "Starting FastAPI backend on port 8000..."
cd /app
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info &
BACKEND_PID=$!

# Wait for backend to start
log "Waiting for backend to start..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        log "Backend is ready!"
        break
    fi
    sleep 1
done

# Start Next.js frontend
log "Starting Next.js frontend on port $PORT..."
cd /app/frontend

# Set Next.js environment variables
export NEXT_PUBLIC_API_URL="http://localhost:8000"
export HOSTNAME="0.0.0.0"

npm start -- --port $PORT --hostname 0.0.0.0 &
FRONTEND_PID=$!

log "All services started successfully!"
log "Backend PID: $BACKEND_PID"
log "Frontend PID: $FRONTEND_PID"

# Monitor processes
while true; do
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        log "Backend process died"
        exit 1
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        log "Frontend process died"
        exit 1
    fi
    sleep 10
done
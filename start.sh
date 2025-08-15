#!/bin/bash

# Musical Instruments Platform Startup Script
# ===========================================

set -e

echo "🎵 Starting Musical Instruments Platform..."

# Check if we're in a Docker container
if [ -f /.dockerenv ]; then
    echo "🐳 Running in Docker container"
    cd /app
else
    echo "💻 Running in local environment"
    cd backend
fi

# Wait for database to be ready (if using external database)
if [ -n "$DATABASE_URL" ]; then
    echo "⏳ Waiting for database to be ready..."
    # Simple database connection check
    python -c "
import asyncio
import sys
from app.database import engine
try:
    asyncio.run(engine.connect().close())
    print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    sys.exit(1)
" || exit 1
fi

# Run database migrations
echo "🔄 Running database migrations..."
python -m alembic upgrade head || {
    echo "⚠️  Migrations failed, but continuing..."
    echo "This might be expected if the database is already up to date"
}

# Start the application
echo "🚀 Starting FastAPI application..."
if [ -n "$PORT" ]; then
    echo "📡 Using port: $PORT"
    exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
else
    echo "📡 Using default port: 8000"
    exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
fi
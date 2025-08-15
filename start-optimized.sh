#!/bin/bash

set -e

export PORT=${PORT:-10000}

echo "Starting Musical Instruments Platform (Optimized)"
echo "Port: $PORT"

# Wait for database if needed
if [ ! -z "$DATABASE_URL" ]; then
    echo "Waiting for database..."
    python -c "
import asyncpg
import asyncio
import os
import sys

async def wait_for_db():
    try:
        conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
        await conn.close()
        print('Database connected!')
    except Exception as e:
        print(f'Database not available: {e}')
        print('Continuing without database...')

asyncio.run(wait_for_db())
"

    # Run migrations if possible
    echo "Running database migrations..."
    python -m alembic upgrade head 2>/dev/null || echo "Migrations skipped"
fi

# Start FastAPI with static file serving
echo "Starting FastAPI server..."
exec python -m uvicorn app.main:app \
    --host 0.0.0.0 \
    --port $PORT \
    --workers 1 \
    --log-level info
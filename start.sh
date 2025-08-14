#!/bin/bash
set -e

# Start backend
cd /app
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start frontend SSR
cd /app/frontend
npm start -- --port 3000 --hostname 0.0.0.0 &

# Start nginx (PID 1)
exec nginx -g 'daemon off;'

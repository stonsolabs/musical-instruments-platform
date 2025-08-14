#!/bin/bash

# Replace $PORT in nginx config with actual PORT value
export PORT=${PORT:-10000}
envsubst '${PORT}' < /etc/nginx/nginx.conf > /tmp/nginx.conf
cp /tmp/nginx.conf /etc/nginx/nginx.conf

# Start nginx in background
nginx &

# Start FastAPI backend in background
cd /app
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &

# Start Next.js frontend in background
cd /app/frontend
npm start -- --port 3000 --hostname 127.0.0.1 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
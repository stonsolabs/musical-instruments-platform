#!/bin/bash

# Deployment script for Render.com
set -e

echo "Starting deployment preparation..."

# Backend preparation
echo "Setting up backend..."
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
if [ "$ENVIRONMENT" = "production" ]; then
    python -m alembic upgrade head
fi

echo "Backend setup complete."

# Frontend preparation
echo "Setting up frontend..."
cd ../frontend

# Install Node.js dependencies
npm ci

# Build the frontend
npm run build

echo "Frontend build complete."

echo "Deployment preparation finished successfully!"
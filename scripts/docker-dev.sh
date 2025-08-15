#!/bin/bash

# Docker Development Script - Start separated services with hot reload

set -e

echo "🐳 Starting Musical Instruments Platform - Development Mode"
echo "   Frontend: http://localhost:3000 (with hot reload)"
echo "   Backend: http://localhost:8000 (with auto-reload)"
echo "   Database: localhost:5432"
echo "   Redis: localhost:6379"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Clean up any existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose -f docker-compose.dev.yml down -v 2>/dev/null || true

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.dev.yml up --build --remove-orphans

# Note: This will run in foreground. Press Ctrl+C to stop all services.

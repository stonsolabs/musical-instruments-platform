#!/bin/bash

# Docker Production Test Script - Test production builds locally

set -e

echo "🐳 Testing Musical Instruments Platform - Production Mode"
echo "   Frontend: http://localhost:3000 (SSR optimized)"
echo "   Backend: http://localhost:10000 (production settings)"
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
docker-compose -f docker-compose.prod.yml down -v 2>/dev/null || true

# Build and start services
echo "🔨 Building production images..."
docker-compose -f docker-compose.prod.yml build --no-cache

echo "🚀 Starting production services..."
docker-compose -f docker-compose.prod.yml up --remove-orphans

# Note: This will run in foreground. Press Ctrl+C to stop all services.

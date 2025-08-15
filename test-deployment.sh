#!/bin/bash

# Test Deployment Script for Musical Instruments Platform
# ======================================================

set -e

echo "🧪 Testing deployment configuration..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is running"

# Check if required files exist
required_files=(
    "Dockerfile"
    "render.yaml"
    "backend/requirements.txt"
    "backend/app/main.py"
    "backend/alembic.ini"
    "backend/alembic/env.py"
    "frontend/package.json"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Required file missing: $file"
        exit 1
    fi
done

print_status "All required files found"

# Test Docker build
echo "🔨 Testing Docker build..."
if docker build -t musical-instruments-test .; then
    print_status "Docker build successful"
else
    print_error "Docker build failed"
    exit 1
fi

# Test container startup
echo "🚀 Testing container startup..."
container_id=$(docker run -d -p 8000:8000 \
    -e DATABASE_URL="postgresql+asyncpg://test:test@localhost/test" \
    -e SECRET_KEY="test-secret-key" \
    -e DEBUG="true" \
    -e ENVIRONMENT="test" \
    musical-instruments-test)

# Wait for container to start
sleep 10

# Check if container is running
if docker ps | grep -q "$container_id"; then
    print_status "Container is running"
else
    print_error "Container failed to start"
    docker logs "$container_id"
    docker rm -f "$container_id" > /dev/null 2>&1 || true
    exit 1
fi

# Test health endpoint (if possible without database)
echo "🏥 Testing health endpoint..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status "Health endpoint is responding"
else
    print_warning "Health endpoint not responding (expected without database)"
fi

# Clean up
echo "🧹 Cleaning up test container..."
docker rm -f "$container_id" > /dev/null 2>&1 || true
docker rmi musical-instruments-test > /dev/null 2>&1 || true

print_status "Test completed successfully!"
echo ""
echo "🎉 Your deployment configuration is ready for Render.com!"
echo ""
echo "Next steps:"
echo "1. Push your changes to GitHub"
echo "2. Create a new Web Service in Render.com"
echo "3. Connect your repository"
echo "4. Configure environment variables"
echo "5. Deploy!"
echo ""
echo "See DEPLOYMENT.md for detailed instructions."

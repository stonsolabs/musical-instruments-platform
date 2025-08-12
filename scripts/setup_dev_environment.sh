#!/bin/bash

set -e  # Exit on any error

echo "🎵 Setting up Musical Instruments Platform Development Environment"

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Choose Python interpreter (override with PYTHON_BIN)
PYTHON_BIN=${PYTHON_BIN:-python3}
if ! command_exists "$PYTHON_BIN"; then
    echo "❌ $PYTHON_BIN is not installed. Please install Python 3.11+ or set PYTHON_BIN to a valid interpreter."
    exit 1
fi

# Ensure Python version is >= 3.8
PY_VER=$($PYTHON_BIN -c 'import sys; print("%d.%d"%sys.version_info[:2])')
case "$PY_VER" in
  3.8|3.9|3.10|3.11|3.12) : ;; 
  3.[0-7]|2.*)
    echo "❌ Python $PY_VER detected. Please install Python 3.11+ (e.g., via Homebrew: brew install python@3.11) or run: PYTHON_BIN=python3.11 $0"
    exit 1
    ;;
  *) : ;; 
esac

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ All prerequisites are installed!"

# Setup environment variables
echo "⚙️ Setting up environment variables..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📋 Created .env file from .env.example"
        echo "⚠️  Please edit .env file with your API keys and configuration"
    else
        echo "❌ .env.example file not found"
        exit 1
    fi
else
    echo "✅ .env file already exists"
fi

# Start database and Redis with Docker (supports Compose v2 and legacy v1)
echo "🐳 Starting database and Redis services..."

# pick docker compose command
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  DOCKER_COMPOSE_CMD="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  DOCKER_COMPOSE_CMD="docker-compose"
else
  echo "❌ Docker Compose not found. Install Docker Desktop (includes 'docker compose')."
  exit 1
fi

$DOCKER_COMPOSE_CMD up -d postgres redis

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Setup backend
echo "📦 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    "$PYTHON_BIN" -m venv venv
    echo "✅ Created Python virtual environment"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip/setuptools/wheel and install Python dependencies
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✅ Installed Python dependencies"

cd ..

# Setup frontend
echo "🌐 Setting up frontend..."
cd frontend

# Install Node.js dependencies
npm install
echo "✅ Installed Node.js dependencies"

cd ..

echo ""
echo "🎉 Development environment setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - OPENAI_API_KEY=your_openai_api_key"
echo "   - AMAZON_ASSOCIATE_TAG=your_amazon_tag"
echo "   - THOMANN_AFFILIATE_ID=your_thomann_id"
echo ""
echo "2. Start the development servers:"
echo "   Backend:  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "   Frontend: cd frontend && npm run dev"
echo ""
echo "3. Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "🎵 Happy coding!"

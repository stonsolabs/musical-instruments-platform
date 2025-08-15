#!/bin/bash

# Deployment script for separate Vercel + Render deployment
# Run this script to prepare your project for deployment

set -e

echo "🚀 Preparing Musical Instruments Platform for separate deployment..."
echo "   Frontend: Vercel"
echo "   Backend: Render.com"
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ] && [ ! -d "frontend" ] && [ ! -d "backend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Frontend preparation
echo "📦 Preparing frontend for Vercel..."
cd frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "   Installing frontend dependencies..."
    npm install
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "   Creating .env.local from example..."
    cp env.example .env.local
    echo "   ⚠️  Please update .env.local with your actual values"
fi

# Build frontend to check for errors
echo "   Building frontend..."
npm run build

cd ..

# Backend preparation  
echo "🐍 Preparing backend for Render..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "   Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "   Installing backend dependencies..."
pip install -r requirements.txt

# Test backend startup
echo "   Testing backend startup..."
python -c "from app.main import app; print('✅ Backend imports successfully')"

cd ..

echo ""
echo "✅ Project prepared for deployment!"
echo ""
echo "Next steps:"
echo "1. 📤 Push your code to GitHub"
echo "2. 🔧 Set up Render backend using render.yaml"
echo "3. 🌐 Set up Vercel frontend (root directory: frontend)"
echo "4. 🔑 Configure environment variables on both platforms"
echo "5. 📖 See VERCEL_RENDER_DEPLOYMENT.md for detailed instructions"
echo ""
echo "Happy deploying! 🎉"

#!/bin/bash

# Prepare for Vercel Deployment Script

set -e

echo "🚀 Preparing Musical Instruments Platform for Vercel deployment..."
echo ""

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if frontend directory exists and has the right files
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: frontend/package.json not found"
    exit 1
fi

if [ ! -f "frontend/next.config.js" ]; then
    echo "❌ Error: frontend/next.config.js not found"
    exit 1
fi

echo "📦 Installing frontend dependencies..."
cd frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "   Installing dependencies..."
    npm install
else
    echo "   Dependencies already installed, checking for updates..."
    npm ci
fi

# Type check
echo "🔍 Running type check..."
npm run type-check

# Build test
echo "🔨 Testing production build..."
npm run build

# Lint check
echo "🧹 Running linter..."
npm run lint || echo "⚠️  Linting issues found, but continuing..."

cd ..

echo ""
echo "✅ Frontend is ready for Vercel deployment!"
echo ""
echo "📋 Next steps:"
echo "1. 🔄 Push your code to GitHub"
echo "2. 🌐 Go to vercel.com and create new project"
echo "3. 📁 Set Root Directory to: frontend"
echo "4. 🔑 Add environment variables:"
echo "   - NEXT_PUBLIC_API_URL=https://your-backend-app.onrender.com"
echo "   - NEXT_PUBLIC_DOMAIN=getyourmusicgear.com"
echo "   - NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX (optional)"
echo "   - NEXT_PUBLIC_GTM_ID=GTM-XXXXXXX (optional)"
echo "5. 🚀 Deploy!"
echo ""
echo "📖 See VERCEL_DEPLOYMENT_STEPS.md for detailed instructions"
echo ""
echo "Happy deploying! 🎉"

#!/bin/bash

echo "🎵 Setting up GetYourMusicGear Frontend v2..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18.18.0 or higher."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18.18.0 or higher is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm 9.0.0 or higher."
    exit 1
fi

echo "✅ npm version: $(npm -v)"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create environment file
if [ ! -f .env.local ]; then
    echo "🔧 Creating .env.local file..."
    cp env.example .env.local
    echo "✅ Environment file created. Please update NEXT_PUBLIC_API_URL in .env.local"
else
    echo "✅ Environment file already exists"
fi

# Create placeholder image directory
mkdir -p public

echo ""
echo "🎉 Setup complete! Next steps:"
echo "1. Update .env.local with your API URL"
echo "2. Add a placeholder-product.jpg image to the public/ folder"
echo "3. Run 'npm run dev' to start the development server"
echo ""
echo "Happy coding! 🎸"

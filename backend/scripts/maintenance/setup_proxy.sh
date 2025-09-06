#!/bin/bash

# Setup script for proxy configuration
echo "🔧 Setting up proxy configuration for image download script"
echo "=========================================================="

# Check if proxy environment variables are set
if [ -z "$PROXY_URL" ]; then
    echo "⚠️  PROXY_URL not set, using default: http://127.0.0.1:8080"
    export PROXY_URL="http://127.0.0.1:8080"
else
    echo "✅ PROXY_URL set to: $PROXY_URL"
fi

if [ -z "$PROXY_USERNAME" ]; then
    echo "⚠️  PROXY_USERNAME not set (will use no authentication)"
else
    echo "✅ PROXY_USERNAME set"
fi

if [ -z "$PROXY_PASSWORD" ]; then
    echo "⚠️  PROXY_PASSWORD not set (will use no authentication)"
else
    echo "✅ PROXY_PASSWORD set"
fi

# Check if we're in the right directory
if [ ! -f "config.py" ]; then
    echo "❌ config.py not found! Please run this from the maintenance directory."
    exit 1
fi

# Test configuration
echo "🔧 Testing configuration..."
python3.11 -c "from config import print_config; print_config()"
if [ $? -ne 0 ]; then
    echo "❌ Configuration test failed!"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "🚀 Ready to run the image download script!"
echo "Run: python3.11 download_missing_images.py"
echo ""
echo "💡 To customize proxy settings, set these environment variables:"
echo "export PROXY_URL='http://your-proxy:port'"
echo "export PROXY_USERNAME='your-username'"
echo "export PROXY_PASSWORD='your-password'"

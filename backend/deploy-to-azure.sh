#!/bin/bash

# Azure Functions Deployment Script for Backend Subdirectory
# This script deploys the backend from a subdirectory to Azure Functions

set -e  # Exit on any error

# Configuration - Update these values for your deployment
FUNCTION_APP_NAME="${FUNCTION_APP_NAME:-musical-instruments-platform}"
RESOURCE_GROUP="${RESOURCE_GROUP:-your-resource-group}"
PYTHON_VERSION="3.11"

echo "🚀 Starting Azure Functions deployment from backend subdirectory..."
echo "Function App: $FUNCTION_APP_NAME"
echo "Resource Group: $RESOURCE_GROUP"
echo "Python Version: $PYTHON_VERSION"

# Check if we're in the right directory
if [[ ! -f "function_app.py" ]]; then
    echo "❌ Error: function_app.py not found. Make sure you're running this from the backend directory."
    exit 1
fi

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Error: Azure CLI is not installed. Please install it first."
    echo "   Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo "❌ Error: Not logged in to Azure. Please run 'az login' first."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Clean up previous deployment files
echo "🧹 Cleaning up previous deployment files..."
rm -rf deployment/
rm -f ../backend-deploy.zip

# Create deployment directory
echo "📦 Preparing deployment package..."
mkdir -p deployment

# Copy all necessary files except excluded ones
rsync -av --exclude='venv/' \
          --exclude='__pycache__/' \
          --exclude='.pytest_cache/' \
          --exclude='*.pyc' \
          --exclude='.coverage' \
          --exclude='local.settings.json' \
          --exclude='.env*' \
          --exclude='deployment/' \
          --exclude='.git' \
          ./ deployment/

# Install dependencies in deployment directory
echo "📥 Installing Python dependencies..."
cd deployment
python -m pip install --upgrade pip
pip install -r requirements.txt --target=".python_packages/lib/site-packages" --quiet

# Remove unnecessary files from dependencies
echo "🗑️  Cleaning up unnecessary files..."
find .python_packages -name "*.pyc" -delete
find .python_packages -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

cd ..

# Create ZIP package
echo "📦 Creating deployment ZIP..."
cd deployment
zip -r ../../backend-deploy.zip . -q
cd ..

echo "✅ Deployment package created: ../backend-deploy.zip"

# Deploy to Azure Functions
echo "🚀 Deploying to Azure Functions..."
az functionapp deployment source config-zip \
    --resource-group "$RESOURCE_GROUP" \
    --name "$FUNCTION_APP_NAME" \
    --src ../backend-deploy.zip \
    --verbose

echo "🎉 Deployment completed successfully!"
echo ""
echo "🌐 Function App URL: https://$FUNCTION_APP_NAME.azurewebsites.net"
echo "🏥 Health Check: https://$FUNCTION_APP_NAME.azurewebsites.net/health"
echo ""

# Test the deployment
echo "🧪 Testing deployment..."
sleep 10  # Give the function time to start

if curl -f "https://$FUNCTION_APP_NAME.azurewebsites.net/health" --silent --show-error; then
    echo "✅ Health check passed!"
else
    echo "⚠️  Health check failed - function may still be starting up"
    echo "   Check the Azure portal for logs if issues persist"
fi

# Clean up
echo "🧹 Cleaning up temporary files..."
rm -rf deployment/
rm -f ../backend-deploy.zip

echo ""
echo "🎊 Deployment process complete!"
echo "📋 Next steps:"
echo "   1. Check the Function App in Azure portal"
echo "   2. Verify environment variables are set"
echo "   3. Test your API endpoints"
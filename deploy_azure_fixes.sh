#!/bin/bash

# Azure Backend Deployment Script
# Updates the Azure App Service with our Redis fixes and other improvements

set -e

echo "🚀 Deploying Azure Backend Fixes"
echo "==============================="

# Configuration
RESOURCE_GROUP="getyourmusicgear"
APP_NAME="getyourmusicgear-api"
ACR_NAME="getyourmusicgear"
IMAGE_NAME="getyourmusicgear-backend"
TAG="fixes-$(date +%Y%m%d-%H%M%S)"

echo "📋 Deployment Configuration:"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   App Name: $APP_NAME"
echo "   Registry: $ACR_NAME.azurecr.io"
echo "   Image: $IMAGE_NAME:$TAG"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/Dockerfile" ]; then
    echo "❌ Error: backend/Dockerfile not found"
    echo "   Make sure you're running this from the project root"
    exit 1
fi

# Check if Azure CLI is logged in
echo "🔑 Checking Azure CLI authentication..."
if ! az account show > /dev/null 2>&1; then
    echo "❌ Error: Not logged in to Azure CLI"
    echo "   Run: az login"
    exit 1
fi

echo "✅ Azure CLI authenticated"

# Build the Docker image
echo "🐳 Building Docker image with fixes..."
cd backend
docker build -t "$ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG" .

if [ $? -ne 0 ]; then
    echo "❌ Error: Docker build failed"
    exit 1
fi

echo "✅ Docker image built successfully"

# Login to Azure Container Registry
echo "🔐 Logging in to Azure Container Registry..."
az acr login --name "$ACR_NAME"

if [ $? -ne 0 ]; then
    echo "❌ Error: ACR login failed"
    exit 1
fi

echo "✅ ACR login successful"

# Push the image
echo "📤 Pushing image to Azure Container Registry..."
docker push "$ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG"

if [ $? -ne 0 ]; then
    echo "❌ Error: Docker push failed"
    exit 1
fi

echo "✅ Image pushed successfully"

# Update App Service
echo "🔄 Updating Azure App Service with new image..."
az webapp config set \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --linux-fx-version "DOCKER|$ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG"

if [ $? -ne 0 ]; then
    echo "❌ Error: App Service update failed"
    exit 1
fi

echo "✅ App Service updated"

# Restart the app
echo "🔄 Restarting App Service..."
az webapp restart \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP"

if [ $? -ne 0 ]; then
    echo "❌ Error: App Service restart failed"
    exit 1
fi

echo "✅ App Service restarted"

# Wait for the app to start
echo "⏳ Waiting for app to start (90 seconds)..."
sleep 90

# Test the health endpoint
echo "🏥 Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s -w "%{http_code}" https://getyourmusicgear-api.azurewebsites.net/health -o /dev/null)

if [ "$HEALTH_RESPONSE" = "200" ]; then
    echo "✅ Health check passed"
else
    echo "⚠️  Health check returned: $HEALTH_RESPONSE"
    echo "   The app might still be starting up"
fi

# Test trending endpoint (our main fix)
echo "🔥 Testing trending endpoint (our Redis fix)..."
TRENDING_RESPONSE=$(curl -s -H "X-API-Key: de798fd16f6a38539f9d590dd72c4a02f20afccd782e91bbbdc34037482632db" \
    https://getyourmusicgear-api.azurewebsites.net/api/v1/trending/instruments?limit=3)

if echo "$TRENDING_RESPONSE" | grep -q "trending_instruments"; then
    echo "✅ Trending endpoint working!"
else
    echo "⚠️  Trending endpoint response: $TRENDING_RESPONSE"
fi

cd ..

echo ""
echo "🎉 Deployment completed!"
echo "==============================="
echo "Backend URL: https://getyourmusicgear-api.azurewebsites.net"
echo "Health Check: https://getyourmusicgear-api.azurewebsites.net/health"
echo "Image Tag: $TAG"
echo ""
echo "✅ Fixed Issues:"
echo "   - Redis client usage in trending service"
echo "   - Trending API 500 errors"
echo "   - Product comparison tracking"
echo ""
echo "Next steps:"
echo "1. Test all API endpoints: python3 backend/test_azure_endpoints.py"
echo "2. Check logs: az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo "3. Update frontend environment variables if needed"

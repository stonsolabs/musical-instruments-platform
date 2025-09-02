#!/bin/bash

# Thomann Image Downloader Deployment Script for Azure Container Apps
# This script builds and deploys the image downloader service to Azure Container Registry and Container Apps

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ACR_NAME="getyourmusicgearacr"
RESOURCE_GROUP="getyourmusicgear"
CONTAINER_APP_NAME="thomann-image-downloader"
CONTAINER_ENVIRONMENT="getyourmusicgear-env"
IMAGE_NAME="thomann-image-downloader"
TAG="latest"

echo -e "${BLUE}🚀 Thomann Image Downloader Deployment to Azure Container Apps${NC}"
echo "=================================================="

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

echo -e "${YELLOW}🔍 Checking Azure login status...${NC}"
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Azure. Please run 'az login' first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Azure login confirmed${NC}"

# Load environment variables from .env file
echo -e "${YELLOW}📁 Loading environment variables from .env file...${NC}"
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo -e "${GREEN}✅ Environment variables loaded from .env file${NC}"
else
    echo -e "${RED}❌ .env file not found. Please create it with required variables.${NC}"
    exit 1
fi

# Validate required environment variables
echo -e "${YELLOW}🔍 Validating required environment variables...${NC}"
if [ -z "$IPROYAL_PROXY_URL" ]; then
    echo -e "${RED}❌ IPROYAL_PROXY_URL not found in .env file${NC}"
    exit 1
fi

if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}❌ DATABASE_URL not found in .env file${NC}"
    exit 1
fi

if [ -z "$AZURE_STORAGE_CONNECTION_STRING" ]; then
    echo -e "${RED}❌ AZURE_STORAGE_CONNECTION_STRING not found in .env file${NC}"
    exit 1
fi

# Set default values for optional variables
AZURE_STORAGE_CONTAINER=${AZURE_BLOB_CONTAINER:-"product-images"}
MAX_CONCURRENT_DOWNLOADS="20"  # Force to 20 for optimal performance

echo -e "${GREEN}✅ All required environment variables are present${NC}"
echo -e "${BLUE}📊 Configuration:${NC}"
echo -e "   📦 Storage Container: $AZURE_STORAGE_CONTAINER"
echo -e "   🚀 Max Concurrent: $MAX_CONCURRENT_DOWNLOADS"
echo -e "   🔗 Proxy: ${IPROYAL_PROXY_URL:0:30}..."

# Login to ACR
echo -e "${YELLOW}🔐 Logging in to Azure Container Registry...${NC}"
az acr login --name $ACR_NAME

# Build the Docker image
echo -e "${YELLOW}🔨 Building Docker image...${NC}"
docker build -f Dockerfile.image_downloader -t $IMAGE_NAME:$TAG .

# Tag the image for ACR
echo -e "${YELLOW}🏷️  Tagging image for ACR...${NC}"
docker tag $IMAGE_NAME:$TAG $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG

# Push the image to ACR
echo -e "${YELLOW}⬆️  Pushing image to ACR...${NC}"
docker push $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG

echo -e "${GREEN}✅ Image pushed to ACR successfully${NC}"

# Check if container app exists
echo -e "${YELLOW}🔍 Checking if container app exists...${NC}"
if az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo -e "${YELLOW}📝 Container app exists, updating...${NC}"
    
    # Update existing container app - just update the image and env vars
    az containerapp update \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --image $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG \
        --set-env-vars \
            AZURE_STORAGE_CONTAINER="$AZURE_STORAGE_CONTAINER" \
            MAX_CONCURRENT_DOWNLOADS="$MAX_CONCURRENT_DOWNLOADS" \
            TEST_MODE="false"
    
    echo -e "${GREEN}✅ Container app updated successfully${NC}"
else
    echo -e "${YELLOW}🆕 Container app doesn't exist, creating...${NC}"
    
    # Get the actual ACR password
    ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)
    
    # Create new container app using proper ACR authentication
    az containerapp create \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --environment $CONTAINER_ENVIRONMENT \
        --image $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG \
        --registry-server $ACR_NAME.azurecr.io \
        --registry-username $ACR_NAME \
        --registry-password $ACR_PASSWORD \
        --secrets \
            database-url="$DATABASE_URL" \
            iproyal-proxy-url="$IPROYAL_PROXY_URL" \
            azure-storage-connection-string="$AZURE_STORAGE_CONNECTION_STRING" \
        --env-vars \
            AZURE_STORAGE_CONTAINER="$AZURE_STORAGE_CONTAINER" \
            MAX_CONCURRENT_DOWNLOADS="$MAX_CONCURRENT_DOWNLOADS" \
            TEST_MODE="false" \
            DATABASE_URL="secretref:database-url" \
            IPROYAL_PROXY_URL="secretref:iproyal-proxy-url" \
            AZURE_STORAGE_CONNECTION_STRING="secretref:azure-storage-connection-string" \
        --cpu 1.0 \
        --memory 2Gi \
        --min-replicas 0 \
        --max-replicas 3 \
        --ingress external \
        --target-port 8000
    
    echo -e "${GREEN}✅ Container app created successfully${NC}"
fi

# Start the container app
echo -e "${YELLOW}🚀 Starting container app...${NC}"
az containerapp update \
    --name $CONTAINER_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --min-replicas 1

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"

# Show deployment status
echo -e "${BLUE}📊 Container App Status:${NC}"
az containerapp show \
    --name $CONTAINER_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query "{Name:name, Status:properties.runningStatus, Replicas:properties.template.scale.minReplicas, Image:properties.template.containers[0].image}" \
    --output table

echo ""
echo -e "${GREEN}🎉 Thomann Image Downloader is now running in Azure Container Apps!${NC}"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo "  # View logs"
echo "  az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow"
echo ""
echo "  # Check status"
echo "  az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP"
echo ""
echo "  # Scale up/down"
echo "  az containerapp update --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --min-replicas 3"
echo "  az containerapp update --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --min-replicas 0"
echo ""
echo -e "${BLUE}Estimated cost: €0.50-1.00 per day (depending on usage)${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "  1. Monitor logs to ensure images are downloading correctly"
echo "  2. Check database to verify images column is being updated"
echo "  3. Verify images are accessible in Azure Storage"
echo "  4. Test frontend to ensure images display correctly"
echo ""
echo -e "${BLUE}🔧 Environment variables used:${NC}"
echo "  📦 Storage Container: $AZURE_STORAGE_CONTAINER"
echo "  🚀 Max Concurrent: $MAX_CONCURRENT_DOWNLOADS"
echo "  🔗 Proxy: ${IPROYAL_PROXY_URL:0:30}..."
echo "  🗄️  Database: ${DATABASE_URL:0:50}..."

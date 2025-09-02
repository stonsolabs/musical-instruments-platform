#!/bin/bash

# Deploy Enhanced Thomann Image Downloader to Azure
# This version includes duplicate prevention by checking blob storage first

set -e

RESOURCE_GROUP="getyourmusicgear"
CONTAINER_APP_NAME="thomann-image-downloader"
ACR_NAME="getyourmusicgear"
IMAGE_NAME="thomann-image-downloader"
IMAGE_TAG="enhanced-$(date +%Y%m%d-%H%M%S)"
FULL_IMAGE_NAME="${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🚀 Deploying Enhanced Thomann Image Downloader${NC}"
echo -e "${BLUE}📦 Image: ${FULL_IMAGE_NAME}${NC}"
echo "============================================================"

# 1. Build the Docker image
echo -e "${YELLOW}1. Building Docker image...${NC}"
docker build -f Dockerfile.image_downloader -t "${FULL_IMAGE_NAME}" .

# 2. Log in to Azure Container Registry
echo -e "${YELLOW}2. Logging in to Azure Container Registry...${NC}"
az acr login --name "${ACR_NAME}"

# 3. Push the Docker image to ACR
echo -e "${YELLOW}3. Pushing Docker image to ACR...${NC}"
docker push "${FULL_IMAGE_NAME}"

# 4. Update the Container App to use the new image
echo -e "${YELLOW}4. Updating Container App with enhanced image...${NC}"
az containerapp update \
    --name "${CONTAINER_APP_NAME}" \
    --resource-group "${RESOURCE_GROUP}" \
    --image "${FULL_IMAGE_NAME}" \
    --set-env-vars \
        MAX_CONCURRENT_DOWNLOADS=20 \
        DUPLICATE_PREVENTION=true \
        BLOB_STORAGE_CHECK=true

# 5. Show the deployment status
echo -e "${YELLOW}5. Checking deployment status...${NC}"
az containerapp show \
    --name "${CONTAINER_APP_NAME}" \
    --resource-group "${RESOURCE_GROUP}" \
    --query "{Name:name, Status:properties.runningStatus, Image:properties.template.containers[0].image, Replicas:properties.template.scale}" \
    --output table

echo ""
echo -e "${GREEN}✅ Enhanced Image Downloader Deployed Successfully!${NC}"
echo -e "${BLUE}📋 New Features:${NC}"
echo "   ✅ Duplicate prevention by checking blob storage"
echo "   ✅ Skips products that already have images"
echo "   ✅ Detailed filtering statistics"
echo "   ✅ Safe for parallel execution"
echo ""
echo -e "${YELLOW}🚀 To start the enhanced downloader:${NC}"
echo "   ./start-image-downloader.sh start"
echo ""
echo -e "${YELLOW}📊 To monitor progress:${NC}"
echo "   ./start-image-downloader.sh logs"
echo ""
echo -e "${YELLOW}⚡ To scale up for faster processing:${NC}"
echo "   ./start-image-downloader.sh scale 5"

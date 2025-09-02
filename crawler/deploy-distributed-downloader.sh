#!/bin/bash

# Deploy Distributed Thomann Image Downloader to Azure
# This version uses database-based distributed locking to prevent duplicate processing
# Safe to run multiple replicas without wasting proxy requests

set -e

RESOURCE_GROUP="getyourmusicgear"
CONTAINER_APP_NAME="thomann-image-downloader"
ACR_NAME="getyourmusicgear"
IMAGE_NAME="thomann-image-downloader"
IMAGE_TAG="distributed-$(date +%Y%m%d-%H%M%S)"
FULL_IMAGE_NAME="${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🚀 Deploying Distributed Thomann Image Downloader${NC}"
echo -e "${BLUE}📦 Image: ${FULL_IMAGE_NAME}${NC}"
echo -e "${YELLOW}🔒 Features: Database-based distributed locking${NC}"
echo "============================================================"

# 1. Build the Docker image
echo -e "${YELLOW}1. Building Docker image with distributed locking...${NC}"
docker build -f Dockerfile.distributed_downloader -t "${FULL_IMAGE_NAME}" .

# 2. Log in to Azure Container Registry
echo -e "${YELLOW}2. Logging in to Azure Container Registry...${NC}"
az acr login --name "${ACR_NAME}"

# 3. Push the Docker image to ACR
echo -e "${YELLOW}3. Pushing Docker image to ACR...${NC}"
docker push "${FULL_IMAGE_NAME}"

# 4. Update the Container App to use the new image
echo -e "${YELLOW}4. Updating Container App with distributed downloader...${NC}"
az containerapp update \
    --name "${CONTAINER_APP_NAME}" \
    --resource-group "${RESOURCE_GROUP}" \
    --image "${FULL_IMAGE_NAME}" \
    --set-env-vars \
        MAX_CONCURRENT_DOWNLOADS=10 \
        DISTRIBUTED_LOCKING=true \
        LOCK_TIMEOUT_MINUTES=30

# 5. Show the deployment status
echo -e "${YELLOW}5. Checking deployment status...${NC}"
az containerapp show \
    --name "${CONTAINER_APP_NAME}" \
    --resource-group "${RESOURCE_GROUP}" \
    --query "{Name:name, Status:properties.runningStatus, Image:properties.template.containers[0].image, Replicas:properties.template.scale}" \
    --output table

echo ""
echo -e "${GREEN}✅ Distributed Image Downloader Deployed Successfully!${NC}"
echo -e "${BLUE}🔒 New Features:${NC}"
echo "   ✅ Database-based distributed locking"
echo "   ✅ Multiple replicas can run safely"
echo "   ✅ No duplicate proxy requests"
echo "   ✅ Automatic expired lock cleanup"
echo "   ✅ Per-replica progress tracking"
echo ""
echo -e "${YELLOW}🚀 Safe Multi-Replica Commands:${NC}"
echo ""
echo -e "${GREEN}# Start with 5 replicas (safe - no duplicates!)${NC}"
echo "   ./start-image-downloader.sh scale 5"
echo ""
echo -e "${GREEN}# Monitor all replicas${NC}"
echo "   ./start-image-downloader.sh logs"
echo ""
echo -e "${GREEN}# Check status${NC}"
echo "   ./start-image-downloader.sh status"
echo ""
echo -e "${GREEN}# Stop all replicas when done${NC}"
echo "   ./start-image-downloader.sh stop"
echo ""
echo -e "${YELLOW}⚡ Expected Performance:${NC}"
echo "   🔄 5 replicas × 10 concurrent = 50 parallel workers"
echo "   🔒 Each product processed exactly once"
echo "   📊 ~2,742 products to process"
echo "   ⏱️  Estimated time: 30-60 minutes"

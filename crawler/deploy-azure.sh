#!/bin/bash

# Azure Container Apps deployment script for Musical Instruments Crawler
# Usage: ./deploy-azure.sh

set -e

# Configuration - Using your existing Azure resources
RESOURCE_GROUP="getyourmusicgear"
CONTAINER_APP_NAME="production-crawler"
CONTAINER_REGISTRY="getyourmusicgearacr.azurecr.io"
IMAGE_NAME="musical-instruments-crawler"
TAG="latest"
ENVIRONMENT_NAME="getyourmusicgear-env"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Deploying Musical Instruments Crawler to Azure Container Apps${NC}"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Azure. Please run 'az login' first.${NC}"
    exit 1
fi

# Login to Azure Container Registry
echo -e "${YELLOW}🔐 Logging in to Azure Container Registry...${NC}"
az acr login --name getyourmusicgearacr

# Build and push Docker image
echo -e "${YELLOW}🔨 Building Docker image...${NC}"
docker build -t $CONTAINER_REGISTRY/$IMAGE_NAME:$TAG .

echo -e "${YELLOW}📤 Pushing image to Azure Container Registry...${NC}"
docker push $CONTAINER_REGISTRY/$IMAGE_NAME:$TAG

# Deploy 13 replicas - one per category (maximum speed for one-time crawl)
echo -e "${YELLOW}🚀 Deploying 13 replicas - one per category...${NC}"

# Get ACR credentials for container apps
echo -e "${YELLOW}🔑 Getting ACR credentials...${NC}"
ACR_USERNAME=$(az acr credential show --name getyourmusicgearacr --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name getyourmusicgearacr --query "passwords[0].value" -o tsv)

# Configure registry credentials for the main container app
echo -e "${YELLOW}🔧 Configuring registry credentials for main container app...${NC}"
az containerapp registry set \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --server $CONTAINER_REGISTRY \
  --username $ACR_USERNAME \
  --password $ACR_PASSWORD

# First, update the main container app for category 0
az containerapp update \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --image $CONTAINER_REGISTRY/$IMAGE_NAME:$TAG \
  --set-env-vars \
    TEST_MODE=false \
    ASSIGNED_CATEGORIES="0" \
    MAX_CONCURRENT_REQUESTS=15 \
    DELAY_MIN_SECONDS=0.5 \
    DELAY_MAX_SECONDS=1.5 \
    DATABASE_URL=secretref:database-url \
    IPROYAL_PROXY_URL=secretref:iproyal-proxy-url \
  --cpu 1.0 \
  --memory 2Gi \
  --min-replicas 0 \
  --max-replicas 1

# Create 12 additional container apps for categories 1-12
for i in {1..12}; do
  CATEGORIES="$i"
  
  APP_NAME="${CONTAINER_APP_NAME}-cat${i}"
  echo -e "${YELLOW}📦 Creating replica for category ${i}...${NC}"
  
  az containerapp create \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --environment $ENVIRONMENT_NAME \
    --image $CONTAINER_REGISTRY/$IMAGE_NAME:$TAG \
    --registry-server $CONTAINER_REGISTRY \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD \
    --secrets \
      database-url=secretref:database-url \
      iproyal-proxy-url=secretref:iproyal-proxy-url \
    --env-vars \
      TEST_MODE=false \
      ASSIGNED_CATEGORIES="$CATEGORIES" \
      MAX_CONCURRENT_REQUESTS=15 \
      DELAY_MIN_SECONDS=0.5 \
      DELAY_MAX_SECONDS=1.5 \
      DATABASE_URL=secretref:database-url \
      IPROYAL_PROXY_URL=secretref:iproyal-proxy-url \
    --cpu 1.0 \
    --memory 2Gi \
    --min-replicas 0 \
    --max-replicas 1 \
    --ingress external \
    --target-port 8000 || echo "Category $i app might already exist, updating instead..."
    
  # If create failed, try update
  if [ $? -ne 0 ]; then
    az containerapp update \
      --name $APP_NAME \
      --resource-group $RESOURCE_GROUP \
      --image $CONTAINER_REGISTRY/$IMAGE_NAME:$TAG \
      --set-env-vars \
        TEST_MODE=false \
        ASSIGNED_CATEGORIES="$CATEGORIES" \
        MAX_CONCURRENT_REQUESTS=15 \
        DELAY_MIN_SECONDS=0.5 \
        DELAY_MAX_SECONDS=1.5
  fi
done

echo -e "${GREEN}✅ Deployment completed!${NC}"
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Set the DATABASE_URL secret: az containerapp secret set --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --secrets database-url='your-db-url'"
echo "2. Set the IPROYAL_PROXY_URL secret: az containerapp secret set --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --secrets iproyal-proxy-url='your-proxy-url'"
echo "3. Monitor logs: az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow"
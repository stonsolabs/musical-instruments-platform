#!/bin/bash

# Azure Setup Script for Musical Instruments Platform
# Azure Functions + Vercel Architecture

set -e

# Configuration
RESOURCE_GROUP="musical-instruments-rg"
LOCATION="eastus"
POSTGRES_SERVER="musical-instruments-db"
REDIS_CACHE="musical-instruments-redis"
STORAGE_ACCOUNT="musicalinstrumentsstorage"
FUNCTIONS_STORAGE="musicalfunctionsstorage"
FUNCTIONS_APP="musical-instruments-api"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Setting up Azure resources for Musical Instruments Platform${NC}"

# Check Azure CLI
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if logged in
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Azure. Please run 'az login' first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Azure CLI is ready${NC}"

# Step 1: Create Resource Group
echo -e "\n${YELLOW}📦 Creating Resource Group...${NC}"
az group create --name $RESOURCE_GROUP --location $LOCATION

# Step 2: Create PostgreSQL Database
echo -e "\n${YELLOW}🗄️  Creating PostgreSQL Database...${NC}"
az postgres flexible-server create \
  --resource-group $RESOURCE_GROUP \
  --name $POSTGRES_SERVER \
  --location $LOCATION \
  --admin-user postgres \
  --admin-password "YourSecurePassword123!" \
  --sku-name Standard_B1ms \
  --version 15 \
  --storage-size 32

# Create database
az postgres flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $POSTGRES_SERVER \
  --database-name musical_instruments

# Configure firewall
az postgres flexible-server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --name $POSTGRES_SERVER \
  --rule-name allow-azure-services \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Step 3: Create Redis Cache
echo -e "\n${YELLOW}🔴 Creating Redis Cache...${NC}"
az redis create \
  --resource-group $RESOURCE_GROUP \
  --name $REDIS_CACHE \
  --location $LOCATION \
  --sku Basic \
  --vm-size c0

# Get Redis connection string
REDIS_CONNECTION_STRING=$(az redis show-connection-string \
  --resource-group $RESOURCE_GROUP \
  --name $REDIS_CACHE \
  --query 'connectionString' -o tsv)

# Step 4: Create Storage Account
echo -e "\n${YELLOW}💾 Creating Storage Account...${NC}"
az storage account create \
  --resource-group $RESOURCE_GROUP \
  --name $STORAGE_ACCOUNT \
  --location $LOCATION \
  --sku Standard_LRS \
  --kind StorageV2

# Create container
az storage container create \
  --account-name $STORAGE_ACCOUNT \
  --name product-images \
  --public-access blob

# Get storage key
STORAGE_KEY=$(az storage account keys list \
  --resource-group $RESOURCE_GROUP \
  --account-name $STORAGE_ACCOUNT \
  --query '[0].value' -o tsv)

# Step 5: Create Functions Storage Account
echo -e "\n${YELLOW}📁 Creating Functions Storage Account...${NC}"
az storage account create \
  --resource-group $RESOURCE_GROUP \
  --name $FUNCTIONS_STORAGE \
  --location $LOCATION \
  --sku Standard_LRS

# Step 6: Create Azure Functions App
echo -e "\n${YELLOW}⚡ Creating Azure Functions App...${NC}"
az functionapp create \
  --resource-group $RESOURCE_GROUP \
  --consumption-plan-location $LOCATION \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --name $FUNCTIONS_APP \
  --storage-account $FUNCTIONS_STORAGE \
  --os-type linux

# Step 7: Configure Environment Variables
echo -e "\n${YELLOW}⚙️  Configuring Environment Variables...${NC}"
az functionapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $FUNCTIONS_APP \
  --settings \
    DATABASE_URL="postgresql+asyncpg://postgres:YourSecurePassword123!@$POSTGRES_SERVER.postgres.database.azure.com:5432/musical_instruments" \
    REDIS_CONNECTION_STRING="$REDIS_CONNECTION_STRING" \
    AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=$STORAGE_ACCOUNT;AccountKey=$STORAGE_KEY;EndpointSuffix=core.windows.net" \
    AZURE_STORAGE_ACCOUNT_NAME="$STORAGE_ACCOUNT" \
    AZURE_STORAGE_CONTAINER_NAME="product-images" \
    ENVIRONMENT="production" \
    SECRET_KEY="your-secret-key-here" \
    OPENAI_API_KEY="your-openai-api-key" \
    AMAZON_ASSOCIATE_TAG="your-amazon-tag" \
    THOMANN_AFFILIATE_ID="your-thomann-id"

# Step 8: Create Application Insights
echo -e "\n${YELLOW}📊 Creating Application Insights...${NC}"
az monitor app-insights component create \
  --resource-group $RESOURCE_GROUP \
  --app musical-instruments-insights \
  --location $LOCATION \
  --kind web

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --resource-group $RESOURCE_GROUP \
  --app musical-instruments-insights \
  --query 'instrumentationKey' -o tsv)

# Add to Functions
az functionapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $FUNCTIONS_APP \
  --settings \
    APPINSIGHTS_INSTRUMENTATIONKEY="$INSTRUMENTATION_KEY"

# Final output
echo -e "\n${GREEN}🎉 Azure setup completed successfully!${NC}"
echo -e "\n${YELLOW}📋 Resource Information:${NC}"
echo -e "Resource Group: ${GREEN}$RESOURCE_GROUP${NC}"
echo -e "PostgreSQL: ${GREEN}$POSTGRES_SERVER.postgres.database.azure.com${NC}"
echo -e "Redis Cache: ${GREEN}$REDIS_CACHE.redis.cache.windows.net${NC}"
echo -e "Storage Account: ${GREEN}$STORAGE_ACCOUNT.blob.core.windows.net${NC}"
echo -e "Functions App: ${GREEN}https://$FUNCTIONS_APP.azurewebsites.net${NC}"
echo -e "Application Insights: ${GREEN}musical-instruments-insights${NC}"

echo -e "\n${YELLOW}⚠️  Important Next Steps:${NC}"
echo "1. Update your environment variables with actual API keys"
echo "2. Deploy your Azure Functions code"
echo "3. Update Vercel with new API URL: https://$FUNCTIONS_APP.azurewebsites.net/api"
echo "4. Test all endpoints"
echo "5. Migrate your data to Azure PostgreSQL"

echo -e "\n${GREEN}✅ Setup script completed!${NC}"

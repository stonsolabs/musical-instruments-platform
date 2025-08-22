#!/bin/bash

# Deploy Azure Functions using Git
echo "🚀 Deploying Azure Functions to Azure..."

# Configuration
RESOURCE_GROUP="musical-instruments-rg"
FUNCTIONS_APP="musical-instruments-api"
FUNCTIONS_FOLDER="azure-functions-deployment/functions"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if Azure CLI is available
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Azure. Please run 'az login' first.${NC}"
    exit 1
fi

# Check if Functions folder exists
if [ ! -d "$FUNCTIONS_FOLDER" ]; then
    echo -e "${RED}❌ Functions folder not found: $FUNCTIONS_FOLDER${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Starting deployment...${NC}"

# Navigate to functions folder
cd $FUNCTIONS_FOLDER

# Install dependencies
echo -e "\n${YELLOW}📦 Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Deploy to Azure Functions
echo -e "\n${YELLOW}🚀 Deploying to Azure Functions...${NC}"
func azure functionapp publish $FUNCTIONS_APP

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ Deployment successful!${NC}"
    echo -e "\n${YELLOW}📋 Deployment Information:${NC}"
    echo -e "Functions App: ${GREEN}https://$FUNCTIONS_APP.azurewebsites.net${NC}"
    echo -e "Health Check: ${GREEN}https://$FUNCTIONS_APP.azurewebsites.net/api/health${NC}"
    
    echo -e "\n${YELLOW}🔍 Testing deployment...${NC}"
    sleep 10
    
    # Test health endpoint
    if curl -f "https://$FUNCTIONS_APP.azurewebsites.net/api/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Health check passed!${NC}"
    else
        echo -e "${YELLOW}⚠️  Health check failed. Check logs for details.${NC}"
    fi
    
    echo -e "\n${YELLOW}📊 View logs:${NC}"
    echo "az webapp log tail --resource-group $RESOURCE_GROUP --name $FUNCTIONS_APP"
    
else
    echo -e "\n${RED}❌ Deployment failed!${NC}"
    exit 1
fi

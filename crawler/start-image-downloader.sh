#!/bin/bash

# Start/Stop Thomann Image Downloader Container App
# Usage: ./start-image-downloader.sh [start|stop|status|logs]

set -e

RESOURCE_GROUP="getyourmusicgear"
CONTAINER_APP_NAME="thomann-image-downloader"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_usage() {
    echo "Usage: $0 [start|stop|status|logs|scale]"
    echo ""
    echo "Commands:"
    echo "  start   - Start the image downloader (set min-replicas to 1)"
    echo "  stop    - Stop the image downloader (set min-replicas to 0)"
    echo "  status  - Show current status"
    echo "  logs    - Show logs (follow mode)"
    echo "  scale   - Scale to specific number of replicas"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 stop"
    echo "  $0 status"
    echo "  $0 logs"
    echo "  $0 scale 3"
}

start_downloader() {
    echo -e "${YELLOW}🚀 Starting Thomann Image Downloader...${NC}"
    az containerapp update \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --min-replicas 1
    echo -e "${GREEN}✅ Image downloader started!${NC}"
}

stop_downloader() {
    echo -e "${YELLOW}🛑 Stopping Thomann Image Downloader...${NC}"
    az containerapp update \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --min-replicas 0
    echo -e "${GREEN}✅ Image downloader stopped!${NC}"
}

show_status() {
    echo -e "${BLUE}📊 Thomann Image Downloader Status:${NC}"
    az containerapp show \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --query "{Name:name, Status:properties.runningStatus, Replicas:properties.template.scale.minReplicas, Image:properties.template.containers[0].image, LastRevision:properties.latestRevisionName}" \
        --output table
}

show_logs() {
    echo -e "${BLUE}📋 Showing logs (press Ctrl+C to stop following):${NC}"
    az containerapp logs show \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --follow
}

scale_downloader() {
    if [ -z "$1" ]; then
        echo -e "${RED}❌ Please specify number of replicas${NC}"
        echo "Usage: $0 scale <number>"
        exit 1
    fi
    
    replicas=$1
    echo -e "${YELLOW}📈 Scaling image downloader to $replicas replicas...${NC}"
    az containerapp update \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --min-replicas $replicas
    echo -e "${GREEN}✅ Scaled to $replicas replicas!${NC}"
}

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo -e "${RED}❌ Not logged in to Azure. Please run 'az login' first.${NC}"
    exit 1
fi

# Parse command
case "${1:-}" in
    start)
        start_downloader
        ;;
    stop)
        stop_downloader
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    scale)
        scale_downloader "$2"
        ;;
    *)
        show_usage
        exit 1
        ;;
esac

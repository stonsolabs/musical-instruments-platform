#!/bin/bash

# Start all 13 crawler replicas simultaneously for one-time full crawl
# Usage: ./start-all-replicas.sh

set -e

RESOURCE_GROUP="getyourmusicgear"
MAIN_APP="production-crawler"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Starting all 13 crawler replicas simultaneously...${NC}"

# Start main app (category 0)
echo -e "${YELLOW}📦 Starting main crawler (category 0)...${NC}"
az containerapp update --name $MAIN_APP --resource-group $RESOURCE_GROUP --min-replicas 1

# Start all category-specific replicas (categories 1-12)
for i in {1..12}; do
    APP_NAME="$MAIN_APP-cat$i"
    echo -e "${YELLOW}📦 Starting replica for category $i...${NC}"
    az containerapp update --name $APP_NAME --resource-group $RESOURCE_GROUP --min-replicas 1 &
done

# Wait for all background jobs to complete
wait

echo -e "${GREEN}✅ All 13 replicas started!${NC}"
echo -e "${YELLOW}📋 Monitor progress:${NC}"
echo "Main crawler: az containerapp logs show --name $MAIN_APP --resource-group $RESOURCE_GROUP --follow"
echo "Category 1: az containerapp logs show --name $MAIN_APP-cat1 --resource-group $RESOURCE_GROUP --follow"
echo "Category 2: az containerapp logs show --name $MAIN_APP-cat2 --resource-group $RESOURCE_GROUP --follow"
echo "..."
echo ""
echo -e "${YELLOW}💰 Estimated cost for full crawl: €1.00-1.50 (1-1.5 hours)${NC}"
echo -e "${YELLOW}⚡ Expected throughput: 13 categories × 15 concurrent = 195 simultaneous requests${NC}"
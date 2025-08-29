# Azure Container Apps Deployment Guide

This guide explains how to deploy the Musical Instruments Crawler to Azure Container Apps for production use.

## Prerequisites

1. Azure CLI installed and configured
2. Docker installed locally
3. Azure Container Registry (ACR) created
4. Azure Container Apps Environment created
5. Azure PostgreSQL database running

## Environment Variables

The crawler requires these environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `IPROYAL_PROXY_URL`: Royal IP proxy URL for web scraping
- `TEST_MODE`: Set to `false` for production (crawl all products)
- `MAX_CONCURRENT_REQUESTS`: Number of concurrent requests (recommend 3-5 for production)
- `DELAY_MIN_SECONDS`: Minimum delay between requests (recommend 2.0)
- `DELAY_MAX_SECONDS`: Maximum delay between requests (recommend 4.0)

## Deployment Steps

### 1. Build and Push Docker Image

```bash
# Login to Azure Container Registry
az acr login --name your-registry

# Build and tag image
docker build -t your-registry.azurecr.io/musical-instruments-crawler:latest .

# Push to registry
docker push your-registry.azurecr.io/musical-instruments-crawler:latest
```

### 2. Deploy to Container Apps

Use the provided deployment script:

```bash
# Update configuration in deploy-azure.sh
# Then run:
./deploy-azure.sh
```

Or deploy manually:

```bash
az containerapp create \
  --name musical-instruments-crawler \
  --resource-group your-resource-group \
  --environment your-container-environment \
  --image your-registry.azurecr.io/musical-instruments-crawler:latest \
  --secrets \
    database-url="your-database-connection-string" \
    iproyal-proxy-url="your-proxy-url" \
  --env-vars \
    TEST_MODE=false \
    MAX_CONCURRENT_REQUESTS=3 \
    DELAY_MIN_SECONDS=2.0 \
    DELAY_MAX_SECONDS=4.0 \
    DATABASE_URL=secretref:database-url \
    IPROYAL_PROXY_URL=secretref:iproyal-proxy-url \
  --cpu 1.0 \
  --memory 2Gi \
  --min-replicas 0 \
  --max-replicas 1
```

### 3. Monitor Deployment

```bash
# View logs
az containerapp logs show \
  --name musical-instruments-crawler \
  --resource-group your-resource-group \
  --follow

# Check status
az containerapp show \
  --name musical-instruments-crawler \
  --resource-group your-resource-group
```

## Production Configuration

For production use:

1. **Set TEST_MODE=false** to crawl all 13 category URLs
2. **Use conservative concurrency** (3-5 concurrent requests) to avoid rate limiting
3. **Add delays** (2-4 seconds) between requests to be respectful to Thomann
4. **Monitor resource usage** and scale as needed
5. **Enable logging** to track crawler performance

## Scaling

The crawler is designed to run as a single instance (max-replicas=1) to avoid duplicate crawling. If you need faster processing:

1. Increase `MAX_CONCURRENT_REQUESTS` (carefully)
2. Reduce delays (but respect rate limits)
3. Split URLs across multiple deployments

## Troubleshooting

Common issues:

1. **Connection errors**: Check DATABASE_URL and proxy settings
2. **Rate limiting**: Increase delays between requests
3. **Memory issues**: Increase memory allocation in container spec
4. **Timeout errors**: Check proxy connectivity and Azure networking

## Cost Optimization

- Use `min-replicas=0` so container scales to zero when not running
- Set appropriate CPU/memory limits
- Monitor usage and adjust resources as needed
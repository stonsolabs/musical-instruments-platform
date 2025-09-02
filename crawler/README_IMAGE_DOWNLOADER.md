# Thomann Image Downloader Service

This service automatically downloads product images from Thomann product pages and stores them in Azure Blob Storage, then updates the database with the image paths for display in the UI.

## Features

- 🖼️ **Automatic Image Download**: Downloads main product images from Thomann product pages
- ☁️ **Azure Storage Integration**: Stores images in Azure Blob Storage under `product-images` container
- 🗄️ **Database Updates**: Updates the `images` column in the products table with proper paths
- 🛡️ **Anti-Blocking**: Uses proxies, random delays, and realistic browser simulation
- 📊 **Concurrent Processing**: Processes multiple products simultaneously (configurable)
- 🚀 **Container Apps Deployment**: Runs on Azure Container Apps for scalability

## How It Works

1. **Product Discovery**: Queries the database for products with Thomann links in `store_links`
2. **Image Extraction**: Visits each Thomann product page and extracts the main product image
3. **Azure Upload**: Uploads images to Azure Blob Storage with organized naming
4. **Database Update**: Updates the `images` column with structured JSON containing image metadata
5. **UI Integration**: Images are automatically available in the frontend through the database

## Database Schema

The service updates the `images` column in the products table with this structure:

```json
{
  "thomann_main": {
    "url": "https://yourstorage.blob.core.windows.net/product-images/thomann/product-name_20241201_143022.jpg",
    "source": "thomann",
    "source_url": "https://www.thomann.co.uk/product_page.htm",
    "downloaded_at": "2024-12-01T14:30:22.123456",
    "type": "main"
  }
}
```

## Azure Storage Structure

Images are stored in the `product-images` container with this path structure:
```
product-images/
└── thomann/
    ├── product-name-1_20241201_143022.jpg
    ├── product-name-2_20241201_143156.jpg
    └── ...
```

## Anti-Blocking Measures

- **Proxy Rotation**: Uses IPRoyal proxy service
- **Random Delays**: 2-5 second delays between requests
- **Realistic Headers**: Simulates real browser behavior
- **Referer Simulation**: Appears to come from Thomann homepage
- **User Agent Rotation**: Randomly selects from multiple browser user agents

## Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Proxy
IPROYAL_PROXY_URL=http://username:password@proxy.iproyal.com:port

# Azure Storage
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_STORAGE_CONTAINER=product-images

# Performance
MAX_CONCURRENT_DOWNLOADS=20
TEST_MODE=false
```

### Performance Settings

- **MAX_CONCURRENT_DOWNLOADS**: Number of simultaneous downloads (default: 20)
- **Delays**: 2-5 seconds between requests to avoid rate limiting
- **Resource Limits**: 1 CPU, 2GB RAM per container instance

## Deployment

### 1. Build and Deploy

```bash
# Deploy to Azure Container Apps
./deploy-image-downloader.sh
```

### 2. Start/Stop Service

```bash
# Start the service
./start-image-downloader.sh start

# Stop the service
./start-image-downloader.sh stop

# Check status
./start-image-downloader.sh status

# View logs
./start-image-downloader.sh logs

# Scale to specific replicas
./start-image-downloader.sh scale 3
```

### 3. Local Testing

```bash
# Test with limited products
python run_image_downloader.py --max-products 5 --test-mode

# Dry run to see what would be processed
python run_image_downloader.py --dry-run

# Run with verbose logging
python run_image_downloader.py --verbose
```

## Monitoring

### Azure Container Apps

```bash
# View logs
az containerapp logs show --name thomann-image-downloader --resource-group getyourmusicgear-rg --follow

# Check status
az containerapp show --name thomann-image-downloader --resource-group getyourmusicgear-rg

# Scale manually
az containerapp update --name thomann-image-downloader --resource-group getyourmusicgear-rg --min-replicas 5
```

### Database Monitoring

```sql
-- Check products with images
SELECT COUNT(*) FROM products WHERE images IS NOT NULL AND images != '{}';

-- Check products without images
SELECT COUNT(*) FROM products WHERE images IS NULL OR images = '{}';

-- View image metadata for a specific product
SELECT name, images FROM products WHERE sku = 'your-sku-here';
```

## Cost Estimation

- **Storage**: ~€0.02 per GB per month
- **Container Apps**: ~€0.50-1.00 per day when running
- **Data Transfer**: Minimal (images are typically 20-50KB each)
- **Total**: ~€15-30 per month for continuous operation

## Troubleshooting

### Common Issues

1. **Proxy Connection Failed**
   - Check IPRoyal proxy credentials
   - Verify proxy service is active

2. **Azure Storage Upload Failed**
   - Verify connection string
   - Check container exists and is accessible

3. **Database Connection Failed**
   - Verify DATABASE_URL
   - Check firewall rules for Azure PostgreSQL

4. **Rate Limiting**
   - Reduce MAX_CONCURRENT_DOWNLOADS
   - Increase delay ranges

### Log Analysis

```bash
# Filter for errors
az containerapp logs show --name thomann-image-downloader --resource-group getyourmusicgear-rg | grep "❌"

# Filter for successful downloads
az containerapp logs show --name thomann-image-downloader --resource-group getyourmusicgear-rg | grep "✅"
```

## Integration with Frontend

The frontend automatically displays images from the `images` column:

```typescript
// Frontend automatically uses the thomann_main image
const productImage = product.images?.thomann_main?.url || defaultImage;
```

## Security Considerations

- **Proxy Authentication**: Stored as Azure Container App secrets
- **Database Access**: Uses connection string with minimal required permissions
- **Storage Access**: Uses connection string with container-level access
- **No Image Processing**: Downloads images as-is without modification

## Future Enhancements

- **Image Optimization**: Compress and resize images for web
- **Multiple Sources**: Download from other affiliate stores
- **Image Validation**: Verify downloaded images are valid
- **Retry Logic**: Automatic retry for failed downloads
- **Batch Processing**: Process images in larger batches

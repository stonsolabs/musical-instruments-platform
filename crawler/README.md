# Simple Product Crawler

A simplified crawler that works with pre-filtered Thomann URLs to crawl products and download images.

## 🚀 Quick Start

### 1. Setup Environment

Copy the environment template and configure your settings:

```bash
cp env.example .env
```

Edit `.env` and set your configuration:
- `IPROYAL_PROXY_URL` - Your iProyal proxy URL (required)
- `DATABASE_URL` - PostgreSQL database connection
- `AZURE_STORAGE_CONNECTION_STRING` - Azure Blob Storage for images

### 2. Test Mode (Recommended First)

Test with just 5 products to make sure everything works:

```bash
export TEST_MODE=true
export MAX_TEST_PRODUCTS=5
python run_simple_crawler.py
```

### 3. Full Crawl

Run the full crawler on all your pre-filtered URLs:

```bash
export TEST_MODE=false
python run_simple_crawler.py
```

## 📁 File Structure

```
crawler/
├── simple_product_crawler.py    # Main crawler logic
├── run_simple_crawler.py        # Runner script
├── database_manager.py          # Database operations
├── image_manager.py             # Image downloading
├── thomann_urls.txt            # Your pre-filtered URLs
├── .env                        # Environment configuration
├── env.example                 # Environment template
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── deploy.sh                   # Azure deployment script
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `IPROYAL_PROXY_URL` | iProyal proxy URL | ✅ |
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `AZURE_STORAGE_CONNECTION_STRING` | Azure Blob Storage | ✅ |
| `TEST_MODE` | Enable test mode (true/false) | ❌ |
| `MAX_TEST_PRODUCTS` | Max products in test mode | ❌ |

### Test Mode

Set these environment variables to test with limited products:

```bash
export TEST_MODE=true
export MAX_TEST_PRODUCTS=5
```

## 🐳 Docker Deployment

### Local Docker

```bash
docker build -t simple-crawler .
docker run --env-file .env simple-crawler
```

### Azure Container Apps

```bash
./deploy.sh
```

## 📊 What It Does

1. **Reads URLs** from `thomann_urls.txt`
2. **Crawls products** from each category URL
3. **Handles pagination** automatically
4. **Downloads images** to Azure Blob Storage
5. **Saves data** to PostgreSQL database
6. **Avoids duplicates** by checking existing products

## 🧪 Testing

Always test with a small number of products first:

```bash
# Test with 5 products
export TEST_MODE=true
export MAX_TEST_PRODUCTS=5
python run_simple_crawler.py

# Test with 10 products
export TEST_MODE=true
export MAX_TEST_PRODUCTS=10
python run_simple_crawler.py
```

## 🔍 Troubleshooting

### Common Issues

1. **Proxy not working**: Check `IPROYAL_PROXY_URL` in `.env`
2. **Database connection failed**: Verify `DATABASE_URL` format
3. **Images not downloading**: Check `AZURE_STORAGE_CONNECTION_STRING`
4. **No products found**: Verify URLs in `thomann_urls.txt`

### Logs

The crawler provides detailed logging:
- ✅ Success messages
- ⚠️ Warnings
- ❌ Errors
- 🧪 Test mode indicators

## 📝 URL Format

Your `thomann_urls.txt` should contain one URL per line:

```
https://www.thomann.co.uk/all-products-from-the-category-electric-guitars.html?marketingAttributes%5B%5D=EXCLUDE_BUNDLE&manufacturer%5B%5D=Fender&gk=GIEG&sp=solr&cme=true&filter=true
https://www.thomann.co.uk/all-products-from-the-category-digital-pianos.html?marketingAttributes%5B%5D=EXCLUDE_BUNDLE&gk=TADP&sp=solr&cme=true&filter=true
```

## 🚀 Production

For production deployment:

1. Set `TEST_MODE=false`
2. Ensure all environment variables are configured
3. Deploy to Azure Container Apps using `./deploy.sh`
4. Monitor logs for any issues

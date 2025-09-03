# Backend Scripts

This directory contains maintenance and utility scripts for the musical instruments platform.

## Organization

### `/maintenance/`
Scripts for ongoing maintenance tasks:
- `deduplicate_images.py` - Remove duplicate product images
- `fix_image_associations.py` - Fix broken image-product associations  
- `cleanup_database.py` - Clean up orphaned records

### `/data/`
Data import and migration scripts:
- `import_products.py` - Import products from external sources
- `migrate_categories.py` - Migrate and merge categories
- `setup_affiliate_stores.py` - Initialize affiliate store data

### `/crawlers/`
Web scraping and data collection:
- `thomann_crawler.py` - Scrape Thomann product data
- `parallel_crawler.py` - Multi-threaded crawling system

### `/monitoring/`
System monitoring and health checks:
- `check_image_status.py` - Verify image availability
- `database_health.py` - Database connection and performance checks

## Usage

All scripts should be run from the backend root directory:

```bash
# From backend/
python -m scripts.maintenance.deduplicate_images
python -m scripts.data.import_products --source thomann
```

## Best Practices

1. **Always test scripts in development first**
2. **Create backups before running destructive operations** 
3. **Use logging instead of print statements**
4. **Include progress indicators for long-running operations**
5. **Handle errors gracefully and provide meaningful messages**
6. **Document script parameters and expected outputs**

## Environment Variables

Scripts may require these environment variables:
- `DATABASE_URL` - Database connection string
- `AZURE_STORAGE_CONNECTION_STRING` - For image operations
- `API_KEY` - For API access if needed

Set these in a `.env` file or export them before running scripts.
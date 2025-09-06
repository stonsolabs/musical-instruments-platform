# Image Management Scripts

This directory contains scripts for managing product images in the musical instruments platform.

## 🚀 Available Scripts

### 1. **Download Missing Images** (`download_missing_images.py`)
Downloads missing images for products that have no images at all.

**What it does:**
- Finds products with `images IS NULL OR images = '{}'`
- Uses proxy to access Thomann website
- Downloads product images
- Updates database with image information

**Setup:**
```bash
# Install dependencies
pip3 install -r requirements.txt

# Configuration is automatically loaded from .env files
# Make sure you have:
# - .env (main configuration)
# - crawler/.env (proxy and storage configuration)

# Run setup
chmod +x setup_proxy.sh
./setup_proxy.sh

# Run the script
python3.11 download_missing_images.py
```

### 2. **Copy Images to Different Container** (`copy_images_to_container.py`)
Copies all images from the database to a different Azure storage container.

**What it does:**
- Reads all image URLs from database
- Copies blobs from source to destination container
- Creates destination container if needed
- Provides detailed progress and results

**Setup:**
```bash
# Configuration is automatically loaded from .env files
# Source account/container come from crawler/.env
# Destination defaults to same account with 'product-images-backup' container

# Run setup
chmod +x setup_copy_container.sh
./setup_copy_container.sh

# Run the script
python3.11 copy_images_to_container.py

# To customize destination:
export DEST_ACCOUNT="your-destination-account"
export DEST_CONTAINER="your-destination-container"
```

## 📊 Current Status Scripts

### 3. **Find Products Needing Redownload** (`find_products_needing_redownload.py`)
Analyzes all products to identify which ones need image attention.

**Categories:**
- No images at all
- Missing thomann_main section
- Empty URLs
- Descriptive URLs that couldn't be fixed

### 4. **Smart Descriptive Fixer** (`smart_descriptive_fixer.py`)
Fixes products with descriptive URLs using brand prefix strategy.

### 5. **Fast Association Fix** (`fast_association_fix.py`)
Fixes ID-based image associations for products with NULL URLs.

## 🔧 Requirements

- Python 3.11+
- Azure CLI (`az`)
- Optional: azcopy for better performance
- Proxy access (for download script)
- Configuration files (`.env` and `crawler/.env`)

## 📁 File Structure

```
maintenance/
├── config.py                       # Configuration loader
├── download_missing_images.py      # Download missing images
├── copy_images_to_container.py     # Copy to different container
├── find_products_needing_redownload.py  # Analyze image status
├── smart_descriptive_fixer.py      # Fix descriptive URLs
├── fast_association_fix.py         # Fix ID-based associations
├── setup_proxy.sh                  # Proxy setup
├── setup_copy_container.sh         # Container copy setup
├── requirements.txt                 # Python dependencies
└── README.md                       # This file
```

## ⚙️ Configuration

The scripts automatically load configuration from:
- **`.env`** (main configuration - database, redis, etc.)
- **`crawler/.env`** (proxy and Azure storage configuration)

**Key Configuration Variables:**
- `DATABASE_URL`: PostgreSQL connection string
- `IPROYAL_PROXY_URL`: Proxy for accessing Thomann
- `AZURE_STORAGE_CONNECTION_STRING`: Azure storage connection
- `AZURE_BLOB_CONTAINER`: Storage container name

**Test Configuration:**
```bash
python3.11 config.py
```

## 🎯 Usage Scenarios

### **Scenario 1: Fresh Start - No Images**
```bash
# 1. Find what needs fixing
python3.11 find_products_needing_redownload.py

# 2. Download missing images
python3.11 download_missing_images.py

# 3. Fix any remaining issues
python3.11 smart_descriptive_fixer.py
```

### **Scenario 2: Backup/Migration**
```bash
# 1. Setup container copy
./setup_copy_container.sh

# 2. Copy all images to backup container
python3.11 copy_images_to_container.py
```

### **Scenario 3: Fix Existing Issues**
```bash
# 1. Analyze current status
python3.11 find_products_needing_redownload.py

# 2. Fix ID-based associations
python3.11 fast_association_fix.py

# 3. Fix descriptive URL issues
python3.11 smart_descriptive_fixer.py
```

## ⚠️ Important Notes

1. **Proxy Required**: The download script requires proxy access to Thomann
2. **Azure Permissions**: Container copy requires proper Azure storage permissions
3. **Rate Limiting**: Scripts include delays to be respectful to external services
4. **Backup**: Always backup your database before running these scripts
5. **Testing**: Test on a small subset first

## 🚨 Troubleshooting

### **Common Issues:**

1. **Proxy Connection Failed**
   - Check proxy URL and credentials
   - Verify proxy is running and accessible

2. **Azure Authentication Failed**
   - Run `az login` to authenticate
   - Check account permissions

3. **Database Connection Failed**
   - Verify DATABASE_URL is correct
   - Check database accessibility

4. **Image Download Failed**
   - Check Thomann website accessibility
   - Verify product URLs are valid

### **Getting Help:**

- Check the log files generated by each script
- Review the JSON results files for detailed error information
- Ensure all environment variables are properly set

## 📈 Progress Tracking

Each script generates:
- **Log files**: Detailed execution logs
- **Results files**: JSON files with operation results
- **Progress indicators**: Real-time progress updates

Use these to track progress and identify any issues during execution.

# Project Files Cleanup Guide

This document identifies files that can be safely removed and documentation that has been consolidated into the main README.

## ✅ Systems to KEEP (Essential for Operations)

**Confirmed by user: These systems are operational and must be preserved:**

### Crawler System - KEEP ALL
- `crawler/` directory - **KEEP EVERYTHING** 
- Purpose: Active product data collection from retailers
- Status: Operational and needed for ongoing data updates

### OpenAI Batch Processing - KEEP ALL  
- `openai/` directory - **KEEP EVERYTHING**
- Purpose: AI content generation using OpenAI batch API
- Status: Operational and actively generates product descriptions

## 🗑️ Files to Remove

### Backend Root Level - DELETE THESE FILES
- `Dockerfile` - Legacy Docker setup, replaced by Azure Functions
- `docker-compose.yml` - Docker Compose configuration, not needed for Azure Functions  
- `docker-compose.dev.yml` - Development Docker setup
- `docker-compose.prod.yml` - Production Docker setup
- `Dockerfile.dev` - Development Docker file
- `render.yaml` - Render.com deployment config (moving to Azure Functions)
- `package.json` - Node.js package file (this is a Python project)

### Backend Scripts & Test Files - DELETE
- `test_product_endpoint.py` - Manual test file, functionality verified
- `check_affiliate_stores.py` - One-time verification script, no longer needed
- `check_table.py` - Database inspection utility, can use database tools
- `create_tables.py` - Manual table creation (using Alembic migrations instead)

### Backend Empty/Unused Directories - DELETE
- `batch_files/` - Empty directory for batch processing files
- `venv/` - Virtual environment (should be in .gitignore)

## 📚 Documentation Consolidation

**All documentation has been merged into comprehensive README.md**

### ✅ Documentation Consolidated
The following content has been integrated into the main `README.md`:
- System architecture overview
- Affiliate system explanation with brand exclusivity
- API documentation with examples
- Azure Functions deployment guide with secrets management
- Database schema documentation  
- Content processing system explanation
- Configuration and environment setup
- Testing and monitoring guidance

### Files No Longer Needed (Content Merged)
Since all content is now in the main README, these files can be removed:
- `README_BATCH_PROCESSING.md` - Content integrated into main README
- Any other standalone documentation files

## 🧹 Frontend Cleanup (Optional)

### Unused Static Images
- `frontend/public/product-images/` - Sample/demo images (~50+ files)
- **Action**: Can be deleted to reduce repository size (~5-10MB)

### Test/Demo Components
- `frontend/src/app/blog-demo/page.tsx` - Demo page
- `frontend/src/app/test-images/` - Test images directory  
- `frontend/src/app/[locale]/test-images/` - Localized test images
- `frontend/src/components/BlogStyleDemo.tsx` - Demo component

## 🚀 Cleanup Commands

### Backend Cleanup
```bash
# Navigate to backend directory
cd backend/

# Delete legacy deployment files
rm -f Dockerfile docker-compose*.yml render.yaml package.json

# Delete test and utility scripts  
rm -f test_product_endpoint.py check_affiliate_stores.py check_table.py create_tables.py

# Delete empty directories
rm -rf batch_files/ venv/

# Delete merged documentation (content now in README.md)
rm -f README_BATCH_PROCESSING.md

echo "Backend cleanup complete!"
```

### Frontend Cleanup (Optional)
```bash
# Navigate to frontend directory  
cd ../frontend/

# Remove sample product images (saves ~5-10MB)
rm -rf public/product-images/

# Remove demo/test files
rm -f src/components/BlogStyleDemo.tsx
rm -f src/components/Untitled.csv
rm -rf src/app/test-images/
rm -rf src/app/[locale]/test-images/  
rm -rf src/app/blog-demo/

echo "Frontend cleanup complete!"
```

## 📊 Estimated Impact

### Space Savings
- Backend cleanup: ~2-3MB (mostly documentation)
- Frontend cleanup: ~5-10MB (sample images)
- **Total savings**: ~7-13MB

### Benefits  
✅ **Cleaner Repository** - Easier navigation and faster clones
✅ **Focused Documentation** - All info in one comprehensive README
✅ **Production Ready** - Only essential files remain
✅ **Better Maintenance** - Clear separation of operational vs legacy code

## 🎯 Final Project Structure

After cleanup, the repository will have this clean structure:

```
musical-instruments-platform/
├── backend/                    # Azure Functions backend
│   ├── app/                   # FastAPI application  
│   ├── alembic/              # Database migrations
│   ├── scripts/              # Operational scripts
│   ├── crawler/              # Data collection system ✅ KEEP
│   ├── openai/               # AI content generation ✅ KEEP  
│   ├── function_app.py       # Azure Functions entry
│   ├── host.json             # Azure Functions config
│   ├── requirements.txt      # Dependencies
│   ├── README.md             # Complete documentation
│   └── AZURE_FUNCTIONS_DEPLOYMENT.md # Deployment guide
├── frontend/                  # Next.js frontend (cleaned)
│   ├── src/                  # Application code
│   ├── public/               # Essential static assets only
│   └── package.json          # Dependencies
└── README.md                 # Main project overview
```

## 🔐 What's Preserved

✅ **All operational systems** - crawler, openai, core backend
✅ **All production code** - app/, alembic/, scripts/
✅ **All deployment configs** - Azure Functions setup
✅ **Complete documentation** - Consolidated in README.md
✅ **All dependencies** - requirements.txt with Azure packages

The cleanup removes only unnecessary files while preserving all functional systems and documentation!
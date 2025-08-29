# Project Files Cleanup Guide

This document identifies files and directories that are no longer necessary and can be safely removed from the Musical Instruments Platform project.

## 🗑️ Safe to Delete - No Longer Needed

### Backend Root Level - DELETE THESE FILES
- `Dockerfile` - Legacy Docker setup, replaced by Azure Functions
- `docker-compose.yml` - Docker Compose configuration, not needed for Azure Functions  
- `docker-compose.dev.yml` - Development Docker setup
- `docker-compose.prod.yml` - Production Docker setup
- `Dockerfile.dev` - Development Docker file
- `render.yaml` - Render.com deployment config (moving to Azure Functions)
- `package.json` - Node.js package file (this is a Python project)

### Backend Scripts & Test Files - REVIEW AND ORGANIZE
- `test_product_endpoint.py` - **DELETE** - Manual test file, functionality verified
- `check_affiliate_stores.py` - **DELETE** - One-time verification script, no longer needed
- `check_table.py` - **DELETE** - Database inspection utility, can use database tools
- `create_tables.py` - **DELETE** - Manual table creation (using Alembic migrations instead)
- `scripts/setup_enhanced_affiliate_stores.py` - **KEEP** - Operational setup script

### Backend Documentation Files - REORGANIZE
**CREATE NEW FOLDER: `docs/`** and move these files:
- `AFFILIATE_SYSTEM_GUIDE.md` - **MOVE to docs/** - System architecture explanation
- `EXCLUSIVE_STORE_FEATURE_EXPLAINED.md` - **MOVE to docs/** - Feature documentation  
- `FINAL_AFFILIATE_SYSTEM_SUMMARY.md` - **MOVE to docs/** - System summary
- `THOMANN_REDIR_INTEGRATION.md` - **MOVE to docs/** - Integration guide
- `README_BATCH_PROCESSING.md` - **MOVE to docs/** - Operational guide
- `AZURE_FUNCTIONS_DEPLOYMENT.md` - **KEEP in root** - Active deployment guide
- `UNUSED_TABLES_AND_COLUMNS.md` - **MOVE to docs/** - Database analysis

### Backend Empty/Unused Directories - DELETE
- `batch_files/` - Empty directory for batch processing files
- `app/utils/` - Empty directory (if confirmed empty)
- `venv/` - Virtual environment (should be in .gitignore)

### Development/Testing Files
- `test_product_endpoint.py` - Manual test file, can be removed after verification
- `check_affiliate_stores.py` - One-time verification script
- `check_table.py` - Database inspection utility
- `create_tables.py` - Manual table creation (using Alembic migrations instead)
- `batch_files/` directory - Empty or test batch processing files

### Legacy Deployment Files
- `../azure-functions-deployment/` - Old Azure deployment attempt (entire directory)
  - Contains legacy functions setup that's superseded by new approach
  - Files: `function.json`, `host.json`, `requirements.txt`, etc.

### Documentation (Consolidate)
Multiple overlapping documentation files can be consolidated:
- `AFFILIATE_SYSTEM_GUIDE.md` - Merge into main README
- `EXCLUSIVE_STORE_FEATURE_EXPLAINED.md` - Merge into main README  
- `FINAL_AFFILIATE_SYSTEM_SUMMARY.md` - Merge into main README
- `THOMANN_REDIR_INTEGRATION.md` - Merge into main README
- `README_BATCH_PROCESSING.md` - Keep (specific operational guide)

## 🧹 Frontend Cleanup

### Unused Static Images
`frontend/public/product-images/` - Large directory of sample product images
- **Size**: ~50+ product image files
- **Status**: These are sample/demo images, not used in production
- **Action**: Can be deleted to reduce repository size

### Development Files
- `frontend/.next/` - Build output (should be in .gitignore)
- `frontend/node_modules/` - Dependencies (should be in .gitignore)
- `frontend/tsconfig.tsbuildinfo` - TypeScript build cache

### Test/Demo Components
- `frontend/src/app/blog-demo/page.tsx` - Demo page
- `frontend/src/app/test-images/` - Test images directory
- `frontend/src/app/[locale]/test-images/` - Localized test images
- `frontend/src/components/BlogStyleDemo.tsx` - Demo component
- `frontend/src/components/Untitled.csv` - Leftover file

## 🔍 Legacy Systems (Consider Removal)

### OpenAI Batch Processing (Keep for now)
`openai/` directory - Batch processing system
- **Status**: Operational and needed for content generation
- **Action**: Keep all files, they're actively used

### Crawler System (Keep for now) 
`crawler/` directory - Product crawling system
- **Status**: Operational for data collection
- **Action**: Keep all files, they're actively used

### Old Migration Attempts
- `../recreate_database.py` - Database recreation script
- `../run_image_update.py` - Image update utility  
- `../scrape_retailer_images.py` - Image scraping utility
- `../test-api-connection.js` - API connection test

## 📊 File Size Analysis

### Large Directories to Clean
1. **Frontend product images**: ~5-10MB of sample images
2. **Documentation files**: Multiple overlapping guides
3. **Docker configurations**: Multiple unused deployment setups

### Estimated Space Savings
- Remove sample product images: ~5-10MB
- Remove Docker files: ~1MB  
- Remove legacy deployment configs: ~2-3MB
- **Total estimated savings**: ~8-15MB

## ✅ Files to Keep (Essential)

### Backend Core
- `app/` - Main application code ✅
- `alembic/` - Database migrations ✅
- `function_app.py` - Azure Functions entry point ✅
- `host.json` - Azure Functions configuration ✅
- `local.settings.json` - Azure Functions local settings ✅
- `requirements.txt` - Python dependencies ✅
- `AZURE_FUNCTIONS_DEPLOYMENT.md` - Deployment guide ✅
- `UNUSED_TABLES_AND_COLUMNS.md` - Database analysis ✅

### Frontend Core
- `src/` - Main application code ✅
- `public/` (core files) - Essential static assets ✅
- `package.json` - Dependencies ✅
- `next.config.js` - Next.js configuration ✅
- `tailwind.config.js` - Styling configuration ✅

### Operational Systems  
- `crawler/` - Product data collection ✅
- `openai/` - AI content generation ✅

## 🚀 Cleanup Action Plan

### Phase 1: Backend File Organization
```bash
# 1. Create docs directory
mkdir docs/

# 2. Move documentation files to docs/
mv AFFILIATE_SYSTEM_GUIDE.md docs/
mv EXCLUSIVE_STORE_FEATURE_EXPLAINED.md docs/
mv FINAL_AFFILIATE_SYSTEM_SUMMARY.md docs/
mv THOMANN_REDIR_INTEGRATION.md docs/
mv README_BATCH_PROCESSING.md docs/
mv UNUSED_TABLES_AND_COLUMNS.md docs/

# 3. Delete unnecessary backend files
rm Dockerfile docker-compose*.yml render.yaml package.json
rm test_product_endpoint.py check_affiliate_stores.py check_table.py create_tables.py
rm -rf batch_files/ venv/

# 4. Check and clean empty directories
rmdir app/utils/ 2>/dev/null || echo "app/utils/ not empty or doesn't exist"
```

### Phase 2: Frontend Cleanup
```bash
# Frontend cleanup  
rm -rf frontend/public/product-images/
rm frontend/src/components/Untitled.csv
rm -rf frontend/src/app/test-images/
rm -rf frontend/src/app/[locale]/test-images/
rm frontend/src/app/blog-demo/page.tsx
rm frontend/src/components/BlogStyleDemo.tsx
```

### Phase 2: Documentation Consolidation
1. Merge affiliate system docs into main README
2. Keep operational guides (batch processing, deployment)
3. Remove redundant documentation files

### Phase 3: Legacy System Review
1. Confirm crawler system is needed long-term
2. Verify OpenAI batch processing usage
3. Remove old deployment configurations

## 🔐 Before Deletion Checklist

- [ ] Confirm no active deployments use Docker configurations
- [ ] Verify frontend doesn't reference sample product images  
- [ ] Check that test scripts aren't needed for operations
- [ ] Backup any configuration that might be referenced later
- [ ] Update .gitignore to prevent similar accumulation

## 📈 Benefits of Cleanup

✅ **Reduced Repository Size** - Faster clones and downloads
✅ **Cleaner Structure** - Easier navigation for developers  
✅ **Less Confusion** - Remove outdated deployment methods
✅ **Improved Performance** - Faster builds without unnecessary files
✅ **Better Maintenance** - Focus on active, relevant code

## 🎯 Post-Cleanup Repository Structure

```
musical-instruments-platform/
├── backend/                          # Azure Functions backend
│   ├── app/                         # FastAPI application  
│   │   ├── api/                     # API endpoints
│   │   ├── services/                # Business logic services
│   │   ├── models.py               # Database models
│   │   ├── main.py                 # FastAPI app
│   │   └── config.py               # Configuration
│   ├── alembic/                     # Database migrations
│   ├── scripts/                     # Operational scripts
│   ├── docs/                        # **NEW** - Documentation folder
│   │   ├── AFFILIATE_SYSTEM_GUIDE.md
│   │   ├── EXCLUSIVE_STORE_FEATURE_EXPLAINED.md
│   │   ├── FINAL_AFFILIATE_SYSTEM_SUMMARY.md  
│   │   ├── THOMANN_REDIR_INTEGRATION.md
│   │   ├── README_BATCH_PROCESSING.md
│   │   └── UNUSED_TABLES_AND_COLUMNS.md
│   ├── function_app.py              # Azure Functions entry point
│   ├── host.json                    # Azure Functions config
│   ├── local.settings.json          # Local Azure Functions settings
│   ├── requirements.txt             # Python dependencies
│   └── AZURE_FUNCTIONS_DEPLOYMENT.md # Deployment guide
├── frontend/                         # Next.js frontend (cleaned)
│   ├── src/                         # Application code
│   ├── public/                      # Essential static assets only
│   └── package.json                 # Dependencies
├── crawler/                          # Data collection system
├── openai/                          # AI content generation
└── README.md                        # Main project documentation
```

## 📋 Summary of Changes

### Files to DELETE (Total: ~15 files)
- 7 Docker/deployment configuration files
- 4 test/check scripts  
- 4 frontend demo/test files
- Empty directories

### Files to ORGANIZE (Total: ~6 files)
- Move 6 documentation files to new `docs/` folder

### Result
- **Cleaner root directory** - Only essential files visible
- **Organized documentation** - All guides in dedicated folder  
- **Reduced repository size** - Remove sample images and unused configs
- **Better maintainability** - Focus on active, production files

This cleanup will result in a more maintainable, focused codebase ready for production deployment on Azure Functions and Vercel.
# Database Cleanup Analysis

## Tables Analysis

### Core Tables (KEEP - Essential for operation)

**Active Production Tables:**
- `products` (2,384 kB) - Main products table with AI-generated content
- `brands` (96 kB) - Product brands
- `categories` (96 kB) - Product categories  
- `affiliate_stores` (80 kB) - Affiliate store configuration
- `product_prices` (48 kB) - Store pricing data
- `brand_exclusivities` (112 kB) - Brand exclusivity rules (e.g., Harley Benton → Thomann)

**Archive Tables (KEEP - User requested):**
- `products_bkp` (5,072 kB) - Backup products table - **KEEP AS REQUESTED**
- `products_filled` (4,016 kB) - Crawler data source - **KEEP AS REQUESTED**

**Configuration Tables (KEEP - System operation):**
- `config_files` (64 kB) - JSON schemas and prompts for OpenAI processing
- `alembic_version` (24 kB) - Database migration tracking

### Tables with Unclear Usage (REVIEW NEEDED)

**Localization System:**
- `locales` (48 kB) - Language/region configuration
- `product_translations` (80 kB) - Product translations (has FK to products)
  - **STATUS**: Currently unused in API, but may be needed for future multi-language features

**Analytics/Tracking:**
- `affiliate_clicks` (56 kB) - Click tracking for affiliate links  
  - **STATUS**: Good for analytics, but not used in current API
- `comparison_views` (40 kB) - Product comparison tracking
  - **STATUS**: Useful for analytics, not used in current API
- `customer_reviews` (40 kB) - User reviews (has FK to products)
  - **STATUS**: Not used in current API, AI content has synthetic reviews

**Crawler System:**
- `crawler_sessions` (32 kB) - Crawler execution tracking
- `crawler_metrics` (32 kB) - Crawler performance metrics  
- `crawler_config` (32 kB) - Crawler configuration
- `crawler_jobs` (24 kB) - Crawler job queue
  - **STATUS**: Used by crawler system, keep for operational monitoring

**OpenAI Batch Processing:**
- `openai_batches` (40 kB) - OpenAI batch job tracking
  - **STATUS**: Used for batch processing monitoring, keep for operations

**Product Enhancement:**
- `product_images` (32 kB) - Product image management (has FK to products)
  - **STATUS**: Used for image processing pipeline

### Potentially Unused Tables (CANDIDATES FOR REMOVAL)

**Store Integration:**
- `product_store_links` (16 kB) - Store-specific product URLs (has FK to products)
- `product_store_availability` (16 kB) - Product availability by store
  - **ISSUE**: These may be redundant with the `store_links` in JSON content and `product_prices` table

## Column Analysis

### Products Table - Column Usage

**Used Columns:**
- `id`, `sku`, `name`, `slug` - Identity fields ✅
- `brand_id`, `category_id` - Relationships ✅  
- `description`, `images`, `msrp_price` - Basic info ✅
- `content` - Rich AI-generated content ✅
- `is_active`, `created_at`, `updated_at` - Status/audit ✅
- `openai_*` fields - Batch processing status ✅

**Potentially Unused Columns in Products:**
- `gtin12`, `gtin13`, `gtin14`, `upc`, `ean`, `mpn`, `isbn` - Product identifiers
  - **STATUS**: Not used in current API, but good for e-commerce integrations
- `avg_rating`, `review_count` - Review aggregates
  - **STATUS**: Used in API but always return 0/null, synthetic reviews in AI content instead
- `category_attributes` - Category-specific attributes  
  - **STATUS**: Not used, specifications in AI content instead
- `last_crawled` - Crawler timestamp
  - **STATUS**: Used by crawler system

### Affiliate Stores - Column Usage

**Used Columns:**
- `id`, `name`, `slug`, `website_url` - Basic store info ✅
- `has_affiliate_program`, `affiliate_*` fields - Affiliate system ✅
- `priority`, `show_affiliate_buttons` - Display control ✅  
- `available_regions`, `regional_priority` - Regional handling ✅
- `is_active`, `created_at`, `updated_at` - Status/audit ✅

**Potentially Unused Columns:**
- `api_endpoint`, `api_key_encrypted` - Direct API integration
  - **STATUS**: Not implemented in current system
- `commission_rate` - Affiliate commission tracking
  - **STATUS**: Used in API response but not functionally used
- `logo_url` - Store logos
  - **STATUS**: Used in API but may not be displayed in frontend

## Recommendations

### Safe to Remove (Low Risk)
- `product_store_links` - Redundant with JSON store_links
- `product_store_availability` - Redundant with product_prices.is_available

### Review with Business Requirements
- `locales`, `product_translations` - Needed if multi-language is planned
- `affiliate_clicks`, `comparison_views` - Good for analytics/tracking  
- `customer_reviews` - May want real reviews vs synthetic AI reviews

### Keep for Operations
- All crawler tables - Needed for monitoring and operations
- `openai_batches` - Needed for batch processing monitoring
- `product_images` - Needed for image processing pipeline

### Column Optimizations
- Consider removing unused product identifier columns if not needed for integrations
- `avg_rating`/`review_count` could be removed if using AI content exclusively
- Some affiliate store columns could be removed if features aren't used

## Total Potential Space Savings
- Remove `product_store_links` + `product_store_availability`: ~32 kB
- Remove unused columns: Minimal space impact
- **Total database size**: ~13 MB, so cleanup impact is minimal

## Next Steps
1. Confirm business requirements for analytics tables
2. Verify if multi-language features are planned  
3. Check if e-commerce product identifiers are needed
4. Test removal of redundant store tables in staging environment
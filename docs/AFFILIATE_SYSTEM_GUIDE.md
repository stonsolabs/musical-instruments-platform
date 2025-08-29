# Affiliate System Guide

This guide explains how to use the enhanced affiliate system that allows you to control which stores show affiliate buttons for specific products.

## Overview

The affiliate system now includes:

1. **Affiliate Store Management** - Configure which stores have affiliate programs
2. **Product-Store Availability** - Control which products show affiliate buttons in which stores
3. **Affiliate Link Generation** - Automatically generate affiliate URLs with proper parameters
4. **Priority System** - Control the order in which stores appear

## Database Schema

### AffiliateStore Table (Enhanced)

New fields added to the `affiliate_stores` table:

- `has_affiliate_program` (boolean) - Whether the store has an affiliate program
- `affiliate_base_url` (text) - Base URL for affiliate links
- `affiliate_id` (string) - Your affiliate ID for this store
- `affiliate_parameters` (JSON) - Additional parameters for affiliate URLs
- `show_affiliate_buttons` (boolean) - Whether to show affiliate buttons globally
- `priority` (integer) - Display priority (higher number = higher priority)

### How It Works

The system automatically decides whether to show affiliate buttons based on:

1. **Store Configuration** - Store has affiliate program enabled and shows affiliate buttons
2. **Product Store Links** - Product has a store link for that specific store
3. **Priority Ordering** - Stores are ordered by priority (higher number = higher priority)

## Setup Instructions

### 1. Run Database Migration

```bash
cd backend
alembic upgrade head
```

### 2. Setup Affiliate Store Configurations

```bash
cd backend
python scripts/setup_affiliate_stores.py
```

This script sets up example configurations for:
- Amazon (affiliate program enabled)
- Thomann (affiliate program enabled)
- Gear4Music (affiliate program enabled)
- Donner (no affiliate program)
- Sweetwater (affiliate program enabled)

### 3. Configure Your Affiliate IDs

Edit the script `scripts/setup_affiliate_stores.py` and replace the placeholder affiliate IDs:

```python
"affiliate_id": "your-actual-amazon-affiliate-id",
"affiliate_parameters": {
    "tag": "your-actual-amazon-tag",
    "ref": "your-actual-amazon-ref"
}
```



## API Endpoints

### Affiliate Stores

- `GET /api/v1/affiliate-stores` - List all affiliate stores
- `GET /api/v1/affiliate-stores/{store_id}` - Get store details
- `PUT /api/v1/affiliate-stores/{store_id}/affiliate-config` - Update affiliate configuration
- `GET /api/v1/affiliate-stores/{store_id}/affiliate-config` - Get affiliate configuration



### Product Affiliate Information

- `GET /api/v1/products/{product_id}/affiliate-stores` - Get all affiliate stores for a product
- `POST /api/v1/products/{product_id}/affiliate-stores` - Get affiliate stores with generated affiliate URLs
- `GET /api/v1/products/{product_id}/affiliate-urls` - Generate affiliate URLs for a product

## Usage Examples

### Frontend Integration Workflow

1. **Send your store links to the API:**
```javascript
const storeLinks = {
    "thomann": {"product_url": "https://www.thomann.de/gb/product/123"},
    "amazon": {"product_url": "https://www.amazon.com/product/456"},
    "gear4music": {"product_url": "https://www.gear4music.com/product/789"}
};

const response = await fetch(`/api/v1/products/${productId}/affiliate-stores`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(storeLinks)
});

const data = await response.json();
```

2. **Use the returned affiliate URLs:**
```javascript
data.affiliate_stores.forEach(store => {
    if (store.affiliate_url) {
        // Use store.affiliate_url for affiliate tracking
        console.log(`${store.name}: ${store.affiliate_url}`);
    } else {
        // Use store.original_url as fallback
        console.log(`${store.name}: ${store.original_url}`);
    }
});
```

### 1. Configure a New Affiliate Store

```python
from app.services.enhanced_affiliate_service import EnhancedAffiliateService

# Update store configuration with domain-specific affiliate IDs
await affiliate_manager.update_store_affiliate_config(
    store_id=1,
    has_affiliate_program=True,
    affiliate_base_url="https://store.com/product/{product_id}",
    affiliate_id="your-default-affiliate-id",
    domain_affiliate_ids={
        "US": "your-us-affiliate-id",
        "UK": "your-uk-affiliate-id",
        "DE": "your-de-affiliate-id"
    },
    affiliate_parameters={"utm_source": "your-site"},
    show_affiliate_buttons=True,
    priority=5
)
```



### 2. Get Affiliate Stores for a Product with URLs

```python
# Get all stores that should show affiliate buttons for a product
affiliate_stores = await affiliate_manager.get_affiliate_stores_for_product(product_id=123)

# With store links filtering and affiliate URL generation
store_links = {
    "thomann": {"product_url": "https://www.thomann.de/gb/product/123"},
    "amazon": {"product_url": "https://www.amazon.com/product/456"}
}
affiliate_stores = await affiliate_manager.get_affiliate_stores_for_product(product_id=123, store_links=store_links)

# Each store will have:
# - original_url: Your original store link
# - affiliate_url: Generated affiliate URL with tracking parameters
```

### 3. Generate Affiliate URL

```python
# Generate affiliate URL for a product in a specific store
affiliate_url = await affiliate_manager.generate_affiliate_url(store, product)

# Special handling for Thomann's RediR™ system
# Thomann uses RediR™ for automatic regional redirects
# See THOMANN_REDIR_INTEGRATION.md for details
```

## Frontend Integration

### Get Affiliate Stores for a Product

```javascript
// Get affiliate stores for a product
const response = await fetch(`/api/v1/products/${productId}/affiliate-stores`);
const data = await response.json();

// Display affiliate buttons
data.affiliate_stores.forEach(store => {
    console.log(`${store.name} - Priority: ${store.priority}`);
});
```

### Get Affiliate URLs

```javascript
// Get affiliate URLs for a product
const response = await fetch(`/api/v1/products/${productId}/affiliate-urls`);
const data = await response.json();

// Use affiliate URLs
data.affiliate_urls.forEach(item => {
    console.log(`${item.store.name}: ${item.affiliate_url}`);
});
```

### Integration with Your Store Links

Since you handle store links on your side, you can:

1. **Get affiliate stores** for a product using the API
2. **Match store slugs** with your existing store links
3. **Generate affiliate URLs** by combining your store links with affiliate parameters

Example:
```javascript
// Get affiliate stores
const affiliateResponse = await fetch(`/api/v1/products/${productId}/affiliate-stores`);
const affiliateData = await affiliateResponse.json();

// Your existing store links
const storeLinks = {
    "thomann": { "product_url": "https://www.thomann.de/gb/product/123" },
    "amazon": { "product_url": "https://www.amazon.com/product/456" }
};

// Combine with affiliate system
affiliateData.affiliate_stores.forEach(store => {
    const storeLink = storeLinks[store.slug];
    if (storeLink && storeLink.product_url) {
        // Add affiliate parameters to your existing URL
        const affiliateUrl = addAffiliateParams(storeLink.product_url, store);
        console.log(`${store.name}: ${affiliateUrl}`);
    }
});
```

## Common Use Cases

### 1. Store Configuration

Configure which stores have affiliate programs and their settings:

1. Set `has_affiliate_program = true` for stores with affiliate programs
2. Set `show_affiliate_buttons = true` to enable affiliate buttons globally
3. Set `priority` values to control display order (higher = first)
4. Configure `domain_affiliate_ids` for stores with different affiliate IDs per region

### 2. Product Store Links

The system automatically checks your product's store links:

1. If product has a store link for a store → show affiliate button
2. If product doesn't have a store link for a store → don't show affiliate button
3. No manual configuration needed per product

### 3. Commission Optimization

For stores with higher commission rates:

1. Set higher `priority` values for stores with better commission rates
2. This will display them first in the affiliate button list

## Best Practices

1. **Always test affiliate links** before going live
2. **Use manual overrides sparingly** - prefer automatic detection when possible
3. **Document override reasons** for future reference
4. **Monitor affiliate performance** and adjust priorities accordingly
5. **Keep affiliate IDs secure** - never commit them to version control

## Troubleshooting

### Affiliate buttons not showing

1. Check if store has `has_affiliate_program = true`
2. Check if store has `show_affiliate_buttons = true`
3. Check if product has `show_affiliate_button = true` for that store
4. Check if product has `is_available = true` for that store

### Affiliate URLs not generating

1. Check if store has `affiliate_base_url` set
2. Check if `affiliate_id` is configured
3. Verify `affiliate_parameters` format

### Performance issues

1. Add database indexes for frequently queried fields
2. Use bulk operations for large datasets
3. Cache affiliate store configurations when possible

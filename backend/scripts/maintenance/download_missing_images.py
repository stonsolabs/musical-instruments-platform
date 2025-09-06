#!/usr/bin/env python3.11
"""
Download Missing Images Script
=============================

This script downloads missing images for products using a proxy.
It starts with products that have no images at all (images IS NULL OR images = '{}').
"""

import asyncio
import asyncpg
import os
import json
import aiohttp
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
import re
from urllib.parse import urljoin, urlparse
import logging

# Import configuration from config module
from config import DATABASE_URL, PROXY_URL, PROXY_USERNAME, PROXY_PASSWORD

# Validate required configuration
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in configuration")
if not PROXY_URL:
    raise ValueError("PROXY_URL not found in configuration")

# Thomann base URL
THOMANN_BASE = "https://www.thomann.co.uk"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'download_missing_images_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def get_products_without_images() -> List[Dict]:
    """Get all products that have no images at all."""
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        rows = await conn.fetch("""
            SELECT id, name, sku 
            FROM products 
            WHERE images IS NULL OR images = '{}'
            ORDER BY id
        """)
        
        products = []
        for row in rows:
            products.append({
                'id': row['id'],
                'name': row['name'],
                'sku': row['sku']
            })
        
        logger.info(f"Found {len(products)} products without images")
        return products
        
    finally:
        await conn.close()

def extract_thomann_url_from_sku(sku: str) -> Optional[str]:
    """Extract Thomann URL from SKU if it's a valid Thomann product."""
    
    # Check if SKU looks like a Thomann product
    if not sku or not isinstance(sku, str):
        return None
    
    # Common patterns for Thomann URLs
    if sku.endswith('.htm') or sku.endswith('.html'):
        # Direct Thomann URL
        if 'thomann.co.uk' in sku:
            return sku
        elif sku.startswith('http'):
            return sku
    
    # Try to construct Thomann URL from SKU
    if '_' in sku and sku.endswith('.htm'):
        # Convert underscores to hyphens and construct URL
        product_path = sku.replace('_', '-')
        return urljoin(THOMANN_BASE, product_path)
    
    return None

async def get_product_image_url(session: aiohttp.ClientSession, product: Dict) -> Optional[str]:
    """Get the main product image URL from Thomann."""
    
    sku = product['sku']
    name = product['name']
    
    # Try to get URL from SKU first
    thomann_url = extract_thomann_url_from_sku(sku)
    
    if not thomann_url:
        logger.warning(f"Could not extract Thomann URL from SKU: {sku}")
        return None
    
    try:
        # Configure proxy if credentials are provided
        proxy_auth = None
        if PROXY_USERNAME and PROXY_PASSWORD:
            proxy_auth = aiohttp.BasicAuth(PROXY_USERNAME, PROXY_PASSWORD)
        
        # Make request through proxy
        async with session.get(
            thomann_url,
            proxy=PROXY_URL,
            proxy_auth=proxy_auth,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            
            if response.status != 200:
                logger.warning(f"Failed to fetch {thomann_url}: {response.status}")
                return None
            
            html_content = await response.text()
            
            # Look for main product image
            # Common patterns for Thomann product images
            image_patterns = [
                r'<img[^>]*class="[^"]*product-image[^"]*"[^>]*src="([^"]+)"',
                r'<img[^>]*class="[^"]*main-image[^"]*"[^>]*src="([^"]+)"',
                r'<img[^>]*id="[^"]*main-image[^"]*"[^>]*src="([^"]+)"',
                r'<img[^>]*data-src="([^"]+)"[^>]*class="[^"]*lazy[^"]*"',
                r'<img[^>]*src="([^"]*product[^"]*\.jpg[^"]*)"',
                r'<img[^>]*src="([^"]*thomann[^"]*\.jpg[^"]*)"'
            ]
            
            for pattern in image_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                if matches:
                    image_url = matches[0]
                    if not image_url.startswith('http'):
                        image_url = urljoin(THOMANN_BASE, image_url)
                    logger.info(f"Found image for {name}: {image_url}")
                    return image_url
            
            logger.warning(f"No image found for {name} at {thomann_url}")
            return None
            
    except Exception as e:
        logger.error(f"Error fetching {thomann_url}: {e}")
        return None

async def download_image(session: aiohttp.ClientSession, image_url: str, product_id: int) -> Optional[str]:
    """Download image and save to local storage."""
    
    try:
        # Configure proxy if credentials are provided
        proxy_auth = None
        if PROXY_USERNAME and PROXY_PASSWORD:
            proxy_auth = aiohttp.BasicAuth(PROXY_USERNAME, PROXY_PASSWORD)
        
        async with session.get(
            image_url,
            proxy=PROXY_URL,
            proxy_auth=proxy_auth,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            timeout=aiohttp.ClientTimeout(total=60)
        ) as response:
            
            if response.status != 200:
                logger.warning(f"Failed to download image {image_url}: {response.status}")
                return None
            
            # Create local storage directory
            local_dir = f"downloaded_images/{product_id}"
            os.makedirs(local_dir, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{product_id}_{timestamp}.jpg"
            filepath = os.path.join(local_dir, filename)
            
            # Save image
            with open(filepath, 'wb') as f:
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded image for product {product_id}: {filepath}")
            return filepath
            
    except Exception as e:
        logger.error(f"Error downloading image for product {product_id}: {e}")
        return None

async def update_product_images(product_id: int, image_url: str, local_path: str) -> bool:
    """Update product images in database."""
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Create images structure
        images = {
            'thomann_main': {
                'url': image_url,
                'type': 'main',
                'source': 'thomann',
                'source_url': '',  # Will be populated later
                'downloaded_at': datetime.now().isoformat(),
                'local_path': local_path
            }
        }
        
        # Update database
        await conn.execute("""
            UPDATE products SET images = $1 WHERE id = $2
        """, json.dumps(images), product_id)
        
        logger.info(f"Updated product {product_id} with image data")
        return True
        
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        return False
    finally:
        await conn.close()

async def process_single_product(session: aiohttp.ClientSession, product: Dict) -> Dict:
    """Process a single product to download its image."""
    
    product_id = product['id']
    name = product['name']
    sku = product['sku']
    
    logger.info(f"Processing product {product_id}: {name}")
    
    try:
        # Get image URL from Thomann
        image_url = await get_product_image_url(session, product)
        
        if not image_url:
            return {
                'id': product_id,
                'name': name,
                'status': 'no_image_found',
                'error': 'Could not find image URL'
            }
        
        # Download image
        local_path = await download_image(session, image_url, product_id)
        
        if not local_path:
            return {
                'id': product_id,
                'name': name,
                'status': 'download_failed',
                'error': 'Failed to download image'
            }
        
        # Update database
        success = await update_product_images(product_id, image_url, local_path)
        
        if success:
            return {
                'id': product_id,
                'name': name,
                'status': 'success',
                'image_url': image_url,
                'local_path': local_path
            }
        else:
            return {
                'id': product_id,
                'name': name,
                'status': 'update_failed',
                'error': 'Failed to update database'
            }
            
    except Exception as e:
        logger.error(f"Error processing product {product_id}: {e}")
        return {
            'id': product_id,
            'name': name,
            'status': 'error',
            'error': str(e)
        }

async def main():
    """Main function."""
    
    if not DATABASE_URL:
        logger.error("DATABASE_URL environment variable not set")
        return
    
    logger.info("🚀 STARTING MISSING IMAGE DOWNLOAD")
    logger.info(f"Using proxy: {PROXY_URL}")
    
    try:
        # Get products without images
        products = await get_products_without_images()
        
        if not products:
            logger.info("✅ No products found without images!")
            return
        
        # Create aiohttp session with proxy support
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        timeout = aiohttp.ClientTimeout(total=60)
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        ) as session:
            
            # Process products
            results = []
            total = len(products)
            
            for i, product in enumerate(products):
                logger.info(f"📊 Progress: {i+1}/{total} ({((i+1)/total)*100:.1f}%)")
                
                result = await process_single_product(session, product)
                results.append(result)
                
                # Small delay to be respectful to Thomann
                await asyncio.sleep(1)
            
            # Analyze results
            successful = sum(1 for r in results if r['status'] == 'success')
            no_image = sum(1 for r in results if r['status'] == 'no_image_found')
            download_failed = sum(1 for r in results if r['status'] == 'download_failed')
            update_failed = sum(1 for r in results if r['status'] == 'update_failed')
            errors = sum(1 for r in results if r['status'] == 'error')
            
            logger.info(f"\n📊 FINAL RESULTS:")
            logger.info(f"✅ Successful: {successful}")
            logger.info(f"❌ No image found: {no_image}")
            logger.info(f"💥 Download failed: {download_failed}")
            logger.info(f"💥 Update failed: {update_failed}")
            logger.info(f"💥 Errors: {errors}")
            logger.info(f"📋 Total processed: {total}")
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"download_results_{timestamp}.json"
            
            with open(results_file, 'w') as f:
                json.dump({
                    'timestamp': timestamp,
                    'summary': {
                        'total': total,
                        'successful': successful,
                        'no_image_found': no_image,
                        'download_failed': download_failed,
                        'update_failed': update_failed,
                        'errors': errors
                    },
                    'results': results
                }, f, indent=2)
            
            logger.info(f"📄 Results saved: {results_file}")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

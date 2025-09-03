#!/usr/bin/env python3.11
"""
Smart Descriptive URL Fixer
===========================

This script fixes descriptive URLs using a smart brand prefix strategy
to get around Azure CLI pagination limits.
"""

import asyncio
import asyncpg
import os
import re
import json
import subprocess
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')

async def get_products_with_descriptive_urls() -> List[Dict]:
    """Get all products that have descriptive URLs (not ID-based) in thomann_main images."""
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Get all products with thomann_main images
        rows = await conn.fetch("""
            SELECT id, name, sku, images
            FROM products 
            WHERE images -> 'thomann_main' ->> 'url' IS NOT NULL
            AND images -> 'thomann_main' ->> 'url' != ''
        """)
        
        descriptive_products = []
        
        for row in rows:
            try:
                images = row['images']
                if isinstance(images, str):
                    images = json.loads(images)
                
                thomann_main = images.get('thomann_main', {})
                url = thomann_main.get('url', '')
                
                if not url:
                    continue
                
                # Extract blob name from URL
                blob_name = url.split('/')[-1]
                
                # Check if it's ID-based (starts with number_)
                if re.match(r'^\d+_', blob_name):
                    # This is ID-based, skip it
                    continue
                else:
                    # This is descriptive, include it
                    descriptive_part = blob_name.split('_')[0]
                    brand = descriptive_part.split('-')[0] if '-' in descriptive_part else descriptive_part
                    
                    descriptive_products.append({
                        'id': row['id'],
                        'name': row['name'],
                        'sku': row['sku'],
                        'url': url,
                        'blob_name': blob_name,
                        'descriptive_part': descriptive_part,
                        'brand': brand
                    })
                    
            except Exception as e:
                print(f"❌ Error processing product {row['id']}: {e}")
                continue
        
        return descriptive_products
        
    finally:
        await conn.close()

def get_blobs_by_brand_prefix(brand: str) -> Dict[str, str]:
    """Get blobs for a specific brand prefix."""
    
    try:
        result = subprocess.run([
            'az', 'storage', 'blob', 'list',
            '--container-name', 'product-images',
            '--account-name', 'getyourmusicgear',
            '--prefix', f'thomann/{brand}',
            '--query', '[].name',
            '--output', 'json'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            print(f"   ❌ Error fetching {brand}: {result.stderr}")
            return {}
        
        blobs = json.loads(result.stdout)
        blob_dict = {}
        
        for blob_name in blobs:
            blob_dict[blob_name] = f"https://getyourmusicgear.blob.core.windows.net/product-images/{blob_name}"
        
        return blob_dict
        
    except Exception as e:
        print(f"   ❌ Exception fetching {brand}: {e}")
        return {}

def find_best_matching_blob(product: Dict, brand_blobs: Dict[str, str]) -> Optional[Dict]:
    """Find the best matching blob for a product with descriptive URL."""
    
    product_id = product['id']
    descriptive_part = product['descriptive_part']
    current_blob_name = product['blob_name']
    
    # Strategy 1: Check if the current descriptive blob exists
    if current_blob_name in brand_blobs:
        # Current blob exists, but check if there's a better timestamp
        matching_descriptive = []
        for blob_name, url in brand_blobs.items():
            if blob_name.startswith(f"thomann/{descriptive_part}_"):
                matching_descriptive.append((blob_name, url))
        
        if matching_descriptive:
            # Find the most recent timestamp
            best_match = max(matching_descriptive, key=lambda x: x[0])
            return {
                'type': 'descriptive_timestamp_fix',
                'old_url': product['url'],
                'new_url': best_match[1],
                'old_blob': current_blob_name,
                'new_blob': best_match[0]
            }
    
    # Strategy 2: Look for ID-based blob
    id_based_blobs = []
    for blob_name, url in brand_blobs.items():
        if blob_name.startswith(f"thomann/{product_id}_"):
            id_based_blobs.append((blob_name, url))
    
    if id_based_blobs:
        # Find the most recent timestamp
        best_match = max(id_based_blobs, key=lambda x: x[0])
        return {
            'type': 'switch_to_id_based',
            'old_url': product['url'],
            'new_url': best_match[1],
            'old_blob': current_blob_name,
            'new_blob': best_match[0]
        }
    
    # Strategy 3: Look for similar descriptive blobs (fuzzy matching)
    similar_descriptive = []
    for blob_name, url in brand_blobs.items():
        if blob_name.startswith(f"thomann/{descriptive_part}"):
            similar_descriptive.append((blob_name, url))
    
    if similar_descriptive:
        # Find the most recent timestamp
        best_match = max(similar_descriptive, key=lambda x: x[0])
        return {
            'type': 'similar_descriptive_fix',
            'old_url': product['url'],
            'new_url': best_match[1],
            'old_blob': current_blob_name,
            'new_blob': best_match[0]
        }
    
    # No match found
    return None

async def update_product_image(product_id: int, new_url: str, fix_type: str) -> bool:
    """Update a single product's image URL."""
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Get current images
        row = await conn.fetchrow("""
            SELECT images FROM products WHERE id = $1
        """, product_id)
        
        if not row:
            return False
        
        images = row['images']
        if isinstance(images, str):
            images = json.loads(images)
        
        # Update thomann_main URL
        if 'thomann_main' not in images:
            images['thomann_main'] = {}
        
        # Extract timestamp from new URL for downloaded_at
        blob_name = new_url.split('/')[-1]
        timestamp_match = re.search(r'_(\d{8}_\d{6})\.jpg$', blob_name)
        if timestamp_match:
            timestamp_str = timestamp_match.group(1)
            downloaded_at = f"2025-{timestamp_str[:2]}-{timestamp_str[2:4]}T{timestamp_str[4:6]}:{timestamp_str[6:8]}:{timestamp_str[8:10]}.{timestamp_str[10:12]}{timestamp_str[12:14]}"
        else:
            downloaded_at = datetime.now().isoformat()
        
        images['thomann_main'].update({
            'url': new_url,
            'type': 'main',
            'source': 'thomann',
            'source_url': images['thomann_main'].get('source_url', ''),
            'downloaded_at': downloaded_at
        })
        
        # Update database
        await conn.execute("""
            UPDATE products SET images = $1 WHERE id = $2
        """, json.dumps(images), product_id)
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating product {product_id}: {e}")
        return False
    finally:
        await conn.close()

async def fix_all_descriptive_products():
    """Fix all products with descriptive URLs using smart brand prefix strategy."""
    
    print("🚀 SMART DESCRIPTIVE URL FIXER")
    print("=" * 60)
    
    # Get all products with descriptive URLs
    print("🔍 Finding products with descriptive URLs...")
    descriptive_products = await get_products_with_descriptive_urls()
    
    if not descriptive_products:
        print("✅ No products with descriptive URLs found!")
        return
    
    print(f"📊 Found {len(descriptive_products)} products with descriptive URLs")
    
    # Group products by brand
    brand_groups = defaultdict(list)
    for product in descriptive_products:
        brand_groups[product['brand']].append(product)
    
    print(f"🏷️  Grouped into {len(brand_groups)} brand categories")
    
    # Process each brand
    total_fixed = 0
    total_no_match = 0
    total_failed = 0
    
    for brand, products in brand_groups.items():
        print(f"\n🔍 Processing brand: {brand} ({len(products)} products)")
        
        # Get blobs for this brand
        brand_blobs = get_blobs_by_brand_prefix(brand)
        print(f"   📦 Found {len(brand_blobs)} blobs for {brand}")
        
        if not brand_blobs:
            print(f"   ⚠️  No blobs found for {brand}, skipping...")
            total_no_match += len(products)
            continue
        
        # Process each product in this brand
        brand_fixed = 0
        brand_no_match = 0
        
        for product in products:
            try:
                match = find_best_matching_blob(product, brand_blobs)
                
                if not match:
                    brand_no_match += 1
                    continue
                
                # Update the product
                success = await update_product_image(
                    product['id'], 
                    match['new_url'], 
                    match['type']
                )
                
                if success:
                    brand_fixed += 1
                    print(f"   ✅ Fixed ID {product['id']}: {product['name']}")
                    print(f"      {match['old_blob']} → {match['new_blob']}")
                else:
                    total_failed += 1
                    
            except Exception as e:
                print(f"   ❌ Error processing product {product['id']}: {e}")
                total_failed += 1
        
        total_fixed += brand_fixed
        total_no_match += brand_no_match
        
        print(f"   📊 {brand}: {brand_fixed} fixed, {brand_no_match} no match")
    
    # Final results
    print(f"\n📊 FINAL RESULTS:")
    print("=" * 60)
    print(f"✅ Fixed: {total_fixed}")
    print(f"❌ No match found: {total_no_match}")
    print(f"💥 Failed: {total_failed}")
    print(f"📋 Total processed: {len(descriptive_products)}")
    
    # Save detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"smart_descriptive_fix_{timestamp}.json"
    
    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'summary': {
                'total_processed': len(descriptive_products),
                'fixed': total_fixed,
                'no_match_found': total_no_match,
                'failed': total_failed
            },
            'brand_groups': {brand: len(products) for brand, products in brand_groups.items()}
        }, f, indent=2)
    
    print(f"📄 Detailed report saved: {report_file}")
    
    if total_fixed > 0:
        print(f"\n🎉 Successfully fixed {total_fixed} products!")
    
    if total_no_match > 0:
        print(f"\n⚠️  {total_no_match} products still need manual review")

async def main():
    """Main function."""
    if not DATABASE_URL:
        print("❌ DATABASE_URL environment variable not set")
        return
    
    try:
        await fix_all_descriptive_products()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3.11
"""
Find Remaining Descriptive URLs
===============================

This script finds all products that still have descriptive URLs in their thomann_main images,
filtering out the ones that already have ID-based URLs (like 123_20250902_123456.jpg).

The goal is to identify products that might still have naming convention mismatches.
"""

import asyncio
import asyncpg
import os
import re
import json
from datetime import datetime
from typing import List, Dict, Tuple

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
                    descriptive_products.append({
                        'id': row['id'],
                        'name': row['name'],
                        'sku': row['sku'],
                        'url': url,
                        'blob_name': blob_name
                    })
                    
            except Exception as e:
                print(f"❌ Error processing product {row['id']}: {e}")
                continue
        
        return descriptive_products
        
    finally:
        await conn.close()

async def analyze_descriptive_urls():
    """Analyze all descriptive URLs to understand the current state."""
    
    print("🔍 FINDING REMAINING DESCRIPTIVE URLS")
    print("=" * 50)
    
    # Get products with descriptive URLs
    descriptive_products = await get_products_with_descriptive_urls()
    
    print(f"📊 Found {len(descriptive_products)} products with descriptive URLs")
    
    if not descriptive_products:
        print("✅ All products already have ID-based URLs!")
        return
    
    # Group by descriptive prefix
    prefix_groups = {}
    for product in descriptive_products:
        blob_name = product['blob_name']
        # Extract descriptive part (before timestamp)
        descriptive_part = blob_name.split('_')[0]
        
        if descriptive_part not in prefix_groups:
            prefix_groups[descriptive_part] = []
        
        prefix_groups[descriptive_part].append(product)
    
    # Show summary by prefix
    print(f"\n📋 Grouped by descriptive prefix:")
    print("-" * 50)
    
    for prefix, products in sorted(prefix_groups.items()):
        print(f"🔸 {prefix}: {len(products)} products")
    
    # Show some examples
    print(f"\n📝 Examples of descriptive URLs:")
    print("-" * 50)
    
    for i, product in enumerate(descriptive_products[:10]):
        print(f"  {i+1}. ID {product['id']}: {product['name']}")
        print(f"     URL: {product['url']}")
        print(f"     Blob: {product['blob_name']}")
        print()
    
    if len(descriptive_products) > 10:
        print(f"  ... and {len(descriptive_products) - 10} more")
    
    # Save detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"remaining_descriptive_urls_{timestamp}.json"
    
    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'total_count': len(descriptive_products),
            'prefix_groups': prefix_groups,
            'products': descriptive_products
        }, f, indent=2)
    
    print(f"📄 Detailed report saved: {report_file}")
    
    # Show potential next steps
    print(f"\n🚀 NEXT STEPS:")
    print("-" * 50)
    print(f"1. Check if these descriptive blobs exist in Azure storage")
    print(f"2. Find matching ID-based blobs for these products")
    print(f"3. Update database to use correct blob URLs")
    print(f"4. Consider running a comprehensive fix for these remaining cases")

async def main():
    """Main function."""
    if not DATABASE_URL:
        print("❌ DATABASE_URL environment variable not set")
        return
    
    try:
        await analyze_descriptive_urls()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

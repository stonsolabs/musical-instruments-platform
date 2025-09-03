#!/usr/bin/env python3.11
"""
Find Products Needing Image Redownload
=====================================

This script identifies all products that need images to be redownloaded:
1. Products with no images at all
2. Products with broken image links
3. Products with missing thomann_main images
4. Products that still have descriptive URLs that couldn't be fixed
"""

import asyncio
import asyncpg
import os
import re
import json
import subprocess
from datetime import datetime
from typing import List, Dict, Tuple
from collections import defaultdict

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')

async def get_products_needing_redownload() -> Dict[str, List[Dict]]:
    """Get all products that need images to be redownloaded."""
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Get all products
        rows = await conn.fetch("""
            SELECT id, name, sku, images
            FROM products 
            ORDER BY id
        """)
        
        categories = {
            'no_images': [],
            'missing_thomann_main': [],
            'broken_links': [],
            'descriptive_urls_unfixed': [],
            'empty_urls': []
        }
        
        for row in rows:
            product_id = row['id']
            name = row['name']
            sku = row['sku']
            images = row['images']
            
            # Parse images if it's a string
            if isinstance(images, str):
                try:
                    images = json.loads(images)
                except:
                    images = {}
            
            # Category 1: No images at all
            if not images or images == {}:
                categories['no_images'].append({
                    'id': product_id,
                    'name': name,
                    'sku': sku,
                    'issue': 'No images column data'
                })
                continue
            
            # Category 2: Missing thomann_main
            if 'thomann_main' not in images:
                categories['missing_thomann_main'].append({
                    'id': product_id,
                    'name': name,
                    'sku': sku,
                    'issue': 'Missing thomann_main section'
                })
                continue
            
            thomann_main = images['thomann_main']
            
            # Category 3: Empty or null URL
            url = thomann_main.get('url', '')
            if not url or url == '' or url == 'null':
                categories['empty_urls'].append({
                    'id': product_id,
                    'name': name,
                    'sku': sku,
                    'issue': 'Empty or null URL'
                })
                continue
            
            # Category 4: Still has descriptive URL (couldn't be fixed)
            blob_name = url.split('/')[-1]
            if not re.match(r'^\d+_', blob_name):
                categories['descriptive_urls_unfixed'].append({
                    'id': product_id,
                    'name': name,
                    'sku': sku,
                    'issue': f'Still has descriptive URL: {blob_name}',
                    'url': url
                })
        
        return categories
        
    finally:
        await conn.close()

def check_azure_blob_exists(blob_name: str) -> bool:
    """Check if a specific blob exists in Azure storage."""
    
    try:
        result = subprocess.run([
            'az', 'storage', 'blob', 'exists',
            '--container-name', 'product-images',
            '--account-name', 'getyourmusicgear',
            '--name', f'thomann/{blob_name}',
            '--query', 'exists',
            '--output', 'tsv'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip().lower() == 'true'
        return False
        
    except Exception:
        return False

async def analyze_broken_links(products_with_urls: List[Dict]) -> List[Dict]:
    """Analyze products with URLs to find broken links."""
    
    broken_links = []
    total = len(products_with_urls)
    
    print(f"🔍 Checking {total} products with URLs for broken links...")
    
    for i, product in enumerate(products_with_urls):
        if i % 100 == 0:
            print(f"   📊 Progress: {i}/{total} ({i/total*100:.1f}%)")
        
        url = product['url']
        blob_name = url.split('/')[-1]
        
        # Check if blob exists in Azure
        if not check_azure_blob_exists(blob_name):
            broken_links.append({
                'id': product['id'],
                'name': product['name'],
                'sku': product['sku'],
                'issue': f'Blob not found in Azure: {blob_name}',
                'url': url
            })
    
    return broken_links

async def main():
    """Main function."""
    if not DATABASE_URL:
        print("❌ DATABASE_URL environment variable not set")
        return
    
    print("🔍 FINDING PRODUCTS NEEDING IMAGE REDOWNLOAD")
    print("=" * 60)
    
    try:
        # Get all products needing redownload
        categories = await get_products_needing_redownload()
        
        # Show summary
        total_products = sum(len(products) for products in categories.values())
        print(f"📊 Found {total_products} products needing attention:")
        print()
        
        for category, products in categories.items():
            print(f"🔸 {category.replace('_', ' ').title()}: {len(products)} products")
        
        print()
        
        # Show details for each category
        for category, products in categories.items():
            if not products:
                continue
                
            print(f"📋 {category.replace('_', ' ').title()}:")
            print("-" * 50)
            
            # Show first 10 examples
            for i, product in enumerate(products[:10]):
                print(f"  {i+1}. ID {product['id']}: {product['name']}")
                if 'issue' in product:
                    print(f"     Issue: {product['issue']}")
                if 'url' in product:
                    print(f"     URL: {product['url']}")
                print()
            
            if len(products) > 10:
                print(f"  ... and {len(products) - 10} more")
            
            print()
        
        # Check for broken links in products with URLs
        if categories['descriptive_urls_unfixed']:
            print("🔍 Checking for broken links in unfixed descriptive URLs...")
            broken_links = await analyze_broken_links(categories['descriptive_urls_unfixed'])
            
            if broken_links:
                print(f"❌ Found {len(broken_links)} broken links:")
                for product in broken_links[:5]:
                    print(f"  - ID {product['id']}: {product['name']}")
                    print(f"    Issue: {product['issue']}")
                if len(broken_links) > 5:
                    print(f"  ... and {len(broken_links) - 5} more")
            else:
                print("✅ All URLs appear to be valid (blobs exist in Azure)")
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"products_needing_redownload_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'summary': {
                    'total_products': total_products,
                    'categories': {cat: len(products) for cat, products in categories.items()}
                },
                'categories': categories
            }, f, indent=2)
        
        print(f"📄 Detailed report saved: {report_file}")
        
        # Show next steps
        print(f"\n🚀 NEXT STEPS:")
        print("-" * 60)
        print(f"1. **No Images**: {len(categories['no_images'])} products need complete image download")
        print(f"2. **Missing thomann_main**: {len(categories['missing_thomann_main'])} products need image structure")
        print(f"3. **Empty URLs**: {len(categories['empty_urls'])} products need URL population")
        print(f"4. **Descriptive URLs Unfixed**: {len(categories['descriptive_urls_unfixed'])} products need manual review")
        
        if total_products > 0:
            print(f"\n💡 Recommendation: Start with the {len(categories['no_images'])} products that have no images at all")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

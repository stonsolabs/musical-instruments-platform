#!/usr/bin/env python3

import asyncio
import asyncpg
import os
import json
import subprocess
import re
from dotenv import load_dotenv

load_dotenv()

async def check_products_with_broken_image_links():
    """Check products that have image URLs in DB but files don't exist in blob storage"""
    
    # Connect to database
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    print("🔍 Loading existing blob files from Azure storage...")
    
    # Get all blob files from Azure storage
    try:
        result = subprocess.run([
            'az', 'storage', 'blob', 'list',
            '--container-name', 'product-images',
            '--account-name', 'getyourmusicgear',
            '--query', '[].name',
            '--output', 'json'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            print(f"❌ Error loading blob storage: {result.stderr}")
            return
            
        blob_names = json.loads(result.stdout)
        existing_blobs = set(blob_names)
        print(f"✅ Found {len(existing_blobs)} total blobs in storage")
        
    except Exception as e:
        print(f"❌ Error loading blob storage: {e}")
        return
    
    print("\n🔍 Checking products with image URLs in database...")
    
    # Query products that have images in DB
    query = """
        SELECT p.id, p.name, p.images
        FROM products p
        WHERE p.images IS NOT NULL 
        AND p.images != '{}' 
        AND p.images != 'null'
        AND jsonb_typeof(p.images) = 'object'
        AND p.content->>'store_links' IS NOT NULL
        AND p.content->'store_links'->>'Thomann' IS NOT NULL
        ORDER BY p.id
    """
    
    products_with_images = await conn.fetch(query)
    print(f"📊 Found {len(products_with_images)} products with image records in DB")
    
    broken_links = []
    valid_links = []
    
    for product in products_with_images:
        images = product['images']
        if isinstance(images, str):
            try:
                images = json.loads(images)
            except:
                continue
                
        if not isinstance(images, dict):
            continue
            
        # Check if the image URL points to an existing blob
        thomann_main = images.get('thomann_main')
        if thomann_main:
            # Handle case where thomann_main might be a dict or string
            image_url = thomann_main
            if isinstance(thomann_main, dict):
                image_url = thomann_main.get('url', '')
            
            if isinstance(image_url, str) and image_url:
                # Extract blob name from URL
                # URL format: https://getyourmusicgear.blob.core.windows.net/product-images/thomann/1234_timestamp.jpg
                match = re.search(r'/product-images/(.+)$', image_url)
                if match:
                    blob_name = match.group(1)
                    if blob_name in existing_blobs:
                        valid_links.append({
                            'id': product['id'],
                            'name': product['name'],
                            'blob_name': blob_name
                        })
                    else:
                        broken_links.append({
                            'id': product['id'],
                            'name': product['name'],
                            'url': image_url,
                            'expected_blob': blob_name
                        })
    
    print(f"\n📊 IMAGE LINK ANALYSIS:")
    print(f"✅ Valid image links: {len(valid_links)}")
    print(f"❌ Broken image links: {len(broken_links)}")
    print(f"📊 Link accuracy: {(len(valid_links)/(len(valid_links)+len(broken_links)))*100:.1f}%")
    
    if broken_links:
        print(f"\n❌ PRODUCTS WITH BROKEN IMAGE LINKS (Sample):")
        for i, item in enumerate(broken_links[:10], 1):
            print(f"  {i}. ID {item['id']}: {item['name'][:50]}...")
            print(f"     Expected: {item['expected_blob']}")
            
        # Check if there are similar blobs for these products
        print(f"\n🔍 Checking for alternative blobs for broken links...")
        fixed_count = 0
        for item in broken_links[:5]:
            product_id = item['id']
            # Look for any blob with this product ID
            matching_blobs = [blob for blob in existing_blobs if blob.startswith(f'thomann/{product_id}_')]
            if matching_blobs:
                print(f"  ✅ Product {product_id} has alternative blob: {matching_blobs[0]}")
                fixed_count += 1
            else:
                print(f"  ❌ Product {product_id} has NO blob files")
                
        print(f"\n📊 RECOVERY POTENTIAL:")
        print(f"🔧 Can be fixed with URL updates: {fixed_count}/5 sampled")
        print(f"📷 Need new image downloads: {5-fixed_count}/5 sampled")
    
    print(f"\n🎯 PRODUCTS THAT ACTUALLY NEED NEW IMAGES:")
    print(f"   📷 Products with broken links + no blob files: ~{len(broken_links) - len(valid_links)}")
    print(f"   📷 Products with no image records: 52 (from previous analysis)")
    print(f"   🎯 Total needing crawler processing: ~{(len(broken_links) - len(valid_links)) + 52}")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check_products_with_broken_image_links())

#!/usr/bin/env python3

import asyncio
import asyncpg
import os
import json
import subprocess
import re
from dotenv import load_dotenv

load_dotenv()

async def identify_all_products_needing_images():
    """Identify ALL products that need image processing"""
    
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
        
        blob_names = json.loads(result.stdout)
        existing_blobs = set(blob_names)
        print(f"✅ Found {len(existing_blobs)} total blobs in storage")
        
    except Exception as e:
        print(f"❌ Error loading blob storage: {e}")
        return
    
    # Get products with Thomann links
    print("\n🔍 Analyzing ALL products with Thomann links...")
    
    query = """
        SELECT p.id, p.name, p.images, p.content->'store_links'->>'Thomann' as thomann_url
        FROM products p
        WHERE p.content->>'store_links' IS NOT NULL
        AND p.content->'store_links'->>'Thomann' IS NOT NULL
        ORDER BY p.id
    """
    
    all_products = await conn.fetch(query)
    print(f"📊 Found {len(all_products)} products with Thomann URLs")
    
    # Categorize products
    categories = {
        'no_images_in_db': [],      # No images field in DB
        'broken_image_links': [],   # Images in DB but files don't exist in blob
        'valid_images': [],         # Images in DB and files exist in blob
        'need_processing': []       # Combined: no_images_in_db + broken_image_links
    }
    
    for product in all_products:
        product_id = product['id']
        images = product['images']
        
        # Check if product has no images in DB
        if (images is None or 
            images == '{}' or 
            images == 'null' or 
            (isinstance(images, dict) and not images) or
            (isinstance(images, dict) and not images.get('thomann_main'))):
            
            categories['no_images_in_db'].append(product)
            categories['need_processing'].append(product)
            continue
            
        # Product has images in DB - check if they exist in blob storage
        if isinstance(images, str):
            try:
                images = json.loads(images)
            except:
                categories['no_images_in_db'].append(product)
                categories['need_processing'].append(product)
                continue
                
        if isinstance(images, dict):
            thomann_main = images.get('thomann_main')
            if thomann_main:
                # Handle case where thomann_main might be a dict or string
                image_url = thomann_main
                if isinstance(thomann_main, dict):
                    image_url = thomann_main.get('url', '')
                
                if isinstance(image_url, str) and image_url:
                    # Extract blob name from URL
                    match = re.search(r'/product-images/(.+)$', image_url)
                    if match:
                        blob_name = match.group(1)
                        if blob_name in existing_blobs:
                            categories['valid_images'].append(product)
                        else:
                            categories['broken_image_links'].append(product)
                            categories['need_processing'].append(product)
                    else:
                        categories['broken_image_links'].append(product)
                        categories['need_processing'].append(product)
                else:
                    categories['no_images_in_db'].append(product)
                    categories['need_processing'].append(product)
            else:
                categories['no_images_in_db'].append(product)
                categories['need_processing'].append(product)
        else:
            categories['no_images_in_db'].append(product)
            categories['need_processing'].append(product)
    
    print(f"\n📊 COMPLETE IMAGE ANALYSIS:")
    print(f"✅ Products with valid images: {len(categories['valid_images'])}")
    print(f"❌ Products with broken image links: {len(categories['broken_image_links'])}")
    print(f"📝 Products with no images in DB: {len(categories['no_images_in_db'])}")
    print(f"🎯 TOTAL PRODUCTS NEEDING PROCESSING: {len(categories['need_processing'])}")
    
    print(f"\n📊 Breakdown:")
    print(f"   📁 Total products with Thomann URLs: {len(all_products)}")
    print(f"   ✅ Already processed (valid images): {len(categories['valid_images'])}")
    print(f"   🔄 Need reprocessing (broken links): {len(categories['broken_image_links'])}")
    print(f"   📥 Need initial processing (no images): {len(categories['no_images_in_db'])}")
    
    # Save the products that need processing to a file
    products_to_process = [
        {
            'id': p['id'],
            'name': p['name'],
            'thomann_url': p['thomann_url'],
            'reason': 'no_images' if p in categories['no_images_in_db'] else 'broken_link'
        }
        for p in categories['need_processing']
    ]
    
    output_file = f"products_needing_images_{len(products_to_process)}_items.json"
    with open(output_file, 'w') as f:
        json.dump(products_to_process, f, indent=2)
    
    print(f"\n💾 Saved {len(products_to_process)} products to: {output_file}")
    
    print(f"\n🚨 CRAWLER UPDATE NEEDED:")
    print(f"   Current crawler processes: 52 products")
    print(f"   Should process: {len(categories['need_processing'])} products")
    print(f"   Missing: {len(categories['need_processing']) - 52} products")
    
    # Show samples
    print(f"\n🔍 Sample products needing processing:")
    for i, product in enumerate(categories['need_processing'][:5], 1):
        reason = 'No images in DB' if product in categories['no_images_in_db'] else 'Broken image link'
        print(f"  {i}. ID {product['id']}: {product['name'][:50]}... ({reason})")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(identify_all_products_needing_images())

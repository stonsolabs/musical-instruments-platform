#!/usr/bin/env python3

import asyncio
import asyncpg
import os
import json
import subprocess
import re
from dotenv import load_dotenv

load_dotenv()

async def fix_all_image_associations():
    """Fix all image associations between database and Azure blob storage"""
    
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    print('🔧 COMPREHENSIVE IMAGE ASSOCIATION FIX')
    print('=' * 50)
    
    # Step 1: Load all blob files from Azure storage
    print('📋 Loading all Azure blob files...')
    try:
        result = subprocess.run([
            'az', 'storage', 'blob', 'list',
            '--container-name', 'product-images',
            '--account-name', 'getyourmusicgear',
            '--query', '[].name',
            '--output', 'json'
        ], capture_output=True, text=True, timeout=120)
        
        blob_names = json.loads(result.stdout)
        
        # Create mapping of product_id -> blob_name
        blob_mapping = {}
        for blob_name in blob_names:
            if blob_name.startswith('thomann/'):
                filename = blob_name[8:]  # Remove 'thomann/' prefix
                match = re.match(r'^(\d+)_', filename)
                if match:
                    product_id = int(match.group(1))
                    # Keep the latest blob if multiple exist
                    if product_id not in blob_mapping or blob_name > blob_mapping[product_id]:
                        blob_mapping[product_id] = blob_name
        
        print(f'✅ Found {len(blob_mapping)} unique products with blob files')
        
    except Exception as e:
        print(f'❌ Error loading blob storage: {e}')
        await conn.close()
        return
    
    # Step 2: Get all products with Thomann URLs
    print('📋 Loading all products with Thomann URLs...')
    
    query = '''
        SELECT p.id, p.name, p.images
        FROM products p
        WHERE p.content->>'store_links' IS NOT NULL
        AND p.content->'store_links'->>'Thomann' IS NOT NULL
        ORDER BY p.id
    '''
    
    products = await conn.fetch(query)
    print(f'✅ Found {len(products)} products with Thomann URLs')
    
    # Step 3: Analyze and fix associations
    print('\\n🔍 Analyzing associations...')
    
    fixes_applied = 0
    missing_blobs = 0
    already_correct = 0
    
    for product in products:
        product_id = product['id']
        images = product['images']
        
        # Check if product has blob file
        if product_id in blob_mapping:
            blob_name = blob_mapping[product_id]
            correct_url = f'https://getyourmusicgear.blob.core.windows.net/product-images/{blob_name}'
            
            # Check current database image status
            needs_update = True
            if images and images != '{}' and isinstance(images, dict):
                current_url = images.get('thomann_main')
                if current_url == correct_url:
                    needs_update = False
                    already_correct += 1
            
            if needs_update:
                # Update the database with correct image URL
                new_images = {
                    'thomann_main': correct_url
                }
                
                try:
                    update_query = '''
                        UPDATE products 
                        SET images = $1, updated_at = NOW()
                        WHERE id = $2
                    '''
                    await conn.execute(update_query, json.dumps(new_images), product_id)
                    fixes_applied += 1
                    
                    if fixes_applied <= 10:  # Show first 10 fixes
                        product_name = product['name'][:40]
                        print(f'   ✅ Fixed Product {product_id}: {product_name}...')
                
                except Exception as e:
                    print(f'   ❌ Error updating Product {product_id}: {e}')
        else:
            missing_blobs += 1
    
    print(f'\\n📊 RESULTS:')
    print(f'   ✅ Already correct: {already_correct}')
    print(f'   🔧 Fixes applied: {fixes_applied}')
    print(f'   ❌ Missing blobs: {missing_blobs}')
    print(f'   📊 Total processed: {len(products)}')
    
    # Step 4: Verify the fixes
    print('\\n🔍 Verifying fixes...')
    
    verify_query = '''
        SELECT COUNT(*) as count
        FROM products p
        WHERE p.content->>'store_links' IS NOT NULL
        AND p.content->'store_links'->>'Thomann' IS NOT NULL
        AND p.images IS NOT NULL
        AND p.images != '{}'
        AND jsonb_typeof(p.images) = 'object'
        AND p.images->>'thomann_main' IS NOT NULL
    '''
    
    products_with_images = await conn.fetchval(verify_query)
    completion_percentage = (products_with_images / len(products)) * 100
    
    print(f'\\n🎯 FINAL STATUS:')
    print(f'   📊 Products with images: {products_with_images} / {len(products)}')
    print(f'   📈 Completion: {completion_percentage:.1f}%')
    print(f'   📥 Still need images: {len(products) - products_with_images}')
    
    await conn.close()
    
    print(f'\\n✅ Image association fix completed!')

if __name__ == "__main__":
    asyncio.run(fix_all_image_associations())

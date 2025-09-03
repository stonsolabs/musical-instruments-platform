#!/usr/bin/env python3

import asyncio
import asyncpg
import os
import json
import subprocess
import re
from dotenv import load_dotenv

load_dotenv()

async def final_image_association_check():
    """Final check and fix of all image associations"""
    
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    print('🎯 FINAL IMAGE ASSOCIATION CHECK')
    print('=' * 40)
    
    # Step 1: Get blob files
    print('📋 Loading Azure blob files...')
    try:
        result = subprocess.run([
            'az', 'storage', 'blob', 'list',
            '--container-name', 'product-images',
            '--account-name', 'getyourmusicgear',
            '--query', '[].name',
            '--output', 'json'
        ], capture_output=True, text=True, timeout=120)
        
        blob_names = json.loads(result.stdout)
        
        blob_mapping = {}
        for blob_name in blob_names:
            if blob_name.startswith('thomann/'):
                filename = blob_name[8:]
                match = re.match(r'^(\d+)_', filename)
                if match:
                    product_id = int(match.group(1))
                    blob_mapping[product_id] = blob_name
        
        print(f'✅ Found {len(blob_mapping)} blob files')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        await conn.close()
        return
    
    # Step 2: Check database status
    total_query = '''
        SELECT COUNT(*) as count
        FROM products 
        WHERE content->>'store_links' IS NOT NULL
        AND content->'store_links'->>'Thomann' IS NOT NULL
    '''
    total_products = await conn.fetchval(total_query)
    
    # Step 3: Check current associations
    current_query = '''
        SELECT COUNT(*) as count
        FROM products 
        WHERE images IS NOT NULL
        AND images != '{}'
        AND jsonb_typeof(images) = 'object'
        AND images->>'thomann_main' LIKE 'https://getyourmusicgear.blob.core.windows.net%'
    '''
    current_associated = await conn.fetchval(current_query)
    
    print(f'\\n📊 Current Status:')
    print(f'   📊 Total Thomann products: {total_products}')
    print(f'   ✅ Currently associated: {current_associated}')
    print(f'   📁 Available blob files: {len(blob_mapping)}')
    
    # Step 4: Find products with blob files but no database association
    print('\\n🔍 Finding products with blobs but no DB association...')
    
    fixes_needed = []
    for product_id in blob_mapping.keys():
        # Check if this product needs association
        check_query = '''
            SELECT id, name, images
            FROM products 
            WHERE id = $1
            AND content->>'store_links' IS NOT NULL
            AND content->'store_links'->>'Thomann' IS NOT NULL
            AND (images IS NULL 
                 OR images = '{}' 
                 OR jsonb_typeof(images) != 'object'
                 OR images->>'thomann_main' IS NULL
                 OR images->>'thomann_main' = '')
        '''
        
        product = await conn.fetchrow(check_query, product_id)
        if product:
            fixes_needed.append((product_id, product['name'], blob_mapping[product_id]))
    
    print(f'✅ Found {len(fixes_needed)} products needing association')
    
    # Step 5: Apply fixes
    if fixes_needed:
        print(f'\\n🔧 Applying fixes...')
        fixes_applied = 0
        
        for product_id, product_name, blob_name in fixes_needed:
            azure_url = f'https://getyourmusicgear.blob.core.windows.net/product-images/{blob_name}'
            
            images_data = {
                'thomann_main': azure_url
            }
            
            try:
                update_query = '''
                    UPDATE products 
                    SET images = $1::jsonb, updated_at = NOW()
                    WHERE id = $2
                '''
                await conn.execute(update_query, json.dumps(images_data), product_id)
                fixes_applied += 1
                
                if fixes_applied <= 10:
                    print(f'   ✅ Fixed Product {product_id}: {product_name[:40]}...')
                
            except Exception as e:
                print(f'   ❌ Error fixing Product {product_id}: {e}')
        
        print(f'\\n✅ Applied {fixes_applied} fixes')
    
    # Step 6: Final verification
    final_query = '''
        SELECT COUNT(*) as count
        FROM products 
        WHERE images IS NOT NULL
        AND images != '{}'
        AND jsonb_typeof(images) = 'object'
        AND images->>'thomann_main' LIKE 'https://getyourmusicgear.blob.core.windows.net%'
    '''
    
    final_count = await conn.fetchval(final_query)
    completion_pct = (final_count / total_products) * 100
    
    print(f'\\n🎯 FINAL RESULTS:')
    print(f'   ✅ Products with images: {final_count} / {total_products}')
    print(f'   📈 Completion: {completion_pct:.1f}%')
    print(f'   📥 Still missing images: {total_products - final_count}')
    print(f'   📁 Blob files utilized: {min(final_count, len(blob_mapping))} / {len(blob_mapping)}')
    
    await conn.close()
    print(f'\\n✅ Image association check completed!')

if __name__ == "__main__":
    asyncio.run(final_image_association_check())

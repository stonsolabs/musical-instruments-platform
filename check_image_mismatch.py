#!/usr/bin/env python3
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = 'postgresql://admin:qQqqDgXlIuBSZDUlgqzQEcoTPBkrCjVD@dpg-d2er32qdbo4c738oofng-a.frankfurt-postgres.render.com/musicgear_db'
ASYNC_DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')

# Path to the frontend public images
IMAGES_DIR = '/Users/felipe/pprojects/musical-instruments-platform/frontend/public/product-images'

async def check_image_mismatches():
    """Check which database image paths don't match actual files."""
    
    # Get all image files
    actual_files = set()
    if os.path.exists(IMAGES_DIR):
        actual_files = set(os.listdir(IMAGES_DIR))
        print(f"Found {len(actual_files)} actual image files")
    else:
        print(f"Images directory not found: {IMAGES_DIR}")
        return

    engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
    
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text('SELECT id, sku, name, images FROM products WHERE images IS NOT NULL AND array_length(images, 1) > 0'))
            products = result.fetchall()
            
            missing_files = []
            matching_files = []
            
            for product in products:
                product_id, sku, name, images = product
                
                for img_path in images:
                    filename = img_path.split('/')[-1]
                    
                    if filename in actual_files:
                        matching_files.append((product_id, sku, name, filename))
                    else:
                        missing_files.append((product_id, sku, name, filename))
            
            print(f"\n=== RESULTS ===")
            print(f"✅ Matching files: {len(matching_files)}")
            print(f"❌ Missing files: {len(missing_files)}")
            
            if missing_files:
                print(f"\n=== MISSING FILES ===")
                for product_id, sku, name, filename in missing_files:
                    print(f"❌ Product {product_id}: {name}")
                    print(f"   SKU: {sku}")
                    print(f"   Missing: {filename}")
                    
                    # Try to find similar files
                    base_name = filename.replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
                    similar = [f for f in actual_files if base_name.split('_')[0] in f.lower()]
                    if similar:
                        print(f"   Similar files: {similar[:3]}")
                    print()
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_image_mismatches())
#!/usr/bin/env python3
"""
Apply Image URL Fixes to Database
- Apply the generated SQL fixes to update image URLs
- Verify the fixes were applied correctly
- Generate report of applied fixes
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Product

async def apply_image_fixes():
    """Apply the image URL fixes to the database"""
    
    print("🚀 Applying Image URL Fixes to Database")
    print("=" * 50)
    
    database_url = "postgresql://getyourmusicgear:arg-KDP8cjy.czu2zdv@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear"
    async_db_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    engine = create_async_engine(async_db_url)
    session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    try:
        # Find the latest fix file
        fix_files = [f for f in os.listdir('.') if f.startswith('image_url_fixes_') and f.endswith('.json')]
        if not fix_files:
            print("❌ No image fix file found. Run fix_image_mapping.py first.")
            return
        
        latest_fix_file = sorted(fix_files)[-1]
        print(f"📋 Loading fixes from: {latest_fix_file}")
        
        with open(latest_fix_file, 'r') as f:
            fix_statements = json.load(f)
        
        print(f"📊 Found {len(fix_statements)} fixes to apply")
        
        # Apply fixes in batches
        batch_size = 100
        applied_count = 0
        error_count = 0
        
        async with session_maker() as session:
            for i in range(0, len(fix_statements), batch_size):
                batch = fix_statements[i:i + batch_size]
                print(f"🔄 Applying batch {i//batch_size + 1}: fixes {i+1}-{min(i+batch_size, len(fix_statements))}")
                
                try:
                    async with session.begin():
                        for fix in batch:
                            try:
                                # Get the product
                                result = await session.execute(
                                    select(Product).where(Product.id == fix['product_id'])
                                )
                                product = result.scalar_one_or_none()
                                
                                if product and product.images:
                                    # Update the main image URL
                                    updated_images = product.images.copy()
                                    
                                    # Find the main image key
                                    main_key = None
                                    for key in updated_images.keys():
                                        if 'main' in key.lower() or 'thomann' in key.lower():
                                            main_key = key
                                            break
                                    
                                    if not main_key and updated_images:
                                        main_key = list(updated_images.keys())[0]
                                    
                                    if main_key:
                                        # Update the URL
                                        if isinstance(updated_images[main_key], dict):
                                            updated_images[main_key]['url'] = fix['new_url']
                                        else:
                                            updated_images[main_key] = fix['new_url']
                                        
                                        product.images = updated_images
                                        applied_count += 1
                                
                            except Exception as e:
                                print(f"  ❌ Error fixing product {fix['product_id']}: {e}")
                                error_count += 1
                    
                    print(f"  ✅ Batch completed")
                    
                except Exception as e:
                    print(f"  ❌ Batch failed: {e}")
                    error_count += len(batch)
        
        print(f"\n📊 RESULTS:")
        print(f"✅ Successfully applied: {applied_count} fixes")
        print(f"❌ Errors: {error_count} fixes")
        print(f"📈 Success rate: {applied_count/(applied_count+error_count)*100:.1f}%")
        
        # Verify some fixes
        print(f"\n🔍 Verifying applied fixes...")
        await verify_fixes(session_maker, fix_statements[:10])
        
    except Exception as e:
        print(f"❌ Error applying fixes: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await engine.dispose()

async def verify_fixes(session_maker, sample_fixes: List[Dict]):
    """Verify that fixes were applied correctly"""
    
    async with session_maker() as session:
        verified_count = 0
        
        for fix in sample_fixes:
            try:
                result = await session.execute(
                    select(Product).where(Product.id == fix['product_id'])
                )
                product = result.scalar_one_or_none()
                
                if product and product.images:
                    # Check if the URL was updated
                    main_key = None
                    for key in product.images.keys():
                        if 'main' in key.lower() or 'thomann' in key.lower():
                            main_key = key
                            break
                    
                    if main_key:
                        current_url = None
                        if isinstance(product.images[main_key], dict):
                            current_url = product.images[main_key].get('url')
                        else:
                            current_url = product.images[main_key]
                        
                        if current_url == fix['new_url']:
                            verified_count += 1
                            print(f"  ✅ Product {fix['product_id']}: URL updated correctly")
                        else:
                            print(f"  ❌ Product {fix['product_id']}: URL not updated")
                            print(f"     Expected: {fix['new_url']}")
                            print(f"     Actual: {current_url}")
                
            except Exception as e:
                print(f"  ❌ Error verifying product {fix['product_id']}: {e}")
        
        print(f"\n📊 Verification: {verified_count}/{len(sample_fixes)} fixes verified")

if __name__ == "__main__":
    asyncio.run(apply_image_fixes())

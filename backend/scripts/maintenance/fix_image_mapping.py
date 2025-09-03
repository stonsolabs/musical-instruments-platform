#!/usr/bin/env python3
"""
Fix Image URL Mapping Job
- Map product IDs to correct blob storage filenames
- Update database with correct Azure blob URLs
- Generate SQL update statements
"""

import asyncio
import json
import re
from datetime import datetime
from typing import Dict, List, Set
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Product

class ImageMappingFixer:
    def __init__(self):
        self.database_url = "postgresql://getyourmusicgear:arg-KDP8cjy.czu2zdv@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear"
        self.async_db_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        self.engine = None
        self.session_maker = None
        
        # Available blob images (ID -> filename mapping)
        self.blob_images = {}  # {product_id: filename}
        self.blob_timestamps = {}  # {product_id: [list of timestamps]}

    async def initialize_db(self):
        """Initialize database connection"""
        self.engine = create_async_engine(self.async_db_url)
        self.session_maker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def close_db(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()

    def load_blob_images(self):
        """Load available blob storage images from Azure CLI output"""
        print("📋 Loading blob storage image list...")
        
        # Run Azure CLI command to get blob list
        import subprocess
        
        try:
            result = subprocess.run([
                'az', 'storage', 'blob', 'list',
                '--container-name', 'product-images',
                '--account-name', 'getyourmusicgear',
                '--query', '[].name',
                '--output', 'json'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                blob_names = json.loads(result.stdout)
                print(f"✅ Found {len(blob_names)} images in blob storage")
                
                # Parse blob names to extract product IDs
                for blob_name in blob_names:
                    if blob_name.startswith('thomann/'):
                        filename = blob_name[8:]  # Remove 'thomann/' prefix
                        
                        # Extract product ID from filename (should be at the start)
                        match = re.match(r'^(\d+)_', filename)
                        if match:
                            product_id = int(match.group(1))
                            
                            # Store the full blob name for URL construction
                            if product_id not in self.blob_images:
                                self.blob_images[product_id] = []
                                self.blob_timestamps[product_id] = []
                            
                            self.blob_images[product_id].append(blob_name)
                            
                            # Extract timestamp if present
                            timestamp_match = re.search(r'_(\d{8}_\d{6})\.jpg$', filename)
                            if timestamp_match:
                                self.blob_timestamps[product_id].append(timestamp_match.group(1))
                
                print(f"📊 Mapped {len(self.blob_images)} product IDs to blob images")
                
                # Show sample mappings
                print("\n🔍 Sample product ID to blob mappings:")
                for i, (product_id, blob_names) in enumerate(list(self.blob_images.items())[:10]):
                    print(f"  Product {product_id}: {len(blob_names)} images")
                    for blob_name in blob_names[:2]:  # Show first 2 images
                        print(f"    - {blob_name}")
                
                return True
                
            else:
                print(f"❌ Error running Azure CLI: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Azure CLI command timed out")
            return False
        except Exception as e:
            print(f"❌ Error loading blob images: {e}")
            return False

    async def find_products_to_fix(self):
        """Find products with broken image URLs that can be fixed"""
        print("\n🔧 Finding products with fixable image URLs...")
        
        fixable_products = []
        unfixable_products = []
        
        async with self.session_maker() as session:
            # Get products with broken Azure blob URLs
            query = select(Product).where(
                Product.is_active == True,
                Product.images.isnot(None)
            )
            
            result = await session.execute(query)
            products = result.scalars().all()
            
            for product in products:
                if not product.images:
                    continue
                
                has_broken_azure_url = False
                can_be_fixed = False
                
                # Check each image URL
                for key, image_data in product.images.items():
                    if isinstance(image_data, dict) and "url" in image_data:
                        url = image_data["url"]
                    elif isinstance(image_data, str):
                        url = image_data
                    else:
                        continue
                    
                    # Check if it's a broken Azure blob URL
                    if "getyourmusicgear.blob.core.windows.net" in url:
                        # Check if we have a blob image for this product ID
                        if product.id in self.blob_images:
                            has_broken_azure_url = True
                            can_be_fixed = True
                            break
                
                if has_broken_azure_url and can_be_fixed:
                    fixable_products.append(product)
                elif has_broken_azure_url:
                    unfixable_products.append(product)
        
        print(f"✅ Found {len(fixable_products)} products that can be fixed")
        print(f"❌ Found {len(unfixable_products)} products that cannot be fixed (no blob image)")
        
        return fixable_products, unfixable_products

    def generate_correct_url(self, product_id: int) -> str:
        """Generate correct Azure blob URL for a product"""
        if product_id not in self.blob_images:
            return None
        
        # Use the most recent image (last in the list)
        blob_name = self.blob_images[product_id][-1]
        return f"https://getyourmusicgear.blob.core.windows.net/product-images/{blob_name}"

    async def generate_fix_statements(self, fixable_products: List[Product]):
        """Generate SQL statements to fix the image URLs"""
        print(f"\n📝 Generating fix statements for {len(fixable_products)} products...")
        
        fix_statements = []
        fixed_count = 0
        
        for product in fixable_products:
            correct_url = self.generate_correct_url(product.id)
            if not correct_url:
                continue
            
            # Update the images dict with correct URL
            updated_images = product.images.copy()
            
            # Find the main image key (usually 'thomann_main')
            main_key = None
            for key in updated_images.keys():
                if 'main' in key.lower() or 'thomann' in key.lower():
                    main_key = key
                    break
            
            if not main_key:
                main_key = list(updated_images.keys())[0]  # Use first key
            
            # Update the URL
            if isinstance(updated_images[main_key], dict):
                updated_images[main_key]['url'] = correct_url
            else:
                updated_images[main_key] = correct_url
            
            # Generate SQL update statement
            sql_statement = f"""UPDATE products SET images = '{json.dumps(updated_images)}'::jsonb WHERE id = {product.id};"""
            fix_statements.append({
                'product_id': product.id,
                'product_name': product.name,
                'old_url': product.images.get(main_key, {}).get('url', 'N/A') if isinstance(product.images.get(main_key), dict) else product.images.get(main_key, 'N/A'),
                'new_url': correct_url,
                'sql': sql_statement
            })
            
            fixed_count += 1
        
        print(f"✅ Generated {fixed_count} fix statements")
        
        # Save fix statements to file
        filename = f"image_url_fixes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(fix_statements, f, indent=2)
        
        print(f"💾 Fix statements saved to: {filename}")
        
        # Generate SQL file
        sql_filename = f"fix_image_urls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        with open(sql_filename, 'w') as f:
            f.write("-- Fix Image URL Mappings\n")
            f.write(f"-- Generated: {datetime.now()}\n")
            f.write(f"-- Total fixes: {len(fix_statements)}\n\n")
            
            for fix in fix_statements:
                f.write(f"-- Product {fix['product_id']}: {fix['product_name']}\n")
                f.write(f"-- Old: {fix['old_url']}\n")
                f.write(f"-- New: {fix['new_url']}\n")
                f.write(f"{fix['sql']}\n\n")
        
        print(f"📄 SQL file saved to: {sql_filename}")
        
        # Show sample fixes
        print(f"\n🔍 Sample fixes:")
        for i, fix in enumerate(fix_statements[:5]):
            print(f"\n{i+1}. Product {fix['product_id']}: {fix['product_name']}")
            print(f"   Old URL: {fix['old_url'][:80]}...")
            print(f"   New URL: {fix['new_url']}")
        
        return fix_statements

    async def apply_fixes_to_database(self, fix_statements: List[Dict], dry_run: bool = True):
        """Apply the fixes to the database"""
        if dry_run:
            print(f"\n🧪 DRY RUN MODE - Would fix {len(fix_statements)} products")
            return
        
        print(f"\n🚀 Applying fixes to database for {len(fix_statements)} products...")
        
        async with self.session_maker() as session:
            try:
                for fix in fix_statements:
                    # Parse the updated images from the fix
                    # This is a simplified approach - in production you'd want more robust parsing
                    product_id = fix['product_id']
                    
                    # Get the current product
                    result = await session.execute(select(Product).where(Product.id == product_id))
                    product = result.scalar_one_or_none()
                    
                    if product:
                        # Update with correct URL
                        correct_url = self.generate_correct_url(product_id)
                        if correct_url:
                            updated_images = product.images.copy()
                            
                            # Update the main image
                            main_key = None
                            for key in updated_images.keys():
                                if 'main' in key.lower() or 'thomann' in key.lower():
                                    main_key = key
                                    break
                            
                            if main_key:
                                if isinstance(updated_images[main_key], dict):
                                    updated_images[main_key]['url'] = correct_url
                                else:
                                    updated_images[main_key] = correct_url
                                
                                product.images = updated_images
                
                await session.commit()
                print(f"✅ Successfully applied {len(fix_statements)} fixes")
                
            except Exception as e:
                await session.rollback()
                print(f"❌ Error applying fixes: {e}")
                raise

async def main():
    """Main execution function"""
    fixer = ImageMappingFixer()
    
    try:
        # Load blob storage images
        if not fixer.load_blob_images():
            print("❌ Failed to load blob storage images")
            return
        
        # Initialize database
        await fixer.initialize_db()
        
        # Find products to fix
        fixable_products, unfixable_products = await fixer.find_products_to_fix()
        
        if fixable_products:
            # Generate fix statements
            fix_statements = await fixer.generate_fix_statements(fixable_products)
            
            # Ask user if they want to apply fixes
            print(f"\n❓ Do you want to apply these fixes to the database?")
            print("   This will update the image URLs for the products.")
            print("   Type 'yes' to apply, anything else for dry run only:")
            
            # For automation, we'll default to dry run
            apply_fixes = False  # Change to True if you want to auto-apply
            
            await fixer.apply_fixes_to_database(fix_statements, dry_run=not apply_fixes)
        
        else:
            print("ℹ️  No fixable products found")
        
    except Exception as e:
        print(f"❌ Error during image mapping fix: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await fixer.close_db()

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Fast Multi-threaded Product Image Association Fixer
Updates database with correct Azure image URLs for products missing thomann_main images
"""

import asyncio
import json
import subprocess
import sys
import re
import os
from datetime import datetime
from typing import Dict, List
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Database connection using asyncpg directly
import asyncpg

class FastAssociationFixer:
    def __init__(self):
        self.updated = 0
        self.failed = 0
        self.not_found = 0
        self.lock = threading.Lock()
        self.database_url = os.getenv('DATABASE_URL')
        
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable required")
    
    async def get_products_missing_images(self) -> List[int]:
        """Get product IDs where thomann_main image URL is NULL"""
        print("🔍 Fetching products missing thomann_main images...")
        
        try:
            conn = await asyncpg.connect(self.database_url)
            
            # Query products where thomann_main image URL is NULL (exactly as specified)
            rows = await conn.fetch("""
                SELECT id, name, images 
                FROM products 
                WHERE images -> 'thomann_main' ->> 'url' IS NULL
                ORDER BY id
            """)
            
            await conn.close()
            
            product_ids = [row['id'] for row in rows]
            print(f"✅ Found {len(product_ids)} products missing thomann_main images")
            
            # Show some examples
            if product_ids:
                print(f"   📋 Examples: {product_ids[:10]}")
                if len(product_ids) > 10:
                    print(f"   ... and {len(product_ids) - 10} more")
            
            return product_ids
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            return []
    
    def get_azure_images(self) -> Dict[int, str]:
        """Get current images from Azure storage"""
        print("🔍 Fetching images from Azure storage...")
        
        result = subprocess.run([
            'az', 'storage', 'blob', 'list',
            '--container-name', 'product-images',
            '--account-name', 'getyourmusicgear',
            '--prefix', 'thomann/',
            '--query', '[].name',
            '--output', 'json'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            print(f"❌ Azure CLI error: {result.stderr}")
            return {}
        
        blob_names = json.loads(result.stdout)
        product_images = {}
        
        # Construct the full URL manually
        base_url = "https://getyourmusicgear.blob.core.windows.net/product-images"
        
        for blob_name in blob_names:
            # Parse product ID: thomann/{product_id}_{timestamp}.jpg
            filename = blob_name.replace('thomann/', '')
            match = re.match(r'^(\d+)_', filename)
            
            if match:
                product_id = int(match.group(1))
                full_url = f"{base_url}/{blob_name}"
                product_images[product_id] = full_url
        
        print(f"✅ Found {len(product_images)} product images in Azure")
        return product_images
    
    async def get_product_source_url(self, product_id: int) -> str:
        """Get the source URL for a product from the content field"""
        try:
            conn = await asyncpg.connect(self.database_url)
            
            # Try to get source URL from content field
            row = await conn.fetchrow("""
                SELECT content 
                FROM products 
                WHERE id = $1
            """, product_id)
            
            await conn.close()
            
            if row and row['content']:
                content = row['content']
                # Look for thomann URL in various possible locations
                if isinstance(content, dict):
                    # Check common locations for source URL
                    for key in ['source_url', 'url', 'thomann_url', 'affiliate_url']:
                        if key in content and content[key]:
                            return content[key]
                    
                    # Check if there's a thomann section
                    if 'thomann' in content and isinstance(content['thomann'], dict):
                        for key in ['url', 'source_url', 'affiliate_url']:
                            if key in content['thomann'] and content['thomann'][key]:
                                return content['thomann'][key]
            
            # Default fallback
            return f"https://www.thomann.co.uk/product_{product_id}.htm"
            
        except Exception as e:
            print(f"⚠️  Warning: Could not get source URL for product {product_id}: {e}")
            return f"https://www.thomann.co.uk/product_{product_id}.htm"
    
    async def update_single_product(self, product_id: int, blob_url: str) -> bool:
        """Update a single product's image association"""
        try:
            conn = await asyncpg.connect(self.database_url)
            
            # Get existing images to preserve them
            row = await conn.fetchrow("""
                SELECT images, content 
                FROM products 
                WHERE id = $1
            """, product_id)
            
            if not row:
                await conn.close()
                return False
            
            # Handle different types of images field
            existing_images = {}
            if row['images']:
                if isinstance(row['images'], str):
                    try:
                        # Try to parse string as JSON
                        existing_images = json.loads(row['images'])
                    except (json.JSONDecodeError, TypeError):
                        # If it's not valid JSON, start with empty dict
                        existing_images = {}
                elif isinstance(row['images'], dict):
                    existing_images = row['images']
                else:
                    # Unknown type, start with empty dict
                    existing_images = {}
            source_url = await self.get_product_source_url(product_id)
            
            # Create new thomann_main image data
            new_image_data = {
                "url": blob_url,
                "type": "main",
                "source": "thomann",
                "source_url": source_url,
                "downloaded_at": datetime.utcnow().isoformat(),
                "fixed_at": datetime.utcnow().isoformat()
            }
            
            # Update images field, preserving existing images
            existing_images['thomann_main'] = new_image_data
            
            # Update product
            await conn.execute("""
                UPDATE products 
                SET images = $1::jsonb,
                    updated_at = NOW()
                WHERE id = $2
            """, json.dumps(existing_images), product_id)
            
            await conn.close()
            
            with self.lock:
                self.updated += 1
            return True
            
        except Exception as e:
            print(f"❌ Error updating product {product_id}: {e}")
            with self.lock:
                self.failed += 1
            return False
    
    def update_associations_threaded(self, product_images: Dict[int, str], max_workers: int = 10) -> Dict:
        """Update associations using multiple threads"""
        print(f"🚀 Starting threaded updates with {max_workers} workers...")
        print(f"🔧 Updating {len(product_images)} product associations...")
        
        start_time = time.time()
        
        # Create event loop for this thread if needed
        def run_async_update(product_id: int, blob_url: str) -> bool:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return loop.run_until_complete(self.update_single_product(product_id, blob_url))
            finally:
                loop.close()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all update tasks
            future_to_product = {
                executor.submit(run_async_update, product_id, blob_url): product_id
                for product_id, blob_url in product_images.items()
            }
            
            # Process completed tasks and show progress
            for i, future in enumerate(as_completed(future_to_product), 1):
                product_id = future_to_product[future]
                
                # Show progress every 50 updates
                if i % 50 == 0:
                    elapsed = time.time() - start_time
                    rate = i / elapsed if elapsed > 0 else 0
                    eta = (len(product_images) - i) / rate if rate > 0 else 0
                    print(f"   📊 Progress: {i}/{len(product_images)} ({rate:.1f}/sec, ETA: {eta:.0f}s)")
        
        elapsed = time.time() - start_time
        print(f"\n⏱️  Total time: {elapsed:.1f} seconds")
        print(f"📊 Final results:")
        print(f"   ✅ Updated: {self.updated}")
        print(f"   ❌ Failed: {self.failed}")
        print(f"   🔍 Not found in storage: {self.not_found}")
        
        return {
            'updated': self.updated, 
            'failed': self.failed, 
            'not_found': self.not_found
        }
    
    async def process_missing_images(self) -> Dict:
        """Main process: find products missing images and associate them with Azure storage"""
        print("🚀 FAST MULTI-THREADED ASSOCIATION FIXER")
        print("=" * 50)
        
        # Step 1: Get products missing thomann_main images
        missing_product_ids = await self.get_products_missing_images()
        if not missing_product_ids:
            print("✅ No products found missing thomann_main images")
            return {'updated': 0, 'failed': 0, 'not_found': 0}
        
        # Step 2: Get Azure storage images
        azure_images = self.get_azure_images()
        if not azure_images:
            print("❌ No images found in Azure storage")
            return {'updated': 0, 'failed': 0, 'not_found': 0}
        
        # Step 3: Find products that have images in storage
        products_to_update = {}
        for product_id in missing_product_ids:
            if product_id in azure_images:
                products_to_update[product_id] = azure_images[product_id]
            else:
                self.not_found += 1
        
        print(f"🔍 Found {len(products_to_update)} products with images in storage")
        print(f"🔍 {self.not_found} products missing images in storage")
        
        if not products_to_update:
            print("✅ No products to update")
            return {'updated': 0, 'failed': 0, 'not_found': self.not_found}
        
        # Step 4: Update associations using threads
        result = self.update_associations_threaded(products_to_update)
        result['not_found'] = self.not_found
        
        return result

def main():
    if len(sys.argv) < 2 or sys.argv[1] != '--execute':
        print("🔍 Use --execute to run association fixing")
        print("Example: python3.11 fast_association_fix.py --execute")
        return
    
    print("🚀 FAST MULTI-THREADED ASSOCIATION FIXER")
    print("=" * 50)
    
    try:
        fixer = FastAssociationFixer()
        
        # Run the main process
        result = asyncio.run(fixer.process_missing_images())
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"fast_association_fix_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'update_result': result
            }, f, indent=2)
        
        print(f"📋 Report saved: {report_file}")
        print("✅ Fast association fixing completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
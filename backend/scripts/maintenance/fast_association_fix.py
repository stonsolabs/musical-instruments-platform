#!/usr/bin/env python3
"""
Fast Multi-threaded Product Image Association Fixer
Updates database with correct Azure image URLs using threading
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
        self.lock = threading.Lock()
        self.database_url = os.getenv('DATABASE_URL')
        
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable required")
    
    def get_azure_images(self):
        """Get current images from Azure storage"""
        print("🔍 Fetching images from Azure storage...")
        
        result = subprocess.run([
            'az', 'storage', 'blob', 'list',
            '--container-name', 'product-images',
            '--account-name', 'getyourmusicgear',
            '--prefix', 'thomann/',
            '--query', '[].{name: name, url: url}',
            '--output', 'json'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            print(f"❌ Azure CLI error: {result.stderr}")
            return {}
        
        blobs = json.loads(result.stdout)
        product_images = {}
        
        for blob in blobs:
            blob_name = blob['name']
            blob_url = blob['url']
            
            # Parse product ID: thomann/{product_id}_{timestamp}.jpg
            filename = blob_name.replace('thomann/', '')
            match = re.match(r'^(\d+)_', filename)
            
            if match:
                product_id = int(match.group(1))
                product_images[product_id] = blob_url
        
        print(f"✅ Found {len(product_images)} product images in Azure")
        return product_images
    
    async def update_single_product(self, product_id, blob_url):
        """Update a single product's image association"""
        try:
            conn = await asyncpg.connect(self.database_url)
            
            # Create new image data
            image_data = {
                "thomann_main": {
                    "url": blob_url,
                    "source": "thomann",
                    "downloaded_at": datetime.utcnow().isoformat(),
                    "type": "main",
                    "fixed_at": datetime.utcnow().isoformat()
                }
            }
            
            # Update product with only the new association
            await conn.execute("""
                UPDATE products 
                SET images = $1::jsonb,
                    updated_at = NOW()
                WHERE id = $2
            """, json.dumps(image_data), product_id)
            
            await conn.close()
            
            with self.lock:
                self.updated += 1
            return True
            
        except Exception as e:
            with self.lock:
                self.failed += 1
            return False
    
    def update_associations_threaded(self, product_images, max_workers=10):
        """Update associations using multiple threads"""
        print(f"🚀 Starting threaded updates with {max_workers} workers...")
        print(f"🔧 Updating {len(product_images)} product associations...")
        
        start_time = time.time()
        
        # Create event loop for this thread if needed
        def run_async_update(product_id, blob_url):
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
        
        return {'updated': self.updated, 'failed': self.failed}

def main():
    if len(sys.argv) < 2 or sys.argv[1] != '--execute':
        print("🔍 Use --execute to run association fixing")
        print("Example: python3.11 fast_association_fix.py --execute")
        return
    
    print("🚀 FAST MULTI-THREADED ASSOCIATION FIXER")
    print("=" * 50)
    
    try:
        fixer = FastAssociationFixer()
        
        # Get Azure images
        azure_images = fixer.get_azure_images()
        if not azure_images:
            return
        
        # Update associations using threads
        result = fixer.update_associations_threaded(azure_images)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"fast_association_fix_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'azure_images_count': len(azure_images),
                'update_result': result
            }, f, indent=2)
        
        print(f"📋 Report saved: {report_file}")
        print("✅ Fast association fixing completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
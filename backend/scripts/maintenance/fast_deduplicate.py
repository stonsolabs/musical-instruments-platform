#!/usr/bin/env python3
"""
Fast Multi-threaded Azure Storage Image Deduplication Script
Uses threading to delete duplicate images efficiently
"""

import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, List
from collections import defaultdict
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class FastImageDeduplicator:
    def __init__(self):
        self.deleted = 0
        self.failed = 0
        self.lock = threading.Lock()
    
    def get_all_thomann_images(self):
        """Get all thomann images from Azure storage"""
        print("🔍 Fetching all thomann images...")
        
        result = subprocess.run([
            'az', 'storage', 'blob', 'list',
            '--container-name', 'product-images',
            '--account-name', 'getyourmusicgear',
            '--prefix', 'thomann/',
            '--query', '[].{name: name, lastModified: properties.lastModified}',
            '--output', 'json'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            print(f"❌ Azure CLI error: {result.stderr}")
            return []
        
        images = json.loads(result.stdout)
        print(f"📊 Found {len(images)} thomann images")
        return images
    
    def analyze_duplicates(self, images):
        """Find duplicate images to delete (keep newest per product)"""
        product_images = defaultdict(list)
        
        for image in images:
            blob_name = image['name']
            filename = blob_name.replace('thomann/', '')
            
            match = re.match(r'^(\d+)_(\d{8}_\d{6})\.(\w+)$', filename)
            if not match:
                continue
                
            product_id = int(match.group(1))
            timestamp_str = match.group(2)
            
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
            except ValueError:
                continue
            
            product_images[product_id].append({
                'blob_name': blob_name,
                'timestamp': timestamp
            })
        
        # Find duplicates to delete (keep newest)
        to_delete = []
        duplicates_count = 0
        
        for product_id, imgs in product_images.items():
            if len(imgs) > 1:
                duplicates_count += 1
                # Sort by timestamp, newest first
                sorted_imgs = sorted(imgs, key=lambda x: x['timestamp'], reverse=True)
                # Add all but the newest to deletion list
                to_delete.extend([img['blob_name'] for img in sorted_imgs[1:]])
        
        print(f"📊 Duplicate analysis:")
        print(f"   👤 Total products: {len(product_images)}")
        print(f"   🔄 Products with duplicates: {duplicates_count}")
        print(f"   🗑️  Images to delete: {len(to_delete)}")
        
        return to_delete
    
    def delete_single_image(self, blob_name):
        """Delete a single image"""
        try:
            result = subprocess.run([
                'az', 'storage', 'blob', 'delete',
                '--container-name', 'product-images',
                '--account-name', 'getyourmusicgear',
                '--name', blob_name,
                '--delete-snapshots', 'include'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            with self.lock:
                if result.returncode == 0:
                    self.deleted += 1
                    return True
                else:
                    self.failed += 1
                    if self.failed <= 5:  # Only print first few failures
                        print(f"     ❌ Failed: {blob_name} - {result.stderr}")
                    return False
                    
        except Exception as e:
            with self.lock:
                self.failed += 1
                if self.failed <= 5:
                    print(f"     ❌ Error: {blob_name} - {e}")
            return False
    
    def delete_images_threaded(self, blob_names, max_workers=20):
        """Delete images using multiple threads"""
        print(f"🚀 Starting threaded deletion with {max_workers} workers...")
        print(f"🗑️  Deleting {len(blob_names)} duplicate images...")
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all deletion tasks
            future_to_blob = {
                executor.submit(self.delete_single_image, blob_name): blob_name 
                for blob_name in blob_names
            }
            
            # Process completed tasks and show progress
            for i, future in enumerate(as_completed(future_to_blob), 1):
                blob_name = future_to_blob[future]
                
                # Show progress every 100 deletions
                if i % 100 == 0:
                    elapsed = time.time() - start_time
                    rate = i / elapsed if elapsed > 0 else 0
                    eta = (len(blob_names) - i) / rate if rate > 0 else 0
                    print(f"   📊 Progress: {i}/{len(blob_names)} ({rate:.1f}/sec, ETA: {eta:.0f}s)")
        
        elapsed = time.time() - start_time
        print(f"\n⏱️  Total time: {elapsed:.1f} seconds")
        print(f"📊 Final results:")
        print(f"   ✅ Deleted: {self.deleted}")
        print(f"   ❌ Failed: {self.failed}")
        
        return {'deleted': self.deleted, 'failed': self.failed}

def main():
    if len(sys.argv) < 2 or sys.argv[1] != '--execute':
        print("🔍 Use --execute to run deduplication")
        print("Example: python3.11 fast_deduplicate.py --execute")
        return
    
    print("🚀 FAST MULTI-THREADED IMAGE DEDUPLICATION")
    print("=" * 50)
    
    deduplicator = FastImageDeduplicator()
    
    # Get all images
    images = deduplicator.get_all_thomann_images()
    if not images:
        return
    
    # Analyze duplicates
    to_delete = deduplicator.analyze_duplicates(images)
    if not to_delete:
        print("✅ No duplicates found")
        return
    
    # Delete using threads
    result = deduplicator.delete_images_threaded(to_delete)
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"fast_deduplication_{timestamp}.json"
    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'total_images_analyzed': len(images),
            'total_to_delete': len(to_delete),
            'deleted': result['deleted'],
            'failed': result['failed']
        }, f, indent=2)
    
    print(f"📋 Report saved: {report_file}")
    print("✅ Fast deduplication completed!")

if __name__ == "__main__":
    main()
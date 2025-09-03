#!/usr/bin/env python3
"""
Quick Azure Storage Image Deduplication Script
Efficiently removes duplicate product images using batch operations
"""

import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, List
from collections import defaultdict
import re

def get_all_thomann_images():
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

def analyze_and_get_duplicates(images):
    """Analyze duplicates and return list of images to delete"""
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
    for product_id, imgs in product_images.items():
        if len(imgs) > 1:
            # Sort by timestamp, keep newest
            sorted_imgs = sorted(imgs, key=lambda x: x['timestamp'], reverse=True)
            to_delete.extend([img['blob_name'] for img in sorted_imgs[1:]])
    
    print(f"📊 Analysis complete:")
    print(f"   👤 Unique products: {len(product_images)}")
    print(f"   🗑️  Images to delete: {len(to_delete)}")
    
    return to_delete

def delete_images_batch(blob_names, batch_size=50):
    """Delete images in batches for efficiency"""
    print(f"🗑️  Deleting {len(blob_names)} duplicate images in batches of {batch_size}...")
    
    deleted = 0
    failed = 0
    
    for i in range(0, len(blob_names), batch_size):
        batch = blob_names[i:i+batch_size]
        print(f"   Processing batch {i//batch_size + 1}/{(len(blob_names)-1)//batch_size + 1}...")
        
        for blob_name in batch:
            try:
                result = subprocess.run([
                    'az', 'storage', 'blob', 'delete',
                    '--container-name', 'product-images',
                    '--account-name', 'getyourmusicgear',
                    '--name', blob_name,
                    '--delete-snapshots', 'include'
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if result.returncode == 0:
                    deleted += 1
                else:
                    failed += 1
                    if failed <= 5:  # Only show first few failures
                        print(f"     ❌ Failed: {blob_name}")
                    
            except Exception as e:
                failed += 1
                if failed <= 5:
                    print(f"     ❌ Error: {blob_name} - {e}")
        
        print(f"     ✅ Batch complete: {deleted} deleted, {failed} failed")
    
    return {'deleted': deleted, 'failed': failed}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        print("🗑️  EXECUTING DELETION OF DUPLICATE IMAGES")
        print("=" * 50)
        
        # Get all images
        images = get_all_thomann_images()
        if not images:
            print("❌ No images found")
            return
        
        # Analyze duplicates
        to_delete = analyze_and_get_duplicates(images)
        if not to_delete:
            print("✅ No duplicates found")
            return
        
        # Delete in batches
        result = delete_images_batch(to_delete)
        
        print(f"\n📊 FINAL SUMMARY:")
        print(f"   ✅ Successfully deleted: {result['deleted']}")
        print(f"   ❌ Failed deletions: {result['failed']}")
        
        # Save simple report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"deduplication_execution_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'total_to_delete': len(to_delete),
                'deleted': result['deleted'],
                'failed': result['failed']
            }, f, indent=2)
        print(f"📋 Report saved: {report_file}")
        
    else:
        print("🔍 Use --execute to run deduplication")
        print("Example: python3.11 quick_deduplicate.py --execute")

if __name__ == "__main__":
    main()
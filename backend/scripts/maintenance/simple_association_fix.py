#!/usr/bin/env python3
"""
Simple Product Image Association Fixer
Updates products table with correct Azure image URLs
"""

import asyncio
import json
import subprocess
import sys
import re
import os
from datetime import datetime
from typing import Dict, List
from pathlib import Path

# Database connection using asyncpg directly
import asyncpg

async def get_azure_images():
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

async def update_product_associations(product_images: Dict[int, str]):
    """Update database with correct image associations"""
    print("🔧 Updating database associations...")
    
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        return
    
    # Convert to asyncpg format
    if database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql://', 1)
    
    try:
        conn = await asyncpg.connect(database_url)
        
        updated = 0
        failed = 0
        
        print(f"📊 Processing {len(product_images)} products...")
        
        for i, (product_id, blob_url) in enumerate(product_images.items(), 1):
            try:
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
                
                updated += 1
                
                if i % 100 == 0:
                    print(f"   ✅ Updated {i}/{len(product_images)} products...")
                    
            except Exception as e:
                failed += 1
                if failed <= 5:
                    print(f"   ❌ Failed product {product_id}: {e}")
        
        await conn.close()
        
        print(f"\n📊 UPDATE SUMMARY:")
        print(f"   ✅ Successfully updated: {updated}")
        print(f"   ❌ Failed updates: {failed}")
        
        return {'updated': updated, 'failed': failed}
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return {'updated': 0, 'failed': 0}

async def main():
    print("🔧 SIMPLE IMAGE ASSOCIATION FIXER")
    print("=" * 50)
    
    # Get Azure images
    azure_images = await get_azure_images()
    if not azure_images:
        print("❌ No Azure images found")
        return
    
    # Update database
    result = await update_product_associations(azure_images)
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"simple_association_fix_{timestamp}.json"
    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'azure_images_count': len(azure_images),
            'update_result': result
        }, f, indent=2)
    
    print(f"📋 Report saved: {report_file}")
    print("✅ Association fixing completed!")

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Cleanup Duplicate Images
- Find products with multiple images in blob storage
- Keep only the latest image per product
- Delete older duplicate images
- Update database to point to the latest image
"""

import asyncio
import json
import subprocess
import re
from datetime import datetime
from typing import Dict, List, Set
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Product

class ImageDuplicateCleanup:
    def __init__(self, dry_run=True):
        self.database_url = "postgresql://getyourmusicgear:arg-KDP8cjy.czu2zdv@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear"
        self.async_db_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        self.engine = None
        self.session_maker = None
        self.dry_run = dry_run
        
        # Statistics
        self.products_with_duplicates = 0
        self.total_duplicate_images = 0
        self.images_to_delete = []
        self.db_updates_needed = []

    async def initialize_db(self):
        """Initialize database connection"""
        self.engine = create_async_engine(self.async_db_url)
        self.session_maker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def close_db(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()

    def get_all_blob_images(self) -> Dict[int, List[Dict]]:
        """Get all images from blob storage organized by product ID"""
        print("📋 Loading all blob storage images...")
        
        try:
            result = subprocess.run([
                'az', 'storage', 'blob', 'list',
                '--container-name', 'product-images',
                '--account-name', 'getyourmusicgear',
                '--query', '[].{name:name,lastModified:properties.lastModified}',
                '--output', 'json'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                print(f"❌ Error loading blob storage: {result.stderr}")
                return {}
            
            blobs = json.loads(result.stdout)
            print(f"📊 Found {len(blobs)} total blobs")
            
            # Group by product ID
            product_images = {}
            
            for blob in blobs:
                blob_name = blob['name']
                if blob_name.startswith('thomann/'):
                    filename = blob_name[8:]  # Remove 'thomann/' prefix
                    
                    # Extract product ID and timestamp
                    match = re.match(r'^(\d+)_(\d{8}_\d{6})\.jpg$', filename)
                    if match:
                        product_id = int(match.group(1))
                        timestamp_str = match.group(2)
                        
                        # Parse timestamp for sorting
                        try:
                            timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                        except:
                            timestamp = datetime.now()
                        
                        if product_id not in product_images:
                            product_images[product_id] = []
                        
                        product_images[product_id].append({
                            'blob_name': blob_name,
                            'filename': filename,
                            'timestamp_str': timestamp_str,
                            'timestamp': timestamp,
                            'last_modified': blob['lastModified'],
                            'url': f"https://getyourmusicgear.blob.core.windows.net/product-images/{blob_name}"
                        })
            
            # Sort images by timestamp for each product (newest first)
            for product_id in product_images:
                product_images[product_id].sort(key=lambda x: x['timestamp'], reverse=True)
            
            return product_images
            
        except Exception as e:
            print(f"❌ Error loading blob storage: {e}")
            return {}

    def analyze_duplicates(self, product_images: Dict[int, List[Dict]]) -> Dict:
        """Analyze which products have duplicate images"""
        print("\n🔍 Analyzing duplicate images...")
        
        duplicates = {}
        single_images = {}
        
        for product_id, images in product_images.items():
            if len(images) > 1:
                # Multiple images - keep latest, mark others for deletion
                latest_image = images[0]  # Already sorted newest first
                old_images = images[1:]
                
                duplicates[product_id] = {
                    'latest_image': latest_image,
                    'old_images': old_images,
                    'total_images': len(images)
                }
                
                self.products_with_duplicates += 1
                self.total_duplicate_images += len(old_images)
                
            else:
                # Single image - keep as is
                single_images[product_id] = images[0]
        
        print(f"📊 DUPLICATE ANALYSIS:")
        print(f"   ✅ Products with single image: {len(single_images)}")
        print(f"   📁 Products with duplicates: {len(duplicates)}")
        print(f"   🗑️  Total duplicate images to remove: {self.total_duplicate_images}")
        
        return {
            'duplicates': duplicates,
            'single_images': single_images
        }

    def plan_cleanup(self, analysis: Dict):
        """Plan the cleanup operations"""
        print("\n📋 Planning cleanup operations...")
        
        duplicates = analysis['duplicates']
        
        # Plan blob deletions
        for product_id, data in duplicates.items():
            for old_image in data['old_images']:
                self.images_to_delete.append({
                    'product_id': product_id,
                    'blob_name': old_image['blob_name'],
                    'url': old_image['url'],
                    'timestamp': old_image['timestamp_str']
                })
        
        print(f"🗑️  Planned blob deletions: {len(self.images_to_delete)}")
        
        # Show examples
        if self.images_to_delete:
            print(f"\n📋 Examples of images to delete:")
            for i, img in enumerate(self.images_to_delete[:10]):
                print(f"   {i+1}. Product {img['product_id']}: {img['blob_name']}")
            if len(self.images_to_delete) > 10:
                print(f"   ... and {len(self.images_to_delete) - 10} more")

    def execute_blob_cleanup(self):
        """Delete duplicate blob images"""
        if not self.images_to_delete:
            print("✅ No duplicate images to delete")
            return
        
        if self.dry_run:
            print(f"\n🔍 DRY RUN: Would delete {len(self.images_to_delete)} duplicate images")
            return
        
        print(f"\n🗑️  Deleting {len(self.images_to_delete)} duplicate images...")
        
        deleted_count = 0
        failed_count = 0
        
        for img in self.images_to_delete:
            try:
                result = subprocess.run([
                    'az', 'storage', 'blob', 'delete',
                    '--container-name', 'product-images',
                    '--name', img['blob_name'],
                    '--account-name', 'getyourmusicgear'
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    deleted_count += 1
                    if deleted_count % 100 == 0:
                        print(f"   🗑️  Deleted {deleted_count}/{len(self.images_to_delete)} images...")
                else:
                    failed_count += 1
                    print(f"   ❌ Failed to delete {img['blob_name']}: {result.stderr}")
                
            except Exception as e:
                failed_count += 1
                print(f"   ❌ Error deleting {img['blob_name']}: {e}")
        
        print(f"\n📊 CLEANUP RESULTS:")
        print(f"   ✅ Successfully deleted: {deleted_count}")
        print(f"   ❌ Failed to delete: {failed_count}")

    async def update_database_urls(self, analysis: Dict):
        """Update database to point to the latest image for each product"""
        duplicates = analysis['duplicates']
        
        if not duplicates:
            print("✅ No database updates needed")
            return
        
        print(f"\n💾 Updating database URLs for {len(duplicates)} products...")
        
        if self.dry_run:
            print("🔍 DRY RUN: Would update database URLs")
            return
        
        async with self.session_maker() as session:
            updated_count = 0
            failed_count = 0
            
            for product_id, data in duplicates.items():
                try:
                    latest_image = data['latest_image']
                    latest_url = latest_image['url']
                    
                    # Get current product
                    query = text("SELECT images FROM products WHERE id = :product_id")
                    result = await session.execute(query, {"product_id": product_id})
                    row = result.fetchone()
                    
                    if row and row.images:
                        current_images = row.images
                        
                        # Update the main image URL
                        updated_images = current_images.copy()
                        
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
                                updated_images[main_key]['url'] = latest_url
                            else:
                                updated_images[main_key] = latest_url
                            
                            # Update database
                            update_query = text("""
                                UPDATE products 
                                SET images = :images, updated_at = NOW()
                                WHERE id = :product_id
                            """)
                            await session.execute(update_query, {
                                "images": json.dumps(updated_images),
                                "product_id": product_id
                            })
                            
                            updated_count += 1
                            
                            if updated_count % 100 == 0:
                                await session.commit()
                                print(f"   💾 Updated {updated_count}/{len(duplicates)} products...")
                
                except Exception as e:
                    failed_count += 1
                    print(f"   ❌ Failed to update product {product_id}: {e}")
            
            await session.commit()
            
            print(f"\n📊 DATABASE UPDATE RESULTS:")
            print(f"   ✅ Successfully updated: {updated_count}")
            print(f"   ❌ Failed to update: {failed_count}")

    def generate_report(self, analysis: Dict):
        """Generate cleanup report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"image_cleanup_report_{timestamp}.json"
        
        report = {
            "cleanup_timestamp": datetime.now().isoformat(),
            "dry_run": self.dry_run,
            "statistics": {
                "products_with_duplicates": self.products_with_duplicates,
                "total_duplicate_images": self.total_duplicate_images,
                "products_with_single_image": len(analysis['single_images'])
            },
            "duplicates_found": analysis['duplicates'],
            "planned_deletions": self.images_to_delete
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n💾 Cleanup report saved to: {filename}")

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Cleanup duplicate product images')
    parser.add_argument(
        '--execute', 
        action='store_true',
        help='Actually perform the cleanup (default is dry run)'
    )
    parser.add_argument(
        '--blob-only', 
        action='store_true',
        help='Only clean up blob storage, skip database updates'
    )
    
    args = parser.parse_args()
    
    dry_run = not args.execute
    
    print("🧹 IMAGE DUPLICATE CLEANUP")
    print("=" * 40)
    if dry_run:
        print("🔍 DRY RUN MODE - No actual changes will be made")
    else:
        print("⚠️  EXECUTE MODE - Changes will be applied!")
    print()
    
    cleanup = ImageDuplicateCleanup(dry_run=dry_run)
    
    try:
        await cleanup.initialize_db()
        
        # Get all blob images
        product_images = cleanup.get_all_blob_images()
        if not product_images:
            print("❌ Could not load blob storage images")
            return
        
        # Analyze duplicates
        analysis = cleanup.analyze_duplicates(product_images)
        
        # Plan cleanup
        cleanup.plan_cleanup(analysis)
        
        # Generate report
        cleanup.generate_report(analysis)
        
        if cleanup.products_with_duplicates > 0:
            if not dry_run:
                # Execute cleanup
                print(f"\n🚀 EXECUTING CLEANUP...")
                cleanup.execute_blob_cleanup()
                
                if not args.blob_only:
                    await cleanup.update_database_urls(analysis)
            
            print(f"\n📊 FINAL SUMMARY:")
            print(f"   Products with duplicates: {cleanup.products_with_duplicates}")
            print(f"   Duplicate images to remove: {cleanup.total_duplicate_images}")
            print(f"   Storage saved: ~{cleanup.total_duplicate_images * 0.5:.1f} MB (estimated)")
        else:
            print("🎉 No duplicate images found! All products have single images.")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await cleanup.close_db()

if __name__ == "__main__":
    asyncio.run(main())

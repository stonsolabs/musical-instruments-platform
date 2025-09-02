#!/usr/bin/env python3
"""
Cleanup Duplicate Images Script
Removes duplicate images from Azure Storage, keeping only the latest one per product.
"""

import asyncio
import os
import re
from azure.storage.blob import BlobServiceClient
from typing import Dict, List
from dotenv import load_dotenv
from datetime import datetime

class ImageCleanup:
    def __init__(self):
        load_dotenv()
        
        # Azure Storage connection
        self.storage_connection = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if not self.storage_connection:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING not found in environment variables")
        
        self.container_name = os.getenv('AZURE_STORAGE_CONTAINER', 'product-images')
        self.blob_client = BlobServiceClient.from_connection_string(self.storage_connection)
        
    def get_all_thomann_images(self) -> Dict[str, List[Dict]]:
        """Get all Thomann images grouped by product slug"""
        container_client = self.blob_client.get_container_client(self.container_name)
        
        images_by_slug = {}
        blob_list = container_client.list_blobs(name_starts_with="thomann/")
        
        for blob in blob_list:
            # Extract info from blob name: thomann/{product_slug}_{timestamp}.jpg
            blob_name = blob.name
            match = re.match(r'thomann/([^_]+(?:-[^_]*)*?)_(\d{8}_\d{6})\.jpg$', blob_name)
            
            if match:
                product_slug = match.group(1)
                timestamp = match.group(2)
                
                if product_slug not in images_by_slug:
                    images_by_slug[product_slug] = []
                
                images_by_slug[product_slug].append({
                    'blob_name': blob_name,
                    'product_slug': product_slug,
                    'timestamp': timestamp,
                    'timestamp_dt': datetime.strptime(timestamp, '%Y%m%d_%H%M%S'),
                    'size': blob.size,
                    'last_modified': blob.last_modified,
                    'url': f"https://{self.blob_client.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}"
                })
        
        return images_by_slug
    
    def identify_duplicates(self, images_by_slug: Dict[str, List[Dict]]) -> Dict[str, Dict]:
        """Identify which images to keep and which to delete"""
        cleanup_plan = {}
        
        for slug, images in images_by_slug.items():
            if len(images) > 1:
                # Sort by timestamp (newest first)
                images.sort(key=lambda x: x['timestamp_dt'], reverse=True)
                
                # Keep the newest image, delete the rest
                keep_image = images[0]
                delete_images = images[1:]
                
                cleanup_plan[slug] = {
                    'product_slug': slug,
                    'total_images': len(images),
                    'keep': keep_image,
                    'delete': delete_images,
                    'bytes_to_free': sum(img['size'] for img in delete_images)
                }
        
        return cleanup_plan
    
    def delete_blob(self, blob_name: str) -> bool:
        """Delete a single blob"""
        try:
            container_client = self.blob_client.get_container_client(self.container_name)
            container_client.delete_blob(blob_name)
            return True
        except Exception as e:
            print(f"❌ Error deleting {blob_name}: {e}")
            return False
    
    async def cleanup_duplicates(self, dry_run: bool = True):
        """Main cleanup function"""
        print("🧹 Starting Duplicate Image Cleanup...")
        print("=" * 60)
        
        if dry_run:
            print("🧪 DRY RUN MODE - No files will be deleted")
        else:
            print("⚡ LIVE MODE - Files will be permanently deleted")
        print()
        
        # Get all images
        print("☁️ Fetching all Thomann images from Azure Storage...")
        images_by_slug = self.get_all_thomann_images()
        
        # Identify duplicates
        print("🔍 Analyzing for duplicates...")
        cleanup_plan = self.identify_duplicates(images_by_slug)
        
        # Statistics
        total_images = sum(len(images) for images in images_by_slug.values())
        unique_products = len(images_by_slug)
        products_with_duplicates = len(cleanup_plan)
        total_duplicates = sum(len(plan['delete']) for plan in cleanup_plan.values())
        total_bytes_to_free = sum(plan['bytes_to_free'] for plan in cleanup_plan.values())
        
        print(f"📊 ANALYSIS RESULTS:")
        print(f"Total images found: {total_images:,}")
        print(f"Unique products: {unique_products:,}")
        print(f"Products with duplicates: {products_with_duplicates:,}")
        print(f"Duplicate images to delete: {total_duplicates:,}")
        print(f"Storage space to free: {total_bytes_to_free/1024/1024:.1f} MB")
        print()
        
        if not cleanup_plan:
            print("✅ No duplicate images found!")
            return
        
        # Show some examples
        print("🔍 Examples of products with duplicates (first 10):")
        for i, (slug, plan) in enumerate(list(cleanup_plan.items())[:10], 1):
            print(f"  {i:2d}. {slug} ({plan['total_images']} images → keep 1, delete {len(plan['delete'])})")
            print(f"      Keep: {plan['keep']['blob_name']}")
            for j, img in enumerate(plan['delete'][:2], 1):  # Show first 2 to delete
                print(f"      Del{j}: {img['blob_name']}")
            if len(plan['delete']) > 2:
                print(f"      ... and {len(plan['delete']) - 2} more")
            print()
        
        if len(cleanup_plan) > 10:
            print(f"      ... and {len(cleanup_plan) - 10} more products with duplicates")
        
        print()
        
        if dry_run:
            print("🧪 DRY RUN - No files deleted. Run with --live to apply cleanup.")
            return
        
        # Confirm before proceeding
        print("⚠️  This will permanently delete duplicate images from Azure Storage!")
        print(f"   {total_duplicates:,} files will be deleted, freeing {total_bytes_to_free/1024/1024:.1f} MB")
        print("   Type 'DELETE' (all caps) to proceed:")
        
        # For script automation, we'll add a parameter
        proceed = input().strip()
        if proceed != 'DELETE':
            print("❌ Operation cancelled.")
            return
        
        # Perform the cleanup
        print("\n🗑️ Deleting duplicate images...")
        success_count = 0
        error_count = 0
        bytes_freed = 0
        
        for i, (slug, plan) in enumerate(cleanup_plan.items(), 1):
            print(f"  [{i:3d}/{len(cleanup_plan)}] Cleaning {slug} ({len(plan['delete'])} duplicates)...")
            
            for img in plan['delete']:
                success = self.delete_blob(img['blob_name'])
                if success:
                    success_count += 1
                    bytes_freed += img['size']
                    print(f"      ✅ Deleted {img['blob_name']}")
                else:
                    error_count += 1
                    print(f"      ❌ Failed to delete {img['blob_name']}")
        
        print(f"\n🎯 CLEANUP RESULTS:")
        print(f"✅ Successfully deleted: {success_count:,} files")
        print(f"❌ Errors: {error_count:,} files")
        print(f"💾 Storage space freed: {bytes_freed/1024/1024:.1f} MB")
        print(f"📊 Success rate: {(success_count/(success_count+error_count)*100):.1f}%")
        
        if success_count > 0:
            print(f"\n✨ Cleanup complete! Kept 1 image per product, removed {success_count:,} duplicates.")

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Clean up duplicate images in Azure Storage')
    parser.add_argument('--live', action='store_true', help='Actually delete files (default is dry-run)')
    parser.add_argument('--auto-confirm', action='store_true', help='Skip confirmation prompt for automation')
    
    args = parser.parse_args()
    
    cleanup = ImageCleanup()
    
    # Override input for automation
    if args.auto_confirm and args.live:
        import builtins
        original_input = builtins.input
        builtins.input = lambda x='': 'DELETE'
        
        try:
            await cleanup.cleanup_duplicates(dry_run=False)
        finally:
            builtins.input = original_input
    else:
        await cleanup.cleanup_duplicates(dry_run=not args.live)

if __name__ == "__main__":
    asyncio.run(main())

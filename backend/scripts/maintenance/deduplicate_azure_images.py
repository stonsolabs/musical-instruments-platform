#!/usr/bin/env python3
"""
Azure Storage Image Deduplication Script
Removes duplicate product images, keeping only the newest image per product
"""

import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Set
from collections import defaultdict
import re

class ImageDeduplicator:
    """Deduplicates images in Azure blob storage"""
    
    def __init__(self, container_name: str = "product-images", account_name: str = "getyourmusicgear"):
        self.container_name = container_name
        self.account_name = account_name
        self.dry_run = True
        
    def get_all_thomann_images(self) -> List[Dict]:
        """Get all thomann images from Azure storage"""
        print("🔍 Fetching all thomann images from Azure storage...")
        
        try:
            result = subprocess.run([
                'az', 'storage', 'blob', 'list',
                '--container-name', self.container_name,
                '--account-name', self.account_name,
                '--prefix', 'thomann/',
                '--query', '[].{name: name, lastModified: properties.lastModified}',
                '--output', 'json'
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                raise Exception(f"Azure CLI error: {result.stderr}")
            
            images = json.loads(result.stdout)
            print(f"📊 Found {len(images)} thomann images in storage")
            return images
            
        except Exception as e:
            print(f"❌ Error fetching images: {e}")
            return []
    
    def parse_image_info(self, blob_name: str) -> Dict:
        """Parse product_id and timestamp from blob name"""
        # Expected format: thomann/{product_id}_{timestamp}.jpg
        filename = blob_name.replace('thomann/', '')
        
        match = re.match(r'^(\d+)_(\d{8}_\d{6})\.(\w+)$', filename)
        if not match:
            return None
            
        product_id = int(match.group(1))
        timestamp_str = match.group(2)
        extension = match.group(3)
        
        # Parse timestamp: YYYYMMDD_HHMMSS
        try:
            timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
        except ValueError:
            return None
        
        return {
            'product_id': product_id,
            'timestamp': timestamp,
            'extension': extension,
            'blob_name': blob_name,
            'filename': filename
        }
    
    def analyze_duplicates(self, images: List[Dict]) -> Dict:
        """Analyze duplicate images per product"""
        product_images = defaultdict(list)
        unparseable = []
        
        for image in images:
            blob_name = image['name']
            parsed = self.parse_image_info(blob_name)
            
            if parsed:
                product_images[parsed['product_id']].append({
                    'blob_name': blob_name,
                    'timestamp': parsed['timestamp'],
                    'last_modified': image['lastModified']
                })
            else:
                unparseable.append(blob_name)
        
        # Find products with duplicates
        duplicates = {pid: imgs for pid, imgs in product_images.items() if len(imgs) > 1}
        singles = {pid: imgs for pid, imgs in product_images.items() if len(imgs) == 1}
        
        total_duplicates = sum(len(imgs) - 1 for imgs in duplicates.values())
        
        print(f"📊 DUPLICATE ANALYSIS:")
        print(f"   👤 Unique products: {len(product_images)}")
        print(f"   🔄 Products with duplicates: {len(duplicates)}")
        print(f"   ✅ Products with single image: {len(singles)}")
        print(f"   🗑️  Extra images to remove: {total_duplicates}")
        print(f"   ❓ Unparseable filenames: {len(unparseable)}")
        
        if unparseable:
            print("\n❓ Unparseable filenames:")
            for name in unparseable[:10]:
                print(f"   - {name}")
            if len(unparseable) > 10:
                print(f"   ... and {len(unparseable) - 10} more")
        
        return {
            'duplicates': duplicates,
            'singles': singles,
            'unparseable': unparseable,
            'stats': {
                'unique_products': len(product_images),
                'products_with_duplicates': len(duplicates),
                'products_with_single_image': len(singles),
                'total_extra_images': total_duplicates,
                'unparseable_count': len(unparseable)
            }
        }
    
    def plan_cleanup(self, analysis: Dict) -> Dict:
        """Plan which images to keep vs delete"""
        duplicates = analysis['duplicates']
        to_delete = []
        to_keep = []
        
        for product_id, images in duplicates.items():
            # Sort by timestamp (newest first)
            sorted_images = sorted(images, key=lambda x: x['timestamp'], reverse=True)
            
            # Keep the newest image
            newest = sorted_images[0]
            to_keep.append({
                'product_id': product_id,
                'blob_name': newest['blob_name'],
                'timestamp': newest['timestamp']
            })
            
            # Mark older images for deletion
            for img in sorted_images[1:]:
                to_delete.append({
                    'product_id': product_id,
                    'blob_name': img['blob_name'],
                    'timestamp': img['timestamp']
                })
        
        print(f"\n🗂️  CLEANUP PLAN:")
        print(f"   ✅ Images to keep: {len(to_keep)}")
        print(f"   🗑️  Images to delete: {len(to_delete)}")
        
        return {
            'to_keep': to_keep,
            'to_delete': to_delete
        }
    
    def execute_cleanup(self, cleanup_plan: Dict, dry_run: bool = True) -> Dict:
        """Execute the cleanup plan"""
        to_delete = cleanup_plan['to_delete']
        
        if dry_run:
            print(f"\n🔍 DRY RUN MODE - Would delete {len(to_delete)} images:")
            for i, img in enumerate(to_delete[:10], 1):
                print(f"   {i}. {img['blob_name']} (Product {img['product_id']})")
            if len(to_delete) > 10:
                print(f"   ... and {len(to_delete) - 10} more")
            return {'deleted': 0, 'failed': 0}
        
        print(f"\n🗑️  DELETING {len(to_delete)} duplicate images...")
        deleted = 0
        failed = 0
        
        for i, img in enumerate(to_delete, 1):
            try:
                result = subprocess.run([
                    'az', 'storage', 'blob', 'delete',
                    '--container-name', self.container_name,
                    '--account-name', self.account_name,
                    '--name', img['blob_name'],
                    '--delete-snapshots', 'include'
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if result.returncode == 0:
                    deleted += 1
                    if i % 50 == 0:
                        print(f"   ✅ Deleted {i}/{len(to_delete)} images...")
                else:
                    print(f"   ❌ Failed to delete {img['blob_name']}: {result.stderr}")
                    failed += 1
                    
            except Exception as e:
                print(f"   ❌ Error deleting {img['blob_name']}: {e}")
                failed += 1
        
        print(f"\n📊 DELETION SUMMARY:")
        print(f"   ✅ Successfully deleted: {deleted}")
        print(f"   ❌ Failed deletions: {failed}")
        
        return {'deleted': deleted, 'failed': failed}
    
    def save_report(self, analysis: Dict, cleanup_plan: Dict, execution_result: Dict = None):
        """Save detailed report of the operation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_deduplication_report_{timestamp}.json"
        
        report = {
            'timestamp': timestamp,
            'analysis': analysis,
            'cleanup_plan': {
                'to_keep_count': len(cleanup_plan['to_keep']),
                'to_delete_count': len(cleanup_plan['to_delete']),
                'sample_deletions': cleanup_plan['to_delete'][:20]  # Sample for verification
            }
        }
        
        if execution_result:
            report['execution_result'] = execution_result
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📋 Report saved to: {filename}")
        return filename

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deduplicate product images in Azure storage')
    parser.add_argument('--execute', action='store_true', 
                       help='Actually delete duplicate images (default is dry-run)')
    parser.add_argument('--container', default='product-images', 
                       help='Azure storage container name')
    parser.add_argument('--account', default='getyourmusicgear', 
                       help='Azure storage account name')
    parser.add_argument('--yes', action='store_true',
                       help='Skip confirmation prompt')
    
    args = parser.parse_args()
    
    print("🧹 AZURE IMAGE DEDUPLICATION TOOL")
    print("=" * 50)
    
    if not args.execute:
        print("🔍 Running in DRY-RUN mode (use --execute to actually delete)")
    else:
        print("⚠️  EXECUTING DELETIONS - This will permanently remove duplicate images!")
        if not args.yes:
            confirm = input("Are you sure? Type 'yes' to continue: ")
            if confirm.lower() != 'yes':
                print("❌ Aborted by user")
                sys.exit(1)
    
    deduplicator = ImageDeduplicator(args.container, args.account)
    
    # Step 1: Get all images
    images = deduplicator.get_all_thomann_images()
    if not images:
        print("❌ No images found or error fetching images")
        sys.exit(1)
    
    # Step 2: Analyze duplicates
    analysis = deduplicator.analyze_duplicates(images)
    
    # Step 3: Plan cleanup
    cleanup_plan = deduplicator.plan_cleanup(analysis)
    
    # Step 4: Execute or dry-run
    execution_result = deduplicator.execute_cleanup(cleanup_plan, dry_run=not args.execute)
    
    # Step 5: Save report
    deduplicator.save_report(analysis, cleanup_plan, execution_result)
    
    print(f"\n✅ Deduplication {'completed' if args.execute else 'planned'}!")

if __name__ == "__main__":
    main()
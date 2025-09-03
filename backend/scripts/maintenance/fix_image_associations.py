#!/usr/bin/env python3
"""
Product Image Association Fixer
After deduplication, this script updates the products table to associate each product 
with its correct remaining image in Azure storage
"""

import asyncio
import json
import subprocess
import sys
import re
from datetime import datetime
from typing import Dict, List, Set, Optional
from pathlib import Path

# Add current directory to path for app imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from app.database import async_session_factory
    from app.config import settings
except ImportError as e:
    print(f"❌ Could not import database modules: {e}")
    print("Make sure you're running from the backend directory and app/ exists.")
    sys.exit(1)

class ImageAssociationFixer:
    """Fixes product-image associations in the database"""
    
    def __init__(self, container_name: str = "product-images", account_name: str = "getyourmusicgear"):
        self.container_name = container_name
        self.account_name = account_name
        self.db_session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.db_session = async_session_factory()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.db_session:
            await self.db_session.close()
    
    def get_current_azure_images(self) -> Dict[int, str]:
        """Get current mapping of product_id -> blob_url from Azure storage"""
        print("🔍 Fetching current images from Azure storage...")
        
        try:
            result = subprocess.run([
                'az', 'storage', 'blob', 'list',
                '--container-name', self.container_name,
                '--account-name', self.account_name,
                '--prefix', 'thomann/',
                '--query', '[].{name: name, url: url}',
                '--output', 'json'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Azure CLI error: {result.stderr}")
            
            blobs = json.loads(result.stdout)
            product_images = {}
            
            for blob in blobs:
                blob_name = blob['name']
                blob_url = blob['url']
                
                # Parse product ID from blob name: thomann/{product_id}_{timestamp}.jpg
                filename = blob_name.replace('thomann/', '')
                match = re.match(r'^(\d+)_', filename)
                
                if match:
                    product_id = int(match.group(1))
                    product_images[product_id] = blob_url
                else:
                    print(f"⚠️  Could not parse product ID from: {blob_name}")
            
            print(f"✅ Found {len(product_images)} product images in Azure storage")
            return product_images
            
        except Exception as e:
            print(f"❌ Error fetching Azure images: {e}")
            return {}
    
    async def get_current_database_associations(self) -> Dict[int, Dict]:
        """Get current image associations from the database"""
        print("🔍 Fetching current database image associations...")
        
        if not self.db_session:
            print("❌ Database session not available")
            return {}
        
        try:
            from sqlalchemy import text
            
            query = text("""
                SELECT id, images
                FROM products
                WHERE images IS NOT NULL
                AND images != '{}'::jsonb
                ORDER BY id
            """)
            
            result = await self.db_session.execute(query)
            rows = result.fetchall()
            db_associations = {}
            
            for row in rows:
                product_id = row.id
                images = row.images
                
                # Parse images JSON if it's a string
                if isinstance(images, str):
                    try:
                        images = json.loads(images)
                    except:
                        continue
                
                if isinstance(images, dict) and images:
                    db_associations[product_id] = images
            
            print(f"✅ Found {len(db_associations)} products with image data in database")
            return db_associations
            
        except Exception as e:
            print(f"❌ Error fetching database associations: {e}")
            return {}
    
    def analyze_mismatches(self, azure_images: Dict[int, str], db_associations: Dict[int, Dict]) -> Dict:
        """Analyze mismatches between Azure storage and database"""
        
        # Products that have images in Azure but not in DB
        azure_only = set(azure_images.keys()) - set(db_associations.keys())
        
        # Products that have images in DB but not in Azure  
        db_only = set(db_associations.keys()) - set(azure_images.keys())
        
        # Products that have images in both but URLs don't match
        url_mismatches = []
        correct_associations = []
        
        for product_id in set(azure_images.keys()) & set(db_associations.keys()):
            azure_url = azure_images[product_id]
            db_images = db_associations[product_id]
            
            # Check if the Azure URL matches the database URL
            thomann_main = db_images.get('thomann_main')
            if thomann_main:
                db_url = thomann_main.get('url') if isinstance(thomann_main, dict) else thomann_main
                
                if db_url != azure_url:
                    url_mismatches.append({
                        'product_id': product_id,
                        'azure_url': azure_url,
                        'db_url': db_url
                    })
                else:
                    correct_associations.append(product_id)
            else:
                # No thomann_main in database, but image exists in Azure
                azure_only.add(product_id)
        
        print(f"\n📊 ASSOCIATION ANALYSIS:")
        print(f"   ✅ Correct associations: {len(correct_associations)}")
        print(f"   🔄 URL mismatches: {len(url_mismatches)}")
        print(f"   ☁️  Azure only (missing in DB): {len(azure_only)}")
        print(f"   💾 DB only (broken links): {len(db_only)}")
        
        return {
            'correct_associations': correct_associations,
            'url_mismatches': url_mismatches,
            'azure_only': azure_only,
            'db_only': db_only
        }
    
    async def fix_associations(self, azure_images: Dict[int, str], mismatches: Dict, dry_run: bool = True) -> Dict:
        """Fix the image associations in the database"""
        
        # Products that need fixing
        needs_fixing = []
        
        # Add URL mismatches
        for mismatch in mismatches['url_mismatches']:
            needs_fixing.append({
                'product_id': mismatch['product_id'],
                'new_url': mismatch['azure_url'],
                'reason': 'URL mismatch'
            })
        
        # Add Azure-only products (missing in DB)
        for product_id in mismatches['azure_only']:
            if product_id in azure_images:
                needs_fixing.append({
                    'product_id': product_id,
                    'new_url': azure_images[product_id],
                    'reason': 'Missing in DB'
                })
        
        print(f"\n🔧 FIXING {len(needs_fixing)} ASSOCIATIONS:")
        
        if dry_run:
            print("🔍 DRY RUN MODE - Would fix these associations:")
            for i, fix in enumerate(needs_fixing[:10], 1):
                print(f"   {i}. Product {fix['product_id']}: {fix['reason']}")
            if len(needs_fixing) > 10:
                print(f"   ... and {len(needs_fixing) - 10} more")
            return {'fixed': 0, 'failed': 0}
        
        if not self.db_session:
            print("❌ Database session not available")
            return {'fixed': 0, 'failed': 0}
        
        fixed = 0
        failed = 0
        
        for i, fix in enumerate(needs_fixing, 1):
            try:
                product_id = fix['product_id']
                new_url = fix['new_url']
                
                # Create new thomann_main image object
                image_data = {
                    "url": new_url,
                    "source": "thomann",
                    "downloaded_at": datetime.utcnow().isoformat(),
                    "type": "main",
                    "fixed_at": datetime.utcnow().isoformat()
                }
                
                from sqlalchemy import text
                
                # Replace entire images column content with only the new association
                update_query = text("""
                    UPDATE products 
                    SET images = :images::jsonb,
                        updated_at = NOW()
                    WHERE id = :product_id
                """)
                
                # Only keep the thomann_main image, remove all other content
                new_images = {
                    "thomann_main": image_data
                }
                
                await self.db_session.execute(update_query, {
                    'images': json.dumps(new_images),
                    'product_id': product_id
                })
                await self.db_session.commit()
                
                fixed += 1
                if i % 50 == 0:
                    print(f"   ✅ Fixed {i}/{len(needs_fixing)} associations...")
                    
            except Exception as e:
                print(f"   ❌ Failed to fix product {fix['product_id']}: {e}")
                failed += 1
        
        print(f"\n📊 FIXING SUMMARY:")
        print(f"   ✅ Successfully fixed: {fixed}")
        print(f"   ❌ Failed fixes: {failed}")
        
        return {'fixed': fixed, 'failed': failed}
    
    async def remove_broken_associations(self, mismatches: Dict, dry_run: bool = True) -> Dict:
        """Remove associations for products that don't have images in Azure"""
        
        broken_products = list(mismatches['db_only'])
        
        if not broken_products:
            print("✅ No broken associations to remove")
            return {'removed': 0, 'failed': 0}
        
        print(f"\n🧹 REMOVING {len(broken_products)} BROKEN ASSOCIATIONS:")
        
        if dry_run:
            print("🔍 DRY RUN MODE - Would remove associations for these products:")
            for i, product_id in enumerate(broken_products[:10], 1):
                print(f"   {i}. Product {product_id}")
            if len(broken_products) > 10:
                print(f"   ... and {len(broken_products) - 10} more")
            return {'removed': 0, 'failed': 0}
        
        if not self.db_session:
            print("❌ Database session not available")
            return {'removed': 0, 'failed': 0}
        
        removed = 0
        failed = 0
        
        for i, product_id in enumerate(broken_products, 1):
            try:
                from sqlalchemy import text
                
                # Clear the images column (set to empty JSON object)
                update_query = text("""
                    UPDATE products 
                    SET images = '{}'::jsonb,
                        updated_at = NOW()
                    WHERE id = :product_id
                """)
                
                await self.db_session.execute(update_query, {'product_id': product_id})
                await self.db_session.commit()
                
                removed += 1
                if i % 50 == 0:
                    print(f"   🧹 Removed {i}/{len(broken_products)} broken associations...")
                    
            except Exception as e:
                print(f"   ❌ Failed to remove association for product {product_id}: {e}")
                failed += 1
        
        print(f"\n📊 REMOVAL SUMMARY:")
        print(f"   ✅ Successfully removed: {removed}")
        print(f"   ❌ Failed removals: {failed}")
        
        return {'removed': removed, 'failed': failed}
    
    def save_report(self, azure_images: Dict, db_associations: Dict, mismatches: Dict, 
                   fix_result: Dict = None, removal_result: Dict = None):
        """Save detailed report of the operation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_association_fix_report_{timestamp}.json"
        
        report = {
            'timestamp': timestamp,
            'azure_images_count': len(azure_images),
            'db_associations_count': len(db_associations),
            'mismatches_analysis': {
                'correct_associations': len(mismatches['correct_associations']),
                'url_mismatches': len(mismatches['url_mismatches']),
                'azure_only': len(mismatches['azure_only']),
                'db_only': len(mismatches['db_only'])
            },
            'sample_fixes': {
                'url_mismatches': mismatches['url_mismatches'][:10],
                'azure_only': list(mismatches['azure_only'])[:10],
                'db_only': list(mismatches['db_only'])[:10]
            }
        }
        
        if fix_result:
            report['fix_result'] = fix_result
            
        if removal_result:
            report['removal_result'] = removal_result
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📋 Report saved to: {filename}")
        return filename

async def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix product image associations in database')
    parser.add_argument('--execute', action='store_true', 
                       help='Actually update database associations (default is dry-run)')
    parser.add_argument('--container', default='product-images', 
                       help='Azure storage container name')
    parser.add_argument('--account', default='getyourmusicgear', 
                       help='Azure storage account name')
    parser.add_argument('--remove-broken', action='store_true',
                       help='Also remove broken associations (images column for products without Azure images)')
    parser.add_argument('--yes', action='store_true',
                       help='Skip confirmation prompt')
    
    args = parser.parse_args()
    
    print("🔧 PRODUCT IMAGE ASSOCIATION FIXER")
    print("=" * 50)
    
    if not args.execute:
        print("🔍 Running in DRY-RUN mode (use --execute to actually update database)")
    else:
        print("⚠️  EXECUTING DATABASE UPDATES - This will modify product image associations!")
        if not args.yes:
            confirm = input("Are you sure? Type 'yes' to continue: ")
            if confirm.lower() != 'yes':
                print("❌ Aborted by user")
                sys.exit(1)
    
    async with ImageAssociationFixer(args.container, args.account) as fixer:
        # Step 1: Get current Azure images
        azure_images = fixer.get_current_azure_images()
        if not azure_images:
            print("❌ No Azure images found or error fetching images")
            sys.exit(1)
        
        # Step 2: Get current database associations
        db_associations = await fixer.get_current_database_associations()
        
        # Step 3: Analyze mismatches
        mismatches = fixer.analyze_mismatches(azure_images, db_associations)
        
        # Step 4: Fix associations
        fix_result = await fixer.fix_associations(azure_images, mismatches, dry_run=not args.execute)
        
        # Step 5: Remove broken associations if requested
        removal_result = None
        if args.remove_broken:
            removal_result = await fixer.remove_broken_associations(mismatches, dry_run=not args.execute)
        
        # Step 6: Save report
        fixer.save_report(azure_images, db_associations, mismatches, fix_result, removal_result)
        
        print(f"\n✅ Association fixing {'completed' if args.execute else 'planned'}!")

if __name__ == "__main__":
    asyncio.run(main())
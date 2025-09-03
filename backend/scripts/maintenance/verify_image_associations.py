#!/usr/bin/env python3
"""
Verify Image Associations with Correct Naming Pattern
- Check actual blob storage filenames vs database URLs
- Use the proper naming pattern: thomann/{product_id}_{timestamp}.jpg
- Get accurate count of properly associated images
"""

import asyncio
import json
import subprocess
import re
from datetime import datetime
from typing import Dict, List, Set, Tuple
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Product

class ImageAssociationVerifier:
    def __init__(self):
        self.database_url = "postgresql://getyourmusicgear:arg-KDP8cjy.czu2zdv@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear"
        self.async_db_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        self.engine = None
        self.session_maker = None

    async def initialize_db(self):
        """Initialize database connection"""
        self.engine = create_async_engine(self.async_db_url)
        self.session_maker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def close_db(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()

    def get_blob_storage_files(self) -> Dict[int, List[str]]:
        """Get all files from Azure blob storage organized by product ID"""
        print("📋 Loading Azure blob storage files...")
        
        try:
            result = subprocess.run([
                'az', 'storage', 'blob', 'list',
                '--container-name', 'product-images',
                '--account-name', 'getyourmusicgear',
                '--query', '[].name',
                '--output', 'json'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                print(f"❌ Error loading blob storage: {result.stderr}")
                return {}
            
            blob_names = json.loads(result.stdout)
            print(f"📊 Found {len(blob_names)} total blobs in storage")
            
            # Group files by product ID
            product_files = {}
            thomann_files = []
            other_files = []
            
            for blob_name in blob_names:
                if blob_name.startswith('thomann/'):
                    thomann_files.append(blob_name)
                    filename = blob_name[8:]  # Remove 'thomann/' prefix
                    
                    # Extract product ID using the actual pattern: {product_id}_{timestamp}.jpg
                    match = re.match(r'^(\d+)_(\d{8}_\d{6})\.jpg$', filename)
                    if match:
                        product_id = int(match.group(1))
                        timestamp = match.group(2)
                        
                        if product_id not in product_files:
                            product_files[product_id] = []
                        product_files[product_id].append({
                            'blob_name': blob_name,
                            'filename': filename,
                            'timestamp': timestamp,
                            'full_url': f"https://getyourmusicgear.blob.core.windows.net/product-images/{blob_name}"
                        })
                else:
                    other_files.append(blob_name)
            
            print(f"📊 Blob Storage Analysis:")
            print(f"   📁 Thomann files: {len(thomann_files)}")
            print(f"   📁 Other files: {len(other_files)}")
            print(f"   🔢 Products with images: {len(product_files)}")
            print(f"   📷 Total images for products: {sum(len(files) for files in product_files.values())}")
            
            # Show sample of thomann files
            print(f"\n📋 Sample Thomann filenames:")
            for i, filename in enumerate(thomann_files[:10]):
                print(f"   {i+1}. {filename}")
            if len(thomann_files) > 10:
                print(f"   ... and {len(thomann_files) - 10} more")
            
            return product_files
            
        except Exception as e:
            print(f"❌ Error loading blob storage: {e}")
            return {}

    async def get_database_products_with_images(self) -> Dict[int, Dict]:
        """Get all products with images from database"""
        print("\n📋 Loading products from database...")
        
        from sqlalchemy import text
        
        async with self.session_maker() as session:
            # Use raw SQL to avoid JSONB/JSON type issues
            query = text("""
                SELECT id, name, slug, images 
                FROM products 
                WHERE images IS NOT NULL 
                AND images != '{}'::jsonb
                AND jsonb_typeof(images) = 'object'
            """)
            result = await session.execute(query)
            rows = result.fetchall()
            
            product_data = {}
            for row in rows:
                images = row.images
                if images and isinstance(images, dict) and len(images) > 0:
                    product_data[row.id] = {
                        'name': row.name,
                        'slug': row.slug,
                        'images': images
                    }
            
            print(f"📊 Found {len(product_data)} products with images in database")
            return product_data

    def analyze_associations(self, blob_files: Dict[int, List[str]], db_products: Dict[int, Dict]) -> Dict:
        """Analyze the associations between blob storage and database"""
        print("\n🔍 Analyzing Image Associations...")
        
        results = {
            'perfect_matches': [],      # DB points to correct blob file
            'wrong_urls': [],           # DB points to wrong/non-existent blob file  
            'missing_in_db': [],        # Blob exists but no DB record
            'missing_in_blob': [],      # DB record but no blob file
            'multiple_blob_files': [],  # Product has multiple blob files
        }
        
        # Check each product in the database
        for product_id, product_data in db_products.items():
            images = product_data['images']
            
            # Extract image URLs from the images JSON
            db_urls = []
            for key, image_data in images.items():
                if isinstance(image_data, dict) and 'url' in image_data:
                    url = image_data['url']
                    if 'getyourmusicgear.blob.core.windows.net' in url:
                        db_urls.append(url)
                elif isinstance(image_data, str) and 'getyourmusicgear.blob.core.windows.net' in image_data:
                    db_urls.append(image_data)
            
            # Check if product has files in blob storage
            blob_files_for_product = blob_files.get(product_id, [])
            
            if not db_urls and not blob_files_for_product:
                continue  # No images anywhere
            elif not db_urls and blob_files_for_product:
                results['missing_in_db'].append({
                    'product_id': product_id,
                    'blob_files': len(blob_files_for_product),
                    'blob_urls': [f['full_url'] for f in blob_files_for_product]
                })
            elif db_urls and not blob_files_for_product:
                results['missing_in_blob'].append({
                    'product_id': product_id,
                    'name': product_data['name'],
                    'db_urls': db_urls
                })
            else:
                # Both exist - check if they match
                blob_urls = [f['full_url'] for f in blob_files_for_product]
                
                if len(blob_files_for_product) > 1:
                    results['multiple_blob_files'].append({
                        'product_id': product_id,
                        'name': product_data['name'],
                        'blob_count': len(blob_files_for_product),
                        'blob_urls': blob_urls,
                        'db_urls': db_urls
                    })
                
                # Check if any DB URL matches any blob URL
                has_match = any(db_url in blob_urls for db_url in db_urls)
                
                if has_match:
                    results['perfect_matches'].append({
                        'product_id': product_id,
                        'name': product_data['name'],
                        'matched_urls': [url for url in db_urls if url in blob_urls]
                    })
                else:
                    results['wrong_urls'].append({
                        'product_id': product_id,
                        'name': product_data['name'],
                        'db_urls': db_urls,
                        'available_blob_urls': blob_urls
                    })
        
        # Check for blob files without database records
        for product_id, files in blob_files.items():
            if product_id not in db_products:
                results['missing_in_db'].append({
                    'product_id': product_id,
                    'blob_files': len(files),
                    'blob_urls': [f['full_url'] for f in files]
                })
        
        return results

    def print_detailed_report(self, results: Dict, total_products: int, total_blob_files: int):
        """Print detailed analysis report"""
        print("\n" + "=" * 80)
        print("📊 DETAILED IMAGE ASSOCIATION ANALYSIS")
        print("=" * 80)
        print(f"📅 Analysis completed at: {datetime.now()}")
        print()
        
        # Summary statistics
        perfect_matches = len(results['perfect_matches'])
        wrong_urls = len(results['wrong_urls']) 
        missing_in_db = len(results['missing_in_db'])
        missing_in_blob = len(results['missing_in_blob'])
        multiple_files = len(results['multiple_blob_files'])
        
        total_with_issues = wrong_urls + missing_in_db + missing_in_blob
        
        print("📈 SUMMARY STATISTICS")
        print("-" * 40)
        print(f"📊 Total products with images in DB: {total_products}")
        print(f"📊 Total blob files in storage: {total_blob_files}")
        print()
        print(f"✅ Perfect matches: {perfect_matches}")
        print(f"❌ Wrong URLs in DB: {wrong_urls}")
        print(f"🔍 Missing in DB: {missing_in_db}")
        print(f"☁️  Missing in blob: {missing_in_blob}")
        print(f"📁 Multiple files: {multiple_files}")
        print()
        print(f"🎯 Association accuracy: {perfect_matches}/{total_products} ({perfect_matches/total_products*100:.1f}%)")
        print(f"🚨 Products needing attention: {total_with_issues}")
        print()
        
        # Detailed breakdowns
        if results['wrong_urls']:
            print("❌ PRODUCTS WITH WRONG URLs (Sample):")
            print("-" * 50)
            for i, item in enumerate(results['wrong_urls'][:5]):
                print(f"  {i+1}. Product {item['product_id']}: {item['name']}")
                print(f"     DB URL: {item['db_urls'][0][:80]}...")
                if item['available_blob_urls']:
                    print(f"     Available: {item['available_blob_urls'][0][:80]}...")
                print()
            if len(results['wrong_urls']) > 5:
                print(f"     ... and {len(results['wrong_urls']) - 5} more")
            print()
        
        if results['missing_in_db']:
            print("🔍 BLOB FILES WITHOUT DB RECORDS (Sample):")
            print("-" * 50)
            for i, item in enumerate(results['missing_in_db'][:5]):
                print(f"  {i+1}. Product {item['product_id']}: {item['blob_files']} files")
                print(f"     URL: {item['blob_urls'][0][:80]}...")
                print()
            if len(results['missing_in_db']) > 5:
                print(f"     ... and {len(results['missing_in_db']) - 5} more")
            print()
        
        if results['multiple_blob_files']:
            print("📁 PRODUCTS WITH MULTIPLE BLOB FILES:")
            print("-" * 50)
            for i, item in enumerate(results['multiple_blob_files'][:5]):
                print(f"  {i+1}. Product {item['product_id']}: {item['name']}")
                print(f"     Files: {item['blob_count']}")
                print(f"     Latest: {sorted(item['blob_urls'])[-1][:80]}...")
                print()
            if len(results['multiple_blob_files']) > 5:
                print(f"     ... and {len(results['multiple_blob_files']) - 5} more")
            print()
        
        print("💡 RECOMMENDATIONS:")
        print("-" * 25)
        if wrong_urls > 0:
            print(f"🔧 Fix {wrong_urls} products with wrong URLs")
        if missing_in_db > 0:
            print(f"📝 Add DB records for {missing_in_db} orphaned blob files")
        if missing_in_blob > 0:
            print(f"📷 Download images for {missing_in_blob} products")
        if perfect_matches == total_products:
            print("🎉 All products have perfectly matched images!")
        
        return {
            'perfect_matches': perfect_matches,
            'total_products': total_products,
            'accuracy_percentage': perfect_matches/total_products*100 if total_products > 0 else 0,
            'total_issues': total_with_issues
        }

    def save_results(self, results: Dict):
        """Save detailed results to JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"image_association_analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"💾 Detailed results saved to: {filename}")

async def main():
    """Main verification function"""
    verifier = ImageAssociationVerifier()
    
    try:
        await verifier.initialize_db()
        
        # Get blob storage files
        blob_files = verifier.get_blob_storage_files()
        if not blob_files:
            print("❌ Could not load blob storage files")
            return
        
        # Get database products
        db_products = await verifier.get_database_products_with_images()
        if not db_products:
            print("❌ Could not load database products")
            return
        
        # Analyze associations
        results = verifier.analyze_associations(blob_files, db_products)
        
        # Calculate totals
        total_blob_files = sum(len(files) for files in blob_files.values())
        
        # Print detailed report
        summary = verifier.print_detailed_report(results, len(db_products), total_blob_files)
        
        # Save results
        verifier.save_results(results)
        
        print(f"\n🎯 FINAL ASSESSMENT:")
        print(f"   Accuracy: {summary['accuracy_percentage']:.1f}%")
        print(f"   Issues: {summary['total_issues']} products need attention")
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await verifier.close_db()

if __name__ == "__main__":
    asyncio.run(main())

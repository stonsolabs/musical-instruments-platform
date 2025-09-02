#!/usr/bin/env python3
"""
Identify Products Missing Images
- Find products without any images
- Find products with broken external URLs
- Find products not in blob storage
- Generate lists for re-processing
"""

import asyncio
import json
import httpx
from datetime import datetime
from typing import Dict, List, Set
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Product

class MissingImageIdentifier:
    def __init__(self):
        self.database_url = "postgresql://getyourmusicgear:arg-KDP8cjy.czu2zdv@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear"
        self.async_db_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        self.engine = None
        self.session_maker = None
        
        # Results
        self.products_without_images = []
        self.products_with_broken_external = []
        self.products_not_in_blob = []
        self.products_with_working_images = []

    async def initialize_db(self):
        """Initialize database connection"""
        self.engine = create_async_engine(self.async_db_url)
        self.session_maker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def close_db(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()

    def load_blob_product_ids(self) -> Set[int]:
        """Load product IDs that have images in blob storage"""
        import subprocess
        
        try:
            result = subprocess.run([
                'az', 'storage', 'blob', 'list',
                '--container-name', 'product-images',
                '--account-name', 'getyourmusicgear',
                '--query', '[].name',
                '--output', 'json'
            ], capture_output=True, text=True, timeout=60)
            
            blob_product_ids = set()
            
            if result.returncode == 0:
                blob_names = json.loads(result.stdout)
                
                for blob_name in blob_names:
                    if blob_name.startswith('thomann/'):
                        filename = blob_name[8:]  # Remove 'thomann/' prefix
                        
                        # Extract product ID from filename
                        import re
                        match = re.match(r'^(\d+)_', filename)
                        if match:
                            product_id = int(match.group(1))
                            blob_product_ids.add(product_id)
                
                print(f"📊 Found {len(blob_product_ids)} product IDs with images in blob storage")
                return blob_product_ids
            
            else:
                print(f"❌ Error loading blob storage: {result.stderr}")
                return set()
                
        except Exception as e:
            print(f"❌ Error loading blob storage: {e}")
            return set()

    async def check_url_exists(self, url: str, client: httpx.AsyncClient) -> bool:
        """Check if URL returns a successful response"""
        try:
            response = await client.head(url, timeout=10.0)
            return response.status_code == 200
        except:
            return False

    async def analyze_all_products(self):
        """Analyze all products to categorize image status"""
        print("🔍 Analyzing All Products for Image Status")
        print("=" * 60)
        
        # Load blob storage product IDs
        blob_product_ids = self.load_blob_product_ids()
        
        async with self.session_maker() as session:
            # Get all active products
            query = select(Product).where(Product.is_active == True)
            result = await session.execute(query)
            products = result.scalars().all()
            
            print(f"📊 Analyzing {len(products)} active products...")
            
            batch_size = 100
            processed = 0
            
            async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as http_client:
                for i in range(0, len(products), batch_size):
                    batch = products[i:i + batch_size]
                    print(f"🔄 Processing batch {i//batch_size + 1}: products {i+1}-{min(i+batch_size, len(products))}")
                    
                    for product in batch:
                        await self.categorize_product(product, blob_product_ids, http_client)
                        processed += 1
                    
                    # Progress update
                    if processed % 1000 == 0:
                        self.print_interim_stats(processed)

    async def categorize_product(self, product: Product, blob_product_ids: Set[int], client: httpx.AsyncClient):
        """Categorize a single product's image status"""
        
        # Check if product has any images
        if not product.images or not isinstance(product.images, dict) or len(product.images) == 0:
            self.products_without_images.append({
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "category": "no_images"
            })
            return
        
        # Extract image URLs
        image_urls = []
        for key, image_data in product.images.items():
            if isinstance(image_data, dict) and "url" in image_data:
                image_urls.append(image_data["url"])
            elif isinstance(image_data, str):
                image_urls.append(image_data)
        
        if not image_urls:
            self.products_without_images.append({
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "category": "empty_images_dict"
            })
            return
        
        # Check image URL status
        has_working_azure = False
        has_broken_external = False
        is_in_blob_storage = product.id in blob_product_ids
        
        for url in image_urls:
            if "getyourmusicgear.blob.core.windows.net" in url:
                # Azure blob URL - assume it's working if product is in blob storage
                if is_in_blob_storage:
                    has_working_azure = True
            else:
                # External URL - check if it works
                url_works = await self.check_url_exists(url, client)
                if not url_works:
                    has_broken_external = True
        
        # Categorize the product
        if has_working_azure:
            self.products_with_working_images.append({
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "category": "working_azure"
            })
        elif is_in_blob_storage:
            # Product is in blob storage but URLs might be wrong - should be rare after our fixes
            self.products_with_working_images.append({
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "category": "azure_url_mismatch"
            })
        elif has_broken_external:
            self.products_with_broken_external.append({
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "category": "broken_external",
                "urls": image_urls
            })
        else:
            # Product not in blob storage and no working external URLs
            self.products_not_in_blob.append({
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "category": "not_in_blob",
                "urls": image_urls
            })

    def print_interim_stats(self, processed: int):
        """Print interim statistics"""
        print(f"\n📊 Interim Stats (after {processed} products):")
        print(f"  Without images: {len(self.products_without_images)}")
        print(f"  With broken external: {len(self.products_with_broken_external)}")
        print(f"  Not in blob storage: {len(self.products_not_in_blob)}")
        print(f"  With working images: {len(self.products_with_working_images)}")
        print()

    def generate_report(self):
        """Generate comprehensive report"""
        total_products = (len(self.products_without_images) + 
                         len(self.products_with_broken_external) + 
                         len(self.products_not_in_blob) + 
                         len(self.products_with_working_images))
        
        print("\n" + "=" * 60)
        print("📋 PRODUCTS MISSING IMAGES ANALYSIS")
        print("=" * 60)
        print(f"📅 Completed at: {datetime.now()}")
        print()
        
        print("📊 SUMMARY STATISTICS")
        print("-" * 30)
        print(f"Total products analyzed: {total_products}")
        print(f"✅ Products with working images: {len(self.products_with_working_images)} ({len(self.products_with_working_images)/total_products*100:.1f}%)")
        print(f"❌ Products needing image processing: {total_products - len(self.products_with_working_images)} ({(total_products - len(self.products_with_working_images))/total_products*100:.1f}%)")
        print()
        
        print("🚨 PRODUCTS NEEDING ATTENTION")
        print("-" * 35)
        print(f"📷 No images at all: {len(self.products_without_images)}")
        print(f"🌐 Broken external URLs: {len(self.products_with_broken_external)}")
        print(f"☁️  Not in blob storage: {len(self.products_not_in_blob)}")
        print()
        
        # Show samples
        if self.products_without_images:
            print("📷 SAMPLE PRODUCTS WITHOUT IMAGES:")
            for i, product in enumerate(self.products_without_images[:10]):
                print(f"  {i+1}. ID: {product['id']} - {product['name']} ({product['category']})")
            if len(self.products_without_images) > 10:
                print(f"  ... and {len(self.products_without_images) - 10} more")
            print()
        
        if self.products_not_in_blob:
            print("☁️  SAMPLE PRODUCTS NOT IN BLOB STORAGE:")
            for i, product in enumerate(self.products_not_in_blob[:10]):
                print(f"  {i+1}. ID: {product['id']} - {product['name']}")
                if 'urls' in product and product['urls']:
                    print(f"     Current URL: {product['urls'][0][:80]}...")
            if len(self.products_not_in_blob) > 10:
                print(f"  ... and {len(self.products_not_in_blob) - 10} more")
            print()
        
        print("💡 RECOMMENDATIONS FOR RE-PROCESSING")
        print("-" * 40)
        
        total_needing_processing = (len(self.products_without_images) + 
                                  len(self.products_with_broken_external) + 
                                  len(self.products_not_in_blob))
        
        if total_needing_processing > 0:
            print(f"🔧 Total products needing image crawling: {total_needing_processing}")
            print()
            print("Priority order for re-processing:")
            print(f"1. Products without images: {len(self.products_without_images)} (highest priority)")
            print(f"2. Products not in blob storage: {len(self.products_not_in_blob)} (medium priority)")
            print(f"3. Products with broken external URLs: {len(self.products_with_broken_external)} (low priority)")
            print()
            print("📋 Product ID lists have been saved for crawler input")
        else:
            print("🎉 All products have working images!")

    def save_processing_lists(self):
        """Save lists of products that need processing"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save comprehensive report
        report_data = {
            "analysis_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_products": len(self.products_without_images) + len(self.products_with_broken_external) + len(self.products_not_in_blob) + len(self.products_with_working_images),
                "working_images": len(self.products_with_working_images),
                "without_images": len(self.products_without_images),
                "broken_external": len(self.products_with_broken_external),
                "not_in_blob": len(self.products_not_in_blob)
            },
            "products_without_images": self.products_without_images,
            "products_with_broken_external": self.products_with_broken_external,
            "products_not_in_blob": self.products_not_in_blob
        }
        
        filename = f"missing_images_analysis_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"💾 Detailed analysis saved to: {filename}")
        
        # Save simple product ID lists for crawler
        high_priority_ids = [p['id'] for p in self.products_without_images]
        medium_priority_ids = [p['id'] for p in self.products_not_in_blob]
        low_priority_ids = [p['id'] for p in self.products_with_broken_external]
        
        # High priority list
        if high_priority_ids:
            with open(f"products_without_images_{timestamp}.txt", 'w') as f:
                f.write("# Products without any images (HIGH PRIORITY)\n")
                f.write("# Format: one product ID per line\n")
                for product_id in high_priority_ids:
                    f.write(f"{product_id}\n")
            print(f"📋 High priority list saved to: products_without_images_{timestamp}.txt")
        
        # Medium priority list
        if medium_priority_ids:
            with open(f"products_not_in_blob_{timestamp}.txt", 'w') as f:
                f.write("# Products not in blob storage (MEDIUM PRIORITY)\n")
                f.write("# Format: one product ID per line\n")
                for product_id in medium_priority_ids:
                    f.write(f"{product_id}\n")
            print(f"📋 Medium priority list saved to: products_not_in_blob_{timestamp}.txt")
        
        # Combined list for crawler
        all_ids = high_priority_ids + medium_priority_ids + low_priority_ids
        if all_ids:
            with open(f"products_needing_images_{timestamp}.txt", 'w') as f:
                f.write("# All products needing image processing\n")
                f.write("# Format: one product ID per line\n")
                f.write("# Order: high priority first, then medium, then low\n")
                for product_id in all_ids:
                    f.write(f"{product_id}\n")
            print(f"📋 Combined list saved to: products_needing_images_{timestamp}.txt")
        
        return len(all_ids)

async def main():
    """Main execution function"""
    identifier = MissingImageIdentifier()
    
    try:
        await identifier.initialize_db()
        await identifier.analyze_all_products()
        identifier.generate_report()
        total_needing_processing = identifier.save_processing_lists()
        
        if total_needing_processing > 0:
            print(f"\n🎯 NEXT STEPS:")
            print(f"   Use the generated .txt files as input for your image crawler")
            print(f"   Process {total_needing_processing} products to complete image coverage")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await identifier.close_db()

if __name__ == "__main__":
    asyncio.run(main())

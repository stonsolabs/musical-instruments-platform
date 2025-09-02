#!/usr/bin/env python3
"""
Comprehensive Product Image Audit Job
- Check all products for image associations
- Verify which images actually exist in Azure blob storage
- Identify missing images and broken links
- Generate report and suggestions for fixing
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, List, Set, Tuple
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Product

class ProductImageAuditor:
    def __init__(self):
        self.database_url = "postgresql://getyourmusicgear:arg-KDP8cjy.czu2zdv@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear"
        self.async_db_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        self.engine = None
        self.session_maker = None
        
        # Statistics
        self.stats = {
            "total_products": 0,
            "products_with_images": 0,
            "products_without_images": 0,
            "total_image_urls": 0,
            "azure_blob_urls": 0,
            "external_urls": 0,
            "working_azure_urls": 0,
            "broken_azure_urls": 0,
            "working_external_urls": 0,
            "broken_external_urls": 0,
        }
        
        # Collections
        self.working_images = []
        self.broken_images = []
        self.products_without_images = []
        self.url_patterns = {}

    async def initialize_db(self):
        """Initialize database connection"""
        self.engine = create_async_engine(self.async_db_url)
        self.session_maker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def close_db(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()

    def extract_image_urls(self, images_dict: Dict) -> List[Tuple[str, str]]:
        """Extract image URLs from product images dict"""
        urls = []
        if not images_dict or not isinstance(images_dict, dict):
            return urls
        
        for key, image_data in images_dict.items():
            if isinstance(image_data, dict) and "url" in image_data:
                urls.append((key, image_data["url"]))
            elif isinstance(image_data, str):
                urls.append((key, image_data))
        
        return urls

    def categorize_url(self, url: str) -> str:
        """Categorize URL by type"""
        if "getyourmusicgear.blob.core.windows.net" in url:
            return "azure_blob"
        elif "thomann.de" in url:
            return "thomann_direct"
        elif url.startswith("http"):
            try:
                domain = url.split("/")[2]
                return f"external_{domain}"
            except:
                return "external_unknown"
        else:
            return "invalid"

    async def check_url_exists(self, url: str, client: httpx.AsyncClient) -> Tuple[bool, int, str]:
        """Check if URL returns a successful response"""
        try:
            response = await client.head(url, timeout=10.0)
            return response.status_code == 200, response.status_code, "OK"
        except httpx.TimeoutException:
            return False, 0, "TIMEOUT"
        except httpx.ConnectError:
            return False, 0, "CONNECTION_ERROR"
        except Exception as e:
            return False, 0, str(e)[:50]

    async def audit_all_products(self):
        """Main audit function"""
        print("🔍 Starting Comprehensive Product Image Audit")
        print("=" * 60)
        print(f"📅 Started at: {datetime.now()}")
        print()

        async with self.session_maker() as session:
            # Get total product count
            total_count_result = await session.execute(select(func.count(Product.id)))
            self.stats["total_products"] = total_count_result.scalar()
            
            print(f"📊 Total products in database: {self.stats['total_products']}")
            
            # Get all products in batches to avoid memory issues
            batch_size = 500
            processed = 0
            
            async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as http_client:
                while processed < self.stats["total_products"]:
                    # Get batch of products
                    query = (
                        select(Product)
                        .where(Product.is_active == True)
                        .offset(processed)
                        .limit(batch_size)
                    )
                    
                    result = await session.execute(query)
                    products = result.scalars().all()
                    
                    if not products:
                        break
                    
                    print(f"🔄 Processing batch {processed//batch_size + 1}: products {processed+1}-{processed+len(products)}")
                    
                    # Process each product in the batch
                    for product in products:
                        await self.audit_product(product, http_client)
                    
                    processed += len(products)
                    
                    # Progress update
                    if processed % 1000 == 0:
                        self.print_interim_stats(processed)

    async def audit_product(self, product: Product, client: httpx.AsyncClient):
        """Audit a single product's images"""
        if not product.images or not isinstance(product.images, dict):
            self.products_without_images.append({
                "id": product.id,
                "name": product.name,
                "slug": product.slug
            })
            self.stats["products_without_images"] += 1
            return
        
        self.stats["products_with_images"] += 1
        image_urls = self.extract_image_urls(product.images)
        
        if not image_urls:
            self.products_without_images.append({
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "reason": "empty_images_dict"
            })
            return
        
        # Check each image URL
        for key, url in image_urls:
            self.stats["total_image_urls"] += 1
            
            # Categorize URL
            url_category = self.categorize_url(url)
            self.url_patterns[url_category] = self.url_patterns.get(url_category, 0) + 1
            
            if url_category == "azure_blob":
                self.stats["azure_blob_urls"] += 1
            else:
                self.stats["external_urls"] += 1
            
            # Check if URL works
            exists, status_code, error = await self.check_url_exists(url, client)
            
            image_info = {
                "product_id": product.id,
                "product_name": product.name,
                "image_key": key,
                "url": url,
                "category": url_category,
                "status_code": status_code,
                "error": error if not exists else None
            }
            
            if exists:
                self.working_images.append(image_info)
                if url_category == "azure_blob":
                    self.stats["working_azure_urls"] += 1
                else:
                    self.stats["working_external_urls"] += 1
            else:
                self.broken_images.append(image_info)
                if url_category == "azure_blob":
                    self.stats["broken_azure_urls"] += 1
                else:
                    self.stats["broken_external_urls"] += 1

    def print_interim_stats(self, processed: int):
        """Print interim statistics"""
        print(f"\n📊 Interim Stats (after {processed} products):")
        print(f"  Products with images: {self.stats['products_with_images']}")
        print(f"  Products without images: {self.stats['products_without_images']}")
        print(f"  Total image URLs: {self.stats['total_image_urls']}")
        print(f"  Working images: {len(self.working_images)}")
        print(f"  Broken images: {len(self.broken_images)}")
        print()

    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "=" * 60)
        print("📋 COMPREHENSIVE IMAGE AUDIT REPORT")
        print("=" * 60)
        print(f"📅 Completed at: {datetime.now()}")
        print()
        
        # Overall Statistics
        print("📊 OVERALL STATISTICS")
        print("-" * 30)
        print(f"Total products: {self.stats['total_products']}")
        print(f"Products with images: {self.stats['products_with_images']} ({self.stats['products_with_images']/self.stats['total_products']*100:.1f}%)")
        print(f"Products without images: {self.stats['products_without_images']} ({self.stats['products_without_images']/self.stats['total_products']*100:.1f}%)")
        print(f"Total image URLs: {self.stats['total_image_urls']}")
        print()
        
        # URL Categories
        print("🏷️ URL CATEGORIES")
        print("-" * 20)
        for category, count in sorted(self.url_patterns.items(), key=lambda x: x[1], reverse=True):
            percentage = count / self.stats['total_image_urls'] * 100 if self.stats['total_image_urls'] > 0 else 0
            print(f"  {category}: {count} ({percentage:.1f}%)")
        print()
        
        # Image Status
        print("✅❌ IMAGE STATUS")
        print("-" * 20)
        total_images = len(self.working_images) + len(self.broken_images)
        if total_images > 0:
            working_pct = len(self.working_images) / total_images * 100
            broken_pct = len(self.broken_images) / total_images * 100
            print(f"✅ Working images: {len(self.working_images)} ({working_pct:.1f}%)")
            print(f"❌ Broken images: {len(self.broken_images)} ({broken_pct:.1f}%)")
            print()
        
        # Azure Blob Specific
        azure_total = self.stats["working_azure_urls"] + self.stats["broken_azure_urls"]
        if azure_total > 0:
            azure_working_pct = self.stats["working_azure_urls"] / azure_total * 100
            azure_broken_pct = self.stats["broken_azure_urls"] / azure_total * 100
            print("☁️ AZURE BLOB STORAGE STATUS")
            print("-" * 30)
            print(f"Total Azure blob URLs: {azure_total}")
            print(f"✅ Working: {self.stats['working_azure_urls']} ({azure_working_pct:.1f}%)")
            print(f"❌ Broken: {self.stats['broken_azure_urls']} ({azure_broken_pct:.1f}%)")
            print()
        
        # Sample broken images
        if self.broken_images:
            print("🚨 SAMPLE BROKEN IMAGES")
            print("-" * 25)
            for i, img in enumerate(self.broken_images[:10]):
                print(f"  {i+1}. {img['product_name']}")
                print(f"     URL: {img['url']}")
                print(f"     Error: {img['status_code']} - {img['error']}")
                print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS")
        print("-" * 20)
        
        if self.stats["broken_azure_urls"] > 0:
            print("🔧 Azure Blob Storage Issues:")
            print("   - Many Azure blob URLs are returning 404")
            print("   - Check if images were actually uploaded to blob storage")
            print("   - Verify container name and file paths")
            print("   - Consider re-running image crawler/uploader")
            print()
        
        if len(self.products_without_images) > 0:
            print(f"📷 Missing Images:")
            print(f"   - {len(self.products_without_images)} products have no images")
            print("   - Consider running image crawler for these products")
            print()
        
        if self.stats["broken_external_urls"] > 0:
            print("🌐 External URL Issues:")
            print("   - Some external URLs are broken or blocked")
            print("   - Consider downloading and hosting these images locally")
            print()

    def save_detailed_report(self):
        """Save detailed JSON report for further analysis"""
        report_data = {
            "audit_timestamp": datetime.now().isoformat(),
            "statistics": self.stats,
            "url_patterns": self.url_patterns,
            "working_images": self.working_images[:100],  # Sample only
            "broken_images": self.broken_images[:100],    # Sample only
            "products_without_images": self.products_without_images[:100]  # Sample only
        }
        
        filename = f"image_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"💾 Detailed report saved to: {filename}")

async def main():
    """Main execution function"""
    auditor = ProductImageAuditor()
    
    try:
        await auditor.initialize_db()
        await auditor.audit_all_products()
        auditor.generate_report()
        auditor.save_detailed_report()
        
    except Exception as e:
        print(f"❌ Error during audit: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await auditor.close_db()

if __name__ == "__main__":
    asyncio.run(main())

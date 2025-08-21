#!/usr/bin/env python3
"""
Admin script for generating AI content for musical instrument products.
This is a background process that can be run to generate comprehensive AI content
for products in the database.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Add the parent directory to the path to import app modules
sys.path.append('..')

from app.database import get_db_session
from app.models import Product
from app.services.ai_content import AIContentGenerator


class AIContentGeneratorAdmin:
    def __init__(self):
        self.ai_generator = AIContentGenerator()
        self.stats = {
            "processed": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0
        }

    async def generate_for_product(self, product: Product, db: AsyncSession, force_regenerate: bool = False) -> dict:
        """Generate AI content for a single product."""
        try:
            # Check if content already exists and we're not forcing regeneration
            if not force_regenerate and product.ai_generated_content:
                print(f"⏭️  Skipping {product.name} (content already exists)")
                self.stats["skipped"] += 1
                return {"status": "skipped", "reason": "Content already exists"}

            print(f"🤖 Generating AI content for: {product.name}")
            
            # Generate AI content
            ai_content = await self.ai_generator.generate_product_content(product)
            
            # Update the product
            product.ai_generated_content = ai_content
            product.updated_at = datetime.utcnow()
            
            await db.commit()
            
            print(f"✅ Successfully generated content for: {product.name}")
            self.stats["success"] += 1
            
            return {
                "status": "success",
                "product_id": product.id,
                "product_name": product.name,
                "content_generated": True
            }
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Failed to generate content for {product.name}: {str(e)}")
            self.stats["failed"] += 1
            
            return {
                "status": "failed",
                "product_id": product.id,
                "product_name": product.name,
                "error": str(e)
            }

    async def generate_for_all_products(self, 
                                      limit: Optional[int] = None, 
                                      force_regenerate: bool = False,
                                      category_filter: Optional[str] = None,
                                      brand_filter: Optional[str] = None) -> dict:
        """Generate AI content for all products or a subset."""
        async with get_db_session() as db:
            # Build query
            stmt = (
                select(Product)
                .where(Product.is_active.is_(True))
            )
            
            if category_filter:
                from app.models import Category
                stmt = stmt.join(Product.category).where(Category.slug == category_filter)
            
            if brand_filter:
                from app.models import Brand
                stmt = stmt.join(Product.brand).where(Brand.slug == brand_filter)
            
            if limit:
                stmt = stmt.limit(limit)
            
            # Execute query
            result = await db.execute(stmt)
            products = result.scalars().all()
            
            print(f"🎯 Found {len(products)} products to process")
            
            if not products:
                return {"message": "No products found matching criteria"}
            
            # Process each product
            results = []
            for product in products:
                self.stats["processed"] += 1
                result = await self.generate_for_product(product, db, force_regenerate)
                results.append(result)
                
                # Small delay to avoid overwhelming the AI API
                await asyncio.sleep(1)
            
            return {
                "total_processed": self.stats["processed"],
                "successful": self.stats["success"],
                "failed": self.stats["failed"],
                "skipped": self.stats["skipped"],
                "results": results
            }

    async def generate_for_product_ids(self, product_ids: List[int], force_regenerate: bool = False) -> dict:
        """Generate AI content for specific product IDs."""
        async with get_db_session() as db:
            stmt = select(Product).where(Product.id.in_(product_ids))
            result = await db.execute(stmt)
            products = result.scalars().all()
            
            if len(products) != len(product_ids):
                found_ids = {p.id for p in products}
                missing_ids = [pid for pid in product_ids if pid not in found_ids]
                print(f"⚠️  Warning: Products not found: {missing_ids}")
            
            print(f"🎯 Processing {len(products)} specific products")
            
            results = []
            for product in products:
                self.stats["processed"] += 1
                result = await self.generate_for_product(product, db, force_regenerate)
                results.append(result)
                
                # Small delay to avoid overwhelming the AI API
                await asyncio.sleep(1)
            
            return {
                "total_processed": self.stats["processed"],
                "successful": self.stats["success"],
                "failed": self.stats["failed"],
                "skipped": self.stats["skipped"],
                "results": results
            }

    def print_stats(self):
        """Print processing statistics."""
        print("\n" + "="*50)
        print("📊 PROCESSING STATISTICS")
        print("="*50)
        print(f"Total processed: {self.stats['processed']}")
        print(f"Successful: {self.stats['success']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Skipped: {self.stats['skipped']}")
        print("="*50)


async def main():
    """Main function to run the AI content generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate AI content for musical instrument products")
    parser.add_argument("--all", action="store_true", help="Generate content for all products")
    parser.add_argument("--limit", type=int, help="Limit number of products to process")
    parser.add_argument("--force", action="store_true", help="Force regeneration of existing content")
    parser.add_argument("--category", type=str, help="Filter by category slug")
    parser.add_argument("--brand", type=str, help="Filter by brand slug")
    parser.add_argument("--product-ids", type=str, help="Comma-separated list of product IDs")
    
    args = parser.parse_args()
    
    generator = AIContentGeneratorAdmin()
    
    try:
        if args.product_ids:
            # Generate for specific product IDs
            product_ids = [int(pid.strip()) for pid in args.product_ids.split(",")]
            result = await generator.generate_for_product_ids(product_ids, args.force)
        elif args.all:
            # Generate for all products
            result = await generator.generate_for_all_products(
                limit=args.limit,
                force_regenerate=args.force,
                category_filter=args.category,
                brand_filter=args.brand
            )
        else:
            print("❌ Please specify --all or --product-ids")
            return
        
        generator.print_stats()
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_content_generation_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"💾 Results saved to: {filename}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
        generator.print_stats()
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        generator.print_stats()


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Batch AI Content Generation for Musical Instrument Products
Optimized for processing thousands of products efficiently and cost-effectively.
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Add the parent directory to the path to import app modules
sys.path.append('..')

from app.database import get_db_session
from app.models import Product
from app.services.ai_content import AIContentGenerator


@dataclass
class BatchConfig:
    """Configuration for batch processing."""
    batch_size: int = 50
    max_concurrent: int = 5
    delay_between_batches: float = 2.0
    delay_between_requests: float = 0.5
    max_retries: int = 3
    retry_delay: float = 5.0
    save_progress_interval: int = 10
    output_dir: str = "batch_results"


class BatchAIContentGenerator:
    def __init__(self, config: BatchConfig):
        self.config = config
        self.ai_generator = AIContentGenerator()
        self.stats = {
            "total_products": 0,
            "processed": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "retries": 0,
            "start_time": None,
            "end_time": None
        }
        self.results = []
        self.progress_file = None
        
        # Create output directory
        Path(config.output_dir).mkdir(exist_ok=True)

    async def generate_batch_content(self, products: List[Product], batch_id: int) -> List[Dict[str, Any]]:
        """Generate content for a batch of products concurrently."""
        print(f"🔄 Processing batch {batch_id} with {len(products)} products...")
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(self.config.max_concurrent)
        
        async def process_product(product: Product) -> Dict[str, Any]:
            async with semaphore:
                return await self._process_single_product(product)
        
        # Process products concurrently
        tasks = [process_product(product) for product in products]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions and format results
        formatted_results = []
        for i, result in enumerate(batch_results):
            if isinstance(result, Exception):
                formatted_results.append({
                    "product_id": products[i].id,
                    "product_name": products[i].name,
                    "status": "failed",
                    "error": str(result)
                })
            else:
                formatted_results.append(result)
        
        return formatted_results

    async def _process_single_product(self, product: Product) -> Dict[str, Any]:
        """Process a single product with retry logic."""
        for attempt in range(self.config.max_retries + 1):
            try:
                # Check if content already exists
                if product.ai_generated_content:
                    self.stats["skipped"] += 1
                    return {
                        "product_id": product.id,
                        "product_name": product.name,
                        "status": "skipped",
                        "reason": "Content already exists"
                    }
                
                # Generate AI content
                ai_content = await self.ai_generator.generate_product_content(product)
                
                # Update product in database
                async with get_db_session() as db:
                    product.ai_generated_content = ai_content
                    product.updated_at = datetime.utcnow()
                    await db.commit()
                
                self.stats["success"] += 1
                return {
                    "product_id": product.id,
                    "product_name": product.name,
                    "status": "success",
                    "content_generated": True
                }
                
            except Exception as e:
                if attempt < self.config.max_retries:
                    self.stats["retries"] += 1
                    print(f"⚠️  Retry {attempt + 1}/{self.config.max_retries} for {product.name}: {str(e)}")
                    await asyncio.sleep(self.config.retry_delay)
                else:
                    self.stats["failed"] += 1
                    return {
                        "product_id": product.id,
                        "product_name": product.name,
                        "status": "failed",
                        "error": str(e)
                    }

    async def process_all_products(self, 
                                 category_filter: Optional[str] = None,
                                 brand_filter: Optional[str] = None,
                                 force_regenerate: bool = False) -> Dict[str, Any]:
        """Process all products in batches."""
        self.stats["start_time"] = datetime.now()
        
        async with get_db_session() as db:
            # Build query
            stmt = select(Product).where(Product.is_active.is_(True))
            
            if category_filter:
                from app.models import Category
                stmt = stmt.join(Product.category).where(Category.slug == category_filter)
            
            if brand_filter:
                from app.models import Brand
                stmt = stmt.join(Product.brand).where(Brand.slug == brand_filter)
            
            # Execute query
            result = await db.execute(stmt)
            all_products = result.scalars().all()
        
        self.stats["total_products"] = len(all_products)
        print(f"🎯 Found {len(all_products)} products to process")
        
        if not all_products:
            return {"message": "No products found matching criteria"}
        
        # Split into batches
        batches = [all_products[i:i + self.config.batch_size] 
                  for i in range(0, len(all_products), self.config.batch_size)]
        
        print(f"📦 Processing {len(batches)} batches of {self.config.batch_size} products each")
        
        # Process batches
        for batch_id, batch_products in enumerate(batches, 1):
            print(f"\n🔄 Processing batch {batch_id}/{len(batches)}")
            
            # Process batch
            batch_results = await self.generate_batch_content(batch_products, batch_id)
            self.results.extend(batch_results)
            self.stats["processed"] += len(batch_products)
            
            # Save progress
            if batch_id % self.config.save_progress_interval == 0:
                await self._save_progress(batch_id)
            
            # Delay between batches
            if batch_id < len(batches):
                print(f"⏳ Waiting {self.config.delay_between_batches}s before next batch...")
                await asyncio.sleep(self.config.delay_between_batches)
        
        self.stats["end_time"] = datetime.now()
        return await self._finalize_results()

    async def process_product_ids(self, product_ids: List[int], force_regenerate: bool = False) -> Dict[str, Any]:
        """Process specific product IDs in batches."""
        self.stats["start_time"] = datetime.now()
        
        async with get_db_session() as db:
            stmt = select(Product).where(Product.id.in_(product_ids))
            result = await db.execute(stmt)
            all_products = result.scalars().all()
        
        if len(all_products) != len(product_ids):
            found_ids = {p.id for p in all_products}
            missing_ids = [pid for pid in product_ids if pid not in found_ids]
            print(f"⚠️  Warning: Products not found: {missing_ids}")
        
        self.stats["total_products"] = len(all_products)
        print(f"🎯 Processing {len(all_products)} specific products")
        
        # Split into batches
        batches = [all_products[i:i + self.config.batch_size] 
                  for i in range(0, len(all_products), self.config.batch_size)]
        
        # Process batches
        for batch_id, batch_products in enumerate(batches, 1):
            print(f"\n🔄 Processing batch {batch_id}/{len(batches)}")
            
            batch_results = await self.generate_batch_content(batch_products, batch_id)
            self.results.extend(batch_results)
            self.stats["processed"] += len(batch_products)
            
            if batch_id % self.config.save_progress_interval == 0:
                await self._save_progress(batch_id)
            
            if batch_id < len(batches):
                await asyncio.sleep(self.config.delay_between_batches)
        
        self.stats["end_time"] = datetime.now()
        return await self._finalize_results()

    async def _save_progress(self, batch_id: int):
        """Save current progress to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        progress_file = f"{self.config.output_dir}/progress_batch_{batch_id}_{timestamp}.json"
        
        progress_data = {
            "batch_id": batch_id,
            "timestamp": timestamp,
            "stats": self.stats,
            "results": self.results
        }
        
        with open(progress_file, 'w') as f:
            json.dump(progress_data, f, indent=2, default=str)
        
        print(f"💾 Progress saved to: {progress_file}")

    async def _finalize_results(self) -> Dict[str, Any]:
        """Finalize and save results."""
        # Calculate processing time
        if self.stats["start_time"] and self.stats["end_time"]:
            processing_time = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
            self.stats["processing_time_seconds"] = processing_time
            self.stats["products_per_minute"] = (self.stats["processed"] / processing_time) * 60
        
        # Save final results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"{self.config.output_dir}/batch_results_{timestamp}.json"
        
        final_results = {
            "processing_config": {
                "batch_size": self.config.batch_size,
                "max_concurrent": self.config.max_concurrent,
                "delay_between_batches": self.config.delay_between_batches,
                "delay_between_requests": self.config.delay_between_requests
            },
            "statistics": self.stats,
            "results": self.results
        }
        
        with open(results_file, 'w') as f:
            json.dump(final_results, f, indent=2, default=str)
        
        print(f"💾 Final results saved to: {results_file}")
        
        return final_results

    def print_stats(self):
        """Print processing statistics."""
        print("\n" + "="*60)
        print("📊 BATCH PROCESSING STATISTICS")
        print("="*60)
        print(f"Total products: {self.stats['total_products']}")
        print(f"Processed: {self.stats['processed']}")
        print(f"Successful: {self.stats['success']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"Retries: {self.stats['retries']}")
        
        if "processing_time_seconds" in self.stats:
            print(f"Processing time: {self.stats['processing_time_seconds']:.2f} seconds")
            print(f"Products per minute: {self.stats['products_per_minute']:.2f}")
        
        print("="*60)


async def main():
    """Main function to run the batch AI content generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch AI content generation for musical instruments")
    parser.add_argument("--all", action="store_true", help="Generate content for all products")
    parser.add_argument("--product-ids", type=str, help="Comma-separated list of product IDs")
    parser.add_argument("--category", type=str, help="Filter by category slug")
    parser.add_argument("--brand", type=str, help="Filter by brand slug")
    parser.add_argument("--force", action="store_true", help="Force regeneration of existing content")
    
    # Batch processing options
    parser.add_argument("--batch-size", type=int, default=50, help="Number of products per batch")
    parser.add_argument("--max-concurrent", type=int, default=5, help="Maximum concurrent requests")
    parser.add_argument("--delay-batches", type=float, default=2.0, help="Delay between batches (seconds)")
    parser.add_argument("--delay-requests", type=float, default=0.5, help="Delay between requests (seconds)")
    parser.add_argument("--max-retries", type=int, default=3, help="Maximum retry attempts")
    parser.add_argument("--output-dir", type=str, default="batch_results", help="Output directory for results")
    
    args = parser.parse_args()
    
    # Create batch configuration
    config = BatchConfig(
        batch_size=args.batch_size,
        max_concurrent=args.max_concurrent,
        delay_between_batches=args.delay_batches,
        delay_between_requests=args.delay_requests,
        max_retries=args.max_retries,
        output_dir=args.output_dir
    )
    
    generator = BatchAIContentGenerator(config)
    
    try:
        if args.product_ids:
            # Generate for specific product IDs
            product_ids = [int(pid.strip()) for pid in args.product_ids.split(",")]
            result = await generator.process_product_ids(product_ids, args.force)
        elif args.all:
            # Generate for all products
            result = await generator.process_all_products(
                category_filter=args.category,
                brand_filter=args.brand,
                force_regenerate=args.force
            )
        else:
            print("❌ Please specify --all or --product-ids")
            return
        
        generator.print_stats()
        
    except KeyboardInterrupt:
        print("\n⏹️  Batch processing interrupted by user")
        generator.print_stats()
        await generator._save_progress(0)  # Save current progress
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        generator.print_stats()


if __name__ == "__main__":
    asyncio.run(main())

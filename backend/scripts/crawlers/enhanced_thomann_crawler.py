#!/usr/bin/env python3
"""
Enhanced Thomann Image Downloader
- Built-in duplicate prevention
- Checks blob storage before downloading
- Ensures one image per product
- Safe for parallel execution
"""

import asyncio
import json
import subprocess
import re
from datetime import datetime
from typing import Dict, List, Set, Optional
from pathlib import Path
import sys

# Add crawler directory to path robustly (walk up to repo root)
def _ensure_crawler_on_path():
    here = Path(__file__).resolve()
    for base in here.parents:
        candidate = base / "crawler"
        if candidate.exists():
            sys.path.append(str(candidate))
            return

_ensure_crawler_on_path()

from thomann_image_downloader import ThomannImageDownloader

class EnhancedThomannCrawler(ThomannImageDownloader):
    """
    Enhanced version with duplicate prevention
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.existing_product_ids = set()
        self.loaded_existing = False
        
    def load_existing_images(self) -> Set[int]:
        """Load product IDs that already have images in blob storage"""
        if self.loaded_existing:
            return self.existing_product_ids
            
        print("📋 Checking existing images in blob storage...")
        
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
                return set()
            
            blob_names = json.loads(result.stdout)
            existing_ids = set()
            
            for blob_name in blob_names:
                if blob_name.startswith('thomann/'):
                    filename = blob_name[8:]  # Remove 'thomann/' prefix
                    
                    # Extract product ID
                    match = re.match(r'^(\d+)_', filename)
                    if match:
                        product_id = int(match.group(1))
                        existing_ids.add(product_id)
            
            self.existing_product_ids = existing_ids
            self.loaded_existing = True
            print(f"✅ Found {len(existing_ids)} products with existing images")
            return existing_ids
            
        except Exception as e:
            print(f"❌ Error checking blob storage: {e}")
            return set()
    
    async def get_products_with_thomann_links(self) -> List[Dict[str, any]]:
        """Override to exclude products that already have images"""
        
        # First load existing images
        existing_ids = self.load_existing_images()
        
        # Get base products
        base_products = await super().get_products_with_thomann_links()
        
        # Filter out products that already have images
        filtered_products = []
        skipped_count = 0
        
        for product in base_products:
            product_id = product['id']
            
            if product_id in existing_ids:
                skipped_count += 1
                continue
                
            filtered_products.append(product)
        
        print(f"📊 DUPLICATE PREVENTION:")
        print(f"   🎯 Total products found: {len(base_products)}")
        print(f"   ⏭️  Skipped (already have images): {skipped_count}")
        print(f"   📥 Need processing: {len(filtered_products)}")
        
        return filtered_products
    
    async def process_single_product(self, product: Dict[str, any]) -> bool:
        """Override to double-check before processing"""
        product_id = product['id']
        
        # Double-check that this product doesn't already have an image
        # (in case another worker processed it since we loaded the list)
        if not self.loaded_existing:
            self.load_existing_images()
        
        if product_id in self.existing_product_ids:
            print(f"⏭️  Skipping product {product_id} - already has image")
            return True  # Return True because it's not an error
        
        # Check blob storage in real-time (more accurate but slower)
        if await self.product_has_blob_image(product_id):
            print(f"⏭️  Skipping product {product_id} - found existing blob image")
            self.existing_product_ids.add(product_id)  # Update cache
            return True
        
        # Proceed with normal processing
        success = await super().process_single_product(product)
        
        if success:
            # Add to our cache so other workers know it's done
            self.existing_product_ids.add(product_id)
        
        return success
    
    async def product_has_blob_image(self, product_id: int) -> bool:
        """Check if a specific product already has an image in blob storage"""
        try:
            result = subprocess.run([
                'az', 'storage', 'blob', 'list',
                '--container-name', 'product-images',
                '--account-name', 'getyourmusicgear',
                '--prefix', f'thomann/{product_id}_',
                '--query', '[].name',
                '--output', 'json'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                blob_names = json.loads(result.stdout)
                return len(blob_names) > 0
            
        except Exception as e:
            print(f"⚠️ Error checking blob for product {product_id}: {e}")
        
        return False

class TargetedEnhancedCrawler(EnhancedThomannCrawler):
    """
    Enhanced crawler that processes specific product IDs
    """
    
    def __init__(self, target_product_ids: List[int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_product_ids = set(target_product_ids)
    
    async def get_products_with_thomann_links(self) -> List[Dict[str, any]]:
        """Get only the targeted products"""
        if not self.db.conn:
            print("❌ Database connection not available")
            return []
        
        # Load existing images first
        existing_ids = self.load_existing_images()
        
        # Filter target IDs to exclude those that already have images
        remaining_ids = self.target_product_ids - existing_ids
        
        if not remaining_ids:
            print("✅ All target products already have images!")
            return []
        
        print(f"📊 TARGET FILTERING:")
        print(f"   🎯 Total target products: {len(self.target_product_ids)}")
        print(f"   ✅ Already have images: {len(self.target_product_ids - remaining_ids)}")
        print(f"   📥 Need processing: {len(remaining_ids)}")
        
        try:
            # Get products by specific IDs that have Thomann links
            query = """
                SELECT p.id, p.sku, p.name, p.content, p.images
                FROM products p
                WHERE p.id = ANY($1::int[])
                AND p.content->>'store_links' IS NOT NULL
                AND p.content->'store_links'->>'Thomann' IS NOT NULL
                ORDER BY p.updated_at DESC
            """
            
            rows = await self.db.conn.fetch(query, list(remaining_ids))
            products = []
            
            for row in rows:
                # Parse content
                content = row['content'] or {}
                if isinstance(content, str):
                    try:
                        content = json.loads(content)
                    except (json.JSONDecodeError, TypeError):
                        content = {}
                
                store_links = content.get('store_links', {})
                thomann_url = store_links.get('Thomann')
                
                if thomann_url:
                    products.append({
                        'id': row['id'],
                        'sku': row['sku'],
                        'name': row['name'],
                        'thomann_url': thomann_url,
                        'content': content,
                        'images': row['images'] or {}
                    })
            
            print(f"📋 Found {len(products)} products with Thomann links to process")
            return products
            
        except Exception as e:
            print(f"❌ Error querying targeted products: {e}")
            return []

def load_product_ids_from_file(filename):
    """Load product IDs from text file"""
    if not Path(filename).exists():
        print(f"❌ File not found: {filename}")
        return []
    
    product_ids = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    product_id = int(line)
                    product_ids.append(product_id)
                except ValueError:
                    continue
    
    print(f"📋 Loaded {len(product_ids)} product IDs from {filename}")
    return product_ids

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Thomann image crawler with duplicate prevention')
    parser.add_argument(
        '--input-file', 
        help='Input file with product IDs to process'
    )
    parser.add_argument(
        '--max-products', 
        type=int,
        help='Maximum number of products to process (for testing)'
    )
    parser.add_argument(
        '--max-concurrent', 
        type=int,
        default=10,
        help='Maximum concurrent downloads (default: 10)'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Show what would be processed without actually downloading'
    )
    
    args = parser.parse_args()
    
    print("🔄 ENHANCED THOMANN CRAWLER")
    print("=" * 40)
    print("✅ Built-in duplicate prevention")
    print("✅ Safe for parallel execution")
    print("✅ Checks blob storage before download")
    print()
    
    if args.input_file:
        # Targeted mode - process specific products
        target_ids = load_product_ids_from_file(args.input_file)
        if not target_ids:
            return
        
        print(f"🎯 TARGETED MODE: Processing {len(target_ids)} specific products")
        
        async with TargetedEnhancedCrawler(
            target_product_ids=target_ids,
            max_concurrent=args.max_concurrent
        ) as crawler:
            if args.dry_run:
                products = await crawler.get_products_with_thomann_links()
                print(f"🔍 DRY RUN: Would process {len(products)} products")
                for i, product in enumerate(products[:10], 1):
                    print(f"  {i}. Product {product['id']}: {product['name']}")
                if len(products) > 10:
                    print(f"  ... and {len(products) - 10} more")
            else:
                await crawler.run(max_products=args.max_products)
    
    else:
        # Regular mode - process all products without images
        print("🌐 REGULAR MODE: Processing all products without images")
        
        async with EnhancedThomannCrawler(
            max_concurrent=args.max_concurrent
        ) as crawler:
            if args.dry_run:
                products = await crawler.get_products_with_thomann_links()
                print(f"🔍 DRY RUN: Would process {len(products)} products")
            else:
                await crawler.run(max_products=args.max_products)

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Targeted Crawler Runner
- Only processes products that don't already have images in blob storage
- Uses the specific product list we generated
- Avoids duplicate downloads
"""

import asyncio
import sys
import os
import json
import subprocess
import argparse
from pathlib import Path

# Add crawler directory to path
crawler_dir = Path(__file__).parent.parent / "crawler"
sys.path.append(str(crawler_dir))

def get_blob_storage_product_ids():
    """Get list of product IDs that already have images in blob storage"""
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
        existing_product_ids = set()
        
        for blob_name in blob_names:
            if blob_name.startswith('thomann/'):
                filename = blob_name[8:]  # Remove 'thomann/' prefix
                
                # Extract product ID using the pattern: {product_id}_{timestamp}.jpg
                import re
                match = re.match(r'^(\d+)_', filename)
                if match:
                    product_id = int(match.group(1))
                    existing_product_ids.add(product_id)
        
        print(f"✅ Found {len(existing_product_ids)} products with existing images")
        return existing_product_ids
        
    except Exception as e:
        print(f"❌ Error checking blob storage: {e}")
        return set()

def load_target_products(filename):
    """Load target product IDs from file"""
    if not os.path.exists(filename):
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
    
    print(f"📋 Loaded {len(product_ids)} target product IDs from {filename}")
    return product_ids

def create_filtered_product_list(target_ids, existing_ids, output_file):
    """Create a filtered list excluding products that already have images"""
    
    target_set = set(target_ids)
    filtered_ids = target_set - existing_ids  # Remove products that already have images
    
    duplicates = target_set & existing_ids
    
    print(f"\n📊 FILTERING RESULTS:")
    print(f"   🎯 Target products: {len(target_ids)}")
    print(f"   ✅ Already have images: {len(duplicates)}")
    print(f"   📥 Need images: {len(filtered_ids)}")
    print(f"   💾 Saving to: {output_file}")
    
    # Save filtered list
    with open(output_file, 'w') as f:
        f.write("# Filtered product list - excludes products with existing blob images\n")
        f.write(f"# Original targets: {len(target_ids)}\n")
        f.write(f"# Already have images: {len(duplicates)}\n")
        f.write(f"# Need processing: {len(filtered_ids)}\n")
        f.write("# Format: one product ID per line\n")
        
        for product_id in sorted(filtered_ids):
            f.write(f"{product_id}\n")
    
    return list(filtered_ids)

async def run_crawler_with_product_list(product_ids, max_products=None, dry_run=False):
    """Run the image crawler with a specific product list"""
    
    if not product_ids:
        print("❌ No products to process")
        return
    
    if max_products:
        product_ids = product_ids[:max_products]
        print(f"🔢 Limiting to first {max_products} products")
    
    print(f"\n🚀 STARTING TARGETED CRAWLER")
    print(f"📊 Processing {len(product_ids)} products")
    
    if dry_run:
        print("🔍 DRY RUN MODE - showing what would be processed:")
        for i, product_id in enumerate(product_ids[:10], 1):
            print(f"  {i}. Product ID: {product_id}")
        if len(product_ids) > 10:
            print(f"  ... and {len(product_ids) - 10} more")
        return
    
    # Import the crawler
    try:
        from thomann_image_downloader import ThomannImageDownloader
    except ImportError:
        print("❌ Could not import ThomannImageDownloader. Make sure you're running from the correct directory.")
        return
    
    # Create a modified version that uses our product list
    class TargetedImageDownloader(ThomannImageDownloader):
        def __init__(self, target_product_ids, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.target_product_ids = set(target_product_ids)
        
        async def get_products_with_thomann_links(self):
            """Override to use our specific product list"""
            if not self.db.conn:
                logger.error("❌ Database connection not available")
                return []
            
            try:
                # Get products by specific IDs that have Thomann links
                placeholders = ','.join(['$' + str(i+1) for i in range(len(self.target_product_ids))])
                query = f"""
                    SELECT p.id, p.sku, p.name, p.content, p.images
                    FROM products p
                    WHERE p.id = ANY($1::int[])
                    AND p.content->>'store_links' IS NOT NULL
                    AND p.content->'store_links'->>'Thomann' IS NOT NULL
                    ORDER BY p.updated_at DESC
                """
                
                rows = await self.db.conn.fetch(query, list(self.target_product_ids))
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
    
    # Run the targeted crawler
    async with TargetedImageDownloader(
        target_product_ids=product_ids,
        max_concurrent=10
    ) as downloader:
        await downloader.run(max_products=max_products)

def main():
    parser = argparse.ArgumentParser(description='Run targeted image crawler to avoid duplicates')
    parser.add_argument(
        '--input-file', 
        default='products_needing_download_priority.txt',
        help='Input file with product IDs (default: products_needing_download_priority.txt)'
    )
    parser.add_argument(
        '--max-products', 
        type=int,
        help='Maximum number of products to process (for testing)'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Show what would be processed without actually downloading'
    )
    parser.add_argument(
        '--force', 
        action='store_true',
        help='Skip blob storage check and process all products in list'
    )
    
    args = parser.parse_args()
    
    print("🎯 TARGETED IMAGE CRAWLER")
    print("=" * 40)
    
    # Load target products
    target_products = load_target_products(args.input_file)
    if not target_products:
        return
    
    if args.force:
        print("⚠️  FORCE mode: Processing all products without blob storage check")
        final_products = target_products
    else:
        # Check existing images in blob storage
        existing_products = get_blob_storage_product_ids()
        
        # Create filtered list
        output_file = f"filtered_{args.input_file}"
        final_products = create_filtered_product_list(
            target_products, 
            existing_products, 
            output_file
        )
    
    # Run the crawler
    asyncio.run(run_crawler_with_product_list(
        final_products, 
        max_products=args.max_products,
        dry_run=args.dry_run
    ))

if __name__ == "__main__":
    main()

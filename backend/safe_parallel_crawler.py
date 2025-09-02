#!/usr/bin/env python3
"""
Safe Parallel Image Crawler
- Prevents duplicate downloads by using distributed locking
- Allows parallel processing without conflicts
- Tracks which products are being processed
- Ensures one image per product
"""

import asyncio
import json
import os
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
from pathlib import Path
import sys

# Add crawler directory to path
crawler_dir = Path(__file__).parent.parent / "crawler"
sys.path.append(str(crawler_dir))

class SafeParallelCrawler:
    """
    Manages parallel crawling with distributed locking to prevent duplicates
    """
    
    def __init__(self, lock_dir="./crawler_locks", lock_timeout_minutes=30):
        self.lock_dir = Path(lock_dir)
        self.lock_dir.mkdir(exist_ok=True)
        self.lock_timeout = timedelta(minutes=lock_timeout_minutes)
        self.processed_products = set()
        
    def _get_lock_file(self, product_id: int) -> Path:
        """Get lock file path for a product"""
        return self.lock_dir / f"product_{product_id}.lock"
    
    def _create_lock(self, product_id: int, worker_id: str) -> bool:
        """
        Create a lock for a product. Returns True if lock acquired, False if already locked.
        """
        lock_file = self._get_lock_file(product_id)
        
        # Check if lock already exists and is still valid
        if lock_file.exists():
            try:
                with open(lock_file, 'r') as f:
                    lock_data = json.load(f)
                
                lock_time = datetime.fromisoformat(lock_data['timestamp'])
                if datetime.now() - lock_time < self.lock_timeout:
                    # Lock is still valid
                    return False
                else:
                    # Lock expired, remove it
                    lock_file.unlink()
            except (json.JSONDecodeError, KeyError, ValueError):
                # Corrupted lock file, remove it
                lock_file.unlink()
        
        # Create new lock
        try:
            lock_data = {
                'product_id': product_id,
                'worker_id': worker_id,
                'timestamp': datetime.now().isoformat(),
                'pid': os.getpid()
            }
            
            with open(lock_file, 'w') as f:
                json.dump(lock_data, f)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create lock for product {product_id}: {e}")
            return False
    
    def _release_lock(self, product_id: int):
        """Release lock for a product"""
        lock_file = self._get_lock_file(product_id)
        try:
            if lock_file.exists():
                lock_file.unlink()
        except Exception as e:
            print(f"⚠️ Failed to release lock for product {product_id}: {e}")
    
    def cleanup_expired_locks(self):
        """Clean up expired lock files"""
        cleaned = 0
        for lock_file in self.lock_dir.glob("product_*.lock"):
            try:
                with open(lock_file, 'r') as f:
                    lock_data = json.load(f)
                
                lock_time = datetime.fromisoformat(lock_data['timestamp'])
                if datetime.now() - lock_time >= self.lock_timeout:
                    lock_file.unlink()
                    cleaned += 1
                    
            except Exception:
                # Corrupted lock file, remove it
                lock_file.unlink()
                cleaned += 1
        
        if cleaned > 0:
            print(f"🧹 Cleaned up {cleaned} expired locks")
    
    async def safe_worker(self, worker_id: str, queue: asyncio.Queue, downloader_class):
        """
        Safe worker that uses locking to prevent duplicate processing
        """
        print(f"🔧 {worker_id} started")
        
        while True:
            try:
                # Get a product from the queue with timeout
                product = await asyncio.wait_for(queue.get(), timeout=1.0)
                product_id = product['id']
                
                # Try to acquire lock for this product
                if not self._create_lock(product_id, worker_id):
                    print(f"🔒 {worker_id}: Product {product_id} already being processed, skipping")
                    queue.task_done()
                    continue
                
                try:
                    print(f"🔨 {worker_id} processing: {product['name'][:50]}... (ID: {product_id})")
                    
                    # Create a single-product downloader instance
                    async with downloader_class(max_concurrent=1) as downloader:
                        success = await downloader.process_single_product(product)
                    
                    if success:
                        print(f"✅ {worker_id} completed: Product {product_id}")
                        self.processed_products.add(product_id)
                    else:
                        print(f"❌ {worker_id} failed: Product {product_id}")
                
                finally:
                    # Always release the lock
                    self._release_lock(product_id)
                    queue.task_done()
                
            except asyncio.TimeoutError:
                # No more work available, exit gracefully
                print(f"🏁 {worker_id} finished - no more work")
                break
            except asyncio.CancelledError:
                print(f"🛑 {worker_id} cancelled")
                break
            except Exception as e:
                print(f"❌ {worker_id} error: {e}")
                if 'product_id' in locals():
                    self._release_lock(product_id)
                queue.task_done()

class SafeThomannCrawler:
    """
    Modified Thomann crawler that works with the safe parallel system
    """
    
    def __init__(self, target_product_ids: List[int], max_workers=10):
        self.target_product_ids = set(target_product_ids)
        self.max_workers = max_workers
        self.safe_crawler = SafeParallelCrawler()
        
    async def get_target_products(self):
        """Get the specific products we want to process"""
        # Import here to avoid circular imports
        sys.path.append('../crawler')
        from database_manager import DatabaseManager
        
        db = DatabaseManager()
        await db.__aenter__()
        
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
            
            rows = await db.conn.fetch(query, list(self.target_product_ids))
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
            
            print(f"📋 Found {len(products)} target products with Thomann links")
            return products
            
        finally:
            await db.__aexit__(None, None, None)
    
    async def run_safe_parallel(self, dry_run=False, max_products=None):
        """Run the crawler with safe parallel processing"""
        
        # Clean up any expired locks first
        self.safe_crawler.cleanup_expired_locks()
        
        # Get target products
        products = await self.get_target_products()
        
        if not products:
            print("✅ No products found to process")
            return
        
        if max_products:
            products = products[:max_products]
            print(f"🔢 Limiting to first {max_products} products")
        
        print(f"🚀 Starting safe parallel crawler with {self.max_workers} workers")
        print(f"📊 Processing {len(products)} products")
        
        if dry_run:
            print("🔍 DRY RUN MODE - showing what would be processed:")
            for i, product in enumerate(products[:10], 1):
                print(f"  {i}. Product {product['id']}: {product['name']}")
            if len(products) > 10:
                print(f"  ... and {len(products) - 10} more")
            return
        
        # Import the image downloader
        from thomann_image_downloader import ThomannImageDownloader
        
        # Create work queue
        work_queue = asyncio.Queue()
        
        # Add all products to the queue
        for product in products:
            await work_queue.put(product)
        
        # Create safe worker tasks
        workers = []
        for i in range(min(self.max_workers, len(products))):
            worker_id = f"worker-{i+1}"
            worker = asyncio.create_task(
                self.safe_crawler.safe_worker(worker_id, work_queue, ThomannImageDownloader)
            )
            workers.append(worker)
        
        # Wait for all work to be done
        await work_queue.join()
        
        # Cancel all workers
        for worker in workers:
            worker.cancel()
        
        # Wait for workers to finish cancellation
        await asyncio.gather(*workers, return_exceptions=True)
        
        print(f"\n🏁 Safe parallel crawler completed!")
        print(f"📊 Successfully processed: {len(self.safe_crawler.processed_products)} products")
        
        # Clean up lock files
        self.safe_crawler.cleanup_expired_locks()

def load_product_ids_from_file(filename):
    """Load product IDs from text file"""
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
    
    print(f"📋 Loaded {len(product_ids)} product IDs from {filename}")
    return product_ids

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Safe parallel image crawler')
    parser.add_argument(
        '--input-file', 
        default='products_needing_download_priority.txt',
        help='Input file with product IDs'
    )
    parser.add_argument(
        '--max-workers', 
        type=int,
        default=10,
        help='Maximum number of parallel workers (default: 10)'
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
        '--cleanup-locks', 
        action='store_true',
        help='Clean up expired lock files and exit'
    )
    
    args = parser.parse_args()
    
    print("🔒 SAFE PARALLEL IMAGE CRAWLER")
    print("=" * 50)
    
    if args.cleanup_locks:
        safe_crawler = SafeParallelCrawler()
        safe_crawler.cleanup_expired_locks()
        print("✅ Lock cleanup completed")
        return
    
    # Load target product IDs
    product_ids = load_product_ids_from_file(args.input_file)
    if not product_ids:
        return
    
    # Create and run safe crawler
    crawler = SafeThomannCrawler(
        target_product_ids=product_ids,
        max_workers=args.max_workers
    )
    
    await crawler.run_safe_parallel(
        dry_run=args.dry_run,
        max_products=args.max_products
    )

if __name__ == "__main__":
    asyncio.run(main())

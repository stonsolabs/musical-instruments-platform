#!/usr/bin/env python3
"""
Distributed Thomann Image Downloader
- Uses database-based distributed locking to prevent duplicate processing
- Safe for multiple replicas processing the same product list
- Guarantees each product is processed only once across all replicas
- Prevents proxy waste
"""

import asyncio
import json
import os
import time
import random
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from loguru import logger
import sys

# Import the base downloader
from thomann_image_downloader import ThomannImageDownloader
from database_manager import DatabaseManager

class DistributedImageDownloader(ThomannImageDownloader):
    """
    Enhanced downloader with distributed locking using database
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.replica_id = os.getenv('CONTAINER_APP_REPLICA_NAME', f"replica-{random.randint(1000, 9999)}")
        self.lock_timeout_minutes = 30  # Lock expires after 30 minutes
        logger.info(f"🔧 Distributed downloader initialized with replica ID: {self.replica_id}")
    
    async def create_processing_lock(self, product_id: int) -> bool:
        """
        Create a distributed lock for a product using database
        Returns True if lock acquired, False if already locked by another replica
        """
        if not self.db.conn:
            return False
        
        try:
            # Try to insert a lock record
            lock_expires_at = datetime.utcnow() + timedelta(minutes=self.lock_timeout_minutes)
            
            query = """
                INSERT INTO processing_locks (product_id, replica_id, locked_at, expires_at)
                VALUES ($1, $2, NOW(), $3)
                ON CONFLICT (product_id) DO NOTHING
                RETURNING product_id
            """
            
            result = await self.db.conn.fetchrow(query, product_id, self.replica_id, lock_expires_at)
            
            if result:
                logger.info(f"🔒 {self.replica_id}: Acquired lock for product {product_id}")
                return True
            else:
                # Lock already exists, check if it's expired
                check_query = """
                    SELECT replica_id, locked_at, expires_at 
                    FROM processing_locks 
                    WHERE product_id = $1
                """
                existing_lock = await self.db.conn.fetchrow(check_query, product_id)
                
                if existing_lock and datetime.utcnow() > existing_lock['expires_at']:
                    # Lock expired, try to take it over
                    update_query = """
                        UPDATE processing_locks 
                        SET replica_id = $2, locked_at = NOW(), expires_at = $3
                        WHERE product_id = $1 AND expires_at < NOW()
                        RETURNING product_id
                    """
                    result = await self.db.conn.fetchrow(update_query, product_id, self.replica_id, lock_expires_at)
                    
                    if result:
                        logger.info(f"🔄 {self.replica_id}: Took over expired lock for product {product_id}")
                        return True
                
                if existing_lock:
                    logger.debug(f"🔒 {self.replica_id}: Product {product_id} locked by {existing_lock['replica_id']}")
                return False
                
        except Exception as e:
            logger.error(f"❌ {self.replica_id}: Error creating lock for product {product_id}: {e}")
            return False
    
    async def release_processing_lock(self, product_id: int):
        """Release the distributed lock for a product"""
        if not self.db.conn:
            return
        
        try:
            query = """
                DELETE FROM processing_locks 
                WHERE product_id = $1 AND replica_id = $2
            """
            await self.db.conn.execute(query, product_id, self.replica_id)
            logger.debug(f"🔓 {self.replica_id}: Released lock for product {product_id}")
            
        except Exception as e:
            logger.error(f"❌ {self.replica_id}: Error releasing lock for product {product_id}: {e}")
    
    async def ensure_locks_table_exists(self):
        """Create the processing_locks table if it doesn't exist"""
        if not self.db.conn:
            return
        
        try:
            create_table_query = """
                CREATE TABLE IF NOT EXISTS processing_locks (
                    product_id INTEGER PRIMARY KEY,
                    replica_id VARCHAR(100) NOT NULL,
                    locked_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    expires_at TIMESTAMP NOT NULL
                );
                
                CREATE INDEX IF NOT EXISTS idx_processing_locks_expires_at 
                ON processing_locks(expires_at);
            """
            await self.db.conn.execute(create_table_query)
            logger.info("✅ Processing locks table ready")
            
        except Exception as e:
            logger.error(f"❌ Error creating locks table: {e}")
    
    async def cleanup_expired_locks(self):
        """Clean up expired locks from previous runs"""
        if not self.db.conn:
            return
        
        try:
            query = "DELETE FROM processing_locks WHERE expires_at < NOW()"
            result = await self.db.conn.execute(query)
            # Extract number of deleted rows from result
            deleted_count = int(result.split()[-1]) if result and result.split() else 0
            if deleted_count > 0:
                logger.info(f"🧹 Cleaned up {deleted_count} expired locks")
                
        except Exception as e:
            logger.error(f"❌ Error cleaning up expired locks: {e}")
    
    async def process_single_product(self, product: Dict[str, Any]) -> bool:
        """
        Override to use distributed locking
        """
        product_id = product['id']
        
        # Try to acquire distributed lock
        if not await self.create_processing_lock(product_id):
            logger.info(f"⏭️  {self.replica_id}: Skipping product {product_id} - locked by another replica")
            return True  # Not an error, just skip
        
        try:
            # Double-check blob storage (in case another replica just finished)
            existing_products = self.load_existing_blob_products()
            if product_id in existing_products:
                logger.info(f"⏭️  {self.replica_id}: Product {product_id} already processed by another replica")
                return True
            
            # Process the product
            logger.info(f"🔨 {self.replica_id}: Processing product {product_id}")
            success = await super().process_single_product(product)
            
            if success:
                logger.info(f"✅ {self.replica_id}: Successfully processed product {product_id}")
            else:
                logger.error(f"❌ {self.replica_id}: Failed to process product {product_id}")
            
            return success
            
        finally:
            # Always release the lock
            await self.release_processing_lock(product_id)
    
    async def distributed_worker(self, worker_id: str, queue: asyncio.Queue):
        """
        Worker that processes products with distributed locking
        """
        logger.info(f"🔧 {worker_id} started (replica: {self.replica_id})")
        processed_count = 0
        skipped_count = 0
        failed_count = 0
        
        while True:
            try:
                # Get a product from the queue with timeout
                product = await asyncio.wait_for(queue.get(), timeout=1.0)
                
                logger.info(f"🎯 {worker_id}: Got product {product['id']} - {product['name'][:50]}...")
                
                success = await self.process_single_product(product)
                
                if success:
                    processed_count += 1
                else:
                    failed_count += 1
                
                # Mark task as done
                queue.task_done()
                
                # Log progress every 10 products
                if (processed_count + failed_count) % 10 == 0:
                    logger.info(f"📊 {worker_id} progress: {processed_count} processed, {failed_count} failed")
                
            except asyncio.TimeoutError:
                # No more work available
                logger.info(f"🏁 {worker_id} finished - no more work (processed: {processed_count}, failed: {failed_count})")
                break
            except asyncio.CancelledError:
                logger.info(f"🛑 {worker_id} cancelled")
                break
            except Exception as e:
                logger.error(f"❌ {worker_id} error: {e}")
                failed_count += 1
                queue.task_done()
        
        return processed_count, failed_count
    
    async def run_distributed(self, max_products: Optional[int] = None):
        """
        Run with distributed processing across multiple replicas
        """
        logger.info(f"🚀 Starting distributed image downloader (replica: {self.replica_id})")
        
        # Setup locks table and cleanup
        await self.ensure_locks_table_exists()
        await self.cleanup_expired_locks()
        
        # Get products that need processing (with blob storage filtering)
        products = await self.get_products_with_thomann_links()
        
        if not products:
            logger.info("✅ No products found that need images")
            return
        
        if max_products:
            products = products[:max_products]
            logger.info(f"🔢 Limiting to first {max_products} products")
        
        logger.info(f"📊 Processing {len(products)} products with {self.max_concurrent} workers")
        logger.info(f"🔒 Using distributed locking to prevent duplicate processing")
        
        # Create work queue
        work_queue = asyncio.Queue()
        
        # Add all products to the queue
        for product in products:
            await work_queue.put(product)
        
        # Create worker tasks
        workers = []
        for i in range(min(self.max_concurrent, len(products))):
            worker_id = f"{self.replica_id}-worker-{i+1}"
            worker = asyncio.create_task(self.distributed_worker(worker_id, work_queue))
            workers.append(worker)
        
        # Wait for all work to be done
        await work_queue.join()
        
        # Cancel all workers
        for worker in workers:
            worker.cancel()
        
        # Wait for workers to finish and collect results
        results = await asyncio.gather(*workers, return_exceptions=True)
        
        # Calculate totals
        total_processed = sum(r[0] for r in results if isinstance(r, tuple))
        total_failed = sum(r[1] for r in results if isinstance(r, tuple))
        
        logger.info(f"🏁 Distributed processing completed!")
        logger.info(f"📊 Replica {self.replica_id} summary:")
        logger.info(f"   ✅ Successfully processed: {total_processed}")
        logger.info(f"   ❌ Failed: {total_failed}")
        logger.info(f"   📥 Total handled: {total_processed + total_failed}")

# Override the main function to use distributed processing
async def main():
    """Main function for distributed processing"""
    max_concurrent = int(os.getenv('MAX_CONCURRENT_DOWNLOADS', '10'))
    test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
    max_products = int(os.getenv('MAX_TEST_PRODUCTS', '0')) if test_mode else None
    
    logger.info(f"🚀 Starting distributed downloader with max_concurrent={max_concurrent}")
    
    async with DistributedImageDownloader(max_concurrent=max_concurrent, test_mode=test_mode) as downloader:
        await downloader.run_distributed(max_products=max_products)

if __name__ == "__main__":
    asyncio.run(main())

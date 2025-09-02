#!/usr/bin/env python3
"""
Test Distributed Locking
Simulate multiple replicas and verify only one processes each product
"""

import asyncio
import random
from distributed_image_downloader import DistributedImageDownloader

class MockDistributedDownloader(DistributedImageDownloader):
    """Mock version for testing without actually downloading images"""
    
    def __init__(self, replica_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.replica_id = replica_name
        self.processed_products = []
        self.skipped_products = []
    
    async def process_single_product(self, product):
        """Mock processing - just simulate work"""
        product_id = product['id']
        
        # Try to acquire lock
        if not await self.create_processing_lock(product_id):
            self.skipped_products.append(product_id)
            return True
        
        try:
            # Simulate processing time
            await asyncio.sleep(random.uniform(0.1, 0.3))
            self.processed_products.append(product_id)
            print(f"✅ {self.replica_id}: Processed product {product_id}")
            return True
            
        finally:
            await self.release_processing_lock(product_id)

async def test_distributed_locking():
    """Test that multiple replicas don't process the same products"""
    print("🧪 Testing Distributed Locking")
    print("=" * 50)
    
    # Create mock products
    test_products = [
        {'id': i, 'name': f'Test Product {i}', 'thomann_url': f'https://test.com/{i}'}
        for i in range(1001, 1021)  # 20 test products
    ]
    
    print(f"📦 Testing with {len(test_products)} products")
    
    # Create multiple replica instances
    replicas = []
    for i in range(3):
        replica = MockDistributedDownloader(
            replica_name=f"test-replica-{i+1}",
            max_concurrent=5,
            test_mode=True
        )
        replicas.append(replica)
    
    # Start all replicas simultaneously
    async def run_replica(replica, products):
        async with replica:
            await replica.ensure_locks_table_exists()
            
            # Create queue and add products
            queue = asyncio.Queue()
            for product in products:
                await queue.put(product)
            
            # Start workers
            workers = []
            for j in range(2):  # 2 workers per replica
                worker = asyncio.create_task(
                    replica.distributed_worker(f"{replica.replica_id}-worker-{j+1}", queue)
                )
                workers.append(worker)
            
            # Wait for completion
            await queue.join()
            
            # Cancel workers
            for worker in workers:
                worker.cancel()
            
            await asyncio.gather(*workers, return_exceptions=True)
            
            return replica.processed_products, replica.skipped_products
    
    print("🚀 Starting 3 replicas simultaneously...")
    
    # Run all replicas concurrently
    tasks = [run_replica(replica, test_products) for replica in replicas]
    results = await asyncio.gather(*tasks)
    
    # Analyze results
    print("\n📊 RESULTS:")
    all_processed = []
    all_skipped = []
    
    for i, (processed, skipped) in enumerate(results):
        replica_name = f"replica-{i+1}"
        print(f"   {replica_name}: processed {len(processed)}, skipped {len(skipped)}")
        all_processed.extend(processed)
        all_skipped.extend(skipped)
    
    # Check for duplicates
    processed_set = set(all_processed)
    duplicates = len(all_processed) - len(processed_set)
    
    print(f"\n🔍 ANALYSIS:")
    print(f"   📦 Total products: {len(test_products)}")
    print(f"   ✅ Unique processed: {len(processed_set)}")
    print(f"   🔄 Total skipped: {len(all_skipped)}")
    print(f"   ❌ Duplicates: {duplicates}")
    print(f"   📈 Coverage: {len(processed_set)}/{len(test_products)} ({len(processed_set)/len(test_products)*100:.1f}%)")
    
    # Verify no duplicates
    if duplicates == 0:
        print(f"\n🎉 SUCCESS: No duplicate processing detected!")
        print(f"✅ Distributed locking working perfectly")
    else:
        print(f"\n❌ FAILURE: Found {duplicates} duplicate processes")
        print(f"🐛 Distributed locking needs debugging")
    
    # Show which products were processed vs skipped
    missing_products = set(p['id'] for p in test_products) - processed_set
    if missing_products:
        print(f"\n⚠️  Missing products: {sorted(missing_products)}")

if __name__ == "__main__":
    asyncio.run(test_distributed_locking())

#!/usr/bin/env python3
"""
Test Enhanced Filtering
Test the blob storage filtering to ensure it works correctly
"""

import asyncio
import sys
from thomann_image_downloader import ThomannImageDownloader

async def test_filtering():
    """Test the enhanced filtering functionality"""
    print("🧪 Testing Enhanced Image Downloader Filtering")
    print("=" * 50)
    
    async with ThomannImageDownloader(max_concurrent=1, test_mode=True) as downloader:
        # Test blob storage loading
        print("1. Testing blob storage loading...")
        existing_products = downloader.load_existing_blob_products()
        print(f"   ✅ Found {len(existing_products)} existing products in blob storage")
        
        # Show sample of existing products
        if existing_products:
            sample_ids = list(existing_products)[:10]
            print(f"   📋 Sample existing product IDs: {sample_ids}")
        
        print()
        
        # Test product filtering
        print("2. Testing product filtering...")
        products = await downloader.get_products_with_thomann_links()
        print(f"   ✅ Found {len(products)} products that need processing")
        
        # Show sample of products to process
        if products:
            print(f"   📋 Sample products to process:")
            for i, product in enumerate(products[:5], 1):
                print(f"      {i}. ID: {product['id']} - {product['name']}")
            if len(products) > 5:
                print(f"      ... and {len(products) - 5} more")
        
        print()
        
        # Verify no overlap
        print("3. Verifying no overlap between existing and to-process...")
        product_ids_to_process = {p['id'] for p in products}
        overlap = existing_products & product_ids_to_process
        
        if overlap:
            print(f"   ❌ ERROR: Found {len(overlap)} products in both lists!")
            print(f"   Overlap IDs: {list(overlap)[:10]}")
        else:
            print(f"   ✅ Perfect! No overlap between existing and to-process products")
        
        print()
        
        # Summary
        total_with_thomann = len(existing_products) + len(products)
        print("📊 SUMMARY:")
        print(f"   Products with images in blob: {len(existing_products)}")
        print(f"   Products needing processing: {len(products)}")
        print(f"   Total products with Thomann links: {total_with_thomann}")
        print(f"   Filtering accuracy: {'✅ Perfect' if len(overlap) == 0 else '❌ Has overlaps'}")

if __name__ == "__main__":
    asyncio.run(test_filtering())

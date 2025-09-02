#!/usr/bin/env python3

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from thomann_image_downloader import ThomannImageDownloader
from database_manager import DatabaseManager

async def test_enhanced_filtering():
    """Test the enhanced filtering logic that includes broken image links"""
    
    print("🧪 Testing Enhanced Filtering Logic")
    print("=" * 50)
    
    # Initialize components using async context manager
    async with DatabaseManager() as db:
        downloader = ThomannImageDownloader(test_mode=True)
        downloader.db = db
        
        # Test the enhanced filtering
        products = await downloader.get_products_with_thomann_links()
        
        print(f"\n📊 ENHANCED FILTERING RESULTS:")
        print(f"   🎯 Products identified for processing: {len(products)}")
        print(f"   🎯 Expected: ~2,690 products")
        print(f"   📊 Match: {'✅ YES' if len(products) > 2000 else '❌ NO'}")
        
        if products:
            print(f"\n🔍 Sample products to process:")
            for i, product in enumerate(products[:5], 1):
                print(f"  {i}. ID {product['id']}: {product['name'][:50]}...")
        
        print(f"\n🎯 RESULT: Enhanced crawler will now process {len(products)} products!")

if __name__ == "__main__":
    asyncio.run(test_enhanced_filtering())

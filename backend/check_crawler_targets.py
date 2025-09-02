#!/usr/bin/env python3

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check_products_needing_images():
    """Check how many products actually need image processing"""
    
    # Connect to database
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    print("🔍 Analyzing products that need image processing...")
    
    # 1. Products with Thomann links but NO images in database
    query_no_images = """
        SELECT COUNT(*) as count
        FROM products p
        WHERE p.content->>'store_links' IS NOT NULL
        AND p.content->'store_links'->>'Thomann' IS NOT NULL
        AND (p.images IS NULL 
             OR p.images = '{}' 
             OR p.images = 'null' 
             OR p.images->>'thomann_main' IS NULL)
    """
    
    # 2. All products with Thomann links
    query_all_thomann = """
        SELECT COUNT(*) as count
        FROM products p
        WHERE p.content->>'store_links' IS NOT NULL
        AND p.content->'store_links'->>'Thomann' IS NOT NULL
    """
    
    # 3. Sample products that need processing
    query_sample = """
        SELECT p.id, p.name, p.content->'store_links'->>'Thomann' as thomann_url
        FROM products p
        WHERE p.content->>'store_links' IS NOT NULL
        AND p.content->'store_links'->>'Thomann' IS NOT NULL
        AND (p.images IS NULL 
             OR p.images = '{}' 
             OR p.images = 'null' 
             OR p.images->>'thomann_main' IS NULL)
        ORDER BY p.updated_at DESC
        LIMIT 10
    """
    
    no_images_count = await conn.fetchval(query_no_images)
    all_thomann_count = await conn.fetchval(query_all_thomann)
    sample_products = await conn.fetch(query_sample)
    
    print(f"\n📊 CRAWLER TARGET ANALYSIS:")
    print(f"📈 Total products with Thomann URLs: {all_thomann_count:,}")
    print(f"🎯 Products needing images: {no_images_count:,}")
    print(f"✅ Products with images: {all_thomann_count - no_images_count:,}")
    print(f"📊 Processing percentage: {(no_images_count/all_thomann_count)*100:.1f}%")
    
    print(f"\n🔍 Sample products that need processing:")
    for i, product in enumerate(sample_products[:5], 1):
        print(f"  {i}. ID {product['id']}: {product['name'][:50]}...")
        print(f"     URL: {product['thomann_url']}")
    
    print(f"\n🚨 ISSUE IDENTIFIED:")
    print(f"   Expected to process: {no_images_count:,} products")
    print(f"   Actually processed: 52 products")
    print(f"   Missing: {no_images_count - 52:,} products")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check_products_needing_images())

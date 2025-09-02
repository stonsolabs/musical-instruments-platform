#!/usr/bin/env python3
"""
Check Image Status Script
Shows the current status of products and images in the database
"""

import asyncio
import json
from database_manager import DatabaseManager

async def check_image_status():
    """Check the current status of products and images"""
    
    async with DatabaseManager() as db:
        if not db.conn:
            print("❌ Database connection not available")
            return
        
        print("🔍 Checking Image Status in Database")
        print("=" * 50)
        
        # Total products count
        total_products = await db.conn.fetchval("SELECT COUNT(*) FROM products")
        print(f"📊 Total products: {total_products}")
        
        # Products with Thomann links
        thomann_products = await db.conn.fetchval("""
            SELECT COUNT(*) FROM products 
            WHERE content->>'store_links' IS NOT NULL 
            AND content->'store_links'->>'Thomann' IS NOT NULL
        """)
        print(f"🔗 Products with Thomann links: {thomann_products}")
        
        # Products with images
        products_with_images = await db.conn.fetchval("""
            SELECT COUNT(*) FROM products 
            WHERE images IS NOT NULL AND images != '{}' AND images != 'null'
        """)
        print(f"🖼️  Products with images: {products_with_images}")
        
        # Products with Thomann images specifically
        thomann_images = await db.conn.fetchval("""
            SELECT COUNT(*) FROM products 
            WHERE images->>'thomann_main' IS NOT NULL
        """)
        print(f"🇩🇪 Products with Thomann images: {thomann_images}")
        
        # Products that need images (have Thomann links but no images)
        need_images = await db.conn.fetchval("""
            SELECT COUNT(*) FROM products 
            WHERE content->>'store_links' IS NOT NULL 
            AND content->'store_links'->>'Thomann' IS NOT NULL
            AND (images IS NULL OR images = '{}' OR images = 'null')
        """)
        print(f"⚠️  Products that need images: {need_images}")
        
        print("\n" + "=" * 50)
        
        if need_images > 0:
            print(f"🚀 Ready to download images for {need_images} products!")
            
            # Show some examples of products that need images
            print("\n📋 Example products needing images:")
            examples = await db.conn.fetch("""
                SELECT name, sku, content->'store_links'->>'Thomann' as thomann_url
                FROM products 
                WHERE content->>'store_links' IS NOT NULL 
                AND content->'store_links'->>'Thomann' IS NOT NULL
                AND (images IS NULL OR images = '{}' OR images = 'null')
                LIMIT 5
            """)
            
            for i, row in enumerate(examples, 1):
                print(f"  {i}. {row['name']}")
                print(f"     SKU: {row['sku']}")
                print(f"     Thomann: {row['thomann_url'][:80]}...")
                print()
        else:
            print("✅ All products with Thomann links already have images!")
        
        # Show some examples of products with images
        print("📸 Example products with images:")
        with_images = await db.conn.fetch("""
            SELECT name, sku, images
            FROM products 
            WHERE images->>'thomann_main' IS NOT NULL
            LIMIT 3
        """)
        
        for i, row in enumerate(with_images, 1):
            print(f"  {i}. {row['name']}")
            print(f"     SKU: {row['sku']}")
            image_data = json.loads(row['images']['thomann_main'])
            print(f"     Image URL: {image_data['url'][:80]}...")
            print(f"     Downloaded: {image_data['downloaded_at']}")
            print()

async def main():
    """Main function"""
    try:
        await check_image_status()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

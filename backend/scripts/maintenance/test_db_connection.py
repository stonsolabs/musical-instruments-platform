#!/usr/bin/env python3
"""
Test script to verify database connection and test queries
"""

import asyncio
import os
import asyncpg
from datetime import datetime

async def test_connection():
    """Test database connection and queries"""
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        return
    
    print(f"🔍 Testing connection to: {database_url.split('@')[1] if '@' in database_url else database_url}")
    
    try:
        # Test connection
        conn = await asyncpg.connect(database_url)
        print("✅ Database connection successful")
        
        # Test the query for products missing thomann_main images
        print("\n🔍 Testing query for products missing thomann_main images...")
        
        rows = await conn.fetch("""
            SELECT id, name, images 
            FROM products 
            WHERE (images -> 'thomann_main' ->> 'url') IS NULL 
               OR (images -> 'thomann_main') IS NULL
               OR images = '{}'
               OR images IS NULL
            ORDER BY id
            LIMIT 10
        """)
        
        print(f"✅ Query successful, found {len(rows)} products (showing first 10)")
        
        if rows:
            print("\n📋 Sample products missing images:")
            for row in rows:
                print(f"   ID: {row['id']}, Name: {row['name'][:50]}...")
                if row['images']:
                    print(f"      Current images: {list(row['images'].keys()) if isinstance(row['images'], dict) else 'Invalid format'}")
                else:
                    print(f"      Current images: None/Empty")
                print()
        
        # Test count query
        count_result = await conn.fetchrow("""
            SELECT COUNT(*) as total
            FROM products 
            WHERE (images -> 'thomann_main' ->> 'url') IS NULL 
               OR (images -> 'thomann_main') IS NULL
               OR images = '{}'
               OR images IS NULL
        """)
        
        total_missing = count_result['total'] if count_result else 0
        print(f"📊 Total products missing thomann_main images: {total_missing}")
        
        # Test total products count
        total_products = await conn.fetchrow("SELECT COUNT(*) as total FROM products")
        total_count = total_products['total'] if total_products else 0
        print(f"📊 Total products in database: {total_count}")
        
        await conn.close()
        print("✅ Test completed successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())

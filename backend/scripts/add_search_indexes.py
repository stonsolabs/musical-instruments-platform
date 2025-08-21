#!/usr/bin/env python3
"""
Script to add PostgreSQL full-text search indexes for better search performance.
Run this after the database is set up with sample data.
"""

import asyncio
import asyncpg
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings


async def add_search_indexes():
    """Add full-text search indexes to the database"""
    
    # Connect to database - convert SQLAlchemy URL to asyncpg format
    db_url = settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
    conn = await asyncpg.connect(db_url)
    
    try:
        print("Adding full-text search indexes...")
        
        # Create a GIN index for full-text search on products
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_search_vector 
            ON products 
            USING GIN (
                to_tsvector('english', 
                    COALESCE(name, '') || ' ' ||
                    COALESCE(description, '') || ' ' ||
                    COALESCE(sku, '')
                )
            );
        """)
        
        # Create a combined search vector that includes brand and category names
        # This will be created later when we have the actual search functionality
        # For now, we'll create a simpler version
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_full_search 
            ON products 
            USING GIN (
                to_tsvector('english', 
                    COALESCE(name, '') || ' ' ||
                    COALESCE(description, '') || ' ' ||
                    COALESCE(sku, '')
                )
            );
        """)
        
        # Create a function to update the search vector
        await conn.execute("""
            CREATE OR REPLACE FUNCTION update_product_search_vector()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.search_vector := to_tsvector('english', 
                    COALESCE(NEW.name, '') || ' ' ||
                    COALESCE(NEW.description, '') || ' ' ||
                    COALESCE(NEW.sku, '')
                );
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Add a trigger to automatically update the search vector
        await conn.execute("""
            DROP TRIGGER IF EXISTS trigger_update_product_search_vector ON products;
            CREATE TRIGGER trigger_update_product_search_vector
                BEFORE INSERT OR UPDATE ON products
                FOR EACH ROW
                EXECUTE FUNCTION update_product_search_vector();
        """)
        
        # Add a search_vector column if it doesn't exist
        await conn.execute("""
            ALTER TABLE products 
            ADD COLUMN IF NOT EXISTS search_vector tsvector;
        """)
        
        # Update existing products with search vectors
        await conn.execute("""
            UPDATE products 
            SET search_vector = to_tsvector('english', 
                COALESCE(name, '') || ' ' ||
                COALESCE(description, '') || ' ' ||
                COALESCE(sku, '')
            );
        """)
        
        # Create indexes for better performance on common queries
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_brand_category 
            ON products (brand_id, category_id, is_active);
        """)
        
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_rating_reviews 
            ON products (avg_rating DESC NULLS LAST, review_count DESC NULLS LAST);
        """)
        
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_active_created 
            ON products (is_active, created_at DESC);
        """)
        
        # Create indexes for price-related queries
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_product_prices_available 
            ON product_prices (product_id, is_available, price);
        """)
        
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_product_prices_store 
            ON product_prices (store_id, is_available);
        """)
        
        print("✅ Full-text search indexes added successfully!")
        
        # Show some statistics
        result = await conn.fetchrow("SELECT COUNT(*) as total_products FROM products WHERE is_active = true")
        print(f"📊 Total active products: {result['total_products']}")
        
        result = await conn.fetchrow("SELECT COUNT(*) as total_prices FROM product_prices WHERE is_available = true")
        print(f"💰 Total available prices: {result['total_prices']}")
        
    except Exception as e:
        print(f"❌ Error adding indexes: {e}")
        raise
    finally:
        await conn.close()


async def test_search_functionality():
    """Test the search functionality"""
    
    # Connect to database - convert SQLAlchemy URL to asyncpg format
    db_url = settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
    conn = await asyncpg.connect(db_url)
    
    try:
        print("\n🧪 Testing search functionality...")
        
        # Test basic search
        result = await conn.fetch("""
            SELECT name, brand_id, category_id 
            FROM products 
            WHERE to_tsvector('english', name) @@ plainto_tsquery('english', 'guitar')
            AND is_active = true
            LIMIT 5;
        """)
        
        print(f"🔍 Found {len(result)} products matching 'guitar'")
        for row in result:
            print(f"  - {row['name']}")
        
        # Test combined search with brand and category
        result = await conn.fetch("""
            SELECT p.name, b.name as brand, c.name as category
            FROM products p
            JOIN brands b ON p.brand_id = b.id
            JOIN categories c ON p.category_id = c.id
            WHERE to_tsvector('english', 
                COALESCE(p.name, '') || ' ' ||
                COALESCE(b.name, '') || ' ' ||
                COALESCE(c.name, '')
            ) @@ plainto_tsquery('english', 'fender')
            AND p.is_active = true
            LIMIT 5;
        """)
        
        print(f"\n🎸 Found {len(result)} products matching 'fender'")
        for row in result:
            print(f"  - {row['name']} ({row['brand']} - {row['category']})")
            
    except Exception as e:
        print(f"❌ Error testing search: {e}")
    finally:
        await conn.close()


if __name__ == "__main__":
    print("🚀 Setting up PostgreSQL full-text search indexes...")
    asyncio.run(add_search_indexes())
    asyncio.run(test_search_functionality())
    print("\n✅ Search setup complete!")

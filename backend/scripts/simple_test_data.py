#!/usr/bin/env python3
"""
Simple script to insert test data directly using asyncpg
Usage: python scripts/simple_test_data.py
"""
import asyncio
import asyncpg
from datetime import datetime

DATABASE_URL = "postgresql://admin:qQqqDgXlIuBSZDUlgqzQEcoTPBkrCjVD@dpg-d2er32qdbo4c738oofng-a.frankfurt-postgres.render.com/musicgear_db"

async def create_tables(conn):
    """Create tables if they don't exist"""
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS brands (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            slug VARCHAR(100) UNIQUE NOT NULL,
            logo_url TEXT,
            website_url TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            slug VARCHAR(100) UNIQUE NOT NULL,
            parent_id INTEGER REFERENCES categories(id),
            description TEXT,
            image_url TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS affiliate_stores (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            slug VARCHAR(100) UNIQUE NOT NULL,
            website_url TEXT NOT NULL,
            logo_url TEXT,
            commission_rate DECIMAL(5,2),
            api_endpoint TEXT,
            api_key_encrypted TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            sku VARCHAR(100) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            slug VARCHAR(255) UNIQUE NOT NULL,
            brand_id INTEGER REFERENCES brands(id) NOT NULL,
            category_id INTEGER REFERENCES categories(id) NOT NULL,
            description TEXT,
            specifications JSONB DEFAULT '{}',
            images TEXT[],
            msrp_price DECIMAL(10,2),
            ai_generated_content JSONB DEFAULT '{}',
            avg_rating DECIMAL(3,2) DEFAULT 0,
            review_count INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS product_prices (
            id SERIAL PRIMARY KEY,
            product_id INTEGER REFERENCES products(id) NOT NULL,
            store_id INTEGER REFERENCES affiliate_stores(id) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            currency VARCHAR(3) DEFAULT 'EUR',
            affiliate_url TEXT NOT NULL,
            is_available BOOLEAN DEFAULT TRUE,
            last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

async def insert_test_data(conn):
    """Insert sample data"""
    print("📦 Inserting brands...")
    brands = [
        ("Fender", "fender", "Iconic American guitar manufacturer"),
        ("Gibson", "gibson", "Legendary guitar and instrument maker"),
        ("Yamaha", "yamaha", "Japanese musical instrument giant"),
        ("Roland", "roland", "Electronic music instrument pioneer"),
        ("Marshall", "marshall", "British amplifier manufacturer"),
        ("Ibanez", "ibanez", "Japanese guitar manufacturer"),
    ]
    
    for name, slug, desc in brands:
        await conn.execute("""
            INSERT INTO brands (name, slug, description, created_at) 
            VALUES ($1, $2, $3, CURRENT_TIMESTAMP) 
            ON CONFLICT (slug) DO NOTHING
        """, name, slug, desc)
    
    print("📦 Inserting categories...")
    categories = [
        ("Electric Guitars", "electric-guitars", "Electric guitars and basses"),
        ("Acoustic Guitars", "acoustic-guitars", "Acoustic and classical guitars"),
        ("Digital Keyboards", "digital-keyboards", "Digital pianos and keyboards"),
        ("Synthesizers", "synthesizers", "Analog and digital synthesizers"),
        ("Amplifiers", "amplifiers", "Guitar and bass amplifiers"),
        ("Studio and Recording Equipment", "studio-and-recording-equipment", "Recording interfaces and equipment"),
    ]
    
    for name, slug, desc in categories:
        await conn.execute("""
            INSERT INTO categories (name, slug, description, is_active, created_at) 
            VALUES ($1, $2, $3, TRUE, CURRENT_TIMESTAMP) 
            ON CONFLICT (slug) DO NOTHING
        """, name, slug, desc)
    
    print("📦 Inserting affiliate stores...")
    stores = [
        ("Amazon", "amazon", "https://amazon.es", 4.5),
        ("Thomann", "thomann", "https://thomann.de", 3.0),
        ("Gear4Music", "gear4music", "https://gear4music.com", 4.0),
        ("Kytary", "kytary", "https://kytary.de", 2.5),
    ]
    
    for name, slug, url, commission in stores:
        await conn.execute("""
            INSERT INTO affiliate_stores (name, slug, website_url, commission_rate, is_active, created_at) 
            VALUES ($1, $2, $3, $4, TRUE, CURRENT_TIMESTAMP) 
            ON CONFLICT (slug) DO NOTHING
        """, name, slug, url, commission)
    
    print("📦 Inserting products...")
    # Get brand and category IDs
    fender_id = await conn.fetchval("SELECT id FROM brands WHERE slug = 'fender'")
    yamaha_id = await conn.fetchval("SELECT id FROM brands WHERE slug = 'yamaha'")
    marshall_id = await conn.fetchval("SELECT id FROM brands WHERE slug = 'marshall'")
    
    electric_guitars_id = await conn.fetchval("SELECT id FROM categories WHERE slug = 'electric-guitars'")
    keyboards_id = await conn.fetchval("SELECT id FROM categories WHERE slug = 'digital-keyboards'")
    amplifiers_id = await conn.fetchval("SELECT id FROM categories WHERE slug = 'amplifiers'")
    
    products = [
        ("FENDER-STRAT-MX-SSS", "Fender Player Stratocaster MX", "fender-player-stratocaster-mx", 
         fender_id, electric_guitars_id, "The Player Stratocaster takes the best features of the original.", 799.00),
        ("YAMAHA-P45", "Yamaha P-45 Digital Piano", "yamaha-p-45-digital-piano", 
         yamaha_id, keyboards_id, "Compact digital piano with 88 weighted keys.", 549.00),
        ("MARSHALL-DSL40CR", "Marshall DSL40CR Guitar Amplifier", "marshall-dsl40cr-guitar-amplifier", 
         marshall_id, amplifiers_id, "40-watt tube guitar amplifier with classic Marshall tone.", 899.00),
    ]
    
    for sku, name, slug, brand_id, cat_id, desc, price in products:
        if brand_id and cat_id:
            product_id = await conn.fetchval("""
                INSERT INTO products (sku, name, slug, brand_id, category_id, description, msrp_price, specifications, ai_generated_content, is_active, created_at, updated_at) 
                VALUES ($1, $2, $3, $4, $5, $6, $7, '{}', '{}', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) 
                ON CONFLICT (sku) DO UPDATE SET updated_at = CURRENT_TIMESTAMP
                RETURNING id
            """, sku, name, slug, brand_id, cat_id, desc, price)
            
            # Add prices for each store
            stores_data = await conn.fetch("SELECT id, slug FROM affiliate_stores LIMIT 3")
            for i, store in enumerate(stores_data):
                price_variation = 0.9 + (i * 0.05)
                final_price = price * price_variation
                affiliate_url = f"https://{store['slug']}.com/product/{sku}?aff=123"
                
                await conn.execute("""
                    INSERT INTO product_prices (product_id, store_id, price, affiliate_url) 
                    VALUES ($1, $2, $3, $4) 
                    ON CONFLICT DO NOTHING
                """, product_id, store['id'], final_price, affiliate_url)

async def main():
    print("🔌 Connecting to Render database...")
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("📋 Creating tables...")
        await create_tables(conn)
        
        print("📦 Inserting test data...")
        await insert_test_data(conn)
        
        print("✅ Test data imported successfully!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
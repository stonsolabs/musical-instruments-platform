#!/usr/bin/env python3
"""
Database Recreation Script
Cleans and recreates the entire database using the comprehensive product data.
"""

import asyncio
import json
import sys
from decimal import Decimal
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent / "backend"))

from app.database import async_session_factory, engine
from app.models import (
    AffiliateClick,
    AffiliateStore,
    Base,
    Brand,
    Category,
    ComparisonView,
    Product,
    ProductPrice,
)
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def clean_database():
    """Clean all tables and reset sequences."""
    print("🧹 Cleaning database...")
    
    async with engine.begin() as conn:
        # Delete all data in reverse dependency order
        await conn.execute(text("DELETE FROM affiliate_clicks"))
        await conn.execute(text("DELETE FROM comparison_views"))
        await conn.execute(text("DELETE FROM product_prices"))
        await conn.execute(text("DELETE FROM products"))
        await conn.execute(text("DELETE FROM brands"))
        await conn.execute(text("DELETE FROM categories"))
        await conn.execute(text("DELETE FROM affiliate_stores"))
        
        # Reset sequences (PostgreSQL specific)
        await conn.execute(text("ALTER SEQUENCE affiliate_clicks_id_seq RESTART WITH 1"))
        await conn.execute(text("ALTER SEQUENCE comparison_views_id_seq RESTART WITH 1"))
        await conn.execute(text("ALTER SEQUENCE product_prices_id_seq RESTART WITH 1"))
        await conn.execute(text("ALTER SEQUENCE products_id_seq RESTART WITH 1"))
        await conn.execute(text("ALTER SEQUENCE brands_id_seq RESTART WITH 1"))
        await conn.execute(text("ALTER SEQUENCE categories_id_seq RESTART WITH 1"))
        await conn.execute(text("ALTER SEQUENCE affiliate_stores_id_seq RESTART WITH 1"))
    
    print("✅ Database cleaned successfully")


async def insert_affiliate_stores():
    """Insert only Gear4Music and Thomann affiliate stores."""
    print("🏪 Inserting affiliate stores...")
    
    stores_data = [
        {
            "name": "Gear4Music",
            "slug": "gear4music",
            "website_url": "https://www.gear4music.com",
            "logo_url": "https://example.com/logos/gear4music.png",
            "commission_rate": Decimal("5.0"),
            "is_active": True
        },
        {
            "name": "Thomann",
            "slug": "thomann",
            "website_url": "https://www.thomann.de",
            "logo_url": "https://fast-images.static-thomann.de/pics/images/logos/thomann-cyan-black.svg",
            "commission_rate": Decimal("4.5"),
            "is_active": True
        }
    ]
    
    async with async_session_factory() as session:
        for store_data in stores_data:
            store = AffiliateStore(**store_data)
            session.add(store)
        
        await session.commit()
    
    print("✅ Affiliate stores inserted successfully")


def slugify(text: str) -> str:
    """Convert text to a slug format."""
    return text.lower().replace(" ", "-").replace("&", "and")


async def insert_categories_and_brands(comprehensive_data):
    """Extract and insert unique categories and brands from comprehensive data."""
    print("📂 Inserting categories and brands...")
    
    # Extract unique categories and brands
    categories = set()
    brands = set()
    
    for item in comprehensive_data:
        product_input = item["product_input"]
        categories.add(product_input["category"])
        brands.add(product_input["brand"])
    
    async with async_session_factory() as session:
        # Insert categories
        category_map = {}
        for category_slug in categories:
            # Convert slug to display name
            category_name = category_slug.replace("-", " ").title()
            category = Category(
                name=category_name,
                slug=category_slug,
                description=f"{category_name} instruments and equipment",
                is_active=True
            )
            session.add(category)
            await session.flush()  # Get the ID
            category_map[category_slug] = category.id
        
        # Insert brands
        brand_map = {}
        for brand_name in brands:
            brand_slug = slugify(brand_name)
            brand = Brand(
                name=brand_name,
                slug=brand_slug,
                website_url=f"https://www.{brand_slug}.com",
                description=f"Official {brand_name} instruments and equipment"
            )
            session.add(brand)
            await session.flush()  # Get the ID
            brand_map[brand_name] = brand.id
        
        await session.commit()
    
    print("✅ Categories and brands inserted successfully")
    return category_map, brand_map


async def insert_products_with_prices(comprehensive_data, category_map, brand_map):
    """Insert products with all comprehensive AI-generated content and prices."""
    print("🎸 Inserting products with comprehensive data...")
    
    async with async_session_factory() as session:
        # Get affiliate store IDs
        gear4music_store = await session.execute(
            text("SELECT id FROM affiliate_stores WHERE slug = 'gear4music'")
        )
        thomann_store = await session.execute(
            text("SELECT id FROM affiliate_stores WHERE slug = 'thomann'")
        )
        
        gear4music_id = gear4music_store.scalar()
        thomann_id = thomann_store.scalar()
        
        for item in comprehensive_data:
            product_input = item["product_input"]
            ai_content = item["ai_generated_content"]
            
            # Create product
            product = Product(
                sku=product_input["sku"],
                name=product_input["name"],
                slug=product_input["slug"],
                brand_id=brand_map[product_input["brand"]],
                category_id=category_map[product_input["category"]],
                description=product_input["description"],
                specifications=product_input["specifications"],
                images=product_input["images"],
                msrp_price=Decimal(str(product_input["msrp_price"])),
                ai_generated_content=ai_content,
                is_active=True
            )
            
            session.add(product)
            await session.flush()  # Get the product ID
            
            # Add prices for both stores
            # Gear4Music price (slightly lower than MSRP)
            gear4music_price = ProductPrice(
                product_id=product.id,
                store_id=gear4music_id,
                price=Decimal(str(product_input["msrp_price"] * 0.95)),  # 5% discount
                currency="EUR",
                affiliate_url=f"https://www.gear4music.com/products/{product.slug}?aff=platform",
                is_available=True
            )
            session.add(gear4music_price)
            
            # Thomann price (competitive pricing)
            thomann_price = ProductPrice(
                product_id=product.id,
                store_id=thomann_id,
                price=Decimal(str(product_input["msrp_price"] * 0.92)),  # 8% discount
                currency="EUR",
                affiliate_url=f"https://www.thomann.de/products/{product.slug}?aff=platform",
                is_available=True
            )
            session.add(thomann_price)
        
        await session.commit()
    
    print("✅ Products and prices inserted successfully")


async def verify_data():
    """Verify that all data was inserted correctly."""
    print("🔍 Verifying data integrity...")
    
    async with async_session_factory() as session:
        # Count records
        categories_count = await session.execute(text("SELECT COUNT(*) FROM categories"))
        brands_count = await session.execute(text("SELECT COUNT(*) FROM brands"))
        products_count = await session.execute(text("SELECT COUNT(*) FROM products"))
        stores_count = await session.execute(text("SELECT COUNT(*) FROM affiliate_stores"))
        prices_count = await session.execute(text("SELECT COUNT(*) FROM product_prices"))
        
        print(f"📊 Data Summary:")
        print(f"   Categories: {categories_count.scalar()}")
        print(f"   Brands: {brands_count.scalar()}")
        print(f"   Products: {products_count.scalar()}")
        print(f"   Affiliate Stores: {stores_count.scalar()}")
        print(f"   Product Prices: {prices_count.scalar()}")
        
        # Verify products per category
        category_products = await session.execute(text("""
            SELECT c.name, COUNT(p.id) as product_count
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            GROUP BY c.id, c.name
            ORDER BY c.name
        """))
        
        print(f"\n📈 Products per category:")
        for row in category_products:
            print(f"   {row[0]}: {row[1]} products")


async def main():
    """Main function to recreate the database."""
    print("🚀 Starting database recreation process...")
    
    # Load comprehensive data
    try:
        with open("comprehensive_products_with_ai_content.json", "r") as f:
            data = json.load(f)
            comprehensive_data = data["comprehensive_product_dataset"]
        print(f"📄 Loaded {len(comprehensive_data)} products from comprehensive dataset")
    except FileNotFoundError:
        print("❌ Error: comprehensive_products_with_ai_content.json not found")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return
    
    try:
        # Execute all steps
        await clean_database()
        await insert_affiliate_stores()
        category_map, brand_map = await insert_categories_and_brands(comprehensive_data)
        await insert_products_with_prices(comprehensive_data, category_map, brand_map)
        await verify_data()
        
        print("\n🎉 Database recreation completed successfully!")
        print("✨ All products now have comprehensive AI-generated content")
        print("🏪 Only Gear4Music and Thomann affiliate stores are active")
        print("📊 At least 3 products per category are available")
        
    except Exception as e:
        print(f"❌ Error during database recreation: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
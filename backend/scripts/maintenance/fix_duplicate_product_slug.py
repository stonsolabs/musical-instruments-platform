#!/usr/bin/env python3
"""
Fix duplicate product slug: traveler-guitar-tb-4p-bass-sbt-htm
This script identifies and fixes the duplicate slug issue.
"""

import asyncio
import sys
import os
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

def get_async_session_factory():
    """Create async session factory from DATABASE_URL"""
    database_url = os.getenv("DATABASE_URL", "")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")
    
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        if "ssl=" not in database_url:
            connector = "&" if "?" in database_url else "?"
            database_url = f"{database_url}{connector}ssl=require"
    
    engine = create_async_engine(database_url, echo=False)
    return async_sessionmaker(engine, expire_on_commit=False)

async def find_duplicate_products():
    """Find products with duplicate slug"""
    session_factory = get_async_session_factory()
    async with session_factory() as session:
        result = await session.execute(text("""
            SELECT id, name, slug, is_active
            FROM products
            WHERE slug = 'traveler-guitar-tb-4p-bass-sbt-htm'
            ORDER BY id
        """))
        
        products = result.fetchall()
        print(f"Found {len(products)} products with duplicate slug:")
        for product in products:
            print(f"  ID {product[0]}: {product[1]} (active: {product[3]})")
        
        return products

async def fix_duplicate_slug():
    """Fix duplicate slug by making them unique"""
    products = await find_duplicate_products()
    
    if len(products) <= 1:
        print("✅ No duplicates found")
        return
    
    session_factory = get_async_session_factory()
    async with session_factory() as session:
        # Keep the first one, update the rest
        keep_id = products[0][0]
        print(f"\n✅ Keeping product ID {keep_id} with original slug")
        
        for idx, product in enumerate(products[1:], start=1):
            product_id = product[0]
            new_slug = f"traveler-guitar-tb-4p-bass-sbt-htm-{idx}"
            
            # Check if new slug already exists
            check_result = await session.execute(
                text("SELECT id FROM products WHERE slug = :slug"),
                {"slug": new_slug}
            )
            if check_result.fetchone():
                # If it exists, add product ID
                new_slug = f"traveler-guitar-tb-4p-bass-sbt-htm-{product_id}"
            
            await session.execute(
                text("UPDATE products SET slug = :new_slug WHERE id = :id"),
                {"new_slug": new_slug, "id": product_id}
            )
            print(f"  Updated product ID {product_id} to slug: {new_slug}")
        
        await session.commit()
        print("\n✅ Duplicate slugs fixed!")

if __name__ == "__main__":
    asyncio.run(fix_duplicate_slug())


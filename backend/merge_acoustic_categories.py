#!/usr/bin/env python3.11
"""
Script to merge acoustic guitar categories into a single 'Acoustic Guitars' category.
Merges categories: Travel Guitars (ID 2), Steel String Acoustic Guitars (ID 3), Acoustic Guitar (ID 25)
"""

import asyncio
from app.database import async_session_factory
from app.models import Category, Product
from sqlalchemy import select, update, delete

async def merge_acoustic_categories():
    async with async_session_factory() as db:
        print("Starting acoustic categories merge...")
        
        # Step 1: Create new 'Acoustic Guitars' category
        print("\n1. Creating new 'Acoustic Guitars' category...")
        new_category = Category(
            name="Acoustic Guitars",
            slug="acoustic-guitars",
            description="All acoustic guitar types including steel string, nylon string, and travel guitars",
            is_active=True
        )
        db.add(new_category)
        await db.flush()  # Get the ID
        new_category_id = new_category.id
        print(f"   Created category with ID: {new_category_id}")
        
        # Step 2: Get product counts from old categories
        old_category_ids = [2, 3, 25]  # Travel Guitars, Steel String Acoustic, Acoustic Guitar
        
        for old_id in old_category_ids:
            stmt = select(Category.name).where(Category.id == old_id)
            result = await db.execute(stmt)
            cat_name = result.scalar()
            
            stmt = select(Product.id).where(Product.category_id == old_id)
            result = await db.execute(stmt)
            product_count = len(result.all())
            print(f"   Category ID {old_id} ({cat_name}): {product_count} products")
        
        # Step 3: Update all products to new category
        print("\n2. Moving all products to new category...")
        for old_id in old_category_ids:
            stmt = update(Product).where(Product.category_id == old_id).values(category_id=new_category_id)
            result = await db.execute(stmt)
            print(f"   Moved {result.rowcount} products from category {old_id} to {new_category_id}")
        
        # Step 4: Verify the move
        print("\n3. Verifying the merge...")
        stmt = select(Product.id).where(Product.category_id == new_category_id)
        result = await db.execute(stmt)
        total_products = len(result.all())
        print(f"   New 'Acoustic Guitars' category now has {total_products} products")
        
        # Step 5: Remove old categories
        print("\n4. Removing old categories...")
        for old_id in old_category_ids:
            stmt = delete(Category).where(Category.id == old_id)
            await db.execute(stmt)
            print(f"   Deleted category {old_id}")
        
        # Commit the transaction
        await db.commit()
        print("\n✅ Successfully merged acoustic categories!")
        print(f"   All acoustic guitars are now in category '{new_category.name}' (slug: {new_category.slug})")

if __name__ == "__main__":
    asyncio.run(merge_acoustic_categories())
#!/usr/bin/env python3
"""
Fix category name mismatches between database and frontend navigation.
"""

import asyncio
import os
import sys

# Ensure app imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update

from app.models import Product, Category

DATABASE_URL = "postgresql+asyncpg://admin:qQqqDgXlIuBSZDUlgqzQEcoTPBkrCjVD@dpg-d2er32qdbo4c738oofng-a.frankfurt-postgres.render.com/musicgear_db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Category name mappings: database_slug -> frontend_slug
CATEGORY_MAPPINGS = {
    "digital-keyboards": "pianos-keyboards",
    "studio-and-recording-equipment": "studio-production"
}

async def fix_category_names():
    async with async_session_factory() as session:
        try:
            for db_slug, frontend_slug in CATEGORY_MAPPINGS.items():
                # Check if the database category exists
                result = await session.execute(
                    select(Category).where(Category.slug == db_slug)
                )
                db_category = result.scalar_one_or_none()
                
                if db_category:
                    print(f"Found category: {db_slug}")
                    
                    # Check if frontend category already exists
                    result = await session.execute(
                        select(Category).where(Category.slug == frontend_slug)
                    )
                    frontend_category = result.scalar_one_or_none()
                    
                    if frontend_category:
                        print(f"Frontend category {frontend_slug} already exists, updating products...")
                        # Update all products from db_category to frontend_category
                        await session.execute(
                            update(Product)
                            .where(Product.category_id == db_category.id)
                            .values(category_id=frontend_category.id)
                        )
                        print(f"Updated products from {db_slug} to {frontend_slug}")
                        
                        # Delete the old category
                        await session.delete(db_category)
                        print(f"Deleted old category: {db_slug}")
                    else:
                        # Update the existing category slug
                        db_category.slug = frontend_slug
                        db_category.name = frontend_slug.replace("-", " ").title()
                        print(f"Updated category {db_slug} to {frontend_slug}")
                else:
                    print(f"Category {db_slug} not found in database")
            
            await session.commit()
            print("Successfully fixed category name mismatches!")
            
        except Exception as e:
            await session.rollback()
            print(f"Error fixing category names: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(fix_category_names())

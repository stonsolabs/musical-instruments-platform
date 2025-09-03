#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.append('backend')
from app.database import get_db
from app.models import Product
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
import json

async def examine_products():
    async for db in get_db():
        try:
            # Get sample products with relationships pre-loaded
            stmt = select(Product).options(
                selectinload(Product.brand),
                selectinload(Product.category)
            ).limit(10)
            result = await db.execute(stmt)
            products = result.scalars().all()
            
            print('=== PRODUCTS TABLE STRUCTURE ===')
            print(f'Total products found: {len(products)}')
            
            for i, product in enumerate(products):
                print(f'\n--- Product {i+1}: {product.name} ---')
                print(f'ID: {product.id}')
                print(f'Slug: {product.slug}')
                print(f'Category: {product.category.name if product.category else "None"}')
                print(f'Brand: {product.brand.name if product.brand else "None"}')
                print(f'Is Active: {product.is_active}')
                
                if product.content:
                    print(f'Content keys: {list(product.content.keys())}')
                    print('Content structure:')
                    for key, value in product.content.items():
                        if isinstance(value, dict):
                            print(f'  {key}: {list(value.keys()) if value else "Empty dict"}')
                        elif isinstance(value, list):
                            print(f'  {key}: List with {len(value)} items')
                        else:
                            print(f'  {key}: {type(value).__name__} = {str(value)[:100]}')
                else:
                    print('Content: None or empty')
                
                print('---' * 20)
                
        except Exception as e:
            print(f"Error examining products: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(examine_products())

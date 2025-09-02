#!/usr/bin/env python3
"""
Product Data Diagnostic Script
Checks what products exist in the database and their image associations
"""

import asyncio
import json
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload

# Import models
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Product, Brand, Category
from app.config import settings

async def check_product_data():
    """Check product data in the database"""
    
    print("🔍 Checking Product Data in Database")
    print("=" * 50)
    
    # Create async engine
    engine = create_async_engine(settings.ASYNC_DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            # Count total products
            total_products_result = await session.execute(select(func.count(Product.id)))
            total_products = total_products_result.scalar()
            print(f"📊 Total products in database: {total_products}")
            
            if total_products == 0:
                print("❌ No products found in database!")
                print("   This explains why product pages are empty.")
                return
            
            # Count active products
            active_products_result = await session.execute(
                select(func.count(Product.id)).where(Product.is_active == True)
            )
            active_products = active_products_result.scalar()
            print(f"✅ Active products: {active_products}")
            print(f"🚫 Inactive products: {total_products - active_products}")
            
            # Get sample products with details
            print("\n" + "=" * 50)
            print("📋 Sample Product Analysis")
            print("=" * 50)
            
            sample_query = (
                select(Product)
                .options(
                    selectinload(Product.brand),
                    selectinload(Product.category)
                )
                .where(Product.is_active == True)
                .limit(5)
            )
            
            result = await session.execute(sample_query)
            sample_products = result.scalars().all()
            
            if not sample_products:
                print("❌ No active products found!")
                return
            
            for i, product in enumerate(sample_products, 1):
                print(f"\n{i}. Product ID: {product.id}")
                print(f"   Name: {product.name}")
                print(f"   Slug: {product.slug}")
                print(f"   Brand: {product.brand.name if product.brand else 'None'}")
                print(f"   Category: {product.category.name if product.category else 'None'}")
                print(f"   Active: {product.is_active}")
                
                # Check images
                if product.images:
                    print(f"   Images: {len(product.images)} image entries")
                    
                    # Show image structure
                    if isinstance(product.images, dict):
                        for key, image_data in product.images.items():
                            if isinstance(image_data, dict) and "url" in image_data:
                                print(f"     - {key}: {image_data['url']}")
                            elif isinstance(image_data, str):
                                print(f"     - {key}: {image_data}")
                            else:
                                print(f"     - {key}: {type(image_data)} {str(image_data)[:100]}...")
                    else:
                        print(f"     Raw images data: {str(product.images)[:200]}...")
                else:
                    print("   Images: None/Empty")
                
                # Check MSRP price
                print(f"   MSRP Price: ${product.msrp_price}" if product.msrp_price else "   MSRP Price: None")
                
                # Check description
                desc_preview = product.description[:100] + "..." if product.description and len(product.description) > 100 else product.description
                print(f"   Description: {desc_preview}" if product.description else "   Description: None")
            
            # Check image statistics
            print("\n" + "=" * 50)
            print("🖼️  Image Statistics")
            print("=" * 50)
            
            # Count products with images (fix PostgreSQL JSONB comparison)
            products_with_images_result = await session.execute(
                select(func.count(Product.id)).where(
                    Product.is_active == True,
                    Product.images.isnot(None),
                    func.jsonb_typeof(Product.images) != 'null'
                )
            )
            products_with_images = products_with_images_result.scalar()
            
            products_without_images = active_products - products_with_images
            
            print(f"✅ Products with images: {products_with_images}")
            print(f"❌ Products without images: {products_without_images}")
            
            if products_with_images > 0:
                print(f"📊 Image coverage: {(products_with_images/active_products)*100:.1f}%")
            
            # Check brands and categories
            print("\n" + "=" * 50)
            print("🏷️  Brands & Categories")
            print("=" * 50)
            
            brands_result = await session.execute(select(func.count(Brand.id)))
            categories_result = await session.execute(select(func.count(Category.id)))
            
            total_brands = brands_result.scalar()
            total_categories = categories_result.scalar()
            
            print(f"🏢 Total brands: {total_brands}")
            print(f"📂 Total categories: {total_categories}")
            
            # Sample brands
            sample_brands_result = await session.execute(select(Brand).limit(5))
            sample_brands = sample_brands_result.scalars().all()
            
            print("\nSample brands:")
            for brand in sample_brands:
                print(f"  - {brand.name} (slug: {brand.slug})")
            
            # Sample categories  
            sample_categories_result = await session.execute(select(Category).limit(5))
            sample_categories = sample_categories_result.scalars().all()
            
            print("\nSample categories:")
            for category in sample_categories:
                print(f"  - {category.name} (slug: {category.slug})")
        
        except Exception as e:
            print(f"❌ Database error: {e}")
            print(f"   Connection string: {settings.ASYNC_DATABASE_URL[:50]}...")
        
        finally:
            await engine.dispose()
    
    print("\n🏁 Product data check complete!")

if __name__ == "__main__":
    asyncio.run(check_product_data())

#!/usr/bin/env python3
"""
Script to update product images in the database.
This script reads the comprehensive product list with images and updates the database.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_async_session_local
from app.models import Product, Brand, Category
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

async def load_product_data() -> List[Dict[str, Any]]:
    """Load product data from JSON file."""
    json_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "scripts",
        "comprehensive_products_with_images.json"
    )
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data["comprehensive_product_dataset"]

async def get_or_create_brand(session: AsyncSession, brand_name: str) -> Brand:
    """Get existing brand or create new one."""
    # Try to find existing brand
    stmt = select(Brand).where(Brand.name == brand_name)
    result = await session.execute(stmt)
    brand = result.scalars().first()
    
    if brand:
        return brand
    
    # Create new brand
    brand_slug = brand_name.lower().replace(' ', '-').replace('&', 'and')
    new_brand = Brand(
        name=brand_name,
        slug=brand_slug,
        description=f"Premium musical instruments from {brand_name}",
        created_at=datetime.utcnow()
    )
    session.add(new_brand)
    await session.flush()
    return new_brand

async def get_or_create_category(session: AsyncSession, category_slug: str) -> Category:
    """Get existing category or create new one."""
    # Try to find existing category
    stmt = select(Category).where(Category.slug == category_slug)
    result = await session.execute(stmt)
    category = result.scalars().first()
    
    if category:
        return category
    
    # Create new category
    category_names = {
        "electric-guitars": "Electric Guitars",
        "acoustic-guitars": "Acoustic Guitars", 
        "digital-keyboards": "Digital Keyboards",
        "amplifiers": "Amplifiers",
        "bass-guitars": "Bass Guitars",
        "drums-percussion": "Drums & Percussion",
        "effects-pedals": "Effects Pedals",
        "dj-equipment": "DJ Equipment",
        "studio-and-recording-equipment": "Studio & Recording Equipment"
    }
    
    category_name = category_names.get(category_slug, category_slug.replace('-', ' ').title())
    
    new_category = Category(
        name=category_name,
        slug=category_slug,
        description=f"Professional {category_name.lower()} for musicians",
        is_active=True,
        created_at=datetime.utcnow()
    )
    session.add(new_category)
    await session.flush()
    return new_category

async def update_or_create_product(session: AsyncSession, product_data: Dict[str, Any]) -> Product:
    """Update existing product or create new one."""
    product_input = product_data["product_input"]
    
    # Try to find existing product by SKU
    stmt = select(Product).where(Product.sku == product_input["sku"])
    result = await session.execute(stmt)
    existing_product = result.scalars().first()
    
    # Get or create brand and category
    brand = await get_or_create_brand(session, product_input["brand"])
    category = await get_or_create_category(session, product_input["category"])
    
    if existing_product:
        # Update existing product
        update_stmt = update(Product).where(Product.sku == product_input["sku"]).values(
            name=product_input["name"],
            slug=product_input["slug"],
            brand_id=brand.id,
            category_id=category.id,
            description=product_input["description"],
            specifications=product_input["specifications"],
            images=product_input["images"],
            msrp_price=product_input["msrp_price"],
            updated_at=datetime.utcnow()
        )
        await session.execute(update_stmt)
        
        # Fetch the updated product
        result = await session.execute(select(Product).where(Product.sku == product_input["sku"]))
        return result.scalars().first()
    else:
        # Create new product
        new_product = Product(
            sku=product_input["sku"],
            name=product_input["name"],
            slug=product_input["slug"],
            brand_id=brand.id,
            category_id=category.id,
            description=product_input["description"],
            specifications=product_input["specifications"],
            images=product_input["images"],
            msrp_price=product_input["msrp_price"],
            ai_generated_content=product_data.get("ai_generated_content", {}),
            avg_rating=4.5,  # Default rating
            review_count=25,  # Default review count
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(new_product)
        await session.flush()
        return new_product

async def main():
    """Main function to update all products."""
    print("🔄 Starting product image update process...")
    
    try:
        # Load product data
        print("📥 Loading product data from JSON file...")
        products_data = await load_product_data()
        print(f"✅ Loaded {len(products_data)} products")
        
        # Create database session
        async_session = get_async_session_local()
        async with async_session() as session:
            updated_count = 0
            created_count = 0
            
            for i, product_data in enumerate(products_data, 1):
                product_input = product_data["product_input"]
                print(f"🔄 Processing product {i}/{len(products_data)}: {product_input['name']}")
                
                try:
                    # Check if product exists
                    stmt = select(Product).where(Product.sku == product_input["sku"])
                    result = await session.execute(stmt)
                    existing_product = result.scalars().first()
                    
                    if existing_product:
                        updated_count += 1
                        action = "Updated"
                    else:
                        created_count += 1
                        action = "Created"
                    
                    # Update or create product
                    product = await update_or_create_product(session, product_data)
                    
                    print(f"  ✅ {action}: {product.name}")
                    print(f"     Images: {len(product.images)} image(s) added")
                    print(f"     Brand: {product_input['brand']}")
                    print(f"     Category: {product_input['category']}")
                    print(f"     Price: ${product.msrp_price}")
                    
                except Exception as e:
                    print(f"  ❌ Error processing {product_input['name']}: {str(e)}")
                    continue
            
            # Commit all changes
            await session.commit()
            print(f"\n🎉 Database update completed successfully!")
            print(f"📊 Summary:")
            print(f"   • Created: {created_count} new products")
            print(f"   • Updated: {updated_count} existing products")
            print(f"   • Total: {created_count + updated_count} products processed")
            
    except Exception as e:
        print(f"❌ Error during update process: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
import asyncio
import json
import os
import sys
from decimal import Decimal
from typing import Any, Dict, List

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.database import async_session_factory, init_db  # noqa: E402
from app.models import Brand, Category, Product  # noqa: E402
from sqlalchemy import select  # noqa: E402


class LocalImagesDataImporter:
    def __init__(self, db_session):
        self.db = db_session

    async def import_comprehensive_data(self, json_file_path: str) -> None:
        """Import comprehensive product data with local images."""
        
        print(f"Importing data from {json_file_path}")
        
        # Read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products_data = data.get('comprehensive_product_dataset', [])
        
        print(f"Found {len(products_data)} products to import")
        
        # Get existing brands and categories
        brands_result = await self.db.execute(select(Brand))
        brands = {b.slug: b for b in brands_result.scalars().all()}
        
        categories_result = await self.db.execute(select(Category))
        categories = {c.slug: c for c in categories_result.scalars().all()}
        
        imported_count = 0
        skipped_count = 0
        
        for product_data in products_data:
            product_input = product_data.get('product_input', {})
            ai_content = product_data.get('ai_generated_content', {})
            
            sku = product_input.get('sku')
            brand_slug = product_input.get('brand', '').lower()
            category_slug = product_input.get('category', '').lower()
            
            # Check if product already exists
            existing_product = await self.db.execute(
                select(Product).where(Product.sku == sku)
            )
            if existing_product.scalar_one_or_none():
                print(f"Skipping existing product: {sku}")
                skipped_count += 1
                continue
            
            # Get brand and category
            brand = brands.get(brand_slug)
            category = categories.get(category_slug)
            
            if not brand:
                print(f"Warning: Brand '{brand_slug}' not found for product {sku}")
                continue
                
            if not category:
                print(f"Warning: Category '{category_slug}' not found for product {sku}")
                continue
            
            # Create product
            product = Product(
                sku=sku,
                name=product_input.get('name'),
                slug=product_input.get('slug'),
                brand_id=brand.id,
                category_id=category.id,
                description=product_input.get('description'),
                specifications=product_input.get('specifications', {}),
                images=product_input.get('images', []),
                msrp_price=Decimal(str(product_input.get('msrp_price', 0))),
                ai_generated_content=ai_content,
                is_active=True
            )
            
            self.db.add(product)
            imported_count += 1
            print(f"Added product: {sku}")
        
        await self.db.commit()
        print(f"\nImport completed!")
        print(f"Imported: {imported_count}")
        print(f"Skipped: {skipped_count}")


async def main():
    """Main function to import local images data."""
    
    # Initialize database
    await init_db()
    
    # Path to the updated JSON file
    json_file = os.path.join(
        os.path.dirname(os.path.dirname(CURRENT_DIR)),
        "comprehensive_products_with_ai_content_local_images.json"
    )
    
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found!")
        print("Please run the update_product_data_with_local_images.py script first.")
        return
    
    async with async_session_factory() as session:
        importer = LocalImagesDataImporter(session)
        await importer.import_comprehensive_data(json_file)
    
    print("✅ Local images data imported successfully!")


if __name__ == "__main__":
    asyncio.run(main())

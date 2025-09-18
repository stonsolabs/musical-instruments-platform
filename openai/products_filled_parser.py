#!/usr/bin/env python3
"""
Products Filled Parser
This parser processes products from products_filled table and inserts them into products table.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session, ProductsFilled, Product, Brand, Category

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductsFilledParser:
    def __init__(self):
        self.session: Optional[AsyncSession] = None

    async def parse_and_insert(self, ai_response: Dict[str, Any], custom_id: str) -> bool:
        """
        Parse AI response and insert into database using the new lightweight schema
        """
        try:
            self.session = await get_async_session()
            
            # Extract SKU from custom_id
            products_filled_sku = custom_id
            
            # Find the product in products_filled table
            result = await self.session.execute(
                text("SELECT sku, name, slug, description, msrp_price, url, created_at, updated_at FROM products_filled WHERE sku = :sku"),
                {"sku": products_filled_sku}
            )
            product_filled = result.fetchone()
            
            if not product_filled:
                logger.error(f"Product not found in products_filled with SKU: {products_filled_sku}")
                return False
            
            # Handle AI response structure - content might be wrapped in 'product' object
            product_data = ai_response.get('product', ai_response)
            
            # Extract data from AI response
            brand_name = product_data.get('brand')
            category_name = product_data.get('category')
            specifications = product_data.get('technical_specifications', {})
            store_links = product_data.get('store_links', {})
            images = product_data.get('images', {})
            warranty_info = product_data.get('warranty_info')
            related_products = product_data.get('related_products', [])
            # Content fields are now at root level (no localization)
            content_fields = {
                'basic_info': product_data.get('basic_info'),
                'usage_guidance': product_data.get('usage_guidance'),
                'customer_reviews': product_data.get('customer_reviews'),
                'maintenance_care': product_data.get('maintenance_care'),
                'purchase_decision': product_data.get('purchase_decision'),
                'technical_analysis': product_data.get('technical_analysis'),
                'professional_assessment': product_data.get('professional_assessment'),
                'notes': product_data.get('notes'),
                'suitable_genres': product_data.get('suitable_genres'),
            }
            content_metadata = product_data.get('metadata', {}) or product_data.get('content_metadata', {})
            qa = product_data.get('qa', {})
            dates = product_data.get('dates', {})
            sources = product_data.get('sources', [])
            
            # Extract product identifiers from AI response
            product_identifiers = product_data.get('product_identifiers', {})
            sku = product_identifiers.get('sku') or product_data.get('sku') or product_filled.sku
            gtin12 = product_identifiers.get('gtin12') or product_identifiers.get('upc')
            gtin13 = product_identifiers.get('gtin13') or product_identifiers.get('ean')
            gtin14 = product_identifiers.get('gtin14')
            upc = product_identifiers.get('upc')
            ean = product_identifiers.get('ean')
            mpn = product_identifiers.get('mpn')
            isbn = product_identifiers.get('isbn')
            
            # Validate required fields
            if not brand_name:
                logger.error("Brand name is required")
                return False
            
            if not category_name:
                logger.error("Category name is required")
                return False
            
            # Get or create brand
            brand = await self._get_or_create_brand(brand_name)
            
            # Get or create category
            category = await self._get_or_create_category(category_name)
            
            # Create product with simplified structure
            product_data = {
                'name': product_filled.name,
                'slug': product_filled.slug,
                'description': product_filled.description,
                'msrp_price': product_filled.msrp_price,
                'brand_id': brand.id,
                'category_id': category.id,
                'images': images,  # Separate JSONB column for images
                'content': {  # Single content JSONB column for everything else
                    'specifications': specifications,  # Now inside content
                    'warranty_info': warranty_info,
                    'related_products': related_products,
                    'content_metadata': content_metadata,
                    'qa': qa,
                    'dates': dates,
                    'sources': sources,
                    'store_links': store_links,  # Store links in content
                    **content_fields  # Add all content fields at root level
                },
                # Product identifiers
                'sku': sku,
                'gtin12': gtin12,
                'gtin13': gtin13,
                'gtin14': gtin14,
                'upc': upc,
                'ean': ean,
                'mpn': mpn,
                'isbn': isbn,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            # Insert product
            product = Product(**product_data)
            self.session.add(product)
            await self.session.flush()  # Get the ID
            
            # Store links, customer reviews, and product images are now stored in the content JSONB
            # No need for separate table inserts
            
            await self.session.commit()
            logger.info(f"Successfully inserted product: {product.name} (ID: {product.id}, SKU: {product.sku})")
            return True
            
        except Exception as e:
            logger.error(f"Error parsing and inserting product: {str(e)}")
            if self.session:
                await self.session.rollback()
            return False
        finally:
            if self.session:
                await self.session.close()

    async def _get_or_create_brand(self, brand_name: str) -> Brand:
        """Get or create brand"""
        if not brand_name:
            raise ValueError("Brand name is required")
        
        # Check if brand exists
        result = await self.session.execute(
            text("SELECT * FROM brands WHERE name = :name"),
            {"name": brand_name}
        )
        brand = result.fetchone()
        
        if brand:
            return Brand(id=brand.id, name=brand.name)
        
        # Create new brand
        slug = brand_name.lower().replace(' ', '-').replace('&', 'and').replace('.', '')
        result = await self.session.execute(
            text("INSERT INTO brands (name, slug, is_active, created_at) VALUES (:name, :slug, :is_active, :created_at) RETURNING id, name"),
            {"name": brand_name, "slug": slug, "is_active": True, "created_at": datetime.utcnow()}
        )
        new_brand = result.fetchone()
        await self.session.commit()
        
        return Brand(id=new_brand.id, name=new_brand.name)

    async def _get_or_create_category(self, category_name: str) -> Category:
        """Get or create category"""
        if not category_name:
            raise ValueError("Category name is required")
        
        # Check if category exists
        result = await self.session.execute(
            text("SELECT * FROM categories WHERE name = :name"),
            {"name": category_name}
        )
        category = result.fetchone()
        
        if category:
            return Category(id=category.id, name=category.name)
        
        # Create new category
        slug = category_name.lower().replace(' ', '-').replace('&', 'and').replace('.', '')
        result = await self.session.execute(
            text("INSERT INTO categories (name, slug, is_active, created_at) VALUES (:name, :slug, :is_active, :created_at) RETURNING id, name"),
            {"name": category_name, "slug": slug, "is_active": True, "created_at": datetime.utcnow()}
        )
        new_category = result.fetchone()
        await self.session.commit()
        
        return Category(id=new_category.id, name=new_category.name)

    # Removed helper methods for inserting into separate tables:
    # - _insert_store_links (replaced by content JSONB)
    # - _insert_customer_reviews (replaced by content JSONB)
    # - _insert_product_images (replaced by images JSONB)

# Test function
async def test_parser():
    """Test the parser with sample data"""
    parser = ProductsFilledParser()
    
    # Sample AI response (simplified)
    sample_response = {
        "brand": "Fender",
        "category": "Electric Guitars",
        "product_identifiers": {
            "sku": "FENDER-STRAT-001",
            "gtin12": "0887654321098",
            "gtin13": "08876543210987",
            "upc": "0887654321098",
            "ean": "08876543210987",
            "mpn": "014-4602-306"
        },
        "specifications": {
            "body_type": "Stratocaster",
            "body_material": "Alder",
            "neck_material": "Maple",
            "fretboard_material": "Rosewood",
            "scale_length": "25.5 inches",
            "number_of_frets": 21,
            "pickup_configuration": "SSS",
            "bridge_type": "Tremolo",
            "tuner_type": "Vintage-style",
            "controls": "1 Volume, 2 Tone",
            "finish": "Olympic White",
            "weight": "7.5 lbs"
        },
        "store_links": {
            "thomann": {"product_url": "https://www.thomann.de/fender_stratocaster.html"},
            "sweetwater": {"product_url": None}
        },
        "images": {
            "front_view": {
                "source": "Thomann",
                "page_url": "https://www.thomann.de/fender_stratocaster.html",
                "image_url": "https://images.thomann.de/pics/prod/123456.jpg",
                "alt_text": "Fender Stratocaster Front View"
            },
            "back_view": {
                "source": "Thomann",
                "page_url": "https://www.thomann.de/fender_stratocaster.html",
                "image_url": "https://images.thomann.de/pics/prod/123457.jpg",
                "alt_text": "Fender Stratocaster Back View"
            },
            "official_image": {
                "source": "Fender Official",
                "page_url": "https://www.fender.com/stratocaster",
                "image_url": "https://www.fender.com/images/stratocaster.jpg",
                "alt_text": "Fender Stratocaster Official"
            }
        },
        "customer_reviews": "Customer reviews summary: Great tone, excellent build quality, classic sound. Average rating 4.5/5 based on 1250 reviews.",
        "basic_info": "The Fender Stratocaster is a legendary electric guitar known for its versatile tone and comfortable playability.",
        "technical_analysis": "Features three single-coil pickups, 5-way selector switch, and classic tremolo bridge system.",
        "purchase_decision": "Ideal for players seeking versatility across multiple genres, from rock to blues to country."
    }
    
    success = await parser.parse_and_insert(sample_response, "test_sku_123")
    print(f"Parser test result: {success}")

if __name__ == "__main__":
    asyncio.run(test_parser())

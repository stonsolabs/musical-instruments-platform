# backend/app/services/ai_content.py
import openai
from typing import Dict, Any, List
import json
from ..config import settings
from ..models import Product

class AIContentGenerator:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_product_content(self, product: Product) -> Dict[str, Any]:
        """Generate comprehensive AI content for a product"""
        
        # Build context from product data
        context = self._build_product_context(product)
        
        # Generate different types of content
        summary = await self._generate_summary(context)
        pros_cons = await self._generate_pros_cons(context)
        use_cases = await self._generate_use_cases(context)
        seo_content = await self._generate_seo_content(context)
        
        return {
            "summary": summary,
            "pros": pros_cons["pros"],
            "cons": pros_cons["cons"],
            "best_for": use_cases["best_for"],
            "genres": use_cases["genres"],
            "skill_level": use_cases["skill_level"],
            "seo_description": seo_content["description"],
            "seo_keywords": seo_content["keywords"],
            "generated_at": "2025-08-11T00:00:00Z",
            "model_version": "gpt-4-turbo"
        }
    
    def _build_product_context(self, product: Product) -> str:
        """Build context string for AI prompts"""
        specs_str = ""
        if product.specifications:
            specs_str = "\n".join([f"- {k}: {v}" for k, v in product.specifications.items()])
        
        context = f"""
Product: {product.name}
Brand: {product.brand.name}
Category: {product.category.name}
Description: {product.description or 'No description available'}

Specifications:
{specs_str}

MSRP Price: €{product.msrp_price or 'N/A'}
"""
        return context
    
    async def _generate_summary(self, context: str) -> str:
        """Generate product summary"""
        prompt = f"""
As a musical instrument expert, write a concise 2-3 sentence summary for this product that highlights its key features and appeal.
Focus on what makes this instrument unique and who would benefit from it.

{context}

Summary:"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert in musical instruments with deep knowledge of guitars, keyboards, drums, and audio equipment."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    async def _generate_pros_cons(self, context: str) -> Dict[str, List[str]]:
        """Generate pros and cons"""
        prompt = f"""
As a musical instrument expert, analyze this product and provide 3-4 pros and 2-3 cons.
Be honest and balanced in your assessment.

{context}

Respond in JSON format:
{{"pros": ["pro1", "pro2", "pro3"], "cons": ["con1", "con2"]}}
"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert musical instrument reviewer. Provide honest, balanced assessments."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        try:
            result = json.loads(response.choices[0].message.content.strip())
            return result
        except json.JSONDecodeError:
            return {"pros": ["Quality construction", "Good value for money"], "cons": ["Limited color options"]}
    
    async def _generate_use_cases(self, context: str) -> Dict[str, Any]:
        """Generate use cases and recommendations"""
        prompt = f"""
Analyze this musical instrument and determine:
1. Who it's best for (3-4 specific use cases)
2. What music genres it suits (3-5 genres)
3. Skill level (Beginner/Intermediate/Advanced/Professional)

{context}

Respond in JSON format:
{{
    "best_for": ["use case 1", "use case 2", "use case 3"],
    "genres": ["genre1", "genre2", "genre3"],
    "skill_level": "Intermediate"
}}
"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert musical instrument consultant helping musicians choose the right instruments."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        try:
            result = json.loads(response.choices[0].message.content.strip())
            return result
        except json.JSONDecodeError:
            return {
                "best_for": ["General playing", "Recording", "Live performance"],
                "genres": ["Rock", "Pop", "Blues"],
                "skill_level": "Intermediate"
            }
    
    async def _generate_seo_content(self, context: str) -> Dict[str, Any]:
        """Generate SEO-optimized content"""
        prompt = f"""
Create SEO content for this musical instrument:
1. Meta description (150-160 characters, compelling)
2. 5-7 relevant keywords for search optimization

{context}

Respond in JSON format:
{{
    "description": "meta description here",
    "keywords": ["keyword1", "keyword2", "keyword3"]
}}
"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an SEO expert specializing in musical instrument e-commerce."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        try:
            result = json.loads(response.choices[0].message.content.strip())
            return result
        except json.JSONDecodeError:
            return {
                "description": f"High-quality musical instrument with excellent features and competitive pricing.",
                "keywords": ["musical instrument", "guitar", "keyboard", "best price"]
            }
    
    async def generate_comparison_content(self, products: List[Product]) -> Dict[str, Any]:
        """Generate AI content for product comparisons"""
        
        products_context = ""
        for i, product in enumerate(products, 1):
            specs_str = ""
            if product.specifications:
                specs_str = ", ".join([f"{k}: {v}" for k, v in product.specifications.items()])
            
            products_context += f"""
Product {i}: {product.name} by {product.brand.name}
- Category: {product.category.name}
- Specs: {specs_str}
- Price: €{product.msrp_price or 'N/A'}
"""
        
        prompt = f"""
As a musical instrument expert, create a comprehensive comparison of these products:

{products_context}

Provide:
1. A summary comparing the key differences
2. Recommendations for different user types
3. Which product wins in specific categories

Respond in JSON format:
{{
    "comparison_summary": "summary text",
    "recommendations": {{
        "beginners": "product recommendation and reason",
        "professionals": "product recommendation and reason",
        "budget_conscious": "product recommendation and reason"
    }},
    "category_winners": {{
        "build_quality": "winning product and reason",
        "value_for_money": "winning product and reason",
        "features": "winning product and reason"
    }}
}}
"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert musical instrument reviewer and consultant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        try:
            result = json.loads(response.choices[0].message.content.strip())
            return result
        except json.JSONDecodeError:
            return {
                "comparison_summary": "These instruments each offer unique advantages for different playing styles and budgets.",
                "recommendations": {
                    "beginners": "Consider the most affordable option with good build quality",
                    "professionals": "Focus on the model with best features and reliability",
                    "budget_conscious": "The best value for money option provides excellent performance per euro"
                },
                "category_winners": {
                    "build_quality": "All products show solid construction",
                    "value_for_money": "Multiple options provide good value",
                    "features": "Each instrument excels in different feature areas"
                }
            }

# backend/app/services/affiliate_manager.py
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
from bs4 import BeautifulSoup
import re
from ..config import settings
from ..models import Product, ProductPrice, AffiliateStore

class AffiliateManager:
    def __init__(self):
        self.session = httpx.AsyncClient(timeout=30.0)
        
    async def log_click(self, product_id: int, store_id: int, user_context: Dict[str, str]):
        """Log affiliate click for analytics"""
        # This would typically store in database and maybe trigger pixel tracking
        print(f"Affiliate click logged: Product {product_id}, Store {store_id}, Country {user_context.get('country')}")
        
    async def update_all_prices(self, db_session):
        """Update prices from all affiliate sources"""
        stores = await self._get_active_stores(db_session)
        
        for store in stores:
            try:
                if store.slug == "amazon":
                    await self._update_amazon_prices(store, db_session)
                elif store.slug == "thomann":
                    await self._update_thomann_prices(store, db_session)
                elif store.slug == "gear4music":
                    await self._update_gear4music_prices(store, db_session)
                
                # Wait between store updates to be respectful
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"Error updating prices for {store.name}: {e}")
    
    async def _get_active_stores(self, db_session) -> List[AffiliateStore]:
        """Get all active affiliate stores"""
        from sqlalchemy import select
        result = await db_session.execute(
            select(AffiliateStore).where(AffiliateStore.is_active == True)
        )
        return result.scalars().all()
    
    async def _update_amazon_prices(self, store: AffiliateStore, db_session):
        """Update prices from Amazon Associates"""
        # Note: Amazon doesn't provide direct API access for affiliate pricing
        # This would typically use Amazon PA-API or scraping (with caution)
        
        from sqlalchemy import select
        
        # Get products that need price updates
        result = await db_session.execute(
            select(Product).where(Product.is_active == True).limit(50)
        )
        products = result.scalars().all()
        
        for product in products:
            try:
                # Simulate Amazon price lookup
                amazon_url = f"https://amazon.es/s?k={product.name.replace(' ', '+')}"
                
                # In production, you would:
                # 1. Use Amazon PA-API for proper affiliate integration
                # 2. Or carefully scrape with proper delays and headers
                # 3. Handle CAPTCHA and IP blocking
                
                # For demo, simulate price data
                simulated_price = float(product.msrp_price or 500) * 0.9  # 10% discount
                affiliate_url = f"https://amazon.es/dp/ASIN123?tag={settings.AMAZON_ASSOCIATE_TAG}"
                
                await self._upsert_price(
                    db_session, product.id, store.id, 
                    simulated_price, "EUR", affiliate_url
                )
                
                await asyncio.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"Error updating Amazon price for {product.name}: {e}")
    
    async def _update_thomann_prices(self, store: AffiliateStore, db_session):
        """Update prices from Thomann affiliate program"""
        
        from sqlalchemy import select
        
        result = await db_session.execute(
            select(Product).where(Product.is_active == True).limit(50)
        )
        products = result.scalars().all()
        
        for product in products:
            try:
                # Thomann search URL
                search_query = product.name.replace(" ", "%20")
                search_url = f"https://www.thomann.de/gb/search_dir.html?sw={search_query}"
                
                # Make request with proper headers
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                }
                
                response = await self.session.get(search_url, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Parse Thomann product listings
                    price_element = soup.find('span', class_='price')
                    product_link = soup.find('a', href=True)
                    
                    if price_element and product_link:
                        price_text = price_element.get_text().strip()
                        price_match = re.search(r'€\s*(\d+[\.,]?\d*)', price_text)
                        
                        if price_match:
                            price = float(price_match.group(1).replace(',', '.'))
                            product_url = "https://www.thomann.de" + product_link['href']
                            
                            # Add affiliate tracking
                            affiliate_url = f"{product_url}?partner_id={settings.THOMANN_AFFILIATE_ID}"
                            
                            await self._upsert_price(
                                db_session, product.id, store.id,
                                price, "EUR", affiliate_url
                            )
                
                await asyncio.sleep(2)  # Rate limiting for scraping
                
            except Exception as e:
                print(f"Error updating Thomann price for {product.name}: {e}")
    
    async def _update_gear4music_prices(self, store: AffiliateStore, db_session):
        """Update prices from Gear4Music via Awin"""
        
        # Gear4Music typically provides product feeds through Awin
        # This would integrate with Awin API or process their product feeds
        
        from sqlalchemy import select
        
        result = await db_session.execute(
            select(Product).where(Product.is_active == True).limit(50)
        )
        products = result.scalars().all()
        
        for product in products:
            try:
                # Simulate Gear4Music pricing
                # In production, use Awin API or process CSV feeds
                
                simulated_price = float(product.msrp_price or 400) * 0.85
                affiliate_url = f"https://www.gear4music.com/search?q={product.name.replace(' ', '+')}&awinid=AWIN_ID"
                
                await self._upsert_price(
                    db_session, product.id, store.id,
                    simulated_price, "EUR", affiliate_url
                )
                
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"Error updating Gear4Music price for {product.name}: {e}")
    
    async def _upsert_price(self, db_session, product_id: int, store_id: int, 
                           price: float, currency: str, affiliate_url: str):
        """Insert or update product price"""
        
        from sqlalchemy import select
        
        # Check if price already exists
        result = await db_session.execute(
            select(ProductPrice).where(
                ProductPrice.product_id == product_id,
                ProductPrice.store_id == store_id
            )
        )
        existing_price = result.scalar_one_or_none()
        
        if existing_price:
            # Update existing price
            existing_price.price = price
            existing_price.currency = currency
            existing_price.affiliate_url = affiliate_url
            existing_price.last_checked = datetime.utcnow()
            existing_price.is_available = True
        else:
            # Create new price entry
            new_price = ProductPrice(
                product_id=product_id,
                store_id=store_id,
                price=price,
                currency=currency,
                affiliate_url=affiliate_url,
                is_available=True,
                last_checked=datetime.utcnow()
            )
            db_session.add(new_price)
        
        await db_session.commit()

# backend/app/services/data_importer.py
import csv
import json
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import Brand, Category, Product, AffiliateStore, ProductPrice

class DataImporter:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def import_sample_data(self):
        """Import sample data for development"""
        
        # Create sample brands
        await self._create_sample_brands()
        
        # Create sample categories
        await self._create_sample_categories()
        
        # Create sample affiliate stores
        await self._create_sample_stores()
        
        # Create sample products
        await self._create_sample_products()
        
        print("Sample data imported successfully!")
    
    async def _create_sample_brands(self):
        """Create sample musical instrument brands"""
        
        brands_data = [
            {"name": "Fender", "slug": "fender", "description": "Iconic American guitar manufacturer"},
            {"name": "Gibson", "slug": "gibson", "description": "Legendary guitar and instrument maker"},
            {"name": "Yamaha", "slug": "yamaha", "description": "Japanese musical instrument giant"},
            {"name": "Roland", "slug": "roland", "description": "Electronic music instrument pioneer"},
            {"name": "Marshall", "slug": "marshall", "description": "British amplifier manufacturer"},
            {"name": "Ibanez", "slug": "ibanez", "description": "Japanese guitar manufacturer"},
            {"name": "Casio", "slug": "casio", "description": "Consumer electronics and musical instruments"},
            {"name": "Korg", "slug": "korg", "description": "Electronic musical instrument manufacturer"},
        ]
        
        for brand_data in brands_data:
            # Check if brand already exists
            result = await self.db.execute(
                select(Brand).where(Brand.slug == brand_data["slug"])
            )
            if not result.scalar_one_or_none():
                brand = Brand(**brand_data)
                self.db.add(brand)
        
        await self.db.commit()
    
    async def _create_sample_categories(self):
        """Create sample product categories"""
        
        categories_data = [
            {"name": "Electric Guitars", "slug": "electric-guitars", "description": "Electric guitars and basses"},
            {"name": "Acoustic Guitars", "slug": "acoustic-guitars", "description": "Acoustic and classical guitars"},
            {"name": "Digital Keyboards", "slug": "digital-keyboards", "description": "Digital pianos and keyboards"},
            {"name": "Synthesizers", "slug": "synthesizers", "description": "Analog and digital synthesizers"},
            {"name": "Amplifiers", "slug": "amplifiers", "description": "Guitar and bass amplifiers"},
            {"name": "Audio Interfaces", "slug": "audio-interfaces", "description": "Recording interfaces and equipment"},
            {"name": "Microphones", "slug": "microphones", "description": "Studio and live microphones"},
            {"name": "Headphones", "slug": "headphones", "description": "Studio and consumer headphones"},
        ]
        
        for cat_data in categories_data:
            result = await self.db.execute(
                select(Category).where(Category.slug == cat_data["slug"])
            )
            if not result.scalar_one_or_none():
                category = Category(**cat_data)
                self.db.add(category)
        
        await self.db.commit()
    
    async def _create_sample_stores(self):
        """Create sample affiliate stores"""
        
        stores_data = [
            {
                "name": "Amazon",
                "slug": "amazon", 
                "website_url": "https://amazon.es",
                "commission_rate": 4.5
            },
            {
                "name": "Thomann",
                "slug": "thomann",
                "website_url": "https://thomann.de",
                "commission_rate": 3.0
            },
            {
                "name": "Gear4Music",
                "slug": "gear4music",
                "website_url": "https://gear4music.com",
                "commission_rate": 4.0
            },
            {
                "name": "Kytary",
                "slug": "kytary",
                "website_url": "https://kytary.de",
                "commission_rate": 2.5
            }
        ]
        
        for store_data in stores_data:
            result = await self.db.execute(
                select(AffiliateStore).where(AffiliateStore.slug == store_data["slug"])
            )
            if not result.scalar_one_or_none():
                store = AffiliateStore(**store_data)
                self.db.add(store)
        
        await self.db.commit()
    
    async def _create_sample_products(self):
        """Create sample products with specifications"""
        
        # Get brands and categories
        brands_result = await self.db.execute(select(Brand))
        brands = {b.slug: b for b in brands_result.scalars().all()}
        
        categories_result = await self.db.execute(select(Category))
        categories = {c.slug: c for c in categories_result.scalars().all()}
        
        stores_result = await self.db.execute(select(AffiliateStore))
        stores = stores_result.scalars().all()
        
        # Sample products data
        products_data = [
            {
                "sku": "FENDER-STRAT-MX-SSS",
                "name": "Fender Player Stratocaster MX",
                "brand": "fender",
                "category": "electric-guitars",
                "description": "The Player Stratocaster takes the best features of the original and adds modern improvements.",
                "msrp_price": 799.00,
                "specifications": {
                    "body_wood": "Alder",
                    "neck_wood": "Maple",
                    "fretboard": "Maple",
                    "pickups": "Player Series Alnico 5 Strat Single-Coil",
                    "bridge": "2-Point Synchronized Tremolo",
                    "scale_length": "25.5\"",
                    "frets": 22,
                    "string_count": 6
                },
                "images": [
                    "https://example.com/fender-strat-1.jpg",
                    "https://example.com/fender-strat-2.jpg"
                ]
            },
            {
                "sku": "YAMAHA-P45",
                "name": "Yamaha P-45 Digital Piano",
                "brand": "yamaha", 
                "category": "digital-keyboards",
                "description": "Compact digital piano with 88 weighted keys and authentic piano sound.",
                "msrp_price": 549.00,
                "specifications": {
                    "keys": 88,
                    "key_action": "Graded Hammer Standard (GHS)",
                    "voices": 10,
                    "polyphony": 64,
                    "connectivity": ["USB", "Sustain Pedal"],
                    "dimensions": "132.6 x 29.5 x 15.4 cm",
                    "weight": "11.5 kg"
                },
                "images": [
                    "https://example.com/yamaha-p45-1.jpg"
                ]
            },
            {
                "sku": "MARSHALL-DSL40CR",
                "name": "Marshall DSL40CR Guitar Amplifier",
                "brand": "marshall",
                "category": "amplifiers", 
                "description": "40-watt tube guitar amplifier with classic Marshall tone.",
                "msrp_price": 899.00,
                "specifications": {
                    "power": "40W",
                    "tubes": "ECC83, EL34",
                    "channels": 2,
                    "speaker": "12\" Celestion V-Type",
                    "effects": "Reverb",
                    "dimensions": "63 x 50 x 26 cm",
                    "weight": "22 kg"
                },
                "images": [
                    "https://example.com/marshall-dsl40cr-1.jpg"
                ]
            }
        ]
        
        for product_data in products_data:
            # Check if product exists
            result = await self.db.execute(
                select(Product).where(Product.sku == product_data["sku"])
            )
            if result.scalar_one_or_none():
                continue
            
            # Create product
            product = Product(
                sku=product_data["sku"],
                name=product_data["name"],
                slug=product_data["name"].lower().replace(" ", "-").replace("'", ""),
                brand_id=brands[product_data["brand"]].id,
                category_id=categories[product_data["category"]].id,
                description=product_data["description"],
                specifications=product_data["specifications"],
                images=product_data["images"],
                msrp_price=product_data["msrp_price"]
            )
            
            self.db.add(product)
            await self.db.flush()  # Get product ID
            
            # Add sample prices from different stores
            for i, store in enumerate(stores[:3]):  # First 3 stores
                price_variation = 0.9 + (i * 0.05)  # Vary prices slightly
                price = float(product_data["msrp_price"]) * price_variation
                
                product_price = ProductPrice(
                    product_id=product.id,
                    store_id=store.id,
                    price=price,
                    currency="EUR",
                    affiliate_url=f"https://{store.slug}.com/product/{product.sku}?aff=123",
                    is_available=True
                )
                self.db.add(product_price)
        
        await self.db.commit()

# Usage script for data import
# backend/scripts/import_sample_data.py
import asyncio
import sys
sys.path.append('..')

from app.database import async_session_factory, init_db
from app.services.data_importer import DataImporter

async def main():
    # Initialize database
    await init_db()
    
    # Import sample data
    async with async_session_factory() as session:
        importer = DataImporter(session)
        await importer.import_sample_data()
    
    print("✅ Sample data imported successfully!")

if __name__ == "__main__":
    asyncio.run(main())
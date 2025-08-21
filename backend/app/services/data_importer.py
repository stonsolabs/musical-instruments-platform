from __future__ import annotations

from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import AffiliateStore, Brand, Category, Product, ProductPrice


class DataImporter:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def import_sample_data(self) -> None:
        await self._create_sample_brands()
        await self._create_sample_categories()
        await self._create_sample_stores()
        await self._create_sample_products()
        print("Sample data imported successfully!")

    async def _create_sample_brands(self) -> None:
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
            result = await self.db.execute(select(Brand).where(Brand.slug == brand_data["slug"]))
            if not result.scalar_one_or_none():
                self.db.add(Brand(**brand_data))
        await self.db.commit()

    async def _create_sample_categories(self) -> None:
        categories_data = [
            {"name": "Electric Guitars", "slug": "electric-guitars", "description": "Electric guitars for all styles and genres"},
            {"name": "Acoustic Guitars", "slug": "acoustic-guitars", "description": "Acoustic and classical guitars"},
            {"name": "Bass Guitars", "slug": "bass-guitars", "description": "Electric and acoustic bass guitars"},
            {"name": "Drums & Percussion", "slug": "drums-percussion", "description": "Drum kits, percussion instruments and accessories"},
            {"name": "Pianos & Keyboards", "slug": "pianos-keyboards", "description": "Digital pianos, keyboards and synthesizers"},
            {"name": "Orchestral", "slug": "orchestral", "description": "String, brass, woodwind and orchestral instruments"},
            {"name": "Live Sound & Lighting", "slug": "live-sound-lighting", "description": "PA systems, mixers, and stage lighting equipment"},
            {"name": "Studio & Production", "slug": "studio-production", "description": "Recording interfaces, monitors and studio equipment"},
            {"name": "Music Software", "slug": "music-software", "description": "DAWs, plugins and music production software"},
            {"name": "DJ Equipment", "slug": "dj-equipment", "description": "DJ controllers, turntables and mixing equipment"},
            {"name": "Home Audio", "slug": "home-audio", "description": "Home stereo systems, speakers and audio equipment"},
        ]
        for cat_data in categories_data:
            result = await self.db.execute(select(Category).where(Category.slug == cat_data["slug"]))
            if not result.scalar_one_or_none():
                self.db.add(Category(**cat_data))
        await self.db.commit()

    async def _create_sample_stores(self) -> None:
        stores_data = [
            {"name": "Amazon", "slug": "amazon", "website_url": "https://amazon.es", "commission_rate": 4.5},
            {"name": "Thomann", "slug": "thomann", "website_url": "https://thomann.de", "commission_rate": 3.0},
            {"name": "Gear4Music", "slug": "gear4music", "website_url": "https://gear4music.com", "commission_rate": 4.0},
            {"name": "Kytary", "slug": "kytary", "website_url": "https://kytary.de", "commission_rate": 2.5},
        ]
        for store_data in stores_data:
            result = await self.db.execute(select(AffiliateStore).where(AffiliateStore.slug == store_data["slug"]))
            if not result.scalar_one_or_none():
                self.db.add(AffiliateStore(**store_data))
        await self.db.commit()

    async def _create_sample_products(self) -> None:
        brands_result = await self.db.execute(select(Brand))
        brands = {b.slug: b for b in brands_result.scalars().all()}
        categories_result = await self.db.execute(select(Category))
        categories = {c.slug: c for c in categories_result.scalars().all()}
        stores_result = await self.db.execute(select(AffiliateStore))
        stores = stores_result.scalars().all()

        products_data: List[Dict[str, Any]] = [
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
                    "string_count": 6,
                },
                "images": [
                    "https://example.com/fender-strat-1.jpg",
                    "https://example.com/fender-strat-2.jpg",
                ],
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
                    "weight": "11.5 kg",
                },
                "images": ["https://example.com/yamaha-p45-1.jpg"],
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
                    "speaker": '12" Celestion V-Type',
                    "effects": "Reverb",
                    "dimensions": "63 x 50 x 26 cm",
                    "weight": "22 kg",
                },
                "images": ["https://example.com/marshall-dsl40cr-1.jpg"],
            },
        ]

        for pdata in products_data:
            result = await self.db.execute(select(Product).where(Product.sku == pdata["sku"]))
            if result.scalar_one_or_none():
                continue
            product = Product(
                sku=pdata["sku"],
                name=pdata["name"],
                slug=pdata["name"].lower().replace(" ", "-").replace("'", ""),
                brand_id=brands[pdata["brand"]].id,
                category_id=categories[pdata["category"]].id,
                description=pdata["description"],
                specifications=pdata["specifications"],
                images=pdata["images"],
                msrp_price=pdata["msrp_price"],
            )
            self.db.add(product)
            await self.db.flush()

            for i, store in enumerate(stores[:3]):
                price_variation = 0.9 + (i * 0.05)
                price = float(pdata["msrp_price"]) * price_variation
                self.db.add(
                    ProductPrice(
                        product_id=product.id,
                        store_id=store.id,
                        price=price,
                        currency="EUR",
                        affiliate_url=f"https://{store.slug}.com/product/{product.sku}?aff=123",
                        is_available=True,
                    )
                )
        await self.db.commit()



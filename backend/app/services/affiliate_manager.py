from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Dict, List

import httpx
from bs4 import BeautifulSoup
import re
from sqlalchemy import select

from ..config import settings
from ..models import AffiliateStore, Product, ProductPrice


class AffiliateManager:
    def __init__(self) -> None:
        self.session = httpx.AsyncClient(timeout=30.0)

    async def log_click(self, product_id: int, store_id: int, user_context: Dict[str, str]):
        # Placeholder: integrate with DB/events if needed
        print(
            f"Affiliate click logged: Product {product_id}, Store {store_id}, Country {user_context.get('country')}"
        )

    async def update_all_prices(self, db_session):
        stores = await self._get_active_stores(db_session)
        for store in stores:
            try:
                if store.slug == "amazon":
                    await self._update_amazon_prices(store, db_session)
                elif store.slug == "thomann":
                    await self._update_thomann_prices(store, db_session)
                elif store.slug == "gear4music":
                    await self._update_gear4music_prices(store, db_session)
                await asyncio.sleep(2)
            except Exception as e:  # noqa: BLE001
                print(f"Error updating prices for {store.name}: {e}")

    async def _get_active_stores(self, db_session) -> List[AffiliateStore]:
        result = await db_session.execute(select(AffiliateStore).where(AffiliateStore.is_active.is_(True)))
        return result.scalars().all()

    async def _update_amazon_prices(self, store: AffiliateStore, db_session):
        result = await db_session.execute(select(Product).where(Product.is_active.is_(True)).limit(50))
        products = result.scalars().all()
        for product in products:
            try:
                simulated_price = float(product.msrp_price or 500) * 0.9
                affiliate_url = f"https://amazon.es/dp/ASIN123?tag={settings.AMAZON_ASSOCIATE_TAG}"
                await self._upsert_price(db_session, product.id, store.id, simulated_price, "EUR", affiliate_url)
                await asyncio.sleep(1)
            except Exception as e:  # noqa: BLE001
                print(f"Error updating Amazon price for {product.name}: {e}")

    async def _update_thomann_prices(self, store: AffiliateStore, db_session):
        result = await db_session.execute(select(Product).where(Product.is_active.is_(True)).limit(50))
        products = result.scalars().all()
        for product in products:
            try:
                search_query = product.name.replace(" ", "%20")
                search_url = f"https://www.thomann.de/intl/search_dir.html?sw={search_query}"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                }
                response = await self.session.get(search_url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    price_element = soup.find("span", class_="price")
                    product_link = soup.find("a", href=True)
                    if price_element and product_link:
                        price_text = price_element.get_text().strip()
                        price_match = re.search(r"€\s*(\d+[\.,]?\d*)", price_text)
                        if price_match:
                            price = float(price_match.group(1).replace(",", "."))
                            # Ensure we use /intl/ path for better international compatibility
                            product_href = product_link["href"]
                            if not product_href.startswith('/intl/'):
                                # Convert regional paths to /intl/ for better international compatibility
                                if product_href.startswith('/gb/'):
                                    product_href = product_href.replace('/gb/', '/intl/', 1)
                                elif product_href.startswith('/de/'):
                                    product_href = product_href.replace('/de/', '/intl/', 1)
                                elif product_href.startswith('/fr/'):
                                    product_href = product_href.replace('/fr/', '/intl/', 1)
                                elif not product_href.startswith('/intl/'):
                                    # For other paths, ensure they use /intl/
                                    product_href = '/intl' + product_href
                            
                            # Always use thomann.de domain for consistent affiliate tracking
                            product_url = "https://www.thomann.de" + product_href
                            # Use enhanced affiliate service for proper URL generation
                            from .enhanced_affiliate_service import EnhancedAffiliateService
                            enhanced_service = EnhancedAffiliateService(db_session)
                            
                            # Get the Thomann store configuration
                            thomann_store_query = select(AffiliateStore).where(AffiliateStore.slug == "thomann")
                            thomann_result = await db_session.execute(thomann_store_query)
                            thomann_store = thomann_result.scalar_one_or_none()
                            
                            if thomann_store:
                                affiliate_url = enhanced_service._add_affiliate_parameters(thomann_store, product_url)
                            else:
                                # Fallback to old method if store not found
                                affiliate_url = f"{product_url}?offid=1&affid={settings.THOMANN_AFFILIATE_ID}"
                            await self._upsert_price(db_session, product.id, store.id, price, "EUR", affiliate_url)
                await asyncio.sleep(2)
            except Exception as e:  # noqa: BLE001
                print(f"Error updating Thomann price for {product.name}: {e}")

    async def _update_gear4music_prices(self, store: AffiliateStore, db_session):
        result = await db_session.execute(select(Product).where(Product.is_active.is_(True)).limit(50))
        products = result.scalars().all()
        for product in products:
            try:
                simulated_price = float(product.msrp_price or 400) * 0.85
                affiliate_url = f"https://www.gear4music.com/search?q={product.name.replace(' ', '+')}&awinid=AWIN_ID"
                await self._upsert_price(db_session, product.id, store.id, simulated_price, "EUR", affiliate_url)
                await asyncio.sleep(1)
            except Exception as e:  # noqa: BLE001
                print(f"Error updating Gear4Music price for {product.name}: {e}")

    async def _upsert_price(self, db_session, product_id: int, store_id: int, price: float, currency: str, affiliate_url: str):
        result = await db_session.execute(
            select(ProductPrice).where(
                ProductPrice.product_id == product_id,
                ProductPrice.store_id == store_id,
            )
        )
        existing_price = result.scalar_one_or_none()
        if existing_price:
            existing_price.price = price
            existing_price.currency = currency
            existing_price.affiliate_url = affiliate_url
            existing_price.last_checked = datetime.utcnow()
            existing_price.is_available = True
        else:
            db_session.add(
                ProductPrice(
                    product_id=product_id,
                    store_id=store_id,
                    price=price,
                    currency=currency,
                    affiliate_url=affiliate_url,
                    is_available=True,
                    last_checked=datetime.utcnow(),
                )
            )
        await db_session.commit()



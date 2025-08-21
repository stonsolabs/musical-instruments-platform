from __future__ import annotations

import json
import hashlib
from typing import List, Dict, Any, Optional
from decimal import Decimal

import redis.asyncio as redis
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..models import Product, Brand, Category, ProductPrice, AffiliateStore
from ..config import settings


class SearchService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.cache_ttl = 300  # 5 minutes

    async def search_products(
        self,
        query: str,
        limit: int = 8,
        db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """
        Search products using PostgreSQL full-text search with Redis caching
        """
        if len(query.strip()) < 2:
            return []

        # Create cache key
        cache_key = f"search:{hashlib.md5(query.lower().encode()).hexdigest()}:{limit}"
        
        # Try to get from cache first
        cached_result = await self.redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        # Perform full-text search
        search_results = await self._perform_full_text_search(query, limit, db)
        
        # Cache the results
        await self.redis_client.setex(
            cache_key, 
            self.cache_ttl, 
            json.dumps(search_results)
        )
        
        return search_results

    async def _perform_full_text_search(
        self,
        query: str,
        limit: int,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """
        Perform PostgreSQL full-text search with ranking
        """
        # Create search vector and query
        search_vector = func.to_tsvector('english', 
            func.concat(
                func.coalesce(Product.name, ''), ' ',
                func.coalesce(Product.description, ''), ' ',
                func.coalesce(Brand.name, ''), ' ',
                func.coalesce(Category.name, '')
            )
        )
        
        search_query = func.plainto_tsquery('english', query)
        
        # Build the search query with ranking
        stmt = (
            select(
                Product,
                Brand,
                Category,
                func.ts_rank(search_vector, search_query).label('rank')
            )
            .join(Product.brand)
            .join(Product.category)
            .where(
                Product.is_active.is_(True),
                search_vector.op('@@')(search_query)
            )
            .order_by(
                func.ts_rank(search_vector, search_query).desc(),
                Product.avg_rating.desc().nullslast(),
                Product.review_count.desc().nullslast()
            )
            .limit(limit)
        )

        result = await db.execute(stmt)
        rows = result.all()

        # Get product IDs for price lookup
        product_ids = [row[0].id for row in rows]

        # Get best prices and all prices for these products
        best_prices = await self._get_best_prices(product_ids, db)
        all_prices = await self._get_all_prices(product_ids, db)

        # Build response
        search_results = []
        for product, brand, category, rank in rows:
            best_price = best_prices.get(product.id)
            product_prices = all_prices.get(product.id, [])
            
            search_results.append({
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "brand": {
                    "id": brand.id,
                    "name": brand.name,
                    "slug": brand.slug
                },
                "category": {
                    "id": category.id,
                    "name": category.name,
                    "slug": category.slug
                },
                "avg_rating": float(product.avg_rating) if product.avg_rating else 0.0,
                "review_count": product.review_count,
                "images": product.images or [],
                "best_price": best_price,
                "prices": product_prices,
                "rank": float(rank),
                "search_highlight": self._highlight_search_terms(product.name, query)
            })

        return search_results

    async def _get_best_prices(
        self,
        product_ids: List[int],
        db: AsyncSession
    ) -> Dict[int, Optional[Dict[str, Any]]]:
        """
        Get best prices for a list of products
        """
        if not product_ids:
            return {}

        # Get best price per product
        best_price_subq = (
            select(
                ProductPrice.product_id,
                func.min(ProductPrice.price).label("best_price")
            )
            .where(
                ProductPrice.product_id.in_(product_ids),
                ProductPrice.is_available.is_(True)
            )
            .group_by(ProductPrice.product_id)
            .subquery()
        )

        # Join with store information
        stmt = (
            select(ProductPrice, AffiliateStore)
            .join(best_price_subq, 
                  (best_price_subq.c.product_id == ProductPrice.product_id) & 
                  (best_price_subq.c.best_price == ProductPrice.price))
            .join(AffiliateStore, AffiliateStore.id == ProductPrice.store_id)
        )

        result = await db.execute(stmt)
        rows = result.all()

        best_prices = {}
        for price, store in rows:
            best_prices[price.product_id] = {
                "price": float(price.price),
                "currency": price.currency,
                "store": {
                    "id": store.id,
                    "name": store.name,
                    "slug": store.slug
                },
                "affiliate_url": price.affiliate_url
            }

        return best_prices

    async def _get_all_prices(
        self,
        product_ids: List[int],
        db: AsyncSession
    ) -> Dict[int, List[Dict[str, Any]]]:
        """
        Get all prices for a list of products
        """
        if not product_ids:
            return {}

        # Get all prices with store information
        stmt = (
            select(ProductPrice, AffiliateStore)
            .join(AffiliateStore, AffiliateStore.id == ProductPrice.store_id)
            .where(ProductPrice.product_id.in_(product_ids))
            .order_by(ProductPrice.product_id, ProductPrice.price)
        )

        result = await db.execute(stmt)
        rows = result.all()

        all_prices = {}
        for price, store in rows:
            if price.product_id not in all_prices:
                all_prices[price.product_id] = []
            
            all_prices[price.product_id].append({
                "id": price.id,
                "price": float(price.price),
                "currency": price.currency,
                "store": {
                    "id": store.id,
                    "name": store.name,
                    "slug": store.slug
                },
                "affiliate_url": price.affiliate_url,
                "is_available": price.is_available,
                "last_checked": price.last_checked.isoformat() if price.last_checked else None
            })

        return all_prices

    def _highlight_search_terms(self, text: str, query: str) -> str:
        """
        Simple highlighting of search terms in text
        """
        query_terms = query.lower().split()
        highlighted_text = text
        
        for term in query_terms:
            if len(term) >= 2:  # Only highlight terms with 2+ characters
                # Simple case-insensitive replacement
                import re
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                highlighted_text = pattern.sub(f'<mark>{term}</mark>', highlighted_text)
        
        return highlighted_text

    async def get_search_suggestions(
        self,
        query: str,
        limit: int = 5,
        db: AsyncSession = None
    ) -> List[str]:
        """
        Get search suggestions based on popular searches
        """
        if len(query.strip()) < 2:
            return []

        cache_key = f"suggestions:{hashlib.md5(query.lower().encode()).hexdigest()}"
        
        # Try cache first
        cached_suggestions = await self.redis_client.get(cache_key)
        if cached_suggestions:
            return json.loads(cached_suggestions)

        # Get suggestions from database
        stmt = (
            select(Product.name)
            .where(
                Product.is_active.is_(True),
                func.lower(Product.name).like(f"%{query.lower()}%")
            )
            .order_by(Product.avg_rating.desc().nullslast())
            .limit(limit)
        )

        result = await db.execute(stmt)
        suggestions = [row[0] for row in result.scalars().all()]

        # Cache suggestions
        await self.redis_client.setex(
            cache_key,
            self.cache_ttl,
            json.dumps(suggestions)
        )

        return suggestions

    async def clear_search_cache(self) -> None:
        """
        Clear all search-related cache
        """
        # Get all search-related keys
        search_keys = await self.redis_client.keys("search:*")
        suggestion_keys = await self.redis_client.keys("suggestions:*")
        
        if search_keys or suggestion_keys:
            await self.redis_client.delete(*(search_keys + suggestion_keys))

    async def close(self):
        """
        Close Redis connection
        """
        await self.redis_client.close()


# Global search service instance
search_service = SearchService()

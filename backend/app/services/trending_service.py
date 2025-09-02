from __future__ import annotations

import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict

import redis.asyncio as redis
from sqlalchemy import select, func, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import Product, Brand, Category, AffiliateStore
from ..config import settings


class TrendingService:
    """Service for managing trending products and popular comparisons using Redis"""
    
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        
        # Cache TTLs
        self.trending_cache_ttl = 3600  # 1 hour
        self.comparison_cache_ttl = 1800  # 30 minutes
        self.analytics_ttl = 86400  # 24 hours
        
        # Redis key patterns
        self.trending_key = "trending:instruments"
        self.comparison_key = "popular:comparisons"
        self.view_count_key = "views:product"
        self.comparison_count_key = "comparisons:pair"
        self.category_trending_key = "trending:category"
    
    def _extract_image_urls(self, images_dict: Dict[str, Any]) -> List[str]:
        """
        Extract image URLs from the images JSON object.
        Expected format: {"thomann_main": {"url": "...", ...}, ...}
        Returns: ["url1", "url2", ...]
        """
        if not images_dict or not isinstance(images_dict, dict):
            return []
        
        urls = []
        for key, image_data in images_dict.items():
            if isinstance(image_data, dict) and "url" in image_data:
                urls.append(image_data["url"])
            elif isinstance(image_data, str):
                # Fallback for simple string URLs
                urls.append(image_data)
        
        return urls

    async def track_product_view(self, product_id: int, user_ip: str = None) -> None:
        """Track a product view for trending calculations"""
        try:
            # Get current hour for time-based trending
            current_hour = datetime.now().strftime("%Y%m%d%H")
            
            # Increment product view count (overall and hourly)
            await self.redis_client.zincrby(f"{self.view_count_key}:total", 1, product_id)
            await self.redis_client.zincrby(f"{self.view_count_key}:hour:{current_hour}", 1, product_id)
            
            # Set expiry for hourly data (keep for 7 days)
            await self.redis_client.expire(f"{self.view_count_key}:hour:{current_hour}", 604800)
            
            # Track unique views by IP (if provided)
            if user_ip:
                unique_key = f"unique_views:{product_id}:{current_hour}"
                await self.redis_client.sadd(unique_key, user_ip)
                await self.redis_client.expire(unique_key, 86400)  # 24 hours
                
        except Exception as e:
            # Don't fail the main request if analytics fail
            print(f"Error tracking product view: {e}")

    async def track_product_comparison(self, product_id_1: int, product_id_2: int) -> None:
        """Track when two products are compared together"""
        try:
            # Create a consistent comparison pair key (smaller ID first)
            pair_key = f"{min(product_id_1, product_id_2)}:{max(product_id_1, product_id_2)}"
            
            # Increment comparison count
            await self.redis_client.zincrby(self.comparison_count_key, 1, pair_key)
            
            # Track individual products in comparisons
            await self.redis_client.zincrby("comparisons:individual", 1, product_id_1)
            await self.redis_client.zincrby("comparisons:individual", 1, product_id_2)
            
        except Exception as e:
            print(f"Error tracking comparison: {e}")

    async def get_trending_instruments(
        self, 
        limit: int = 10, 
        category_id: Optional[int] = None,
        db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """Get trending instruments based on views and comparisons"""
        
        # Try cache first
        cache_key = f"{self.trending_key}:{category_id or 'all'}:{limit}"
        cached_result = await self.redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        # Get trending product IDs from Redis analytics
        trending_ids = await self._calculate_trending_products(limit * 2, category_id)
        
        if not trending_ids or not db:
            return []

        # Fetch product details from database
        query = (
            select(Product)
            .options(
                selectinload(Product.brand),
                selectinload(Product.category)
            )
            .where(
                Product.id.in_(trending_ids),
                Product.is_active.is_(True)
            )
        )
        
        if category_id:
            query = query.where(Product.category_id == category_id)
            
        result = await db.execute(query)
        products = result.scalars().all()
        
        # Create product lookup and preserve trending order
        product_dict = {p.id: p for p in products}
        trending_products = []
        
        for product_id in trending_ids:
            if product_id in product_dict:
                product = product_dict[product_id]
                
                # Get trending score
                trending_score = await self._get_product_trending_score(product_id)
                
                trending_products.append({
                    "id": product.id,
                    "name": product.name,
                    "slug": product.slug,
                    "brand": {
                        "id": product.brand.id,
                        "name": product.brand.name,
                        "slug": product.brand.slug
                    },
                    "category": {
                        "id": product.category.id,
                        "name": product.category.name,
                        "slug": product.category.slug
                    },
                    "images": self._extract_image_urls(product.images) if product.images else [],
                    "msrp_price": float(product.msrp_price) if product.msrp_price else None,
                    "trending_score": trending_score,
                    "view_count_24h": await self._get_product_views_24h(product_id)
                })
                
                if len(trending_products) >= limit:
                    break
        
        # Cache the result
        await self.redis_client.setex(
            cache_key,
            self.trending_cache_ttl,
            json.dumps(trending_products)
        )
        
        return trending_products

    async def get_popular_comparisons(
        self, 
        limit: int = 10,
        db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """Get most popular product comparisons"""
        
        # Try cache first
        cache_key = f"{self.comparison_key}:{limit}"
        cached_result = await self.redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        # Get top comparison pairs from Redis
        comparison_pairs = await self.redis_client.zrevrange(
            self.comparison_count_key, 0, limit - 1, withscores=True
        )
        
        if not comparison_pairs or not db:
            return []

        # Extract product IDs from pairs
        all_product_ids = set()
        for pair_key, score in comparison_pairs:
            id1, id2 = map(int, pair_key.split(':'))
            all_product_ids.update([id1, id2])
        
        # Fetch all products at once
        query = (
            select(Product)
            .options(
                selectinload(Product.brand),
                selectinload(Product.category)
            )
            .where(
                Product.id.in_(list(all_product_ids)),
                Product.is_active.is_(True)
            )
        )
        
        result = await db.execute(query)
        products = {p.id: p for p in result.scalars().all()}
        
        # Build comparison results
        popular_comparisons = []
        for pair_key, comparison_count in comparison_pairs:
            id1, id2 = map(int, pair_key.split(':'))
            
            if id1 in products and id2 in products:
                product1 = products[id1]
                product2 = products[id2]
                
                popular_comparisons.append({
                    "comparison_count": int(comparison_count),
                    "products": [
                        {
                            "id": product1.id,
                            "name": product1.name,
                            "slug": product1.slug,
                            "brand": {"name": product1.brand.name, "slug": product1.brand.slug},
                            "category": {"name": product1.category.name, "slug": product1.category.slug},
                            "images": self._extract_image_urls(product1.images) if product1.images else [],
                            "msrp_price": float(product1.msrp_price) if product1.msrp_price else None
                        },
                        {
                            "id": product2.id,
                            "name": product2.name,
                            "slug": product2.slug,
                            "brand": {"name": product2.brand.name, "slug": product2.brand.slug},
                            "category": {"name": product2.category.name, "slug": product2.category.slug},
                            "images": self._extract_image_urls(product2.images) if product2.images else [],
                            "msrp_price": float(product2.msrp_price) if product2.msrp_price else None
                        }
                    ],
                    "comparison_url": f"/compare?products={product1.slug},{product2.slug}"
                })
        
        # Cache the result
        await self.redis_client.setex(
            cache_key,
            self.comparison_cache_ttl,
            json.dumps(popular_comparisons)
        )
        
        return popular_comparisons

    async def get_category_trending(self, db: AsyncSession = None) -> Dict[str, List[Dict]]:
        """Get trending products by category"""
        
        cache_key = "trending:by_category"
        cached_result = await self.redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        if not db:
            return {}

        # Get all categories
        categories_query = select(Category).where(Category.id.isnot(None))
        categories_result = await db.execute(categories_query)
        categories = categories_result.scalars().all()
        
        # Get trending for each category
        category_trending = {}
        for category in categories:
            trending = await self.get_trending_instruments(
                limit=5, 
                category_id=category.id, 
                db=db
            )
            if trending:
                category_trending[category.slug] = {
                    "category_name": category.name,
                    "trending_products": trending
                }
        
        # Cache for 2 hours
        await self.redis_client.setex(
            cache_key,
            7200,
            json.dumps(category_trending)
        )
        
        return category_trending

    async def _calculate_trending_products(
        self, 
        limit: int, 
        category_id: Optional[int] = None
    ) -> List[int]:
        """Calculate trending products using weighted scoring"""
        
        # Get recent views (last 24 hours)
        current_time = datetime.now()
        product_scores = defaultdict(float)
        
        # Weight recent hours more heavily
        for hours_ago in range(24):
            hour_key = (current_time - timedelta(hours=hours_ago)).strftime("%Y%m%d%H")
            weight = max(1.0 - (hours_ago * 0.02), 0.1)  # Decay factor
            
            try:
                hourly_views = await self.redis_client.zrevrange(
                    f"{self.view_count_key}:hour:{hour_key}", 
                    0, -1, 
                    withscores=True
                )
                
                for product_id_str, views in hourly_views:
                    product_id = int(product_id_str)
                    product_scores[product_id] += views * weight
                    
            except Exception:
                continue
        
        # Add comparison bonus (products frequently compared are trending)
        try:
            comparison_scores = await self.redis_client.zrevrange(
                "comparisons:individual", 0, -1, withscores=True
            )
            
            for product_id_str, comparisons in comparison_scores:
                product_id = int(product_id_str)
                # Comparisons are worth 3x a view
                product_scores[product_id] += comparisons * 3
                
        except Exception:
            pass
        
        # Sort by score and return top product IDs
        sorted_products = sorted(
            product_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [product_id for product_id, score in sorted_products[:limit]]

    async def _get_product_trending_score(self, product_id: int) -> float:
        """Get trending score for a specific product"""
        try:
            # Recent views score
            views_score = 0
            current_time = datetime.now()
            
            for hours_ago in range(24):
                hour_key = (current_time - timedelta(hours=hours_ago)).strftime("%Y%m%d%H")
                weight = max(1.0 - (hours_ago * 0.02), 0.1)
                
                views = await self.redis_client.zscore(
                    f"{self.view_count_key}:hour:{hour_key}", product_id
                ) or 0
                views_score += views * weight
            
            # Comparison bonus
            comparison_score = await self.redis_client.zscore(
                "comparisons:individual", product_id
            ) or 0
            
            return views_score + (comparison_score * 3)
            
        except Exception:
            return 0.0

    async def _get_product_views_24h(self, product_id: int) -> int:
        """Get total views for product in last 24 hours"""
        try:
            total_views = 0
            current_time = datetime.now()
            
            for hours_ago in range(24):
                hour_key = (current_time - timedelta(hours=hours_ago)).strftime("%Y%m%d%H")
                views = await self.redis_client.zscore(
                    f"{self.view_count_key}:hour:{hour_key}", product_id
                ) or 0
                total_views += int(views)
            
            return total_views
            
        except Exception:
            return 0

    async def clear_trending_cache(self) -> None:
        """Clear all trending and comparison caches"""
        try:
            # Get all cache keys
            trending_keys = await self.redis_client.keys("trending:*")
            comparison_keys = await self.redis_client.keys("popular:*")
            
            if trending_keys or comparison_keys:
                await self.redis_client.delete(*(trending_keys + comparison_keys))
                
        except Exception as e:
            print(f"Error clearing trending cache: {e}")

    async def get_analytics_summary(self) -> Dict[str, Any]:
        """Get analytics summary for admin dashboard"""
        try:
            # Total views today
            today = datetime.now().strftime("%Y%m%d")
            total_views_today = 0
            
            for hour in range(24):
                hour_key = f"{today}{hour:02d}"
                hour_views = await self.redis_client.zcard(f"{self.view_count_key}:hour:{hour_key}")
                total_views_today += hour_views
            
            # Total comparisons
            total_comparisons = await self.redis_client.zcard(self.comparison_count_key)
            
            # Most viewed product today
            current_hour = datetime.now().strftime("%Y%m%d%H")
            top_product_today = await self.redis_client.zrevrange(
                f"{self.view_count_key}:hour:{current_hour}", 0, 0, withscores=True
            )
            
            return {
                "total_views_today": total_views_today,
                "total_comparisons": total_comparisons,
                "top_product_current_hour": top_product_today[0] if top_product_today else None,
                "cache_status": "healthy"
            }
            
        except Exception as e:
            return {"error": str(e), "cache_status": "error"}

    async def close(self):
        """Close Redis connection"""
        await self.redis_client.close()


# Global trending service instance
trending_service = TrendingService()
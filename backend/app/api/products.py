from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from ..database import get_db
from ..models import AffiliateStore, Product, ProductPrice
from ..services.enhanced_affiliate_service import EnhancedAffiliateService
from ..utils.vote_utils import get_multiple_products_vote_stats, get_product_vote_stats


router = APIRouter(prefix="/products", tags=["products"])


def _extract_image_urls(images_dict: Dict[str, Any]) -> List[str]:
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


def _get_thomann_info(product: Product) -> Dict[str, Any]:
    """
    Get Thomann URL information for a product.
    Returns either the actual Thomann URL from store_links or a search URL.
    """
    thomann_info = {
        "has_direct_url": False,
        "url": None,
        "fallback_search_url": f"https://thomann.com/intl/search_dir.html?sw={product.name.replace(' ', '%20')}&aff=123"
    }
    
    # Check if we have Thomann URL in store_links (AI-generated content)
    if product.content and isinstance(product.content, dict):
        store_links = product.content.get('store_links', {})
        if store_links:
            # Try different possible keys for Thomann URL
            thomann_url = (
                store_links.get('Thomann') or 
                store_links.get('thomann') or 
                store_links.get('thomann_url') or 
                store_links.get('THOMANN')
            )
            
            if thomann_url and isinstance(thomann_url, str) and thomann_url.startswith('http'):
                thomann_info["has_direct_url"] = True
                thomann_info["url"] = thomann_url
    
    # If no direct URL found, use the fallback search URL
    if not thomann_info["has_direct_url"]:
        thomann_info["url"] = thomann_info["fallback_search_url"]
    
    return thomann_info


def get_content_for_display(content: Dict[str, Any], language: str = "en-GB") -> Dict[str, Any]:
    """
    Extract content for display, combining localized content with global fields.
    Some fields like specifications, store_links, etc. are always in English.
    """
    if not content:
        return {}
    
    result = {}
    
    # Add global fields that are always in English
    global_fields = ['specifications', 'store_links', 'warranty_info', 'qa', 'sources', 'dates', 'content_metadata', 'related_products']
    for field in global_fields:
        if field in content:
            result[field] = content[field]
    
    # Get localized content
    localized_content = content.get('localized_content', {})
    if localized_content:
        # Try requested language first
        selected_content = None
        if language in localized_content:
            selected_content = localized_content[language]
        else:
            # Fallback to English variants
            english_variants = ['en-GB', 'en-US', 'en']
            for variant in english_variants:
                if variant in localized_content:
                    selected_content = localized_content[variant]
                    break
        
        # If no English found, use first available
        if not selected_content and localized_content:
            first_language = next(iter(localized_content.keys()))
            selected_content = localized_content[first_language]
        
        # Merge localized content into result
        if selected_content:
            result.update(selected_content)
            result['_language_used'] = language if language in localized_content else next(iter(localized_content.keys()))
    
    return result


@router.get("")
async def search_products(
    q: Optional[str] = Query(None, alias="query"),
    query: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    slugs: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, alias="price_min"),
    max_price: Optional[float] = Query(None, alias="price_max"),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    sort_by: str = Query("name"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    # Handle parameter aliases
    search_query = q or query
    min_price_filter = min_price or price_min
    max_price_filter = max_price or price_max
    offset = (page - 1) * limit

    base_stmt = (
        select(Product)
        .options(joinedload(Product.brand), joinedload(Product.category))
        .where(Product.is_active.is_(True))
    )
    
    # If fetching by slugs, also load prices for comparison
    if slugs:
        base_stmt = base_stmt.options(joinedload(Product.prices).joinedload(ProductPrice.store))

    # Filters
    if search_query:
        like_expr = f"%{search_query.lower()}%"
        base_stmt = base_stmt.where(func.lower(Product.name).like(like_expr))
    if category:
        from ..models import Category

        base_stmt = base_stmt.join(Product.category).where(Category.slug == category)
    if brand:
        from ..models import Brand

        base_stmt = base_stmt.join(Product.brand).where(Brand.slug == brand)
    if slugs:
        # Filter by specific product slugs (comma-separated)
        slug_list = [slug.strip() for slug in slugs.split(',') if slug.strip()]
        if slug_list:
            base_stmt = base_stmt.where(Product.slug.in_(slug_list))

    # Price filtering
    if min_price_filter is not None or max_price_filter is not None:
        # Create subquery for best prices
        price_subq = (
            select(
                ProductPrice.product_id,
                func.min(ProductPrice.price).label("best_price"),
            )
            .where(ProductPrice.is_available.is_(True))
            .group_by(ProductPrice.product_id)
            .subquery()
        )
        base_stmt = base_stmt.outerjoin(price_subq, price_subq.c.product_id == Product.id)
        
        if min_price_filter is not None:
            base_stmt = base_stmt.where(price_subq.c.best_price >= min_price_filter)
        if max_price_filter is not None:
            base_stmt = base_stmt.where(price_subq.c.best_price <= max_price_filter)

    # Sorting
    if sort_by == "price":
        # Sort by best available price
        if min_price_filter is not None or max_price_filter is not None:
            # Price subquery already joined above
            base_stmt = base_stmt.order_by(asc(price_subq.c.best_price.nullslast()))
        else:
            price_subq = (
                select(
                    ProductPrice.product_id,
                    func.min(ProductPrice.price).label("best_price"),
                )
                .where(ProductPrice.is_available.is_(True))
                .group_by(ProductPrice.product_id)
                .subquery()
            )
            base_stmt = (
                base_stmt.outerjoin(price_subq, price_subq.c.product_id == Product.id).order_by(
                    asc(price_subq.c.best_price.nullslast())
                )
            )
    elif sort_by == "rating":
        base_stmt = base_stmt.order_by(desc(Product.avg_rating))
    elif sort_by == "popularity":
        # Sort by review count as a proxy for popularity
        base_stmt = base_stmt.order_by(desc(Product.review_count))
    else:
        base_stmt = base_stmt.order_by(asc(Product.name))

    # Count total
    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    # Pagination
    stmt = base_stmt.offset(offset).limit(limit)
    result = await db.execute(stmt)
    products: List[Product] = result.scalars().unique().all()
    
    # Debug logging
    print(f"🔍 Products API - Filters: query='{search_query}', category='{category}', brand='{brand}', price_min={min_price_filter}, price_max={max_price_filter}, sort_by='{sort_by}'")
    print(f"📊 Products API - Results: {len(products)} products, total={total}, page={page}, limit={limit}")

    # Compute best price per product and vote stats
    product_ids = [p.id for p in products]
    best_prices: Dict[int, Dict[str, Any]] = {}
    vote_stats_dict = await get_multiple_products_vote_stats(db, product_ids)
    
    # Note: Thomann URLs are now extracted from store_links in product content, not prices
    
    if product_ids:
        bp_stmt = (
            select(
                ProductPrice.product_id,
                func.min(ProductPrice.price).label("best_price"),
            )
            .where(ProductPrice.product_id.in_(product_ids), ProductPrice.is_available.is_(True))
            .group_by(ProductPrice.product_id)
            .subquery()
        )

        join_stmt = (
            select(ProductPrice)
            .join(bp_stmt, (bp_stmt.c.product_id == ProductPrice.product_id) & (bp_stmt.c.best_price == ProductPrice.price))
            .join(AffiliateStore, AffiliateStore.id == ProductPrice.store_id)
        )
        join_res = await db.execute(join_stmt)
        rows = join_res.scalars().all()
        # Need store names: fetch mapping
        store_map = {
            s.id: s
            for s in (await db.execute(select(AffiliateStore).where(AffiliateStore.id.in_([r.store_id for r in rows])))).scalars().all()
        }
        for r in rows:
            store = store_map.get(r.store_id)
            best_prices[r.product_id] = {
                "price": float(r.price),
                "currency": r.currency,
                "store_name": store.name if store else None,
            }

    items: List[Dict[str, Any]] = []
    for p in products:
        bp = best_prices.get(p.id)
        vote_stats = vote_stats_dict.get(p.id, {
            "thumbs_up_count": 0,
            "thumbs_down_count": 0,
            "total_votes": 0,
            "vote_score": 0
        })
        
        # Build prices array if prices are loaded (for comparison)
        prices = None
        if slugs and hasattr(p, 'prices') and p.prices:
            prices = [
                {
                    "id": pr.id,
                    "store": {
                        "id": pr.store.id,
                        "name": pr.store.name,
                        "logo_url": pr.store.logo_url,
                        "website_url": pr.store.website_url,
                    },
                    "price": float(pr.price),
                    "currency": pr.currency,
                    "affiliate_url": pr.affiliate_url,
                    "last_checked": pr.last_checked.isoformat() if pr.last_checked else None,
                    "is_available": pr.is_available,
                }
                for pr in sorted(p.prices, key=lambda x: (x.price or Decimal("0")))
                if pr.is_available
            ]
        
        # Get content for display (combines localized + global fields)
        display_content = get_content_for_display(p.content or {})
        
        # Get Thomann URL information from store_links in product content
        thomann_info = _get_thomann_info(p)
        
        items.append(
            {
                "id": p.id,
                "name": p.name,
                "slug": p.slug,
                "brand": {"id": p.brand.id, "name": p.brand.name, "slug": p.brand.slug},
                "category": {
                    "id": p.category.id,
                    "name": p.category.name,
                    "slug": p.category.slug,
                },
                "description": p.description,
                "specifications": p.content.get('specifications', {}) if p.content else {},
                "images": _extract_image_urls(p.images) if p.images else [],
                "msrp_price": float(p.msrp_price) if p.msrp_price is not None else None,
                "avg_rating": float(p.avg_rating) if p.avg_rating is not None else 0.0,
                "review_count": p.review_count,
                "vote_stats": vote_stats,
                "best_price": (
                    {
                        "price": bp["price"],
                        "currency": bp["currency"],
                        "affiliate_url": None,
                        "last_checked": None,
                        "store": {"name": bp["store_name"]} if bp else None,
                    }
                    if bp
                    else None
                ),
                "prices": prices,
                "thomann_info": thomann_info,
                "ai_content": p.content or {},
                "content": display_content,
            }
        )

    return {
        "products": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit,
        },
        "filters_applied": {
            k: v
            for k, v in {
                "query": search_query,
                "category": category,
                "brand": brand,
                "price_min": min_price_filter,
                "price_max": max_price_filter,
                "sort_by": sort_by,
            }.items()
            if v not in (None, "")
        },
    }





@router.get("/{product_id}")
async def get_product(
    product_id: int, 
    user_region: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get product with affiliate stores following brand exclusivity and regional rules"""
    stmt = (
        select(Product)
        .options(selectinload(Product.brand), selectinload(Product.category), selectinload(Product.prices).selectinload(ProductPrice.store))
        .where(Product.id == product_id)
    )
    result = await db.execute(stmt)
    product: Product | None = result.scalars().unique().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Build response
    prices = [
        {
            "store": {
                "id": pr.store.id,
                "name": pr.store.name,
                "logo_url": pr.store.logo_url,
                "website_url": pr.store.website_url,
            },
            "price": float(pr.price),
            "currency": pr.currency,
            "affiliate_url": pr.affiliate_url,
            "last_checked": pr.last_checked.isoformat(),
        }
        for pr in sorted(product.prices, key=lambda x: (x.price or Decimal("0")))
        if pr.is_available
    ]
    best_price = prices[0] if prices else None

    # Get affiliate stores using enhanced service with brand exclusivity rules
    affiliate_service = EnhancedAffiliateService(db)
    affiliate_stores = await affiliate_service.get_affiliate_stores_for_product(
        product=product,
        user_region=user_region
    )

    # Get content for display (combines localized + global fields)
    display_content = get_content_for_display(product.content or {})
    
    # Get vote statistics
    vote_stats = await get_product_vote_stats(db, product_id)

    return {
        "id": product.id,
        "sku": product.sku,
        "name": product.name,
        "slug": product.slug,
        "brand": {"id": product.brand.id, "name": product.brand.name, "slug": product.brand.slug},
        "category": {
            "id": product.category.id,
            "name": product.category.name,
            "slug": product.category.slug,
        },
        "description": product.description,
        "specifications": product.content.get('specifications', {}) if product.content else {},
        "images": _extract_image_urls(product.images) if product.images else [],
        "msrp_price": float(product.msrp_price) if product.msrp_price is not None else None,
        "avg_rating": float(product.avg_rating) if product.avg_rating is not None else 0.0,
        "review_count": product.review_count,
        "vote_stats": vote_stats,
        "ai_content": product.content or {},
        "content": display_content,
        "prices": prices,
        "best_price": best_price,
        "affiliate_stores": affiliate_stores,
        "total_affiliate_stores": len(affiliate_stores),
        "user_region": user_region,
    }


@router.post("/{product_id}/affiliate-stores")
async def get_product_affiliate_stores_with_links(
    product_id: int,
    store_links: Dict,
    user_region: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get affiliate stores for a product with store links and regional preferences"""
    
    # Get product with brand relationship
    product_query = select(Product).options(selectinload(Product.brand)).where(Product.id == product_id)
    product_result = await db.execute(product_query)
    product = product_result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get affiliate stores using enhanced service
    affiliate_service = EnhancedAffiliateService(db)
    affiliate_stores = await affiliate_service.get_affiliate_stores_for_product(
        product=product,
        user_region=user_region,
        store_links=store_links
    )
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "brand": product.brand.name if product.brand else None,
        "affiliate_stores": affiliate_stores,
        "total_stores": len(affiliate_stores),
        "store_links_provided": len(store_links),
        "user_region": user_region,
        "message": "Returns stores filtered by brand exclusivity, regional preferences, and store links"
    }


@router.get("/{product_id}/affiliate-urls")
async def get_product_affiliate_urls(
    product_id: int,
    user_region: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get affiliate URLs for a product in all available stores"""
    
    # First check if product exists
    product_query = select(Product).options(selectinload(Product.brand)).where(Product.id == product_id)
    product_result = await db.execute(product_query)
    product = product_result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get affiliate stores for this product using enhanced service
    affiliate_service = EnhancedAffiliateService(db)
    affiliate_stores = await affiliate_service.get_affiliate_stores_for_product(
        product=product,
        user_region=user_region
    )
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "affiliate_stores": affiliate_stores,
        "total_stores": len(affiliate_stores)
    }






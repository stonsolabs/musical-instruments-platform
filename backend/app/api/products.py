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



def get_clean_content(content: Dict[str, Any], language: str = "en-GB") -> Dict[str, Any]:
    """
    Extract content for frontend, including all rich product information.
    """
    if not content:
        return {}
    
    result = {}
    
    # Include all top-level content fields that the frontend expects
    top_level_fields = [
        'qa', 'dates', 'sources', 'setup_tips', 'audience_fit', 
        'quick_badges', 'warranty_info', 'specifications', 
        'category_specific', 'comparison_helpers', 'professional_ratings',
        'accessory_recommendations', 'store_links'
    ]
    
    for field in top_level_fields:
        if field in content:
            result[field] = content[field]
    
    # Merge Q&A from multiple locations
    qa_list = []
    
    # Get Q&A from top level
    if content.get('qa') and isinstance(content['qa'], list):
        qa_list.extend(content['qa'])
    
    # Get Q&A from content_metadata (filter out sensitive metadata)
    content_metadata = content.get('content_metadata', {})
    if content_metadata.get('qa') and isinstance(content_metadata['qa'], list):
        qa_list.extend(content_metadata['qa'])
    
    # Remove duplicates and sensitive metadata
    if qa_list:
        seen_questions = set()
        unique_qa = []
        for qa_item in qa_list:
            if isinstance(qa_item, dict) and 'question' in qa_item and 'answer' in qa_item:
                question_lower = qa_item['question'].lower().strip()
                if question_lower not in seen_questions:
                    # Filter out sensitive metadata fields
                    clean_qa = {
                        'question': qa_item['question'],
                        'answer': qa_item['answer']
                    }
                    # Keep any other non-sensitive fields
                    for key, value in qa_item.items():
                        if key not in ['question', 'answer', 'generated_by', 'created_by', 'metadata', 'internal_notes']:
                            clean_qa[key] = value
                    unique_qa.append(clean_qa)
                    seen_questions.add(question_lower)
        
        if unique_qa:
            result['qa'] = unique_qa
    
    # Handle sources from content_metadata if not found at top level  
    if 'sources' not in result and content.get('content_metadata', {}).get('sources'):
        result['sources'] = content['content_metadata']['sources']
        
    # Handle dates from content_metadata if not found at top level
    if 'dates' not in result and content.get('content_metadata', {}).get('dates'):
        result['dates'] = content['content_metadata']['dates']
    
    # Get localized content for the requested language
    localized_content = content.get('localized_content', {})
    if localized_content:
        # Include the full localized_content structure for frontend to access
        result['localized_content'] = localized_content
        
        # Also merge selected language content at root level for backward compatibility
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
        
        # Merge user-facing content at root level
        if selected_content:
            content_fields = [
                'basic_info', 'usage_guidance', 'customer_reviews', 
                'maintenance_care', 'purchase_decision', 'technical_analysis', 
                'professional_assessment'
            ]
            for field in content_fields:
                if field in selected_content:
                    result[field] = selected_content[field]
    
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

    # Price filtering removed - not using best price functionality

    # Sorting
    if sort_by == "price":
        # Price sorting removed - not using best price functionality
        base_stmt = base_stmt.order_by(asc(Product.name))  # Fallback to name sorting
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

    # Get vote stats for products (best price functionality removed)
    product_ids = [p.id for p in products]
    vote_stats_dict = await get_multiple_products_vote_stats(db, product_ids)

    items: List[Dict[str, Any]] = []
    for p in products:
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
        
        # Get clean content for display (no sensitive AI metadata)
        clean_content = get_clean_content(p.content or {})
        
        # Extract thomann URL for affiliate buttons
        thomann_info = None
        if p.content and p.content.get('store_links', {}).get('Thomann'):
            thomann_info = {
                "has_direct_url": True,
                "url": p.content['store_links']['Thomann']
            }
        
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
                "images": _extract_image_urls(p.images) if p.images else [],
                "msrp_price": float(p.msrp_price) if p.msrp_price is not None else None,
                "avg_rating": float(p.avg_rating) if p.avg_rating is not None else 0.0,
                "review_count": p.review_count,
                "vote_stats": vote_stats,
                "prices": prices,
                "content": clean_content,
                "thomann_info": thomann_info,
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
    """Get product by ID with affiliate stores following brand exclusivity and regional rules"""
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
    # Best price functionality removed

    # Get affiliate stores using enhanced service with brand exclusivity rules
    affiliate_service = EnhancedAffiliateService(db)
    affiliate_stores = await affiliate_service.get_affiliate_stores_for_product(
        product=product,
        user_region=user_region
    )

    # Get clean content for display (no sensitive AI metadata) 
    clean_content = get_clean_content(product.content or {})
    
    # Extract thomann URL for affiliate buttons
    thomann_info = None
    if product.content and product.content.get('store_links', {}).get('Thomann'):
        thomann_info = {
            "has_direct_url": True,
            "url": product.content['store_links']['Thomann']
        }
    
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
        "images": _extract_image_urls(product.images) if product.images else [],
        "msrp_price": float(product.msrp_price) if product.msrp_price is not None else None,
        "avg_rating": float(product.avg_rating) if product.avg_rating is not None else 0.0,
        "review_count": product.review_count,
        "vote_stats": vote_stats,
        "content": clean_content,
        "thomann_info": thomann_info,
        "prices": prices,
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






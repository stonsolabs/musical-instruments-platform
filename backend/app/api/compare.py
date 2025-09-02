from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..database import get_db
from ..models import Product, ProductPrice
from ..services.trending_service import trending_service


router = APIRouter(prefix="/compare", tags=["compare"])


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


@router.post("")
async def compare_products(
    product_ids: List[int] = Body(..., embed=False), db: AsyncSession = Depends(get_db)
):
    if not product_ids or len(product_ids) < 1:
        raise HTTPException(status_code=400, detail="Provide at least one product ID")

    stmt = (
        select(Product)
        .options(joinedload(Product.brand), joinedload(Product.category), joinedload(Product.prices))
        .where(Product.id.in_(product_ids))
    )
    result = await db.execute(stmt)
    products = result.scalars().unique().all()
    if len(products) < 1:
        raise HTTPException(status_code=404, detail="Some products not found")

    # Build comparison data
    products_data: List[Dict[str, Any]] = []
    spec_sets: List[set[str]] = []
    for p in products:
        prices = [
            {
                "id": pr.id,
                "store": {"id": pr.store_id, "name": pr.store.name, "slug": pr.store.slug},
                "price": float(pr.price),
                "currency": pr.currency,
                "affiliate_url": pr.affiliate_url,
                "last_checked": pr.last_checked.isoformat(),
                "is_available": pr.is_available,
            }
            for pr in p.prices
            if pr.is_available
        ]
        products_data.append(
            {
                "id": p.id,
                "sku": p.sku,
                "name": p.name,
                "slug": p.slug,
                "brand": {"id": p.brand.id, "name": p.brand.name, "slug": p.brand.slug},
                "category": {
                    "id": p.category.id,
                    "name": p.category.name,
                    "slug": p.category.slug,
                },
                "specifications": p.content.get('specifications', {}) if p.content else {},
                "images": _extract_image_urls(p.images) if p.images else [],
                "msrp_price": float(p.msrp_price) if p.msrp_price else None,
                "avg_rating": float(p.avg_rating) if p.avg_rating else 0.0,
                "review_count": p.review_count,
                "ai_content": p.content or {},
                "prices": prices,
                "best_price": (sorted(prices, key=lambda x: x["price"])[0] if prices else None),
            }
        )
        specs = p.content.get('specifications', {}) if p.content else {}
        spec_sets.append(set(specs.keys()) if specs else set())

    common_specs = sorted(list(set.intersection(*spec_sets))) if spec_sets else []

    # Build comparison matrix for common specs
    comparison_matrix: Dict[str, Dict[str, Any]] = {}
    for spec in common_specs:
        row: Dict[str, Any] = {}
        for p in products:
            specs = p.content.get('specifications', {}) if p.content else {}
            row[str(p.id)] = specs.get(spec, None)
        comparison_matrix[spec] = row

    return {
        "products": products_data,
        "common_specs": common_specs,
        "comparison_matrix": comparison_matrix,
        "generated_at": datetime.utcnow().isoformat(),
    }



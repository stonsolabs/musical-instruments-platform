from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..database import get_db
from ..models import Product, ProductPrice


router = APIRouter(prefix="/compare", tags=["compare"])


@router.post("")
async def compare_products(
    product_ids: List[int] = Body(..., embed=False), db: AsyncSession = Depends(get_db)
):
    if not product_ids or len(product_ids) < 2:
        raise HTTPException(status_code=400, detail="Provide at least two product IDs")

    stmt = (
        select(Product)
        .options(joinedload(Product.brand), joinedload(Product.category), joinedload(Product.prices))
        .where(Product.id.in_(product_ids))
    )
    result = await db.execute(stmt)
    products = result.scalars().unique().all()
    if len(products) < 2:
        raise HTTPException(status_code=404, detail="Some products not found")

    # Build comparison data
    products_data: List[Dict[str, Any]] = []
    spec_sets: List[set[str]] = []
    for p in products:
        prices = [
            {
                "store": {"id": pr.store_id},
                "price": float(pr.price),
                "currency": pr.currency,
                "affiliate_url": pr.affiliate_url,
                "last_checked": pr.last_checked.isoformat(),
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
                "specifications": p.specifications or {},
                "images": p.images or [],
                "msrp_price": float(p.msrp_price) if p.msrp_price else None,
                "avg_rating": float(p.avg_rating) if p.avg_rating else 0.0,
                "review_count": p.review_count,
                "ai_content": p.ai_generated_content or {},
                "prices": prices,
                "best_price": (sorted(prices, key=lambda x: x["price"])[0] if prices else None),
            }
        )
        spec_sets.append(set(p.specifications.keys()) if p.specifications else set())

    common_specs = sorted(list(set.intersection(*spec_sets))) if spec_sets else []

    # Build comparison matrix for common specs
    comparison_matrix: Dict[str, Dict[str, Any]] = {}
    for spec in common_specs:
        row: Dict[str, Any] = {}
        for p in products:
            row[str(p.id)] = (p.specifications or {}).get(spec, None)
        comparison_matrix[spec] = row

    return {
        "products": products_data,
        "common_specs": common_specs,
        "comparison_matrix": comparison_matrix,
        "generated_at": datetime.utcnow().isoformat(),
    }



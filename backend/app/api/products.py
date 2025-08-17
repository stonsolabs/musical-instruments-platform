from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..database import get_db
from ..models import AffiliateStore, Product, ProductPrice


router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
async def search_products(
    q: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    slugs: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    sort_by: str = Query("name"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * limit

    base_stmt = (
        select(Product)
        .options(joinedload(Product.brand), joinedload(Product.category))
        .where(Product.is_active.is_(True))
    )

    # Filters
    if q:
        like_expr = f"%{q.lower()}%"
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

    # Sorting
    if sort_by == "price":
        # Sort by best available price
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
    else:
        base_stmt = base_stmt.order_by(asc(Product.name))

    # Count total
    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    # Pagination
    stmt = base_stmt.offset(offset).limit(limit)
    result = await db.execute(stmt)
    products: List[Product] = result.scalars().unique().all()

    # Compute best price per product
    product_ids = [p.id for p in products]
    best_prices: Dict[int, Dict[str, Any]] = {}
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
                "specifications": p.specifications or {},
                "images": p.images or [],
                "msrp_price": float(p.msrp_price) if p.msrp_price is not None else None,
                "avg_rating": float(p.avg_rating) if p.avg_rating is not None else 0.0,
                "review_count": p.review_count,
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
                "ai_content": p.ai_generated_content or {},
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
                "q": q,
                "category": category,
                "brand": brand,
                "min_price": min_price,
                "max_price": max_price,
                "sort_by": sort_by,
            }.items()
            if v not in (None, "")
        },
    }


@router.get("/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Product)
        .options(joinedload(Product.brand), joinedload(Product.category), joinedload(Product.prices).joinedload(ProductPrice.store))
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
        "specifications": product.specifications or {},
        "images": product.images or [],
        "msrp_price": float(product.msrp_price) if product.msrp_price is not None else None,
        "avg_rating": float(product.avg_rating) if product.avg_rating is not None else 0.0,
        "review_count": product.review_count,
        "ai_content": product.ai_generated_content or {},
        "prices": prices,
        "best_price": best_price,
    }



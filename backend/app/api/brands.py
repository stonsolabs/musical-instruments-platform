from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Brand, Category, Product


router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("")
async def list_brands(category: Optional[str] = Query(None), db: AsyncSession = Depends(get_db)):
    if category:
        # Brands that have products in a given category
        stmt = (
            select(Brand)
            .join(Product, Product.brand_id == Brand.id)
            .join(Category, Category.id == Product.category_id)
            .where(Category.slug == category)
            .distinct()
        )
    else:
        stmt = select(Brand)

    result = await db.execute(stmt)
    brands = result.scalars().all()
    return [
        {
            "id": b.id,
            "name": b.name,
            "slug": b.slug,
            "logo_url": b.logo_url,
            "description": b.description,
        }
        for b in brands
    ]



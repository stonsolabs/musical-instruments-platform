from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Category


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
async def list_categories(parent_id: Optional[int] = Query(None), db: AsyncSession = Depends(get_db)):
    stmt = select(Category).where(Category.is_active.is_(True))
    if parent_id is not None:
        stmt = stmt.where(Category.parent_id == parent_id)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "description": c.description,
            "parent_id": c.parent_id,
            "image_url": c.image_url,
        }
        for c in categories
    ]



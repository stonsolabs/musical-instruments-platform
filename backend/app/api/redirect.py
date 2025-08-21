from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from ..database import get_db
from ..models import ProductPrice
from ..services.affiliate_manager import AffiliateManager


router = APIRouter(prefix="/redirect", tags=["affiliate"])


@router.get("/{product_id}/{store_id}")
async def redirect_affiliate(product_id: int, store_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProductPrice).where(
            ProductPrice.product_id == product_id,
            ProductPrice.store_id == store_id,
            ProductPrice.is_available.is_(True),
        )
    )
    price = result.scalars().first()
    if not price:
        raise HTTPException(status_code=404, detail="Affiliate link not found")

    # Log click (fire and forget)
    manager = AffiliateManager()
    client_ip = request.client.host if request.client else None
    user_context = {"country": request.headers.get("CF-IPCountry") or "", "ip": client_ip or ""}
    try:
        await manager.log_click(product_id, store_id, user_context)
    except Exception:
        pass

    return RedirectResponse(url=price.affiliate_url, status_code=302)



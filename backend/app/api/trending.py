from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..services.trending_service import trending_service

router = APIRouter(prefix="/trending", tags=["trending"])


@router.get("/instruments")
async def get_trending_instruments(
    limit: int = Query(10, ge=1, le=50),
    category_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Get trending musical instruments based on views and comparisons
    """
    try:
        trending = await trending_service.get_trending_instruments(
            limit=limit,
            category_id=category_id,
            db=db
        )
        return {
            "trending_instruments": trending,
            "total": len(trending),
            "category_id": category_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trending instruments: {str(e)}")


@router.get("/comparisons") 
async def get_popular_comparisons(
    limit: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    """
    Get most popular instrument comparisons
    """
    try:
        comparisons = await trending_service.get_popular_comparisons(
            limit=limit,
            db=db
        )
        return {
            "popular_comparisons": comparisons,
            "total": len(comparisons)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get popular comparisons: {str(e)}")


@router.get("/by-category")
async def get_trending_by_category(
    db: AsyncSession = Depends(get_db),
):
    """
    Get trending instruments grouped by category
    """
    try:
        category_trending = await trending_service.get_category_trending(db=db)
        return {
            "trending_by_category": category_trending,
            "categories": len(category_trending)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get category trending: {str(e)}")


@router.post("/track/view/{product_id}")
async def track_product_view(
    product_id: int,
    request: Request
):
    """
    Track a product view for trending calculations
    """
    try:
        # Get client IP for unique view tracking
        client_ip = request.client.host if request.client else None
        
        await trending_service.track_product_view(product_id, client_ip)
        return {"message": "View tracked successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track view: {str(e)}")


@router.get("/track/comparison")
async def track_product_comparison(
    product_id_1: int = Query(...),
    product_id_2: int = Query(...)
):
    """
    Track when two products are compared together
    """
    if product_id_1 == product_id_2:
        raise HTTPException(status_code=400, detail="Cannot compare a product with itself")
        
    try:
        await trending_service.track_product_comparison(product_id_1, product_id_2)
        return {"message": "Comparison tracked successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track comparison: {str(e)}")


@router.get("/analytics")
async def get_analytics_summary():
    """
    Get trending analytics summary (admin endpoint)
    """
    try:
        analytics = await trending_service.get_analytics_summary()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")


@router.post("/cache/clear")
async def clear_trending_cache():
    """
    Clear trending and comparison caches (admin endpoint)
    """
    try:
        await trending_service.clear_trending_cache()
        return {"message": "Trending cache cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")
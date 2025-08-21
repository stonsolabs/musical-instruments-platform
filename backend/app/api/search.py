from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..services.search_service import search_service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/autocomplete")
async def search_autocomplete(
    q: str = Query(..., min_length=2, max_length=100),
    limit: int = Query(8, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    """
    Get autocomplete suggestions for product search
    """
    try:
        results = await search_service.search_products(q, limit, db)
        return {
            "query": q,
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=2, max_length=100),
    limit: int = Query(5, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
):
    """
    Get search term suggestions
    """
    try:
        suggestions = await search_service.get_search_suggestions(q, limit, db)
        return {
            "query": q,
            "suggestions": suggestions,
            "total": len(suggestions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get suggestions: {str(e)}")


@router.post("/cache/clear")
async def clear_search_cache():
    """
    Clear search cache (admin endpoint)
    """
    try:
        await search_service.clear_search_cache()
        return {"message": "Search cache cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")

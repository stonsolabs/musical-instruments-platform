from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import AffiliateStore
from ..services.affiliate_manager import AffiliateManager

router = APIRouter(prefix="/affiliate-stores", tags=["affiliate-stores"])


@router.get("")
async def list_affiliate_stores(
    has_affiliate_program: Optional[bool] = Query(None),
    show_affiliate_buttons: Optional[bool] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """List all affiliate stores with optional filtering"""
    
    query = select(AffiliateStore)
    
    # Apply filters
    if has_affiliate_program is not None:
        query = query.where(AffiliateStore.has_affiliate_program.is_(has_affiliate_program))
    if show_affiliate_buttons is not None:
        query = query.where(AffiliateStore.show_affiliate_buttons.is_(show_affiliate_buttons))
    if is_active is not None:
        query = query.where(AffiliateStore.is_active.is_(is_active))
    
    # Order by priority (highest first) then by name
    query = query.order_by(AffiliateStore.priority.desc(), AffiliateStore.name)
    
    result = await db.execute(query)
    stores = result.scalars().all()
    
    return {
        "stores": [
            {
                "id": store.id,
                "name": store.name,
                "slug": store.slug,
                "website_url": store.website_url,
                "logo_url": store.logo_url,
                "has_affiliate_program": store.has_affiliate_program,
                "show_affiliate_buttons": store.show_affiliate_buttons,
                "priority": store.priority,
                "commission_rate": float(store.commission_rate) if store.commission_rate else None,
                "is_active": store.is_active,
            }
            for store in stores
        ]
    }


@router.get("/{store_id}")
async def get_affiliate_store(
    store_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get detailed information about a specific affiliate store"""
    
    query = select(AffiliateStore).where(AffiliateStore.id == store_id)
    result = await db.execute(query)
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(status_code=404, detail="Affiliate store not found")
    
    return {
        "id": store.id,
        "name": store.name,
        "slug": store.slug,
        "website_url": store.website_url,
        "logo_url": store.logo_url,
        "has_affiliate_program": store.has_affiliate_program,
        "affiliate_base_url": store.affiliate_base_url,
        "affiliate_id": store.affiliate_id,
        "affiliate_parameters": store.affiliate_parameters,
        "show_affiliate_buttons": store.show_affiliate_buttons,
        "priority": store.priority,
        "commission_rate": float(store.commission_rate) if store.commission_rate else None,
        "is_active": store.is_active,
        "created_at": store.created_at.isoformat(),
    }


@router.put("/{store_id}/affiliate-config")
async def update_store_affiliate_config(
    store_id: int,
    has_affiliate_program: Optional[bool] = None,
    affiliate_base_url: Optional[str] = None,
    affiliate_id: Optional[str] = None,
    affiliate_parameters: Optional[Dict] = None,
    show_affiliate_buttons: Optional[bool] = None,
    priority: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """Update affiliate configuration for a store"""
    
    affiliate_manager = AffiliateManager(db)
    
    try:
        store = await affiliate_manager.update_store_affiliate_config(
            store_id=store_id,
            has_affiliate_program=has_affiliate_program,
            affiliate_base_url=affiliate_base_url,
            affiliate_id=affiliate_id,
            affiliate_parameters=affiliate_parameters,
            show_affiliate_buttons=show_affiliate_buttons,
            priority=priority
        )
        
        return {
            "id": store.id,
            "name": store.name,
            "has_affiliate_program": store.has_affiliate_program,
            "affiliate_base_url": store.affiliate_base_url,
            "affiliate_id": store.affiliate_id,
            "affiliate_parameters": store.affiliate_parameters,
            "show_affiliate_buttons": store.show_affiliate_buttons,
            "priority": store.priority,
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{store_id}/affiliate-config")
async def get_store_affiliate_config(
    store_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get affiliate configuration for a store"""
    
    affiliate_manager = AffiliateManager(db)
    config = await affiliate_manager.get_store_affiliate_config(store_id)
    
    if not config:
        raise HTTPException(status_code=404, detail="Store not found or has no affiliate program")
    
    return config




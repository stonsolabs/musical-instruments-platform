from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models import Product, ProductVote
from ..schemas import VoteRequest, VoteResponse, ProductVoteStats
from ..utils.vote_utils import get_product_vote_stats as get_vote_stats, get_user_vote_for_product


router = APIRouter(prefix="/voting", tags=["voting"])


def get_client_ip(request: Request) -> str:
    """Extract client IP address from request."""
    # Check for X-Forwarded-For header first (for proxies/load balancers)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For can contain multiple IPs, take the first one
        return forwarded_for.split(",")[0].strip()
    
    # Fallback to X-Real-IP
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Finally, use the client host
    return request.client.host if request.client else "unknown"


@router.post("/products/{product_id}/vote", response_model=VoteResponse)
async def vote_on_product(
    product_id: int,
    vote_request: VoteRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Vote on a product (thumbs up or down)."""
    user_ip = get_client_ip(request)
    
    # Check if product exists
    product_query = select(Product).where(Product.id == product_id, Product.is_active.is_(True))
    product_result = await db.execute(product_query)
    product = product_result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user already voted
    existing_vote_query = select(ProductVote).where(
        and_(ProductVote.product_id == product_id, ProductVote.user_ip == user_ip)
    )
    existing_vote_result = await db.execute(existing_vote_query)
    existing_vote = existing_vote_result.scalar_one_or_none()
    
    vote_type = vote_request.vote_type
    message = ""
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # User is trying to vote the same way again, remove the vote (toggle off)
            await db.delete(existing_vote)
            message = f"Your {vote_type} vote has been removed"
            
            user_vote = None
        else:
            # User is changing their vote
            old_vote_type = existing_vote.vote_type
            existing_vote.vote_type = vote_type
            existing_vote.updated_at = func.now()
            
            message = f"Your vote has been changed from {old_vote_type} to {vote_type}"
            
            user_vote = vote_type
    else:
        # New vote
        new_vote = ProductVote(
            product_id=product_id,
            user_ip=user_ip,
            vote_type=vote_type
        )
        db.add(new_vote)
        
        message = f"Your {vote_type} vote has been recorded"
        
        user_vote = vote_type
    
    await db.commit()
    
    # Get updated vote statistics
    vote_stats = await get_vote_stats(db, product_id)
    
    return VoteResponse(
        success=True,
        message=message,
        vote_counts={
            "thumbs_up": vote_stats["thumbs_up_count"],
            "thumbs_down": vote_stats["thumbs_down_count"],
            "total": vote_stats["total_votes"],
            "score": vote_stats["vote_score"]
        },
        user_vote=user_vote
    )


@router.get("/products/{product_id}/stats", response_model=ProductVoteStats)
async def get_product_vote_stats(
    product_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Get voting statistics for a product."""
    user_ip = get_client_ip(request)
    
    # Check if product exists
    product_query = select(Product.id).where(Product.id == product_id, Product.is_active.is_(True))
    product_result = await db.execute(product_query)
    product = product_result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get vote statistics and user vote
    vote_stats = await get_vote_stats(db, product_id)
    user_vote = await get_user_vote_for_product(db, product_id, user_ip)
    
    return ProductVoteStats(
        thumbs_up_count=vote_stats["thumbs_up_count"],
        thumbs_down_count=vote_stats["thumbs_down_count"],
        total_votes=vote_stats["total_votes"],
        vote_score=vote_stats["vote_score"],
        user_vote=user_vote
    )


@router.get("/products/most-voted")
async def get_most_voted_products(
    limit: int = 20,
    sort_by: str = "vote_score",  # vote_score, total_votes, thumbs_up_count
    db: AsyncSession = Depends(get_db)
):
    """Get the most voted products."""
    # Validate sort_by parameter
    valid_sorts = ["vote_score", "total_votes", "thumbs_up_count"]
    if sort_by not in valid_sorts:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid sort_by parameter. Must be one of: {', '.join(valid_sorts)}"
        )
    
    # Build query with vote statistics using subquery
    vote_stats_subq = (
        select(
            ProductVote.product_id,
            func.sum(func.case((ProductVote.vote_type == 'up', 1), 0)).label('thumbs_up_count'),
            func.sum(func.case((ProductVote.vote_type == 'down', 1), 0)).label('thumbs_down_count'),
            func.count().label('total_votes'),
            (func.sum(func.case((ProductVote.vote_type == 'up', 1), 0)) - 
             func.sum(func.case((ProductVote.vote_type == 'down', 1), 0))).label('vote_score')
        )
        .group_by(ProductVote.product_id)
        .having(func.count() > 0)
        .subquery()
    )
    
    # Main query joining products with vote stats
    query = (
        select(Product, vote_stats_subq)
        .options(selectinload(Product.brand), selectinload(Product.category))
        .join(vote_stats_subq, Product.id == vote_stats_subq.c.product_id)
        .where(Product.is_active.is_(True))
    )
    
    # Apply sorting
    if sort_by == "vote_score":
        query = query.order_by(vote_stats_subq.c.vote_score.desc(), vote_stats_subq.c.total_votes.desc())
    elif sort_by == "total_votes":
        query = query.order_by(vote_stats_subq.c.total_votes.desc(), vote_stats_subq.c.vote_score.desc())
    elif sort_by == "thumbs_up_count":
        query = query.order_by(vote_stats_subq.c.thumbs_up_count.desc(), vote_stats_subq.c.total_votes.desc())
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    results = result.all()
    
    # Format response
    products_data = []
    for product, vote_stats in results:
        products_data.append({
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "brand": {
                "id": product.brand.id,
                "name": product.brand.name,
                "slug": product.brand.slug
            },
            "category": {
                "id": product.category.id,
                "name": product.category.name,
                "slug": product.category.slug
            },
            "vote_stats": {
                "thumbs_up_count": int(vote_stats.thumbs_up_count or 0),
                "thumbs_down_count": int(vote_stats.thumbs_down_count or 0),
                "total_votes": int(vote_stats.total_votes or 0),
                "vote_score": int(vote_stats.vote_score or 0)
            },
            "images": product.images,
            "msrp_price": float(product.msrp_price) if product.msrp_price else None
        })
    
    return {
        "products": products_data,
        "total": len(products_data),
        "sort_by": sort_by,
        "limit": limit
    }

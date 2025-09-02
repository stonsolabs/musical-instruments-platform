"""
Utility functions for vote statistics calculation.
"""
from typing import Dict, List, Optional
from sqlalchemy import func, select, case
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import ProductVote


async def get_product_vote_stats(db: AsyncSession, product_id: int) -> Dict[str, int]:
    """
    Get vote statistics for a single product.
    
    Args:
        db: Database session
        product_id: ID of the product
        
    Returns:
        Dictionary with vote statistics
    """
    vote_stats_query = select(
        func.sum(case((ProductVote.vote_type == 'up', 1), else_=0)).label('thumbs_up'),
        func.sum(case((ProductVote.vote_type == 'down', 1), else_=0)).label('thumbs_down'),
        func.count().label('total_votes')
    ).where(ProductVote.product_id == product_id)
    
    result = await db.execute(vote_stats_query)
    stats = result.first()
    
    thumbs_up = int(stats.thumbs_up or 0)
    thumbs_down = int(stats.thumbs_down or 0)
    total_votes = int(stats.total_votes or 0)
    vote_score = thumbs_up - thumbs_down
    
    return {
        "thumbs_up_count": thumbs_up,
        "thumbs_down_count": thumbs_down,
        "total_votes": total_votes,
        "vote_score": vote_score
    }


async def get_multiple_products_vote_stats(db: AsyncSession, product_ids: List[int]) -> Dict[int, Dict[str, int]]:
    """
    Get vote statistics for multiple products.
    
    Args:
        db: Database session
        product_ids: List of product IDs
        
    Returns:
        Dictionary mapping product_id to vote statistics
    """
    if not product_ids:
        return {}
    
    vote_stats_query = select(
        ProductVote.product_id,
        func.sum(case((ProductVote.vote_type == 'up', 1), else_=0)).label('thumbs_up'),
        func.sum(case((ProductVote.vote_type == 'down', 1), else_=0)).label('thumbs_down'),
        func.count().label('total_votes')
    ).where(ProductVote.product_id.in_(product_ids)).group_by(ProductVote.product_id)
    
    result = await db.execute(vote_stats_query)
    stats_rows = result.all()
    
    # Initialize all products with zero stats
    stats_dict = {}
    for product_id in product_ids:
        stats_dict[product_id] = {
            "thumbs_up_count": 0,
            "thumbs_down_count": 0,
            "total_votes": 0,
            "vote_score": 0
        }
    
    # Update with actual stats
    for row in stats_rows:
        thumbs_up = int(row.thumbs_up or 0)
        thumbs_down = int(row.thumbs_down or 0)
        total_votes = int(row.total_votes or 0)
        vote_score = thumbs_up - thumbs_down
        
        stats_dict[row.product_id] = {
            "thumbs_up_count": thumbs_up,
            "thumbs_down_count": thumbs_down,
            "total_votes": total_votes,
            "vote_score": vote_score
        }
    
    return stats_dict


async def get_user_vote_for_product(db: AsyncSession, product_id: int, user_ip: str) -> Optional[str]:
    """
    Get the current user's vote for a product.
    
    Args:
        db: Database session
        product_id: ID of the product
        user_ip: User's IP address
        
    Returns:
        Vote type ('up' or 'down') or None if no vote
    """
    vote_query = select(ProductVote.vote_type).where(
        ProductVote.product_id == product_id,
        ProductVote.user_ip == user_ip
    )
    
    result = await db.execute(vote_query)
    return result.scalar_one_or_none()

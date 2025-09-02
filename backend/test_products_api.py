#!/usr/bin/env python3
"""
Test script to reproduce the Products API error locally
"""

import asyncio
import sys
import os
from decimal import Decimal

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select, func, asc, desc

from app.models import Product, ProductPrice, AffiliateStore, Brand, Category
from app.config import settings
from app.utils.vote_utils import get_multiple_products_vote_stats

async def test_products_query():
    """Test the exact query used in products API"""
    
    print("🔍 Testing Products API Query")
    print("=" * 50)
    
    # Use Azure database URL
    database_url = "postgresql://getyourmusicgear:arg-KDP8cjy.czu2zdv@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear"
    async_db_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    engine = create_async_engine(async_db_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            print("📊 Testing basic product query...")
            
            # Simulate the exact query from products API
            base_stmt = (
                select(Product)
                .options(selectinload(Product.brand), selectinload(Product.category))
                .where(Product.is_active.is_(True))
            )
            
            # Test sorting
            base_stmt = base_stmt.order_by(asc(Product.name))
            
            # Test pagination
            offset = 0
            limit = 3
            
            # Count query (this might be where the error occurs)
            print("📊 Testing count query...")
            count_stmt = select(func.count()).select_from(base_stmt.subquery())
            total = (await session.execute(count_stmt)).scalar_one()
            print(f"✅ Count query successful: {total} products")
            
            # Main query
            print("📊 Testing main query...")
            stmt = base_stmt.offset(offset).limit(limit)
            result = await session.execute(stmt)
            products = result.scalars().unique().all()
            print(f"✅ Main query successful: {len(products)} products fetched")
            
            # Test price queries
            print("📊 Testing price queries...")
            product_ids = [p.id for p in products]
            
            if product_ids:
                # Best prices query
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
                join_res = await session.execute(join_stmt)
                rows = join_res.scalars().all()
                print(f"✅ Price queries successful: {len(rows)} price records")
                
                # Test vote stats
                print("📊 Testing vote stats...")
                vote_stats_dict = await get_multiple_products_vote_stats(session, product_ids)
                print(f"✅ Vote stats successful: {len(vote_stats_dict)} vote records")
            
            # Test content access (potential JSONB issue)
            print("📊 Testing content field access...")
            for i, product in enumerate(products):
                print(f"Product {i+1}:")
                print(f"  - Name: {product.name}")
                print(f"  - Images type: {type(product.images)}")
                print(f"  - Content type: {type(product.content)}")
                
                # Test content access (this might cause the error)
                try:
                    content = product.content or {}
                    print(f"  - Content access: OK ({len(content)} keys)")
                    
                    # Test specifications access 
                    specs = content.get('specifications', {}) if content else {}
                    print(f"  - Specifications access: OK ({len(specs)} specs)")
                    
                except Exception as e:
                    print(f"  - ❌ Content access error: {e}")
                    
                # Test image access
                try:
                    images = product.images if product.images else {}
                    print(f"  - Images access: OK ({len(images)} images)")
                except Exception as e:
                    print(f"  - ❌ Images access error: {e}")
                    
                print()
            
            print("✅ All tests passed! Products API should work.")
            
        except Exception as e:
            print(f"❌ Error occurred: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_products_query())

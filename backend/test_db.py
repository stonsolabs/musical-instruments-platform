#!/usr/bin/env python3
"""
Simple database connection test script
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test_db_connection():
    """Test database connection"""
    # Get DATABASE_URL from environment
    database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/musical_instruments")
    
    # Ensure asyncpg is used
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    print(f"Testing connection to: {database_url}")
    
    try:
        # Create engine
        engine = create_async_engine(database_url, echo=True)
        
        # Test connection
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ Database connection successful! Test result: {row[0]}")
        
        await engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_db_connection())

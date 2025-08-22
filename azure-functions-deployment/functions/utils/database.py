import os
import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Create async engine
engine = None
AsyncSessionLocal = None

try:
    if DATABASE_URL:
        engine = create_async_engine(
            DATABASE_URL,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=10,
            max_overflow=20
        )
        
        AsyncSessionLocal = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        logger.info("Database engine created successfully")
    else:
        logger.warning("DATABASE_URL not provided")
        
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")

async def get_db_session() -> AsyncSession:
    """Get database session"""
    if not AsyncSessionLocal:
        raise Exception("Database not configured")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

async def test_database_connection():
    """Test database connection"""
    if not engine:
        raise Exception("Database engine not configured")
    
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        raise e

async def execute_query(query: str, params: dict = None):
    """Execute a query and return results"""
    if not engine:
        raise Exception("Database engine not configured")
    
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text(query), params or {})
            return result.fetchall()
    except Exception as e:
        logger.error(f"Query execution failed: {str(e)}")
        raise e

async def execute_scalar(query: str, params: dict = None):
    """Execute a query and return single value"""
    if not engine:
        raise Exception("Database engine not configured")
    
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text(query), params or {})
            return result.scalar()
    except Exception as e:
        logger.error(f"Scalar query execution failed: {str(e)}")
        raise e

# Synchronous wrapper for Azure Functions
def test_database_connection_sync():
    """Synchronous wrapper for database connection test"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test_database_connection())
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        raise e

def execute_query_sync(query: str, params: dict = None):
    """Synchronous wrapper for query execution"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(execute_query(query, params))
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Query execution failed: {str(e)}")
        raise e

def execute_scalar_sync(query: str, params: dict = None):
    """Synchronous wrapper for scalar query execution"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(execute_scalar(query, params))
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Scalar query execution failed: {str(e)}")
        raise e

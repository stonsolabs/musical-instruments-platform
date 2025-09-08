import asyncio
import os
from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/musical_instruments")

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Override with environment variable if available
env_database_url = os.getenv("DATABASE_URL")
if env_database_url:
    DATABASE_URL = env_database_url

# Convert to async URL if needed
async_database_url = DATABASE_URL
if async_database_url.startswith("postgresql://") and not async_database_url.startswith("postgresql+asyncpg://"):
    async_database_url = async_database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create async engine
async_engine = create_async_engine(async_database_url, echo=False)
async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Create sync engine for migrations
sync_engine = create_engine(DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://"), echo=False)

Base = declarative_base()

# Database models
class ProductsFilled(Base):
    __tablename__ = "products_filled"
    
    id = Column(Integer, primary_key=True)
    sku = Column(String(255), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    slug = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    images = Column(JSON, nullable=True)
    msrp_price = Column(Float, nullable=True)
    msrp_currency = Column(String(10), nullable=True)
    url = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Brand(Base):
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    logo_url = Column(Text, nullable=True)
    website_url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Locale(Base):
    __tablename__ = "locales"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    msrp_price = Column(Float, nullable=True)
    # msrp_currency moved to localized content per locale
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    images = Column(JSONB, default=dict)  # Product images (universal)
    content = Column(JSONB, default=dict)  # All content including specifications, localized content, metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Product identifiers - these are important for e-commerce and inventory management
    sku = Column(String(255), nullable=True, index=True)  # Stock Keeping Unit
    gtin12 = Column(String(12), nullable=True, index=True)  # Global Trade Item Number (UPC)
    gtin13 = Column(String(13), nullable=True, index=True)  # Global Trade Item Number (EAN)
    gtin14 = Column(String(14), nullable=True, index=True)  # Global Trade Item Number (ITF-14)
    upc = Column(String(12), nullable=True, index=True)  # Universal Product Code
    ean = Column(String(13), nullable=True, index=True)  # European Article Number
    mpn = Column(String(255), nullable=True, index=True)  # Manufacturer Part Number
    isbn = Column(String(13), nullable=True, index=True)  # International Standard Book Number (for music books)
    
    # Relationships
    brand = relationship("Brand", backref="products")
    category = relationship("Category", backref="products")

# Removed unnecessary tables:
# - ProductTranslation (replaced by products.content.localized_content)
# - AffiliateStore (replaced by products.content.store_links)
# - ProductStoreLink (replaced by products.content.store_links)
# - CustomerReview (replaced by products.content.localized_content[locale].customer_reviews)
# - ProductImage (replaced by products.images)

# Database session management
async def get_async_session() -> AsyncSession:
    """Get async database session"""
    async with async_session_maker() as session:
        return session

async def create_tables():
    """Create all tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    """Drop all tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Test database connection
async def test_connection():
    """Test database connection"""
    try:
        async with async_engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())

# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, Decimal, Boolean, DateTime, ForeignKey, JSON, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Brand(Base):
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    logo_url = Column(Text)
    website_url = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="brand")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(Text)
    image_url = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="category")
    parent = relationship("Category", remote_side=[id])

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    description = Column(Text)
    specifications = Column(JSON, default={})
    images = Column(ARRAY(Text), default=[])
    msrp_price = Column(Decimal(10, 2))
    ai_generated_content = Column(JSON, default={})
    avg_rating = Column(Decimal(3, 2), default=0)
    review_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    brand = relationship("Brand", back_populates="products")
    category = relationship("Category", back_populates="products")
    prices = relationship("ProductPrice", back_populates="product")

class AffiliateStore(Base):
    __tablename__ = "affiliate_stores"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    website_url = Column(Text, nullable=False)
    logo_url = Column(Text)
    commission_rate = Column(Decimal(5, 2))  # Percentage
    api_endpoint = Column(Text)
    api_key_encrypted = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    prices = relationship("ProductPrice", back_populates="store")

class ProductPrice(Base):
    __tablename__ = "product_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    store_id = Column(Integer, ForeignKey("affiliate_stores.id"), nullable=False, index=True)
    price = Column(Decimal(10, 2), nullable=False)
    currency = Column(String(3), default="EUR")
    affiliate_url = Column(Text, nullable=False)
    is_available = Column(Boolean, default=True, index=True)
    last_checked = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="prices")
    store = relationship("AffiliateStore", back_populates="prices")
    
    # Unique constraint to prevent duplicate prices for same product-store combination
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )

class ComparisonView(Base):
    __tablename__ = "comparison_views"
    
    id = Column(Integer, primary_key=True, index=True)
    product_ids = Column(ARRAY(Integer), nullable=False)
    user_ip = Column(String(45))
    user_country = Column(String(2), index=True)
    created_at = Column(DateTime, default=func.now(), index=True)

class AffiliateClick(Base):
    __tablename__ = "affiliate_clicks"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    store_id = Column(Integer, ForeignKey("affiliate_stores.id"), nullable=False, index=True)
    user_ip = Column(String(45))
    user_country = Column(String(2), index=True)
    referrer = Column(Text)
    created_at = Column(DateTime, default=func.now(), index=True)

# ========== PYDANTIC SCHEMAS ==========

# backend/app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class BrandBase(BaseModel):
    name: str
    slug: str
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    description: Optional[str] = None

class BrandResponse(BrandBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    slug: str
    parent_id: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    sku: str
    name: str
    slug: str
    brand_id: int
    category_id: int
    description: Optional[str] = None
    specifications: Dict[str, Any] = {}
    images: List[str] = []
    msrp_price: Optional[Decimal] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    avg_rating: Optional[Decimal] = 0
    review_count: int = 0
    is_active: bool
    created_at: datetime
    updated_at: datetime
    ai_generated_content: Dict[str, Any] = {}
    
    class Config:
        from_attributes = True

class ProductSummary(BaseModel):
    id: int
    name: str
    slug: str
    brand_name: str
    category_name: str
    best_price: Optional[Decimal] = None
    best_price_store: Optional[str] = None
    avg_rating: Optional[Decimal] = 0
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True

class AffiliateStoreBase(BaseModel):
    name: str
    slug: str
    website_url: str
    logo_url: Optional[str] = None
    commission_rate: Optional[Decimal] = None

class AffiliateStoreResponse(AffiliateStoreBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductPriceBase(BaseModel):
    product_id: int
    store_id: int
    price: Decimal
    currency: str = "EUR"
    affiliate_url: str
    is_available: bool = True

class ProductPriceResponse(ProductPriceBase):
    id: int
    last_checked: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class ComparisonRequest(BaseModel):
    product_ids: List[int] = Field(..., min_items=2, max_items=10)

class SearchFilters(BaseModel):
    q: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    sort_by: str = "name"
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)

# ========== DATABASE CONFIGURATION ==========

# backend/app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from .models import Base
from .config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
    autocommit=False,
)

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    """Dependency to get database session"""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# ========== CONFIGURATION ==========

# backend/app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/musical_instruments"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Musical Instruments API"
    
    # Environment
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # CORS
    ALLOWED_HOSTS: list = ["*"]
    
    # Affiliate Programs
    AMAZON_ASSOCIATE_TAG: str = ""
    THOMANN_AFFILIATE_ID: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# ========== REQUIREMENTS.txt ==========

# backend/requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.12.1
redis==5.0.1
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
openai==1.3.7
httpx==0.25.2
beautifulsoup4==4.12.2
lxml==4.9.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
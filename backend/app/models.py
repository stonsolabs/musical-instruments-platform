from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    Numeric,
    Float,
    ARRAY,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    products: Mapped[list["Product"]] = relationship(back_populates="brand")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("categories.id"))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    products: Mapped[list["Product"]] = relationship(back_populates="category")
    parent: Mapped[Category | None] = relationship(remote_side=[id])


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    brand_id: Mapped[int] = mapped_column(Integer, ForeignKey("brands.id"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    images: Mapped[dict] = mapped_column(JSON, default=dict)  # Universal images (separate for search)
    msrp_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    content: Mapped[dict] = mapped_column(JSON, default=dict)  # All AI-generated content (locales, models, artists, etc.)
    avg_rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), default=0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Product identifiers - these are important for e-commerce and inventory management
    gtin12: Mapped[str | None] = mapped_column(String(12), nullable=True, index=True)  # Global Trade Item Number (UPC)
    gtin13: Mapped[str | None] = mapped_column(String(13), nullable=True, index=True)  # Global Trade Item Number (EAN)
    gtin14: Mapped[str | None] = mapped_column(String(14), nullable=True, index=True)  # Global Trade Item Number (ITF-14)
    upc: Mapped[str | None] = mapped_column(String(12), nullable=True, index=True)  # Universal Product Code
    ean: Mapped[str | None] = mapped_column(String(13), nullable=True, index=True)  # European Article Number
    mpn: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)  # Manufacturer Part Number
    isbn: Mapped[str | None] = mapped_column(String(13), nullable=True, index=True)  # International Standard Book Number (for music books)

    # Crawler-specific fields
    category_attributes: Mapped[dict] = mapped_column(JSON, default=dict)
    last_crawled: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # OpenAI-specific fields
    openai_product_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    openai_processing_status: Mapped[str] = mapped_column(String(50), default='pending')  # pending, processing, completed, failed
    openai_batch_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    openai_processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    openai_error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    brand: Mapped["Brand"] = relationship(back_populates="products")
    category: Mapped["Category"] = relationship(back_populates="products")
    prices: Mapped[list["ProductPrice"]] = relationship(back_populates="product")


class AffiliateStore(Base):
    __tablename__ = "affiliate_stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    website_url: Mapped[str] = mapped_column(Text, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    commission_rate: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    api_endpoint: Mapped[str | None] = mapped_column(Text, nullable=True)
    api_key_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Affiliate program settings
    has_affiliate_program: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    affiliate_base_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    affiliate_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    domain_affiliate_ids: Mapped[dict] = mapped_column(JSON, default=dict)
    affiliate_parameters: Mapped[dict] = mapped_column(JSON, default=dict)
    show_affiliate_buttons: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    priority: Mapped[int] = mapped_column(Integer, default=0, index=True)
    
    # Regional settings
    available_regions: Mapped[List[str] | None] = mapped_column(ARRAY(String), nullable=True)
    primary_region: Mapped[str | None] = mapped_column(String(10), nullable=True)
    regional_priority: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Store fallback settings
    use_store_fallback: Mapped[bool] = mapped_column(Boolean, default=True)
    store_fallback_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    prices: Mapped[list["ProductPrice"]] = relationship(back_populates="store")
    brand_exclusivities: Mapped[list["BrandExclusivity"]] = relationship(back_populates="store")


class ProductPrice(Base):
    __tablename__ = "product_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    store_id: Mapped[int] = mapped_column(Integer, ForeignKey("affiliate_stores.id"), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    affiliate_url: Mapped[str] = mapped_column(Text, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    last_checked: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product: Mapped["Product"] = relationship(back_populates="prices")
    store: Mapped["AffiliateStore"] = relationship(back_populates="prices")

    # Unique constraint to prevent duplicate product-store price combinations
    __table_args__ = (UniqueConstraint('product_id', 'store_id', name='uq_product_store_price'),)


class ComparisonView(Base):
    __tablename__ = "comparison_views"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # ARRAY(Integer) is PostgreSQL specific; use JSON for portability if needed
    product_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    user_ip: Mapped[str | None] = mapped_column(String(45))
    user_country: Mapped[str | None] = mapped_column(String(2), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class AffiliateClick(Base):
    __tablename__ = "affiliate_clicks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    store_id: Mapped[int] = mapped_column(Integer, ForeignKey("affiliate_stores.id"), nullable=False, index=True)
    user_ip: Mapped[str | None] = mapped_column(String(45))
    user_country: Mapped[str | None] = mapped_column(String(2), index=True)
    referrer: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


# Crawler-specific models
class CrawlerSession(Base):
    __tablename__ = "crawler_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(50), default='running')  # running, completed, failed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CrawlerMetric(Base):
    __tablename__ = "crawler_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[str | None] = mapped_column(String(100), index=True)
    request_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    response_status: Mapped[int | None] = mapped_column(Integer, nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, default=False)
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CrawlerConfig(Base):
    __tablename__ = "crawler_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ProductsFilled(Base):
    __tablename__ = "products_filled"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    slug: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    images: Mapped[list | None] = mapped_column(JSON, nullable=True)
    msrp_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    msrp_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CrawlerJob(Base):
    __tablename__ = "crawler_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    job_type: Mapped[str] = mapped_column(String(100), nullable=False)
    parameters: Mapped[dict] = mapped_column(JSON, default=dict)
    priority: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(50), default='pending')  # pending, running, completed, failed
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


# OpenAI-specific models
class OpenAIBatch(Base):
    __tablename__ = "openai_batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    batch_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    product_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(50), default='pending')  # pending, processing, completed, failed
    openai_job_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    result_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    original_url: Mapped[str] = mapped_column(Text, nullable=False)
    azure_blob_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    azure_blob_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_type: Mapped[str] = mapped_column(String(50), default='product')  # product, gallery, thumbnail
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    processing_status: Mapped[str] = mapped_column(String(50), default='pending')  # pending, processing, completed, failed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    product: Mapped["Product"] = relationship("Product")


class BrandExclusivity(Base):
    __tablename__ = "brand_exclusivities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    brand_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    store_id: Mapped[int] = mapped_column(Integer, ForeignKey("affiliate_stores.id"), nullable=False, index=True)
    is_exclusive: Mapped[bool] = mapped_column(Boolean, default=True, index=True)  # True = exclusive, False = preferred
    regions: Mapped[List[str] | None] = mapped_column(ARRAY(String), nullable=True)  # ['US', 'EU', 'UK'] or null for all
    priority_boost: Mapped[int] = mapped_column(Integer, default=0)  # Additional priority for this brand-store combination
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    store: Mapped["AffiliateStore"] = relationship(back_populates="brand_exclusivities")

    # Unique constraint to prevent duplicate brand-store combinations
    __table_args__ = (UniqueConstraint('brand_name', 'store_id', name='uq_brand_store_exclusivity'),)


class ProductVote(Base):
    __tablename__ = "product_votes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    user_ip: Mapped[str] = mapped_column(String(45), nullable=False, index=True)  # IPv4/IPv6 address
    vote_type: Mapped[str] = mapped_column(String(10), nullable=False, index=True)  # 'up' or 'down'
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Note: No back_populates since we removed votes relationship from Product for better design

    # Unique constraint to prevent duplicate votes from same IP for same product
    __table_args__ = (UniqueConstraint('product_id', 'user_ip', name='uq_product_user_vote'),)



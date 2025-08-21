from __future__ import annotations

from datetime import datetime
from decimal import Decimal

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
    specifications: Mapped[dict] = mapped_column(JSON, default=dict)
    images: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list)
    msrp_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    ai_generated_content: Mapped[dict] = mapped_column(JSON, default=dict)
    avg_rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), default=0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

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

    prices: Mapped[list["ProductPrice"]] = relationship(back_populates="store")


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

    product: Mapped["Product"] = relationship(back_populates="prices")
    store: Mapped["AffiliateStore"] = relationship(back_populates="prices")


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



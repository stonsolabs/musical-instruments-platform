from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


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
    images: Dict[str, Any] = {}  # Universal images (separate for search)
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
    content: Dict[str, Any] = {}  # All AI-generated content (locales, models, artists, etc.)

    class Config:
        from_attributes = True


class ProductSummary(BaseModel):
    id: int
    name: str
    slug: str
    brand_name: str
    category_name: str
    avg_rating: Optional[Decimal] = 0
    image_url: Optional[str] = None


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


class ProductPriceStore(BaseModel):
    id: int
    name: str
    logo_url: Optional[str] = None
    website_url: str


class ProductPriceResponse(ProductPriceBase):
    id: int
    last_checked: datetime
    created_at: datetime
    store: ProductPriceStore | None = None

    class Config:
        from_attributes = True


class SearchFilters(BaseModel):
    q: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    sort_by: str = "name"
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)


class SearchResponse(BaseModel):
    products: List[Dict[str, Any]]
    pagination: Dict[str, int]
    filters_applied: Dict[str, Any]


class ComparisonResponse(BaseModel):
    products: List[Dict[str, Any]]
    common_specs: List[str]
    comparison_matrix: Dict[str, Dict[str, Any]]
    generated_at: str


class VoteRequest(BaseModel):
    vote_type: str = Field(..., pattern="^(up|down)$", description="Vote type: 'up' or 'down'")


class VoteResponse(BaseModel):
    success: bool
    message: str
    vote_counts: Dict[str, int]
    user_vote: Optional[str] = None


class ProductVoteStats(BaseModel):
    thumbs_up_count: int
    thumbs_down_count: int
    total_votes: int
    vote_score: int
    user_vote: Optional[str] = None



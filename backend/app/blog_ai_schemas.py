"""
Pydantic models for AI-enhanced blog system
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TemplateType(str, Enum):
    GENERAL = "general"
    BUYING_GUIDE = "buying_guide"
    REVIEW = "review"
    COMPARISON = "comparison"
    TUTORIAL = "tutorial"
    HISTORY = "history"
    QUIZ = "quiz"
    NEW_RELEASE = "new_release"
    ARTIST_SPOTLIGHT = "artist_spotlight"

class GenerationStatus(str, Enum):
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AIProvider(str, Enum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"
    PERPLEXITY = "perplexity"

class BlogGenerationTemplate(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category_id: Optional[int]
    template_type: TemplateType
    base_prompt: str
    system_prompt: Optional[str]
    product_context_prompt: Optional[str]
    required_product_types: List[str] = []
    min_products: int = 0
    max_products: int = 10
    suggested_tags: List[str] = []
    seo_title_template: Optional[str]
    seo_description_template: Optional[str]
    content_structure: Dict[str, Any] = {}
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BlogGenerationTemplateCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    category_id: Optional[int] = None
    template_type: TemplateType = TemplateType.GENERAL
    base_prompt: str = Field(..., min_length=10)
    system_prompt: Optional[str] = None
    product_context_prompt: Optional[str] = None
    required_product_types: List[str] = []
    min_products: int = Field(0, ge=0, le=50)
    max_products: int = Field(10, ge=1, le=50)
    suggested_tags: List[str] = []
    seo_title_template: Optional[str] = Field(None, max_length=255)
    seo_description_template: Optional[str] = None
    content_structure: Dict[str, Any] = {}
    is_active: bool = True

    @validator('max_products')
    def max_products_must_be_greater_than_min(cls, v, values):
        if 'min_products' in values and v < values['min_products']:
            raise ValueError('max_products must be greater than or equal to min_products')
        return v

class BlogGenerationHistory(BaseModel):
    id: int
    blog_post_id: int
    template_id: Optional[int]
    generation_status: GenerationStatus
    prompt_used: Optional[str]
    model_used: Optional[str]
    tokens_used: Optional[int]
    generation_time_ms: Optional[int]
    error_message: Optional[str]
    generation_metadata: Dict[str, Any] = {}
    created_at: datetime
    
    class Config:
        from_attributes = True

class EnhancedBlogPostProduct(BaseModel):
    id: int
    product_id: int
    position: int
    context: Optional[str]
    ai_context: Optional[str]  # AI's reasoning for including this product
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    mentioned_in_sections: List[str] = []
    product_name: Optional[str]
    product_slug: Optional[str]
    product_brand: Optional[str]
    
    class Config:
        from_attributes = True

class BlogContentSection(BaseModel):
    id: int
    blog_post_id: int
    section_type: str
    section_title: Optional[str]
    section_content: str
    section_order: int = 0
    products_featured: List[int] = []
    ai_generated: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True

class BlogContentSectionCreate(BaseModel):
    section_type: str = Field(..., max_length=100)
    section_title: Optional[str] = Field(None, max_length=255)
    section_content: str = Field(..., min_length=1)
    section_order: int = Field(0, ge=0)
    products_featured: List[int] = []
    ai_generated: bool = False

class AIBlogPost(BaseModel):
    """Extended blog post model with AI generation fields"""
    id: int
    title: str
    slug: str
    excerpt: Optional[str]
    content: str
    featured_image: Optional[str]
    category_id: Optional[int]
    author_name: str
    status: str
    seo_title: Optional[str]
    seo_description: Optional[str]
    reading_time: Optional[int]
    view_count: int
    featured: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    # AI-specific fields
    generated_by_ai: bool = False
    generation_prompt: Optional[str]
    generation_model: Optional[str]
    generation_params: Dict[str, Any] = {}
    ai_notes: Optional[str]
    
    # Related data
    products: List[EnhancedBlogPostProduct] = []
    sections: List[BlogContentSection] = []
    generation_history: List[BlogGenerationHistory] = []
    
    class Config:
        from_attributes = True

class BlogGenerationRequest(BaseModel):
    template_id: int
    title: Optional[str] = None
    category_id: Optional[int] = None
    product_ids: List[int] = []
    custom_prompt_additions: Optional[str] = None
    target_word_count: int = Field(800, ge=300, le=3000)
    include_seo_optimization: bool = True
    auto_publish: bool = False
    generation_params: Dict[str, Any] = {}
    provider: AIProvider = AIProvider.OPENAI

class CloneRewriteRequest(BaseModel):
    source_url: str
    title: Optional[str] = None
    category_id: Optional[int] = None
    product_ids: List[int] = []
    custom_instructions: Optional[str] = None
    target_word_count: int = Field(800, ge=300, le=3000)
    include_seo_optimization: bool = True
    auto_publish: bool = False
    generation_params: Dict[str, Any] = {}
    provider: AIProvider = AIProvider.OPENAI

class ProductSelectionCriteria(BaseModel):
    """Criteria for AI to select relevant products"""
    categories: List[str] = []
    min_rating: float = Field(0.0, ge=0.0, le=5.0)
    max_price: Optional[float] = Field(None, gt=0)
    min_price: Optional[float] = Field(None, gt=0)
    brands: List[str] = []
    exclude_product_ids: List[int] = []
    require_availability: bool = True
    
class AIProductRecommendation(BaseModel):
    """AI recommendation for including a product"""
    product_id: int
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    suggested_context: str
    suggested_sections: List[str] = []
    
class BlogGenerationResult(BaseModel):
    """Result of AI blog generation"""
    success: bool
    blog_post_id: Optional[int] = None
    generation_history_id: Optional[int] = None
    generated_content: Optional[str] = None
    generated_title: Optional[str] = None
    generated_excerpt: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    suggested_products: List[AIProductRecommendation] = []
    sections: List[BlogContentSectionCreate] = []
    tokens_used: Optional[int] = None
    generation_time_ms: Optional[int] = None
    error_message: Optional[str] = None
    warnings: List[str] = []

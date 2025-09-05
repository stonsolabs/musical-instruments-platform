"""
API endpoints for blog system
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import logging
import re

from app.database import get_db
from app.api.dependencies import get_api_key

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic models
class BlogCategory(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    sort_order: int
    is_active: bool
    
    class Config:
        from_attributes = True

class BlogTag(BaseModel):
    id: int
    name: str
    slug: str
    
    class Config:
        from_attributes = True

class BlogPostProduct(BaseModel):
    id: int
    product_id: int
    position: int
    context: Optional[str]
    product_name: Optional[str]
    product_slug: Optional[str]
    product_brand: Optional[str]
    
    class Config:
        from_attributes = True

class BlogPost(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str]
    content: str
    featured_image: Optional[str]
    category: Optional[BlogCategory]
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
    tags: List[BlogTag] = []
    products: List[BlogPostProduct] = []
    
    class Config:
        from_attributes = True

class BlogPostSummary(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str]
    featured_image: Optional[str]
    category: Optional[BlogCategory]
    author_name: str
    reading_time: Optional[int]
    view_count: int
    featured: bool
    published_at: Optional[datetime]
    tags: List[BlogTag] = []
    
    class Config:
        from_attributes = True

class BlogPostCreate(BaseModel):
    title: str = Field(..., max_length=255)
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    content: str = Field(...)
    featured_image: Optional[str] = None
    category_id: int
    author_name: str = Field(default="GetYourMusicGear Team", max_length=100)
    author_email: Optional[str] = None
    status: str = Field(default="draft", regex="^(draft|published|archived)$")
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    featured: bool = False
    tag_names: List[str] = []
    product_ids: List[int] = []

def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug.strip('-')

def estimate_reading_time(content: str) -> int:
    """Estimate reading time in minutes (assuming 200 words per minute)"""
    word_count = len(content.split())
    reading_time = max(1, round(word_count / 200))
    return reading_time

@router.get("/blog/categories", response_model=List[BlogCategory])
async def get_blog_categories(
    db: AsyncSession = Depends(get_db)
):
    """Get all blog categories"""
    
    try:
        query = """
        SELECT id, name, slug, description, icon, color, sort_order, is_active
        FROM blog_categories
        WHERE is_active = true
        ORDER BY sort_order, name
        """
        
        result = await db.execute(text(query))
        categories = result.fetchall()
        
        return [
            BlogCategory(
                id=row[0],
                name=row[1], 
                slug=row[2],
                description=row[3],
                icon=row[4],
                color=row[5],
                sort_order=row[6],
                is_active=row[7]
            )
            for row in categories
        ]
        
    except Exception as e:
        logger.error(f"Failed to fetch blog categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch blog categories")

@router.get("/blog/posts", response_model=List[BlogPostSummary])
async def get_blog_posts(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    featured: Optional[bool] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """Get blog posts with filtering and pagination"""
    
    try:
        where_clauses = ["bp.status = 'published'"]
        params = {}
        
        if category:
            where_clauses.append("bc.slug = :category")
            params['category'] = category
            
        if tag:
            where_clauses.append("EXISTS (SELECT 1 FROM blog_post_tags bpt JOIN blog_tags bt ON bpt.tag_id = bt.id WHERE bpt.blog_post_id = bp.id AND bt.slug = :tag)")
            params['tag'] = tag
            
        if featured is not None:
            where_clauses.append("bp.featured = :featured")
            params['featured'] = featured
        
        where_clause = "WHERE " + " AND ".join(where_clauses)
        
        query = f"""
        SELECT 
            bp.id, bp.title, bp.slug, bp.excerpt, bp.featured_image,
            bp.author_name, bp.reading_time, bp.view_count, bp.featured,
            bp.published_at,
            bc.id as category_id, bc.name as category_name, bc.slug as category_slug,
            bc.description as category_description, bc.icon as category_icon, 
            bc.color as category_color, bc.sort_order as category_sort_order,
            bc.is_active as category_is_active
        FROM blog_posts bp
        LEFT JOIN blog_categories bc ON bp.category_id = bc.id
        {where_clause}
        ORDER BY bp.featured DESC, bp.published_at DESC, bp.created_at DESC
        LIMIT :limit OFFSET :offset
        """
        
        params.update({'limit': limit, 'offset': offset})
        
        result = await db.execute(text(query), params)
        posts = result.fetchall()
        
        # Get tags for each post
        post_ids = [post[0] for post in posts]
        tags_query = """
        SELECT bpt.blog_post_id, bt.id, bt.name, bt.slug
        FROM blog_post_tags bpt
        JOIN blog_tags bt ON bpt.tag_id = bt.id
        WHERE bpt.blog_post_id = ANY(:post_ids)
        ORDER BY bt.name
        """
        
        if post_ids:
            tags_result = await db.execute(text(tags_query), {'post_ids': post_ids})
            tags_data = tags_result.fetchall()
            
            # Group tags by post_id
            tags_by_post = {}
            for tag_row in tags_data:
                post_id = tag_row[0]
                if post_id not in tags_by_post:
                    tags_by_post[post_id] = []
                tags_by_post[post_id].append(BlogTag(id=tag_row[1], name=tag_row[2], slug=tag_row[3]))
        else:
            tags_by_post = {}
        
        return [
            BlogPostSummary(
                id=row[0],
                title=row[1],
                slug=row[2], 
                excerpt=row[3],
                featured_image=row[4],
                author_name=row[5],
                reading_time=row[6],
                view_count=row[7],
                featured=row[8],
                published_at=row[9],
                category=BlogCategory(
                    id=row[10],
                    name=row[11],
                    slug=row[12],
                    description=row[13],
                    icon=row[14],
                    color=row[15],
                    sort_order=row[16],
                    is_active=row[17]
                ) if row[10] else None,
                tags=tags_by_post.get(row[0], [])
            )
            for row in posts
        ]
        
    except Exception as e:
        logger.error(f"Failed to fetch blog posts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch blog posts")

@router.get("/blog/posts/{slug}", response_model=BlogPost)
async def get_blog_post(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a single blog post by slug"""
    
    try:
        # Get the main post data
        query = """
        SELECT 
            bp.id, bp.title, bp.slug, bp.excerpt, bp.content, bp.featured_image,
            bp.author_name, bp.status, bp.seo_title, bp.seo_description,
            bp.reading_time, bp.view_count, bp.featured, bp.published_at,
            bp.created_at, bp.updated_at,
            bc.id as category_id, bc.name as category_name, bc.slug as category_slug,
            bc.description as category_description, bc.icon as category_icon, 
            bc.color as category_color, bc.sort_order as category_sort_order,
            bc.is_active as category_is_active
        FROM blog_posts bp
        LEFT JOIN blog_categories bc ON bp.category_id = bc.id
        WHERE bp.slug = :slug AND bp.status = 'published'
        """
        
        result = await db.execute(text(query), {'slug': slug})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        post_id = row[0]
        
        # Get tags
        tags_query = """
        SELECT bt.id, bt.name, bt.slug
        FROM blog_post_tags bpt
        JOIN blog_tags bt ON bpt.tag_id = bt.id
        WHERE bpt.blog_post_id = :post_id
        ORDER BY bt.name
        """
        
        tags_result = await db.execute(text(tags_query), {'post_id': post_id})
        tags_data = tags_result.fetchall()
        tags = [BlogTag(id=tag[0], name=tag[1], slug=tag[2]) for tag in tags_data]
        
        # Get associated products
        products_query = """
        SELECT 
            bpp.id, bpp.product_id, bpp.position, bpp.context,
            p.name as product_name, p.slug as product_slug,
            b.name as brand_name
        FROM blog_post_products bpp
        LEFT JOIN products p ON bpp.product_id = p.id
        LEFT JOIN brands b ON p.brand_id = b.id
        WHERE bpp.blog_post_id = :post_id
        ORDER BY bpp.position, bpp.id
        """
        
        products_result = await db.execute(text(products_query), {'post_id': post_id})
        products_data = products_result.fetchall()
        products = [
            BlogPostProduct(
                id=prod[0],
                product_id=prod[1],
                position=prod[2],
                context=prod[3],
                product_name=prod[4],
                product_slug=prod[5],
                product_brand=prod[6]
            )
            for prod in products_data
        ]
        
        # Update view count
        await db.execute(text("UPDATE blog_posts SET view_count = view_count + 1 WHERE id = :post_id"), {'post_id': post_id})
        await db.commit()
        
        return BlogPost(
            id=row[0],
            title=row[1],
            slug=row[2],
            excerpt=row[3],
            content=row[4],
            featured_image=row[5],
            author_name=row[6],
            status=row[7],
            seo_title=row[8],
            seo_description=row[9],
            reading_time=row[10],
            view_count=row[11] + 1,  # +1 for the current view
            featured=row[12],
            published_at=row[13],
            created_at=row[14],
            updated_at=row[15],
            category=BlogCategory(
                id=row[16],
                name=row[17],
                slug=row[18],
                description=row[19],
                icon=row[20],
                color=row[21],
                sort_order=row[22],
                is_active=row[23]
            ) if row[16] else None,
            tags=tags,
            products=products
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch blog post {slug}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch blog post")

@router.post("/blog/posts", response_model=dict)
async def create_blog_post(
    post_data: BlogPostCreate,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Create a new blog post (admin only)"""
    
    try:
        # Generate slug if not provided
        slug = post_data.slug or generate_slug(post_data.title)
        
        # Estimate reading time
        reading_time = estimate_reading_time(post_data.content)
        
        # Insert blog post
        insert_query = """
        INSERT INTO blog_posts (
            title, slug, excerpt, content, featured_image, category_id,
            author_name, author_email, status, seo_title, seo_description,
            reading_time, featured, published_at
        ) VALUES (
            :title, :slug, :excerpt, :content, :featured_image, :category_id,
            :author_name, :author_email, :status, :seo_title, :seo_description,
            :reading_time, :featured, :published_at
        ) RETURNING id
        """
        
        published_at = datetime.utcnow() if post_data.status == 'published' else None
        
        result = await db.execute(text(insert_query), {
            'title': post_data.title,
            'slug': slug,
            'excerpt': post_data.excerpt,
            'content': post_data.content,
            'featured_image': post_data.featured_image,
            'category_id': post_data.category_id,
            'author_name': post_data.author_name,
            'author_email': post_data.author_email,
            'status': post_data.status,
            'seo_title': post_data.seo_title or post_data.title,
            'seo_description': post_data.seo_description,
            'reading_time': reading_time,
            'featured': post_data.featured,
            'published_at': published_at
        })
        
        post_id = result.scalar()
        
        # Add tags
        for tag_name in post_data.tag_names:
            tag_slug = generate_slug(tag_name)
            
            # Insert or get tag
            tag_query = """
            INSERT INTO blog_tags (name, slug) 
            VALUES (:name, :slug)
            ON CONFLICT (slug) DO UPDATE SET name = :name
            RETURNING id
            """
            
            tag_result = await db.execute(text(tag_query), {'name': tag_name, 'slug': tag_slug})
            tag_id = tag_result.scalar()
            
            # Link tag to post
            await db.execute(text("""
                INSERT INTO blog_post_tags (blog_post_id, tag_id) 
                VALUES (:post_id, :tag_id)
                ON CONFLICT DO NOTHING
            """), {'post_id': post_id, 'tag_id': tag_id})
        
        # Add product associations
        for i, product_id in enumerate(post_data.product_ids):
            await db.execute(text("""
                INSERT INTO blog_post_products (blog_post_id, product_id, position, context)
                VALUES (:post_id, :product_id, :position, :context)
                ON CONFLICT DO NOTHING
            """), {
                'post_id': post_id,
                'product_id': product_id,
                'position': i,
                'context': 'featured'
            })
        
        await db.commit()
        
        logger.info(f"Created blog post {post_id}: {post_data.title}")
        
        return {
            "id": post_id,
            "slug": slug,
            "message": "Blog post created successfully"
        }
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create blog post: {e}")
        raise HTTPException(status_code=500, detail="Failed to create blog post")

@router.get("/blog/search")
async def search_blog_posts(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Search blog posts by title and content"""
    
    try:
        query = """
        SELECT 
            bp.id, bp.title, bp.slug, bp.excerpt, bp.featured_image,
            bp.author_name, bp.reading_time, bp.published_at,
            bc.name as category_name, bc.slug as category_slug,
            bc.color as category_color
        FROM blog_posts bp
        LEFT JOIN blog_categories bc ON bp.category_id = bc.id
        WHERE bp.status = 'published' 
        AND (
            bp.title ILIKE :search_term 
            OR bp.excerpt ILIKE :search_term 
            OR bp.content ILIKE :search_term
        )
        ORDER BY bp.featured DESC, bp.published_at DESC
        LIMIT :limit
        """
        
        search_term = f"%{q}%"
        result = await db.execute(text(query), {'search_term': search_term, 'limit': limit})
        posts = result.fetchall()
        
        return {
            "query": q,
            "results": [
                {
                    "id": row[0],
                    "title": row[1],
                    "slug": row[2],
                    "excerpt": row[3],
                    "featured_image": row[4],
                    "author_name": row[5],
                    "reading_time": row[6],
                    "published_at": row[7],
                    "category": {
                        "name": row[8],
                        "slug": row[9],
                        "color": row[10]
                    } if row[8] else None
                }
                for row in posts
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to search blog posts: {e}")
        raise HTTPException(status_code=500, detail="Failed to search blog posts")
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
import json

from app.database import get_db
from app.api.dependencies import get_api_key, require_admin, optional_admin
from app.blog_ai_schemas import (
    BlogGenerationTemplate, BlogGenerationTemplateCreate, BlogGenerationRequest,
    BlogGenerationResult, AIBlogPost, BlogGenerationHistory, EnhancedBlogPostProduct,
    BlogContentSection
)
from app.services.simple_blog_generator import SimpleBlogGenerator

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
    structured_content: Optional[dict] = None
    featured_image: Optional[str]
    category: Optional[BlogCategory]
    author_name: str
    status: str
    seo_title: Optional[str]
    seo_description: Optional[str]
    reading_time: Optional[int]
    view_count: int
    featured: bool
    noindex: bool = False
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
    status: str = Field(default="draft", pattern="^(draft|published|archived)$")
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
    sort_by: Optional[str] = Query(None, description="Optional sort: 'views' for most read, otherwise latest"),
    db: AsyncSession = Depends(get_db)
):
    """Get blog posts with filtering and pagination"""
    
    try:
        where_clauses = ["bp.status = 'published'"]
        params = {}
        
        if category:
            where_clauses.append("COALESCE(bp.content_json->>'category', 'general') = :category")
            params['category'] = category
            
        if tag:
            where_clauses.append("bp.content_json->'tags' ? :tag")
            params['tag'] = tag
            
        if featured is not None:
            # featured column doesn't exist in simplified table, use default false
            where_clauses.append("false = :featured")
            params['featured'] = featured
        
        where_clause = "WHERE " + " AND ".join(where_clauses)
        
        order_clause = "ORDER BY bp.published_at DESC, bp.created_at DESC"
        if sort_by == 'views':
            order_clause = "ORDER BY bp.published_at DESC, bp.created_at DESC"

        query = f"""
        SELECT 
            bp.id, bp.title, bp.slug, bp.excerpt, bp.featured_image,
            bp.author_name, 
            COALESCE((bp.content_json->>'word_count')::int / 200, 5) as reading_time,
            0 as view_count,
            false as featured,
            bp.published_at,
            -- Create category object from content_json
            NULL as category_id,
            COALESCE(bp.content_json->>'category', 'general') as category_name,
            COALESCE(bp.content_json->>'category', 'general') as category_slug,
            'General content category' as category_description,
            '📝' as category_icon,
            '#6366f1' as category_color,
            1 as category_sort_order,
            true as category_is_active
        FROM blog_posts bp
        {where_clause}
        {order_clause}
        LIMIT :limit OFFSET :offset
        """
        
        params.update({'limit': limit, 'offset': offset})
        
        result = await db.execute(text(query), params)
        posts = result.fetchall()
        
        # Get tags from content_json for each post
        post_ids = [post[0] for post in posts]
        
        if post_ids:
            # Get content_json for all posts to extract tags
            tags_query = """
            SELECT id, content_json->'tags' as tags_json
            FROM blog_posts 
            WHERE id = ANY(:post_ids)
            """
            tags_result = await db.execute(text(tags_query), {'post_ids': post_ids})
            tags_data = tags_result.fetchall()
            
            # Build tags for each post from JSON
            tags_by_post = {}
            for post_id, tags_json in tags_data:
                tags_by_post[post_id] = []
                if tags_json:
                    import json
                    tag_names = json.loads(tags_json) if isinstance(tags_json, str) else tags_json
                    if isinstance(tag_names, list):
                        for i, tag_name in enumerate(tag_names):
                            # Create slug from tag name
                            import re
                            tag_slug = re.sub(r'[^a-zA-Z0-9\s-]', '', tag_name.lower())
                            tag_slug = re.sub(r'\s+', '-', tag_slug).strip('-')
                            tags_by_post[post_id].append(BlogTag(id=i+1, name=tag_name, slug=tag_slug))
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

@router.get("/blog/tags/popular", response_model=List[BlogTag])
async def get_popular_tags(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get most-used tags across published posts"""
    try:
        query = """
        SELECT bt.id, bt.name, bt.slug, COUNT(*) as usage
        FROM blog_post_tags bpt
        JOIN blog_tags bt ON bpt.tag_id = bt.id
        JOIN blog_posts bp ON bpt.blog_post_id = bp.id
        WHERE bp.status = 'published'
        GROUP BY bt.id, bt.name, bt.slug
        ORDER BY usage DESC
        LIMIT :limit
        """
        result = await db.execute(text(query), {"limit": limit})
        rows = result.fetchall()
        return [BlogTag(id=r[0], name=r[1], slug=r[2]) for r in rows]
    except Exception as e:
        logger.error(f"Failed to fetch popular tags: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch popular tags")

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
            bp.id, bp.title, bp.slug, bp.excerpt, bp.content, bp.structured_content, bp.featured_image,
            bp.author_name, bp.status, bp.seo_title, bp.seo_description,
            bp.reading_time, bp.view_count, bp.featured, bp.published_at,
            bp.created_at, bp.updated_at,
            bp.noindex,
            bc.id as category_id, bc.name as category_name, bc.slug as category_slug,
            bc.description as category_description, bc.icon as category_icon, 
            bc.color as category_color, bc.sort_order as category_sort_order,
            bc.is_active as category_is_active
        FROM blog_posts bp
        LEFT JOIN blog_categories bc ON bp.category_id = bc.id
        WHERE bp.slug = :slug AND bp.status IN ('published', 'draft')
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
        
        # Parse structured_content if it's a JSON string
        structured_content = row[5]
        if isinstance(structured_content, str):
            try:
                structured_content = json.loads(structured_content)
            except (json.JSONDecodeError, TypeError):
                structured_content = None
        
        return BlogPost(
            id=row[0],
            title=row[1],
            slug=row[2],
            excerpt=row[3],
            content=row[4],
            structured_content=structured_content,
            featured_image=row[6],
            author_name=row[7],
            status=row[8],
            seo_title=row[9],
            seo_description=row[10],
            reading_time=row[11],
            view_count=row[12] + 1,  # +1 for the current view
            featured=row[13],
            published_at=row[14],
            created_at=row[15],
            updated_at=row[16],
            noindex=row[17] or False,
            category=BlogCategory(
                id=row[18],
                name=row[19],
                slug=row[20],
                description=row[21],
                icon=row[22],
                color=row[23],
                sort_order=row[24],
                is_active=row[25]
            ) if row[18] else None,
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
    admin: dict = Depends(require_admin)
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

# === AI GENERATION ENDPOINTS ===

@router.get("/blog/templates", response_model=List[BlogGenerationTemplate])
async def get_blog_generation_templates(
    template_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get blog generation templates"""
    
    try:
        where_clauses = ["is_active = true"]
        params = {}
        
        if template_type:
            where_clauses.append("template_type = :template_type")
            params['template_type'] = template_type
        
        where_clause = "WHERE " + " AND ".join(where_clauses)
        
        query = f"""
        SELECT id, name, description, category_id, template_type, base_prompt,
               system_prompt, product_context_prompt, required_product_types,
               min_products, max_products, suggested_tags, seo_title_template,
               seo_description_template, content_structure, is_active,
               created_at, updated_at
        FROM blog_generation_templates
        {where_clause}
        ORDER BY template_type, name
        """
        
        result = await db.execute(text(query), params)
        templates = result.fetchall()
        
        return [
            BlogGenerationTemplate(
                id=row[0],
                name=row[1],
                description=row[2],
                category_id=row[3],
                template_type=row[4],
                base_prompt=row[5],
                system_prompt=row[6],
                product_context_prompt=row[7],
                required_product_types=row[8] or [],
                min_products=row[9],
                max_products=row[10],
                suggested_tags=row[11] or [],
                seo_title_template=row[12],
                seo_description_template=row[13],
                content_structure=row[14] or {},
                is_active=row[15],
                created_at=row[16],
                updated_at=row[17]
            )
            for row in templates
        ]
        
    except Exception as e:
        logger.error(f"Failed to fetch blog generation templates: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch templates")

@router.post("/blog/templates", response_model=dict)
async def create_blog_generation_template(
    template_data: BlogGenerationTemplateCreate,
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Create a new blog generation template (admin only)"""
    
    try:
        insert_query = """
        INSERT INTO blog_generation_templates (
            name, description, category_id, template_type, base_prompt,
            system_prompt, product_context_prompt, required_product_types,
            min_products, max_products, suggested_tags, seo_title_template,
            seo_description_template, content_structure, is_active
        ) VALUES (
            :name, :description, :category_id, :template_type, :base_prompt,
            :system_prompt, :product_context_prompt, :required_product_types,
            :min_products, :max_products, :suggested_tags, :seo_title_template,
            :seo_description_template, :content_structure, :is_active
        ) RETURNING id
        """
        
        result = await db.execute(text(insert_query), {
            'name': template_data.name,
            'description': template_data.description,
            'category_id': template_data.category_id,
            'template_type': template_data.template_type,
            'base_prompt': template_data.base_prompt,
            'system_prompt': template_data.system_prompt,
            'product_context_prompt': template_data.product_context_prompt,
            'required_product_types': json.dumps(template_data.required_product_types),
            'min_products': template_data.min_products,
            'max_products': template_data.max_products,
            'suggested_tags': json.dumps(template_data.suggested_tags),
            'seo_title_template': template_data.seo_title_template,
            'seo_description_template': template_data.seo_description_template,
            'content_structure': json.dumps(template_data.content_structure),
            'is_active': template_data.is_active
        })
        
        template_id = result.scalar()
        await db.commit()
        
        logger.info(f"Created blog generation template {template_id}: {template_data.name}")
        
        return {
            "id": template_id,
            "message": "Blog generation template created successfully"
        }
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create blog generation template: {e}")
        raise HTTPException(status_code=500, detail="Failed to create template")

@router.post("/blog/generate", response_model=BlogGenerationResult)
async def generate_blog_post(
    request: BlogGenerationRequest,
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Generate a blog post using AI (admin only)"""
    
    try:
        # Get OpenAI API key from environment
        import os
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
        # Initialize AI generator
        import openai
        openai_client = openai.AsyncClient(api_key=openai_api_key)
        ai_generator = SimpleBlogGenerator(openai_client)
        
        # Generate blog post
        blog_content = ai_generator.generate_blog_post(
            topic=request.topic,
            template_name=getattr(request, 'template_name', 'buying-guide'),
            products=getattr(request, 'products', []),
            target_words=getattr(request, 'target_words', 4000)
        )
        
        # Save to database using simplified structure
        from sqlalchemy import text
        insert_query = """
        INSERT INTO blog_posts (title, slug, excerpt, seo_title, seo_description, content_json, 
                               author_name, category, tags, featured_products, published_at, created_at, updated_at)
        VALUES (:title, :slug, :excerpt, :seo_title, :seo_description, :content_json, 
                :author_name, :category, :tags, :featured_products, NOW(), NOW(), NOW())
        RETURNING id
        """
        
        # Generate slug from title
        import re
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', blog_content['title'].lower())
        slug = re.sub(r'\s+', '-', slug).strip('-')
        
        values = {
            'title': blog_content['title'],
            'slug': slug,
            'excerpt': blog_content.get('excerpt', ''),
            'seo_title': blog_content.get('seo_title', blog_content['title']),
            'seo_description': blog_content.get('seo_description', ''),
            'content_json': json.dumps(blog_content),
            'author_name': 'GetYourMusicGear Team',
            'category': blog_content.get('category', 'general'),
            'tags': json.dumps(blog_content.get('tags', [])),
            'featured_products': json.dumps(blog_content.get('featured_products', []))
        }
        
        result = await db.execute(text(insert_query), values)
        blog_post_id = result.fetchone()[0]
        await db.commit()
        
        logger.info(f"Generated and saved AI blog post {blog_post_id}")
        
        # Return result in expected format
        from app.blog_ai_schemas import BlogGenerationResult
        return BlogGenerationResult(
            success=True,
            blog_post_id=blog_post_id,
            title=blog_content['title'],
            slug=slug,
            content=blog_content,
            error_message=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate blog post: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate blog post")

@router.get("/blog/generation-history", response_model=List[BlogGenerationHistory])
async def get_generation_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """Get blog generation history (admin only)"""
    
    try:
        where_clauses = []
        params = {'limit': limit, 'offset': offset}
        
        if status:
            where_clauses.append("generation_status = :status")
            params['status'] = status
        
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        query = f"""
        SELECT id, blog_post_id, template_id, generation_status, prompt_used,
               model_used, tokens_used, generation_time_ms, error_message,
               generation_metadata, created_at
        FROM blog_generation_history
        {where_clause}
        ORDER BY created_at DESC
        LIMIT :limit OFFSET :offset
        """
        
        result = await db.execute(text(query), params)
        history = result.fetchall()
        
        return [
            BlogGenerationHistory(
                id=row[0],
                blog_post_id=row[1],
                template_id=row[2],
                generation_status=row[3],
                prompt_used=row[4],
                model_used=row[5],
                tokens_used=row[6],
                generation_time_ms=row[7],
                error_message=row[8],
                generation_metadata=row[9] or {},
                created_at=row[10]
            )
            for row in history
        ]
        
    except Exception as e:
        logger.error(f"Failed to fetch generation history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch generation history")

@router.get("/blog/ai-posts/{post_id}", response_model=AIBlogPost)
async def get_ai_blog_post(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get AI-generated blog post with enhanced details"""
    
    try:
        # Get the main post data with AI fields
        query = """
        SELECT 
            bp.id, bp.title, bp.slug, bp.excerpt, bp.content, bp.structured_content, bp.featured_image,
            bp.author_name, bp.status, bp.seo_title, bp.seo_description,
            bp.reading_time, bp.view_count, bp.featured, bp.published_at,
            bp.created_at, bp.updated_at, bp.category_id,
            bp.generated_by_ai, bp.generation_prompt, bp.generation_model,
            bp.generation_params, bp.ai_notes
        FROM blog_posts bp
        WHERE bp.id = :post_id
        """
        
        result = await db.execute(text(query), {'post_id': post_id})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        # Get enhanced product associations
        products_query = """
        SELECT 
            bpp.id, bpp.product_id, bpp.position, bpp.context,
            bpp.ai_context, bpp.relevance_score, bpp.mentioned_in_sections,
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
        
        # Get content sections
        sections_query = """
        SELECT id, blog_post_id, section_type, section_title, section_content,
               section_order, products_featured, ai_generated, created_at
        FROM blog_content_sections
        WHERE blog_post_id = :post_id
        ORDER BY section_order
        """
        
        sections_result = await db.execute(text(sections_query), {'post_id': post_id})
        sections_data = sections_result.fetchall()
        
        # Get generation history
        history_query = """
        SELECT id, blog_post_id, template_id, generation_status, prompt_used,
               model_used, tokens_used, generation_time_ms, error_message,
               generation_metadata, created_at
        FROM blog_generation_history
        WHERE blog_post_id = :post_id
        ORDER BY created_at DESC
        """
        
        history_result = await db.execute(text(history_query), {'post_id': post_id})
        history_data = history_result.fetchall()
        
        # Parse structured_content if it's a JSON string
        structured_content = row[5]
        if isinstance(structured_content, str):
            try:
                structured_content = json.loads(structured_content)
            except (json.JSONDecodeError, TypeError):
                structured_content = None
        
        return AIBlogPost(
            id=row[0],
            title=row[1],
            slug=row[2],
            excerpt=row[3],
            content=row[4],
            structured_content=structured_content,
            featured_image=row[6],
            author_name=row[7],
            status=row[8],
            seo_title=row[9],
            seo_description=row[10],
            reading_time=row[11],
            view_count=row[12],
            featured=row[13],
            published_at=row[14],
            created_at=row[15],
            updated_at=row[16],
            category_id=row[17],
            generated_by_ai=row[18],
            generation_prompt=row[19],
            generation_model=row[20],
            generation_params=row[21] or {},
            ai_notes=row[22],
            products=[
                EnhancedBlogPostProduct(
                    id=prod[0],
                    product_id=prod[1],
                    position=prod[2],
                    context=prod[3],
                    ai_context=prod[4],
                    relevance_score=prod[5],
                    mentioned_in_sections=prod[6] or [],
                    product_name=prod[7],
                    product_slug=prod[8],
                    product_brand=prod[9]
                )
                for prod in products_data
            ],
            sections=[
                BlogContentSection(
                    id=sec[0],
                    blog_post_id=sec[1],
                    section_type=sec[2],
                    section_title=sec[3],
                    section_content=sec[4],
                    section_order=sec[5],
                    products_featured=sec[6] or [],
                    ai_generated=sec[7],
                    created_at=sec[8]
                )
                for sec in sections_data
            ],
            generation_history=[
                BlogGenerationHistory(
                    id=hist[0],
                    blog_post_id=hist[1],
                    template_id=hist[2],
                    generation_status=hist[3],
                    prompt_used=hist[4],
                    model_used=hist[5],
                    tokens_used=hist[6],
                    generation_time_ms=hist[7],
                    error_message=hist[8],
                    generation_metadata=hist[9] or {},
                    created_at=hist[10]
                )
                for hist in history_data
            ]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch AI blog post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch AI blog post")

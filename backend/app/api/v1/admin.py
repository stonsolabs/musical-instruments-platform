"""
Admin-only API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
import logging
import json

from app.database import get_db
from app.middleware.azure_auth import require_azure_admin, get_azure_user, azure_auth
from app.blog_ai_schemas import (
    BlogGenerationTemplate, BlogGenerationTemplateCreate, BlogGenerationRequest,
    BlogGenerationResult, AIBlogPost, BlogGenerationHistory, EnhancedBlogPostProduct,
    BlogContentSection, CloneRewriteRequest
)
from app.services.simple_blog_generator import SimpleBlogGenerator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])

# === ADMIN DASHBOARD ===

@router.get("/user-info")
async def get_admin_info(
    request: Request,
    admin: dict = Depends(require_azure_admin)
):
    """Get current admin user information"""
    return {
        "user": admin,
        "permissions": ["blog_manage", "ai_generate", "view_history"],
        "login_time": datetime.utcnow().isoformat(),
        "ip_address": request.client.host
    }

@router.get("/sso/token")
async def get_admin_sso_token(
    admin: dict = Depends(require_azure_admin)
):
    """Issue a short-lived admin token for cross-site frontend usage."""
    token_info = azure_auth.issue_admin_token(admin['email'], ttl_seconds=3600)
    return token_info

@router.get("/sso/bridge", response_class=HTMLResponse)
async def admin_sso_bridge(origin: Optional[str] = None):
    """
    Simple HTML page, hosted on API domain, that fetches an admin token using Easy Auth cookie
    and posts it back to the opener via postMessage, then closes itself.
    """
    safe_origin = origin or "*"
    html = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset=\"utf-8\" />
    <title>Admin SSO Bridge</title>
    <meta name=\"robots\" content=\"noindex,nofollow\" />
  </head>
  <body>
    <script>
      (async function() {{
        try {{
          const resp = await fetch('/api/v1/admin/sso/token', {{ credentials: 'include' }});
          if (!resp.ok) throw new Error('Token request failed: ' + resp.status);
          const data = await resp.json();
          if (window.opener) {{
            window.opener.postMessage({{ type: 'GYMG_SSO_TOKEN', token: data.token, expires_at: data.expires_at }}, '{safe_origin}');
          }}
        }} catch (e) {{
          console.error('SSO bridge error', e);
        }} finally {{
          window.close();
        }}
      }})();
    </script>
  </body>
</html>
"""
    return HTMLResponse(content=html)

@router.get("/stats")
async def get_admin_stats(
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get admin dashboard statistics"""
    try:
        # Blog post statistics
        blog_stats_query = """
        SELECT 
            COUNT(*) as total_posts,
            COUNT(*) FILTER (WHERE status = 'published') as published_posts,
            COUNT(*) FILTER (WHERE generated_by_ai = true) as ai_generated_posts,
            SUM(view_count) as total_views,
            COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '7 days') as posts_last_week,
            COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '30 days') as posts_last_month
        FROM blog_posts
        """
        
        result = await db.execute(text(blog_stats_query))
        blog_stats = result.fetchone()
        
        # Generation statistics  
        gen_stats_query = """
        SELECT 
            COUNT(*) as total_generations,
            COUNT(*) FILTER (WHERE generation_status = 'completed') as successful_generations,
            COUNT(*) FILTER (WHERE generation_status = 'failed') as failed_generations,
            SUM(tokens_used) as total_tokens_used,
            AVG(generation_time_ms) as avg_generation_time
        FROM blog_generation_history
        WHERE created_at >= NOW() - INTERVAL '30 days'
        """
        
        result = await db.execute(text(gen_stats_query))
        gen_stats = result.fetchone()
        
        # Top performing posts
        top_posts_query = """
        SELECT title, slug, view_count, generated_by_ai
        FROM blog_posts 
        WHERE status = 'published'
        ORDER BY view_count DESC
        LIMIT 5
        """
        
        result = await db.execute(text(top_posts_query))
        top_posts = [dict(row._mapping) for row in result.fetchall()]
        
        return {
            "blog": {
                "total_posts": blog_stats[0] or 0,
                "published_posts": blog_stats[1] or 0,
                "ai_generated_posts": blog_stats[2] or 0,
                "total_views": blog_stats[3] or 0,
                "posts_last_week": blog_stats[4] or 0,
                "posts_last_month": blog_stats[5] or 0
            },
            "ai_generation": {
                "total_generations": gen_stats[0] or 0,
                "successful_generations": gen_stats[1] or 0,
                "failed_generations": gen_stats[2] or 0,
                "total_tokens_used": gen_stats[3] or 0,
                "avg_generation_time_ms": int(gen_stats[4] or 0),
                "success_rate": round((gen_stats[1] or 0) / max(gen_stats[0] or 1, 1) * 100, 1)
            },
            "top_posts": top_posts,
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch admin stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")

# === BLOG MANAGEMENT ===

@router.get("/blog/posts")
async def get_admin_blog_posts(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    ai_generated: Optional[bool] = Query(None),
    category: Optional[str] = Query(None),
    content_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get blog posts for admin management with enhanced filtering"""
    try:
        where_clauses = []
        params = {'limit': limit, 'offset': offset}
        
        if status:
            where_clauses.append("bp.status = :status")
            params['status'] = status
        
        if ai_generated is not None:
            where_clauses.append("bp.generated_by_ai = :ai_generated")
            params['ai_generated'] = ai_generated
        
        if category:
            where_clauses.append("bc.slug = :category")
            params['category'] = category
        
        if content_type:
            # Map content types to template patterns
            content_type_mapping = {
                'review': ['review', 'hands-on', 'deep dive'],
                'buying_guide': ['buying guide', 'guide template', 'what to look for'],
                'comparison': ['comparison', 'battle', 'showdown', 'vs'],
                'tutorial': ['tutorial', 'how-to', 'setup', 'maintenance'],
                'roundup': ['roundup', 'best picks', 'top'],
                'seasonal': ['seasonal', 'deals', 'black friday', 'holiday'],
                'artist': ['artist spotlight', 'rig'],
                'historical': ['history', 'evolution'],
                'quiz': ['quiz', 'interactive']
            }
            
            if content_type in content_type_mapping:
                patterns = content_type_mapping[content_type]
                # Search in generation_model field which stores template name
                pattern_conditions = " OR ".join([f"bp.generation_model ILIKE :pattern_{i}" for i in range(len(patterns))])
                where_clauses.append(f"({pattern_conditions})")
                for i, pattern in enumerate(patterns):
                    params[f'pattern_{i}'] = f'%{pattern}%'
        
        if search:
            where_clauses.append("(bp.title ILIKE :search OR bp.excerpt ILIKE :search)")
            params['search'] = f'%{search}%'
        
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        # Get total count for pagination
        count_query = f"""
        SELECT COUNT(DISTINCT bp.id)
        FROM blog_posts bp
        LEFT JOIN blog_categories bc ON bp.category_id = bc.id
        {where_clause}
        """
        
        count_result = await db.execute(text(count_query), params)
        total_count = count_result.scalar()
        
        # Get posts
        query = f"""
        SELECT 
            bp.id, bp.title, bp.slug, bp.excerpt, bp.featured_image,
            bp.author_name, bp.status, bp.reading_time, bp.view_count, 
            bp.featured, bp.published_at, bp.created_at, bp.updated_at,
            bp.noindex,
            bp.generated_by_ai, bp.generation_model,
            bc.name as category_name, bc.slug as category_slug,
            bc.color as category_color,
            COUNT(bpt.tag_id) as tag_count
        FROM blog_posts bp
        LEFT JOIN blog_categories bc ON bp.category_id = bc.id
        LEFT JOIN blog_post_tags bpt ON bp.id = bpt.blog_post_id
        {where_clause}
        GROUP BY bp.id, bc.id
        ORDER BY bp.created_at DESC
        LIMIT :limit OFFSET :offset
        """
        
        result = await db.execute(text(query), params)
        posts = [dict(row._mapping) for row in result.fetchall()]
        
        return {
            "posts": posts,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total_count,
                "page": (offset // limit) + 1,
                "total_pages": (total_count + limit - 1) // limit
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch admin blog posts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch blog posts")

# === TEMPLATES (ADMIN) ===

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    template_type: Optional[str] = None
    base_prompt: Optional[str] = None
    system_prompt: Optional[str] = None
    product_context_prompt: Optional[str] = None
    required_product_types: Optional[List[str]] = None
    min_products: Optional[int] = Field(None, ge=0, le=50)
    max_products: Optional[int] = Field(None, ge=1, le=50)
    suggested_tags: Optional[List[str]] = None
    seo_title_template: Optional[str] = None
    seo_description_template: Optional[str] = None
    content_structure: Optional[dict] = None
    is_active: Optional[bool] = None

@router.get("/blog/templates")
async def get_admin_blog_templates(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_azure_admin)
):
    try:
        query = """
        SELECT id, name, description, category_id, template_type, base_prompt,
               system_prompt, product_context_prompt, required_product_types,
               min_products, max_products, suggested_tags, seo_title_template,
               seo_description_template, content_structure, is_active,
               created_at, updated_at
        FROM blog_generation_templates
        WHERE is_active = true
        ORDER BY template_type, name
        """
        res = await db.execute(text(query))
        rows = res.fetchall()
        templates = []
        for r in rows:
            templates.append({
                "id": r[0], "name": r[1], "description": r[2], "category_id": r[3],
                "template_type": r[4], "base_prompt": r[5], "system_prompt": r[6],
                "product_context_prompt": r[7], "required_product_types": r[8] or [],
                "min_products": r[9], "max_products": r[10], "suggested_tags": r[11] or [],
                "seo_title_template": r[12], "seo_description_template": r[13],
                "content_structure": r[14] or {}, "is_active": r[15],
                "created_at": r[16], "updated_at": r[17]
            })
        return templates
    except Exception as e:
        logger.error(f"Failed to fetch admin templates: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch templates")

@router.put("/blog/templates/{template_id}")
async def update_admin_blog_template(
    template_id: int,
    payload: TemplateUpdate,
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_azure_admin)
):
    try:
        mapping = {
            "name": "name",
            "description": "description",
            "category_id": "category_id",
            "template_type": "template_type",
            "base_prompt": "base_prompt",
            "system_prompt": "system_prompt",
            "product_context_prompt": "product_context_prompt",
            "required_product_types": "required_product_types",
            "min_products": "min_products",
            "max_products": "max_products",
            "suggested_tags": "suggested_tags",
            "seo_title_template": "seo_title_template",
            "seo_description_template": "seo_description_template",
            "content_structure": "content_structure",
            "is_active": "is_active",
        }
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=400, detail="No fields to update")
        fields = []
        params = {"id": template_id}
        import json as _json
        for k, col in mapping.items():
            if k in data:
                v = data[k]
                if k in ("required_product_types", "suggested_tags", "content_structure"):
                    v = _json.dumps(v)
                fields.append(f"{col} = :{k}")
                params[k] = v
        fields.append("updated_at = CURRENT_TIMESTAMP")
        q = f"UPDATE blog_generation_templates SET {', '.join(fields)} WHERE id = :id"
        await db.execute(text(q), params)
        await db.commit()
        return {"id": template_id, "updated": list(data.keys())}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update template {template_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update template")

# === BULK PUBLISH ===

class PublishBatchRequest(BaseModel):
    ids: List[int] = Field(default_factory=list)
    strategy: str = Field(default="now", pattern="^(now|backfill)$")
    backfill_days: Optional[int] = Field(default=None, ge=1, le=90)


@router.post("/blog/posts/publish-batch")
async def publish_blog_posts_batch(
    payload: PublishBatchRequest,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Publish multiple posts at once. Strategy:
    - now: set status=published and published_at=now for all ids
    - backfill: distribute published_at randomly over the past N days
    """
    try:
        if not payload.ids:
            raise HTTPException(status_code=400, detail="No IDs provided")

        # Ensure IDs exist
        result = await db.execute(
            text("SELECT id FROM blog_posts WHERE id = ANY(:ids)"),
            {"ids": payload.ids},
        )
        existing_ids = {row[0] for row in result.fetchall()}
        missing = [i for i in payload.ids if i not in existing_ids]
        if missing:
            raise HTTPException(status_code=404, detail=f"Posts not found: {missing}")

        updates = []
        if payload.strategy == "now":
            pub_at = datetime.utcnow()
            for pid in payload.ids:
                updates.append({"id": pid, "published_at": pub_at})
        else:
            # backfill
            from random import randint, choice
            now = datetime.utcnow()
            days = max(1, int(payload.backfill_days or 7))
            for pid in payload.ids:
                delta_days = randint(0, days)
                dt = now - timedelta(days=delta_days)
                hour = randint(9, 21)
                minute = choice([0, 15, 30, 45])
                dt = dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
                updates.append({"id": pid, "published_at": dt})

        # Apply updates
        for u in updates:
            await db.execute(
                text(
                    "UPDATE blog_posts SET status = 'published', published_at = :published_at WHERE id = :id"
                ),
                {"published_at": u["published_at"], "id": u["id"]},
            )
        await db.commit()

        return {"updated": len(updates), "ids": [u["id"] for u in updates]}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed bulk publish: {e}")
        raise HTTPException(status_code=500, detail="Failed to bulk publish posts")

# === BULK STATUS UPDATE (draft/archive) ===

class StatusBatchRequest(BaseModel):
    ids: List[int] = Field(default_factory=list)
    status: str = Field(..., pattern=r"^(draft|archived)$")
    all: bool = False


@router.post("/blog/posts/status-batch")
async def set_status_blog_posts_batch(
    payload: StatusBatchRequest,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Set status for multiple posts to 'draft' or 'archived'"""
    try:
        if not payload.ids and not payload.all:
            raise HTTPException(status_code=400, detail="No IDs provided and 'all' flag not set")

        if payload.all:
            # Update all posts
            result = await db.execute(
                text(
                    "UPDATE blog_posts "
                    "SET status = :status, "
                    "    published_at = CASE WHEN CAST(:status AS VARCHAR)='draft' THEN NULL ELSE published_at END "
                    "RETURNING id"
                ),
                {"status": payload.status},
            )
            updated_ids = [row[0] for row in result.fetchall()]
            await db.commit()
            return {"updated": len(updated_ids), "status": payload.status, "ids": updated_ids, "all": True}

        # Validate IDs exist
        result = await db.execute(
            text("SELECT id FROM blog_posts WHERE id = ANY(:ids)"),
            {"ids": payload.ids},
        )
        existing_ids = {row[0] for row in result.fetchall()}
        missing = [i for i in payload.ids if i not in existing_ids]
        if missing:
            raise HTTPException(status_code=404, detail=f"Posts not found: {missing}")

        # Update selected posts in a single statement
        result = await db.execute(
            text(
                "UPDATE blog_posts "
                "SET status = :status, "
                "    published_at = CASE WHEN CAST(:status AS VARCHAR)='draft' THEN NULL ELSE published_at END "
                "WHERE id = ANY(:ids) "
                "RETURNING id"
            ),
            {"status": payload.status, "ids": payload.ids},
        )
        updated_ids = [row[0] for row in result.fetchall()]
        await db.commit()
        return {"updated": len(updated_ids), "status": payload.status, "ids": updated_ids}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed bulk status update: {e}")
        raise HTTPException(status_code=500, detail="Failed to update post statuses")

# === BULK SEO (noindex) ===

class SeoBatchRequest(BaseModel):
    ids: List[int] = Field(default_factory=list)
    noindex: bool = False


@router.post("/blog/posts/seo-batch")
async def set_seo_flags_blog_posts_batch(
    payload: SeoBatchRequest,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Set SEO flags (e.g., noindex) for multiple posts"""
    try:
        if not payload.ids:
            raise HTTPException(status_code=400, detail="No IDs provided")

        result = await db.execute(
            text("SELECT id FROM blog_posts WHERE id = ANY(:ids)"),
            {"ids": payload.ids},
        )
        existing_ids = {row[0] for row in result.fetchall()}
        missing = [i for i in payload.ids if i not in existing_ids]
        if missing:
            raise HTTPException(status_code=404, detail=f"Posts not found: {missing}")

        for pid in payload.ids:
            await db.execute(
                text("UPDATE blog_posts SET noindex = :noindex WHERE id = :id"),
                {"noindex": payload.noindex, "id": pid},
            )
        await db.commit()
        return {"updated": len(payload.ids), "noindex": payload.noindex, "ids": payload.ids}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed bulk SEO update: {e}")
        raise HTTPException(status_code=500, detail="Failed to update SEO flags")

# === AI GENERATION ===

@router.post("/blog/generate")
async def generate_ai_blog_post(
    request: BlogGenerationRequest,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Generate a blog post using AI (admin only)"""
    try:
        # Get OpenAI API key
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
        import json
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
        
        logger.info(f"AI blog post generated by admin {admin['email']}: post_id={blog_post_id}")
        
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

@router.post("/blog/clone-rewrite")
async def clone_and_rewrite_blog_post(
    request: CloneRewriteRequest,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Clone content from a source URL and rewrite it with AI (admin only)"""
    try:
        import os
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
        # TODO: Implement clone_and_rewrite functionality for SimpleBlogGenerator
        raise HTTPException(status_code=501, detail="Clone and rewrite functionality temporarily unavailable - use the simplified blog system instead")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to clone & rewrite blog post: {e}")
        raise HTTPException(status_code=500, detail="Failed to clone & rewrite blog post")

# Duplicate endpoint removed - using the main /blog/templates endpoint above

@router.get("/blog/generation-history")
async def get_generation_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get blog generation history"""
    try:
        where_clauses = []
        params = {'limit': limit, 'offset': offset}
        
        if status:
            where_clauses.append("generation_status = :status")
            params['status'] = status
        
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        query = f"""
        SELECT 
            bgh.id, bgh.blog_post_id, bgh.template_id, bgh.generation_status,
            bgh.model_used, bgh.tokens_used, bgh.generation_time_ms,
            bgh.error_message, bgh.created_at,
            bp.title as post_title, bp.slug as post_slug,
            bgt.name as template_name
        FROM blog_generation_history bgh
        LEFT JOIN blog_posts bp ON bgh.blog_post_id = bp.id
        LEFT JOIN blog_generation_templates bgt ON bgh.template_id = bgt.id
        {where_clause}
        ORDER BY bgh.created_at DESC
        LIMIT :limit OFFSET :offset
        """
        
        result = await db.execute(text(query), params)
        history = [dict(row._mapping) for row in result.fetchall()]
        
        return {
            "history": history,
            "pagination": {
                "limit": limit,
                "offset": offset
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch generation history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch generation history")

# === SYSTEM STATUS ===

@router.get("/system/health")
async def admin_system_health(
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get system health status for admin"""
    try:
        # Check database connection
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
        
        # Check OpenAI API key
        import os
        openai_key_status = "configured" if os.getenv('OPENAI_API_KEY') else "missing"
        
        # Check recent generation performance
        perf_query = """
        SELECT 
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE generation_status = 'completed') as successful,
            AVG(generation_time_ms) as avg_time
        FROM blog_generation_history 
        WHERE created_at >= NOW() - INTERVAL '24 hours'
        """
        
        result = await db.execute(text(perf_query))
        perf_stats = result.fetchone()
        
        return {
            "database": {"status": db_status},
            "openai": {"status": openai_key_status},
            "generation_performance_24h": {
                "total_attempts": perf_stats[0] or 0,
                "successful": perf_stats[1] or 0,
                "avg_time_ms": int(perf_stats[2] or 0),
                "success_rate": round((perf_stats[1] or 0) / max(perf_stats[0] or 1, 1) * 100, 1)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "database": {"status": "error", "error": str(e)},
            "timestamp": datetime.utcnow().isoformat()
        }

# === BATCH GENERATION ===
# Batch processing is now handled by the CLI system
# Use: python3.11 blog_generator_cli.py generate --posts 50
# Then: python3.11 blog_generator_cli.py process --file results.jsonl

@router.get("/blog/batches")
async def get_batch_jobs(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get batch jobs list"""
    try:
        where_clauses = []
        params = {'limit': limit, 'offset': offset}
        
        if status:
            where_clauses.append("status = :status")
            params['status'] = status
        
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        query = f"""
        SELECT 
            id, batch_id, batch_name, request_count, status,
            azure_batch_id, created_at, azure_created_at, completed_at,
            total_requests, completed_requests, failed_requests,
            created_by_email
        FROM blog_batch_jobs
        {where_clause}
        ORDER BY created_at DESC
        LIMIT :limit OFFSET :offset
        """
        
        result = await db.execute(text(query), params)
        batches = [dict(row._mapping) for row in result.fetchall()]
        
        return {
            "batches": batches,
            "pagination": {
                "limit": limit,
                "offset": offset
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch batch jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch batch jobs")

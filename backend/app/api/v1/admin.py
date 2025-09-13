"""
Admin-only API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Optional
from fastapi.responses import HTMLResponse
from datetime import datetime
import logging
import json

from app.database import get_db
from app.middleware.azure_auth import require_azure_admin, get_azure_user, azure_auth
from app.blog_ai_schemas import (
    BlogGenerationTemplate, BlogGenerationTemplateCreate, BlogGenerationRequest,
    BlogGenerationResult, AIBlogPost, BlogGenerationHistory, EnhancedBlogPostProduct,
    BlogContentSection, CloneRewriteRequest
)
from app.services.blog_ai_generator import BlogAIGenerator
from app.services.blog_batch_generator import BlogBatchGenerator

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
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get blog posts for admin management"""
    try:
        where_clauses = []
        params = {'limit': limit, 'offset': offset}
        
        if status:
            where_clauses.append("bp.status = :status")
            params['status'] = status
        
        if ai_generated is not None:
            where_clauses.append("bp.generated_by_ai = :ai_generated")
            params['ai_generated'] = ai_generated
        
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        query = f"""
        SELECT 
            bp.id, bp.title, bp.slug, bp.excerpt, bp.featured_image,
            bp.author_name, bp.status, bp.reading_time, bp.view_count, 
            bp.featured, bp.published_at, bp.created_at, bp.updated_at,
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
                "total": len(posts)  # In a real app, you'd do a separate COUNT query
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch admin blog posts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch blog posts")

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
        ai_generator = BlogAIGenerator(openai_api_key, db)
        
        # Generate blog post
        result = await ai_generator.generate_blog_post(request)
        
        if result.success:
            logger.info(f"AI blog post generated by admin {admin['email']}: post_id={result.blog_post_id}")
        else:
            logger.error(f"AI generation failed for admin {admin['email']}: {result.error_message}")
        
        return result
        
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
        ai_generator = BlogAIGenerator(openai_api_key, db)
        result = await ai_generator.clone_and_rewrite(request)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to clone & rewrite blog post: {e}")
        raise HTTPException(status_code=500, detail="Failed to clone & rewrite blog post")

@router.get("/blog/templates")
async def get_generation_templates(
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get blog generation templates"""
    try:
        query = """
        SELECT id, name, description, template_type, min_products, max_products,
               suggested_tags, is_active, created_at
        FROM blog_generation_templates
        WHERE is_active = true
        ORDER BY template_type, name
        """
        
        result = await db.execute(text(query))
        templates = [dict(row._mapping) for row in result.fetchall()]
        
        return {"templates": templates}
        
    except Exception as e:
        logger.error(f"Failed to fetch templates: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch templates")

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

@router.post("/blog/batch/create")
async def create_batch_generation(
    generation_requests: List[BlogGenerationRequest],
    batch_name: Optional[str] = None,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Create a batch generation request"""
    try:
        batch_generator = BlogBatchGenerator(db, admin['email'])
        result = await batch_generator.create_batch_generation_request(
            generation_requests, batch_name
        )
        
        if result["success"]:
            logger.info(f"Batch created by admin {admin['email']}: {result['batch_name']}")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to create batch: {e}")
        raise HTTPException(status_code=500, detail="Failed to create batch")

@router.post("/blog/batch/{batch_id}/upload")
async def upload_batch_to_azure(
    batch_id: str,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Upload batch file to Azure OpenAI"""
    try:
        # Get batch info from database
        query = "SELECT batch_file_path FROM blog_batch_jobs WHERE batch_id = :batch_id"
        result = await db.execute(text(query), {'batch_id': batch_id})
        batch_info = result.fetchone()
        
        if not batch_info:
            raise HTTPException(status_code=404, detail="Batch not found")
        
        batch_generator = BlogBatchGenerator(db, admin['email'])
        upload_result = await batch_generator.upload_batch_to_azure(batch_info[0])
        
        if upload_result["success"]:
            logger.info(f"Batch uploaded by admin {admin['email']}: {batch_id}")
        
        return upload_result
        
    except Exception as e:
        logger.error(f"Failed to upload batch: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload batch")

@router.post("/blog/batch/{file_id}/start")
async def start_batch_job(
    file_id: str,
    batch_name: str,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Start a batch job in Azure OpenAI"""
    try:
        batch_generator = BlogBatchGenerator(db, admin['email'])
        job_result = await batch_generator.create_azure_batch_job(file_id, batch_name)
        
        if job_result["success"]:
            logger.info(f"Batch job started by admin {admin['email']}: {job_result['batch_id']}")
        
        return job_result
        
    except Exception as e:
        logger.error(f"Failed to start batch job: {e}")
        raise HTTPException(status_code=500, detail="Failed to start batch job")

@router.get("/blog/batch/{azure_batch_id}/status")
async def check_batch_status(
    azure_batch_id: str,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Check batch job status"""
    try:
        batch_generator = BlogBatchGenerator(db, admin['email'])
        status_result = await batch_generator.check_batch_status(azure_batch_id)
        
        return status_result
        
    except Exception as e:
        logger.error(f"Failed to check batch status: {e}")
        raise HTTPException(status_code=500, detail="Failed to check batch status")

@router.post("/blog/batch/{azure_batch_id}/download")
async def download_batch_results(
    azure_batch_id: str,
    output_file_id: str,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Download batch results"""
    try:
        batch_generator = BlogBatchGenerator(db, admin['email'])
        download_result = await batch_generator.download_batch_results(
            azure_batch_id, output_file_id
        )
        
        if download_result["success"]:
            logger.info(f"Batch results downloaded by admin {admin['email']}: {azure_batch_id}")
        
        return download_result
        
    except Exception as e:
        logger.error(f"Failed to download batch results: {e}")
        raise HTTPException(status_code=500, detail="Failed to download batch results")

@router.post("/blog/batch/process")
async def process_batch_results(
    results_file_path: str,
    metadata_file_path: str,
    auto_publish: bool = False,
    admin: dict = Depends(require_azure_admin),
    db: AsyncSession = Depends(get_db)
):
    """Process batch results and create blog posts"""
    try:
        batch_generator = BlogBatchGenerator(db, admin['email'])
        process_result = await batch_generator.process_batch_results(
            results_file_path, metadata_file_path, auto_publish
        )
        
        if process_result["success"]:
            logger.info(f"Batch processed by admin {admin['email']}: {process_result['batch_id']} - {process_result['total_processed']} posts")
        
        return process_result
        
    except Exception as e:
        logger.error(f"Failed to process batch results: {e}")
        raise HTTPException(status_code=500, detail="Failed to process batch results")

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

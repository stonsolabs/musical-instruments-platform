#!/usr/bin/env python3
"""
Simplified Blog Batch Processor Service
Processes OpenAI batch results and saves to simplified blog structure
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import async_session_factory

logger = logging.getLogger(__name__)

class SimpleBlogBatchProcessor:
    
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        self.errors = []
    
    async def process_batch_file(self, batch_file_path: str, 
                               dry_run: bool = False) -> Dict[str, Any]:
        """
        Process OpenAI batch results file and save blog posts
        
        Args:
            batch_file_path: Path to JSONL batch results file
            dry_run: If True, validate but don't save to database
            
        Returns:
            Processing summary with stats and errors
        """
        
        self.processed_count = 0
        self.error_count = 0
        self.errors = []
        
        logger.info(f"Processing batch file: {batch_file_path}")
        
        try:
            with open(batch_file_path, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    try:
                        batch_item = json.loads(line.strip())
                        await self._process_batch_item(batch_item, dry_run)
                        self.processed_count += 1
                        
                        if self.processed_count % 10 == 0:
                            logger.info(f"Processed {self.processed_count} items...")
                            
                    except Exception as e:
                        self.error_count += 1
                        error_msg = f"Line {line_num}: {str(e)}"
                        self.errors.append(error_msg)
                        logger.error(error_msg)
        
        except FileNotFoundError:
            raise ValueError(f"Batch file not found: {batch_file_path}")
        
        summary = {
            "processed_count": self.processed_count,
            "error_count": self.error_count,
            "errors": self.errors[:10],  # Limit to first 10 errors
            "success_rate": (self.processed_count / (self.processed_count + self.error_count)) * 100 if (self.processed_count + self.error_count) > 0 else 0
        }
        
        logger.info(f"Processing complete: {summary}")
        return summary
    
    async def _process_batch_item(self, batch_item: Dict, dry_run: bool = False):
        """Process individual batch result item"""
        
        # Extract the response content
        try:
            response = batch_item.get('response', {})
            choices = response.get('body', {}).get('choices', [])
            
            if not choices:
                raise ValueError("No choices in response")
            
            content = choices[0].get('message', {}).get('content', '')
            
            if not content:
                raise ValueError("Empty content in response")
            
            # Parse the JSON content
            try:
                blog_content = json.loads(content)
            except json.JSONDecodeError as e:
                # Try to extract JSON if wrapped in markdown
                if '```json' in content:
                    start = content.find('```json') + 7
                    end = content.rfind('```')
                    if end > start:
                        content = content[start:end].strip()
                        blog_content = json.loads(content)
                    else:
                        raise e
                else:
                    raise e
            
            # Validate required fields
            self._validate_blog_content(blog_content)
            
            # Generate slug from title
            slug = self._generate_slug(blog_content['title'])
            
            # Save to database if not dry run
            if not dry_run:
                await self._save_blog_post(blog_content, slug)
                
        except Exception as e:
            custom_id = batch_item.get('custom_id', 'unknown')
            raise ValueError(f"Failed to process item {custom_id}: {str(e)}")
    
    def _validate_blog_content(self, content: Dict):
        """Validate blog content structure"""
        
        required_fields = ['title', 'sections']
        for field in required_fields:
            if field not in content:
                raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(content['sections'], list) or len(content['sections']) == 0:
            raise ValueError("Sections must be a non-empty list")
        
        # Validate sections
        for i, section in enumerate(content['sections']):
            if not isinstance(section, dict):
                raise ValueError(f"Section {i} must be an object")
            
            if 'type' not in section:
                raise ValueError(f"Section {i} missing type field")
        
        # Estimate word count
        word_count = self._estimate_word_count(content)
        if word_count < 2500:
            logger.warning(f"Content may be too short: {word_count} words")
    
    def _estimate_word_count(self, content: Dict) -> int:
        """Estimate total word count of the blog post"""
        total_words = 0
        
        for section in content.get('sections', []):
            if 'content' in section:
                # Simple word count estimation
                text = section['content'].replace('#', '').replace('*', '').replace('-', '')
                words = len(text.split())
                total_words += words
        
        return total_words
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        import re
        
        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
        
        # Limit length
        return slug[:100]
    
    async def _save_blog_post(self, content: Dict, slug: str):
        """Save blog post to simplified database structure"""
        
        async with async_session_factory() as session:
            try:
                # Prepare data
                title = content['title']
                excerpt = content.get('excerpt', title[:200])
                seo_title = content.get('seo_title', title)
                seo_description = content.get('seo_description', excerpt)
                category = content.get('category', 'general')
                
                # Check if slug already exists
                result = await session.execute(
                    text("SELECT id FROM blog_posts WHERE slug = :slug"),
                    {"slug": slug}
                )
                
                if result.fetchone():
                    # Generate unique slug
                    counter = 1
                    original_slug = slug
                    while True:
                        new_slug = f"{original_slug}-{counter}"
                        result = await session.execute(
                            text("SELECT id FROM blog_posts WHERE slug = :slug"),
                            {"slug": new_slug}
                        )
                        if not result.fetchone():
                            slug = new_slug
                            break
                        counter += 1
                
                # Calculate reading time (rough estimate: 200 words per minute)
                word_count = self._estimate_word_count(content)
                reading_time = max(1, round(word_count / 200))
                
                # Insert blog post
                insert_query = text("""
                    INSERT INTO blog_posts (
                        title, slug, excerpt, content_json, seo_title, seo_description,
                        author_name, status, published_at, created_at, updated_at
                    ) VALUES (
                        :title, :slug, :excerpt, :content_json, :seo_title, :seo_description,
                        :author_name, :status, :published_at, :created_at, :updated_at
                    )
                    RETURNING id
                """)
                
                now = datetime.utcnow()
                
                result = await session.execute(insert_query, {
                    "title": title,
                    "slug": slug,
                    "excerpt": excerpt,
                    "content_json": json.dumps(content),
                    "seo_title": seo_title,
                    "seo_description": seo_description,
                    "author_name": "GetYourMusicGear Team",
                    "status": "draft",  # Always create as draft for review
                    "published_at": None,
                    "created_at": now,
                    "updated_at": now
                })
                
                blog_post_id = result.fetchone()[0]
                
                await session.commit()
                
                logger.info(f"Saved blog post: {title} (ID: {blog_post_id}, Slug: {slug})")
                
            except Exception as e:
                await session.rollback()
                raise e
    
    async def get_processing_stats(self) -> Dict[str, Any]:
        """Get current processing statistics"""
        async with async_session_factory() as session:
            # Get blog post counts by status
            result = await session.execute(text("""
                SELECT status, COUNT(*) as count 
                FROM blog_posts 
                GROUP BY status
            """))
            
            status_counts = {row[0]: row[1] for row in result.fetchall()}
            
            # Get recent posts
            result = await session.execute(text("""
                SELECT title, slug, created_at, content_json->>'category' as category
                FROM blog_posts 
                ORDER BY created_at DESC 
                LIMIT 10
            """))
            
            recent_posts = [dict(row._mapping) for row in result.fetchall()]
            
            return {
                "status_counts": status_counts,
                "recent_posts": recent_posts,
                "total_posts": sum(status_counts.values())
            }
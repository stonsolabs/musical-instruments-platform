"""
AI Blog Post Generation Service
"""

import asyncio
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import openai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import logging

from app.models.blog_ai import (
    BlogGenerationRequest, BlogGenerationResult, AIProductRecommendation,
    BlogContentSectionCreate, ProductSelectionCriteria, TemplateType
)

logger = logging.getLogger(__name__)

class BlogAIGenerator:
    def __init__(self, openai_api_key: str, db_session: AsyncSession):
        self.client = openai.AsyncOpenAI(api_key=openai_api_key)
        self.db = db_session
        self.default_model = "gpt-4o"
    
    async def generate_blog_post(self, request: BlogGenerationRequest) -> BlogGenerationResult:
        """Generate a complete blog post using AI"""
        start_time = datetime.now()
        
        try:
            # Get generation template
            template = await self._get_template(request.template_id)
            if not template:
                return BlogGenerationResult(
                    success=False,
                    error_message="Template not found"
                )
            
            # Get relevant products
            products = await self._select_relevant_products(
                request.product_ids, 
                template,
                request.category_id
            )
            
            # Build generation prompt
            prompt = await self._build_generation_prompt(
                template, 
                products, 
                request
            )
            
            # Generate content with AI
            generation_response = await self._call_ai_generation(
                prompt,
                template.get('system_prompt'),
                request.generation_params
            )
            
            if not generation_response['success']:
                return BlogGenerationResult(
                    success=False,
                    error_message=generation_response.get('error', 'AI generation failed'),
                    tokens_used=generation_response.get('tokens_used')
                )
            
            # Parse AI response
            parsed_content = await self._parse_ai_response(
                generation_response['content'],
                products,
                template
            )
            
            # Create blog post record
            blog_post_id = await self._create_blog_post_record(
                parsed_content,
                request,
                template,
                prompt,
                generation_response
            )
            
            # Record generation history
            history_id = await self._record_generation_history(
                blog_post_id,
                request.template_id,
                prompt,
                generation_response,
                "completed"
            )
            
            end_time = datetime.now()
            generation_time = int((end_time - start_time).total_seconds() * 1000)
            
            return BlogGenerationResult(
                success=True,
                blog_post_id=blog_post_id,
                generation_history_id=history_id,
                generated_content=parsed_content['content'],
                generated_title=parsed_content['title'],
                generated_excerpt=parsed_content['excerpt'],
                seo_title=parsed_content.get('seo_title'),
                seo_description=parsed_content.get('seo_description'),
                suggested_products=parsed_content.get('product_recommendations', []),
                sections=parsed_content.get('sections', []),
                tokens_used=generation_response.get('tokens_used'),
                generation_time_ms=generation_time
            )
            
        except Exception as e:
            logger.error(f"Blog AI generation error: {e}")
            
            # Record failed generation
            if 'blog_post_id' in locals():
                await self._record_generation_history(
                    locals().get('blog_post_id'),
                    request.template_id,
                    locals().get('prompt', ''),
                    {},
                    "failed",
                    str(e)
                )
            
            return BlogGenerationResult(
                success=False,
                error_message=str(e)
            )
    
    async def _get_template(self, template_id: int) -> Optional[Dict[str, Any]]:
        """Get blog generation template"""
        query = """
        SELECT id, name, template_type, base_prompt, system_prompt, 
               product_context_prompt, required_product_types, min_products, 
               max_products, suggested_tags, seo_title_template, 
               seo_description_template, content_structure
        FROM blog_generation_templates 
        WHERE id = :template_id AND is_active = true
        """
        
        result = await self.db.execute(text(query), {'template_id': template_id})
        row = result.fetchone()
        
        if not row:
            return None
            
        return {
            'id': row[0],
            'name': row[1],
            'template_type': row[2],
            'base_prompt': row[3],
            'system_prompt': row[4],
            'product_context_prompt': row[5],
            'required_product_types': row[6] or [],
            'min_products': row[7],
            'max_products': row[8],
            'suggested_tags': row[9] or [],
            'seo_title_template': row[10],
            'seo_description_template': row[11],
            'content_structure': row[12] or {}
        }
    
    async def _select_relevant_products(
        self, 
        requested_product_ids: List[int], 
        template: Dict[str, Any],
        category_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Select relevant products for the blog post"""
        
        # Start with requested products
        products = []
        
        if requested_product_ids:
            query = """
            SELECT p.id, p.name, p.slug, p.description, p.avg_rating, 
                   p.review_count, p.featured, b.name as brand_name,
                   c.name as category_name, c.slug as category_slug
            FROM products p
            LEFT JOIN brands b ON p.brand_id = b.id
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.id = ANY(:product_ids)
            ORDER BY p.featured DESC, p.avg_rating DESC
            """
            
            result = await self.db.execute(text(query), {'product_ids': requested_product_ids})
            products = [dict(row._mapping) for row in result.fetchall()]
        
        # If we need more products, find relevant ones
        needed_products = max(0, template['min_products'] - len(products))
        
        if needed_products > 0:
            additional_products = await self._find_additional_products(
                template,
                category_id,
                [p['id'] for p in products],
                needed_products
            )
            products.extend(additional_products)
        
        # Limit to max products
        return products[:template['max_products']]
    
    async def _find_additional_products(
        self,
        template: Dict[str, Any],
        category_id: Optional[int],
        exclude_ids: List[int],
        needed_count: int
    ) -> List[Dict[str, Any]]:
        """Find additional relevant products"""
        
        where_clauses = ["p.id NOT IN :exclude_ids" if exclude_ids else "1=1"]
        params = {'exclude_ids': exclude_ids if exclude_ids else []}
        
        # Filter by category if specified
        if category_id:
            where_clauses.append("c.parent_id = :category_id OR p.category_id = :category_id")
            params['category_id'] = category_id
        
        # Filter by required product types from template
        if template.get('required_product_types'):
            category_filter = " OR ".join([
                f"c.slug ILIKE '%{ptype}%' OR c.name ILIKE '%{ptype}%'" 
                for ptype in template['required_product_types']
            ])
            where_clauses.append(f"({category_filter})")
        
        query = f"""
        SELECT p.id, p.name, p.slug, p.description, p.avg_rating, 
               p.review_count, p.featured, b.name as brand_name,
               c.name as category_name, c.slug as category_slug
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE {' AND '.join(where_clauses)}
        ORDER BY p.featured DESC, p.avg_rating DESC, p.review_count DESC
        LIMIT :limit
        """
        
        params['limit'] = needed_count
        
        result = await self.db.execute(text(query), params)
        return [dict(row._mapping) for row in result.fetchall()]
    
    async def _build_generation_prompt(
        self,
        template: Dict[str, Any],
        products: List[Dict[str, Any]],
        request: BlogGenerationRequest
    ) -> str:
        """Build the generation prompt for AI"""
        
        # Start with base prompt
        prompt_parts = [template['base_prompt']]
        
        # Add content structure if available
        if template.get('content_structure', {}).get('sections'):
            sections = template['content_structure']['sections']
            prompt_parts.append(f"\nStructure your content with these sections: {', '.join(sections)}")
        
        # Add product context
        if products and template.get('product_context_prompt'):
            product_info = "\n".join([
                f"- {p['name']} by {p['brand_name']} (Rating: {p['avg_rating'] or 'N/A'}, Category: {p['category_name']})"
                for p in products
            ])
            
            prompt_parts.append(f"\n{template['product_context_prompt']}")
            prompt_parts.append(f"\nFeatured Products:\n{product_info}")
        
        # Add custom additions
        if request.custom_prompt_additions:
            prompt_parts.append(f"\nAdditional requirements: {request.custom_prompt_additions}")
        
        # Add formatting requirements
        prompt_parts.append(f"""
        
IMPORTANT FORMATTING REQUIREMENTS:
- Target word count: {request.target_word_count} words
- Use markdown formatting for structure
- Include proper headings (## for main sections, ### for subsections)
- Write in an engaging, informative tone
- Include specific product recommendations with detailed explanations
- Make sure content is SEO-friendly and valuable to readers
        
Response format should be JSON:
{{
    "title": "Generated blog post title",
    "excerpt": "Brief excerpt (1-2 sentences)",
    "content": "Full blog post content in markdown",
    "seo_title": "SEO optimized title",
    "seo_description": "SEO meta description",
    "sections": [
        {{"type": "introduction", "title": "Introduction", "content": "Section content"}},
        {{"type": "main", "title": "Main Content", "content": "Section content"}}
    ],
    "product_recommendations": [
        {{"product_id": 123, "relevance_score": 0.95, "reasoning": "Why this product fits", "suggested_context": "recommended", "suggested_sections": ["introduction", "recommendations"]}}
    ]
}}
        """)
        
        return "\n".join(prompt_parts)
    
    async def _call_ai_generation(
        self,
        prompt: str,
        system_prompt: Optional[str],
        generation_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call OpenAI API for content generation"""
        
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            # Set default parameters
            params = {
                "model": generation_params.get("model", self.default_model),
                "messages": messages,
                "temperature": generation_params.get("temperature", 0.7),
                "max_tokens": generation_params.get("max_tokens", 3000),
                "response_format": {"type": "json_object"}
            }
            
            response = await self.client.chat.completions.create(**params)
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "model": params["model"]
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                "success": False,
                "error": str(e),
                "tokens_used": 0
            }
    
    async def _parse_ai_response(
        self,
        ai_response: str,
        products: List[Dict[str, Any]],
        template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse and validate AI response"""
        
        try:
            parsed = json.loads(ai_response)
            
            # Validate required fields
            required_fields = ['title', 'content']
            for field in required_fields:
                if field not in parsed:
                    raise ValueError(f"Missing required field: {field}")
            
            # Generate excerpt if not provided
            if not parsed.get('excerpt'):
                # Extract first 200 characters from content, clean markdown
                content_clean = re.sub(r'[#*`\[\]()]', '', parsed['content'])
                parsed['excerpt'] = content_clean[:200].strip() + "..."
            
            # Validate product recommendations
            if 'product_recommendations' in parsed:
                valid_product_ids = {p['id'] for p in products}
                parsed['product_recommendations'] = [
                    rec for rec in parsed['product_recommendations']
                    if rec.get('product_id') in valid_product_ids
                ]
            
            # Estimate reading time
            word_count = len(parsed['content'].split())
            parsed['reading_time'] = max(1, round(word_count / 200))
            
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            # Fallback: try to extract content between markers
            return self._fallback_parse_ai_response(ai_response)
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            raise
    
    def _fallback_parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """Fallback parser if JSON parsing fails"""
        # Simple fallback - treat entire response as content
        lines = ai_response.strip().split('\n')
        title = lines[0].replace('#', '').strip() if lines else "Generated Blog Post"
        
        return {
            'title': title,
            'content': ai_response,
            'excerpt': ai_response[:200] + "..." if len(ai_response) > 200 else ai_response,
            'reading_time': max(1, round(len(ai_response.split()) / 200))
        }
    
    async def _create_blog_post_record(
        self,
        parsed_content: Dict[str, Any],
        request: BlogGenerationRequest,
        template: Dict[str, Any],
        prompt: str,
        generation_response: Dict[str, Any]
    ) -> int:
        """Create blog post database record"""
        
        # Generate slug from title
        slug = re.sub(r'[^\w\s-]', '', parsed_content['title'].lower())
        slug = re.sub(r'[\s_-]+', '-', slug).strip('-')
        
        # Insert blog post
        insert_query = """
        INSERT INTO blog_posts (
            title, slug, excerpt, content, category_id, author_name,
            status, seo_title, seo_description, reading_time, featured,
            generated_by_ai, generation_prompt, generation_model, generation_params,
            published_at
        ) VALUES (
            :title, :slug, :excerpt, :content, :category_id, :author_name,
            :status, :seo_title, :seo_description, :reading_time, :featured,
            :generated_by_ai, :generation_prompt, :generation_model, :generation_params,
            :published_at
        ) RETURNING id
        """
        
        published_at = datetime.utcnow() if request.auto_publish else None
        
        result = await self.db.execute(text(insert_query), {
            'title': parsed_content['title'],
            'slug': slug,
            'excerpt': parsed_content.get('excerpt'),
            'content': parsed_content['content'],
            'category_id': request.category_id or template.get('category_id'),
            'author_name': 'AI Assistant',
            'status': 'published' if request.auto_publish else 'draft',
            'seo_title': parsed_content.get('seo_title') or parsed_content['title'],
            'seo_description': parsed_content.get('seo_description'),
            'reading_time': parsed_content.get('reading_time', 5),
            'featured': False,
            'generated_by_ai': True,
            'generation_prompt': prompt,
            'generation_model': generation_response.get('model'),
            'generation_params': json.dumps(request.generation_params),
            'published_at': published_at
        })
        
        blog_post_id = result.scalar()
        
        # Add product associations
        if parsed_content.get('product_recommendations'):
            await self._add_product_associations(blog_post_id, parsed_content['product_recommendations'])
        
        # Add content sections
        if parsed_content.get('sections'):
            await self._add_content_sections(blog_post_id, parsed_content['sections'])
        
        # Add tags
        if template.get('suggested_tags'):
            await self._add_blog_tags(blog_post_id, template['suggested_tags'])
        
        await self.db.commit()
        
        return blog_post_id
    
    async def _add_product_associations(
        self, 
        blog_post_id: int, 
        product_recommendations: List[Dict[str, Any]]
    ):
        """Add product associations to blog post"""
        
        for i, rec in enumerate(product_recommendations):
            await self.db.execute(text("""
                INSERT INTO blog_post_products (
                    blog_post_id, product_id, position, context, ai_context, 
                    relevance_score, mentioned_in_sections
                ) VALUES (
                    :blog_post_id, :product_id, :position, :context, :ai_context,
                    :relevance_score, :mentioned_in_sections
                )
            """), {
                'blog_post_id': blog_post_id,
                'product_id': rec['product_id'],
                'position': i,
                'context': rec.get('suggested_context', 'featured'),
                'ai_context': rec.get('reasoning'),
                'relevance_score': rec.get('relevance_score'),
                'mentioned_in_sections': json.dumps(rec.get('suggested_sections', []))
            })
    
    async def _add_content_sections(
        self,
        blog_post_id: int,
        sections: List[Dict[str, Any]]
    ):
        """Add structured content sections"""
        
        for i, section in enumerate(sections):
            await self.db.execute(text("""
                INSERT INTO blog_content_sections (
                    blog_post_id, section_type, section_title, section_content,
                    section_order, ai_generated
                ) VALUES (
                    :blog_post_id, :section_type, :section_title, :section_content,
                    :section_order, :ai_generated
                )
            """), {
                'blog_post_id': blog_post_id,
                'section_type': section.get('type', 'content'),
                'section_title': section.get('title'),
                'section_content': section.get('content', ''),
                'section_order': i,
                'ai_generated': True
            })
    
    async def _add_blog_tags(self, blog_post_id: int, tag_names: List[str]):
        """Add tags to blog post"""
        
        for tag_name in tag_names:
            tag_slug = re.sub(r'[^\w\s-]', '', tag_name.lower())
            tag_slug = re.sub(r'[\s_-]+', '-', tag_slug).strip('-')
            
            # Insert or get tag
            tag_result = await self.db.execute(text("""
                INSERT INTO blog_tags (name, slug) 
                VALUES (:name, :slug)
                ON CONFLICT (slug) DO UPDATE SET name = :name
                RETURNING id
            """), {'name': tag_name, 'slug': tag_slug})
            
            tag_id = tag_result.scalar()
            
            # Link tag to post
            await self.db.execute(text("""
                INSERT INTO blog_post_tags (blog_post_id, tag_id) 
                VALUES (:blog_post_id, :tag_id)
                ON CONFLICT DO NOTHING
            """), {'blog_post_id': blog_post_id, 'tag_id': tag_id})
    
    async def _record_generation_history(
        self,
        blog_post_id: Optional[int],
        template_id: int,
        prompt: str,
        generation_response: Dict[str, Any],
        status: str,
        error_message: Optional[str] = None
    ) -> int:
        """Record generation history"""
        
        insert_query = """
        INSERT INTO blog_generation_history (
            blog_post_id, template_id, generation_status, prompt_used,
            model_used, tokens_used, generation_time_ms, error_message,
            generation_metadata
        ) VALUES (
            :blog_post_id, :template_id, :generation_status, :prompt_used,
            :model_used, :tokens_used, :generation_time_ms, :error_message,
            :generation_metadata
        ) RETURNING id
        """
        
        result = await self.db.execute(text(insert_query), {
            'blog_post_id': blog_post_id,
            'template_id': template_id,
            'generation_status': status,
            'prompt_used': prompt,
            'model_used': generation_response.get('model'),
            'tokens_used': generation_response.get('tokens_used'),
            'generation_time_ms': None,  # Will be updated later
            'error_message': error_message,
            'generation_metadata': json.dumps(generation_response)
        })
        
        return result.scalar()
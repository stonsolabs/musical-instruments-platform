#!/usr/bin/env python3
"""
Blog Batch Processor Service - Production-ready service for processing blog batch results
Handles parsing, validation, and database insertion of AI-generated blog content
"""

import asyncio
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import async_session_factory

class BlogBatchProcessorService:
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        self.errors = []
        self.default_author_id = None
    
    async def initialize(self):
        """Initialize the service by setting up default author"""
        await self._setup_default_author()
    
    async def _setup_default_author(self):
        """Setup default author for blog posts"""
        try:
            async with async_session_factory() as session:
                # Get all active authors
                result = await session.execute(text("SELECT id, name FROM authors WHERE is_active = true ORDER BY id"))
                authors = result.fetchall()
                
                if authors:
                    # Use the first author as default, but we'll rotate through them
                    self.available_authors = authors
                    self.author_index = 0
                    print(f"📝 Loaded {len(authors)} authors for rotation")
                else:
                    # Create default author if none exists
                    await session.execute(text("""
                        INSERT INTO authors (name, email, bio, is_active, created_at, updated_at)
                        VALUES ('GetYourMusicGear Team', 'team@getyourmusicgear.com', 'Professional music gear reviewers and experts', true, NOW(), NOW())
                        ON CONFLICT (email) DO NOTHING
                    """))
                    await session.commit()
                    
                    result = await session.execute(text("SELECT id, name FROM authors WHERE email = 'team@getyourmusicgear.com'"))
                    author = result.fetchone()
                    if author:
                        self.available_authors = [author]
                        self.author_index = 0
                        print(f"📝 Created default author: GetYourMusicGear Team (ID: {author[0]})")
                    else:
                        self.available_authors = []
                        self.author_index = 0
        except Exception as e:
            print(f"⚠️  Error setting up author: {e}")
            self.available_authors = []
            self.author_index = 0
    
    async def process_batch_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a batch results file and insert blog posts into database
        
        Args:
            file_path: Path to the batch results JSONL file
            
        Returns:
            Dictionary with processing statistics
        """
        print(f"🚀 Processing batch results file: {file_path}")
        print("=" * 60)
        
        self.processed_count = 0
        self.error_count = 0
        self.errors = []
        
        # Calculate staggered dates (spread posts over 30 days)
        base_date = datetime.utcnow()
        date_increment = 0
        
        async with async_session_factory() as session:
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        # Parse the batch result entry
                        entry = json.loads(line.strip())
                        custom_id = entry.get('custom_id', f'unknown-{line_num}')
                        
                        # Extract AI response content
                        response = entry.get('response', {})
                        body = response.get('body', {})
                        choices = body.get('choices', [])
                        
                        if not choices:
                            self.error_count += 1
                            error_msg = f"Line {line_num}: No choices in response"
                            self.errors.append(error_msg)
                            print(f"❌ {error_msg}")
                            continue
                        
                        ai_content = choices[0].get('message', {}).get('content', '')
                        if not ai_content:
                            self.error_count += 1
                            error_msg = f"Line {line_num}: No content in AI response"
                            self.errors.append(error_msg)
                            print(f"❌ {error_msg}")
                            continue
                        
                        # Parse structured content
                        structured_content = self._parse_structured_content(ai_content)
                        if not structured_content:
                            self.error_count += 1
                            error_msg = f"Line {line_num}: Failed to parse structured content"
                            self.errors.append(error_msg)
                            print(f"❌ {error_msg}")
                            continue
                        
                        # Determine template type from custom_id
                        template_type = self._extract_template_type(custom_id)
                        
                        # Create blog post with staggered date
                        blog_post_id = await self._create_blog_post(
                            session, 
                            structured_content, 
                            template_type, 
                            custom_id,
                            base_date,
                            date_increment
                        )
                        
                        # Increment date for next post (spread over 30 days)
                        date_increment += 1
                        
                        if blog_post_id:
                            self.processed_count += 1
                            print(f"✅ Line {line_num}: Created blog post {blog_post_id} ({template_type})")
                            # Commit after each successful post to avoid transaction issues
                            await session.commit()
                        else:
                            self.error_count += 1
                            print(f"❌ Line {line_num}: Failed to create blog post")
                            # Rollback on failure and start fresh transaction
                            await session.rollback()
                            # Start a new transaction for the next iteration
                            await session.begin()
                            
                    except Exception as e:
                        self.error_count += 1
                        error_msg = f"Line {line_num}: {str(e)}"
                        self.errors.append(error_msg)
                        print(f"❌ {error_msg}")
                        # Rollback on error
                        try:
                            await session.rollback()
                        except:
                            pass
        
        print(f"\n🎉 Processing completed!")
        print(f"✅ Successfully processed: {self.processed_count} blog posts")
        print(f"❌ Errors: {self.error_count}")
        
        return {
            "processed_count": self.processed_count,
            "error_count": self.error_count,
            "errors": self.errors,
            "success_rate": (self.processed_count / (self.processed_count + self.error_count)) * 100 if (self.processed_count + self.error_count) > 0 else 0
        }
    
    def _parse_structured_content(self, ai_content: str) -> Optional[Dict[str, Any]]:
        """Parse the AI-generated JSON content into structured format"""
        try:
            # Parse the JSON content
            parsed = json.loads(ai_content)
            
            # Ensure parsed is a dictionary
            if not isinstance(parsed, dict):
                print(f"Expected dict, got {type(parsed)}")
                return None
            
            # Extract basic information
            title = parsed.get('title', parsed.get('sub_header', 'Generated Blog Post'))
            def _smart_excerpt(text: str, limit: int = 200) -> str:
                import re
                if not text:
                    return ""
                clean = re.sub(r"[#*`\[\]()]", "", text).strip()
                if len(clean) <= limit:
                    return clean
                window = clean[: limit + 20]
                half = max(1, limit // 2)
                punct_idx = max(window.rfind('.'), window.rfind('!'), window.rfind('?'))
                if punct_idx >= half:
                    return window[: punct_idx + 1].strip()
                space_idx = clean.rfind(' ', 0, limit)
                if space_idx > 0:
                    return (clean[:space_idx] + '…').strip()
                return (clean[:limit] + '…').strip()

            base_excerpt = parsed.get('excerpt') or parsed.get('bold_paragraph_text') or ''
            excerpt = _smart_excerpt(base_excerpt or parsed.get('content',''), 200) if (base_excerpt or parsed.get('content')) else ""
            
            # Build the full content with proper product integration
            full_content = self._build_rich_content(parsed)
            
            # Extract all product IDs mentioned in the content
            product_ids = self._extract_all_product_ids(parsed)
            
            # Create structured sections for the database
            content_sections = self._create_content_sections(parsed)
            
            return {
                'title': title,
                'excerpt': excerpt,
                'content': full_content,
                'structured_content': parsed,
                'content_sections': content_sections,
                'product_ids': product_ids,
                'seo_title': title,
                'seo_description': excerpt
            }
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None
        except Exception as e:
            print(f"Parse error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _build_rich_content(self, parsed: Dict[str, Any]) -> str:
        """Build rich markdown content from parsed JSON structure"""
        content_parts = []
        
        # Add title
        title = parsed.get('title', '')
        if title:
            content_parts.append(f"# {title}")
        
        # Add excerpt/intro
        excerpt = parsed.get('excerpt', '')
        if excerpt:
            content_parts.append(f"**{excerpt}**")
        
        # Process different content sections based on structure
        if 'first_impressions' in parsed:
            content_parts.append(self._process_first_impressions(parsed['first_impressions']))
        
        if 'build_analysis' in parsed:
            content_parts.append(self._process_build_analysis(parsed['build_analysis']))
        
        if 'performance_testing' in parsed:
            content_parts.append(self._process_performance_testing(parsed['performance_testing']))
        
        if 'competitive_comparison' in parsed:
            content_parts.append(self._process_competitive_comparison(parsed['competitive_comparison']))
        
        if 'ownership_experience' in parsed:
            content_parts.append(self._process_ownership_experience(parsed['ownership_experience']))
        
        if 'pros_cons' in parsed:
            content_parts.append(self._process_pros_cons(parsed['pros_cons']))
        
        if 'buyer_guidance' in parsed:
            content_parts.append(self._process_buyer_guidance(parsed['buyer_guidance']))
        
        if 'final_verdict' in parsed:
            content_parts.append(self._process_final_verdict(parsed['final_verdict']))
        
        # Process other sections
        for key, value in parsed.items():
            if key not in ['title', 'excerpt', 'first_impressions', 'build_analysis', 
                          'performance_testing', 'competitive_comparison', 'ownership_experience',
                          'pros_cons', 'buyer_guidance', 'final_verdict'] and isinstance(value, dict):
                content_parts.append(self._process_generic_section(key, value))
        
        return "\n\n".join(filter(None, content_parts))
    
    def _process_first_impressions(self, section: Dict[str, Any]) -> str:
        """Process first impressions section"""
        parts = [f"## {section.get('title', 'First Impressions')}"]
        
        if section.get('unboxing'):
            parts.append(f"### Unboxing\n{section['unboxing']}")
        
        if section.get('initial_thoughts'):
            parts.append(f"### Initial Thoughts\n{section['initial_thoughts']}")
        
        if section.get('build_quality_first_look'):
            parts.append(f"### Build Quality First Look\n{section['build_quality_first_look']}")
        
        if section.get('affiliate_cta'):
            parts.append(f"**{section['affiliate_cta']}**")
        
        return "\n\n".join(parts)
    
    def _process_build_analysis(self, section: Dict[str, Any]) -> str:
        """Process build analysis section"""
        parts = [f"## {section.get('title', 'Build Quality Analysis')}"]
        
        for key in ['materials', 'construction', 'durability', 'attention_to_detail', 'value_assessment']:
            if section.get(key):
                parts.append(f"### {key.replace('_', ' ').title()}\n{section[key]}")
        
        if section.get('affiliate_cta'):
            parts.append(f"**{section['affiliate_cta']}**")
        
        return "\n\n".join(parts)
    
    def _process_performance_testing(self, section: Dict[str, Any]) -> str:
        """Process performance testing section"""
        parts = [f"## {section.get('title', 'Performance Testing')}"]
        
        for key in ['test_conditions', 'results', 'strengths', 'weaknesses', 'comparison_to_specs']:
            if section.get(key):
                parts.append(f"### {key.replace('_', ' ').title()}\n{section[key]}")
        
        if section.get('affiliate_cta'):
            parts.append(f"**{section['affiliate_cta']}**")
        
        return "\n\n".join(parts)
    
    def _process_competitive_comparison(self, section: Dict[str, Any]) -> str:
        """Process competitive comparison section"""
        parts = [f"## {section.get('title', 'Competitive Comparison')}"]
        
        competitors = section.get('competitors', [])
        for i, competitor in enumerate(competitors, 1):
            parts.append(f"### {competitor.get('name', f'Competitor {i}')}")
            parts.append(f"**Price:** {competitor.get('price', 'N/A')}")
            parts.append(f"**How it compares:** {competitor.get('how_it_compares', '')}")
            parts.append(f"**When to choose:** {competitor.get('when_to_choose_competitor', '')}")
            if competitor.get('affiliate_cta'):
                parts.append(f"**{competitor['affiliate_cta']}**")
            parts.append("")  # Add spacing
        
        return "\n\n".join(parts)
    
    def _process_ownership_experience(self, section: Dict[str, Any]) -> str:
        """Process ownership experience section"""
        parts = [f"## {section.get('title', 'Long-term Ownership Experience')}"]
        
        for key in ['durability_over_time', 'maintenance', 'customer_support', 'resale_value']:
            if section.get(key):
                parts.append(f"### {key.replace('_', ' ').title()}\n{section[key]}")
        
        if section.get('affiliate_cta'):
            parts.append(f"**{section['affiliate_cta']}**")
        
        return "\n\n".join(parts)
    
    def _process_pros_cons(self, section: Dict[str, Any]) -> str:
        """Process pros and cons section"""
        parts = [f"## {section.get('title', 'Pros and Cons')}"]
        
        if section.get('pros'):
            parts.append("### Pros")
            for pro in section['pros']:
                parts.append(f"✅ {pro}")
        
        if section.get('cons'):
            parts.append("### Cons")
            for con in section['cons']:
                parts.append(f"❌ {con}")
        
        if section.get('overall_assessment'):
            parts.append(f"### Overall Assessment\n{section['overall_assessment']}")
        
        return "\n\n".join(parts)
    
    def _process_buyer_guidance(self, section: Dict[str, Any]) -> str:
        """Process buyer guidance section"""
        parts = [f"## {section.get('title', 'Who Should Buy This')}"]
        
        for key in ['ideal_buyer', 'skill_level', 'use_cases', 'alternatives']:
            if section.get(key):
                parts.append(f"### {key.replace('_', ' ').title()}\n{section[key]}")
        
        if section.get('affiliate_cta'):
            parts.append(f"**{section['affiliate_cta']}**")
        
        return "\n\n".join(parts)
    
    def _process_final_verdict(self, section: Dict[str, Any]) -> str:
        """Process final verdict section"""
        parts = [f"## {section.get('title', 'Final Verdict')}"]
        
        if section.get('rating'):
            parts.append(f"**Rating: {section['rating']}/10**")
        
        if section.get('summary'):
            parts.append(f"**Summary:** {section['summary']}")
        
        if section.get('recommendation'):
            parts.append(f"**Recommendation:** {section['recommendation']}")
        
        if section.get('final_cta'):
            parts.append(f"**{section['final_cta']}**")
        
        if section.get('current_deals'):
            parts.append(f"**Current Deals:** {section['current_deals']}")
        
        return "\n\n".join(parts)
    
    def _process_generic_section(self, title: str, section: Dict[str, Any]) -> str:
        """Process generic section"""
        parts = [f"## {title.replace('_', ' ').title()}"]
        
        for key, value in section.items():
            if isinstance(value, str):
                parts.append(f"### {key.replace('_', ' ').title()}\n{value}")
            elif isinstance(value, list):
                parts.append(f"### {key.replace('_', ' ').title()}")
                for item in value:
                    if isinstance(item, str):
                        parts.append(f"- {item}")
                    elif isinstance(item, dict):
                        # Render common dict-shaped items in readable markdown instead of raw dicts
                        if 'criterion' in item:
                            parts.append(f"- {item.get('criterion')}: {item.get('description', '')}")
                            if item.get('why_matters'):
                                parts.append(f"  - Why it matters: {item['why_matters']}")
                            if item.get('red_flags'):
                                parts.append(f"  - Red flags: {item['red_flags']}")
                        elif 'tier' in item and 'recommendation' in item:
                            parts.append(f"- {item.get('tier')}: {item.get('recommendation')}" + (f" — {item.get('reasoning')}" if item.get('reasoning') else ""))
                        elif 'mistake' in item:
                            parts.append(f"- Mistake: {item.get('mistake')}")
                            if item.get('why_happens'):
                                parts.append(f"  - Why it happens: {item['why_happens']}")
                            if item.get('how_to_avoid'):
                                parts.append(f"  - How to avoid: {item['how_to_avoid']}")
                            if item.get('better_alternative'):
                                parts.append(f"  - Better alternative: {item['better_alternative']}")
                        elif 'step' in item and 'title' in item:
                            parts.append(f"- Step {item.get('step')}: {item.get('title')}")
                            if item.get('description'):
                                parts.append(f"  - {item['description']}")
                        else:
                            # Generic pretty-print: key: value pairs on one bullet
                            kv = []
                            for k, v in item.items():
                                if isinstance(v, (str, int, float)) and v is not None:
                                    kv.append(f"{k.replace('_',' ').title()}: {v}")
                            if kv:
                                parts.append(f"- {'; '.join(kv)}")
                            else:
                                parts.append(f"- {item.get('name', '')}".strip())

        return "\n\n".join(parts)
    
    def _extract_all_product_ids(self, parsed: Dict[str, Any]) -> List[str]:
        """Extract all product IDs from the parsed content"""
        product_ids = set()
        
        # Search through all text content for product IDs
        def search_for_product_ids(obj):
            if isinstance(obj, str):
                # Look for patterns like (1163), [1163], product_id: 1163, etc.
                patterns = [
                    r'\((\d+)\)',
                    r'\[(\d+)\]',
                    r'product_id["\']?\s*:\s*["\']?(\d+)',
                    r'#(\d+)',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, obj)
                    product_ids.update(matches)
            
            elif isinstance(obj, dict):
                for value in obj.values():
                    search_for_product_ids(value)
            elif isinstance(obj, list):
                for item in obj:
                    search_for_product_ids(item)
        
        search_for_product_ids(parsed)
        return list(product_ids)
    
    def _create_content_sections(self, parsed: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create structured content sections for database storage"""
        sections = []
        section_order = 1
        
        # Add main sections
        for key, value in parsed.items():
            if isinstance(value, dict) and key not in ['title', 'excerpt']:
                sections.append({
                    'section_type': key,
                    'section_title': value.get('title', key.replace('_', ' ').title()),
                    'section_content': json.dumps(value),
                    'section_order': section_order
                })
                section_order += 1
        
        return sections
    
    def _extract_template_type(self, custom_id: str) -> str:
        """Extract template type from custom_id"""
        if 'review' in custom_id:
            return 'review'
        elif 'comparison' in custom_id:
            return 'comparison'
        elif 'buying_guide' in custom_id:
            return 'buying_guide'
        elif 'artist_spotlight' in custom_id:
            return 'artist_spotlight'
        elif 'general' in custom_id:
            return 'general'
        else:
            return 'blog'
    
    async def _create_blog_post(
        self, 
        session, 
        structured_content: Dict[str, Any], 
        template_type: str,
        custom_id: str,
        base_date: datetime,
        date_increment: int
    ) -> Optional[int]:
        """Create blog post in database with proper formatting"""
        try:
            # Generate slug from title
            title = structured_content['title']
            slug = re.sub(r'[^\w\s-]', '', title.lower())
            slug = re.sub(r'[\s_-]+', '-', slug).strip('-')
            
            # Ensure slug is unique by adding custom_id suffix if needed
            original_slug = slug
            counter = 1
            while True:
                # Check if slug exists
                check_query = "SELECT id FROM blog_posts WHERE slug = :slug"
                result = await session.execute(text(check_query), {'slug': slug})
                if not result.fetchone():
                    break
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            # Insert blog post
            insert_query = """
            INSERT INTO blog_posts (
                title, slug, excerpt, content, structured_content, 
                author_name, status, seo_title, seo_description, 
                reading_time, featured, generated_by_ai, 
                generation_prompt, generation_model, generation_params,
                published_at, created_at, updated_at
            ) VALUES (
                :title, :slug, :excerpt, :content, :structured_content,
                :author_name, :status, :seo_title, :seo_description,
                :reading_time, :featured, :generated_by_ai,
                :generation_prompt, :generation_model, :generation_params,
                :published_at, :created_at, :updated_at
            ) RETURNING id
            """
            
            # Calculate staggered date (spread posts over 30 days)
            from datetime import timedelta
            post_date = base_date + timedelta(days=date_increment % 30, hours=date_increment % 24)
            now = datetime.utcnow()
            
            # Rotate through available authors
            if hasattr(self, 'available_authors') and self.available_authors:
                author = self.available_authors[self.author_index % len(self.available_authors)]
                author_name = author[1]  # author name
                self.author_index += 1
            else:
                author_name = "GetYourMusicGear Team"
            
            result = await session.execute(text(insert_query), {
                'title': title,
                'slug': slug,
                'excerpt': structured_content.get('excerpt', ''),
                'content': structured_content['content'],
                'structured_content': json.dumps(structured_content['structured_content']),
                'author_name': author_name,
                'status': 'draft',  # Insert as draft for review
                'seo_title': structured_content.get('seo_title', title),
                'seo_description': structured_content.get('seo_description', ''),
                'reading_time': max(1, round(len(structured_content['content'].split()) / 200)),
                'featured': False,
                'generated_by_ai': True,
                'generation_prompt': f'Batch generated from {custom_id}',
                'generation_model': 'gpt-4.1',
                'generation_params': json.dumps({'template_type': template_type}),
                'published_at': post_date,  # Staggered publication date
                'created_at': now,
                'updated_at': now
            })
            
            blog_post_id = result.scalar_one()
            
            # Create content sections
            for section in structured_content.get('content_sections', []):
                await self._create_content_section(session, blog_post_id, section)
            
            # Create product associations
            for product_id in structured_content.get('product_ids', []):
                await self._create_product_association(session, blog_post_id, product_id)
            
            return blog_post_id
            
        except Exception as e:
            print(f"Error creating blog post: {e}")
            return None
    
    async def _create_content_section(self, session: AsyncSession, blog_post_id: int, section: Dict[str, Any]):
        """Create content section in database"""
        try:
            insert_query = """
            INSERT INTO blog_content_sections (
                blog_post_id, section_type, section_title, 
                section_content, section_order, created_at, updated_at
            ) VALUES (
                :blog_post_id, :section_type, :section_title,
                :section_content, :section_order, :created_at, :updated_at
            )
            """
            
            now = datetime.utcnow()
            await session.execute(text(insert_query), {
                'blog_post_id': blog_post_id,
                'section_type': section.get('section_type', section.get('type', 'general')),
                'section_title': section.get('section_title', section.get('title', '')),
                'section_content': section.get('section_content', json.dumps(section)),
                'section_order': section.get('section_order', section.get('order', 1)),
                'created_at': now,
                'updated_at': now
            })
        except Exception as e:
            print(f"Error creating content section: {e}")
            # Don't re-raise - continue with other sections
            # This prevents transaction abortion
    
    async def _create_product_association(self, session: AsyncSession, blog_post_id: int, product_id: str):
        """Create product association in database"""
        try:
            insert_query = """
            INSERT INTO blog_post_products (
                blog_post_id, product_id, created_at, updated_at
            ) VALUES (
                :blog_post_id, :product_id, :created_at, :updated_at
            ) ON CONFLICT (blog_post_id, product_id) DO NOTHING
            """
            
            now = datetime.utcnow()
            await session.execute(text(insert_query), {
                'blog_post_id': blog_post_id,
                'product_id': int(product_id),
                'created_at': now,
                'updated_at': now
            })
        except Exception as e:
            print(f"Error creating product association: {e}")
            # Don't re-raise - continue with other products
            # This prevents transaction abortion
    
    async def get_processing_stats(self) -> Dict[str, Any]:
        """Get statistics about processed blog posts"""
        async with async_session_factory() as session:
            # Get total blog posts
            result = await session.execute(text("SELECT COUNT(*) FROM blog_posts"))
            total_posts = result.scalar_one()
            
            # Get AI-generated posts
            result = await session.execute(text("SELECT COUNT(*) FROM blog_posts WHERE generated_by_ai = true"))
            ai_posts = result.scalar_one()
            
            # Get posts by template type
            result = await session.execute(text("""
                SELECT generation_params->>'template_type' as template_type, COUNT(*) as count
                FROM blog_posts 
                WHERE generated_by_ai = true AND generation_params IS NOT NULL
                GROUP BY generation_params->>'template_type'
                ORDER BY count DESC
            """))
            template_stats = {row[0]: row[1] for row in result.fetchall()}
            
            # Get recent posts
            result = await session.execute(text("""
                SELECT title, created_at 
                FROM blog_posts 
                WHERE generated_by_ai = true 
                ORDER BY created_at DESC 
                LIMIT 5
            """))
            recent_posts = [{'title': row[0], 'created_at': row[1]} for row in result.fetchall()]
            
            return {
                "total_posts": total_posts,
                "ai_generated_posts": ai_posts,
                "template_distribution": template_stats,
                "recent_posts": recent_posts
            }

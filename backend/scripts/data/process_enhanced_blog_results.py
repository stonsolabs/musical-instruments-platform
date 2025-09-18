#!/usr/bin/env python3
"""
Process Enhanced Blog Results
Handles the new JSON structure with comprehensive affiliate integration
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.app.database import async_session_factory
from sqlalchemy import text

class EnhancedBlogProcessor:
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        self.errors = []
    
    async def process_batch_results(self, batch_file_path: str):
        """Process batch results with enhanced JSON structure"""
        print(f"🚀 Processing enhanced blog batch: {batch_file_path}")
        
        with open(batch_file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    batch_result = json.loads(line.strip())
                    await self.process_single_result(batch_result, line_num)
                except json.JSONDecodeError as e:
                    self.error_count += 1
                    self.errors.append(f"Line {line_num}: JSON decode error - {e}")
                except Exception as e:
                    self.error_count += 1
                    self.errors.append(f"Line {line_num}: Processing error - {e}")
        
        print(f"\n📊 Processing Summary:")
        print(f"  ✅ Successfully processed: {self.processed_count}")
        print(f"  ❌ Errors: {self.error_count}")
        
        if self.errors:
            print(f"\n🔍 Errors encountered:")
            for error in self.errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more errors")
    
    async def process_single_result(self, batch_result: Dict, line_num: int):
        """Process a single batch result"""
        try:
            # Extract the blog content from the batch result
            if 'response' in batch_result and 'body' in batch_result['response']:
                choices = batch_result['response']['body'].get('choices', [])
                if choices and 'message' in choices[0]:
                    content = choices[0]['message'].get('content', '')
                    
                    # Parse the JSON content
                    blog_data = json.loads(content)
                    
                    # Validate the structure
                    if self.validate_blog_structure(blog_data):
                        # Process the blog post
                        await self.save_blog_post(blog_data, batch_result.get('custom_id', f'blog-{line_num}'))
                        self.processed_count += 1
                    else:
                        self.error_count += 1
                        self.errors.append(f"Line {line_num}: Invalid blog structure")
                else:
                    self.error_count += 1
                    self.errors.append(f"Line {line_num}: No content in response")
            else:
                self.error_count += 1
                self.errors.append(f"Line {line_num}: Invalid batch result structure")
                
        except Exception as e:
            self.error_count += 1
            self.errors.append(f"Line {line_num}: Error processing result - {e}")
    
    def validate_blog_structure(self, blog_data: Dict) -> bool:
        """Validate the enhanced blog JSON structure"""
        required_fields = ['title', 'excerpt', 'seo_title', 'seo_description', 'sections', 'tags', 'meta']
        
        # Check top-level fields
        for field in required_fields:
            if field not in blog_data:
                return False
        
        # Check sections structure
        if not isinstance(blog_data['sections'], list):
            return False
        
        for section in blog_data['sections']:
            if 'type' not in section or 'title' not in section:
                return False
            
            # Check for product showcases
            if section['type'] == 'product_showcase_inline':
                if 'products' not in section or not isinstance(section['products'], list):
                    return False
                
                for product in section['products']:
                    if 'product_id' not in product or 'context' not in product:
                        return False
        
        return True
    
    async def save_blog_post(self, blog_data: Dict, custom_id: str):
        """Save the processed blog post to database"""
        async with async_session_factory() as session:
            try:
                # Extract basic info
                title = blog_data['title']
                excerpt = blog_data['excerpt']
                seo_title = blog_data.get('seo_title', title)
                seo_description = blog_data.get('seo_description', excerpt)
                tags = blog_data.get('tags', [])
                meta = blog_data.get('meta', {})
                sections = blog_data['sections']
                
                # Calculate word count
                word_count = self.calculate_word_count(blog_data)
                reading_time = max(1, word_count // 250)  # 250 words per minute
                
                # Extract product IDs for affiliate integration
                product_ids = self.extract_product_ids(blog_data)
                
                # Create structured content
                structured_content = {
                    'sections': sections,
                    'meta': meta,
                    'product_recommendations': blog_data.get('product_recommendations', []),
                    'affiliate_integration': 'comprehensive'
                }
                
                # Insert blog post
                result = await session.execute(
                    text("""
                        INSERT INTO blog_posts (
                            title, excerpt, content, seo_title, seo_description,
                            reading_time, word_count, structured_content,
                            author_name, status, created_at, updated_at
                        ) VALUES (
                            :title, :excerpt, :content, :seo_title, :seo_description,
                            :reading_time, :word_count, :structured_content,
                            :author_name, :status, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
                        ) RETURNING id
                    """),
                    {
                        'title': title,
                        'excerpt': excerpt,
                        'content': self.generate_markdown_content(sections),
                        'seo_title': seo_title,
                        'seo_description': seo_description,
                        'reading_time': reading_time,
                        'word_count': word_count,
                        'structured_content': json.dumps(structured_content),
                        'author_name': 'GetYourMusicGear AI',
                        'status': 'draft'
                    }
                )
                
                blog_post_id = result.fetchone()[0]
                
                # Insert tags
                for tag_name in tags:
                    await self.upsert_tag(session, tag_name)
                    await self.link_blog_tag(session, blog_post_id, tag_name)
                
                # Insert product associations
                for product_id in product_ids:
                    await self.link_blog_product(session, blog_post_id, product_id)
                
                await session.commit()
                print(f"✅ Saved blog post: {title[:50]}... (ID: {blog_post_id})")
                
            except Exception as e:
                await session.rollback()
                raise e
    
    def calculate_word_count(self, blog_data: Dict) -> int:
        """Calculate total word count from all content"""
        word_count = 0
        
        # Count words in main content
        for section in blog_data.get('sections', []):
            if 'content' in section:
                word_count += len(section['content'].split())
        
        return word_count
    
    def extract_product_ids(self, blog_data: Dict) -> List[int]:
        """Extract all product IDs mentioned in the blog"""
        product_ids = set()
        
        # Extract from sections
        for section in blog_data.get('sections', []):
            if section.get('type') == 'product_showcase_inline':
                for product in section.get('products', []):
                    if 'product_id' in product:
                        product_ids.add(product['product_id'])
            
            if 'products_mentioned' in section:
                product_ids.update(section['products_mentioned'])
        
        # Extract from product recommendations
        for rec in blog_data.get('product_recommendations', []):
            if 'product_id' in rec:
                product_ids.add(rec['product_id'])
        
        return list(product_ids)
    
    def generate_markdown_content(self, sections: List[Dict]) -> str:
        """Generate markdown content from structured sections"""
        markdown_parts = []
        
        for section in sections:
            section_type = section.get('type', '')
            title = section.get('title', '')
            content = section.get('content', '')
            
            # Add title
            if title:
                markdown_parts.append(f"## {title}")
            
            # Add content
            if content:
                markdown_parts.append(content)
            
            # Add section-specific content
            if section_type == 'pros_cons':
                pros = section.get('pros', [])
                cons = section.get('cons', [])
                
                if pros:
                    markdown_parts.append("### Pros")
                    for pro in pros:
                        markdown_parts.append(f"- {pro}")
                
                if cons:
                    markdown_parts.append("### Cons")
                    for con in cons:
                        markdown_parts.append(f"- {con}")
            
            elif section_type == 'faqs':
                faqs = section.get('faqs', [])
                for faq in faqs:
                    markdown_parts.append(f"**Q: {faq.get('question', '')}**")
                    markdown_parts.append(f"A: {faq.get('answer', '')}")
            
            markdown_parts.append("")  # Add spacing
        
        return "\n".join(markdown_parts)
    
    async def upsert_tag(self, session, tag_name: str):
        """Upsert a tag"""
        await session.execute(
            text("""
                INSERT INTO blog_tags (name, slug, created_at, updated_at)
                VALUES (:name, :slug, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT (slug) DO UPDATE SET
                    name = EXCLUDED.name,
                    updated_at = CURRENT_TIMESTAMP
            """),
            {
                'name': tag_name,
                'slug': tag_name.lower().replace(' ', '-').replace('_', '-')
            }
        )
    
    async def link_blog_tag(self, session, blog_post_id: int, tag_name: str):
        """Link a blog post to a tag"""
        tag_slug = tag_name.lower().replace(' ', '-').replace('_', '-')
        
        await session.execute(
            text("""
                INSERT INTO blog_post_tags (blog_post_id, tag_id)
                SELECT :blog_post_id, id FROM blog_tags WHERE slug = :tag_slug
                ON CONFLICT DO NOTHING
            """),
            {
                'blog_post_id': blog_post_id,
                'tag_slug': tag_slug
            }
        )
    
    async def link_blog_product(self, session, blog_post_id: int, product_id: int):
        """Link a blog post to a product"""
        await session.execute(
            text("""
                INSERT INTO blog_post_products (blog_post_id, product_id, created_at)
                VALUES (:blog_post_id, :product_id, CURRENT_TIMESTAMP)
                ON CONFLICT (blog_post_id, product_id) DO NOTHING
            """),
            {
                'blog_post_id': blog_post_id,
                'product_id': product_id
            }
        )

async def main():
    if len(sys.argv) != 2:
        print("Usage: python process_enhanced_blog_results.py <batch_file_path>")
        sys.exit(1)
    
    batch_file_path = sys.argv[1]
    
    if not os.path.exists(batch_file_path):
        print(f"❌ Batch file not found: {batch_file_path}")
        sys.exit(1)
    
    processor = EnhancedBlogProcessor()
    await processor.process_batch_results(batch_file_path)

if __name__ == "__main__":
    asyncio.run(main())

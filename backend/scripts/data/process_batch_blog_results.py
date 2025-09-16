#!/usr/bin/env python3
"""
Process OpenAI batch results and insert blog posts into database.
This script reads the batch output JSONL file and creates blog posts with structured content.
"""

import asyncio
import sys
import os
import json
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text
import slugify

def clean_slug(text: str) -> str:
    """Create a clean URL-friendly slug"""
    return slugify.slugify(text, max_length=100, word_boundary=True, separator='-')

def extract_json_from_content(content: str) -> Optional[Dict[Any, Any]]:
    """Extract JSON from content, handling cases where there might be extra text"""
    # Try to parse as direct JSON first
    try:
        return json.loads(content.strip())
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON within the content
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON between code blocks
    code_block_match = re.search(r'```(?:json)?\s*(\{.*\})\s*```', content, re.DOTALL)
    if code_block_match:
        try:
            return json.loads(code_block_match.group(1))
        except json.JSONDecodeError:
            pass
    
    return None

def validate_blog_structure(blog_data: Dict[Any, Any]) -> bool:
    """Validate that the blog post has the required structure"""
    required_fields = ['title', 'sections']
    
    for field in required_fields:
        if field not in blog_data:
            return False
    
    # Validate sections structure
    if not isinstance(blog_data['sections'], list) or len(blog_data['sections']) == 0:
        return False
    
    # Check that sections have required fields
    for section in blog_data['sections']:
        if not isinstance(section, dict) or 'type' not in section or 'content' not in section:
            return False
    
    return True

def convert_structured_to_html(blog_data: Dict[Any, Any]) -> str:
    """Convert structured JSON sections to HTML content"""
    html_parts = []
    
    for section in blog_data.get('sections', []):
        section_type = section.get('type', '')
        title = section.get('title')
        content = section.get('content', '')
        
        # Add section title if present
        if title and section_type != 'introduction':
            html_parts.append(f'<h2>{title}</h2>')
        
        # Add section content
        html_parts.append(content)
        
        # Handle special section types
        if section_type == 'product_showcase' and 'products' in section:
            html_parts.append('<div class="product-showcase">')
            for product in section['products']:
                if 'context' in product:
                    html_parts.append(f'<div class="product-context" data-product-id="{product.get("product_id")}">')
                    html_parts.append(f'<p><strong>Our Pick:</strong> {product["context"]}</p>')
                    html_parts.append('</div>')
            html_parts.append('</div>')
        
        elif section_type == 'faqs' and 'faqs' in section:
            html_parts.append('<div class="faq-section">')
            for faq in section['faqs']:
                html_parts.append('<div class="faq-item">')
                html_parts.append(f'<h4>{faq.get("question", "")}</h4>')
                html_parts.append(f'<p>{faq.get("answer", "")}</p>')
                html_parts.append('</div>')
            html_parts.append('</div>')
    
    return '\n\n'.join(html_parts)

def extract_product_references(blog_data: Dict[Any, Any]) -> List[Dict[str, Any]]:
    """Extract product references from structured content"""
    products = []
    
    for section in blog_data.get('sections', []):
        # Handle product showcase sections
        if section.get('type') == 'product_showcase' and 'products' in section:
            for product in section['products']:
                products.append({
                    'product_id': product.get('product_id'),
                    'context': product.get('context', ''),
                    'position': product.get('position', len(products) + 1)
                })
        
        # Handle products mentioned in other sections
        if 'products_mentioned' in section:
            for product_id in section['products_mentioned']:
                # Only add if not already added
                if not any(p['product_id'] == product_id for p in products):
                    products.append({
                        'product_id': product_id,
                        'context': None,
                        'position': len(products) + 1
                    })
    
    return products

async def get_category_id_by_name(category_name: str) -> Optional[int]:
    """Get category ID by name"""
    async with async_session_factory() as session:
        result = await session.execute(
            text("SELECT id FROM blog_categories WHERE name ILIKE :name LIMIT 1"),
            {"name": f"%{category_name}%"}
        )
        row = result.fetchone()
        return row[0] if row else None

async def create_tags(tag_names: List[str]) -> List[int]:
    """Create or get existing tags and return their IDs"""
    tag_ids = []
    
    async with async_session_factory() as session:
        for tag_name in tag_names:
            # Check if tag exists
            result = await session.execute(
                text("SELECT id FROM blog_tags WHERE name = :name"),
                {"name": tag_name}
            )
            existing = result.fetchone()
            
            if existing:
                tag_ids.append(existing[0])
            else:
                # Create new tag
                result = await session.execute(
                    text("""
                        INSERT INTO blog_tags (name, slug) 
                        VALUES (:name, :slug) 
                        RETURNING id
                    """),
                    {
                        "name": tag_name,
                        "slug": clean_slug(tag_name)
                    }
                )
                tag_ids.append(result.fetchone()[0])
        
        await session.commit()
    
    return tag_ids

async def get_random_author() -> str:
    """Get a random author from the database"""
    async with async_session_factory() as session:
        result = await session.execute(
            text("SELECT author_name FROM blog_posts WHERE author_name IS NOT NULL ORDER BY RANDOM() LIMIT 1")
        )
        author = result.fetchone()
        return author[0] if author else "Music Gear Expert"

async def insert_blog_post(blog_data: Dict[Any, Any], custom_id: str) -> Optional[int]:
    """Insert a blog post into the database"""
    
    try:
        # Extract basic data
        title = blog_data.get('title', 'Untitled')
        excerpt = blog_data.get('excerpt', '')
        seo_title = blog_data.get('seo_title') or title
        seo_description = blog_data.get('seo_description', '')
        reading_time = blog_data.get('reading_time', 5)
        
        # Get random author from database
        author_name = await get_random_author()
        
        # Convert structured content to HTML
        content = convert_structured_to_html(blog_data)
        structured_content = json.dumps(blog_data)
        
        # Create slug
        slug = clean_slug(title)
        
        # Get or create category (default to first category if not specified)
        category_id = 1  # Default category
        
        # Extract tags
        tags = blog_data.get('tags', [])
        tag_ids = await create_tags(tags) if tags else []
        
        # Extract product references
        products = extract_product_references(blog_data)
        
        async with async_session_factory() as session:
            # Check for duplicate slug
            counter = 1
            original_slug = slug
            while True:
                result = await session.execute(
                    text("SELECT id FROM blog_posts WHERE slug = :slug"),
                    {"slug": slug}
                )
                if not result.fetchone():
                    break
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            # Insert blog post
            result = await session.execute(
                text("""
                    INSERT INTO blog_posts (
                        title, slug, excerpt, content, structured_content,
                        category_id, author_name, status, featured, 
                        seo_title, seo_description, reading_time,
                        created_at, updated_at
                    ) VALUES (
                        :title, :slug, :excerpt, :content, :structured_content,
                        :category_id, :author_name, :status, :featured,
                        :seo_title, :seo_description, :reading_time,
                        CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
                    ) RETURNING id
                """),
                {
                    "title": title,
                    "slug": slug,
                    "excerpt": excerpt,
                    "content": content,
                    "structured_content": structured_content,
                    "category_id": category_id,
                    "author_name": author_name,
                    "status": "draft",  # Start as draft for review
                    "featured": False,
                    "seo_title": seo_title,
                    "seo_description": seo_description,
                    "reading_time": reading_time
                }
            )
            blog_post_id = result.fetchone()[0]
            
            # Insert blog post tags
            for tag_id in tag_ids:
                await session.execute(
                    text("""
                        INSERT INTO blog_post_tags (blog_post_id, blog_tag_id) 
                        VALUES (:blog_post_id, :tag_id)
                        ON CONFLICT DO NOTHING
                    """),
                    {"blog_post_id": blog_post_id, "tag_id": tag_id}
                )
            
            # Insert blog post products
            for product in products:
                await session.execute(
                    text("""
                        INSERT INTO blog_post_products (
                            blog_post_id, product_id, position, context
                        ) VALUES (:blog_post_id, :product_id, :position, :context)
                    """),
                    {
                        "blog_post_id": blog_post_id,
                        "product_id": product['product_id'],
                        "position": product['position'],
                        "context": product['context']
                    }
                )
            
            await session.commit()
            
            print(f"✅ Created blog post: '{title}' (ID: {blog_post_id})")
            return blog_post_id
            
    except Exception as e:
        print(f"❌ Failed to create blog post from {custom_id}: {e}")
        return None

async def process_batch_file(batch_output_file: str):
    """Process the batch output file and create blog posts"""
    
    if not os.path.exists(batch_output_file):
        print(f"❌ Batch output file not found: {batch_output_file}")
        return
    
    print(f"🚀 Processing batch results from: {batch_output_file}")
    
    success_count = 0
    error_count = 0
    
    with open(batch_output_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                # Parse JSONL line
                batch_result = json.loads(line.strip())
                
                custom_id = batch_result.get('custom_id', f'line-{line_num}')
                
                # Check if request was successful
                if batch_result.get('response', {}).get('status_code') != 200:
                    print(f"⚠️  Skipping {custom_id}: API request failed")
                    error_count += 1
                    continue
                
                # Extract the generated content
                response_body = batch_result.get('response', {}).get('body', {})
                choices = response_body.get('choices', [])
                
                if not choices:
                    print(f"⚠️  Skipping {custom_id}: No choices in response")
                    error_count += 1
                    continue
                
                content = choices[0].get('message', {}).get('content', '')
                
                if not content:
                    print(f"⚠️  Skipping {custom_id}: Empty content")
                    error_count += 1
                    continue
                
                # Extract JSON from content
                blog_data = extract_json_from_content(content)
                
                if not blog_data:
                    print(f"⚠️  Skipping {custom_id}: Could not extract valid JSON")
                    error_count += 1
                    continue
                
                # Validate structure
                if not validate_blog_structure(blog_data):
                    print(f"⚠️  Skipping {custom_id}: Invalid blog structure")
                    error_count += 1
                    continue
                
                # Insert blog post
                blog_post_id = await insert_blog_post(blog_data, custom_id)
                
                if blog_post_id:
                    success_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                print(f"❌ Error processing line {line_num}: {e}")
                error_count += 1
    
    print(f"\n🎉 Batch processing completed!")
    print(f"✅ Successfully created: {success_count} blog posts")
    print(f"❌ Errors: {error_count}")
    
    if success_count > 0:
        print(f"\n📝 Next steps:")
        print(f"1. Review draft posts in your admin panel")
        print(f"2. Edit/approve posts as needed")
        print(f"3. Publish approved posts")

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Process OpenAI batch results and create blog posts')
    parser.add_argument('batch_file', help='Path to the batch output JSONL file')
    
    args = parser.parse_args()
    
    try:
        await process_batch_file(args.batch_file)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
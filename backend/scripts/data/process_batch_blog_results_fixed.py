#!/usr/bin/env python3
"""
Fixed version of batch blog results processor.
Properly handles AI metadata, template detection, and content processing.
"""

import asyncio
import sys
import os
import json
import re
import random
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
    
    return True

def strip_html_tags(text: str) -> str:
    """Remove HTML tags and clean up text"""
    if not text:
        return ""
    
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', str(text))
    
    # Clean up extra whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    return clean_text

def extract_template_from_meta(blog_data: Dict[Any, Any]) -> str:
    """Extract template name from meta.content_type field"""
    meta = blog_data.get('meta', {})
    content_type = meta.get('content_type', '')
    
    # Map content types back to template names
    template_mapping = {
        'ultimate_2025_buying_guide': 'Ultimate 2025 Buying Guide',
        'head-to-head_battle:_product_showdown': 'High-Converting Product Battle',
        'head_to_head_battle_product_showdown': 'High-Converting Product Battle',
        'budget_hero_finder': 'Budget Hero Finder',
        'professional_deep_dive_review': 'Professional Deep Dive Review',
        'affiliate_roundup:_best_picks': 'Affiliate Roundup: Best Picks',
        'affiliate_roundup_best_picks': 'Affiliate Roundup: Best Picks'
    }
    
    # Try exact match first
    if content_type in template_mapping:
        return template_mapping[content_type]
    
    # Try fuzzy matching
    content_type_clean = content_type.lower().replace(':', '_').replace(' ', '_')
    for key, template in template_mapping.items():
        if key in content_type_clean or content_type_clean in key:
            return template
    
    # Default fallback based on keywords
    if 'buying' in content_type.lower() or 'guide' in content_type.lower():
        return 'Ultimate 2025 Buying Guide'
    elif 'battle' in content_type.lower() or 'vs' in content_type.lower():
        return 'High-Converting Product Battle'
    elif 'review' in content_type.lower():
        return 'Professional Deep Dive Review'
    elif 'roundup' in content_type.lower():
        return 'Affiliate Roundup: Best Picks'
    
    return 'Ultimate 2025 Buying Guide'  # Default fallback

def create_clean_content(blog_data: Dict[Any, Any]) -> str:
    """Create clean markdown content from structured sections"""
    content_parts = []
    
    for section in blog_data.get('sections', []):
        # Add section title
        title = section.get('title')
        if title:
            content_parts.append(f"## {title}")
        
        # Add clean content without HTML
        content = section.get('content', '')
        if content:
            clean_content = strip_html_tags(content)
            content_parts.append(clean_content)
        
        # Handle product showcase sections
        if section.get('type') == 'product_showcase' and 'products' in section:
            content_parts.append("### Featured Products")
            for i, product in enumerate(section['products'], 1):
                if 'context' in product:
                    clean_context = strip_html_tags(product['context'])
                    content_parts.append(f"**Product {i}:** {clean_context}")
    
    return '\n\n'.join(content_parts) if content_parts else blog_data.get('excerpt', '')

def extract_product_references(blog_data: Dict[Any, Any]) -> List[Dict[str, Any]]:
    """Extract product references from structured content"""
    products = []
    
    for section in blog_data.get('sections', []):
        # Handle product showcase sections
        if section.get('type') == 'product_showcase' and 'products' in section:
            for product in section['products']:
                if 'product_id' in product:
                    products.append({
                        'product_id': product['product_id'],
                        'context': strip_html_tags(product.get('context', '')),
                        'position': product.get('position', len(products) + 1)
                    })
    
    return products

async def get_random_author() -> str:
    """Get a random author name"""
    authors = [
        "Alex Rodriguez", "Sarah Chen", "Mike Johnson", "Emily Davis", 
        "David Kim", "Jessica Taylor", "Chris Martinez", "Anna Wilson",
        "Ryan Thompson", "Maria Garcia", "James Brown", "Lisa Anderson"
    ]
    return random.choice(authors)

async def create_tags(tag_names: List[str]) -> List[int]:
    """Create or get existing tags and return their IDs"""
    if not tag_names:
        return []
    
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
                try:
                    result = await session.execute(
                        text("""
                            INSERT INTO blog_tags (name, slug) 
                            VALUES (:name, :slug) 
                            ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name
                            RETURNING id
                        """),
                        {
                            "name": tag_name,
                            "slug": clean_slug(tag_name)
                        }
                    )
                    tag_ids.append(result.fetchone()[0])
                except Exception as e:
                    print(f"  ⚠️  Warning: Could not create tag '{tag_name}': {e}")
        
        await session.commit()
    
    return tag_ids

async def insert_blog_post(blog_data: Dict[Any, Any], custom_id: str) -> Optional[int]:
    """Insert a blog post into the database with proper AI metadata"""
    
    try:
        # Extract basic data
        title = blog_data.get('title', 'Untitled')
        excerpt = blog_data.get('excerpt', '')
        seo_title = blog_data.get('seo_title') or title
        seo_description = blog_data.get('seo_description', '')
        reading_time = blog_data.get('reading_time', 5)
        
        # Get random author
        author_name = await get_random_author()
        
        # Extract template name from meta
        generation_model = extract_template_from_meta(blog_data)
        
        # Create clean content without HTML artifacts
        content = create_clean_content(blog_data)
        structured_content = json.dumps(blog_data)
        
        # Create slug
        slug = clean_slug(title)
        
        # Get or create category
        category_id = 1  # Default category
        
        # Extract tags
        tags = blog_data.get('tags', [])
        tag_ids = await create_tags(tags)
        
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
            
            # Insert blog post with AI metadata
            result = await session.execute(
                text("""
                    INSERT INTO blog_posts (
                        title, slug, excerpt, content, structured_content,
                        category_id, author_name, status, featured, 
                        seo_title, seo_description, reading_time,
                        generated_by_ai, generation_model,
                        created_at, updated_at
                    ) VALUES (
                        :title, :slug, :excerpt, :content, :structured_content,
                        :category_id, :author_name, :status, :featured,
                        :seo_title, :seo_description, :reading_time,
                        :generated_by_ai, :generation_model,
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
                    "reading_time": reading_time,
                    "generated_by_ai": True,  # Mark as AI generated
                    "generation_model": generation_model  # Store template name
                }
            )
            blog_post_id = result.fetchone()[0]
            
            # Insert blog post tags
            for tag_id in tag_ids:
                try:
                    await session.execute(
                        text("""
                            INSERT INTO blog_post_tags (blog_post_id, tag_id) 
                            VALUES (:blog_post_id, :tag_id)
                            ON CONFLICT DO NOTHING
                        """),
                        {"blog_post_id": blog_post_id, "tag_id": tag_id}
                    )
                except Exception as e:
                    print(f"  ⚠️  Warning: Could not link tag {tag_id}: {e}")
            
            # Insert blog post products
            for product in products:
                try:
                    await session.execute(
                        text("""
                            INSERT INTO blog_post_products (
                                blog_post_id, product_id, position, context
                            ) VALUES (:blog_post_id, :product_id, :position, :context)
                            ON CONFLICT (blog_post_id, product_id) DO UPDATE SET
                                position = EXCLUDED.position,
                                context = EXCLUDED.context
                        """),
                        {
                            "blog_post_id": blog_post_id,
                            "product_id": product['product_id'],
                            "position": product['position'],
                            "context": product['context']
                        }
                    )
                except Exception as e:
                    print(f"  ⚠️  Warning: Could not link product {product['product_id']}: {e}")
            
            await session.commit()
            
            print(f"✅ Created blog post: '{title}' (ID: {blog_post_id})")
            print(f"   Template: {generation_model}")
            print(f"   Author: {author_name}")
            print(f"   Content: {len(content)} chars")
            print(f"   Products: {len(products)}")
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
        print(f"2. Check template detection and content quality")
        print(f"3. Verify product associations")
        print(f"4. Publish approved posts")

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Process OpenAI batch results (FIXED VERSION)')
    parser.add_argument('batch_file', help='Path to the batch output JSONL file')
    
    args = parser.parse_args()
    
    try:
        await process_batch_file(args.batch_file)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
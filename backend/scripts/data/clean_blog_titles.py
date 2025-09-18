#!/usr/bin/env python3
"""
Clean Blog Titles Script - Remove year references from existing blog post titles
Makes blog posts evergreen by removing year-specific references
"""

import asyncio
import sys
import os
import re

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

class BlogTitleCleaner:
    def __init__(self):
        self.updated_count = 0
        self.errors = []
    
    def clean_title(self, title: str) -> str:
        """Clean title by removing year references and making it evergreen"""
        # Remove year references like "2024", "2025", etc.
        title = re.sub(r'\s+(20\d{2})\s*', ' ', title)
        title = re.sub(r'\s+(20\d{2})$', '', title)
        title = re.sub(r'^(20\d{2})\s+', '', title)
        
        # Remove "Edition" references that are year-specific
        title = re.sub(r'\s+Edition\s*$', '', title)
        
        # Clean up extra spaces
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title
    
    async def clean_all_titles(self):
        """Clean all blog post titles in the database"""
        print("🧹 Cleaning blog post titles to make them evergreen...")
        
        async with async_session_factory() as session:
            # Get all blog posts with titles
            result = await session.execute(text("""
                SELECT id, title, slug 
                FROM blog_posts 
                WHERE title IS NOT NULL AND title != ''
                ORDER BY id
            """))
            
            posts = result.fetchall()
            print(f"Found {len(posts)} blog posts to check")
            
            for post in posts:
                post_id, original_title, original_slug = post
                cleaned_title = self.clean_title(original_title)
                
                # Only update if the title actually changed
                if cleaned_title != original_title:
                    try:
                        # Generate new slug from cleaned title
                        new_slug = re.sub(r'[^\w\s-]', '', cleaned_title.lower())
                        new_slug = re.sub(r'[\s_-]+', '-', new_slug).strip('-')
                        
                        # Ensure slug is unique
                        original_new_slug = new_slug
                        counter = 1
                        while True:
                            check_result = await session.execute(
                                text("SELECT id FROM blog_posts WHERE slug = :slug AND id != :id"),
                                {'slug': new_slug, 'id': post_id}
                            )
                            if not check_result.fetchone():
                                break
                            new_slug = f"{original_new_slug}-{counter}"
                            counter += 1
                        
                        # Update the post
                        await session.execute(text("""
                            UPDATE blog_posts 
                            SET title = :title, slug = :slug, updated_at = NOW()
                            WHERE id = :id
                        """), {
                            'title': cleaned_title,
                            'slug': new_slug,
                            'id': post_id
                        })
                        
                        self.updated_count += 1
                        print(f"✅ Updated post {post_id}: '{original_title}' → '{cleaned_title}'")
                        
                    except Exception as e:
                        error_msg = f"Error updating post {post_id}: {str(e)}"
                        self.errors.append(error_msg)
                        print(f"❌ {error_msg}")
            
            await session.commit()
        
        print(f"\n🎉 Title cleaning completed!")
        print(f"✅ Updated: {self.updated_count} blog posts")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.errors:
            print("\nErrors encountered:")
            for error in self.errors:
                print(f"  - {error}")

async def main():
    cleaner = BlogTitleCleaner()
    await cleaner.clean_all_titles()

if __name__ == "__main__":
    asyncio.run(main())

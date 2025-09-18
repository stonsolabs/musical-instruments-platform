#!/usr/bin/env python3
"""
Clean Blog Posts Script - Remove all existing blog posts to start fresh
Cleans up problematic blog posts with content display issues
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

class BlogPostCleaner:
    def __init__(self):
        self.deleted_count = 0
        self.errors = []
    
    async def clean_all_posts(self):
        """Remove all existing blog posts and related data"""
        print("🧹 Cleaning up all existing blog posts...")
        
        async with async_session_factory() as session:
            try:
                # Get count of posts to delete
                result = await session.execute(text("SELECT COUNT(*) FROM blog_posts"))
                total_posts = result.scalar_one()
                print(f"Found {total_posts} blog posts to delete")
                
                if total_posts == 0:
                    print("No blog posts to clean up")
                    return
                
                # Delete in correct order to respect foreign key constraints
                print("Deleting blog post products...")
                await session.execute(text("DELETE FROM blog_post_products"))
                
                print("Deleting blog content sections...")
                await session.execute(text("DELETE FROM blog_content_sections"))
                
                print("Deleting blog post tags...")
                await session.execute(text("DELETE FROM blog_post_tags"))
                
                print("Deleting blog posts...")
                await session.execute(text("DELETE FROM blog_posts"))
                
                # Reset sequences
                print("Resetting sequences...")
                await session.execute(text("ALTER SEQUENCE blog_posts_id_seq RESTART WITH 1"))
                await session.execute(text("ALTER SEQUENCE blog_content_sections_id_seq RESTART WITH 1"))
                await session.execute(text("ALTER SEQUENCE blog_post_products_id_seq RESTART WITH 1"))
                await session.execute(text("ALTER SEQUENCE blog_post_tags_id_seq RESTART WITH 1"))
                
                await session.commit()
                self.deleted_count = total_posts
                
                print(f"✅ Successfully deleted {self.deleted_count} blog posts and related data")
                
            except Exception as e:
                await session.rollback()
                error_msg = f"Error cleaning blog posts: {str(e)}"
                self.errors.append(error_msg)
                print(f"❌ {error_msg}")
        
        print(f"\n🎉 Blog cleanup completed!")
        print(f"✅ Deleted: {self.deleted_count} blog posts")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.errors:
            print("\nErrors encountered:")
            for error in self.errors:
                print(f"  - {error}")

async def main():
    cleaner = BlogPostCleaner()
    await cleaner.clean_all_posts()

if __name__ == "__main__":
    asyncio.run(main())
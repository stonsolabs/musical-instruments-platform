"""
Clean all existing blog posts to start fresh with enhanced templates.
This script safely removes all blog posts and related data.

Run:
  ENVIRONMENT=production python3.11 clean_blog_posts.py
"""
import asyncio
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

async def get_blog_posts_count():
    """Get current count of blog posts"""
    async with async_session_factory() as session:
        result = await session.execute(
            text("SELECT COUNT(*) FROM blog_posts")
        )
        return result.scalar()

async def clean_blog_data():
    """Clean all blog posts and related data"""
    async with async_session_factory() as session:
        
        print("🧹 Starting blog cleanup process...")
        
        # Get initial count
        initial_count = await get_blog_posts_count()
        print(f"📊 Found {initial_count} blog posts to delete")
        
        if initial_count == 0:
            print("✅ No blog posts to delete")
            return
        
        # Delete in correct order to avoid foreign key constraints
        tables_to_clean = [
            ("blog_post_tags", "blog post tags"),
            ("blog_post_products", "blog post products"), 
            ("blog_generation_history", "generation history"),
            ("blog_posts", "blog posts")
        ]
        
        deleted_counts = {}
        
        for table, description in tables_to_clean:
            try:
                # Get count before deletion
                result = await session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count_before = result.scalar()
                
                if count_before > 0:
                    # Delete all records
                    result = await session.execute(text(f"DELETE FROM {table}"))
                    deleted_counts[description] = count_before
                    print(f"  🗑️  Deleted {count_before} {description}")
                else:
                    print(f"  ✅ No {description} to delete")
                    
            except Exception as e:
                print(f"  ❌ Error deleting {description}: {e}")
                await session.rollback()
                raise
        
        # Reset sequences to start from 1
        try:
            await session.execute(text("ALTER SEQUENCE blog_posts_id_seq RESTART WITH 1"))
            await session.execute(text("ALTER SEQUENCE blog_generation_history_id_seq RESTART WITH 1"))
            print("  🔄 Reset ID sequences")
        except Exception as e:
            print(f"  ⚠️  Warning: Could not reset sequences: {e}")
        
        # Commit all changes
        await session.commit()
        
        # Verify cleanup
        final_count = await get_blog_posts_count()
        
        print(f"\n🎉 Blog cleanup completed!")
        print(f"📊 Summary:")
        for description, count in deleted_counts.items():
            print(f"  • {description}: {count} deleted")
        print(f"📊 Final blog posts count: {final_count}")
        
        if final_count == 0:
            print("✅ All blog data successfully cleaned")
        else:
            print(f"⚠️  Warning: {final_count} blog posts remain")
        
        return deleted_counts

async def main():
    """Main execution function"""
    try:
        print("🚀 Starting blog cleanup for fresh start...")
        print("⚠️  This will DELETE ALL existing blog posts!")
        
        # Confirm deletion (in production, you might want to add a confirmation)
        deleted_counts = await clean_blog_data()
        
        print(f"\n✨ Ready for fresh blog content generation!")
        print(f"📋 Next steps:")
        print(f"  1. Generate new batch with enhanced templates") 
        print(f"  2. Process batch results")
        print(f"  3. Review and publish quality content")
        print(f"  4. Monitor performance and conversion")
        
    except Exception as e:
        print(f"💥 Error during cleanup: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
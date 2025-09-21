#!/usr/bin/env python3
"""
Script to fix duplicate blog post titles by making them unique
"""

import asyncio
import json
from typing import Dict, List, Any
from sqlalchemy import text
from app.database import async_session_factory

class DuplicateTitleFixer:
    def __init__(self):
        self.title_variations = {
            "Ultimate Guide to Gear Tips: Master Your Music Setup": [
                "Ultimate Guide to Gear Tips: Master Your Music Setup",
                "Essential Gear Tips for Musicians: Master Your Setup", 
                "Pro Gear Tips: Optimizing Your Music Setup for Success"
            ],
            "Ultimate Guide to Instrument History: Evolution & Icons": [
                "Ultimate Guide to Instrument History: Evolution & Icons",
                "Musical Instrument History: From Origins to Modern Icons",
                "The Story of Musical Instruments: Evolution Through Time"
            ]
        }
    
    async def find_duplicate_titles(self):
        """Find all duplicate titles"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT title, COUNT(*) as count
                FROM blog_posts
                GROUP BY title
                HAVING COUNT(*) > 1
                ORDER BY count DESC, title
            '''))
            
            return result.fetchall()
    
    async def get_posts_with_title(self, title: str):
        """Get all posts with a specific title"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT id, title, created_at, seo_title, excerpt
                FROM blog_posts
                WHERE title = :title
                ORDER BY created_at ASC
            '''), {'title': title})
            
            return result.fetchall()
    
    async def update_post_title(self, post_id: int, new_title: str, new_seo_title: str, dry_run: bool = True):
        """Update a post's title"""
        async with async_session_factory() as session:
            if not dry_run:
                await session.execute(text('''
                    UPDATE blog_posts 
                    SET title = :new_title, seo_title = :new_seo_title
                    WHERE id = :post_id
                '''), {
                    'post_id': post_id,
                    'new_title': new_title,
                    'new_seo_title': new_seo_title
                })
                await session.commit()
                print(f"  ✅ Updated post {post_id} title to: {new_title}")
            else:
                print(f"  🔍 Would update post {post_id} title to: {new_title}")
    
    async def fix_duplicates(self, dry_run: bool = True):
        """Fix all duplicate titles"""
        duplicates = await self.find_duplicate_titles()
        
        if not duplicates:
            print("No duplicate titles found!")
            return
        
        print(f"Found {len(duplicates)} duplicate titles to fix:")
        
        total_fixed = 0
        
        for original_title, count in duplicates:
            print(f"\n📝 Fixing: \"{original_title}\" ({count} duplicates)")
            
            # Get all posts with this title
            posts = await self.get_posts_with_title(original_title)
            
            # Get title variations
            variations = self.title_variations.get(original_title, [original_title])
            
            # If we don't have enough variations, generate them
            while len(variations) < len(posts):
                base_title = original_title.replace("Ultimate Guide to ", "")
                variations.extend([
                    f"Complete Guide to {base_title}",
                    f"Expert Guide to {base_title}",
                    f"Professional Guide to {base_title}",
                    f"Comprehensive Guide to {base_title}",
                    f"Essential Guide to {base_title}"
                ])
            
            # Update each post with a unique title (keep first one as-is)
            for i, (post_id, title, created_at, seo_title, excerpt) in enumerate(posts):
                if i == 0:
                    print(f"  ➡️  Post {post_id}: Keeping original title")
                    continue
                
                new_title = variations[i] if i < len(variations) else f"{original_title} #{i+1}"
                new_seo_title = new_title  # Update SEO title to match
                
                await self.update_post_title(post_id, new_title, new_seo_title, dry_run)
                total_fixed += 1
        
        print(f"\n🎉 {total_fixed} posts {'would be' if dry_run else 'were'} updated with unique titles")
    
    async def verify_no_duplicates(self):
        """Verify no duplicates remain"""
        duplicates = await self.find_duplicate_titles()
        
        if duplicates:
            print(f"⚠️  Still found {len(duplicates)} duplicate titles:")
            for title, count in duplicates:
                print(f"  \"{title}\" appears {count} times")
        else:
            print("✅ No duplicate titles found!")

async def main():
    print("🔧 Duplicate Title Fixer")
    print("=" * 50)
    
    fixer = DuplicateTitleFixer()
    
    # Show current duplicates
    print("\n📊 Analyzing duplicate titles...")
    duplicates = await fixer.find_duplicate_titles()
    
    if not duplicates:
        print("✅ No duplicate titles found!")
        return
    
    print(f"Found {len(duplicates)} duplicate titles:")
    for title, count in duplicates:
        print(f"  \"{title}\" appears {count} times")
    
    # Fix duplicates (dry run first)
    print("\n🔍 Running dry run to fix duplicates...")
    await fixer.fix_duplicates(dry_run=True)
    
    # Ask for confirmation
    print("\n❓ Do you want to apply these changes? (y/N)")
    import sys
    if "--apply" in sys.argv:
        print("✅ Applying changes...")
        await fixer.fix_duplicates(dry_run=False)
        
        print("\n📊 Verifying results...")
        await fixer.verify_no_duplicates()
        print("🎉 Duplicate titles fixed!")
    else:
        print("ℹ️  Dry run completed. Use --apply flag to apply changes.")

if __name__ == "__main__":
    asyncio.run(main())
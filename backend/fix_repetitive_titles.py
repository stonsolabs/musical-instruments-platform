#!/usr/bin/env python3
"""
Script to fix repetitive blog post titles (too many "Ultimate Guide" titles)
Make titles more diverse and engaging
"""

import asyncio
import random
from typing import Dict, List, Any
from sqlalchemy import text
from app.database import async_session_factory

class RepetitiveTitleFixer:
    def __init__(self):
        # Title transformation patterns
        self.title_transforms = {
            # Buying guides
            "Ultimate Guide to": [
                "Your Complete Guide to",
                "Everything You Need to Know About", 
                "The Insider's Guide to",
                "Smart Shopper's Guide to",
                "The Essential Guide to",
                "Mastering the Art of",
                "The Complete Handbook for"
            ],
            
            # Reviews
            "Ultimate": [
                "In-Depth",
                "Comprehensive", 
                "Complete",
                "Professional",
                "Expert",
                "Detailed",
                "Honest"
            ],
            
            # More creative starts
            "creative_starts": [
                "Decode the Secrets of",
                "Unlock the Power of", 
                "Navigate the World of",
                "Master the Art of",
                "Transform Your",
                "Revolutionize Your",
                "Elevate Your"
            ]
        }
        
        # Specific title replacements for different content types
        self.specific_replacements = {
            "buying-guide": [
                "Smart Buying: {}",
                "Your {} Shopping Blueprint", 
                "Finding the Perfect {}",
                "The {}: Buyer's Complete Roadmap",
                "Shopping Smart: {}",
                "Your {} Investment Guide",
                "The {} Purchase Decision Guide"
            ],
            "review": [
                "Real World Test: {}",
                "Hands-On with the {}",
                "Inside Look: {}",
                "Breaking Down the {}",
                "Living with the {}: My Experience",
                "The {} Reality Check",
                "{}: Worth Your Money?"
            ],
            "comparison": [
                "{}: The Great Showdown",
                "Battle of the Giants: {}",
                "{}: Which Reigns Supreme?",
                "Head-to-Head: {}",
                "The {} Face-Off",
                "{}: Choosing Your Champion",
                "Clash of Titans: {}"
            ],
            "artist-spotlight": [
                "{}: The Legendary Story",
                "Celebrating {}: Icon & Inspiration", 
                "{}: Music's Revolutionary Force",
                "The {} Legacy: Gear & Genius",
                "{}: Behind the Music & Magic",
                "Icon Spotlight: {}",
                "{}: The Artist Who Changed Everything"
            ],
            "instrument-history": [
                "The {} Story: From Origins to Icons",
                "{}: Evolution of a Legend",
                "How {} Changed Music Forever",
                "The {} Revolution: A Musical Journey",
                "{}: Tracing the Musical Timeline",
                "From Past to Present: The {} Chronicles",
                "The {} Legacy: A Historical Deep Dive"
            ],
            "gear-tips": [
                "{}: Pro Secrets Revealed",
                "Mastering {}: Tips from the Pros",
                "{}: Your Complete Setup Guide",
                "Pro-Level {}: Insider Techniques", 
                "{}: The Professional's Playbook",
                "Optimize Your {}: Expert Strategies",
                "{}: Advanced Techniques Unlocked"
            ],
            "news-feature": [
                "{}: The Industry Game-Changer",
                "How {} is Reshaping Music",
                "The {} Revolution: What It Means",
                "{}: Breaking Down the Impact",
                "Industry Spotlight: {}",
                "{}: The Future is Here",
                "The {} Phenomenon Explained"
            ]
        }
    
    async def find_repetitive_titles(self):
        """Find titles that start with repetitive phrases"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT id, title, content_json, created_at
                FROM blog_posts
                WHERE title LIKE 'Ultimate Guide%' 
                   OR title LIKE 'The Ultimate%'
                   OR title LIKE 'Ultimate %'
                ORDER BY created_at DESC
            '''))
            
            posts = []
            for row in result.fetchall():
                post_id, title, content_json, created_at = row
                category = None
                if content_json and isinstance(content_json, dict):
                    category = content_json.get('category')
                posts.append((post_id, title, category, created_at))
            
            return posts
    
    def generate_new_title(self, old_title: str, category: str = None) -> str:
        """Generate a new, more creative title"""
        
        # Extract the main topic from the old title
        topic = old_title
        
        # Remove common prefixes
        for prefix in ["Ultimate Guide to ", "The Ultimate Guide to ", "Ultimate ", "The Ultimate "]:
            if topic.startswith(prefix):
                topic = topic[len(prefix):]
                break
        
        # Remove common suffixes
        for suffix in [": Make the Right Choice", ": Expert Tips & Picks", ": Complete Guide", ": Your Guide"]:
            if topic.endswith(suffix):
                topic = topic[:-len(suffix)]
                break
        
        # Use category-specific templates if available
        if category and category in self.specific_replacements:
            templates = self.specific_replacements[category]
            template = random.choice(templates)
            return template.format(topic)
        
        # General transformations
        if "Guide to" in old_title:
            new_start = random.choice(self.title_transforms["Ultimate Guide to"])
            return f"{new_start} {topic}"
        
        if old_title.startswith("Ultimate"):
            new_start = random.choice(self.title_transforms["Ultimate"])
            return f"{new_start} {topic}"
        
        # Creative alternatives
        creative_start = random.choice(self.title_transforms["creative_starts"])
        return f"{creative_start} {topic}"
    
    async def update_post_title(self, post_id: int, new_title: str, dry_run: bool = True):
        """Update a post's title and SEO title"""
        async with async_session_factory() as session:
            if not dry_run:
                # Also update SEO title to match
                new_seo_title = f"{new_title} | GetYourMusicGear.com"
                
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
                print(f"  ✅ Updated post {post_id}")
            else:
                print(f"  🔍 Would update post {post_id}")
            
            print(f"    Old: {await self.get_post_title(post_id)}")
            print(f"    New: {new_title}")
    
    async def get_post_title(self, post_id: int) -> str:
        """Get current title of a post"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT title FROM blog_posts WHERE id = :post_id
            '''), {'post_id': post_id})
            
            row = result.fetchone()
            return row[0] if row else ""
    
    async def fix_repetitive_titles(self, dry_run: bool = True, limit: int = None):
        """Fix repetitive titles"""
        repetitive_posts = await self.find_repetitive_titles()
        
        if not repetitive_posts:
            print("No repetitive titles found!")
            return
        
        print(f"Found {len(repetitive_posts)} repetitive titles to fix")
        
        if limit:
            repetitive_posts = repetitive_posts[:limit]
            print(f"Processing first {limit} posts...")
        
        fixed_count = 0
        
        for post_id, old_title, category, created_at in repetitive_posts:
            print(f"\n📝 Post {post_id} ({category or 'unknown'}):")
            
            # Generate new title
            new_title = self.generate_new_title(old_title, category)
            
            # Make sure it's different
            if new_title == old_title:
                new_title = f"Your Complete Guide to {old_title.replace('Ultimate Guide to ', '')}"
            
            await self.update_post_title(post_id, new_title, dry_run)
            fixed_count += 1
        
        print(f"\n🎉 {fixed_count} posts {'would be' if dry_run else 'were'} updated with diverse titles")
    
    async def analyze_title_patterns(self):
        """Analyze current title patterns"""
        async with async_session_factory() as session:
            # Count titles by starting phrase
            patterns = [
                "Ultimate Guide%",
                "The Ultimate%", 
                "Ultimate %",
                "Best %",
                "Top %",
                "Complete Guide%",
                "How to %"
            ]
            
            print("📊 Title Pattern Analysis:")
            for pattern in patterns:
                result = await session.execute(text('''
                    SELECT COUNT(*) FROM blog_posts WHERE title LIKE :pattern
                '''), {'pattern': pattern})
                
                count = result.fetchone()[0]
                if count > 0:
                    print(f"  '{pattern.replace('%', '...')}': {count} posts")

async def main():
    print("🎨 Repetitive Title Fixer")
    print("=" * 50)
    
    fixer = RepetitiveTitleFixer()
    
    # Analyze current patterns
    print("\n📊 Analyzing title patterns...")
    await fixer.analyze_title_patterns()
    
    # Show repetitive titles
    repetitive = await fixer.find_repetitive_titles()
    print(f"\nFound {len(repetitive)} posts with repetitive 'Ultimate' titles")
    
    if not repetitive:
        print("✅ No repetitive titles found!")
        return
    
    # Fix titles (dry run first, limit to 20 for testing)
    print("\n🔍 Running dry run to fix repetitive titles (first 20)...")
    await fixer.fix_repetitive_titles(dry_run=True, limit=20)
    
    # Ask for confirmation
    print("\n❓ Do you want to apply these changes to ALL repetitive titles? (y/N)")
    import sys
    if "--apply" in sys.argv:
        print("✅ Applying changes to all repetitive titles...")
        await fixer.fix_repetitive_titles(dry_run=False)
        
        print("\n📊 Updated title patterns:")
        await fixer.analyze_title_patterns()
        print("🎉 Repetitive titles diversified!")
    else:
        print("ℹ️  Dry run completed. Use --apply flag to apply changes.")

if __name__ == "__main__":
    asyncio.run(main())
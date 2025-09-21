#!/usr/bin/env python3
"""
Script to delete existing blog posts and regenerate them with improved product matching
"""

import asyncio
import json
from typing import List
from sqlalchemy import text
from app.database import async_session_factory
from app.services.improved_blog_generator import ImprovedBlogGenerator

class BlogRegenerator:
    def __init__(self):
        self.generator = ImprovedBlogGenerator()
        
    async def delete_existing_posts(self, confirm: bool = False):
        """Delete existing blog posts"""
        async with async_session_factory() as session:
            # Count existing posts
            result = await session.execute(text('''
                SELECT COUNT(*) FROM blog_posts
            '''))
            count = result.fetchone()[0]
            
            print(f"Found {count} existing blog posts")
            
            if not confirm:
                print("Run with --confirm to actually delete posts")
                return
            
            # Delete all blog posts
            await session.execute(text('''
                DELETE FROM blog_posts
            '''))
            await session.commit()
            
            print(f"✅ Deleted {count} blog posts")
    
    async def generate_new_batch(self, num_posts: int = 100):
        """Generate a new batch of blog posts with improved product matching"""
        
        await self.generator.initialize()
        
        # Diverse blog post ideas with better templates
        blog_ideas = [
            # AKAI/MIDI Controller focused posts
            ("AKAI MPK Mini MK3 Black: Compact MIDI Powerhouse", "review"),
            ("AKAI MPK Mini Plus: Feature-Packed Controller Review", "review"),
            ("AKAI MPC Key: The Ultimate Standalone Workstation", "review"),
            ("AKAI APC Key 25: Perfect Ableton Companion", "review"),
            ("MIDI Controller Showdown: AKAI vs Arturia vs Novation", "comparison"),
            ("Building Your First Home Studio: MIDI Controller Guide", "buying-guide"),
            
            # Guitar focused posts
            ("Fender Telecaster vs Stratocaster: Iconic Guitar Battle", "comparison"),
            ("Gibson Les Paul: The Rock Legend's Complete Guide", "review"),
            ("Electric Guitar Shopping: Beginner to Pro Selection", "buying-guide"),
            ("Vintage Guitar Collecting: Investment Grade Instruments", "buying-guide"),
            ("Guitar Amplifier Guide: Tube vs Solid State vs Digital", "comparison"),
            ("Setting Up Your Guitar: Professional Setup Guide", "gear-tips"),
            
            # Piano/Keyboard posts
            ("Roland FP-30X vs Yamaha P-125: Digital Piano Battle", "comparison"),
            ("Kawai Digital Pianos: Finding Your Perfect Touch", "buying-guide"),
            ("Stage Piano Guide: Professional Performance Keyboards", "buying-guide"),
            ("Home Recording with Digital Pianos: Complete Setup", "gear-tips"),
            ("Piano Learning: Acoustic vs Digital for Beginners", "comparison"),
            
            # Recording/Audio posts
            ("Audio Interface Shopping: Home Studio Essentials", "buying-guide"),
            ("Studio Monitor Selection: Accurate Sound for Mixing", "buying-guide"),
            ("Microphone Guide: Vocals, Instruments, and Podcasting", "buying-guide"),
            ("Budget Home Studio: Professional Results Under $1000", "buying-guide"),
            ("Recording Electric Guitar: Amp vs Interface vs Both", "gear-tips"),
            
            # Artist spotlights (with relevant gear)
            ("Jimi Hendrix: The Guitar Revolutionary and His Gear", "artist-spotlight"),
            ("Herbie Hancock: Jazz Piano Pioneer and Synthesizer Master", "artist-spotlight"),
            ("Stevie Wonder: Keyboard Genius and Studio Innovation", "artist-spotlight"),
            ("Eddie Van Halen: Guitar Innovation and Tone Mastery", "artist-spotlight"),
            ("Quincy Jones: Producer's Approach to Studio Gear", "artist-spotlight"),
            
            # Instrument history
            ("The Electric Guitar Revolution: From Jazz to Rock", "instrument-history"),
            ("Synthesizer Evolution: From Moog to Modern Digital", "instrument-history"),
            ("The Drum Kit: From Jazz Traps to Modern Electronic", "instrument-history"),
            ("Digital Piano Development: Sampling Technology Progress", "instrument-history"),
            ("MIDI: The Protocol That Connected Music Technology", "instrument-history"),
            
            # Gear tips and maintenance
            ("Guitar String Guide: Tone, Tension, and Longevity", "gear-tips"),
            ("Keyboard Maintenance: Keeping Your Keys Responsive", "gear-tips"),
            ("Cable Management for Musicians: Signal Quality Tips", "gear-tips"),
            ("Instrument Storage: Protecting Your Musical Investment", "gear-tips"),
            ("Live Performance Setup: Reliability and Redundancy", "gear-tips"),
            
            # Brand comparisons and reviews
            ("Yamaha vs Roland: The Synthesizer Giants Compared", "comparison"),
            ("Fender vs Gibson: Guitar Legacy and Modern Innovation", "comparison"),
            ("Audio-Technica vs Shure: Microphone Quality Showdown", "comparison"),
            ("Native Instruments vs Arturia: Software Controller Battle", "comparison"),
            
            # News and trends
            ("Digital Audio Workstation Evolution: Modern Production", "news-feature"),
            ("Sustainable Music Gear: Environmental Responsibility", "news-feature"),
            ("AI in Music Production: Creative Tools vs Human Touch", "news-feature"),
            ("Streaming's Impact on Music Gear: Home Studio Boom", "news-feature"),
            ("Vintage Gear Revival: Why Old School Sounds Matter", "news-feature"),
            
            # Specific product reviews with proper matching
            ("Roland Jupiter-X: Modern Take on Classic Synthesis", "review"),
            ("Yamaha MODX: Affordable Workstation Powerhouse", "review"),
            ("Arturia KeyLab MK3: MIDI Controller Excellence", "review"),
            ("Shure SM7B: The Podcast and Vocal Recording Standard", "review"),
            ("Audio-Technica AT2020: Studio Condenser Value Pick", "review"),
        ]
        
        # Generate more ideas if needed
        while len(blog_ideas) < num_posts:
            additional_ideas = [
                ("Professional Guitar Recording Techniques", "gear-tips"),
                ("Home Studio Acoustics: Budget Treatment Solutions", "gear-tips"),
                ("MIDI Programming: Advanced Controller Techniques", "gear-tips"),
                ("Live Sound Setup: Small Venue Audio Guide", "gear-tips"),
                ("Music Production Workflow: Hardware vs Software", "comparison"),
                ("Beginner's Guide to Audio Interfaces", "buying-guide"),
                ("Synthesizer Types: Analog, Digital, and Hybrid", "comparison"),
                ("Guitar Effects Pedals: Building Your Signal Chain", "buying-guide"),
                ("Studio Headphones vs Monitors: When to Use Each", "comparison"),
                ("Music Gear Insurance: Protecting Your Investment", "gear-tips"),
            ]
            blog_ideas.extend(additional_ideas)
        
        # Limit to requested number
        blog_ideas = blog_ideas[:num_posts]
        
        print(f"Generating {len(blog_ideas)} new blog posts...")
        
        generated_count = 0
        failed_count = 0
        
        for i, (topic, template) in enumerate(blog_ideas):
            print(f"\n[{i+1}/{len(blog_ideas)}] Generating: {topic}")
            
            try:
                # Generate blog content
                content = await self.generator.generate_blog_post(topic, template)
                
                # Save to database
                await self._save_blog_post(content, topic, template)
                
                generated_count += 1
                print(f"  ✅ Generated and saved: {content['title']}")
                
                # Show products that were included
                for section in content['sections']:
                    if section.get('type') == 'product_spotlight':
                        product = section.get('product', {})
                        print(f"    📦 Product: {product.get('name', 'Unknown')} (ID: {product.get('id', 'N/A')})")
                
            except Exception as e:
                failed_count += 1
                print(f"  ❌ Failed to generate: {e}")
                continue
        
        print(f"\n🎉 Batch generation complete!")
        print(f"  ✅ Generated: {generated_count} posts")
        print(f"  ❌ Failed: {failed_count} posts")
    
    async def _save_blog_post(self, content: dict, original_topic: str, template: str):
        """Save generated blog post to database"""
        async with async_session_factory() as session:
            # Create slug from title
            import re
            slug = re.sub(r'[^a-zA-Z0-9\s-]', '', content['title'])
            slug = re.sub(r'\s+', '-', slug.strip()).lower()
            
            # Insert blog post
            await session.execute(text('''
                INSERT INTO blog_posts (
                    title, slug, excerpt, content_json, seo_title, seo_description,
                    status, generated_by_ai, generation_model, generation_params,
                    author_name, created_at, updated_at
                ) VALUES (
                    :title, :slug, :excerpt, :content_json, :seo_title, :seo_description,
                    'published', true, 'improved_generator', :generation_params,
                    :author_name, NOW(), NOW()
                )
            '''), {
                'title': content['title'],
                'slug': slug,
                'excerpt': content.get('excerpt', ''),
                'content_json': json.dumps(content),
                'seo_title': content.get('seo_title', content['title']),
                'seo_description': content.get('seo_description', content.get('excerpt', '')),
                'generation_params': json.dumps({
                    'original_topic': original_topic,
                    'template': template,
                    'generation_method': 'improved_product_matching',
                    'word_count': content.get('word_count', 0)
                }),
                'author_name': self._get_random_author()
            })
            
            await session.commit()
    
    def _get_random_author(self) -> str:
        """Get a random author name for blog posts"""
        authors = [
            "Marcus Rodriguez",
            "Sarah Chen", 
            "David Thompson",
            "Lisa Park",
            "James Wilson",
            "Amanda Foster",
            "Michael Garcia",
            "Jennifer Lee",
            "Robert Kim",
            "Catherine Martinez"
        ]
        import random
        return random.choice(authors)

async def main():
    print("🔄 Blog Post Regenerator")
    print("=" * 50)
    
    regenerator = BlogRegenerator()
    
    import sys
    
    # Delete existing posts
    if "--delete" in sys.argv or "--confirm" in sys.argv:
        print("\n🗑️  Deleting existing blog posts...")
        await regenerator.delete_existing_posts(confirm=True)
    else:
        print("\n📊 Checking existing blog posts...")
        await regenerator.delete_existing_posts(confirm=False)
    
    # Generate new batch
    if "--generate" in sys.argv:
        num_posts = 100
        if "--num" in sys.argv:
            try:
                idx = sys.argv.index("--num")
                num_posts = int(sys.argv[idx + 1])
            except (IndexError, ValueError):
                pass
        
        print(f"\n📝 Generating {num_posts} new blog posts...")
        await regenerator.generate_new_batch(num_posts)
    else:
        print("\nℹ️  Use --generate flag to create new posts")
        print("   Use --delete flag to remove existing posts")
        print("   Use --num X to specify number of posts (default: 100)")

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Production Blog Batch Generator
Creates 100 diverse, high-quality blog posts with proper product matching
"""

import asyncio
import json
import random
from typing import List, Tuple
from sqlalchemy import text
from app.database import async_session_factory
from app.services.improved_blog_generator import ImprovedBlogGenerator

class ProductionBlogBatchGenerator:
    def __init__(self):
        self.generator = ImprovedBlogGenerator()
        self.authors = [
            "Marcus Rodriguez",
            "Sarah Chen", 
            "David Thompson",
            "Lisa Park",
            "James Wilson",
            "Amanda Foster",
            "Michael Garcia",
            "Jennifer Lee",
            "Robert Kim",
            "Catherine Martinez",
            "Alex Rivera",
            "Samantha Brooks",
            "Daniel Chang",
            "Rachel Green",
            "Kevin O'Connor"
        ]
        
    async def initialize(self):
        """Initialize the generator"""
        await self.generator.initialize()
        
    def get_comprehensive_blog_topics(self) -> List[Tuple[str, str]]:
        """Generate 100 diverse blog post topics with templates"""
        
        topics = []
        
        # === BUYING GUIDES (25 posts) ===
        buying_guides = [
            ("Best Electric Guitars Under $500: 2024 Buyer's Guide", "buying-guide"),
            ("Acoustic Guitar Shopping: Finding Your Perfect Sound", "buying-guide"),
            ("MIDI Controller Guide: Home Studio Essentials", "buying-guide"),
            ("Digital Piano Buying Guide: Touch, Sound, and Features", "buying-guide"),
            ("Audio Interface Selection: Professional Recording Made Simple", "buying-guide"),
            ("Studio Monitor Guide: Accurate Sound for Home Producers", "buying-guide"),
            ("Microphone Buying Guide: Vocals, Instruments, and Podcasting", "buying-guide"),
            ("Guitar Amplifier Guide: Finding Your Signature Sound", "buying-guide"),
            ("Electric Bass Shopping: 4-String vs 5-String Guide", "buying-guide"),
            ("Home Recording Setup: Complete Beginner's Equipment Guide", "buying-guide"),
            ("Synthesizer Buying Guide: Analog vs Digital vs Software", "buying-guide"),
            ("Drum Kit Selection: Acoustic vs Electronic for Home", "buying-guide"),
            ("Violin Shopping Made Simple: Quality Instruments by Budget", "buying-guide"),
            ("DJ Equipment Essentials: Building Your First Professional Setup", "buying-guide"),
            ("Guitar Pedal Selection: Building Your Effects Chain", "buying-guide"),
            ("Studio Headphones vs Monitors: When to Use Each", "buying-guide"),
            ("MIDI Keyboard Guide: 25, 49, 61, or 88 Keys?", "buying-guide"),
            ("Audio Cable Guide: XLR, TRS, and USB Explained", "buying-guide"),
            ("Condenser vs Dynamic Microphones: Making the Right Choice", "buying-guide"),
            ("Guitar String Guide: Tone, Tension, and Longevity", "buying-guide"),
            ("Portable Recording Gear: Mobile Studio Solutions", "buying-guide"),
            ("Music Production Software: DAW Selection Guide", "buying-guide"),
            ("Live Performance Gear: Stage-Ready Equipment Guide", "buying-guide"),
            ("Budget Home Studio: Professional Results Under $1000", "buying-guide"),
            ("Vintage Gear Shopping: Investment-Grade Instruments", "buying-guide"),
        ]
        
        # === PRODUCT REVIEWS (20 posts) ===
        reviews = [
            ("AKAI MPK Mini MK3: The Ultimate Portable MIDI Controller", "review"),
            ("Roland FP-30X Digital Piano: Professional Performance Review", "review"),
            ("Yamaha P-125 vs Casio PX-770: Digital Piano Showdown", "review"),
            ("Arturia KeyLab 88 MK3: Flagship MIDI Controller Deep Dive", "review"),
            ("Shure SM7B Microphone: The Podcast and Vocal Standard", "review"),
            ("Audio-Technica AT2020: Studio Condenser Value Champion", "review"),
            ("Focusrite Scarlett Solo: Entry-Level Interface Excellence", "review"),
            ("Gibson Les Paul Standard: Rock Legend Status Justified?", "review"),
            ("Fender Player Stratocaster: Modern Classic Performance", "review"),
            ("Martin D-28: Acoustic Guitar Icon Tested", "review"),
            ("Yamaha DGX-670: Feature-Packed Portable Piano Review", "review"),
            ("Native Instruments Komplete Kontrol S61: Premium MIDI Experience", "review"),
            ("KRK Rokit 5 G4: Studio Monitor Performance Analysis", "review"),
            ("Rode PodMic: Purpose-Built Podcasting Microphone Test", "review"),
            ("PreSonus AudioBox USB 96: Budget Interface Excellence", "review"),
            ("Alesis V49: Affordable MIDI Controller Value Test", "review"),
            ("Kawai ES110: Portable Digital Piano Performance Review", "review"),
            ("AKAI MPC Live II: Standalone Production Powerhouse", "review"),
            ("Novation Launchkey 61 MK3: Ableton Integration Master", "review"),
            ("Arturia MiniLab 3: Compact Controller Big Features", "review"),
        ]
        
        # === COMPARISONS (15 posts) ===
        comparisons = [
            ("Yamaha vs Roland Digital Pianos: The Ultimate Showdown", "comparison"),
            ("AKAI vs Arturia MIDI Controllers: Feature Battle", "comparison"),
            ("Fender vs Gibson Electric Guitars: Legendary Rivalry", "comparison"),
            ("Audio-Technica vs Shure Microphones: Sound Quality Face-Off", "comparison"),
            ("Focusrite vs PreSonus Audio Interfaces: Home Studio Battle", "comparison"),
            ("KRK vs Yamaha Studio Monitors: Mixing Accuracy Test", "comparison"),
            ("Martin vs Taylor Acoustic Guitars: Tone Philosophy Clash", "comparison"),
            ("Kawai vs Yamaha Digital Piano Technology Comparison", "comparison"),
            ("Native Instruments vs Arturia Software Controllers", "comparison"),
            ("Condenser vs Dynamic Microphones: Studio Applications", "comparison"),
            ("Tube vs Solid State Guitar Amps: Tone Characteristics", "comparison"),
            ("88-Key vs 61-Key Digital Pianos: Size vs Features", "comparison"),
            ("USB vs XLR Microphones: Connection Type Benefits", "comparison"),
            ("Active vs Passive Studio Monitors: Power Delivery Methods", "comparison"),
            ("Hardware vs Software Synthesizers: Sound Generation Battle", "comparison"),
        ]
        
        # === ARTIST SPOTLIGHTS (12 posts) ===
        artist_spotlights = [
            ("Jimi Hendrix: Revolutionary Guitar Techniques and Gear", "artist-spotlight"),
            ("Herbie Hancock: Jazz Piano Pioneer and Synthesizer Explorer", "artist-spotlight"),
            ("Stevie Wonder: Keyboard Mastery and Studio Innovation", "artist-spotlight"),
            ("Eddie Van Halen: Guitar Innovation and Tone Revolution", "artist-spotlight"),
            ("Keith Emerson: Progressive Rock Keyboard Virtuoso", "artist-spotlight"),
            ("Jaco Pastorius: Electric Bass Revolutionary", "artist-spotlight"),
            ("Rick Wakeman: Symphonic Rock Keyboard Orchestrator", "artist-spotlight"),
            ("Gary Moore: Blues Rock Guitar Legend", "artist-spotlight"),
            ("Chick Corea: Jazz Fusion Piano Master", "artist-spotlight"),
            ("Steve Vai: Technical Guitar Virtuosity", "artist-spotlight"),
            ("Jordan Rudess: Progressive Metal Keyboard Wizard", "artist-spotlight"),
            ("Marcus Miller: Bass Guitar Funk Master", "artist-spotlight"),
        ]
        
        # === INSTRUMENT HISTORY (10 posts) ===
        instrument_history = [
            ("Electric Guitar Evolution: From Jazz Boxes to Metal Machines", "instrument-history"),
            ("Digital Piano Development: Sampling Technology Revolution", "instrument-history"),
            ("MIDI Protocol History: Connecting Music Technology", "instrument-history"),
            ("Synthesizer Evolution: From Moog to Modern Digital", "instrument-history"),
            ("Electric Bass History: From Upright to Electric Innovation", "instrument-history"),
            ("Home Recording Revolution: From 4-Track to Digital", "instrument-history"),
            ("Guitar Amplifier Development: Tube to Solid State to Digital", "instrument-history"),
            ("Drum Machine Evolution: Rhythm Programming History", "instrument-history"),
            ("Audio Interface Development: Analog to Digital Conversion", "instrument-history"),
            ("Music Production Software: DAW Evolution Timeline", "instrument-history"),
        ]
        
        # === GEAR TIPS (10 posts) ===
        gear_tips = [
            ("Guitar Setup and Maintenance: DIY Professional Results", "gear-tips"),
            ("Digital Piano Care: Keeping Your Keys Responsive", "gear-tips"),
            ("Home Studio Acoustics: Budget Room Treatment Solutions", "gear-tips"),
            ("MIDI Controller Programming: Advanced Techniques", "gear-tips"),
            ("Audio Cable Management: Signal Quality and Organization", "gear-tips"),
            ("Microphone Placement Techniques: Capturing Perfect Sound", "gear-tips"),
            ("Live Performance Setup: Reliability and Redundancy", "gear-tips"),
            ("Music Gear Storage: Protecting Your Investment", "gear-tips"),
            ("Recording Level Optimization: Avoiding Clipping and Noise", "gear-tips"),
            ("Software Controller Mapping: Workflow Optimization", "gear-tips"),
        ]
        
        # === NEWS FEATURES (8 posts) ===
        news_features = [
            ("AI in Music Production: Creative Enhancement vs Human Touch", "news-feature"),
            ("Sustainable Music Gear: Environmental Responsibility in Manufacturing", "news-feature"),
            ("Streaming Impact on Music Gear: Home Studio Democratization", "news-feature"),
            ("Vintage Gear Revival: Why Analog Sounds Matter in Digital Age", "news-feature"),
            ("Remote Collaboration Tools: Music Creation in Digital Age", "news-feature"),
            ("Music Education Technology: Learning Instruments in 2024", "news-feature"),
            ("Subscription Music Software: Ownership vs Access Models", "news-feature"),
            ("NFTs and Music Gear: Digital Ownership Revolution", "news-feature"),
        ]
        
        # Combine all topics
        topics.extend(buying_guides)
        topics.extend(reviews)
        topics.extend(comparisons)
        topics.extend(artist_spotlights)
        topics.extend(instrument_history)
        topics.extend(gear_tips)
        topics.extend(news_features)
        
        # Shuffle for variety
        random.shuffle(topics)
        
        return topics[:100]  # Ensure exactly 100 posts
    
    async def delete_existing_posts(self, confirm: bool = False):
        """Delete existing blog posts"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT COUNT(*) FROM blog_posts
            '''))
            count = result.fetchone()[0]
            
            print(f"Found {count} existing blog posts")
            
            if not confirm:
                print("ℹ️  Use --delete flag to remove existing posts")
                return count
            
            # Delete all blog posts
            await session.execute(text('''
                DELETE FROM blog_posts
            '''))
            await session.commit()
            
            print(f"✅ Deleted {count} blog posts")
            return count
    
    async def generate_production_batch(self, num_posts: int = 100):
        """Generate production-quality blog posts"""
        
        await self.initialize()
        
        # Get diverse topics
        topics = self.get_comprehensive_blog_topics()
        topics = topics[:num_posts]
        
        print(f"🚀 Generating {len(topics)} production blog posts...")
        print("📊 Topic distribution:")
        
        # Count by template
        template_counts = {}
        for _, template in topics:
            template_counts[template] = template_counts.get(template, 0) + 1
        
        for template, count in sorted(template_counts.items()):
            print(f"  {template}: {count} posts")
        
        print("\n" + "="*60)
        
        generated_count = 0
        failed_count = 0
        
        for i, (topic, template) in enumerate(topics):
            print(f"\n[{i+1}/{len(topics)}] Generating: {topic}")
            print(f"Template: {template}")
            
            try:
                # Generate blog content
                content = await self.generator.generate_blog_post(
                    topic=topic, 
                    template_name=template,
                    target_words=random.randint(3500, 4500)
                )
                
                # Save to database
                await self._save_blog_post(content, topic, template)
                
                generated_count += 1
                print(f"✅ Generated: {content['title']}")
                print(f"   Word count: {content.get('word_count', 0)}")
                print(f"   Author: {content.get('author_name', 'Unknown')}")
                
                # Show products that were included
                product_count = 0
                for section in content.get('sections', []):
                    if section.get('type') == 'product_spotlight':
                        product = section.get('product', {})
                        product_count += 1
                        print(f"   📦 Product {product_count}: {product.get('name', 'Unknown')} (ID: {product.get('id', 'N/A')})")
                
                if product_count == 0:
                    print("   ⚠️  No product spotlights found")
                
            except Exception as e:
                failed_count += 1
                print(f"❌ Failed: {str(e)[:100]}...")
                continue
        
        print(f"\n🎉 Production batch complete!")
        print(f"✅ Successfully generated: {generated_count} posts")
        print(f"❌ Failed to generate: {failed_count} posts")
        print(f"📊 Success rate: {(generated_count/(generated_count+failed_count)*100):.1f}%")
        
        # Show final statistics
        await self._show_batch_statistics()
    
    async def _save_blog_post(self, content: dict, original_topic: str, template: str):
        """Save generated blog post to database"""
        async with async_session_factory() as session:
            # Create slug from title
            import re
            slug = re.sub(r'[^a-zA-Z0-9\s-]', '', content['title'])
            slug = re.sub(r'\s+', '-', slug.strip()).lower()
            slug = slug[:100]  # Limit slug length
            
            # Ensure unique slug
            base_slug = slug
            counter = 1
            while True:
                result = await session.execute(text('''
                    SELECT COUNT(*) FROM blog_posts WHERE slug = :slug
                '''), {'slug': slug})
                
                if result.fetchone()[0] == 0:
                    break
                    
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Insert blog post
            await session.execute(text('''
                INSERT INTO blog_posts (
                    title, slug, excerpt, content_json, seo_title, seo_description,
                    status, generated_by_ai, generation_model, generation_params,
                    author_name, created_at, updated_at
                ) VALUES (
                    :title, :slug, :excerpt, :content_json, :seo_title, :seo_description,
                    'published', true, 'production_batch_v2', :generation_params,
                    :author_name, NOW(), NOW()
                )
            '''), {
                'title': content['title'],
                'slug': slug,
                'excerpt': content.get('excerpt', '')[:300],  # Limit excerpt
                'content_json': json.dumps(content),
                'seo_title': content.get('seo_title', content['title'])[:200],
                'seo_description': content.get('seo_description', content.get('excerpt', ''))[:300],
                'generation_params': json.dumps({
                    'original_topic': original_topic,
                    'template': template,
                    'generation_method': 'improved_product_matching_v2',
                    'word_count': content.get('word_count', 0),
                    'featured_products': content.get('featured_products', [])
                }),
                'author_name': random.choice(self.authors)
            })
            
            await session.commit()
    
    async def _show_batch_statistics(self):
        """Show statistics of generated batch"""
        async with async_session_factory() as session:
            # Count by template
            result = await session.execute(text('''
                SELECT 
                    generation_params->>'template' as template,
                    COUNT(*) as count,
                    AVG((generation_params->>'word_count')::int) as avg_words
                FROM blog_posts 
                WHERE generated_by_ai = true 
                AND generation_model = 'production_batch_v2'
                GROUP BY generation_params->>'template'
                ORDER BY count DESC
            '''))
            
            print(f"\n📊 Final Batch Statistics:")
            total_posts = 0
            for row in result.fetchall():
                template, count, avg_words = row
                total_posts += count
                print(f"  {template}: {count} posts (avg {avg_words:.0f} words)")
            
            print(f"\nTotal posts in batch: {total_posts}")
            
            # Count products
            result2 = await session.execute(text('''
                SELECT COUNT(DISTINCT jsonb_array_elements_text(generation_params->'featured_products'))
                FROM blog_posts 
                WHERE generated_by_ai = true 
                AND generation_model = 'production_batch_v2'
                AND generation_params->'featured_products' IS NOT NULL
            '''))
            
            unique_products = result2.fetchone()[0] or 0
            print(f"Unique products featured: {unique_products}")

async def main():
    print("🏭 Production Blog Batch Generator v2.0")
    print("=" * 60)
    
    generator = ProductionBlogBatchGenerator()
    
    import sys
    
    # Check for delete flag
    if "--delete" in sys.argv:
        print("🗑️  Deleting existing blog posts...")
        await generator.delete_existing_posts(confirm=True)
    else:
        await generator.delete_existing_posts(confirm=False)
    
    # Check for generate flag
    if "--generate" in sys.argv:
        num_posts = 100
        if "--num" in sys.argv:
            try:
                idx = sys.argv.index("--num")
                num_posts = int(sys.argv[idx + 1])
            except (IndexError, ValueError):
                pass
        
        print(f"\n🚀 Starting production batch generation...")
        await generator.generate_production_batch(num_posts)
    else:
        print("\nℹ️  Usage:")
        print("  --generate: Create new production blog posts")
        print("  --delete: Remove existing posts first") 
        print("  --num X: Number of posts to generate (default: 100)")
        print("\nExample: python generate_production_batch.py --delete --generate --num 50")

if __name__ == "__main__":
    asyncio.run(main())
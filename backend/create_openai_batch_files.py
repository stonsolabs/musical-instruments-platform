#!/usr/bin/env python3
"""
OpenAI Batch File Generator for Blog Posts
Creates JSONL files for Azure OpenAI Batch API processing
"""

import asyncio
import json
import random
from typing import List, Tuple
from datetime import datetime
from app.services.improved_blog_generator import ImprovedBlogGenerator

class OpenAIBatchFileGenerator:
    def __init__(self):
        self.generator = ImprovedBlogGenerator()
        
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
    
    async def create_batch_requests(self, num_posts: int = 100, output_file: str = None):
        """Create OpenAI batch requests for blog generation"""
        
        await self.initialize()
        
        # Get diverse topics
        topics = self.get_comprehensive_blog_topics()
        topics = topics[:num_posts]
        
        print(f"🔄 Creating OpenAI batch requests for {len(topics)} blog posts...")
        
        # Count by template
        template_counts = {}
        for _, template in topics:
            template_counts[template] = template_counts.get(template, 0) + 1
        
        print("📊 Topic distribution:")
        for template, count in sorted(template_counts.items()):
            print(f"  {template}: {count} posts")
        
        print("\n" + "="*60)
        
        batch_requests = []
        
        for i, (topic, template) in enumerate(topics):
            print(f"[{i+1}/{len(topics)}] Creating request: {topic}")
            
            # Select relevant products for this topic
            relevant_products = self.generator._select_relevant_products(topic, template, max_products=5)
            
            print(f"  Selected {len(relevant_products)} products:")
            for product in relevant_products:
                print(f"    - {product['brand_name']} {product['name']} (ID: {product['id']})")
            
            # Build the enhanced prompt with specific product data
            prompt = self.generator._build_enhanced_prompt(
                topic=topic,
                template_name=template,
                products=relevant_products,
                target_words=random.randint(3500, 4500)
            )
            
            # Create batch request
            request = {
                "custom_id": f"blog_post_{i+1:03d}_{template}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4-turbo-preview",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert music journalist and gear reviewer. Always respond with valid JSON only. Focus on the specific products provided and create engaging, informative content that helps readers make informed purchasing decisions."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 8000,
                    "temperature": 0.7
                },
                "metadata": {
                    "original_topic": topic,
                    "template": template,
                    "featured_product_ids": [str(p['id']) for p in relevant_products],
                    "target_words": random.randint(3500, 4500),
                    "generation_timestamp": datetime.now().isoformat()
                }
            }
            
            batch_requests.append(request)
        
        # Save to JSONL file
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"blog_batch_{timestamp}.jsonl"
        
        with open(output_file, 'w') as f:
            for request in batch_requests:
                f.write(json.dumps(request) + '\n')
        
        print(f"\n✅ Created {len(batch_requests)} batch requests")
        print(f"📁 Saved to: {output_file}")
        print(f"📊 File size: {round(len(open(output_file, 'r').read()) / 1024 / 1024, 2)} MB")
        
        # Show statistics
        print(f"\n📊 Batch Statistics:")
        print(f"  Total requests: {len(batch_requests)}")
        print(f"  Unique products featured: {len(set([p_id for req in batch_requests for p_id in req['metadata']['featured_product_ids']]))}")
        print(f"  Average target words: {sum([req['metadata']['target_words'] for req in batch_requests]) // len(batch_requests)}")
        
        return output_file

async def main():
    print("🔄 OpenAI Batch File Generator for Blog Posts")
    print("=" * 60)
    
    generator = OpenAIBatchFileGenerator()
    
    import sys
    
    # Parse arguments
    num_posts = 100
    output_file = None
    
    if "--num" in sys.argv:
        try:
            idx = sys.argv.index("--num")
            num_posts = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            print("❌ Invalid --num argument")
            return
    
    if "--output" in sys.argv:
        try:
            idx = sys.argv.index("--output")
            output_file = sys.argv[idx + 1]
        except (IndexError, ValueError):
            print("❌ Invalid --output argument")
            return
    
    print(f"🎯 Configuration:")
    print(f"  Posts to generate: {num_posts}")
    print(f"  Output file: {output_file or 'Auto-generated'}")
    
    # Create batch file
    result_file = await generator.create_batch_requests(num_posts, output_file)
    
    print(f"\n🚀 Next Steps:")
    print(f"  1. Upload {result_file} to Azure OpenAI Batch API")
    print(f"  2. Wait for batch processing to complete")
    print(f"  3. Download the output file")
    print(f"  4. Run: python process_batch_output.py <output_file>")

if __name__ == "__main__":
    asyncio.run(main())
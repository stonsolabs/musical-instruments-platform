#!/usr/bin/env python3
"""
Simple blog batch preparation script.
Creates 5 test blog posts and batch file for 50+ posts.
"""

import asyncio
import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

# Sample blog post ideas for testing
SAMPLE_BLOG_IDEAS = [
    {
        "title": "Best Electric Guitars for Beginners Under $500",
        "template": "Ultimate 2025 Buying Guide",
        "category": "Electric Guitars",
        "product_ids": [262, 267, 264, 305],
        "tags": ["electric_guitar", "beginner", "budget"]
    },
    {
        "title": "Gibson Les Paul vs. Epiphone: Premium vs Budget",
        "template": "Head-to-Head Battle: Product Showdown", 
        "category": "Electric Guitars",
        "product_ids": [297, 279],
        "tags": ["gibson", "epiphone", "comparison"]
    },
    {
        "title": "Best Synthesizers for Beginners 2025",
        "template": "Ultimate 2025 Buying Guide",
        "category": "Synthesizers", 
        "product_ids": [507, 508, 509, 514, 519],
        "tags": ["synthesizer", "beginner", "2025"]
    },
    {
        "title": "Best Bass Guitars for Beginners 2025",
        "template": "Ultimate 2025 Buying Guide",
        "category": "Bass Guitars",
        "product_ids": [482, 484, 551, 675],
        "tags": ["bass_guitar", "beginner", "2025"]
    },
    {
        "title": "Best Digital Pianos for Beginners 2025",
        "template": "Ultimate 2025 Buying Guide", 
        "category": "Digital Pianos",
        "product_ids": [589, 697, 722, 746, 747],
        "tags": ["digital_piano", "beginner", "2025"]
    }
]

# Extended list for batch generation (50 posts)
EXTENDED_BLOG_IDEAS = [
    # Electric Guitars (15 posts)
    {"title": "Best Electric Guitars for Beginners Under $500", "template": "Ultimate 2025 Buying Guide", "category": "Electric Guitars", "product_ids": [262, 267, 264, 305], "tags": ["electric_guitar", "beginner", "budget"]},
    {"title": "Gibson Les Paul vs. Epiphone: Premium Worth It?", "template": "Head-to-Head Battle: Product Showdown", "category": "Electric Guitars", "product_ids": [297, 279], "tags": ["gibson", "epiphone", "comparison"]},
    {"title": "Fender Stratocaster Buying Guide 2025", "template": "Ultimate 2025 Buying Guide", "category": "Electric Guitars", "product_ids": [376, 620, 646], "tags": ["fender", "stratocaster", "2025"]},
    {"title": "Best Left-Handed Electric Guitars Under $1000", "template": "Affiliate Roundup: Best Picks", "category": "Electric Guitars", "product_ids": [263, 308, 428], "tags": ["left_handed", "budget"]},
    {"title": "ESP LTD vs. Schecter: Metal Guitar Battle", "template": "Head-to-Head Battle: Product Showdown", "category": "Electric Guitars", "product_ids": [274, 276, 363, 366], "tags": ["esp", "schecter", "metal"]},
    {"title": "Best Electric Guitars for Jazz Music", "template": "Affiliate Roundup: Best Picks", "category": "Electric Guitars", "product_ids": [298, 331, 333, 379], "tags": ["jazz", "genre_specific"]},
    {"title": "PRS SE vs. Standard: Which to Choose?", "template": "Head-to-Head Battle: Product Showdown", "category": "Electric Guitars", "product_ids": [269, 280, 286, 421], "tags": ["prs", "comparison"]},
    {"title": "Best Electric Guitars Under $300", "template": "Budget Heroes: Best Bang for Buck", "category": "Electric Guitars", "product_ids": [262, 267, 364], "tags": ["budget", "under_300"]},
    {"title": "Ibanez vs. ESP: Metal Guitar Showdown", "template": "Head-to-Head Battle: Product Showdown", "category": "Electric Guitars", "product_ids": [363, 366], "tags": ["ibanez", "esp", "metal"]},
    {"title": "Best Electric Guitars for Rock Music", "template": "Affiliate Roundup: Best Picks", "category": "Electric Guitars", "product_ids": [297, 376, 620], "tags": ["rock", "genre_specific"]},
    {"title": "Harley Benton vs. Squier: Budget Battle", "template": "Head-to-Head Battle: Product Showdown", "category": "Electric Guitars", "product_ids": [262, 267], "tags": ["budget", "comparison"]},
    {"title": "Best Electric Guitars for Blues", "template": "Affiliate Roundup: Best Picks", "category": "Electric Guitars", "product_ids": [376, 620, 297], "tags": ["blues", "genre_specific"]},
    {"title": "7-String Electric Guitars: Complete Guide", "template": "Ultimate 2025 Buying Guide", "category": "Electric Guitars", "product_ids": [274, 276, 363], "tags": ["7_string", "extended_range"]},
    {"title": "Best Electric Guitars for Country Music", "template": "Affiliate Roundup: Best Picks", "category": "Electric Guitars", "product_ids": [376, 620, 646], "tags": ["country", "genre_specific"]},
    {"title": "Semi-Hollow Electric Guitars: Best Options", "template": "Affiliate Roundup: Best Picks", "category": "Electric Guitars", "product_ids": [298, 331, 333], "tags": ["semi_hollow", "jazz"]},

    # Synthesizers (10 posts)  
    {"title": "Best Synthesizers for Beginners 2025", "template": "Ultimate 2025 Buying Guide", "category": "Synthesizers", "product_ids": [507, 508, 509, 514, 519], "tags": ["synthesizer", "beginner", "2025"]},
    {"title": "Korg Volca Series: Complete Review", "template": "Professional Deep Dive Review", "category": "Synthesizers", "product_ids": [514, 523, 542], "tags": ["korg", "volca", "review"]},
    {"title": "Best Budget Synthesizers Under $500", "template": "Budget Heroes: Best Bang for Buck", "category": "Synthesizers", "product_ids": [463, 477, 507, 519], "tags": ["budget", "under_500"]},
    {"title": "Arturia PolyBrute vs. Moog Subsequent", "template": "Head-to-Head Battle: Product Showdown", "category": "Synthesizers", "product_ids": [506, 521], "tags": ["arturia", "moog", "analog"]},
    {"title": "Best Polyphonic Synthesizers 2025", "template": "Affiliate Roundup: Best Picks", "category": "Synthesizers", "product_ids": [506, 521, 964, 975], "tags": ["polyphonic", "2025"]},
    {"title": "Behringer Synthesizer Collection Review", "template": "Professional Deep Dive Review", "category": "Synthesizers", "product_ids": [477, 519, 762], "tags": ["behringer", "budget"]},
    {"title": "Analog vs. Digital Synthesizers Guide", "template": "Comparison Guide Template", "category": "Synthesizers", "product_ids": [477, 521, 964], "tags": ["analog_vs_digital", "guide"]},
    {"title": "Best Monophonic Synthesizers", "template": "Affiliate Roundup: Best Picks", "category": "Synthesizers", "product_ids": [521, 964, 477], "tags": ["monophonic", "analog"]},
    {"title": "Roland Boutique Series Review", "template": "Professional Deep Dive Review", "category": "Synthesizers", "product_ids": [510, 613, 767], "tags": ["roland", "boutique", "vintage"]},
    {"title": "Best Synthesizers for EDM Production", "template": "Affiliate Roundup: Best Picks", "category": "Synthesizers", "product_ids": [506, 507, 510], "tags": ["edm", "production", "electronic"]},

    # Bass Guitars (10 posts)
    {"title": "Best Bass Guitars for Beginners 2025", "template": "Ultimate 2025 Buying Guide", "category": "Bass Guitars", "product_ids": [482, 484, 551, 675], "tags": ["bass_guitar", "beginner", "2025"]},
    {"title": "Fender Precision vs. Jazz Bass Battle", "template": "Head-to-Head Battle: Product Showdown", "category": "Bass Guitars", "product_ids": [309, 374, 381, 502], "tags": ["fender", "precision", "jazz_bass"]},
    {"title": "Best 5-String Bass Guitars Under $1500", "template": "Affiliate Roundup: Best Picks", "category": "Bass Guitars", "product_ids": [314, 335, 343, 380], "tags": ["5_string", "under_1500"]},
    {"title": "Marcus Miller Bass Collection Review", "template": "Artist Spotlight: Gear, Tone, and Affordable Alternatives", "category": "Bass Guitars", "product_ids": [306, 335, 343, 348], "tags": ["marcus_miller", "artist"]},
    {"title": "Best Bass Guitars for Rock Music", "template": "Affiliate Roundup: Best Picks", "category": "Bass Guitars", "product_ids": [309, 381, 666], "tags": ["rock", "genre_specific"]},
    {"title": "Short Scale vs. Long Scale Bass Guide", "template": "Comparison Guide Template", "category": "Bass Guitars", "product_ids": [484, 778, 884], "tags": ["scale_length", "guide"]},
    {"title": "Best Active Bass Guitars", "template": "Affiliate Roundup: Best Picks", "category": "Bass Guitars", "product_ids": [314, 335, 505], "tags": ["active", "electronics"]},
    {"title": "Music Man StingRay Complete Guide", "template": "Professional Deep Dive Review", "category": "Bass Guitars", "product_ids": [314, 505, 559], "tags": ["music_man", "stingray"]},
    {"title": "Best Budget Bass Guitars Under $400", "template": "Budget Heroes: Best Bang for Buck", "category": "Bass Guitars", "product_ids": [482, 484, 551], "tags": ["budget", "under_400"]},
    {"title": "Best Bass Guitars for Jazz", "template": "Affiliate Roundup: Best Picks", "category": "Bass Guitars", "product_ids": [374, 381, 502], "tags": ["jazz", "genre_specific"]},

    # Digital Pianos (10 posts)
    {"title": "Best Digital Pianos for Beginners 2025", "template": "Ultimate 2025 Buying Guide", "category": "Digital Pianos", "product_ids": [589, 697, 722, 746], "tags": ["digital_piano", "beginner", "2025"]},
    {"title": "Yamaha Clavinova vs. Kawai CA Series", "template": "Head-to-Head Battle: Product Showdown", "category": "Digital Pianos", "product_ids": [359, 370, 581, 596], "tags": ["yamaha", "kawai", "premium"]},
    {"title": "Casio Privia vs. Yamaha Arius Battle", "template": "Head-to-Head Battle: Product Showdown", "category": "Digital Pianos", "product_ids": [361, 365, 607, 589], "tags": ["casio", "yamaha", "budget"]},
    {"title": "Best Portable Digital Pianos Under $1000", "template": "Affiliate Roundup: Best Picks", "category": "Digital Pianos", "product_ids": [570, 578, 697, 865], "tags": ["portable", "under_1000"]},
    {"title": "Best Digital Pianos with Wooden Keys", "template": "Affiliate Roundup: Best Picks", "category": "Digital Pianos", "product_ids": [370, 581, 596, 630], "tags": ["wooden_keys", "premium"]},
    {"title": "Kawai Concert Artist Series Review", "template": "Professional Deep Dive Review", "category": "Digital Pianos", "product_ids": [359, 581, 596], "tags": ["kawai", "concert_artist", "premium"]},
    {"title": "Best Digital Pianos Under $500", "template": "Budget Heroes: Best Bang for Buck", "category": "Digital Pianos", "product_ids": [589, 697, 722], "tags": ["budget", "under_500"]},
    {"title": "Weighted vs. Semi-Weighted Keys Guide", "template": "Comparison Guide Template", "category": "Digital Pianos", "product_ids": [589, 697, 722], "tags": ["weighted_keys", "guide"]},
    {"title": "Roland Digital Piano Collection", "template": "Professional Deep Dive Review", "category": "Digital Pianos", "product_ids": [570, 578, 612], "tags": ["roland", "collection"]},
    {"title": "Best Stage Digital Pianos", "template": "Affiliate Roundup: Best Picks", "category": "Digital Pianos", "product_ids": [570, 578, 865], "tags": ["stage_piano", "performance"]},

    # Acoustic Guitars (5 posts)  
    {"title": "Best Acoustic Guitars Under $300", "template": "Budget Heroes: Best Bang for Buck", "category": "Acoustic Guitars", "product_ids": [155, 190, 199, 208], "tags": ["acoustic", "budget", "under_300"]},
    {"title": "Taylor vs. Martin: Ultimate Comparison", "template": "Head-to-Head Battle: Product Showdown", "category": "Acoustic Guitars", "product_ids": [186, 197, 232], "tags": ["taylor", "martin", "premium"]},
    {"title": "Best Travel Acoustic Guitars", "template": "Affiliate Roundup: Best Picks", "category": "Acoustic Guitars", "product_ids": [38, 46, 61, 75], "tags": ["travel", "portable"]},
    {"title": "Best 12-String Acoustic Guitars", "template": "Affiliate Roundup: Best Picks", "category": "Acoustic Guitars", "product_ids": [229, 251, 254], "tags": ["12_string", "acoustic"]},
    {"title": "Solid Wood vs. Laminate Guide", "template": "Comparison Guide Template", "category": "Acoustic Guitars", "product_ids": [186, 220, 222], "tags": ["wood_type", "construction"]}
]

async def get_structured_prompt(blog_idea):
    """Get the structured JSON prompt for a blog idea"""
    return f"""You are an expert blog post writer with a deep knowledge of the {blog_idea['category']} space, specializing in writing high quality SEO optimized content.

Write a comprehensive 2500-3000 word blog post using the title "{blog_idea['title']}" in structured JSON format.

Template Style: {blog_idea['template']}
Category: {blog_idea['category']}
Product IDs to feature: {blog_idea['product_ids']}
Tags: {', '.join(blog_idea['tags'])}

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Conduct original research or provide unique analysis to enhance originality
5. Add deeper insights or lesser-known facts about the main topics
6. Enhance depth and quality suitable for print or reference
7. Include engaging and unique content that's shareable and recommendable
8. Differentiate content with unique perspectives or exclusive information
9. Provide personal experiences or case studies to showcase expertise
10. Expand on practical steps and detailed guidance to ensure readers can achieve their goals

Ensure the tone is formal and professional, written in 1st person plural ("We", "Our team" - but avoid referencing a specific company). Incorporate a balance of perplexity and burstiness to make the article sound humanlike. The aim is to educate readers with hyper-specific/detailed content that goes beyond the obvious to resolve specific issues.

Your output must be in JSON format using these elements:

Sub-header (use as often as needed):
{{
    "sub_header": "...",
    "paragraph_text": "..."
}}

Sub-sub-header (hierarchical under sub-headers):
{{
    "sub_sub_header": "...",
    "paragraph_text": "..."
}}

Bolded text:
{{ 
    "bold_paragraph_text": "...", 
}}

Normal text:
{{
    "paragraph_text": "..."
}}

Helpful tip (max once):
{{ 
    "article_tip": {{
    "tip_title": "...",
    "tip_text": "..."
       }}
}}

Quick Guide (max once, near beginning):
{{
    "quick_guide": {{
    "guide_title": "...: …",
    "guide_text": ["1. ...", "2. ...", "3. ..."]
    }}
}}

Table:
{{
 "simple_table": {{
"Headers": ["...", "..."], 
    "Rows": [
      {{
        "...": "...",
        "...": "..."
      }}
    ]  
  }}
}}

Additional notes:
- Do not mention any year in the slug
- Capitalize all major words in headers and subheaders

RESPOND ONLY WITH VALID JSON IN THIS EXACT FORMAT:
{{
  "title": "{blog_idea['title']}",
  "slug": "seo-friendly-slug-without-years",
  "seo_title": "SEO-optimized title (50-60 chars)",
  "seo_description": "SEO meta description (110-160 chars)",
  "primary_keyword": "main keyword for SEO",
  "reading_time": 12,
  "content": [
    // Use the JSON elements above to structure your content
  ],
  "tags": {json.dumps(blog_idea['tags'])},
  "meta": {{
    "content_type": "{blog_idea['template'].lower().replace(' ', '_')}",
    "target_audience": ["beginners", "enthusiasts"],
    "key_benefits": ["save_money", "make_informed_decisions"],
    "word_count": 2500
  }}
}}

Make the content engaging, informative, and focused on helping readers make informed purchasing decisions. Do not mention AI generation."""

async def generate_sample_posts():
    """Generate 5 sample blog posts directly using our API"""
    print("🚀 Generating 5 sample blog posts directly...")
    
    for i, idea in enumerate(SAMPLE_BLOG_IDEAS):
        print(f"\n📝 Generating: {idea['title']}")
        
        # In a real implementation, you would call your blog generation API here
        # For now, we'll just show the structured prompt
        prompt = await get_structured_prompt(idea)
        
        print(f"✅ Generated prompt for: {idea['title']}")
        print(f"📊 Template: {idea['template']}")
        print(f"🎯 Products: {idea['product_ids']}")
        
        # Save individual prompt to file for testing
        filename = f"/Users/felipe/pprojects/musical-instruments-platform/sample_blog_prompt_{i+1}.txt"
        with open(filename, 'w') as f:
            f.write(prompt)
        print(f"💾 Saved prompt to: {filename}")

async def create_batch_file():
    """Create batch file for 50+ blog posts"""
    print("\n🚀 Creating batch file for 50+ blog posts...")
    
    batch_requests = []
    
    for i, idea in enumerate(EXTENDED_BLOG_IDEAS):
        prompt = await get_structured_prompt(idea)
        
        batch_request = {
            "custom_id": f"blog-post-{i+1:03d}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert music gear writer creating comprehensive blog posts. Always respond with valid JSON only, no explanations or comments."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 8000,
                "temperature": 0.7
            }
        }
        batch_requests.append(batch_request)
    
    # Save batch file
    batch_filename = f"/Users/felipe/pprojects/musical-instruments-platform/batch_blog_requests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    with open(batch_filename, 'w') as f:
        for request in batch_requests:
            f.write(json.dumps(request) + '\n')
    
    print(f"📄 Created batch file: {batch_filename}")
    print(f"📊 Total requests: {len(batch_requests)}")
    
    # Create summary
    summary = {
        "created_at": datetime.now().isoformat(),
        "total_requests": len(batch_requests),
        "categories": {},
        "templates": {}
    }
    
    # Count categories and templates
    for idea in EXTENDED_BLOG_IDEAS:
        cat = idea['category']
        template = idea['template']
        summary['categories'][cat] = summary['categories'].get(cat, 0) + 1
        summary['templates'][template] = summary['templates'].get(template, 0) + 1
    
    summary_file = batch_filename.replace('.jsonl', '_summary.json')
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"📋 Created summary: {summary_file}")
    print(f"📂 Categories: {list(summary['categories'].keys())}")
    print(f"📋 Templates: {list(summary['templates'].keys())}")
    
    return batch_filename

async def main():
    print("🎵 Blog Content Generation System")
    print("=" * 50)
    
    try:
        # Generate 5 sample posts
        await generate_sample_posts()
        
        # Create batch file for 50+ posts
        batch_file = await create_batch_file()
        
        print(f"\n🎉 Generation completed!")
        print(f"📁 Batch file: {batch_file}")
        print(f"🔢 Total batch requests: {len(EXTENDED_BLOG_IDEAS)}")
        
        print(f"\n📝 Next steps:")
        print(f"1. Review sample prompts in project root")
        print(f"2. Upload batch file to OpenAI for processing")
        print(f"3. Process results when batch completes")
        print(f"4. Import generated content to your blog system")
        
    except Exception as e:
        print(f"💥 Error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
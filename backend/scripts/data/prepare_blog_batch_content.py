#!/usr/bin/env python3
"""
Prepare blog batch content using the blog post ideas document.
This script creates batch files for mass blog generation using our templates.
"""

import asyncio
import sys
import os
import json
import random
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

# Blog post ideas extracted from the blog_post_ideas.md document
BLOG_POST_IDEAS = [
    # Electric Guitars
    {
        "title": "Best Electric Guitars for Beginners Under $500",
        "template_name": "Ultimate 2025 Buying Guide",
        "category_id": 0,  # Electric Guitars
        "product_ids": [262, 267, 264, 305],
        "tags": ["electric_guitar", "beginner", "budget", "buying_guide"]
    },
    {
        "title": "Gibson Les Paul vs. Epiphone: Is the Premium Worth It?",
        "template_name": "Head-to-Head Battle: Product Showdown",
        "category_id": 0,
        "product_ids": [297, 279],
        "tags": ["gibson", "epiphone", "les_paul", "comparison"]
    },
    {
        "title": "Fender Stratocaster Buying Guide 2025",
        "template_name": "Ultimate 2025 Buying Guide", 
        "category_id": 0,
        "product_ids": [376, 620, 646, 1019],
        "tags": ["fender", "stratocaster", "buying_guide", "2025"]
    },
    {
        "title": "Best Left-Handed Electric Guitars Under $1000",
        "template_name": "Affiliate Roundup: Best Picks",
        "category_id": 0,
        "product_ids": [263, 308, 428],
        "tags": ["left_handed", "electric_guitar", "budget"]
    },
    {
        "title": "ESP LTD vs. Schecter: Metal Guitar Comparison",
        "template_name": "Head-to-Head Battle: Product Showdown",
        "category_id": 0,
        "product_ids": [274, 276, 363, 366],
        "tags": ["esp", "schecter", "metal", "comparison"]
    }
]

async def get_template_ids():
    """Get template IDs mapped by name"""
    async with async_session_factory() as session:
        result = await session.execute(
            text("SELECT id, name FROM blog_generation_templates WHERE is_active = true")
        )
        return {row[1]: row[0] for row in result.fetchall()}

async def create_batch_files():
    """Create batch files for OpenAI batch processing"""
    
    print("🚀 Preparing blog batch content generation...")
    
    # Get template mappings
    template_ids = await get_template_ids()
    
    print(f"📋 Found {len(template_ids)} templates")
    
    # Create batch requests (simplified for now)
    batch_requests = []
    for i, idea in enumerate(BLOG_POST_IDEAS[:5]):  # First 5 for testing
        batch_request = {
            "custom_id": f"blog-post-{i+1:03d}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert music gear writer creating comprehensive blog posts using structured JSON format."
                    },
                    {
                        "role": "user", 
                        "content": f"Write a blog post titled: {idea['title']}\n\nUse template: {idea['template_name']}\nProduct IDs: {idea['product_ids']}\nTags: {', '.join(idea['tags'])}\n\nReturn structured JSON with sections, titles, and content."
                    }
                ],
                "max_tokens": 4000,
                "temperature": 0.7
            }
        }
        batch_requests.append(batch_request)
    
    # Save to JSONL file
    batch_filename = f"/Users/felipe/pprojects/musical-instruments-platform/batch_blog_requests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    with open(batch_filename, 'w') as f:
        for request in batch_requests:
            f.write(json.dumps(request) + '\n')
    
    print(f"📄 Created batch file: {batch_filename}")
    print(f"📊 Generated {len(batch_requests)} batch requests")
    
    return batch_filename, len(batch_requests)

async def main():
    try:
        batch_file, count = await create_batch_files()
        
        print(f"\n🎉 Batch generation preparation completed!")
        print(f"📁 Batch file: {batch_file}")
        print(f"🔢 Total requests: {count}")
        
    except Exception as e:
        print(f"💥 Error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
from __future__ import annotations

import asyncio
import json
import csv
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import text

from backend.app.database import async_session_factory

# High-converting product combinations based on analysis
HIGH_VALUE_PRODUCT_SETS = {
    "Electric Guitars": {
        "beginner": [262, 267, 264, 305],
        "intermediate": [376, 620, 646, 1019],
        "professional": [297, 279, 269, 280],
        "budget": [155, 190, 262, 267],
        "premium": [619, 253, 602, 655],
    },
    "Digital Pianos": {
        "beginner": [589, 697, 722, 746],
        "intermediate": [370, 361, 365, 578],
        "professional": [581, 596, 630, 704],
        "portable": [570, 578, 697, 865],
        "weighted_keys": [370, 581, 596, 630],
    },
    "Acoustic Guitars": {
        "beginner": [155, 190, 199, 208],
        "intermediate": [186, 197, 232, 455],
        "travel": [38, 46, 61, 75],
        "twelve_string": [229, 251, 254, 554],
        "premium": [186, 220, 222, 230],
    },
    "Bass Guitars": {
        "beginner": [482, 484, 551, 675],
        "intermediate": [381, 309, 374, 502],
        "five_string": [314, 335, 343, 380],
        "active": [282, 303, 311, 320],
        "professional": [314, 505, 559, 701],
    },
    "Synthesizers": {
        "beginner": [507, 508, 509, 514],
        "analog": [477, 521, 964, 975],
        "digital": [510, 613, 767, 869],
        "budget": [463, 477, 507, 519],
        "polyphonic": [506, 521, 964, 975],
    },
}

# Content templates optimized for different marketing goals
BATCH_CONTENT_TEMPLATES = [
    {
        "name": "Ultimate 2025 Buying Guide",
        "template_type": "buying_guide",
        "target_word_count": 3500,
        "conversion_focus": "high",
        "seo_priority": "primary",
        "content_pillars": [
            "comprehensive_analysis",
            "budget_breakdowns",
            "expert_recommendations",
            "comparison_tables",
            "setup_guides"
        ],
    },
    {
        "name": "Head-to-Head Product Battle",
        "template_type": "comparison",
        "target_word_count": 2500,
        "conversion_focus": "high",
        "seo_priority": "primary",
        "content_pillars": [
            "direct_comparison",
            "winner_analysis",
            "use_case_scenarios",
            "value_assessment",
            "purchase_guidance"
        ],
    },
    {
        "name": "Budget Hero Roundup",
        "template_type": "value_focused",
        "target_word_count": 2000,
        "conversion_focus": "medium",
        "seo_priority": "secondary",
        "content_pillars": [
            "value_analysis",
            "price_comparison",
            "smart_compromises",
            "upgrade_paths",
            "deal_alerts"
        ],
    },
    {
        "name": "Professional Deep Dive",
        "template_type": "review",
        "target_word_count": 2800,
        "conversion_focus": "high",
        "seo_priority": "primary",
        "content_pillars": [
            "technical_analysis",
            "real_world_testing",
            "competitive_context",
            "ownership_experience",
            "expert_verdict"
        ],
    },
    {
        "name": "Seasonal Deal Hunter",
        "template_type": "deals",
        "target_word_count": 1800,
        "conversion_focus": "very_high",
        "seo_priority": "urgent",
        "content_pillars": [
            "time_sensitive_offers",
            "price_tracking",
            "deal_stacking",
            "urgency_creation",
            "value_validation"
        ],
    },
]

# SEO-optimized keywords and topics
SEO_KEYWORDS = {
    "Electric Guitars": [
        "best electric guitar 2025",
        "electric guitar buying guide",
        "beginner electric guitar",
        "electric guitar under 500",
        "fender vs gibson",
        "best electric guitar for metal",
        "electric guitar setup guide",
    ],
    "Digital Pianos": [
        "best digital piano 2025",
        "digital piano buying guide",
        "yamaha vs kawai digital piano",
        "weighted keys digital piano",
        "portable digital piano",
        "digital piano under 1000",
        "best digital piano for beginners",
    ],
    "Acoustic Guitars": [
        "best acoustic guitar 2025",
        "acoustic guitar buying guide",
        "taylor vs martin guitar",
        "beginner acoustic guitar",
        "travel guitar review",
        "12 string guitar",
        "acoustic guitar under 300",
    ],
    "Bass Guitars": [
        "best bass guitar 2025",
        "bass guitar buying guide",
        "fender precision vs jazz bass",
        "5 string bass guitar",
        "bass guitar for beginners",
        "active vs passive bass",
        "bass guitar under 500",
    ],
    "Synthesizers": [
        "best synthesizer 2025",
        "analog vs digital synthesizer",
        "beginner synthesizer guide",
        "budget synthesizer under 300",
        "polyphonic synthesizer",
        "hardware vs software synth",
        "modular synthesizer guide",
    ],
}

async def analyze_product_performance() -> Dict[str, Any]:
    """Analyze product database for high-performing content opportunities."""
    async with async_session_factory() as session:
        # Get product categories with counts
        category_analysis = await session.execute(
            text("""
                SELECT c.name, c.slug, COUNT(p.id) as product_count,
                       AVG(p.avg_rating) as avg_rating,
                       COUNT(CASE WHEN p.avg_rating >= 4.0 THEN 1 END) as high_rated_count
                FROM categories c
                LEFT JOIN products p ON c.id = p.category_id
                WHERE c.is_active = true AND p.is_active = true
                GROUP BY c.id, c.name, c.slug
                HAVING COUNT(p.id) > 10
                ORDER BY product_count DESC
            """)
        )
        
        categories = []
        for row in category_analysis:
            categories.append({
                "name": row.name,
                "slug": row.slug,
                "product_count": row.product_count,
                "avg_rating": float(row.avg_rating or 0),
                "high_rated_count": row.high_rated_count,
                "content_opportunity": "high" if row.product_count > 100 else "medium"
            })
        
        # Get top brands for content
        brand_analysis = await session.execute(
            text("""
                SELECT b.name, b.slug, COUNT(p.id) as product_count,
                       AVG(p.avg_rating) as avg_rating
                FROM brands b
                LEFT JOIN products p ON b.id = p.brand_id
                WHERE b.name != 'Unknown Brand' AND p.is_active = true
                GROUP BY b.id, b.name, b.slug
                HAVING COUNT(p.id) > 5
                ORDER BY product_count DESC
                LIMIT 20
            """)
        )
        
        brands = []
        for row in brand_analysis:
            brands.append({
                "name": row.name,
                "slug": row.slug,
                "product_count": row.product_count,
                "avg_rating": float(row.avg_rating or 0),
            })
        
        return {
            "categories": categories,
            "brands": brands,
            "analysis_date": datetime.now().isoformat(),
        }

def generate_content_calendar(months: int = 6) -> List[Dict[str, Any]]:
    """Generate a content calendar for batch production."""
    calendar = []
    start_date = datetime.now()
    
    # Monthly themes for seasonal relevance
    monthly_themes = {
        1: {"theme": "New Year Gear Goals", "focus": "resolutions, upgrades"},
        2: {"theme": "Home Studio Month", "focus": "recording, production"},
        3: {"theme": "Spring Cleaning Setup", "focus": "organization, maintenance"},
        4: {"theme": "Outdoor Performance Prep", "focus": "portable, live gear"},
        5: {"theme": "Graduation Gift Guide", "focus": "student, beginner"},
        6: {"theme": "Summer Performance Season", "focus": "live, festival gear"},
        7: {"theme": "Mid-Year Gear Refresh", "focus": "upgrades, reviews"},
        8: {"theme": "Back-to-School Music", "focus": "education, programs"},
        9: {"theme": "Studio Setup Season", "focus": "professional, recording"},
        10: {"theme": "Halloween/Gig Prep", "focus": "performance, effects"},
        11: {"theme": "Black Friday Prep", "focus": "deals, value"},
        12: {"theme": "Holiday Gift Guides", "focus": "gifts, year-end"},
    }
    
    for month_offset in range(months):
        month_date = start_date + timedelta(days=30 * month_offset)
        month_num = month_date.month
        theme_info = monthly_themes.get(month_num, monthly_themes[1])
        
        # Generate 4-6 posts per month
        for week in range(4):
            post_date = month_date + timedelta(days=7 * week)
            
            calendar.append({
                "publish_date": post_date.isoformat(),
                "month_theme": theme_info["theme"],
                "theme_focus": theme_info["focus"],
                "content_type": "buying_guide" if week == 0 else 
                              "comparison" if week == 1 else
                              "review" if week == 2 else "deals",
                "priority": "high" if week < 2 else "medium",
                "target_category": list(HIGH_VALUE_PRODUCT_SETS.keys())[week % len(HIGH_VALUE_PRODUCT_SETS)],
            })
    
    return calendar

def create_batch_requests(content_calendar: List[Dict[str, Any]], 
                         analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create optimized batch requests for content generation."""
    batch_requests = []
    
    for item in content_calendar:
        category = item["target_category"]
        content_type = item["content_type"]
        
        # Select appropriate template
        template = next(
            (t for t in BATCH_CONTENT_TEMPLATES if content_type in t["template_type"]),
            BATCH_CONTENT_TEMPLATES[0]
        )
        
        # Select product combination
        product_sets = HIGH_VALUE_PRODUCT_SETS.get(category, {})
        if content_type == "buying_guide":
            products = product_sets.get("intermediate", [])[:5]
        elif content_type == "comparison":
            products = product_sets.get("beginner", [])[:3]
        elif content_type == "review":
            products = product_sets.get("professional", [])[:1]
        else:  # deals
            products = product_sets.get("budget", [])[:7]
        
        # Create SEO-optimized titles
        keywords = SEO_KEYWORDS.get(category, [])
        primary_keyword = keywords[0] if keywords else f"best {category.lower()}"
        
        title_templates = {
            "buying_guide": f"Best {category} 2025: Ultimate Buying Guide + Expert Picks",
            "comparison": f"{category} Showdown 2025: Which Should You Buy?",
            "review": f"Professional {category} Review: Worth the Investment?",
            "deals": f"Hot {category} Deals Alert: Save Up to 50% This Week",
        }
        
        batch_request = {
            "custom_id": f"{category.lower().replace(' ', '_')}_{content_type}_{item['publish_date'][:7]}",
            "template_name": template["name"],
            "category_name": category,
            "product_ids": products,
            "target_word_count": template["target_word_count"],
            "seo_data": {
                "primary_keyword": primary_keyword,
                "title": title_templates.get(content_type, f"Best {category} Guide"),
                "meta_description": f"Expert {category.lower()} guide with reviews, comparisons, and recommendations. Find the perfect {category.lower()} for your needs and budget.",
            },
            "content_pillars": template["content_pillars"],
            "publish_date": item["publish_date"],
            "theme": item["month_theme"],
            "priority": item["priority"],
            "conversion_focus": template["conversion_focus"],
        }
        
        batch_requests.append(batch_request)
    
    return batch_requests

async def export_batch_data(batch_requests: List[Dict[str, Any]], 
                           analysis: Dict[str, Any]]) -> None:
    """Export batch data for AI generation."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Export batch requests as JSON
    with open(f"blog_batch_requests_{timestamp}.json", "w") as f:
        json.dump({
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "total_requests": len(batch_requests),
                "categories_covered": list(set(r["category_name"] for r in batch_requests)),
                "content_types": list(set(r["template_name"] for r in batch_requests)),
            },
            "batch_requests": batch_requests,
            "analysis": analysis,
        }, f, indent=2)
    
    # Export as CSV for easy review
    with open(f"blog_content_calendar_{timestamp}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "publish_date", "category", "content_type", "title", "word_count", 
            "priority", "theme", "product_count", "primary_keyword"
        ])
        writer.writeheader()
        
        for req in batch_requests:
            writer.writerow({
                "publish_date": req["publish_date"][:10],
                "category": req["category_name"],
                "content_type": req["template_name"],
                "title": req["seo_data"]["title"],
                "word_count": req["target_word_count"],
                "priority": req["priority"],
                "theme": req["theme"],
                "product_count": len(req["product_ids"]),
                "primary_keyword": req["seo_data"]["primary_keyword"],
            })
    
    print(f"✅ Exported {len(batch_requests)} batch requests")
    print(f"📊 Analysis data: {len(analysis['categories'])} categories, {len(analysis['brands'])} brands")
    print(f"📅 Content calendar spans {len(set(r['publish_date'][:7] for r in batch_requests))} months")
    print(f"🎯 Files created: blog_batch_requests_{timestamp}.json, blog_content_calendar_{timestamp}.csv")

async def main():
    """Main execution function."""
    print("🔍 Analyzing product database...")
    analysis = await analyze_product_performance()
    
    print("📅 Generating content calendar...")
    content_calendar = generate_content_calendar(months=6)
    
    print("🚀 Creating batch requests...")
    batch_requests = create_batch_requests(content_calendar, analysis)
    
    print("💾 Exporting data...")
    await export_batch_data(batch_requests, analysis)
    
    # Print summary
    print("\n📈 BATCH CONTENT SUMMARY")
    print("=" * 50)
    
    by_category = {}
    by_type = {}
    
    for req in batch_requests:
        cat = req["category_name"]
        typ = req["template_name"]
        
        by_category[cat] = by_category.get(cat, 0) + 1
        by_type[typ] = by_type.get(typ, 0) + 1
    
    print("By Category:")
    for cat, count in sorted(by_category.items()):
        print(f"  {cat}: {count} posts")
    
    print("\nBy Content Type:")
    for typ, count in sorted(by_type.items()):
        print(f"  {typ}: {count} posts")
    
    print(f"\nTotal Posts Planned: {len(batch_requests)}")
    print(f"Estimated Word Count: {sum(r['target_word_count'] for r in batch_requests):,} words")
    print(f"High Priority Posts: {len([r for r in batch_requests if r['priority'] == 'high'])}")

if __name__ == "__main__":
    asyncio.run(main())
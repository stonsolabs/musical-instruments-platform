#!/usr/bin/env python3
"""
Fix SEO Placeholder System - Remove Unused Placeholders
Since the system doesn't actually replace SEO template placeholders, 
we should remove them and use simple, static SEO templates.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

# Simple, static SEO templates without placeholders
STATIC_SEO_TEMPLATES = {
    "buying_guide": {
        "seo_title_template": "Ultimate Buying Guide: Expert Picks and Recommendations",
        "seo_description_template": "Complete buying guide with expert picks, detailed reviews, and everything you need to choose the perfect instrument."
    },
    "comparison": {
        "seo_title_template": "Product Comparison: Which One Should You Choose?",
        "seo_description_template": "Detailed product comparison with analysis, clear winner, and expert recommendations for your needs."
    },
    "general": {
        "seo_title_template": "Best Picks: Top Recommendations Compared",
        "seo_description_template": "Discover the best picks with pros/cons, use-cases, and buying tips."
    },
    "review": {
        "seo_title_template": "Professional Review: In-Depth Analysis",
        "seo_description_template": "Professional review with testing, performance analysis, pros/cons, and final verdict."
    },
    "tutorial": {
        "seo_title_template": "Step-by-Step Guide with Recommended Gear",
        "seo_description_template": "Complete step-by-step guide with recommended gear for each step."
    },
    "history": {
        "seo_title_template": "History and Evolution: From Origins to Modern Era",
        "seo_description_template": "Explore the history, key milestones, and today's relevant gear."
    },
    "artist_spotlight": {
        "seo_title_template": "Artist Spotlight: Gear and How to Get the Sound",
        "seo_description_template": "Explore signature tone, core gear, and affordable alternatives to get the sound."
    },
    "new_release": {
        "seo_title_template": "First Look: What's New",
        "seo_description_template": "New product announcements with key features, differences from previous models, and early verdict."
    },
    "quiz": {
        "seo_title_template": "Quiz: Find Your Perfect Match",
        "seo_description_template": "Take our quick quiz to find the best option for your needs and budget."
    }
}

async def fix_seo_placeholder_system():
    """Fix SEO templates by removing unused placeholders"""
    print("🚀 Fixing SEO placeholder system...")
    print("=" * 60)
    print("⚠️  ISSUE FOUND: SEO templates have placeholders but no replacement system!")
    print("🔧 SOLUTION: Using static SEO templates without placeholders")
    print("=" * 60)
    
    async with async_session_factory() as session:
        # Get all active templates
        result = await session.execute(text("""
            SELECT id, name, template_type, seo_title_template, seo_description_template
            FROM blog_generation_templates 
            WHERE is_active = true
            ORDER BY template_type, name
        """))
        templates = result.fetchall()
        
        updated_count = 0
        
        for template in templates:
            template_id, name, template_type, current_title, current_desc = template
            
            # Get the static SEO template for this template type
            if template_type in STATIC_SEO_TEMPLATES:
                static_template = STATIC_SEO_TEMPLATES[template_type]
                new_title = static_template["seo_title_template"]
                new_desc = static_template["seo_description_template"]
                
                # Check if template needs updating (has placeholders)
                needs_update = False
                
                # Check for any placeholders
                placeholders = ['{', '}']
                for placeholder in placeholders:
                    if current_title and placeholder in current_title:
                        needs_update = True
                        print(f"📝 Updating {name} - removing placeholders from title")
                        break
                    if current_desc and placeholder in current_desc:
                        needs_update = True
                        print(f"📝 Updating {name} - removing placeholders from description")
                        break
                
                if needs_update:
                    # Update the template
                    await session.execute(text("""
                        UPDATE blog_generation_templates 
                        SET seo_title_template = :seo_title,
                            seo_description_template = :seo_description,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = :template_id
                    """), {
                        'template_id': template_id,
                        'seo_title': new_title,
                        'seo_description': new_desc
                    })
                    
                    updated_count += 1
                    print(f"✅ Updated: {name}")
                else:
                    print(f"✅ Already static: {name}")
            else:
                print(f"⚠️  No static template found for type: {template_type}")
        
        await session.commit()
        
        print(f"\n🎉 Successfully fixed {updated_count} SEO templates!")
        print(f"📊 Total templates processed: {len(templates)}")
        print(f"\n💡 RECOMMENDATION:")
        print(f"   The blog generation system should be updated to either:")
        print(f"   1. Implement placeholder replacement for SEO templates, OR")
        print(f"   2. Use AI-generated SEO titles/descriptions (current approach)")
        print(f"   Currently using approach #2 - AI generates SEO content directly.")
        print(f"✨ SEO placeholder system fix completed!")

if __name__ == "__main__":
    asyncio.run(fix_seo_placeholder_system())

#!/usr/bin/env python3
"""
Clean SEO Templates - Remove Fixed Years and Unused Placeholders
Updates all SEO title and description templates to be evergreen and use only valid placeholders
"""

import asyncio
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

# Clean SEO templates for each template type
CLEAN_SEO_TEMPLATES = {
    "buying_guide": {
        "seo_title_template": "Best {category}: Ultimate Buying Guide + Expert Picks",
        "seo_description_template": "The complete {category} buying guide. Expert picks, detailed reviews, budget breakdowns, and everything you need to choose the perfect {category}."
    },
    "comparison": {
        "seo_title_template": "{product1} vs {product2}: Which Wins?",
        "seo_description_template": "Epic {category} comparison: {product1} vs {product2}. Detailed analysis, clear winner, and expert recommendations for your needs."
    },
    "general": {
        "seo_title_template": "Best {category}: Top Picks Compared",
        "seo_description_template": "Discover the best {category} with pros/cons, use-cases, and buying tips."
    },
    "review": {
        "seo_title_template": "{brand} {model} Review: Professional Analysis",
        "seo_description_template": "In-depth {brand} {model} review with professional testing, real-world performance analysis, pros/cons, and final verdict."
    },
    "tutorial": {
        "seo_title_template": "How to {topic}: Step-by-Step Guide with Recommended Gear",
        "seo_description_template": "A step-by-step guide to {topic}, plus recommended gear for each step."
    },
    "history": {
        "seo_title_template": "The History of {topic}: From Origins to Modern Era",
        "seo_description_template": "Explore the history of {topic}, key milestones, and today's relevant gear."
    },
    "artist_spotlight": {
        "seo_title_template": "Artist Spotlight: {artist} — Gear & How to Get the Sound",
        "seo_description_template": "Explore {artist}'s signature tone, core gear, and affordable alternatives to get the sound."
    },
    "new_release": {
        "seo_title_template": "First Look: {brand} {name} — What's New",
        "seo_description_template": "{brand} announces the new {name}. Key features, differences from previous model, and early verdict."
    },
    "quiz": {
        "seo_title_template": "Quiz: Which {category} Is Right for You?",
        "seo_description_template": "Take our quick quiz to find the best {category} for your needs and budget."
    }
}

async def clean_seo_templates():
    """Clean all SEO templates to remove fixed years and unused placeholders"""
    print("🚀 Starting SEO template cleanup...")
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
            
            # Get the clean SEO template for this template type
            if template_type in CLEAN_SEO_TEMPLATES:
                clean_template = CLEAN_SEO_TEMPLATES[template_type]
                new_title = clean_template["seo_title_template"]
                new_desc = clean_template["seo_description_template"]
                
                # Check if template needs updating
                needs_update = False
                
                # Check for fixed years
                if current_title and ('2025' in current_title or '2024' in current_title):
                    needs_update = True
                    print(f"📝 Updating {name} - removing fixed year from title")
                
                if current_desc and ('2025' in current_desc or '2024' in current_desc):
                    needs_update = True
                    print(f"📝 Updating {name} - removing fixed year from description")
                
                # Check for unused placeholders
                if current_title and ('%(seo_title)s' in current_title or '%(seo_description)s' in current_title):
                    needs_update = True
                    print(f"📝 Updating {name} - removing unused placeholder from title")
                
                if current_desc and ('%(seo_title)s' in current_desc or '%(seo_description)s' in current_desc):
                    needs_update = True
                    print(f"📝 Updating {name} - removing unused placeholder from description")
                
                # Check for non-existent placeholders
                invalid_placeholders = ['{artist}', '{product_1}', '{product_2}', '{product_3}', '{name}', '{budget}', '{discount}', '{season}']
                for placeholder in invalid_placeholders:
                    if current_title and placeholder in current_title:
                        needs_update = True
                        print(f"📝 Updating {name} - removing invalid placeholder {placeholder} from title")
                    if current_desc and placeholder in current_desc:
                        needs_update = True
                        print(f"📝 Updating {name} - removing invalid placeholder {placeholder} from description")
                
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
                    print(f"✅ Already clean: {name}")
            else:
                print(f"⚠️  No clean template found for type: {template_type}")
        
        await session.commit()
        
        print(f"\n🎉 Successfully cleaned {updated_count} SEO templates!")
        print(f"📊 Total templates processed: {len(templates)}")
        print(f"✨ SEO template cleanup completed!")

if __name__ == "__main__":
    asyncio.run(clean_seo_templates())

#!/usr/bin/env python3
"""
Final SEO Template Cleanup - Remove All Invalid Placeholders
Final cleanup to ensure all SEO templates use only valid placeholders and are evergreen
"""

import asyncio
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

# Final clean SEO templates - only using valid placeholders
FINAL_CLEAN_SEO_TEMPLATES = {
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
        "seo_title_template": "Artist Spotlight: Gear & How to Get the Sound",
        "seo_description_template": "Explore signature tone, core gear, and affordable alternatives to get the sound."
    },
    "new_release": {
        "seo_title_template": "First Look: {brand} — What's New",
        "seo_description_template": "{brand} announces new products. Key features, differences from previous models, and early verdict."
    },
    "quiz": {
        "seo_title_template": "Quiz: Which {category} Is Right for You?",
        "seo_description_template": "Take our quick quiz to find the best {category} for your needs and budget."
    }
}

async def final_seo_cleanup():
    """Final cleanup of all SEO templates"""
    print("🚀 Starting final SEO template cleanup...")
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
            
            # Get the final clean SEO template for this template type
            if template_type in FINAL_CLEAN_SEO_TEMPLATES:
                clean_template = FINAL_CLEAN_SEO_TEMPLATES[template_type]
                new_title = clean_template["seo_title_template"]
                new_desc = clean_template["seo_description_template"]
                
                # Check if template needs updating
                needs_update = False
                
                # Check for any invalid placeholders
                invalid_placeholders = [
                    '{artist}', '{product_1}', '{product_2}', '{product_3}', 
                    '{name}', '{budget}', '{discount}', '{season}', '{year}',
                    '%(seo_title)s', '%(seo_description)s'
                ]
                
                for placeholder in invalid_placeholders:
                    if current_title and placeholder in current_title:
                        needs_update = True
                        print(f"📝 Updating {name} - removing invalid placeholder {placeholder} from title")
                    if current_desc and placeholder in current_desc:
                        needs_update = True
                        print(f"📝 Updating {name} - removing invalid placeholder {placeholder} from description")
                
                # Check for double braces (inconsistent format)
                if current_title and '{{' in current_title:
                    needs_update = True
                    print(f"📝 Updating {name} - fixing double braces in title")
                if current_desc and '{{' in current_desc:
                    needs_update = True
                    print(f"📝 Updating {name} - fixing double braces in description")
                
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
        print(f"✨ Final SEO template cleanup completed!")

if __name__ == "__main__":
    asyncio.run(final_seo_cleanup())

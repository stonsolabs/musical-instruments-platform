#!/usr/bin/env python3
"""
Update ALL existing blog generation templates to use structured JSON format.
This script will enhance every active template with structured JSON output.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text
import json

# Enhanced JSON structure for blog content
STRUCTURED_JSON_FORMAT = """
RESPOND ONLY WITH VALID JSON IN THIS EXACT FORMAT:
{
  "title": "Main blog post title",
  "excerpt": "Brief 1-2 sentence summary for previews",
  "seo_title": "SEO-optimized title (60 chars max)",
  "seo_description": "SEO meta description (155 chars max)",
  "featured_image_alt": "Alt text for featured image",
  "reading_time": 8,
  "sections": [
    {
      "type": "introduction",
      "title": "Section title (can be null for intro)",
      "content": "Full HTML content for this section",
      "products_mentioned": [1, 2, 3]
    },
    {
      "type": "comparison_table", 
      "title": "Quick Comparison",
      "content": "HTML table or structured comparison content",
      "products_mentioned": [1, 2, 3, 4]
    },
    {
      "type": "product_showcase",
      "title": "Top Picks",
      "content": "Content introducing the products",
      "products": [
        {
          "product_id": 1,
          "context": "Why this product was selected and what makes it special",
          "position": 1
        }
      ]
    },
    {
      "type": "buying_guide",
      "title": "What to Look For",
      "content": "Educational content about choosing products in this category"
    },
    {
      "type": "faqs",
      "title": "Frequently Asked Questions", 
      "content": "HTML with FAQ structure",
      "faqs": [
        {
          "question": "What should I consider when choosing X?",
          "answer": "Detailed answer with helpful context"
        }
      ]
    },
    {
      "type": "conclusion",
      "title": "Final Thoughts",
      "content": "Wrap-up content with key takeaways"
    }
  ],
  "tags": ["buying_guide", "2025", "expert_picks"],
  "meta": {
    "content_type": "buying_guide",
    "expertise_level": "intermediate",
    "target_audience": ["beginners", "hobbyists"],
    "key_benefits": ["save_money", "avoid_mistakes", "find_perfect_match"]
  }
}

CRITICAL: Output ONLY the JSON object. No explanations, comments, or extra text.
"""

# Template-specific section mappings based on template type
SECTION_MAPPINGS = {
    "review": [
        {"type": "introduction", "required": True},
        {"type": "first_impressions", "required": True},
        {"type": "build_analysis", "required": True}, 
        {"type": "performance_testing", "required": True},
        {"type": "competitive_comparison", "required": False},
        {"type": "pros_cons", "required": True},
        {"type": "buyer_guidance", "required": True},
        {"type": "conclusion", "required": True}
    ],
    "buying_guide": [
        {"type": "introduction", "required": True},
        {"type": "buying_guide", "required": True},
        {"type": "common_mistakes", "required": False},
        {"type": "product_showcase", "required": True},
        {"type": "budget_guide", "required": False},
        {"type": "faqs", "required": True},
        {"type": "conclusion", "required": True}
    ],
    "comparison": [
        {"type": "introduction", "required": True},
        {"type": "comparison_table", "required": True},
        {"type": "detailed_comparison", "required": True},
        {"type": "winner_analysis", "required": True},
        {"type": "use_cases", "required": False},
        {"type": "conclusion", "required": True}
    ],
    "general": [
        {"type": "introduction", "required": True},
        {"type": "comparison_table", "required": False},
        {"type": "product_showcase", "required": True},
        {"type": "buying_guide", "required": False},
        {"type": "faqs", "required": True},
        {"type": "conclusion", "required": True}
    ],
    "tutorial": [
        {"type": "introduction", "required": True},
        {"type": "requirements", "required": True},
        {"type": "step_by_step", "required": True},
        {"type": "troubleshooting", "required": False},
        {"type": "product_showcase", "required": False},
        {"type": "conclusion", "required": True}
    ],
    "history": [
        {"type": "introduction", "required": True},
        {"type": "historical_timeline", "required": True},
        {"type": "evolution_analysis", "required": True},
        {"type": "modern_impact", "required": True},
        {"type": "product_showcase", "required": False},
        {"type": "conclusion", "required": True}
    ],
    "artist_spotlight": [
        {"type": "introduction", "required": True},
        {"type": "artist_background", "required": True},
        {"type": "signature_gear", "required": True},
        {"type": "affordable_alternatives", "required": True},
        {"type": "tone_analysis", "required": False},
        {"type": "conclusion", "required": True}
    ],
    "quiz": [
        {"type": "introduction", "required": True},
        {"type": "quiz_questions", "required": True},
        {"type": "results_analysis", "required": True},
        {"type": "product_recommendations", "required": True},
        {"type": "conclusion", "required": True}
    ],
    "new_release": [
        {"type": "introduction", "required": True},
        {"type": "first_impressions", "required": True},
        {"type": "key_features", "required": True},
        {"type": "competitive_comparison", "required": True},
        {"type": "pricing_availability", "required": True},
        {"type": "conclusion", "required": True}
    ]
}

async def get_all_templates():
    """Get all active templates from database"""
    async with async_session_factory() as session:
        result = await session.execute(
            text("SELECT id, name, template_type, base_prompt FROM blog_generation_templates WHERE is_active = true ORDER BY name")
        )
        return result.fetchall()

async def update_template_with_structured_json(session, template_id, template_name, template_type, original_prompt):
    """Update a single template with structured JSON format"""
    
    # Get section mapping for this template type
    sections = SECTION_MAPPINGS.get(template_type, SECTION_MAPPINGS["general"])
    
    # Create enhanced prompt with structured JSON
    enhanced_prompt = f"""{original_prompt}

{STRUCTURED_JSON_FORMAT}"""
    
    # Create content structure
    content_structure = {
        "format": "structured_json",
        "sections": sections,
        "expected_length": "1500-2500 words",
        "product_integration": "context_driven"
    }
    
    # Update the template
    await session.execute(
        text("""
            UPDATE blog_generation_templates SET 
                base_prompt = :base_prompt,
                content_structure = :content_structure,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = :id
        """),
        {
            "id": template_id,
            "base_prompt": enhanced_prompt,
            "content_structure": json.dumps(content_structure)
        }
    )
    
    return True

async def update_all_templates():
    """Update all existing templates with structured JSON format"""
    async with async_session_factory() as session:
        try:
            # Get all templates
            templates = await get_all_templates()
            print(f"Found {len(templates)} active templates to update...")
            
            updated_count = 0
            
            for template_id, template_name, template_type, original_prompt in templates:
                try:
                    # Skip if already has structured JSON format
                    if "RESPOND ONLY WITH VALID JSON" in original_prompt:
                        print(f"⏭️  Skipping {template_name} (already has structured JSON)")
                        continue
                    
                    # Update the template
                    await update_template_with_structured_json(
                        session, template_id, template_name, template_type, original_prompt
                    )
                    
                    print(f"✅ Updated: {template_name} ({template_type})")
                    updated_count += 1
                    
                except Exception as e:
                    print(f"❌ Failed to update {template_name}: {e}")
            
            # Commit all changes
            await session.commit()
            print(f"\n🎉 Successfully updated {updated_count} templates with structured JSON format!")
            print(f"📝 {len(templates) - updated_count} templates were already up to date.")
            
        except Exception as e:
            await session.rollback()
            print(f"💥 Error during batch update: {e}")
            raise

async def main():
    print("🚀 Starting batch update of all blog templates...")
    await update_all_templates()
    print("✨ Template update completed!")

if __name__ == "__main__":
    asyncio.run(main())
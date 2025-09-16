#!/usr/bin/env python3
"""
Update blog generation templates to use structured JSON format.
This enhances the content generation to include proper section structure.
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

# Updated templates with structured JSON format
ENHANCED_TEMPLATES = [
    {
        "name": "Professional Deep-Dive Review",
        "base_prompt": (
            f"Write a comprehensive product review following professional standards. "
            f"Structure: (1) Introduction with first impressions; (2) Build quality analysis; "
            f"(3) Performance testing results; (4) Competitive comparison; "
            f"(5) Long-term ownership insights; (6) Detailed pros and cons; (7) Who should buy; "
            f"(8) Final verdict with rating. Include technical details and honest assessment.\n\n"
            f"{STRUCTURED_JSON_FORMAT}"
        ),
        "content_structure": {
            "format": "structured_json",
            "sections": [
                {"type": "introduction", "required": True},
                {"type": "build_analysis", "required": True}, 
                {"type": "performance_testing", "required": True},
                {"type": "competitive_comparison", "required": True},
                {"type": "ownership_experience", "required": False},
                {"type": "pros_cons", "required": True},
                {"type": "buyer_guidance", "required": True},
                {"type": "conclusion", "required": True}
            ],
            "expected_length": "2000-3000 words",
            "product_integration": "detailed_analysis"
        }
    },
    {
        "name": "Affiliate Roundup: Best Picks",
        "base_prompt": (
            f"Create a high-converting roundup of the featured products. Include: "
            f"(1) Engaging introduction framing the problem; "
            f"(2) Quick comparison table with key specs; (3) Detailed product showcases with pros/cons; "
            f"(4) Buying guide with key factors; (5) Use-case recommendations; (6) FAQs; "
            f"(7) Conclusion with final recommendations.\n\n"
            f"{STRUCTURED_JSON_FORMAT}"
        ),
        "content_structure": {
            "format": "structured_json",
            "sections": [
                {"type": "introduction", "required": True},
                {"type": "comparison_table", "required": True},
                {"type": "product_showcase", "required": True},
                {"type": "buying_guide", "required": True},
                {"type": "use_cases", "required": False},
                {"type": "faqs", "required": True},
                {"type": "conclusion", "required": True}
            ],
            "expected_length": "1500-2500 words",
            "product_integration": "comparison_focused"
        }
    },
    {
        "name": "Educational Buying Guide",
        "base_prompt": (
            f"Write a comprehensive educational buying guide. Structure: "
            f"(1) Introduction explaining why this guide matters; "
            f"(2) Key factors to consider when choosing; (3) Common mistakes to avoid; "
            f"(4) Product recommendations by skill level; (5) Budget considerations; "
            f"(6) Where to buy and what to look for; (7) FAQs; (8) Conclusion with action steps.\n\n"
            f"{STRUCTURED_JSON_FORMAT}"
        ),
        "content_structure": {
            "format": "structured_json", 
            "sections": [
                {"type": "introduction", "required": True},
                {"type": "buying_guide", "required": True},
                {"type": "common_mistakes", "required": True},
                {"type": "product_showcase", "required": True},
                {"type": "budget_guide", "required": False},
                {"type": "shopping_tips", "required": False},
                {"type": "faqs", "required": True},
                {"type": "conclusion", "required": True}
            ],
            "expected_length": "1800-2800 words",
            "product_integration": "educational_context"
        }
    }
]

async def update_templates():
    """Update existing templates with enhanced JSON structure"""
    async with async_session_factory() as session:
        try:
            # Update the most commonly used templates
            for template_data in ENHANCED_TEMPLATES:
                # Find template by name
                result = await session.execute(
                    text("SELECT id FROM blog_generation_templates WHERE name = :name"),
                    {"name": template_data["name"]}
                )
                template_row = result.fetchone()
                
                if template_row:
                    # Update existing template
                    await session.execute(
                        text("""
                            UPDATE blog_generation_templates SET 
                                base_prompt = :base_prompt,
                                content_structure = :content_structure,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE id = :id
                        """),
                        {
                            "id": template_row[0],
                            "base_prompt": template_data["base_prompt"],
                            "content_structure": json.dumps(template_data["content_structure"])
                        }
                    )
                    print(f"✅ Updated template: {template_data['name']}")
                else:
                    print(f"⚠️  Template not found: {template_data['name']}")
            
            await session.commit()
            print(f"\n🎉 Successfully updated {len(ENHANCED_TEMPLATES)} templates with structured JSON format!")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error updating templates: {e}")
            raise

async def main():
    await update_templates()

if __name__ == "__main__":
    asyncio.run(main())
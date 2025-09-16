"""
Enhanced blog templates specifically optimized for affiliate conversion.

This script adds/updates templates with conversion-focused prompts, proper word counts,
and affiliate optimization elements.

Run:
  ENVIRONMENT=production python -m backend.scripts.data.update_blog_templates_for_conversion
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, List
from sqlalchemy import text

from backend.app.database import async_session_factory

# Enhanced templates optimized for affiliate conversion
CONVERSION_OPTIMIZED_TEMPLATES: List[Dict[str, Any]] = [
    {
        "name": "Ultimate 2025 Buying Guide",
        "description": "Comprehensive 3500+ word buying guides optimized for affiliate conversion",
        "template_type": "buying_guide",
        "base_prompt": (
            "Create the definitive buying guide for {category} in 2025. This should be THE resource people bookmark and buy from. "
            "\n\n## CONVERSION-FOCUSED STRUCTURE:\n"
            "1. **Hook Introduction** (200 words): Address the #1 buyer pain point and position this as the solution\n"
            "2. **Quick Picks Summary** (300 words): Best Overall, Best Budget, Best Premium with prices and key reasons\n"
            "3. **Complete Buyer's Criteria** (500 words): What to look for, red flags, must-have vs nice-to-have features\n"
            "4. **Detailed Product Analysis** (1500+ words): For each featured product include:\n"
            "   - Why it made our list (unique value proposition)\n"
            "   - Key specifications and real-world performance\n"
            "   - Sound/build quality assessment\n"
            "   - Who it's perfect for (skill level, use cases)\n"
            "   - Honest pros and cons (4-5 each)\n"
            "   - Current pricing and value assessment\n"
            "   - [🛒 Check Latest Price] call-to-action\n"
            "5. **Budget Breakdown** (400 words): $300-500 / $500-1000 / $1000+ tiers with specific recommendations\n"
            "6. **Common Mistakes** (300 words): What NOT to buy and why\n"
            "7. **Setup & Accessories Guide** (300 words): Essential gear to complete the setup\n"
            "8. **Expert Verdict** (200 words): Final recommendations by use case\n\n"
            "Include comparison tables, real user scenarios, and 2-3 compelling affiliate CTAs per product. "
            "Target 3500+ words minimum. Focus on solving real buyer problems with actionable advice."
        ),
        "system_prompt": (
            "You are a music gear expert with 20+ years experience and a track record of helping people make great purchases. "
            "Write with authority and deep knowledge. Include specific technical details, real-world insights, and honest assessments. "
            "Your goal is to help readers make confident purchase decisions that they'll be happy with long-term. "
            "Be genuinely helpful - recommend the right product for the right person, not the most expensive."
        ),
        "product_context_prompt": (
            "For each product, provide comprehensive analysis: brand reputation context, key differentiators, sound characteristics, "
            "build quality assessment, ideal use cases, skill level fit, value proposition, and honest pros/cons. "
            "Include realistic price context, availability notes, and current market positioning. "
            "Explain WHY each product is recommended for specific users with concrete examples."
        ),
        "min_products": 5,
        "max_products": 10,
        "suggested_tags": ["buying_guide", "2025", "ultimate", "comprehensive", "best"],
        "seo_title_template": "Best {category} 2025: Ultimate Buying Guide + Expert Picks",
        "seo_description_template": "The complete 2025 {category} buying guide. Expert picks, detailed reviews, budget breakdowns, and everything you need to choose the perfect {category}.",
        "content_structure": {"sections": [
            "introduction", "quick_picks", "buying_criteria", "detailed_reviews", "budget_breakdown", 
            "common_mistakes", "setup_guide", "comparison_table", "expert_verdict", "faqs"
        ]},
        "target_word_count": 3500,
        "conversion_elements": [
            "multiple_ctas_per_product",
            "price_urgency",
            "social_proof",
            "comparison_tables",
            "budget_guidance"
        ],
        "is_active": True,
    },
    {
        "name": "High-Converting Product Battle",
        "description": "Epic head-to-head comparisons that drive purchase decisions",
        "template_type": "comparison",
        "base_prompt": (
            "Create an epic, sports-style head-to-head comparison that becomes the definitive resource for this decision. "
            "\n\n## BATTLE STRUCTURE:\n"
            "1. **Fight Card Introduction** (200 words): Present competitors like a boxing match - specs, strengths, price points\n"
            "2. **Quick Verdict Table** (150 words): Winner by category at a glance\n"
            "3. **Round-by-Round Analysis** (1200 words):\n"
            "   - **Round 1: Build Quality & Design** (300 words)\n"
            "   - **Round 2: Sound/Performance** (300 words)\n"
            "   - **Round 3: Features & Usability** (300 words)\n"
            "   - **Round 4: Value for Money** (300 words)\n"
            "4. **Detailed Specs Comparison Table** (200 words): Side-by-side technical comparison\n"
            "5. **Real-World Scenarios** (400 words): Which wins for different use cases\n"
            "6. **Clear Winners** (300 words): Best for Beginners, Best for Pros, Best Value, etc.\n"
            "7. **Alternative Options** (200 words): If these don't fit, consider these\n"
            "8. **Final Verdict** (150 words): Our definitive recommendation\n\n"
            "Use engaging sports commentary style but maintain expert credibility. Include [🛒 Check Price] CTAs for each product. "
            "Declare clear winners with solid reasoning. Target 2500+ words."
        ),
        "system_prompt": (
            "You are a music gear reviewer who makes complex comparisons easy to understand. "
            "Be analytical but engaging, with clear verdicts and practical advice. "
            "Your comparisons should feel like watching an exciting sports match while being genuinely informative."
        ),
        "product_context_prompt": (
            "Compare products on concrete attributes: build materials, sound characteristics, feature sets, "
            "reliability, brand support, resale value, and real-world performance. "
            "Declare clear winners with solid reasoning backed by technical analysis and user experience insights."
        ),
        "min_products": 2,
        "max_products": 4,
        "suggested_tags": ["comparison", "vs", "battle", "showdown", "head_to_head"],
        "seo_title_template": "{product1} vs {product2} (2025): Epic Battle & Clear Winner",
        "seo_description_template": "Epic {category} comparison: {product1} vs {product2}. Detailed analysis, clear winner, and expert recommendations for your needs.",
        "content_structure": {"sections": [
            "fight_card", "quick_verdict", "round_by_round", "comparison_table", 
            "use_cases", "winner_by_category", "alternatives", "final_verdict"
        ]},
        "target_word_count": 2500,
        "conversion_elements": [
            "clear_winners",
            "use_case_matching",
            "comparison_tables",
            "decisive_recommendations"
        ],
        "is_active": True,
    },
    {
        "name": "Budget Hero Finder",
        "description": "Value-focused roundups that convert budget-conscious buyers",
        "template_type": "general",
        "base_prompt": (
            "Find the absolute best value {category} that deliver incredible performance despite lower prices. "
            "This isn't about cheap - it's about smart spending. \n\n## VALUE-FOCUSED STRUCTURE:\n"
            "1. **Value Proposition** (200 words): Why spending smart beats spending more\n"
            "2. **Our Budget Heroes** (800 words): Top 3-5 products that punch above their weight:\n"
            "   - Why it's a value champion (specific advantages)\n"
            "   - Where it excels vs expensive options\n"
            "   - What corners were cut (and why they don't matter)\n"
            "   - Real-world performance vs price\n"
            "   - [💰 Check Best Deal] CTA\n"
            "3. **Price-to-Performance Analysis** (400 words): Cost per feature breakdown\n"
            "4. **What You're NOT Sacrificing** (300 words): Core features that remain excellent\n"
            "5. **Smart Upgrade Paths** (300 words): When and how to upgrade later\n"
            "6. **Value-Maximizing Accessories** (200 words): Gear that multiplies your investment\n"
            "7. **Budget Traps to Avoid** (300 words): False economy purchases that cost more long-term\n"
            "8. **Best Current Deals** (200 words): Where to find the best prices today\n\n"
            "Include specific price comparisons and urgency elements. Target 2200+ words. Focus on ROI and long-term value."
        ),
        "system_prompt": (
            "You are a value-hunting expert who finds diamonds in the rough. "
            "Emphasize smart spending and genuine value over pure cheapness. "
            "Help people understand what makes something a good deal vs just cheap."
        ),
        "product_context_prompt": (
            "For each product, explain the value proposition: where it excels despite lower price, "
            "what corners were cut (and why they don't matter), competitive advantages, and upgrade potential. "
            "Include specific price-to-performance ratios and long-term value analysis."
        ),
        "min_products": 3,
        "max_products": 7,
        "suggested_tags": ["budget", "value", "bang_for_buck", "affordable", "deals"],
        "seo_title_template": "Best Budget {category} 2025: Incredible Value Under ${budget}",
        "seo_description_template": "Top budget {category} that deliver incredible value. Expert picks under ${budget} with performance that rivals expensive models.",
        "content_structure": {"sections": [
            "value_intro", "budget_heroes", "price_performance", "smart_compromises", 
            "upgrade_paths", "value_accessories", "avoid_these", "best_deals"
        ]},
        "target_word_count": 2200,
        "conversion_elements": [
            "value_emphasis",
            "deal_urgency",
            "price_comparisons",
            "upgrade_paths"
        ],
        "is_active": True,
    },
    {
        "name": "Deal Alert Generator",
        "description": "Time-sensitive deal content with urgency and scarcity",
        "template_type": "general",
        "base_prompt": (
            "Create urgent, time-sensitive deal content that drives immediate action. "
            "\n\n## DEAL ALERT STRUCTURE:\n"
            "1. **Deal Alert Header** (100 words): Immediate attention grabber with savings highlights\n"
            "2. **Hot Deals Right Now** (600 words): 5-8 best current deals:\n"
            "   - Normal vs sale price (with % savings)\n"
            "   - Why this is a genuine bargain\n"
            "   - Limited time/stock warnings\n"
            "   - [🔥 Grab This Deal] urgent CTA\n"
            "3. **Lightning Deals** (300 words): Extremely limited-time offers to act on NOW\n"
            "4. **Upcoming Sales** (200 words): Deals to watch for in coming days/weeks\n"
            "5. **Price History Context** (200 words): How current prices compare to historical lows\n"
            "6. **Deal Stacking Tips** (200 words): How to maximize savings with multiple offers\n"
            "7. **What to Avoid** (150 words): Fake sales and poor value 'deals'\n"
            "8. **Last Chance Alerts** (150 words): Deals ending soon\n\n"
            "Create genuine urgency without being pushy. Include countdown timers, stock alerts, and price drop notifications. "
            "Target 1800+ words with maximum conversion focus."
        ),
        "system_prompt": (
            "You are a deal hunter who tracks prices and knows when to buy. "
            "Create urgency without being pushy, and always provide genuine value. "
            "Help people understand what makes a good deal vs marketing hype."
        ),
        "product_context_prompt": (
            "For each deal, include: normal price, current deal price, savings amount/percentage, "
            "deal duration, why it's a good value, competitive pricing context, and historical price data. "
            "Only recommend deals that are genuinely good value."
        ),
        "min_products": 5,
        "max_products": 12,
        "suggested_tags": ["deals", "sale", "discount", "limited_time", "urgent"],
        "seo_title_template": "🔥 Hot {category} Deals: Save Up to {discount}% (Limited Time)",
        "seo_description_template": "Hot {season} deals on {category}! Limited-time discounts up to {discount}% off. Don't miss these expert-picked bargains.",
        "content_structure": {"sections": [
            "deal_alert", "hot_deals", "lightning_deals", "upcoming_sales", 
            "price_history", "stacking_tips", "deal_warnings", "last_chance"
        ]},
        "target_word_count": 1800,
        "conversion_elements": [
            "urgency_creation",
            "scarcity_tactics",
            "price_anchoring",
            "deal_validation"
        ],
        "is_active": True,
    }
]

async def update_templates() -> None:
    """Update existing templates with conversion optimization."""
    async with async_session_factory() as session:
        for template in CONVERSION_OPTIMIZED_TEMPLATES:
            # Check if template exists
            exists = await session.execute(
                text("SELECT id FROM blog_generation_templates WHERE name = :name"),
                {"name": template["name"]},
            )
            row = exists.fetchone()
            
            if row is not None:
                # Update existing template
                print(f"Updating existing template: {template['name']}")
                await session.execute(
                    text("""
                        UPDATE blog_generation_templates SET 
                            description = :description,
                            template_type = :template_type,
                            base_prompt = :base_prompt,
                            system_prompt = :system_prompt,
                            product_context_prompt = :product_context_prompt,
                            min_products = :min_products,
                            max_products = :max_products,
                            suggested_tags = :suggested_tags,
                            seo_title_template = :seo_title_template,
                            seo_description_template = :seo_description_template,
                            content_structure = :content_structure,
                            is_active = :is_active,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE name = :name
                    """),
                    {
                        "name": template["name"],
                        "description": template.get("description"),
                        "template_type": template["template_type"],
                        "base_prompt": template["base_prompt"],
                        "system_prompt": template.get("system_prompt"),
                        "product_context_prompt": template.get("product_context_prompt"),
                        "min_products": template.get("min_products", 0),
                        "max_products": template.get("max_products", 10),
                        "suggested_tags": json.dumps(template.get("suggested_tags", [])),
                        "seo_title_template": template.get("seo_title_template"),
                        "seo_description_template": template.get("seo_description_template"),
                        "content_structure": json.dumps(template.get("content_structure", {})),
                        "is_active": template.get("is_active", True),
                    },
                )
            else:
                # Insert new template
                print(f"Creating new template: {template['name']}")
                await session.execute(
                    text("""
                        INSERT INTO blog_generation_templates (
                            name, description, template_type, base_prompt, system_prompt,
                            product_context_prompt, min_products, max_products,
                            suggested_tags, seo_title_template, seo_description_template, 
                            content_structure, is_active
                        ) VALUES (
                            :name, :description, :template_type, :base_prompt, :system_prompt,
                            :product_context_prompt, :min_products, :max_products,
                            :suggested_tags, :seo_title_template, :seo_description_template, 
                            :content_structure, :is_active
                        )
                    """),
                    {
                        "name": template["name"],
                        "description": template.get("description"),
                        "template_type": template["template_type"],
                        "base_prompt": template["base_prompt"],
                        "system_prompt": template.get("system_prompt"),
                        "product_context_prompt": template.get("product_context_prompt"),
                        "min_products": template.get("min_products", 0),
                        "max_products": template.get("max_products", 10),
                        "suggested_tags": json.dumps(template.get("suggested_tags", [])),
                        "seo_title_template": template.get("seo_title_template"),
                        "seo_description_template": template.get("seo_description_template"),
                        "content_structure": json.dumps(template.get("content_structure", {})),
                        "is_active": template.get("is_active", True),
                    },
                )
        
        await session.commit()
        print(f"\n✅ Successfully updated {len(CONVERSION_OPTIMIZED_TEMPLATES)} templates for better affiliate conversion")

async def add_conversion_fields() -> None:
    """Add conversion optimization fields to existing templates."""
    async with async_session_factory() as session:
        # Check if target_word_count column exists
        try:
            await session.execute(
                text("ALTER TABLE blog_generation_templates ADD COLUMN target_word_count INTEGER DEFAULT 2000")
            )
            print("✅ Added target_word_count column")
        except Exception:
            print("ℹ️ target_word_count column already exists")
        
        # Check if conversion_elements column exists
        try:
            await session.execute(
                text("ALTER TABLE blog_generation_templates ADD COLUMN conversion_elements JSONB DEFAULT '[]'")
            )
            print("✅ Added conversion_elements column")
        except Exception:
            print("ℹ️ conversion_elements column already exists")
        
        await session.commit()

async def main():
    """Main execution function."""
    print("🔧 Adding conversion optimization fields...")
    await add_conversion_fields()
    
    print("\n📝 Updating templates with conversion optimization...")
    await update_templates()
    
    print("\n📊 CONVERSION OPTIMIZATION SUMMARY")
    print("=" * 50)
    print("Enhanced Templates:")
    for template in CONVERSION_OPTIMIZED_TEMPLATES:
        print(f"• {template['name']}")
        print(f"  - Target: {template['target_word_count']} words")
        print(f"  - Products: {template['min_products']}-{template['max_products']}")
        print(f"  - Conversion elements: {len(template.get('conversion_elements', []))}")
        print()
    
    print("🎯 Key Improvements:")
    print("• Detailed word count targeting for SEO")
    print("• Multiple CTAs per product for better conversion")
    print("• Urgency and scarcity elements")
    print("• Clear section structure for better readability")
    print("• Social proof and authority building")
    print("• Price comparison and value emphasis")
    print("\n🚀 Your templates are now optimized for maximum affiliate conversion!")

if __name__ == "__main__":
    asyncio.run(main())
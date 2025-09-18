#!/usr/bin/env python3
"""
Enhanced Blog Templates - Comprehensive 2500-3000 word blogs with rich affiliate integration
This script creates advanced blog templates that generate high-quality, conversion-focused content.
"""

import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

# Enhanced JSON structure for rich blog content with affiliate integration
ENHANCED_JSON_STRUCTURE = """
RESPOND ONLY WITH VALID JSON IN THIS EXACT FORMAT:
{
  "title": "SEO-optimized blog post title (60 chars max)",
  "excerpt": "Compelling 1-2 sentence summary (150-200 chars)",
  "seo_title": "SEO title (60 chars max)",
  "seo_description": "SEO meta description (155 chars max)",
  "featured_image_alt": "Descriptive alt text for featured image",
  "reading_time": 12,
  "word_count": 3000,
  "sections": [
    {
      "type": "introduction",
      "title": "Hook readers with compelling opening",
      "content": "Engaging introduction that addresses pain points and promises value",
      "affiliate_placement": "none"
    },
    {
      "type": "product_showcase_inline",
      "title": "Top Pick: [Product Name]",
      "content": "Detailed product analysis with pros/cons and use cases",
      "products": [
        {
          "product_id": 1,
          "context": "Why this is the top choice with specific benefits",
          "position": 1,
          "affiliate_placement": "inline",
          "cta_text": "Check Latest Price"
        }
      ],
      "affiliate_placement": "inline"
    },
    {
      "type": "comparison_table",
      "title": "Quick Comparison",
      "content": "Side-by-side comparison of featured products",
      "headers": ["Feature", "Product A", "Product B", "Product C"],
      "rows": [
        ["Price Range", "$300-400", "$500-600", "$700-800"],
        ["Best For", "Beginners", "Intermediate", "Professional"]
      ],
      "products_mentioned": [1, 2, 3],
      "affiliate_placement": "below_table"
    },
    {
      "type": "buying_guide",
      "title": "What to Look For",
      "content": "Comprehensive buying criteria with specific recommendations",
      "affiliate_placement": "none"
    },
    {
      "type": "product_showcase_inline",
      "title": "Budget Pick: [Product Name]",
      "content": "Detailed analysis of budget-friendly option",
      "products": [
        {
          "product_id": 2,
          "context": "Best value proposition and who it's perfect for",
          "position": 2,
          "affiliate_placement": "inline",
          "cta_text": "View at Store"
        }
      ],
      "affiliate_placement": "inline"
    },
    {
      "type": "pros_cons",
      "title": "Pros & Cons Analysis",
      "pros": ["Specific advantage 1", "Specific advantage 2", "Specific advantage 3"],
      "cons": ["Specific limitation 1", "Specific limitation 2"],
      "content": "Balanced analysis of trade-offs",
      "affiliate_placement": "none"
    },
    {
      "type": "product_showcase_inline",
      "title": "Premium Choice: [Product Name]",
      "content": "In-depth analysis of high-end option",
      "products": [
        {
          "product_id": 3,
          "context": "Why professionals choose this and what makes it worth the investment",
          "position": 3,
          "affiliate_placement": "inline",
          "cta_text": "Shop Now"
        }
      ],
      "affiliate_placement": "inline"
    },
    {
      "type": "use_cases",
      "title": "Who Should Buy What",
      "content": "Clear recommendations by user type, skill level, and budget",
      "products_mentioned": [1, 2, 3],
      "affiliate_placement": "none"
    },
    {
      "type": "faqs",
      "title": "Frequently Asked Questions",
      "content": "Address common concerns and questions",
      "faqs": [
        {
          "question": "What's the most important factor when choosing?",
          "answer": "Detailed answer with specific guidance and product recommendations"
        }
      ],
      "affiliate_placement": "none"
    },
    {
      "type": "conclusion",
      "title": "Final Recommendations",
      "content": "Clear final verdict with specific product recommendations and next steps",
      "products_mentioned": [1, 2, 3],
      "affiliate_placement": "none"
    }
  ],
  "tags": ["buying_guide", "expert_picks", "comparison"],
  "meta": {
    "content_type": "comprehensive_guide",
    "expertise_level": "all_levels",
    "target_audience": ["beginners", "intermediate", "professionals"],
    "key_benefits": ["save_money", "avoid_mistakes", "find_perfect_match", "expert_guidance"],
    "estimated_read_time": 12,
    "affiliate_integration": "comprehensive"
  },
  "product_recommendations": [
    {
      "product_id": 1,
      "relevance_score": 0.95,
      "reasoning": "Top overall choice for most users due to balance of features and value",
      "suggested_context": "top_pick",
      "suggested_sections": ["product_showcase_inline", "comparison_table", "conclusion"],
      "affiliate_placement": "inline"
    },
    {
      "product_id": 2,
      "relevance_score": 0.90,
      "reasoning": "Best budget option that doesn't compromise on quality",
      "suggested_context": "budget_pick",
      "suggested_sections": ["product_showcase_inline", "comparison_table", "use_cases"],
      "affiliate_placement": "inline"
    },
    {
      "product_id": 3,
      "relevance_score": 0.88,
      "reasoning": "Premium choice for professionals and serious enthusiasts",
      "suggested_context": "premium_choice",
      "suggested_sections": ["product_showcase_inline", "comparison_table", "conclusion"],
      "affiliate_placement": "inline"
    }
  ]
}

CRITICAL REQUIREMENTS:
- Target MINIMUM 2500 words, aim for 3000+ words for comprehensive coverage
- Include 3-5 inline product showcases with affiliate CTAs
- Every product mention should have clear affiliate integration
- Use specific, actionable language that drives conversions
- Include comparison tables and detailed analysis
- Address different user types and budgets
- Provide clear next steps and purchase guidance
- ALWAYS include product_id for each product mentioned
- Use consistent affiliate_placement values: "none", "inline", "below_table", "below", "above"
- Include specific CTA text for each product showcase
"""

# Enhanced templates with comprehensive affiliate integration
ENHANCED_TEMPLATES = [
    {
        "name": "Ultimate Buying Guide with Affiliate Integration",
        "description": "Comprehensive 3000+ word buying guides with deep affiliate integration throughout content",
        "template_type": "buying_guide",
        "base_prompt": f"""Create the definitive buying guide for {{category}}. This should be THE resource people bookmark and share.

STRUCTURE REQUIREMENTS:
1. **Hook Introduction** - Address the #1 pain point and promise specific value
2. **Inline Product Showcases** - 3-5 detailed product analyses with affiliate CTAs throughout content
3. **Comparison Tables** - Side-by-side specs and features with clear winners
4. **Buying Criteria** - What to look for with specific product examples
5. **Use Case Recommendations** - Clear guidance by skill level, budget, and use case
6. **Pros/Cons Analysis** - Honest assessment of trade-offs
7. **FAQ Section** - Address common concerns with product recommendations
8. **Final Verdict** - Clear recommendations with next steps

AFFILIATE INTEGRATION REQUIREMENTS:
- Include 3-5 inline product showcases with "Check Latest Price" CTAs
- Every product mention should have clear affiliate placement
- Use comparison tables to drive conversions
- Include specific pricing context and value propositions
- Address different budgets with clear product recommendations
- End each product section with compelling CTAs

CONTENT QUALITY:
- Target 2500-3000 words for comprehensive coverage
- Use specific, actionable language that drives decisions
- Include real-world scenarios and use cases
- Provide honest assessments of pros/cons
- Address beginner to professional skill levels
- Include current pricing and availability context

{ENHANCED_JSON_STRUCTURE}""",
        "system_prompt": """You are a music gear expert with 20+ years experience writing conversion-focused buying guides. Your content drives affiliate sales while providing genuine value. Write with authority, include specific details, and always guide readers toward confident purchase decisions. Use contractions, vary sentence length, and avoid generic AI phrasing. Show, don't tell with concrete examples and scenarios.""",
        "product_context_prompt": """For each featured product, provide comprehensive analysis including: specific features that matter, real-world performance, build quality assessment, ideal use cases, skill level fit, value proposition, honest pros/cons, current pricing context, and clear affiliate CTAs. Make every product mention actionable and conversion-focused.""",
        "required_product_types": [],
        "min_products": 3,
        "max_products": 8,
        "suggested_tags": ["buying_guide", "ultimate", "comprehensive", "affiliate"],
        "seo_title_template": "Best {{category}}: Ultimate Buying Guide + Top Picks",
        "seo_description_template": "The complete {{category}} buying guide. Expert picks, detailed reviews, budget breakdowns, and everything you need to choose the perfect {{category}}.",
        "content_structure": {
            "sections": [
                "introduction", "product_showcase_inline", "comparison_table", "buying_guide", 
                "product_showcase_inline", "pros_cons", "product_showcase_inline", "use_cases", 
                "faqs", "conclusion"
            ],
            "affiliate_integration": "comprehensive",
            "target_word_count": "2500-3000"
        },
        "is_active": True,
    },
    {
        "name": "Head-to-Head Battle with Affiliate CTAs",
        "description": "High-converting direct comparisons with inline affiliate integration",
        "template_type": "comparison",
        "base_prompt": f"""Create an epic head-to-head comparison between {{product_count}} competing products with comprehensive affiliate integration.

STRUCTURE REQUIREMENTS:
1. **Fight Card Intro** - Dramatic opening that sets up the comparison
2. **Quick Verdict Summary** - Clear winners by category upfront
3. **Round-by-Round Analysis** - Detailed comparison in key areas
4. **Inline Product Showcases** - Detailed analysis of each product with CTAs
5. **Comparison Tables** - Side-by-side specs and features
6. **Use Case Scenarios** - Which product for which situation
7. **Value Analysis** - Bang for buck assessment
8. **Final Recommendations** - Clear winners with purchase guidance

AFFILIATE INTEGRATION REQUIREMENTS:
- Include inline product showcases for each competitor
- Add "Check Latest Price" CTAs after each product analysis
- Use comparison tables to highlight differences
- Include specific pricing and value propositions
- End with clear purchase recommendations
- Address different budgets and use cases

CONTENT QUALITY:
- Target 2500-3000 words for comprehensive analysis
- Make comparisons engaging like a sports match
- Include specific technical details and real-world performance
- Provide clear verdicts with solid reasoning
- Address different user types and budgets
- Include current pricing and availability

{ENHANCED_JSON_STRUCTURE}""",
        "system_prompt": """You are a music gear reviewer who makes complex comparisons easy to understand and drives conversions. Be analytical but engaging, with clear verdicts and practical advice. Write like you're commentating a sports match - exciting but informative. Use specific details and always guide toward purchase decisions.""",
        "product_context_prompt": """Compare products on concrete attributes: build materials, sound characteristics, feature sets, reliability, brand support, resale value, and real-world performance. For each product, include detailed analysis with specific CTAs and clear value propositions. Declare clear winners with solid reasoning.""",
        "required_product_types": [],
        "min_products": 2,
        "max_products": 5,
        "suggested_tags": ["comparison", "vs", "battle", "showdown", "affiliate"],
        "seo_title_template": "{{product1}} vs {{product2}}: Which Wins?",
        "seo_description_template": "Epic {{category}} comparison: {{product1}} vs {{product2}}. Detailed analysis, clear winner, and expert recommendations for your needs.",
        "content_structure": {
            "sections": [
                "introduction", "quick_verdict", "product_showcase_inline", "comparison_table", 
                "product_showcase_inline", "use_cases", "value_analysis", "conclusion"
            ],
            "affiliate_integration": "comprehensive",
            "target_word_count": "2500-3000"
        },
        "is_active": True,
    },
    {
        "name": "Budget Heroes with Value-Focused Affiliates",
        "description": "Value-focused roundups that convert budget-conscious buyers with strategic affiliate placement",
        "template_type": "general",
        "base_prompt": f"""Find the absolute best value {{category}} that punch above their price point with comprehensive affiliate integration.

STRUCTURE REQUIREMENTS:
1. **Value Proposition Intro** - Why budget doesn't mean compromise
2. **Top 3 Budget Heroes** - Detailed analysis of each with CTAs
3. **Price-to-Performance Analysis** - What you get for your money
4. **Smart Compromises** - What you're NOT sacrificing
5. **Upgrade Paths** - How to grow with your gear
6. **Value Accessories** - Essential add-ons that maximize value
7. **Red Flags to Avoid** - What to skip in budget options
8. **Best Deals** - Current pricing and where to buy

AFFILIATE INTEGRATION REQUIREMENTS:
- Include inline product showcases for each budget hero
- Add "Check Latest Price" CTAs throughout content
- Highlight current deals and discounts
- Include value-focused messaging
- Address upgrade paths with product recommendations
- End with clear purchase guidance

CONTENT QUALITY:
- Target 2500-3000 words for comprehensive value analysis
- Focus on genuine value, not just cheap prices
- Include specific pricing data and comparisons
- Address different budget ranges
- Provide realistic expectations
- Include current deals and availability

{ENHANCED_JSON_STRUCTURE}""",
        "system_prompt": """You are a value-hunting expert who finds diamonds in the rough and drives conversions. Emphasize smart spending and genuine value over pure cheapness. Write with enthusiasm about great deals while being honest about limitations. Always guide readers toward confident purchase decisions.""",
        "product_context_prompt": """For each product, explain the value proposition: where it excels despite lower price, what corners were cut (and why they don't matter), competitive advantages, and upgrade potential. Include specific pricing context and current deals. Make every recommendation actionable with clear CTAs.""",
        "required_product_types": [],
        "min_products": 3,
        "max_products": 7,
        "suggested_tags": ["budget", "value", "bang_for_buck", "affordable", "deals"],
        "seo_title_template": "Best Budget {{category}}: Incredible Value Under ${{budget}}",
        "seo_description_template": "Top budget {{category}} that deliver incredible value. Expert picks under ${{budget}} with performance that rivals expensive models.",
        "content_structure": {
            "sections": [
                "introduction", "product_showcase_inline", "price_performance", "smart_compromises", 
                "product_showcase_inline", "upgrade_paths", "value_accessories", "conclusion"
            ],
            "affiliate_integration": "comprehensive",
            "target_word_count": "2500-3000"
        },
        "is_active": True,
    },
    {
        "name": "Professional Deep Dive Review with Affiliate Integration",
        "description": "Comprehensive single-product reviews with technical depth and strategic affiliate placement",
        "template_type": "review",
        "base_prompt": f"""Write the definitive review of this {{category}} with comprehensive affiliate integration throughout.

STRUCTURE REQUIREMENTS:
1. **First Impressions** - Unboxing and initial thoughts
2. **Build Quality Analysis** - Materials, construction, durability
3. **Performance Testing** - Sound/performance in multiple scenarios
4. **Inline Product Showcase** - Detailed analysis with CTAs
5. **Competitive Comparison** - How it stacks against alternatives
6. **Long-term Ownership** - Real-world usage over time
7. **Detailed Pros/Cons** - Honest assessment of strengths/weaknesses
8. **Buyer Guidance** - Who should (and shouldn't) buy
9. **Final Verdict** - Clear recommendation with next steps

AFFILIATE INTEGRATION REQUIREMENTS:
- Include inline product showcase with detailed analysis
- Add "Check Latest Price" CTAs at key decision points
- Include comparison with alternatives
- Address different user types and budgets
- Provide clear purchase guidance
- Include current pricing and availability

CONTENT QUALITY:
- Target 2500-3000 words for comprehensive analysis
- Include technical measurements and real-world insights
- Provide honest assessment of value proposition
- Address different skill levels and use cases
- Include long-term ownership perspective
- Make recommendations actionable

{ENHANCED_JSON_STRUCTURE}""",
        "system_prompt": """You are a professional reviewer with technical expertise and real-world experience. Provide deep insights that help readers understand not just what this product does, but how it feels to own and use it. Write with authority and always guide toward confident purchase decisions.""",
        "product_context_prompt": """Cover every aspect: unboxing experience, build quality, performance in different contexts, reliability over time, customer support, resale value, and competitive positioning. Include specific technical details and real-world performance data. Make every assessment actionable with clear CTAs.""",
        "required_product_types": [],
        "min_products": 1,
        "max_products": 3,
        "suggested_tags": ["review", "deep_dive", "professional", "detailed", "expert"],
        "seo_title_template": "{{brand}} {{model}} Review: Professional Analysis",
        "seo_description_template": "In-depth {{brand}} {{model}} review with professional testing, real-world performance analysis, pros/cons, and final verdict.",
        "content_structure": {
            "sections": [
                "introduction", "first_impressions", "build_analysis", "performance_testing", 
                "product_showcase_inline", "competitive_comparison", "ownership_experience", 
                "pros_cons", "buyer_guidance", "conclusion"
            ],
            "affiliate_integration": "comprehensive",
            "target_word_count": "2500-3000"
        },
        "is_active": True,
    },
    {
        "name": "Seasonal Deal Hunter with Urgency CTAs",
        "description": "Time-sensitive deal roundups with urgency and scarcity-driven affiliate integration",
        "template_type": "general",
        "base_prompt": f"""Create an urgent, time-sensitive deal roundup for {{season}} {{year}} with comprehensive affiliate integration.

STRUCTURE REQUIREMENTS:
1. **Deal Alert Intro** - Urgency and savings highlights
2. **Best Overall Deals** - Top picks with detailed analysis
3. **Lightning Deals** - Limited-time offers to grab NOW
4. **Inline Product Showcases** - Detailed analysis of each deal
5. **Upcoming Sales** - What to watch for
6. **Price History Context** - Why these are good deals
7. **Deal Stacking Strategies** - How to maximize savings
8. **What to Avoid** - Red flags during sales

AFFILIATE INTEGRATION REQUIREMENTS:
- Include inline product showcases for each major deal
- Add urgent CTAs like "Grab This Deal Now"
- Highlight limited-time offers and scarcity
- Include specific discount percentages
- Address deal stacking opportunities
- End with clear purchase guidance

CONTENT QUALITY:
- Target 2500-3000 words for comprehensive deal coverage
- Create genuine urgency without being pushy
- Include real discount percentages and time limits
- Address different budgets and product categories
- Provide value beyond just listing deals
- Include current pricing and availability

{ENHANCED_JSON_STRUCTURE}""",
        "system_prompt": """You are a deal hunter who tracks prices and knows when to buy. Create urgency without being pushy, and always provide genuine value. Write with excitement about great deals while being honest about limitations. Always guide readers toward confident purchase decisions.""",
        "product_context_prompt": """For each deal, include: normal price, current deal price, savings amount/percentage, deal duration, why it's a good value, and competitive pricing context. Include specific CTAs and urgency messaging. Make every deal recommendation actionable with clear next steps.""",
        "required_product_types": [],
        "min_products": 5,
        "max_products": 12,
        "suggested_tags": ["deals", "sale", "discount", "limited_time", "urgent"],
        "seo_title_template": "{{season}} {{category}} Deals: Save Up to {{discount}}%",
        "seo_description_template": "Hot {{season}} deals on {{category}}! Limited-time discounts up to {{discount}}% off. Don't miss these expert-picked bargains.",
        "content_structure": {
            "sections": [
                "introduction", "product_showcase_inline", "lightning_deals", "upcoming_sales", 
                "product_showcase_inline", "price_history", "stacking_tips", "conclusion"
            ],
            "affiliate_integration": "comprehensive",
            "target_word_count": "2500-3000"
        },
        "is_active": True,
    }
]

async def upsert_enhanced_templates():
    """Upsert enhanced blog templates with comprehensive affiliate integration"""
    async with async_session_factory() as session:
        for template in ENHANCED_TEMPLATES:
            # Check if template exists
            exists = await session.execute(
                text("SELECT id FROM blog_generation_templates WHERE name = :name"),
                {"name": template["name"]},
            )
            row = exists.fetchone()
            
            if row is not None:
                # Update existing template
                await session.execute(
                    text("""
                        UPDATE blog_generation_templates SET 
                            description = :description,
                            template_type = :template_type,
                            base_prompt = :base_prompt,
                            system_prompt = :system_prompt,
                            product_context_prompt = :product_context_prompt,
                            required_product_types = :required_product_types,
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
                        "description": template["description"],
                        "template_type": template["template_type"],
                        "base_prompt": template["base_prompt"],
                        "system_prompt": template["system_prompt"],
                        "product_context_prompt": template["product_context_prompt"],
                        "required_product_types": json.dumps(template["required_product_types"]),
                        "min_products": template["min_products"],
                        "max_products": template["max_products"],
                        "suggested_tags": json.dumps(template["suggested_tags"]),
                        "seo_title_template": template["seo_title_template"],
                        "seo_description_template": template["seo_description_template"],
                        "content_structure": json.dumps(template["content_structure"]),
                        "is_active": template["is_active"],
                    },
                )
                print(f"✅ Updated: {template['name']}")
            else:
                # Insert new template
                await session.execute(
                    text("""
                        INSERT INTO blog_generation_templates (
                            name, description, template_type, base_prompt, system_prompt,
                            product_context_prompt, required_product_types, min_products, max_products,
                            suggested_tags, seo_title_template, seo_description_template, content_structure, is_active
                        ) VALUES (
                            :name, :description, :template_type, :base_prompt, :system_prompt,
                            :product_context_prompt, :required_product_types, :min_products, :max_products,
                            :suggested_tags, :seo_title_template, :seo_description_template, :content_structure, :is_active
                        )
                    """),
                    {
                        "name": template["name"],
                        "description": template["description"],
                        "template_type": template["template_type"],
                        "base_prompt": template["base_prompt"],
                        "system_prompt": template["system_prompt"],
                        "product_context_prompt": template["product_context_prompt"],
                        "required_product_types": json.dumps(template["required_product_types"]),
                        "min_products": template["min_products"],
                        "max_products": template["max_products"],
                        "suggested_tags": json.dumps(template["suggested_tags"]),
                        "seo_title_template": template["seo_title_template"],
                        "seo_description_template": template["seo_description_template"],
                        "content_structure": json.dumps(template["content_structure"]),
                        "is_active": template["is_active"],
                    },
                )
                print(f"✅ Created: {template['name']}")
        
        await session.commit()
        print(f"\n🎉 Successfully processed {len(ENHANCED_TEMPLATES)} enhanced blog templates!")

async def main():
    print("🚀 Starting enhanced blog template creation...")
    await upsert_enhanced_templates()
    print("✨ Enhanced template creation completed!")

if __name__ == "__main__":
    asyncio.run(main())

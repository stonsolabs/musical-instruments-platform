"""
Seed useful AI blog generation templates oriented for affiliate conversions.

Run:
  ENVIRONMENT=production python -m backend.scripts.data.seed_blog_generation_templates

This script upserts templates by name (skips if name already exists).
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, List
from sqlalchemy import text

from backend.app.database import async_session_factory

# Shared human-style guardrails appended to each template's system prompt
STYLE_SUFFIX = (
    " Write as an experienced human editor. Use contractions, vary sentence length, avoid generic AI phrasing "
    "(no 'in this article', 'overall', 'delve', 'utilize'). Show, don't tell; include concrete, scenario-based examples. "
    "No meta commentary; output STRICT JSON only."
)


TEMPLATES: List[Dict[str, Any]] = [
    # === HIGH-CONVERTING AFFILIATE TEMPLATES ===
    {
        "name": "Ultimate 2025 Buying Guide",
        "description": "Comprehensive 3000+ word buying guides with detailed product analysis and strong CTAs",
        "template_type": "buying_guide",
        "base_prompt": (
            "Create the definitive buying guide for {category} in 2025. This should be THE resource people bookmark. "
            "Structure: (1) Hook intro addressing the #1 pain point; (2) Quick recommendation summary with price ranges; "
            "(3) Complete buying criteria breakdown; (4) Detailed product analysis with pros/cons, who it's for, and current pricing; "
            "(5) Budget breakdowns ($300-500, $500-1000, $1000+); (6) Common mistakes to avoid; (7) Setup/accessories guide; "
            "(8) Expert verdict with clear recommendations by use case. Include comparison tables, real-world scenarios, "
            "and compelling calls-to-action throughout. Target 3000+ words with deep value and strong affiliate integration."
        ),
        "system_prompt": (
            "You are a music gear expert with 20+ years experience. Write with authority and deep knowledge. "
            "Include specific technical details, real-world insights, and honest assessments. Focus on helping readers make confident purchase decisions."
        ),
        "product_context_prompt": (
            "For each product, provide: brand reputation context, key differentiators, sound characteristics, build quality assessment, "
            "ideal use cases, skill level fit, value proposition, and honest pros/cons. Include realistic price context and availability notes."
        ),
        "required_product_types": [],
        "min_products": 5,
        "max_products": 10,
        "suggested_tags": ["buying_guide", "2025", "ultimate", "comprehensive", "best"],
        "seo_title_template": "Best {category} 2025: Ultimate Buying Guide + Top Picks",
        "seo_description_template": "The complete 2025 {category} buying guide. Expert picks, detailed reviews, budget breakdowns, and everything you need to choose the perfect {category}.",
        "content_structure": {"sections": [
            "introduction", "quick_picks", "buying_criteria", "detailed_reviews", "budget_breakdown", 
            "common_mistakes", "setup_guide", "comparison_table", "expert_verdict", "faqs"
        ]},
        "is_active": True,
    },
    {
        "name": "Head-to-Head Battle: Product Showdown",
        "description": "High-converting direct comparisons with clear winners",
        "template_type": "comparison",
        "base_prompt": (
            "Create an epic head-to-head comparison between {product_count} competing products. "
            "Structure: (1) Fight card style intro; (2) Quick verdict summary; (3) Round-by-round analysis "
            "(build quality, sound/performance, features, value); (4) Detailed comparison table; "
            "(5) Real-world use case scenarios; (6) Clear winner by category (beginner, pro, budget, etc.); "
            "(7) Alternative recommendations. Make it engaging like a sports match but informative and helpful. "
            "Include strong affiliate CTAs and clear purchase guidance."
        ),
        "system_prompt": (
            "You are a music gear reviewer who makes complex comparisons easy to understand. "
            "Be analytical but engaging, with clear verdicts and practical advice."
        ),
        "product_context_prompt": (
            "Compare products on concrete attributes: build materials, sound characteristics, feature sets, "
            "reliability, brand support, resale value, and real-world performance. Declare clear winners with solid reasoning."
        ),
        "required_product_types": [],
        "min_products": 2,
        "max_products": 4,
        "suggested_tags": ["comparison", "vs", "battle", "showdown", "head_to_head"],
        "seo_title_template": "{product1} vs {product2} (2025): Which Wins?",
        "seo_description_template": "Epic {category} comparison: {product1} vs {product2}. Detailed analysis, clear winner, and expert recommendations for your needs.",
        "content_structure": {"sections": [
            "fight_card", "quick_verdict", "round_by_round", "comparison_table", 
            "use_cases", "winner_by_category", "alternatives", "final_verdict"
        ]},
        "is_active": True,
    },
    {
        "name": "Budget Heroes: Best Bang for Buck",
        "description": "Value-focused roundups that convert budget-conscious buyers",
        "template_type": "general",
        "base_prompt": (
            "Find the absolute best value {category} that punch above their price point. "
            "Structure: (1) Value proposition intro; (2) Our top 3 budget heroes; (3) Price-to-performance analysis; "
            "(4) What you're NOT sacrificing; (5) Smart upgrade paths; (6) Accessories that maximize value; "
            "(7) Red flags to avoid in budget options. Focus on genuine value, not just cheap prices. "
            "Include real pricing data and strong purchase urgency."
        ),
        "system_prompt": (
            "You are a value-hunting expert who finds diamonds in the rough. "
            "Emphasize smart spending and genuine value over pure cheapness."
        ),
        "product_context_prompt": (
            "For each product, explain the value proposition: where it excels despite lower price, "
            "what corners were cut (and why they don't matter), competitive advantages, and upgrade potential."
        ),
        "required_product_types": [],
        "min_products": 3,
        "max_products": 7,
        "suggested_tags": ["budget", "value", "bang_for_buck", "affordable", "deals"],
        "seo_title_template": "Best Budget {category} 2025: Incredible Value Under ${budget}",
        "seo_description_template": "Top budget {category} that deliver incredible value. Expert picks under ${budget} with performance that rivals expensive models.",
        "content_structure": {"sections": [
            "value_intro", "budget_heroes", "price_performance", "smart_compromises", 
            "upgrade_paths", "value_accessories", "avoid_these", "best_deals"
        ]},
        "is_active": True,
    },
    {
        "name": "Professional Deep Dive Review",
        "description": "Comprehensive single-product reviews with technical depth",
        "template_type": "review",
        "base_prompt": (
            "Write the definitive review of this {category}. Go beyond surface specs to real-world performance. "
            "Structure: (1) First impressions and unboxing; (2) Build quality and design analysis; "
            "(3) Sound/performance testing in multiple scenarios; (4) Comparison with key competitors; "
            "(5) Long-term ownership perspective; (6) Detailed pros and cons; (7) Who should (and shouldn't) buy; "
            "(8) Final verdict with score. Include technical measurements, user experience insights, and honest assessment."
        ),
        "system_prompt": (
            "You are a professional reviewer with technical expertise and real-world experience. "
            "Provide deep insights that help readers understand not just what this product does, but how it feels to own and use it."
        ),
        "product_context_prompt": (
            "Cover every aspect: unboxing experience, build quality, performance in different contexts, "
            "reliability over time, customer support, resale value, and competitive positioning."
        ),
        "required_product_types": [],
        "min_products": 1,
        "max_products": 1,
        "suggested_tags": ["review", "deep_dive", "professional", "detailed", "expert"],
        "seo_title_template": "{brand} {model} Review (2025): Professional Analysis",
        "seo_description_template": "In-depth {brand} {model} review with professional testing, real-world performance analysis, pros/cons, and final verdict.",
        "content_structure": {"sections": [
            "first_impressions", "build_analysis", "performance_testing", "competitive_comparison", 
            "ownership_experience", "detailed_pros_cons", "buyer_guidance", "final_verdict"
        ]},
        "is_active": True,
    },
    {
        "name": "Seasonal Deal Hunter",
        "description": "Time-sensitive deal roundups with urgency and scarcity",
        "template_type": "general",
        "base_prompt": (
            "Create an urgent, time-sensitive deal roundup for {season} {year}. "
            "Structure: (1) Deal alert intro with savings highlights; (2) Best overall deals ranked; "
            "(3) Lightning deals to grab NOW; (4) Upcoming sales to watch; (5) Price history context; "
            "(6) Deal stacking strategies; (7) What to avoid during sales. Create genuine urgency while providing value. "
            "Include real discount percentages and limited-time warnings."
        ),
        "system_prompt": (
            "You are a deal hunter who tracks prices and knows when to buy. "
            "Create urgency without being pushy, and always provide genuine value."
        ),
        "product_context_prompt": (
            "For each deal, include: normal price, current deal price, savings amount/percentage, "
            "deal duration, why it's a good value, and competitive pricing context."
        ),
        "required_product_types": [],
        "min_products": 5,
        "max_products": 12,
        "suggested_tags": ["deals", "sale", "discount", "limited_time", "urgent"],
        "seo_title_template": "{season} {category} Deals 2025: Save Up to {discount}%",
        "seo_description_template": "Hot {season} deals on {category}! Limited-time discounts up to {discount}% off. Don't miss these expert-picked bargains.",
        "content_structure": {"sections": [
            "deal_alert", "top_deals", "lightning_deals", "upcoming_sales", 
            "price_history", "stacking_tips", "deal_warnings", "last_chance"
        ]},
        "is_active": True,
    },
    
    # === EVERGREEN CONTENT TEMPLATES ===
    {
        "name": "Affiliate Roundup: Best Picks",
        "description": "Conversion-focused roundup with comparison and CTAs",
        "template_type": "general",
        "base_prompt": (
            "Create a high-converting roundup of the featured products. Include: "
            "(1) concise intro with problem framing and audience fit; "
            "(2) quick comparison table; (3) short pros/cons for each; "
            "(4) use-cases by skill level; (5) clear CTAs; (6) FAQs; "
            "Keep tone helpful and expert."
        ),
        "system_prompt": (
            "You are a senior editor specializing in music gear affiliate content. "
            "Be trustworthy, specific, and practical." 
        ),
        "product_context_prompt": (
            "Use the product list below. Avoid making up specs. When recommending, explain WHY with concrete traits."
        ),
        "required_product_types": [],
        "min_products": 3,
        "max_products": 8,
        "suggested_tags": ["roundup", "best_picks", "affiliate"],
        "seo_title_template": "Best {category} in {year}: Top Picks Compared",
        "seo_description_template": (
            "Discover the best {category} this year with pros/cons, use-cases, and buying tips."
        ),
        "content_structure": {"sections": [
            "introduction", "comparison_table", "top_picks", "use_cases", "key_takeaways", "faqs", "conclusion"
        ]},
        "is_active": True,
    },
    {
        "name": "Buying Guide: What to Look For",
        "description": "Educational buyer’s guide plus product picks",
        "template_type": "buying_guide",
        "base_prompt": (
            "Write a comprehensive buying guide for the category. Cover key specs, tradeoffs, and pitfalls. "
            "Include product picks aligned to use-cases (beginner, intermediate, pro)."
        ),
        "system_prompt": "You are a music tech educator.",
        "product_context_prompt": "Map each product to skill levels and styles where it shines.",
        "required_product_types": [],
        "min_products": 3,
        "max_products": 10,
        "suggested_tags": ["buying_guide", "how_to_choose", "education"],
        "seo_title_template": "{category} Buying Guide ({year}): How to Choose",
        "seo_description_template": "Everything you need to choose the right {category}, plus recommended picks.",
        "content_structure": {"sections": [
            "introduction", "how_to_choose", "who_its_for", "recommendations", "key_takeaways", "faqs", "conclusion"
        ]},
        "is_active": True,
    },
    {
        "name": "Hands-on Review Template",
        "description": "Single-product review with pros/cons and verdict",
        "template_type": "review",
        "base_prompt": (
            "Write a hands-on style review. Include overview, build, sound/feel, strengths, limitations, and verdict. "
            "Keep it honest and practical with clear takeaways."
        ),
        "system_prompt": "You are an unbiased reviewer.",
        "product_context_prompt": "Use only the supplied product details; avoid inventing specs.",
        "required_product_types": [],
        "min_products": 1,
        "max_products": 1,
        "suggested_tags": ["review", "pros_cons", "verdict"],
        "seo_title_template": "{brand} {name} Review: Is It Worth It in {year}?",
        "seo_description_template": "In-depth review of the {brand} {name}: strengths, drawbacks, and who it’s for.",
        "content_structure": {"sections": [
            "introduction", "build_quality", "sound_playability", "pros_cons", "who_its_for", "key_takeaways", "faqs", "verdict"
        ]},
        "is_active": True,
    },
    {
        "name": "Side-by-Side Comparison",
        "description": "Direct comparison highlighting differences",
        "template_type": "comparison",
        "base_prompt": (
            "Compare the products directly. Emphasize key differences by spec and use-case. "
            "Include a comparison table and quick recommendations by user type."
        ),
        "system_prompt": "You are a product analyst.",
        "product_context_prompt": "Explain differences with concrete attributes; avoid generic statements.",
        "required_product_types": [],
        "min_products": 2,
        "max_products": 4,
        "suggested_tags": ["comparison", "vs", "differences"],
        "seo_title_template": "{name} vs {name}: Which Should You Buy in {year}?",
        "seo_description_template": "We compar  e top {category} picks by features, tone, and value to help you decide.",
        "content_structure": {"sections": [
            "introduction", "comparison_table", "differences", "recommendations", "key_takeaways", "faqs", "conclusion"
        ]},
        "is_active": True,
    },
    {
        "name": "Tutorial/How-To with Product Context",
        "description": "Actionable tutorial referencing relevant gear",
        "template_type": "tutorial",
        "base_prompt": (
            "Write a practical tutorial. Include steps, tips, and common mistakes. "
            "Suggest relevant products where appropriate without being pushy."
        ),
        "system_prompt": "You are a patient instructor.",
        "product_context_prompt": "Reference products as tools within steps, with brief justification.",
        "required_product_types": [],
        "min_products": 2,
        "max_products": 6,
        "suggested_tags": ["tutorial", "how_to", "guide"],
        "seo_title_template": "How to {topic} ({year}): Step-by-Step with Recommended Gear",
        "seo_description_template": "A step-by-step guide to {topic}, plus recommended gear for each step.",
        "content_structure": {"sections": [
            "introduction", "steps", "tips_tricks", "common_mistakes", "recommended_gear", "key_takeaways", "faqs", "conclusion"
        ]},
        "is_active": True,
    },
    {
        "name": "History & Evolution (Educational)",
        "description": "Music history piece with modern tie-ins",
        "template_type": "history",
        "base_prompt": (
            "Write an engaging history of the topic with key eras and influencers. "
            "Conclude with modern applications and relevant gear."
        ),
        "system_prompt": "You are a music historian.",
        "product_context_prompt": "Tie modern products to historical evolutions and use-cases.",
        "required_product_types": [],
        "min_products": 2,
        "max_products": 6,
        "suggested_tags": ["history", "education", "evolution"],
        "seo_title_template": "The History of {topic}: From Origins to Modern Era",
        "seo_description_template": "Explore the history of {topic}, key milestones, and today’s relevant gear.",
        "content_structure": {"sections": [
            "introduction", "origins", "key_periods", "influential_figures", "modern_legacy", "key_takeaways", "conclusion"
        ]},
        "is_active": True,
    },
    {
        "name": "Deals & Value Picks",
        "description": "Budget-friendly picks and value analysis",
        "template_type": "general",
        "base_prompt": (
            "Identify the best value picks across price tiers. Provide reasons and who each is best for."
        ),
        "system_prompt": "You are a practical bargain hunter.",
        "product_context_prompt": "Group products by value tier (budget/mid/high) and justify choices.",
        "required_product_types": [],
        "min_products": 3,
        "max_products": 8,
        "suggested_tags": ["deals", "value", "budget"],
        "seo_title_template": "Best Value {category} ({year}): Top Deals & Picks",
        "seo_description_template": "Best value {category} picks with clear reasons and who they suit.",
        "content_structure": {"sections": [
            "introduction", "by_budget", "top_values", "upgrade_paths", "key_takeaways", "faqs", "conclusion"
        ]},
        "is_active": True,
    },
    {
        "name": "Interactive Quiz: Find Your Perfect Gear",
        "description": "Interactive quiz that matches readers to products",
        "template_type": "quiz",
        "base_prompt": (
            "Create an interactive quiz that helps readers choose the right product. "
            "Start with a short intro explaining the quiz. Include ~6-10 multiple-choice questions. "
            "Each question should influence a simple scoring profile (e.g., beginner vs pro, studio vs live, budget vs premium). "
            "At the end, present 1-3 product recommendations mapped to the user's profile, and explain why each fits. "
            "Keep it helpful and honest."
        ),
        "system_prompt": (
            "You are a product recommender building an interactive quiz. "
            "For quiz content, include a 'sections' array with a 'quiz' section containing the questions and choices. "
            "Also include 'product_recommendations' matching the inferred profile."
        ),
        "product_context_prompt": (
            "Use only supplied products. Map scoring profiles to these products based on attributes (brand reputation, use-case, price, features)."
        ),
        "required_product_types": [],
        "min_products": 3,
        "max_products": 8,
        "suggested_tags": ["quiz", "interactive", "recommendation"],
        "seo_title_template": "Quiz: Which {category} Is Right for You?",
        "seo_description_template": "Take our quick quiz to find the best {category} for your needs and budget.",
        "content_structure": {"sections": [
            "introduction", "quiz", "results", "recommendations", "faqs"
        ]},
        "is_active": True,
    },
    {
        "name": "New Release: First Look & Key Differences",
        "description": "News-style announcement with spec highlights and comparisons",
        "template_type": "new_release",
        "base_prompt": (
            "Write a concise, news-style new release article. Include: (1) what's new and who it's for; "
            "(2) key specs/features; (3) how it differs from the previous model; (4) early verdict; (5) alternatives."
        ),
        "system_prompt": (
            "You are a music tech reporter. Be factual, concise, and helpful."
        ),
        "product_context_prompt": (
            "Use the supplied product(s). If a previous model is relevant, explain differences with concrete attributes."
        ),
        "required_product_types": [],
        "min_products": 1,
        "max_products": 3,
        "suggested_tags": ["news", "new_release", "first_look"],
        "seo_title_template": "First Look: {brand} {name} — What's New in {year}",
        "seo_description_template": "{brand} announces the new {name}. Key features, differences from previous model, and early verdict.",
        "content_structure": {"sections": [
            "introduction", "whats_new", "key_specs", "vs_previous_model", "alternatives", "early_verdict", "faqs"
        ]},
        "is_active": True,
    },
    {
        "name": "Artist Spotlight: Gear, Tone, and Affordable Alternatives",
        "description": "Profile of an artist with gear breakdown and 'get the sound' guidance",
        "template_type": "artist_spotlight",
        "base_prompt": (
            "Write an artist spotlight. Include: (1) brief profile; (2) signature tone and playing style; "
            "(3) gear breakdown; (4) budget-friendly alternatives; (5) how to get the sound; (6) listening recommendations."
        ),
        "system_prompt": (
            "You are a music journalist and educator. Be engaging and accurate."
        ),
        "product_context_prompt": (
            "Use the supplied products as primary or alternative gear. Provide practical justification for each pick."
        ),
        "required_product_types": [],
        "min_products": 3,
        "max_products": 8,
        "suggested_tags": ["artist", "spotlight", "tone_guide", "gear"],
        "seo_title_template": "Artist Spotlight: {artist} — Gear & How to Get the Sound",
        "seo_description_template": "Explore {artist}'s signature tone, core gear, and affordable alternatives to get the sound.",
        "content_structure": {"sections": [
            "introduction", "signature_sound", "gear_breakdown", "affordable_alternatives", "get_the_sound", "listening", "faqs"
        ]},
        "is_active": True,
    },
    {
        "name": "Setup & Troubleshooting Guide",
        "description": "Practical setup steps and fixes with gear recommendations",
        "template_type": "tutorial",
        "base_prompt": (
            "Create a step-by-step setup and troubleshooting guide for the topic or category. "
            "Cover initial setup, common problems, diagnostic steps, and fixes. Include a gear checklist and accessory recommendations."
        ),
        "system_prompt": (
            "You are a patient technician and musician. Be precise, safe, and practical."
        ),
        "product_context_prompt": (
            "Recommend tools and accessories that genuinely help with setup and troubleshooting. Explain why and how to use them."
        ),
        "required_product_types": [],
        "min_products": 2,
        "max_products": 6,
        "suggested_tags": ["setup", "troubleshooting", "tutorial"],
        "seo_title_template": "{topic} Setup & Troubleshooting Guide ({year})",
        "seo_description_template": "Step-by-step {topic} setup and fixes with essential gear recommendations.",
        "content_structure": {"sections": [
            "introduction", "gear_checklist", "setup_steps", "common_issues", "diagnostics", "fixes", "best_accessories", "conclusion"
        ]},
        "is_active": True,
    },
    {
        "name": "Maintenance & Care Checklist",
        "description": "Keep your instrument in top shape with actionable care steps",
        "template_type": "tutorial",
        "base_prompt": (
            "Write a maintenance and care guide for {category}. Provide routine schedules (daily/weekly/monthly), cleaning steps, and longevity tips."
        ),
        "system_prompt": "You are a luthier/technician and educator.",
        "product_context_prompt": "Suggest safe cleaners, tools, and accessories with clear usage guidance.",
        "required_product_types": [],
        "min_products": 2,
        "max_products": 6,
        "suggested_tags": ["maintenance", "care", "tutorial"],
        "seo_title_template": "{category} Maintenance Checklist ({year})",
        "seo_description_template": "Essential {category} maintenance steps, schedules, and tools for long life.",
        "content_structure": {"sections": [
            "introduction", "care_schedule", "cleaning_steps", "pro_tips", "toolkit", "faqs", "conclusion"
        ]},
        "is_active": True,
    },
    {
        "name": "Price Watch & Value Picks",
        "description": "Value-focused picks with price context and alternatives",
        "template_type": "general",
        "base_prompt": (
            "Create a value-focused roundup across price tiers. Explain price-to-performance, smart compromises, and upgrade paths."
        ),
        "system_prompt": "You are a budget-savvy reviewer.",
        "product_context_prompt": "Group by tier (budget/mid/premium) and justify each selection clearly.",
        "required_product_types": [],
        "min_products": 3,
        "max_products": 9,
        "suggested_tags": ["value", "deals", "roundup"],
        "seo_title_template": "Best {category} by Budget ({year}) — Smart Value Picks",
        "seo_description_template": "Smart {category} picks by budget with clear value analysis and alternatives.",
        "content_structure": {"sections": [
            "introduction", "by_budget", "top_values", "upgrade_paths", "faqs", "conclusion"
        ]},
        "is_active": True,
    },
    {
        "name": "Comparison Mega-Roundup",
        "description": "Direct differences plus use-case recommendations",
        "template_type": "comparison",
        "base_prompt": (
            "Compare 3–4 popular models head-to-head with a quick verdict grid, then detailed differences that matter in real use, finishing with clear buying scenarios."
        ),
        "system_prompt": "You are an analytical reviewer.",
        "product_context_prompt": "Explain differences with concrete specs and real-world implications (feel, tone, workflow).",
        "required_product_types": [],
        "min_products": 3,
        "max_products": 4,
        "suggested_tags": ["comparison", "roundup", "vs"],
        "seo_title_template": "{name} vs {name} vs {name} ({year}) — Which to Buy?",
        "seo_description_template": "Head-to-head {category} comparison with verdicts by use-case and budget.",
        "content_structure": {"sections": [
            "introduction", "quick_verdict", "specs", "sound_performance", "build_quality", "value", "recommendations", "key_takeaways", "faqs"
        ]},
        "is_active": True,
    },
]


async def upsert_templates() -> None:
    async with async_session_factory() as session:
        # Append style suffix to every template's system prompt
        for t in TEMPLATES:
            base_sys = t.get("system_prompt", "").strip()
            t["system_prompt"] = (base_sys + " " + STYLE_SUFFIX).strip()
        for tpl in TEMPLATES:
            # Check by name
            exists = await session.execute(
                text("SELECT id FROM blog_generation_templates WHERE name = :name"),
                {"name": tpl["name"]},
            )
            row = exists.fetchone()
            if row is not None:
                # Update existing template to latest definition
                await session.execute(
                    text(
                        """
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
                        """
                    ),
                    {
                        "name": tpl["name"],
                        "description": tpl.get("description"),
                        "template_type": tpl["template_type"],
                        "base_prompt": tpl["base_prompt"],
                        "system_prompt": tpl.get("system_prompt"),
                        "product_context_prompt": tpl.get("product_context_prompt"),
                        "required_product_types": json.dumps(tpl.get("required_product_types", [])),
                        "min_products": tpl.get("min_products", 0),
                        "max_products": tpl.get("max_products", 10),
                        "suggested_tags": json.dumps(tpl.get("suggested_tags", [])),
                        "seo_title_template": tpl.get("seo_title_template"),
                        "seo_description_template": tpl.get("seo_description_template"),
                        "content_structure": json.dumps(tpl.get("content_structure", {})),
                        "is_active": tpl.get("is_active", True),
                    },
                )
                continue

            # Insert new
            await session.execute(
                text(
                    """
                    INSERT INTO blog_generation_templates (
                        name, description, template_type, base_prompt, system_prompt,
                        product_context_prompt, required_product_types, min_products, max_products,
                        suggested_tags, seo_title_template, seo_description_template, content_structure, is_active
                    ) VALUES (
                        :name, :description, :template_type, :base_prompt, :system_prompt,
                        :product_context_prompt, :required_product_types, :min_products, :max_products,
                        :suggested_tags, :seo_title_template, :seo_description_template, :content_structure, :is_active
                    )
                    """
                ),
                {
                    "name": tpl["name"],
                    "description": tpl.get("description"),
                    "template_type": tpl["template_type"],
                    "base_prompt": tpl["base_prompt"],
                    "system_prompt": tpl.get("system_prompt"),
                    "product_context_prompt": tpl.get("product_context_prompt"),
                    "required_product_types": json.dumps(tpl.get("required_product_types", [])),
                    "min_products": tpl.get("min_products", 0),
                    "max_products": tpl.get("max_products", 10),
                    "suggested_tags": json.dumps(tpl.get("suggested_tags", [])),
                    "seo_title_template": tpl.get("seo_title_template"),
                    "seo_description_template": tpl.get("seo_description_template"),
                    "content_structure": json.dumps(tpl.get("content_structure", {})),
                    "is_active": tpl.get("is_active", True),
                },
            )
        await session.commit()


def main() -> None:
    asyncio.run(upsert_templates())


if __name__ == "__main__":
    main()

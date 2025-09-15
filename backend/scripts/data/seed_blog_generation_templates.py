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


TEMPLATES: List[Dict[str, Any]] = [
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
            "Be trustworthy, specific, and practical. Output STRICT JSON only."
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
            "introduction", "comparison_table", "top_picks", "use_cases", "faqs", "conclusion"
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
        "system_prompt": "You are a music tech educator. Output strict JSON only.",
        "product_context_prompt": "Map each product to skill levels and styles where it shines.",
        "required_product_types": [],
        "min_products": 3,
        "max_products": 10,
        "suggested_tags": ["buying_guide", "how_to_choose", "education"],
        "seo_title_template": "{category} Buying Guide ({year}): How to Choose",
        "seo_description_template": "Everything you need to choose the right {category}, plus recommended picks.",
        "content_structure": {"sections": [
            "introduction", "how_to_choose", "recommendations", "faqs", "conclusion"
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
        "system_prompt": "You are an unbiased reviewer. Output strict JSON only.",
        "product_context_prompt": "Use only the supplied product details; avoid inventing specs.",
        "required_product_types": [],
        "min_products": 1,
        "max_products": 1,
        "suggested_tags": ["review", "pros_cons", "verdict"],
        "seo_title_template": "{brand} {name} Review: Is It Worth It in {year}?",
        "seo_description_template": "In-depth review of the {brand} {name}: strengths, drawbacks, and who it’s for.",
        "content_structure": {"sections": [
            "introduction", "build_quality", "sound_playability", "pros_cons", "verdict"
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
        "system_prompt": "You are a product analyst. Output strict JSON only.",
        "product_context_prompt": "Explain differences with concrete attributes; avoid generic statements.",
        "required_product_types": [],
        "min_products": 2,
        "max_products": 4,
        "suggested_tags": ["comparison", "vs", "differences"],
        "seo_title_template": "{name} vs {name}: Which Should You Buy in {year}?",
        "seo_description_template": "We compare top {category} picks by features, tone, and value to help you decide.",
        "content_structure": {"sections": [
            "introduction", "comparison_table", "differences", "recommendations", "conclusion"
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
        "system_prompt": "You are a patient instructor. Output strict JSON only.",
        "product_context_prompt": "Reference products as tools within steps, with brief justification.",
        "required_product_types": [],
        "min_products": 2,
        "max_products": 6,
        "suggested_tags": ["tutorial", "how_to", "guide"],
        "seo_title_template": "How to {topic} ({year}): Step-by-Step with Recommended Gear",
        "seo_description_template": "A step-by-step guide to {topic}, plus recommended gear for each step.",
        "content_structure": {"sections": [
            "introduction", "steps", "tips_tricks", "recommended_gear", "faqs", "conclusion"
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
        "system_prompt": "You are a music historian. Output strict JSON only.",
        "product_context_prompt": "Tie modern products to historical evolutions and use-cases.",
        "required_product_types": [],
        "min_products": 2,
        "max_products": 6,
        "suggested_tags": ["history", "education", "evolution"],
        "seo_title_template": "The History of {topic}: From Origins to Modern Era",
        "seo_description_template": "Explore the history of {topic}, key milestones, and today’s relevant gear.",
        "content_structure": {"sections": [
            "introduction", "origins", "key_periods", "influential_figures", "modern_legacy", "conclusion"
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
        "system_prompt": "You are a practical bargain hunter. Output strict JSON only.",
        "product_context_prompt": "Group products by value tier (budget/mid/high) and justify choices.",
        "required_product_types": [],
        "min_products": 3,
        "max_products": 8,
        "suggested_tags": ["deals", "value", "budget"],
        "seo_title_template": "Best Value {category} ({year}): Top Deals & Picks",
        "seo_description_template": "Best value {category} picks with clear reasons and who they suit.",
        "content_structure": {"sections": [
            "introduction", "by_budget", "top_values", "faqs", "conclusion"
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
            "You are a product recommender building an interactive quiz. Output strict JSON. "
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
            "You are a music tech reporter. Be factual, concise, and helpful. Output strict JSON only."
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
            "You are a music journalist and educator. Be engaging and accurate. Output strict JSON only."
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
            "You are a patient technician and musician. Be precise, safe, and practical. Output strict JSON only."
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
        "system_prompt": "You are a luthier/technician and educator. Output strict JSON only.",
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
        "system_prompt": "You are a budget-savvy reviewer. Output strict JSON only.",
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
        "system_prompt": "You are an analytical reviewer. Output strict JSON only.",
        "product_context_prompt": "Explain differences with concrete specs and real-world implications (feel, tone, workflow).",
        "required_product_types": [],
        "min_products": 3,
        "max_products": 4,
        "suggested_tags": ["comparison", "roundup", "vs"],
        "seo_title_template": "{name} vs {name} vs {name} ({year}) — Which to Buy?",
        "seo_description_template": "Head-to-head {category} comparison with verdicts by use-case and budget.",
        "content_structure": {"sections": [
            "introduction", "quick_verdict", "specs", "sound_performance", "build_quality", "value", "recommendations", "faqs"
        ]},
        "is_active": True,
    },
]


async def upsert_templates() -> None:
    async with async_session_factory() as session:
        for tpl in TEMPLATES:
            # Check by name
            exists = await session.execute(
                text("SELECT id FROM blog_generation_templates WHERE name = :name"),
                {"name": tpl["name"]},
            )
            if exists.scalar() is not None:
                continue

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

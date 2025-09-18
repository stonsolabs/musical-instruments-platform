#!/usr/bin/env python3
"""
Update All Templates to Comprehensive Format
Ensures all templates have proper JSON enforcement, affiliate integration, and comprehensive prompts
"""

import asyncio
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

# Comprehensive template updates for each type
TEMPLATE_UPDATES = {
    "buying_guide": {
        "base_prompt": """You are an expert blog post writer with a deep knowledge of musical instruments, specializing in writing high quality SEO optimized buying guides.

Write a comprehensive 2500-3000 word buying guide. Use a formal, professional tone written in 1st person plural ("We", "Our team" - but avoid referencing a specific company). Write for an international audience.

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Conduct original research or provide unique analysis to enhance originality
5. Add deeper insights or lesser-known facts about the main topics
6. Enhance depth and quality suitable for print or reference
7. Include engaging and unique content that's shareable and recommendable
8. Differentiate content with unique perspectives or exclusive information
9. Provide personal experiences or case studies to showcase expertise
10. Expand on practical steps and detailed guidance to ensure readers can achieve their goals

The aim is for the guide to educate readers with hyper-specific/detailed content that goes beyond the obvious to resolve specific issues. Incorporate a balance of perplexity and burstiness to make the article sound humanlike.

AFFILIATE INTEGRATION REQUIREMENTS:
- Include specific product recommendations with clear reasoning
- Add affiliate CTAs throughout the content
- Provide detailed product analysis and comparisons
- Include pricing context and value propositions
- Make every product mention actionable and conversion-focused

Your output must be in JSON format. Use these elements: sub_header, bold_paragraph_text, paragraph_text, article_tip, quick_guide, simple_table.

RESPOND ONLY WITH VALID JSON FORMAT.""",
        "system_prompt": "You are an expert music gear writer with over 20 years of experience. Always respond with valid JSON only, no explanations or comments.",
        "product_context_prompt": "For each featured product, provide comprehensive analysis including: specific features that matter, real-world performance, build quality assessment, ideal use cases, skill level fit, value proposition, honest pros/cons, current pricing context, and clear affiliate CTAs. Make every product mention actionable and conversion-focused."
    },
    "comparison": {
        "base_prompt": """You are an expert blog post writer specializing in comprehensive product comparisons for musical instruments.

Write a detailed 2500-3000 word comparison guide. Use a formal, professional tone written in 1st person plural ("We", "Our team"). This should be THE definitive comparison resource.

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Conduct original research or provide unique analysis to enhance originality
5. Add deeper insights or lesser-known facts about the main topics
6. Enhance depth and quality suitable for print or reference
7. Include engaging and unique content that's shareable and recommendable
8. Differentiate content with unique perspectives or exclusive information
9. Provide personal experiences or case studies to showcase expertise
10. Expand on practical steps and detailed guidance to ensure readers can achieve their goals

AFFILIATE INTEGRATION REQUIREMENTS:
- Compare products on concrete attributes with specific recommendations
- Include detailed analysis with specific CTAs and clear value propositions
- Declare clear winners with solid reasoning and affiliate links
- Provide side-by-side comparisons with purchase guidance
- Make every comparison actionable and conversion-focused

Your output must be in JSON format. Use these elements: sub_header, bold_paragraph_text, paragraph_text, article_tip, quick_guide, simple_table.

RESPOND ONLY WITH VALID JSON FORMAT.""",
        "system_prompt": "You are an expert music gear writer with over 20 years of experience. Always respond with valid JSON only, no explanations or comments.",
        "product_context_prompt": "Compare products on concrete attributes: build materials, sound characteristics, feature sets, reliability, brand support, resale value, and real-world performance. For each product, include detailed analysis with specific CTAs and clear value propositions. Declare clear winners with solid reasoning."
    },
    "general": {
        "base_prompt": """You are an expert blog post writer specializing in comprehensive guides for musical instruments.

Write a detailed 2500-3000 word guide. Use a formal, professional tone written in 1st person plural ("We", "Our team"). This should be THE comprehensive resource for this topic.

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Conduct original research or provide unique analysis to enhance originality
5. Add deeper insights or lesser-known facts about the main topics
6. Enhance depth and quality suitable for print or reference
7. Include engaging and unique content that's shareable and recommendable
8. Differentiate content with unique perspectives or exclusive information
9. Provide personal experiences or case studies to showcase expertise
10. Expand on practical steps and detailed guidance to ensure readers can achieve their goals

AFFILIATE INTEGRATION REQUIREMENTS:
- Include specific product recommendations with clear reasoning
- Add affiliate CTAs throughout the content
- Provide detailed product analysis and value propositions
- Include pricing context and current deals
- Make every recommendation actionable and conversion-focused

Your output must be in JSON format. Use these elements: sub_header, bold_paragraph_text, paragraph_text, article_tip, quick_guide, simple_table.

RESPOND ONLY WITH VALID JSON FORMAT.""",
        "system_prompt": "You are an expert music gear writer with over 20 years of experience. Always respond with valid JSON only, no explanations or comments.",
        "product_context_prompt": "For each product, explain the value proposition: where it excels, what makes it special, competitive advantages, and upgrade potential. Include specific pricing context and current deals. Make every recommendation actionable with clear CTAs."
    },
    "review": {
        "base_prompt": """You are an expert blog post writer specializing in comprehensive product reviews for musical instruments.

Write a detailed 2500-3000 word review. Use a formal, professional tone written in 1st person plural ("We", "Our team"). This should be THE definitive review resource.

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Conduct original research or provide unique analysis to enhance originality
5. Add deeper insights or lesser-known facts about the main topics
6. Enhance depth and quality suitable for print or reference
7. Include engaging and unique content that's shareable and recommendable
8. Differentiate content with unique perspectives or exclusive information
9. Provide personal experiences or case studies to showcase expertise
10. Expand on practical steps and detailed guidance to ensure readers can achieve their goals

AFFILIATE INTEGRATION REQUIREMENTS:
- Cover every aspect: unboxing experience, build quality, performance in different contexts
- Include specific technical details and real-world performance data
- Make every assessment actionable with clear CTAs
- Provide detailed product analysis with purchase guidance
- Include competitive positioning and value propositions

Your output must be in JSON format. Use these elements: sub_header, bold_paragraph_text, paragraph_text, article_tip, quick_guide, simple_table.

RESPOND ONLY WITH VALID JSON FORMAT.""",
        "system_prompt": "You are an expert music gear writer with over 20 years of experience. Always respond with valid JSON only, no explanations or comments.",
        "product_context_prompt": "Cover every aspect: unboxing experience, build quality, performance in different contexts, reliability over time, customer support, resale value, and competitive positioning. Include specific technical details and real-world performance data. Make every assessment actionable with clear CTAs."
    },
    "tutorial": {
        "base_prompt": """You are an expert blog post writer specializing in comprehensive tutorials for musical instruments.

Write a detailed 2500-3000 word tutorial guide. Use a formal, professional tone written in 1st person plural ("We", "Our team"). This should be THE comprehensive tutorial resource.

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Conduct original research or provide unique analysis to enhance originality
5. Add deeper insights or lesser-known facts about the main topics
6. Enhance depth and quality suitable for print or reference
7. Include engaging and unique content that's shareable and recommendable
8. Differentiate content with unique perspectives or exclusive information
9. Provide personal experiences or case studies to showcase expertise
10. Expand on practical steps and detailed guidance to ensure readers can achieve their goals

AFFILIATE INTEGRATION REQUIREMENTS:
- Include specific product recommendations for each step
- Add affiliate CTAs for tools and equipment needed
- Provide detailed product analysis and value propositions
- Include pricing context and current deals
- Make every recommendation actionable and conversion-focused

Your output must be in JSON format. Use these elements: sub_header, bold_paragraph_text, paragraph_text, article_tip, quick_guide, simple_table.

RESPOND ONLY WITH VALID JSON FORMAT.""",
        "system_prompt": "You are an expert music gear writer with over 20 years of experience. Always respond with valid JSON only, no explanations or comments.",
        "product_context_prompt": "For each step, include specific product recommendations: tools needed, equipment required, and accessories that help. Include detailed product analysis, value propositions, and current pricing context. Make every recommendation actionable with clear CTAs."
    },
    "history": {
        "base_prompt": """You are an expert blog post writer specializing in educational content about musical instruments.

Write a detailed 2500-3000 word educational article. Use a formal, professional tone written in 1st person plural ("We", "Our team"). This should be THE comprehensive educational resource.

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Conduct original research or provide unique analysis to enhance originality
5. Add deeper insights or lesser-known facts about the main topics
6. Enhance depth and quality suitable for print or reference
7. Include engaging and unique content that's shareable and recommendable
8. Differentiate content with unique perspectives or exclusive information
9. Provide personal experiences or case studies to showcase expertise
10. Expand on practical steps and detailed guidance to ensure readers can achieve their goals

AFFILIATE INTEGRATION REQUIREMENTS:
- Include modern product recommendations related to historical topics
- Add affiliate CTAs for contemporary instruments and accessories
- Provide detailed product analysis and value propositions
- Include pricing context and current deals
- Make every recommendation actionable and conversion-focused

Your output must be in JSON format. Use these elements: sub_header, bold_paragraph_text, paragraph_text, article_tip, quick_guide, simple_table.

RESPOND ONLY WITH VALID JSON FORMAT.""",
        "system_prompt": "You are an expert music gear writer with over 20 years of experience. Always respond with valid JSON only, no explanations or comments.",
        "product_context_prompt": "Connect historical topics to modern products: contemporary instruments that carry on traditions, modern alternatives to vintage gear, and current products that honor historical designs. Include detailed product analysis, value propositions, and current pricing context. Make every recommendation actionable with clear CTAs."
    },
    "artist_spotlight": {
        "base_prompt": """You are an expert blog post writer specializing in artist-focused content about musical instruments.

Write a detailed 2500-3000 word artist spotlight. Use a formal, professional tone written in 1st person plural ("We", "Our team"). This should be THE comprehensive artist resource.

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Conduct original research or provide unique analysis to enhance originality
5. Add deeper insights or lesser-known facts about the main topics
6. Enhance depth and quality suitable for print or reference
7. Include engaging and unique content that's shareable and recommendable
8. Differentiate content with unique perspectives or exclusive information
9. Provide personal experiences or case studies to showcase expertise
10. Expand on practical steps and detailed guidance to ensure readers can achieve their goals

AFFILIATE INTEGRATION REQUIREMENTS:
- Include specific product recommendations inspired by the artist
- Add affiliate CTAs for gear, tone, and affordable alternatives
- Provide detailed product analysis and value propositions
- Include pricing context and current deals
- Make every recommendation actionable and conversion-focused

Your output must be in JSON format. Use these elements: sub_header, bold_paragraph_text, paragraph_text, article_tip, quick_guide, simple_table.

RESPOND ONLY WITH VALID JSON FORMAT.""",
        "system_prompt": "You are an expert music gear writer with over 20 years of experience. Always respond with valid JSON only, no explanations or comments.",
        "product_context_prompt": "For each product, explain the artist connection: how it relates to their sound, why they chose it, and how it contributes to their signature tone. Include detailed product analysis, value propositions, and current pricing context. Make every recommendation actionable with clear CTAs."
    },
    "new_release": {
        "base_prompt": """You are an expert blog post writer specializing in new product releases for musical instruments.

Write a detailed 2500-3000 word new release analysis. Use a formal, professional tone written in 1st person plural ("We", "Our team"). This should be THE comprehensive new release resource.

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Conduct original research or provide unique analysis to enhance originality
5. Add deeper insights or lesser-known facts about the main topics
6. Enhance depth and quality suitable for print or reference
7. Include engaging and unique content that's shareable and recommendable
8. Differentiate content with unique perspectives or exclusive information
9. Provide personal experiences or case studies to showcase expertise
10. Expand on practical steps and detailed guidance to ensure readers can achieve their goals

AFFILIATE INTEGRATION REQUIREMENTS:
- Include specific product recommendations and comparisons
- Add affiliate CTAs for new releases and alternatives
- Provide detailed product analysis and value propositions
- Include pricing context and current deals
- Make every recommendation actionable and conversion-focused

Your output must be in JSON format. Use these elements: sub_header, bold_paragraph_text, paragraph_text, article_tip, quick_guide, simple_table.

RESPOND ONLY WITH VALID JSON FORMAT.""",
        "system_prompt": "You are an expert music gear writer with over 20 years of experience. Always respond with valid JSON only, no explanations or comments.",
        "product_context_prompt": "For each product, explain the new features, improvements over previous models, and competitive advantages. Include detailed product analysis, value propositions, and current pricing context. Make every recommendation actionable with clear CTAs."
    },
    "quiz": {
        "base_prompt": """You are an expert blog post writer specializing in interactive content for musical instruments.

Write a detailed 2500-3000 word interactive guide. Use a formal, professional tone written in 1st person plural ("We", "Our team"). This should be THE comprehensive interactive resource.

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Conduct original research or provide unique analysis to enhance originality
5. Add deeper insights or lesser-known facts about the main topics
6. Enhance depth and quality suitable for print or reference
7. Include engaging and unique content that's shareable and recommendable
8. Differentiate content with unique perspectives or exclusive information
9. Provide personal experiences or case studies to showcase expertise
10. Expand on practical steps and detailed guidance to ensure readers can achieve their goals

AFFILIATE INTEGRATION REQUIREMENTS:
- Include specific product recommendations for each quiz result
- Add affiliate CTAs for recommended products
- Provide detailed product analysis and value propositions
- Include pricing context and current deals
- Make every recommendation actionable and conversion-focused

Your output must be in JSON format. Use these elements: sub_header, bold_paragraph_text, paragraph_text, article_tip, quick_guide, simple_table.

RESPOND ONLY WITH VALID JSON FORMAT.""",
        "system_prompt": "You are an expert music gear writer with over 20 years of experience. Always respond with valid JSON only, no explanations or comments.",
        "product_context_prompt": "For each quiz result, include specific product recommendations that match the user's profile. Include detailed product analysis, value propositions, and current pricing context. Make every recommendation actionable with clear CTAs."
    }
}

async def update_all_templates():
    """Update all templates to comprehensive format"""
    print("🚀 Starting comprehensive template updates...")
    print("=" * 60)
    
    async with async_session_factory() as session:
        # Get all active templates
        result = await session.execute(text("""
            SELECT id, name, template_type, base_prompt, system_prompt, product_context_prompt
            FROM blog_generation_templates 
            WHERE is_active = true
            ORDER BY template_type, name
        """))
        templates = result.fetchall()
        
        updated_count = 0
        
        for template in templates:
            template_id, name, template_type, current_prompt, current_system, current_product = template
            
            # Get the comprehensive update for this template type
            if template_type in TEMPLATE_UPDATES:
                update = TEMPLATE_UPDATES[template_type]
                
                # Check if template needs updating
                needs_update = False
                
                # Check prompt length (should be at least 1000 chars)
                if len(current_prompt or '') < 1000:
                    needs_update = True
                    print(f"📝 Updating {name} - prompt too short ({len(current_prompt or '')} chars)")
                
                # Check for JSON enforcement
                if not current_prompt or 'RESPOND ONLY WITH VALID JSON FORMAT' not in current_prompt:
                    needs_update = True
                    print(f"📝 Updating {name} - missing JSON enforcement")
                
                # Check for affiliate integration
                if not current_prompt or 'AFFILIATE INTEGRATION' not in current_prompt:
                    needs_update = True
                    print(f"📝 Updating {name} - missing affiliate integration")
                
                if needs_update:
                    # Update the template
                    await session.execute(text("""
                        UPDATE blog_generation_templates 
                        SET base_prompt = :base_prompt,
                            system_prompt = :system_prompt,
                            product_context_prompt = :product_context_prompt,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = :template_id
                    """), {
                        'template_id': template_id,
                        'base_prompt': update['base_prompt'],
                        'system_prompt': update['system_prompt'],
                        'product_context_prompt': update['product_context_prompt']
                    })
                    
                    updated_count += 1
                    print(f"✅ Updated: {name}")
                else:
                    print(f"✅ Already up to date: {name}")
            else:
                print(f"⚠️  No update template found for type: {template_type}")
        
        await session.commit()
        
        print(f"\n🎉 Successfully updated {updated_count} templates!")
        print(f"📊 Total templates processed: {len(templates)}")
        print(f"✨ Template update completed!")

if __name__ == "__main__":
    asyncio.run(update_all_templates())

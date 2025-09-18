#!/usr/bin/env python3
"""
Create Rich Blog Templates - Complete overhaul with proper affiliate integration
This script creates truly rich, affiliate-focused blog templates with advanced JSON structures
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

class RichBlogTemplateCreator:
    def __init__(self):
        self.templates = []
    
    def create_templates(self):
        """Create rich, affiliate-focused blog templates"""
        
        # 1. ULTIMATE BUYING GUIDE WITH DEEP AFFILIATE INTEGRATION
        self.templates.append({
            'name': 'Ultimate Buying Guide: Deep Affiliate Integration',
            'description': 'Comprehensive 3000+ word buying guides with strategic affiliate placement throughout content',
            'template_type': 'buying_guide',
            'base_prompt': '''You are a world-class music gear expert and affiliate marketing specialist. Create a comprehensive 3000+ word buying guide that seamlessly integrates product recommendations with natural, conversion-focused content.

CONTENT REQUIREMENTS:
- Write in first person plural ("We", "Our team") with authoritative expertise
- Target 3000+ words with deep, actionable insights
- Include specific product recommendations with detailed reasoning
- Integrate affiliate CTAs naturally throughout the content
- Provide unique insights not found elsewhere
- Include real-world testing and comparison data

AFFILIATE INTEGRATION STRATEGY:
- Place product showcases at strategic content points
- Include detailed product analysis with pros/cons
- Add pricing context and value propositions
- Create urgency with limited-time offers
- Include multiple product options for different budgets
- Use social proof and expert recommendations

JSON STRUCTURE REQUIREMENTS:
Your response must be valid JSON with this exact structure:
{
  "title": "Main title of the guide",
  "excerpt": "Compelling 150-word excerpt",
  "introduction": {
    "hook": "Attention-grabbing opening",
    "problem_statement": "What problem this solves",
    "solution_preview": "What readers will learn"
  },
  "quick_picks": {
    "title": "Quick Picks Section Title",
    "products": [
      {
        "product_id": "1234",
        "name": "Product Name",
        "price": "$299",
        "why_we_love_it": "Brief compelling reason",
        "best_for": "Ideal use case",
        "affiliate_cta": "Strong call-to-action"
      }
    ]
  },
  "buying_criteria": {
    "title": "What to Look For",
    "criteria": [
      {
        "criterion": "Build Quality",
        "description": "Detailed explanation",
        "why_matters": "Why this is important",
        "red_flags": "What to avoid"
      }
    ]
  },
  "detailed_reviews": [
    {
      "product_id": "1234",
      "name": "Product Name",
      "rating": 9.2,
      "price": "$299",
      "overview": "Brief overview",
      "key_features": ["Feature 1", "Feature 2"],
      "performance_analysis": "Detailed performance review",
      "pros": ["Pro 1", "Pro 2"],
      "cons": ["Con 1", "Con 2"],
      "ideal_for": "Who should buy this",
      "affiliate_cta": "Compelling call-to-action",
      "current_deals": "Any current offers or discounts"
    }
  ],
  "comparison_table": {
    "title": "Head-to-Head Comparison",
    "headers": ["Feature", "Product A", "Product B", "Product C"],
    "rows": [
      ["Price", "$299", "$399", "$199"],
      ["Rating", "9.2/10", "8.8/10", "8.5/10"]
    ]
  },
  "budget_breakdown": {
    "title": "Budget Breakdown",
    "tiers": [
      {
        "tier": "Budget ($100-300)",
        "recommendation": "Product recommendation",
        "reasoning": "Why this is the best value",
        "product_id": "1234"
      }
    ]
  },
  "common_mistakes": {
    "title": "Common Buying Mistakes",
    "mistakes": [
      {
        "mistake": "Mistake description",
        "why_happens": "Why people make this mistake",
        "how_to_avoid": "How to avoid it",
        "better_alternative": "Better approach"
      }
    ]
  },
  "setup_guide": {
    "title": "Setup and Getting Started",
    "steps": [
      {
        "step": 1,
        "title": "Step title",
        "description": "Detailed instructions",
        "required_products": ["Product ID if needed"],
        "tips": "Pro tips for this step"
      }
    ]
  },
  "expert_verdict": {
    "title": "Our Expert Verdict",
    "winner": "Product Name",
    "reasoning": "Why this is the winner",
    "product_id": "1234",
    "final_cta": "Strong final call-to-action"
  },
  "faqs": [
    {
      "question": "FAQ question",
      "answer": "Detailed answer with product recommendations where relevant"
    }
  ],
  "conclusion": {
    "summary": "Brief summary of key points",
    "final_recommendation": "Final product recommendation",
    "next_steps": "What readers should do next",
    "affiliate_cta": "Final compelling call-to-action"
  }
}

CRITICAL: Respond ONLY with valid JSON. No explanations or additional text.''',
            'system_prompt': 'You are a world-class music gear expert and affiliate marketing specialist. Create comprehensive, conversion-focused buying guides with strategic product placement. Always respond with valid JSON only.',
            'product_context_prompt': 'For each product, provide: detailed analysis, real-world performance, build quality, ideal use cases, skill level fit, value proposition, honest pros/cons, current pricing, and compelling affiliate CTAs. Make every product mention actionable and conversion-focused.',
            'content_structure': {
                'format': 'structured_json',
                'sections': [
                    {'type': 'introduction', 'required': True},
                    {'type': 'quick_picks', 'required': True},
                    {'type': 'buying_criteria', 'required': True},
                    {'type': 'detailed_reviews', 'required': True},
                    {'type': 'comparison_table', 'required': True},
                    {'type': 'budget_breakdown', 'required': True},
                    {'type': 'common_mistakes', 'required': True},
                    {'type': 'setup_guide', 'required': True},
                    {'type': 'expert_verdict', 'required': True},
                    {'type': 'faqs', 'required': True},
                    {'type': 'conclusion', 'required': True}
                ],
                'expected_length': '3000+ words',
                'affiliate_integration': 'comprehensive',
                'product_showcases': 'strategic_placement'
            },
            'seo_title_template': 'Ultimate {category} Buying Guide: Expert Picks & Reviews',
            'seo_description_template': 'Complete {category} buying guide with expert reviews, comparisons, and recommendations. Find the perfect {category} for your needs and budget.'
        })
        
        # 2. HEAD-TO-HEAD BATTLE WITH AFFILIATE CTAs
        self.templates.append({
            'name': 'Epic Product Battle: Affiliate-Focused Showdown',
            'description': 'High-converting head-to-head comparisons with strategic affiliate placement and clear winners',
            'template_type': 'comparison',
            'base_prompt': '''You are a battle-tested music gear expert creating epic head-to-head product showdowns. Write a compelling 3000+ word comparison that drives purchase decisions through strategic affiliate integration.

CONTENT REQUIREMENTS:
- Create an engaging "battle" narrative with clear winners
- Include detailed performance comparisons
- Integrate affiliate CTAs at strategic moments
- Provide specific use-case recommendations
- Include real-world testing data
- Create urgency with limited-time offers

BATTLE STRUCTURE:
- Fight card introduction
- Quick verdict for busy readers
- Round-by-round analysis
- Detailed comparison tables
- Use-case specific recommendations
- Clear winner declaration
- Strong affiliate CTAs

JSON STRUCTURE REQUIREMENTS:
Your response must be valid JSON with this exact structure:
{
  "title": "Epic Battle Title",
  "excerpt": "Compelling 150-word excerpt",
  "fight_card": {
    "title": "The Fight Card",
    "products": [
      {
        "product_id": "1234",
        "name": "Product A",
        "nickname": "The Champion",
        "price": "$299",
        "key_strength": "Main strength",
        "weakness": "Main weakness"
      }
    ]
  },
  "quick_verdict": {
    "title": "Quick Verdict",
    "winner": "Product Name",
    "reasoning": "Brief why it wins",
    "product_id": "1234",
    "cta": "Strong call-to-action"
  },
  "round_by_round": [
    {
      "round": 1,
      "title": "Round 1: Build Quality",
      "winner": "Product A",
      "analysis": "Detailed analysis",
      "score": "10-9",
      "affiliate_cta": "CTA for winning product"
    }
  ],
  "comparison_table": {
    "title": "Head-to-Head Comparison",
    "headers": ["Feature", "Product A", "Product B"],
    "rows": [
      ["Price", "$299", "$399"],
      ["Rating", "9.2/10", "8.8/10"]
    ]
  },
  "use_cases": [
    {
      "scenario": "Scenario description",
      "winner": "Product Name",
      "reasoning": "Why this product wins",
      "product_id": "1234",
      "affiliate_cta": "Compelling CTA"
    }
  ],
  "value_analysis": {
    "title": "Value Analysis",
    "best_value": "Product Name",
    "reasoning": "Why it offers best value",
    "product_id": "1234",
    "price_justification": "Why the price is justified"
  },
  "alternatives": [
    {
      "product_id": "1234",
      "name": "Alternative Product",
      "when_to_choose": "When to choose this instead",
      "affiliate_cta": "CTA for alternative"
    }
  ],
  "final_verdict": {
    "title": "Final Verdict",
    "winner": "Product Name",
    "reasoning": "Comprehensive reasoning",
    "product_id": "1234",
    "final_cta": "Strong final call-to-action",
    "limited_time_offer": "Any current deals"
  }
}

CRITICAL: Respond ONLY with valid JSON. No explanations or additional text.''',
            'system_prompt': 'You are a battle-tested music gear expert creating epic product showdowns. Write compelling comparisons that drive purchase decisions. Always respond with valid JSON only.',
            'product_context_prompt': 'For each product in the battle, provide: detailed performance analysis, build quality assessment, real-world testing results, pros/cons, value proposition, and compelling affiliate CTAs. Make every comparison actionable.',
            'content_structure': {
                'format': 'structured_json',
                'sections': [
                    {'type': 'fight_card', 'required': True},
                    {'type': 'quick_verdict', 'required': True},
                    {'type': 'round_by_round', 'required': True},
                    {'type': 'comparison_table', 'required': True},
                    {'type': 'use_cases', 'required': True},
                    {'type': 'value_analysis', 'required': True},
                    {'type': 'alternatives', 'required': True},
                    {'type': 'final_verdict', 'required': True}
                ],
                'expected_length': '3000+ words',
                'affiliate_integration': 'battle_focused',
                'product_showcases': 'strategic_placement'
            },
            'seo_title_template': '{product_a} vs {product_b}: Epic Battle & Winner Revealed',
            'seo_description_template': 'Epic head-to-head battle between {product_a} and {product_b}. See which one wins in our comprehensive comparison with real-world testing.'
        })
        
        # 3. PROFESSIONAL DEEP DIVE REVIEW WITH AFFILIATE INTEGRATION
        self.templates.append({
            'name': 'Professional Deep Dive: Affiliate-Integrated Review',
            'description': 'Comprehensive single-product reviews with technical depth and strategic affiliate placement',
            'template_type': 'review',
            'base_prompt': '''You are a world-renowned music gear expert conducting a comprehensive product review. Create a detailed 3000+ word review that combines technical analysis with strategic affiliate integration.

CONTENT REQUIREMENTS:
- Provide in-depth technical analysis
- Include real-world testing and performance data
- Integrate affiliate CTAs naturally throughout
- Compare against competitors
- Include detailed pros/cons analysis
- Provide clear buyer guidance

REVIEW STRUCTURE:
- First impressions and unboxing
- Detailed build analysis
- Performance testing results
- Competitive comparison
- Ownership experience
- Clear recommendation with affiliate CTA

JSON STRUCTURE REQUIREMENTS:
Your response must be valid JSON with this exact structure:
{
  "title": "Professional Review Title",
  "excerpt": "Compelling 150-word excerpt",
  "first_impressions": {
    "title": "First Impressions",
    "unboxing": "Unboxing experience",
    "initial_thoughts": "Initial thoughts",
    "build_quality_first_look": "First look at build quality",
    "affiliate_cta": "Early CTA for interested readers"
  },
  "build_analysis": {
    "title": "Build Quality Analysis",
    "materials": "Materials used and quality",
    "construction": "Construction details",
    "durability": "Durability assessment",
    "attention_to_detail": "Attention to detail",
    "value_assessment": "Value for money assessment"
  },
  "performance_testing": {
    "title": "Performance Testing",
    "test_conditions": "Testing conditions",
    "results": "Detailed test results",
    "strengths": "Performance strengths",
    "weaknesses": "Performance weaknesses",
    "comparison_to_specs": "How it compares to manufacturer specs"
  },
  "competitive_comparison": {
    "title": "Competitive Comparison",
    "competitors": [
      {
        "product_id": "1234",
        "name": "Competitor Product",
        "price": "$299",
        "how_it_compares": "How it compares",
        "when_to_choose_competitor": "When to choose competitor",
        "affiliate_cta": "CTA for competitor if relevant"
      }
    ]
  },
  "ownership_experience": {
    "title": "Long-term Ownership Experience",
    "durability_over_time": "How it holds up over time",
    "maintenance": "Maintenance requirements",
    "customer_support": "Customer support experience",
    "resale_value": "Resale value assessment"
  },
  "pros_cons": {
    "title": "Pros and Cons",
    "pros": ["Pro 1", "Pro 2", "Pro 3"],
    "cons": ["Con 1", "Con 2", "Con 3"],
    "overall_assessment": "Overall assessment"
  },
  "buyer_guidance": {
    "title": "Who Should Buy This",
    "ideal_buyer": "Ideal buyer profile",
    "skill_level": "Required skill level",
    "use_cases": "Best use cases",
    "alternatives": "Alternative recommendations",
    "affiliate_cta": "Strong call-to-action"
  },
  "final_verdict": {
    "title": "Final Verdict",
    "rating": 9.2,
    "summary": "Brief summary",
    "recommendation": "Final recommendation",
    "product_id": "1234",
    "final_cta": "Compelling final CTA",
    "current_deals": "Any current deals or offers"
  }
}

CRITICAL: Respond ONLY with valid JSON. No explanations or additional text.''',
            'system_prompt': 'You are a world-renowned music gear expert conducting comprehensive product reviews. Provide detailed technical analysis with strategic affiliate integration. Always respond with valid JSON only.',
            'product_context_prompt': 'Provide comprehensive analysis including: detailed build quality assessment, real-world performance testing, competitive comparison, long-term ownership experience, honest pros/cons, and compelling affiliate CTAs.',
            'content_structure': {
                'format': 'structured_json',
                'sections': [
                    {'type': 'first_impressions', 'required': True},
                    {'type': 'build_analysis', 'required': True},
                    {'type': 'performance_testing', 'required': True},
                    {'type': 'competitive_comparison', 'required': True},
                    {'type': 'ownership_experience', 'required': True},
                    {'type': 'pros_cons', 'required': True},
                    {'type': 'buyer_guidance', 'required': True},
                    {'type': 'final_verdict', 'required': True}
                ],
                'expected_length': '3000+ words',
                'affiliate_integration': 'review_focused',
                'product_showcases': 'strategic_placement'
            },
            'seo_title_template': '{product_name} Review: Professional Analysis & Verdict',
            'seo_description_template': 'Comprehensive {product_name} review with professional testing, build analysis, and expert verdict. See if it\'s worth the investment.'
        })
        
        # 4. BUDGET HERO FINDER WITH VALUE-FOCUSED AFFILIATES
        self.templates.append({
            'name': 'Budget Hero Finder: Value-Focused Affiliate Integration',
            'description': 'Value-focused roundups that convert budget-conscious buyers with strategic affiliate placement',
            'template_type': 'general',
            'base_prompt': '''You are a budget-conscious music gear expert who finds incredible value in affordable products. Create a compelling 3000+ word guide that helps readers find the best bang-for-buck options with strategic affiliate integration.

CONTENT REQUIREMENTS:
- Focus on value and performance per dollar
- Include detailed price-performance analysis
- Integrate affiliate CTAs for budget-conscious buyers
- Provide smart compromise recommendations
- Include upgrade path guidance
- Create urgency with limited-time deals

VALUE STRUCTURE:
- Value introduction and philosophy
- Budget hero recommendations
- Price-performance analysis
- Smart compromises
- Upgrade paths
- Value accessories
- Deal alerts

JSON STRUCTURE REQUIREMENTS:
Your response must be valid JSON with this exact structure:
{
  "title": "Budget Hero Guide Title",
  "excerpt": "Compelling 150-word excerpt",
  "value_intro": {
    "title": "Our Value Philosophy",
    "philosophy": "Our approach to finding value",
    "what_makes_hero": "What makes a product a budget hero",
    "red_flags": "What to avoid in budget products"
  },
  "budget_heroes": [
    {
      "product_id": "1234",
      "name": "Product Name",
      "price": "$199",
      "value_score": 9.5,
      "why_hero": "Why this is a budget hero",
      "performance": "Performance analysis",
      "best_for": "Ideal use case",
      "affiliate_cta": "Compelling CTA",
      "current_deal": "Any current deals"
    }
  ],
  "price_performance": {
    "title": "Price-Performance Analysis",
    "analysis": "Detailed price-performance analysis",
    "sweet_spots": "Price sweet spots to target",
    "diminishing_returns": "Where you hit diminishing returns"
  },
  "smart_compromises": {
    "title": "Smart Compromises",
    "compromises": [
      {
        "compromise": "What to compromise on",
        "why_okay": "Why this compromise is acceptable",
        "what_not_to_compromise": "What not to compromise on",
        "product_recommendations": ["Product IDs that make smart compromises"]
      }
    ]
  },
  "upgrade_paths": {
    "title": "Upgrade Paths",
    "paths": [
      {
        "starting_point": "Starting product",
        "upgrade_options": [
          {
            "product_id": "1234",
            "name": "Upgrade Option",
            "price": "$299",
            "improvement": "What you get for the extra money",
            "affiliate_cta": "CTA for upgrade"
          }
        ]
      }
    ]
  },
  "value_accessories": {
    "title": "Value Accessories",
    "accessories": [
      {
        "product_id": "1234",
        "name": "Accessory Name",
        "price": "$49",
        "value_add": "What value this adds",
        "affiliate_cta": "CTA for accessory"
      }
    ]
  },
  "deal_alerts": {
    "title": "Current Deal Alerts",
    "deals": [
      {
        "product_id": "1234",
        "name": "Product Name",
        "original_price": "$299",
        "sale_price": "$199",
        "savings": "$100",
        "expires": "Deal expiration",
        "affiliate_cta": "Urgent CTA"
      }
    ]
  },
  "final_recommendations": {
    "title": "Final Recommendations",
    "best_overall_value": "Product Name",
    "reasoning": "Why this offers best value",
    "product_id": "1234",
    "final_cta": "Strong final CTA"
  }
}

CRITICAL: Respond ONLY with valid JSON. No explanations or additional text.''',
            'system_prompt': 'You are a budget-conscious music gear expert who finds incredible value in affordable products. Create compelling value-focused guides with strategic affiliate integration. Always respond with valid JSON only.',
            'product_context_prompt': 'For each budget hero, provide: detailed value analysis, price-performance assessment, real-world testing, honest limitations, upgrade recommendations, and compelling affiliate CTAs for value-conscious buyers.',
            'content_structure': {
                'format': 'structured_json',
                'sections': [
                    {'type': 'value_intro', 'required': True},
                    {'type': 'budget_heroes', 'required': True},
                    {'type': 'price_performance', 'required': True},
                    {'type': 'smart_compromises', 'required': True},
                    {'type': 'upgrade_paths', 'required': True},
                    {'type': 'value_accessories', 'required': True},
                    {'type': 'deal_alerts', 'required': True},
                    {'type': 'final_recommendations', 'required': True}
                ],
                'expected_length': '3000+ words',
                'affiliate_integration': 'value_focused',
                'product_showcases': 'strategic_placement'
            },
            'seo_title_template': 'Best Budget {category}: Value Heroes Under ${budget}',
            'seo_description_template': 'Discover the best budget {category} options that deliver incredible value. Our expert picks under ${budget} with detailed analysis and current deals.'
        })
        
        # 5. ARTIST SPOTLIGHT WITH GEAR BREAKDOWN
        self.templates.append({
            'name': 'Artist Spotlight: Signature Sound Breakdown',
            'description': 'In-depth artist profiles with signature gear analysis and affordable alternatives',
            'template_type': 'artist_spotlight',
            'base_prompt': '''You are a music historian and gear expert who specializes in analyzing iconic artists' signature sounds. Create a comprehensive 3000+ word artist spotlight that breaks down their gear and provides affordable alternatives.

CONTENT REQUIREMENTS:
- Provide detailed artist background and influence
- Analyze signature gear and tone
- Include affordable alternatives for each piece
- Integrate affiliate CTAs for gear recommendations
- Include setup guides and tone tips
- Provide historical context and modern applications

SPOTLIGHT STRUCTURE:
- Artist introduction and influence
- Signature gear breakdown
- Tone analysis and techniques
- Affordable alternatives
- Setup guides
- Modern applications

JSON STRUCTURE REQUIREMENTS:
Your response must be valid JSON with this exact structure:
{
  "title": "Artist Spotlight Title",
  "excerpt": "Compelling 150-word excerpt",
  "artist_intro": {
    "title": "Artist Introduction",
    "background": "Artist background and influence",
    "signature_sound": "What makes their sound unique",
    "impact": "Their impact on music"
  },
  "signature_gear": {
    "title": "Signature Gear Breakdown",
    "gear": [
      {
        "category": "Guitar",
        "original_gear": "Original gear used",
        "product_id": "1234",
        "affordable_alternative": "Affordable alternative",
        "price": "$299",
        "tone_contribution": "How it contributes to their sound",
        "affiliate_cta": "CTA for alternative"
      }
    ]
  },
  "tone_analysis": {
    "title": "Tone Analysis",
    "signature_elements": "Key elements of their tone",
    "techniques": "Signature techniques",
    "setup_tips": "Setup tips to achieve their sound"
  },
  "affordable_alternatives": {
    "title": "Affordable Alternatives",
    "alternatives": [
      {
        "product_id": "1234",
        "name": "Alternative Product",
        "price": "$199",
        "how_it_compares": "How it compares to original",
        "tone_similarity": "Tone similarity percentage",
        "affiliate_cta": "Compelling CTA"
      }
    ]
  },
  "setup_guide": {
    "title": "Getting Their Sound",
    "steps": [
      {
        "step": 1,
        "title": "Step title",
        "description": "Detailed instructions",
        "required_gear": ["Product IDs"],
        "tips": "Pro tips"
      }
    ]
  },
  "modern_applications": {
    "title": "Modern Applications",
    "contemporary_artists": "Artists who use similar approaches",
    "modern_gear": "Modern gear that achieves similar results",
    "affiliate_cta": "CTA for modern gear"
  },
  "final_thoughts": {
    "title": "Final Thoughts",
    "legacy": "Artist's legacy",
    "influence": "Their influence on modern music",
    "recommendation": "Final gear recommendation",
    "product_id": "1234",
    "final_cta": "Strong final CTA"
  }
}

CRITICAL: Respond ONLY with valid JSON. No explanations or additional text.''',
            'system_prompt': 'You are a music historian and gear expert specializing in iconic artists\' signature sounds. Create comprehensive artist spotlights with gear analysis and affordable alternatives. Always respond with valid JSON only.',
            'product_context_prompt': 'For each piece of gear, provide: detailed analysis of its role in the artist\'s sound, affordable alternatives with tone comparisons, setup tips, and compelling affiliate CTAs for gear recommendations.',
            'content_structure': {
                'format': 'structured_json',
                'sections': [
                    {'type': 'artist_intro', 'required': True},
                    {'type': 'signature_gear', 'required': True},
                    {'type': 'tone_analysis', 'required': True},
                    {'type': 'affordable_alternatives', 'required': True},
                    {'type': 'setup_guide', 'required': True},
                    {'type': 'modern_applications', 'required': True},
                    {'type': 'final_thoughts', 'required': True}
                ],
                'expected_length': '3000+ words',
                'affiliate_integration': 'gear_focused',
                'product_showcases': 'strategic_placement'
            },
            'seo_title_template': '{artist_name} Gear: Signature Sound Breakdown & Affordable Alternatives',
            'seo_description_template': 'Discover {artist_name}\'s signature gear and learn how to achieve their iconic sound with affordable alternatives. Complete gear breakdown and setup guide.'
        })
    
    async def insert_templates(self):
        """Insert the new templates into the database"""
        async with async_session_factory() as session:
            # First, deactivate all existing templates
            await session.execute(text('UPDATE blog_generation_templates SET is_active = false'))
            print("Deactivated all existing templates")
            
            # Insert new templates
            for template in self.templates:
                await session.execute(text('''
                    INSERT INTO blog_generation_templates (
                        name, description, template_type, base_prompt, system_prompt,
                        product_context_prompt, content_structure, seo_title_template,
                        seo_description_template, is_active, created_at, updated_at
                    ) VALUES (
                        :name, :description, :template_type, :base_prompt, :system_prompt,
                        :product_context_prompt, :content_structure, :seo_title_template,
                        :seo_description_template, :is_active, :created_at, :updated_at
                    )
                '''), {
                    'name': template['name'],
                    'description': template['description'],
                    'template_type': template['template_type'],
                    'base_prompt': template['base_prompt'],
                    'system_prompt': template['system_prompt'],
                    'product_context_prompt': template['product_context_prompt'],
                    'content_structure': json.dumps(template['content_structure']),
                    'seo_title_template': template['seo_title_template'],
                    'seo_description_template': template['seo_description_template'],
                    'is_active': True,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                })
                print(f"Inserted template: {template['name']}")
            
            await session.commit()
            print(f"✅ Successfully inserted {len(self.templates)} new rich templates")

async def main():
    """Main function to create rich blog templates"""
    print("🚀 Creating Rich Blog Templates with Deep Affiliate Integration")
    print("=" * 60)
    
    creator = RichBlogTemplateCreator()
    creator.create_templates()
    await creator.insert_templates()
    
    print("\n🎉 Rich blog templates created successfully!")
    print("These templates feature:")
    print("- 3000+ word comprehensive content")
    print("- Strategic affiliate integration throughout")
    print("- Advanced JSON structures for rich rendering")
    print("- Conversion-focused CTAs and product showcases")
    print("- Professional, expert-level content quality")

if __name__ == "__main__":
    asyncio.run(main())

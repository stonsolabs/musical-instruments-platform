#!/usr/bin/env python3
"""
Create Simple, Effective Blog Templates - Guitar World/Drum Helper Style
Replaces the overly complex templates with proven, engaging formats
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database import async_session_factory
from sqlalchemy import text

class SimpleBlogTemplateCreator:
    def __init__(self):
        self.templates = []
    
    def create_templates(self):
        """Create simple, effective blog templates based on successful music blogs"""
        
        # 1. PRACTICAL BUYING GUIDE (Guitar World Style)
        self.templates.append({
            'name': 'Practical Buying Guide',
            'description': 'Conversational buying guides focusing on real musician needs (1200-1800 words)',
            'template_type': 'buying_guide',
            'base_prompt': '''Write an engaging buying guide that helps musicians make smart decisions. Use a conversational, passionate tone like Guitar World.

STYLE:
- Write like you're talking to a fellow musician
- Share personal insights and real-world experience
- Include practical scenarios: bedroom practice, live gigs, studio recording
- Focus on what actually matters to musicians, not just specs

STRUCTURE:
- Engaging introduction that connects to musician pain points
- Clear product recommendations with WHY they matter
- Practical advice musicians can actually use
- Real-world scenarios where products shine
- Honest pros/cons without being overly negative

Make it genuinely helpful and engaging - not a dry product list.''',
            
            'system_prompt': 'You are a passionate musician and gear expert writing for fellow musicians. Create engaging, practical content that helps people make better music gear decisions.',
            
            'product_context_prompt': 'For each product, explain: why it fits the musician\'s needs, what scenarios it\'s perfect for, honest strengths and limitations, and who should buy it. Make recommendations feel natural and helpful.',
            
            'content_structure': {
                'format': 'simple_json',
                'target_length': '1200-1800 words',
                'style': 'conversational',
                'focus': 'practical_value'
            },
            'min_products': 3,
            'max_products': 6,
            'seo_title_template': 'Best {category} for {audience}: What Actually Matters',
            'seo_description_template': 'Practical {category} buying guide focusing on real musician needs. Find the right gear for your style and budget.'
        })
        
        # 2. HEAD-TO-HEAD COMPARISON (Drum Helper Style)
        self.templates.append({
            'name': 'Head-to-Head Comparison',
            'description': 'Direct product comparisons with clear winners and practical advice (1000-1500 words)',
            'template_type': 'comparison',
            'base_prompt': '''Create a direct, honest comparison between products. Make it easy for musicians to understand which one fits their needs.

STYLE:
- Clear, direct comparisons
- Highlight key differences that matter
- Include specific use cases for each product
- Provide clear guidance on which to choose when

STRUCTURE:
- Quick summary for busy readers
- Key differences breakdown
- Use case scenarios
- Clear recommendation for different needs

Focus on helping musicians make confident decisions.''',
            
            'system_prompt': 'You are a gear expert helping musicians choose between specific products. Provide clear, honest comparisons that lead to confident purchase decisions.',
            
            'product_context_prompt': 'Compare products directly on factors that matter to musicians: sound quality, build, value, and practical use cases. Be honest about trade-offs.',
            
            'content_structure': {
                'format': 'simple_json',
                'target_length': '1000-1500 words',
                'style': 'direct_comparison',
                'focus': 'decision_making'
            },
            'min_products': 2,
            'max_products': 4,
            'seo_title_template': '{product_a} vs {product_b}: Which Should You Choose?',
            'seo_description_template': 'Direct comparison between {product_a} and {product_b}. See which one fits your needs and budget.'
        })
        
        # 3. SINGLE PRODUCT REVIEW (Personal, Honest)
        self.templates.append({
            'name': 'Honest Product Review',
            'description': 'Personal, honest reviews focusing on real-world performance (1200-1600 words)',
            'template_type': 'review',
            'base_prompt': '''Write an honest, personal review of this product. Share real insights that help musicians understand if it's right for them.

STYLE:
- Personal experience and insights
- Honest about both strengths and weaknesses
- Include real-world testing scenarios
- Focus on practical performance over specs

STRUCTURE:
- First impressions and setup
- Real-world performance testing
- Honest pros and cons
- Who should (and shouldn't) buy it

Make it feel like getting advice from a trusted musician friend.''',
            
            'system_prompt': 'You are an experienced musician sharing honest insights about gear. Help fellow musicians make informed decisions based on real-world performance.',
            
            'product_context_prompt': 'Share honest, detailed insights about the product\'s real-world performance, build quality, value proposition, and who it\'s best suited for.',
            
            'content_structure': {
                'format': 'simple_json',
                'target_length': '1200-1600 words',
                'style': 'personal_honest',
                'focus': 'real_world_performance'
            },
            'min_products': 1,
            'max_products': 3,
            'seo_title_template': '{product_name} Review: Honest Insights from Real Use',
            'seo_description_template': 'Honest {product_name} review with real-world testing. See if it\'s worth your investment.'
        })
        
        # 4. VALUE GUIDE (Budget-Focused)
        self.templates.append({
            'name': 'Smart Value Guide',
            'description': 'Budget-conscious guides focusing on best bang for buck (1000-1400 words)',
            'template_type': 'general',
            'base_prompt': '''Help musicians find the best value in their budget range. Focus on smart compromises and genuine value.

STYLE:
- Value-focused without being cheap
- Explain what you get for your money
- Include smart compromise advice
- Show upgrade paths when relevant

STRUCTURE:
- Value philosophy and approach
- Best bang-for-buck recommendations
- Smart compromises to consider
- When to spend more vs. save money

Help musicians make the most of their budget.''',
            
            'system_prompt': 'You are a budget-conscious musician who knows how to find genuine value. Help others get the most music gear for their money.',
            
            'product_context_prompt': 'Focus on value proposition, price-performance ratio, smart compromises, and long-term satisfaction for budget-conscious musicians.',
            
            'content_structure': {
                'format': 'simple_json',
                'target_length': '1000-1400 words',
                'style': 'value_focused',
                'focus': 'budget_optimization'
            },
            'min_products': 3,
            'max_products': 5,
            'seo_title_template': 'Best Budget {category}: Smart Value for Your Money',
            'seo_description_template': 'Budget-focused {category} guide with genuine value picks. Get the most music gear for your money.'
        })
    
    async def insert_templates(self):
        """Insert the simple templates into the database"""
        async with async_session_factory() as session:
            # First, deactivate all existing templates
            await session.execute(text('UPDATE blog_generation_templates SET is_active = false'))
            print("✅ Deactivated all existing complex templates")
            
            # Insert new simple templates
            for template in self.templates:
                await session.execute(text('''
                    INSERT INTO blog_generation_templates (
                        name, description, template_type, base_prompt, system_prompt,
                        product_context_prompt, min_products, max_products,
                        seo_title_template, seo_description_template, content_structure,
                        is_active, created_at, updated_at
                    ) VALUES (
                        :name, :description, :template_type, :base_prompt, :system_prompt,
                        :product_context_prompt, :min_products, :max_products,
                        :seo_title_template, :seo_description_template, :content_structure,
                        :is_active, :created_at, :updated_at
                    )
                '''), {
                    'name': template['name'],
                    'description': template['description'],
                    'template_type': template['template_type'],
                    'base_prompt': template['base_prompt'],
                    'system_prompt': template['system_prompt'],
                    'product_context_prompt': template['product_context_prompt'],
                    'min_products': template['min_products'],
                    'max_products': template['max_products'],
                    'seo_title_template': template['seo_title_template'],
                    'seo_description_template': template['seo_description_template'],
                    'content_structure': json.dumps(template['content_structure']),
                    'is_active': True,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                })
                print(f"✅ Inserted template: {template['name']}")
            
            await session.commit()
            print(f"\n🎉 Successfully created {len(self.templates)} simple, effective templates")

async def main():
    """Main function to create simple blog templates"""
    print("🚀 Creating Simple, Effective Blog Templates")
    print("Based on Guitar World & Drum Helper success patterns")
    print("=" * 60)
    
    creator = SimpleBlogTemplateCreator()
    creator.create_templates()
    await creator.insert_templates()
    
    print("\n✨ Templates now focus on:")
    print("- Conversational, passionate writing")
    print("- Practical musician scenarios")
    print("- 1200-1800 word target (readable length)")
    print("- Only available products")
    print("- Genuine value for musicians")

if __name__ == "__main__":
    asyncio.run(main())
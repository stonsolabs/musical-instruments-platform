"""
Blog AI Prompt Templates and Generation Logic
This module contains specialized prompts for different types of blog content
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class BlogPromptTemplates:
    """
    Collection of specialized prompt templates for different blog content types
    """
    
    @staticmethod
    def get_base_system_prompt() -> str:
        """Base system prompt for all blog generation"""
        return """You are an expert music gear writer and reviewer with over 20 years of experience in the music industry. 

You have extensive knowledge of:
- Musical instruments across all categories (guitars, keyboards, drums, brass, woodwinds, strings)
- Music gear technology and specifications
- Sound engineering and production
- Music theory and performance
- Brand histories and market positioning
- Price points and value propositions

Your writing style is:
- Informative and authoritative but accessible
- Engaging and conversational without being casual
- Honest and balanced in reviews and recommendations
- Detail-oriented but not overwhelming for beginners
- SEO-conscious while maintaining natural flow

Always provide practical, actionable advice that helps musicians make informed decisions."""

    @staticmethod
    def get_buying_guide_template() -> Dict[str, Any]:
        """Template for buying guide blog posts"""
        return {
            "name": "Comprehensive Buying Guide",
            "template_type": "buying_guide",
            "base_prompt": """You are an expert blog post writer with a deep knowledge of the {category} space, specializing in writing high quality SEO optimized guides.

Write a comprehensive {word_count} word buying guide for {category} instruments using a formal, professional tone written in 1st person plural ("We", "Our team" - but avoid referencing a specific company). This guide should help both beginners and experienced players choose the right instrument for their needs and budget.

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

Structure your guide with these sections:
1. **Introduction** - Why choosing the right {category} matters
2. **Key Considerations** - What to look for when buying
3. **Budget Breakdown** - Price ranges and what you get at each level
4. **Top Recommendations** - Specific product recommendations with detailed explanations
5. **Advanced Features** - Features that matter for intermediate/advanced players
6. **Maintenance and Care** - How to keep your instrument in top condition
7. **Conclusion** - Final buying advice

For each recommended product, explain:
- Why it's recommended for specific skill levels or use cases
- Key features that set it apart
- Sound characteristics and build quality
- Who it's best suited for (beginner, intermediate, professional)
- Value proposition at its price point
- Any notable pros/cons

Incorporate a balance of perplexity and burstiness to make the article sound humanlike. The aim is to educate readers with hyper-specific/detailed content that goes beyond the obvious to resolve specific issues.

Target audience: Musicians of all skill levels looking to purchase {category} instruments
Word count: {word_count} words
SEO focus: Include relevant keywords naturally throughout""",
            
            "product_context_prompt": """For each featured product, provide:
- Detailed explanation of why it's included in this buying guide
- Specific features that make it stand out in its category/price range
- Who this product is best suited for (skill level, musical styles, use cases)
- How it compares to similar alternatives
- Clear pros and cons based on real-world usage
- Value assessment for the price point

Use your expertise to explain technical aspects in an accessible way.""",
            
            "content_structure": {
                "sections": [
                    "introduction",
                    "key_considerations", 
                    "budget_breakdown",
                    "top_recommendations",
                    "advanced_features",
                    "maintenance_care",
                    "conclusion"
                ],
                "min_products": 5,
                "max_products": 10
            },
            
            "seo_template": "Best {category} {year} - Complete Buying Guide & Expert Reviews",
            "meta_description_template": "Expert buying guide for {category} instruments. Compare top brands, features, and prices. Find the perfect instrument for your skill level and budget with our detailed reviews."
        }

    @staticmethod
    def get_product_review_template() -> Dict[str, Any]:
        """Template for detailed product reviews"""
        return {
            "name": "In-Depth Product Review",
            "template_type": "review",
            "base_prompt": """You are an expert blog post writer with a deep knowledge of the {category} space, specializing in writing high quality SEO optimized reviews.

Write a comprehensive {word_count} word review of the {product_name}. Ensure the tone is formal and professional, written in 1st person plural ("We", "Our team" - but avoid referencing a specific company). This should be an authoritative review that helps potential buyers understand exactly what they're getting.

Structure your review following this mandatory sequence:
1. **Opening (3 paragraphs)** - Hook the reader immediately, demonstrate expertise with phrases like "We performed extensive tests..." or "Our team has thoroughly assessed..." Format this in bold. End with mini summary praising positive aspects.
2. **"Short on Time? Here are Our Key Findings"** - Pros vs cons section with detailed explanations
3. **Features Table** - Generate features with accurate statistics/numbers
4. **Quality & Performance Analysis (2 paragraphs)** - Include anecdotal evidence demonstrating product engagement
5. **Article Tip** - Most vital information or warnings for readers
6. **3 Relevant Subheaders** - Each with 2 paragraphs of 5 sentences, include list formatting in last paragraph
7. **Setup/Installation Guide** - Include 3-step quick guide
8. **Pricing** - Comprehensive pricing analysis
9. **Reliability & Support** - Include anecdotal response times (5 sentences per paragraph)
10. **Summary** - Standout features with subtle drawbacks as hidden advantages
11. **Secret Tip** - 2-3 sentences of beyond-obvious advice
12. **FAQ** - Frequently asked questions (5+ sentences per answer)
13. **Comparison Footer** - "Compare {product_name} With Top Alternatives"

Content Requirements:
- Based on extensive hands-on experience with anecdotal evidence
- Honest about both strengths and limitations
- Include specific testing scenarios with detailed results
- Provide accurate statistics and technical specifications
- Comparative analysis with direct competitors
- Educational focus about the brand and product

Incorporate a balance of perplexity and burstiness to make the review sound humanlike.
Target word count: {word_count} words""",
            
            "product_context_prompt": """Focus primarily on the main product being reviewed. Include 1-2 direct competitors for comparison context. For each product mentioned:
- Provide specific technical specifications
- Describe actual sound characteristics you've experienced
- Compare build quality and materials
- Explain real-world performance in different scenarios
- Give honest assessment of value proposition

Your comparisons should help readers understand where this product fits in the market.""",
            
            "content_structure": {
                "sections": [
                    "overview",
                    "build_quality",
                    "sound_performance", 
                    "features_functionality",
                    "playability_comfort",
                    "value_analysis",
                    "pros_cons",
                    "final_verdict"
                ],
                "min_products": 1,
                "max_products": 3
            },
            
            "seo_template": "{product_name} Review {year} - Honest Expert Analysis",
            "meta_description_template": "Comprehensive {product_name} review. Sound quality, build analysis, pros/cons, and value assessment from our expert team. Is it worth buying?"
        }

    @staticmethod
    def get_comparison_template() -> Dict[str, Any]:
        """Template for product comparison guides"""
        return {
            "name": "Product Comparison Guide", 
            "template_type": "comparison",
            "base_prompt": """You are an expert blog post writer with a deep knowledge of the {category} space, specializing in writing high quality SEO optimized listicles. A listicle is a structured list-format article that presents information in numbered format for easy digestion.

Write a detailed {word_count} word comparison listicle of {product_count} popular {category} instruments. Use an informal, down-to-earth tone written in 1st person plural ("We", "Our team" - but avoid referencing a specific company). Help readers choose between these specific models by highlighting their unique strengths and ideal use cases.

Content Quality Rules:
1. Minimum {word_count} words total
2. Each section must have at least 150 words minimum
3. Integrate relevant statistics in at least 5 instances across the listicle
4. Demonstrate expertise with specific hard facts, examples, numbers/data
5. Solve specific problems readers may have
6. Provide hands-on, practical, creative tips/ideas/facts
7. Include unique insights beyond obvious information

Structure your comparison with numbered sub-headers:
1. **Introduction** - Why these products were chosen, demonstrate expertise
2. **Quick Comparison Table** - Side-by-side specs and key features
3. **Detailed Analysis** - Deep dive into each product (numbered sub-sections)
4. **Head-to-Head Comparisons** - Direct comparisons in key areas
5. **Use Case Recommendations** - Which product for which scenario
6. **Price & Value Analysis** - Bang for buck assessment
7. **Final Recommendations** - Clear winner in different categories

For each product section, include:
- "sub_header" (numbered starting with "1.", "2.", etc.)
- "bold_paragraph_text" 
- "paragraph_text" (use multiple times, more in first sections than last)
- "article_tip" with unique tip_title per section

Make clear recommendations for different budgets, skill levels, and musical styles. Incorporate balance of perplexity and burstiness for human-like content.
Target word count: {word_count} words""",
            
            "product_context_prompt": """For each product in the comparison:
- Explain why it was selected for this comparison
- Highlight its unique selling points and differentiators
- Provide specific technical details and specifications
- Describe real-world performance characteristics
- Compare directly with the other products in relevant categories
- Give clear recommendations for who should choose this option

Focus on practical differences that matter to buyers.""",
            
            "content_structure": {
                "sections": [
                    "introduction",
                    "comparison_table",
                    "detailed_analysis",
                    "head_to_head",
                    "use_case_recommendations", 
                    "value_analysis",
                    "final_recommendations"
                ],
                "min_products": 2,
                "max_products": 5
            },
            
            "seo_template": "{product_1} vs {product_2} vs {product_3} - Which {category} Is Best?",
            "meta_description_template": "Detailed comparison of top {category} instruments. Features, sound, build quality, and value analysis to help you choose the right instrument for your needs."
        }

    @staticmethod
    def get_tutorial_template() -> Dict[str, Any]:
        """Template for educational/tutorial content"""
        return {
            "name": "Tutorial & Educational Guide",
            "template_type": "tutorial", 
            "base_prompt": """You are an expert blog post writer with a deep knowledge of the {category} space, specializing in writing high quality SEO optimized guides.

Create a comprehensive {word_count} word tutorial about {topic} for {skill_level} musicians using a formal, professional tone written in 1st person plural ("We", "Our team" - but avoid referencing a specific company). This should be educational content that teaches practical skills and knowledge.

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Add deeper insights or lesser-known facts about main topics
5. Provide personal experiences or case studies to showcase expertise
6. Expand on practical steps and detailed guidance
7. Include engaging and unique content that's shareable
8. Differentiate content with unique perspectives

Structure your tutorial with these sections:
1. **Introduction** - What you'll learn and why it matters
2. **Prerequisites** - What you need to know/have before starting
3. **Step-by-Step Guide** - Detailed instructions broken into clear steps
4. **Common Mistakes** - What to avoid and troubleshooting tips
5. **Practice Exercises** - Ways to develop and reinforce the skills
6. **Gear Recommendations** - Equipment that helps with this topic
7. **Next Steps** - How to continue developing these skills

Your tutorial should be:
- Clear and easy to follow with hyper-specific details
- Practical with actionable advice beyond the obvious
- Progressive (building complexity appropriately)
- Encouraging for learners
- Based on proven teaching methods and expertise

Incorporate balance of perplexity and burstiness to make content humanlike. Include specific examples, exercises, and real-world applications.
Target word count: {word_count} words""",
            
            "product_context_prompt": """Recommend specific products that are ideal for learning or implementing the tutorial topic:
- Explain why each product is recommended for this learning context
- Specify what features make it good for beginners/intermediate/advanced learners
- Provide alternatives at different price points
- Explain how the gear supports the learning process
- Give specific examples of how to use the gear in practice

Focus on products that genuinely enhance the learning experience.""",
            
            "content_structure": {
                "sections": [
                    "introduction",
                    "prerequisites",
                    "step_by_step",
                    "common_mistakes",
                    "practice_exercises",
                    "gear_recommendations", 
                    "next_steps"
                ],
                "min_products": 1,
                "max_products": 5
            },
            
            "seo_template": "How to {topic} - Complete Guide for {skill_level} Musicians",
            "meta_description_template": "Learn {topic} with our step-by-step guide. Tips, techniques, and gear recommendations for {skill_level} musicians to master this skill."
        }

    @staticmethod
    def get_history_template() -> Dict[str, Any]:
        """Template for historical/cultural content"""
        return {
            "name": "Historical & Cultural Article",
            "template_type": "history",
            "base_prompt": """You are an expert blog post writer with a deep knowledge of the {category} space, specializing in writing high quality SEO optimized guides.

Write a comprehensive {word_count} word article about the history and cultural significance of {topic} using a formal, professional tone written in 1st person plural ("We", "Our team" - but avoid referencing a specific company). This should be an engaging historical narrative that connects past to present.

Content Quality Rules:
1. Less than 25% of all sentences must be longer than 20 words
2. Do not use passive voice
3. Include unique insights or data not commonly found on similar pages
4. Conduct original research or provide unique analysis
5. Add deeper insights or lesser-known facts about main topics
6. Enhance depth and quality suitable for print or reference
7. Include engaging and unique content that's shareable
8. Provide personal experiences or case studies to showcase expertise

Structure your article with these sections:
1. **Origins** - How and where {topic} began
2. **Key Historical Periods** - Major developments and milestones
3. **Influential Figures** - Important people who shaped the evolution
4. **Cultural Impact** - How {topic} influenced music and society
5. **Technical Evolution** - How the technology/technique developed
6. **Modern Legacy** - How historical developments influence today's music
7. **Conclusion** - The lasting significance and future outlook

Your article should be:
- Historically accurate and well-researched with unique perspectives
- Engaging storytelling that brings history to life
- Educational without being academic, hyper-specific and detailed
- Connected to modern relevance beyond obvious connections
- Culturally sensitive and inclusive

Incorporate balance of perplexity and burstiness for humanlike content. Include interesting anecdotes, lesser-known facts, and clear connections between historical developments and modern music.
Target word count: {word_count} words""",
            
            "product_context_prompt": """Feature instruments or gear that have historical significance or modern relevance to the topic:
- Explain the historical context and importance of vintage/classic instruments
- Show how modern instruments connect to historical traditions
- Highlight recreations or reissues of historically significant gear
- Explain what modern musicians can learn from historical examples
- Connect specific products to the cultural movements discussed

Focus on products that genuinely connect to and illustrate the historical narrative.""",
            
            "content_structure": {
                "sections": [
                    "origins",
                    "key_periods", 
                    "influential_figures",
                    "cultural_impact",
                    "technical_evolution",
                    "modern_legacy",
                    "conclusion"
                ],
                "min_products": 0,
                "max_products": 4
            },
            
            "seo_template": "The History of {topic} - From Origins to Modern Day",
            "meta_description_template": "Explore the fascinating history of {topic}. Key moments, influential musicians, and evolution from historical origins to modern instruments and techniques."
        }

    @staticmethod
    def get_listicle_template() -> Dict[str, Any]:
        """Template for listicle blog posts"""
        return {
            "name": "SEO Optimized Listicle",
            "template_type": "listicle",
            "base_prompt": """You are an expert blog post writer with a deep knowledge of the {category} space, specializing in writing high quality SEO optimized listicles. A listicle is a type of online content that is structured primarily as a list, presenting information in a numbered format for easy reader digestion.

Write a {word_count} word listicle using the title "{title}". Use an informal, down-to-earth tone written in 1st person plural ("We", "Our team" - but do not reference a specific company). The aim is to solve a specific problem readers may have or provide hands-on, practical, creative tips/ideas/facts while demonstrating expertise.

Content Requirements:
- Minimum {word_count} words total
- Each section must have at least 150 words minimum
- If listicle has 5 sub-headers: each section needs 500+ words
- If listicle has 10 sub-headers: each section needs 300+ words
- If listicle has 20 sub-headers: each section needs 150+ words
- Integrate relevant statistics in at least 5 instances across the listicle
- Underline expertise with specific hard facts, examples, numbers/data, and statistics
- Include unique insights beyond obvious information

Structure Requirements:
- Create concise introduction demonstrating expertise with phrases like "We performed extensive tests..." or "Our team has thoroughly assessed..."
- Number each sub-header starting with "1.", "2.", "3.", etc.
- Use variable paragraph distribution: first sections have more paragraph elements than last sections
- Include unique tip_title for each section's article_tip

JSON Structure per section:
- "sub_header" (numbered)
- "bold_paragraph_text"
- "paragraph_text" (use multiple times per section)
- "article_tip" with unique "tip_title"

Incorporate balance of perplexity and burstiness for human-like content.
Target word count: {word_count} words""",
            
            "product_context_prompt": """For each product in the listicle:
- Explain why it was selected for this specific list
- Highlight unique selling points and differentiators
- Provide specific technical details and real-world performance
- Compare with similar alternatives when relevant
- Give clear recommendations for target audience
- Focus on practical differences that matter to buyers

Ensure products genuinely fit the listicle's purpose and provide value to readers.""",
            
            "content_structure": {
                "sections": [
                    "introduction",
                    "numbered_items"
                ],
                "min_products": 3,
                "max_products": 20
            },
            
            "seo_template": "{number} Best {category} {year} - Expert Picks & Reviews",
            "meta_description_template": "Discover the top {number} {category} with our expert reviews. Compare features, prices, and performance to find your perfect match."
        }

    @staticmethod
    def get_detailed_review_template() -> Dict[str, Any]:
        """Template for comprehensive product reviews"""
        return {
            "name": "Comprehensive Product Review",
            "template_type": "detailed_review",
            "base_prompt": """You are an expert blog post writer with a deep knowledge of the {category} space, specializing in writing high quality SEO optimized reviews.

Write a comprehensive {word_count} word review of the {product_name}. Ensure the tone is formal and professional, written in 1st person plural ("We", "Our team" - but avoid referencing a specific company). The aim is to educate readers about the brand by providing up-to-date, helpful content.

Mandatory Structure (follow this sequence exactly):
1. **Opening (3 paragraphs)** - Hook reader immediately, demonstrate expertise with "We performed extensive tests..." or similar. Format in bold. End with mini summary praising positive aspects. No "Introduction" headline.
2. **"Short on Time? Here are Our Key Findings"** - Pros vs cons with detailed explanations
3. **Features Table** - Generate features with accurate statistics/numbers
4. **Quality & Performance Analysis (2 paragraphs)** - Include anecdotal evidence of product engagement with specific testing scenarios
5. **Article Tip** - Most vital information or warnings for readers
6. **3 Relevant Subheaders** - Topics like scope/reach, features/plans, policy/transparency, user experience. Each: 2 paragraphs of 5 sentences, format part of last paragraph as list with catchy bullet points
7. **Setup/Installation Guide** - Include quick_guide with 3 easy steps
8. **Pricing** - Comprehensive pricing analysis
9. **Reliability & Support** - Include anecdotal reference with specific response times and resolution times (5 sentences per paragraph)
10. **Summary** - Standout features with subtle drawbacks as hidden advantages ("While priced above competitors, it reflects superior quality")
11. **Secret Tip** - 2-3 sentences of specific, beyond-obvious advice
12. **FAQ** - Questions frequently asked online, 5+ sentences per answer
13. **Comparison Footer** - "Compare {product_name} With Top Alternatives"

Content Requirements:
- Include anecdotal evidence demonstrating product engagement
- Mention specific waiting times and resolution times for support
- Provide accurate statistics/numbers in features table
- Educational focus about the brand
- Balance of perplexity and burstiness for human-like content

Target word count: {word_count} words""",
            
            "product_context_prompt": """Focus primarily on the main product being reviewed. Include 1-2 direct competitors for comparison context:
- Provide specific technical specifications and real testing results
- Describe actual sound characteristics and performance you've experienced
- Compare build quality, materials, and construction details
- Explain real-world performance in different usage scenarios
- Give honest assessment of value proposition and market positioning
- Include anecdotal evidence of customer support interactions

Comparisons should help readers understand market positioning and alternatives.""",
            
            "content_structure": {
                "sections": [
                    "opening_hook",
                    "pro_cons_summary",
                    "features_table",
                    "performance_analysis",
                    "vital_tip",
                    "detailed_subheaders",
                    "setup_guide",
                    "pricing_analysis",
                    "support_reliability",
                    "summary_drawbacks",
                    "secret_tip",
                    "faq_section",
                    "comparison_footer"
                ],
                "min_products": 1,
                "max_products": 3
            },
            
            "seo_template": "{product_name} Review {year} - Honest Expert Analysis",
            "meta_description_template": "Comprehensive {product_name} review. Sound quality, build analysis, pros/cons, and value assessment from our expert team. Is it worth buying?"
        }

class BlogPromptBuilder:
    """
    Builder class for creating customized blog generation prompts
    """
    
    def __init__(self):
        self.templates = BlogPromptTemplates()
    
    def build_prompt(
        self,
        template_type: str,
        products: List[Dict[str, Any]],
        custom_variables: Dict[str, Any],
        word_count: int = 2500
    ) -> Dict[str, str]:
        """
        Build a complete prompt for blog generation
        
        Args:
            template_type: Type of blog post template to use
            products: List of products to feature
            custom_variables: Variables to substitute in template
            word_count: Target word count for the post
            
        Returns:
            Dict containing system_prompt, user_prompt, and metadata
        """
        
        # Get the appropriate template
        template_method = getattr(self.templates, f'get_{template_type}_template', None)
        if not template_method:
            raise ValueError(f"Unknown template type: {template_type}")
        
        template = template_method()
        
        # Build system prompt
        system_prompt = self.templates.get_base_system_prompt()
        if template.get('additional_system_prompt'):
            system_prompt += f"\n\n{template['additional_system_prompt']}"
        
        # Substitute variables in base prompt
        base_prompt = template['base_prompt'].format(
            word_count=word_count,
            **custom_variables
        )
        
        # Add product context if products are provided
        user_prompt_parts = [base_prompt]
        
        if products and template.get('product_context_prompt'):
            product_info = self._format_product_info(products)
            product_context = template['product_context_prompt']
            user_prompt_parts.extend([
                f"\n{product_context}",
                f"\nFeatured Products:\n{product_info}"
            ])
        
        # Add JSON response format requirement
        user_prompt_parts.append(self._get_json_format_requirement(template, products))
        
        user_prompt = "\n".join(user_prompt_parts)
        
        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "template_metadata": template,
            "expected_structure": template.get('content_structure', {})
        }
    
    def _format_product_info(self, products: List[Dict[str, Any]]) -> str:
        """Format product information for inclusion in prompts"""
        product_lines = []
        
        for i, product in enumerate(products, 1):
            brand = product.get('brand_name', 'Unknown Brand')
            category = product.get('category_name', 'Unknown Category') 
            rating = product.get('avg_rating')
            rating_str = f"Rating: {rating:.1f}/5" if rating else "Rating: N/A"
            review_count = product.get('review_count', 0)
            
            line = f"{i}. {product['name']} by {brand}"
            line += f" ({category}, {rating_str}"
            if review_count:
                line += f", {review_count} reviews)"
            else:
                line += ")"
                
            if product.get('description'):
                # Truncate description to avoid prompt bloat
                desc = product['description'][:150]
                if len(product['description']) > 150:
                    desc += "..."
                line += f"\n   Description: {desc}"
            
            product_lines.append(line)
        
        return "\n".join(product_lines)
    
    def _get_json_format_requirement(
        self, 
        template: Dict[str, Any], 
        products: List[Dict[str, Any]]
    ) -> str:
        """Generate JSON format requirements for the response"""
        
        product_ids = [p['id'] for p in products] if products else []
        
        return f"""
IMPORTANT: Your response must be valid JSON with this exact structure:

{{
    "title": "Generated blog post title (SEO optimized)",
    "excerpt": "Brief excerpt/summary (150-200 characters)",
    "content": "Full blog post content in markdown format",
    "seo_title": "SEO optimized title (max 60 characters)",
    "seo_description": "SEO meta description (max 160 characters)",
    "sections": [
        {{
            "type": "introduction",
            "title": "Section Title",
            "content": "Section content in markdown"
        }}
    ],
    "product_recommendations": [
        {{
            "product_id": {product_ids[0] if product_ids else 'PRODUCT_ID'},
            "relevance_score": 0.95,
            "reasoning": "Why this product is recommended and fits the content",
            "suggested_context": "recommended|featured|comparison|alternative",
            "suggested_sections": ["introduction", "recommendations"]
        }}
    ]
}}

Ensure all JSON is properly formatted and valid. Product IDs must match the provided products: {product_ids}
"""

# Utility functions for prompt customization
def get_current_year() -> int:
    """Get current year for date-sensitive prompts"""
    return datetime.now().year

def format_category_name(category: str) -> str:
    """Format category name for use in prompts"""
    return category.lower().replace('_', ' ').replace('-', ' ')

def generate_seo_keywords(topic: str, products: List[Dict[str, Any]]) -> List[str]:
    """Generate relevant SEO keywords for a topic and products"""
    keywords = [topic.lower()]
    
    # Add product-related keywords
    for product in products:
        if product.get('brand_name'):
            keywords.append(product['brand_name'].lower())
        if product.get('category_name'):
            keywords.append(product['category_name'].lower())
    
    # Add year for freshness
    current_year = get_current_year()
    keywords.append(str(current_year))
    
    # Add generic music keywords
    keywords.extend(['music', 'instruments', 'gear', 'review', 'guide'])
    
    return list(set(keywords))  # Remove duplicates
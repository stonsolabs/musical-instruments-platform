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
            "base_prompt": """Write a comprehensive buying guide for {category} instruments. Your guide should help both beginners and experienced players choose the right instrument for their needs and budget.

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
            "base_prompt": """Write a comprehensive, hands-on review of the {product_name}. This should be an authoritative review that helps potential buyers understand exactly what they're getting.

Structure your review with these sections:
1. **Overview** - First impressions and key specifications
2. **Build Quality & Design** - Materials, construction, aesthetics
3. **Sound & Performance** - Detailed sound analysis across different contexts
4. **Features & Functionality** - All features and how they perform in practice
5. **Playability & Comfort** - User experience and ergonomics
6. **Value Analysis** - Price vs. performance assessment
7. **Pros & Cons** - Honest breakdown of strengths and weaknesses
8. **Final Verdict** - Who should buy this and why

Your review should be:
- Based on extensive hands-on experience
- Honest about both strengths and limitations
- Comparative (how it stacks up against competitors)
- Practical (real-world usage scenarios)
- Detailed enough to help buying decisions

Include specific technical details, sound characteristics, and usage examples.
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
            "base_prompt": """Write a detailed comparison of {product_count} popular {category} instruments. Help readers choose between these specific models by highlighting their unique strengths and ideal use cases.

Structure your comparison with these sections:
1. **Introduction** - Why these products were chosen for comparison
2. **Quick Comparison Table** - Side-by-side specs and key features
3. **Detailed Analysis** - Deep dive into each product
4. **Head-to-Head Comparisons** - Direct comparisons in key areas
5. **Use Case Recommendations** - Which product for which scenario
6. **Price & Value Analysis** - Bang for buck assessment
7. **Final Recommendations** - Clear winner in different categories

For each product, cover:
- Key specifications and features
- Sound characteristics and tonal qualities
- Build quality and materials
- Target audience and ideal use cases
- Strengths and weaknesses
- Value proposition at its price point

Make clear recommendations for different budgets, skill levels, and musical styles.
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
            "base_prompt": """Create a comprehensive tutorial about {topic} for {skill_level} musicians. This should be educational content that teaches practical skills and knowledge.

Structure your tutorial with these sections:
1. **Introduction** - What you'll learn and why it matters
2. **Prerequisites** - What you need to know/have before starting
3. **Step-by-Step Guide** - Detailed instructions broken into clear steps
4. **Common Mistakes** - What to avoid and troubleshooting tips
5. **Practice Exercises** - Ways to develop and reinforce the skills
6. **Gear Recommendations** - Equipment that helps with this topic
7. **Next Steps** - How to continue developing these skills

Your tutorial should be:
- Clear and easy to follow
- Practical with actionable advice
- Progressive (building complexity appropriately)
- Encouraging for learners
- Based on proven teaching methods

Include specific examples, exercises, and real-world applications.
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
            "base_prompt": """Write about the history and cultural significance of {topic}. This should be an engaging historical narrative that connects past to present.

Structure your article with these sections:
1. **Origins** - How and where {topic} began
2. **Key Historical Periods** - Major developments and milestones
3. **Influential Figures** - Important people who shaped the evolution
4. **Cultural Impact** - How {topic} influenced music and society
5. **Technical Evolution** - How the technology/technique developed
6. **Modern Legacy** - How historical developments influence today's music
7. **Conclusion** - The lasting significance and future outlook

Your article should be:
- Historically accurate and well-researched
- Engaging storytelling that brings history to life
- Educational without being academic
- Connected to modern relevance
- Culturally sensitive and inclusive

Include interesting anecdotes, lesser-known facts, and clear connections between historical developments and modern music.
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
        word_count: int = 800
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
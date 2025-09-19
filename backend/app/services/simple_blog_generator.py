"""
Simplified Blog AI Generator Service
Generates blog content using the new simplified JSON structure
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class SimpleBlogGenerator:
    
    def __init__(self, openai_client=None):
        self.openai_client = openai_client
    
    def generate_blog_post(
        self,
        topic: str,
        template_name: str = "buying-guide",
        products: List[Dict] = None,
        target_words: int = 4000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a blog post using the simplified JSON structure
        
        Args:
            topic: The blog post topic/title
            template_name: Template type (buying-guide, review, comparison, artist-spotlight, instrument-history, gear-tips, news-feature)
            products: List of products to include
            target_words: Target word count (3000-5000)
            
        Returns:
            Generated blog post content as dict
        """
        
        if not products:
            products = []
            
        # Build the generation prompt
        prompt = self._build_prompt(topic, template_name, products, target_words)
        
        # Call AI model (placeholder for actual implementation)
        response = self._call_ai_model(prompt)
        
        # Parse and validate response
        try:
            content = json.loads(response)
            return self._validate_and_enhance_content(content, products)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            raise ValueError("AI response is not valid JSON")
    
    def _build_prompt(self, topic: str, template_name: str, products: List[Dict], target_words: int) -> str:
        """Build the AI generation prompt"""
        
        template_config = BLOG_TEMPLATES.get(template_name, BLOG_TEMPLATES["buying-guide"])
        
        base_prompt = f"""
Create a comprehensive {template_config['name'].lower()} about "{topic}".

CRITICAL REQUIREMENTS:
- Target word count: {target_words} words (minimum 3000, maximum 5000)
- Write in {template_config['tone']} tone
- {template_config['description']}
- Affiliate integration level: {template_config['affiliate_integration']}
- Make content evergreen (no specific years unless essential)
- Focus on providing real value to readers

RESPONSE FORMAT:
Respond ONLY with a valid JSON object in this exact structure:

{{
  "title": "SEO-optimized title (60 chars max)",
  "excerpt": "Compelling excerpt (150-160 chars)",
  "seo_title": "SEO title with keywords",
  "seo_description": "Meta description (150-160 chars)",
  "sections": [
    {{
      "type": "intro",
      "content": "Hook + context + what readers will learn (400-600 words)"
    }},"""

        # Add template-specific sections
        sections_guide = {
            "buying-guide": '''
    {
      "type": "quick_picks",
      "title": "Our Top Picks",
      "products": [
        {
          "id": "product_id",
          "name": "Product Name", 
          "price": "$XXX",
          "reason": "Why we recommend it",
          "affiliate_url": "https://example.com/product"
        }
      ]
    },
    {
      "type": "content",
      "content": "## What to Look For\\n\\nDetailed buying criteria (800-1000 words)"
    },
    {
      "type": "product_spotlight", 
      "product": {
        "id": "product_id",
        "name": "Product Name",
        "price": "$XXX", 
        "rating": 4.5,
        "pros": ["Pro 1", "Pro 2"],
        "cons": ["Con 1", "Con 2"],
        "affiliate_url": "https://example.com/product"
      }
    },
    {
      "type": "content",
      "content": "## Detailed Reviews\\n\\nIn-depth analysis (1500-2000 words)"
    },
    {
      "type": "affiliate_banner"
    },''',
            
            "artist-spotlight": '''
    {
      "type": "content",
      "content": "## Early Life and Musical Journey\\n\\nDetailed biography (600-800 words)"
    },
    {
      "type": "content",
      "content": "## Musical Impact and Influence\\n\\nTheir contribution to music (600-800 words)"
    },
    {
      "type": "content",
      "content": "## Signature Gear and Sound\\n\\nInstruments and equipment they made famous (800-1000 words)"
    },
    {
      "type": "product_spotlight",
      "product": {
        "id": "signature_instrument_id",
        "name": "Signature Instrument",
        "price": "$XXX",
        "rating": 4.8,
        "pros": ["Authentic sound", "Quality craftsmanship"],
        "cons": ["Premium price"],
        "affiliate_url": "https://example.com/signature"
      }
    },
    {
      "type": "content", 
      "content": "## Legacy and Continuing Influence\\n\\nTheir lasting impact (400-600 words)"
    },''',
            
            "instrument-history": '''
    {
      "type": "content",
      "content": "## Origins and Early Development\\n\\nHow it all began (600-800 words)"
    },
    {
      "type": "content",
      "content": "## Evolution Through the Decades\\n\\nKey changes and improvements (800-1000 words)"
    },
    {
      "type": "content",
      "content": "## Innovations and Breakthroughs\\n\\nTechnological advances (600-800 words)"
    },
    {
      "type": "content",
      "content": "## Cultural Impact and Famous Players\\n\\nHow it shaped music (800-1000 words)"
    },
    {
      "type": "product_spotlight",
      "product": {
        "id": "modern_version_id",
        "name": "Modern Version",
        "price": "$XXX",
        "rating": 4.6,
        "pros": ["Classic design", "Modern improvements"],
        "cons": ["Higher price than vintage"],
        "affiliate_url": "https://example.com/modern"
      }
    },''',
            
            "gear-tips": '''
    {
      "type": "content",
      "content": "## Essential Tips Every Player Should Know\\n\\nCore knowledge (800-1000 words)"
    },
    {
      "type": "content",
      "content": "## Common Mistakes to Avoid\\n\\nPitfalls and how to prevent them (600-800 words)"
    },
    {
      "type": "content",
      "content": "## Maintenance and Care\\n\\nKeeping your gear in top shape (600-800 words)"
    },
    {
      "type": "content",
      "content": "## Pro Techniques and Advanced Tips\\n\\nTake it to the next level (800-1000 words)"
    },
    {
      "type": "product_spotlight",
      "product": {
        "id": "recommended_accessory_id", 
        "name": "Essential Accessory",
        "price": "$XXX",
        "rating": 4.7,
        "pros": ["Professional quality", "Great value"],
        "cons": ["Requires learning curve"],
        "affiliate_url": "https://example.com/accessory"
      }
    },''',
            
            "news-feature": '''
    {
      "type": "content",
      "content": "## Background and Context\\n\\nSetting the stage (600-800 words)"
    },
    {
      "type": "content",
      "content": "## Key Details and Developments\\n\\nWhat's happening (800-1000 words)"
    },
    {
      "type": "content",
      "content": "## Industry Impact\\n\\nWhy this matters (600-800 words)"
    },
    {
      "type": "content",
      "content": "## Expert Analysis\\n\\nProfessional perspective (600-800 words)"
    },'''
        }
        
        # Default sections for review and comparison
        if template_name == "review":
            sections_guide[template_name] = '''
    {
      "type": "content",
      "content": "## Overview and First Impressions\\n\\nInitial thoughts (400-500 words)"
    },
    {
      "type": "content", 
      "content": "## Performance Analysis\\n\\nDetailed testing results (1000-1200 words)"
    },
    {
      "type": "content",
      "content": "## Pros and Cons\\n\\nHonest assessment (600-800 words)"
    },
    {
      "type": "product_spotlight",
      "product": {
        "id": "reviewed_product_id",
        "name": "Reviewed Product",
        "price": "$XXX",
        "rating": 4.3,
        "pros": ["Strong point 1", "Strong point 2"],
        "cons": ["Weakness 1", "Weakness 2"],
        "affiliate_url": "https://example.com/reviewed"
      }
    },
    {
      "type": "content",
      "content": "## Comparison with Competitors\\n\\nHow it stacks up (600-800 words)"
    },'''
        elif template_name == "comparison":
            sections_guide[template_name] = '''
    {
      "type": "content",
      "content": "## Side-by-Side Analysis\\n\\nDetailed comparison (1000-1200 words)"
    },
    {
      "type": "comparison_table",
      "title": "Feature Comparison",
      "products": [
        {
          "id": "product1_id",
          "name": "Product 1",
          "features": {"price": "$XXX", "rating": "4.5/5", "feature1": "Value1"}
        },
        {
          "id": "product2_id", 
          "name": "Product 2",
          "features": {"price": "$XXX", "rating": "4.3/5", "feature1": "Value2"}
        }
      ]
    },
    {
      "type": "content",
      "content": "## Detailed Analysis\\n\\nIn-depth feature breakdown (1000-1200 words)"
    },
    {
      "type": "content",
      "content": "## Recommendations by Use Case\\n\\nWho should buy what (600-800 words)"
    },'''

        base_prompt += sections_guide.get(template_name, sections_guide["buying-guide"])
        
        base_prompt += '''
    {
      "type": "conclusion",
      "content": "## Final Thoughts\\n\\nSummary and recommendations (300-500 words)"
    }
  ],
  "tags": ["tag1", "tag2", "tag3"],
  "category": "''' + template_name + '''",
  "featured_products": ["product_id1", "product_id2"]
}

CONTENT GUIDELINES:
- Write comprehensive, detailed sections that reach the target word count
- Use proper markdown formatting (##, ###, -, *, etc.)
- Include specific details, specs, and examples
- Add personal insights and expert knowledge  
- Use lists, quotes, and structured content for readability
- Integrate products naturally within the content flow
- Focus on providing genuine value to readers
- Include relevant anecdotes and stories
- Make content engaging and easy to read

'''

        # Add product context if available
        if products:
            product_context = "\n\nAVAILABLE PRODUCTS TO REFERENCE:\n"
            for product in products:
                product_context += f"- {product.get('name', 'N/A')} (ID: {product.get('id', 'N/A')}) - ${product.get('price', 'N/A')}\n"
            base_prompt += product_context

        base_prompt += f"\n\nTopic: {topic}\nTarget words: {target_words}\n\nRespond with JSON only:"
        
        return base_prompt
    
    def _call_ai_model(self, prompt: str) -> str:
        """Call the AI model to generate content"""
        # Placeholder - replace with actual OpenAI API call
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4.1",
                    messages=[
                        {"role": "system", "content": "You are an expert music journalist and gear reviewer. Always respond with valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=8000,
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                raise
        
        # Fallback mock response for testing
        return json.dumps({
            "title": "Sample Article",
            "excerpt": "A sample article excerpt.",
            "seo_title": "Sample Article - Music Gear Guide",
            "seo_description": "Learn about music gear in this comprehensive guide.",
            "sections": [
                {
                    "type": "intro",
                    "content": "This is a sample introduction..."
                }
            ],
            "tags": ["sample", "test"],
            "category": "general",
            "featured_products": []
        })
    
    def _validate_and_enhance_content(self, content: Dict, products: List[Dict]) -> Dict:
        """Validate and enhance the generated content"""
        
        # Ensure required fields exist
        required_fields = ["title", "sections"]
        for field in required_fields:
            if field not in content:
                raise ValueError(f"Missing required field: {field}")
        
        # Set defaults for optional fields
        content.setdefault("excerpt", content["title"])
        content.setdefault("seo_title", content["title"])
        content.setdefault("seo_description", content.get("excerpt", ""))
        content.setdefault("tags", [])
        content.setdefault("category", "general")
        content.setdefault("featured_products", [])
        
        # Validate sections
        if not isinstance(content["sections"], list) or len(content["sections"]) == 0:
            raise ValueError("Sections must be a non-empty list")
        
        # Add metadata
        content["generated_at"] = datetime.now().isoformat()
        content["word_count"] = self._estimate_word_count(content)
        
        return content
    
    def _estimate_word_count(self, content: Dict) -> int:
        """Estimate total word count of the blog post"""
        total_words = 0
        
        for section in content.get("sections", []):
            if "content" in section:
                # Simple word count estimation
                text = section["content"].replace("#", "").replace("*", "").replace("-", "")
                words = len(text.split())
                total_words += words
        
        return total_words

# Template configurations
BLOG_TEMPLATES = {
    "buying-guide": {
        "name": "Buying Guide",
        "description": "Comprehensive guides to help users choose the right products",
        "target_words": 4000,
        "tone": "expert and friendly",
        "affiliate_integration": "seamless"
    },
    "review": {
        "name": "Product Review", 
        "description": "In-depth reviews of specific products",
        "target_words": 3500,
        "tone": "honest and expert",
        "affiliate_integration": "moderate"
    },
    "comparison": {
        "name": "Product Comparison",
        "description": "Side-by-side comparisons of similar products", 
        "target_words": 3000,
        "tone": "analytical and helpful",
        "affiliate_integration": "high"
    },
    "artist-spotlight": {
        "name": "Artist Spotlight",
        "description": "Celebrating musicians and their impact on music",
        "target_words": 4000,
        "tone": "celebratory and inspiring",
        "affiliate_integration": "subtle"
    },
    "instrument-history": {
        "name": "Instrument History",
        "description": "Deep dives into the history and evolution of instruments",
        "target_words": 4500,
        "tone": "educational and engaging",
        "affiliate_integration": "light"
    },
    "gear-tips": {
        "name": "Gear Tips",
        "description": "Practical advice and tips for musicians",
        "target_words": 3500,
        "tone": "helpful and expert",
        "affiliate_integration": "moderate"
    },
    "news-feature": {
        "name": "News Feature",
        "description": "Informative articles about music industry news",
        "target_words": 3000,
        "tone": "journalistic and informative",
        "affiliate_integration": "minimal"
    }
}
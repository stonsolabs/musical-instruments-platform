"""
Simplified Blog AI Generator Service
Generates blog content using the new simplified JSON structure
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from sqlalchemy import text
from ..database import async_session_factory

logger = logging.getLogger(__name__)

class SimpleBlogGenerator:
    
    def __init__(self, openai_client=None):
        self.openai_client = openai_client
        self.templates = {}
    
    async def _load_templates(self):
        """Load templates from database"""
        if self.templates:
            return  # Already loaded
            
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT name, prompt FROM blog_templates ORDER BY name
            '''))
            
            for row in result.fetchall():
                self.templates[row[0]] = row[1]
            
            logger.info(f"Loaded {len(self.templates)} templates from database")
    
    async def generate_blog_post(
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
        
        # Load templates from database
        await self._load_templates()
        
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
        """Build the AI generation prompt using database templates"""
        
        # Get template from database (loaded templates)
        base_template = self.templates.get(template_name)
        if not base_template:
            logger.warning(f"Template {template_name} not found, using buying-guide")
            base_template = self.templates.get('buying-guide', 'Create a comprehensive guide about {topic}.')
        
        # Use the database template and format it with the topic
        prompt = base_template.format(topic=topic)
        
        # Add JSON structure requirements
        prompt += f"""

TARGET WORD COUNT: {target_words} words (minimum 3000, maximum 5000)

RESPONSE FORMAT:
Respond ONLY with a valid JSON object in this exact structure:

{{
  "title": "Creative, engaging title (50-65 chars)",
  "excerpt": "Compelling excerpt (150-160 chars)", 
  "seo_title": "SEO title with keywords",
  "seo_description": "Meta description (150-160 chars)",
  "sections": [
    {{
      "type": "intro",
      "content": "Hook + context + preview (400-600 words in markdown)"
    }},
    {{
      "type": "content", 
      "content": "## Main Section\\n\\nDetailed content (800-1200 words)"
    }},
    {{
      "type": "product_spotlight",
      "product": {{
        "id": "product_id",
        "name": "Product Name",
        "price": "$XXX",
        "rating": 4.5,
        "pros": ["Pro 1", "Pro 2"],
        "cons": ["Con 1"],
        "affiliate_url": "https://example.com/product"
      }}
    }},
    {{
      "type": "content",
      "content": "## Additional Section\\n\\nMore detailed content (800-1200 words)"
    }},
    {{
      "type": "conclusion",
      "content": "## Final Thoughts\\n\\nSummary and recommendations (300-500 words)"
    }}
  ],
  "tags": ["tag1", "tag2", "tag3"],
  "category": "{template_name}",
  "featured_products": ["product_id1", "product_id2"]
}}

CRITICAL: Respond with JSON only. No text before or after."""

        # Add product context if available
        if products:
            product_context = "\n\nAVAILABLE PRODUCTS TO REFERENCE:\n"
            for product in products:
                product_context += f"- {product.get('name', 'N/A')} (ID: {product.get('id', 'N/A')}) - ${product.get('price', 'N/A')}\n"
            prompt += product_context

        prompt += f"\n\nTopic: {topic}\nTarget words: {target_words}\n\nRespond with JSON only:"
        
        return prompt
    
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

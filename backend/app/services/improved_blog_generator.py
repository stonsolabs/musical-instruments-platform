#!/usr/bin/env python3
"""
Improved Blog AI Generator Service
Properly matches products to content and creates rich blog posts
"""

import json
import logging
import random
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from sqlalchemy import text
from ..database import async_session_factory

logger = logging.getLogger(__name__)

class ImprovedBlogGenerator:
    
    def __init__(self, openai_client=None):
        self.openai_client = openai_client
        self.templates = {}
        self.products_by_category = {}
        self.all_products = []
    
    async def initialize(self):
        """Initialize the service by loading templates and products"""
        async with async_session_factory() as session:
            await self._load_templates(session)
            await self._load_products(session)
    
    async def _load_templates(self, session):
        """Load templates from database"""
        result = await session.execute(text('''
            SELECT name, prompt FROM blog_templates ORDER BY name
        '''))
        
        for row in result.fetchall():
            self.templates[row[0]] = row[1]
        
        logger.info(f"Loaded {len(self.templates)} templates from database")
    
    async def _load_products(self, session):
        """Load and organize products by category"""
        query = """
        SELECT DISTINCT
            p.id,
            p.name,
            p.slug,
            p.avg_rating as rating,
            p.review_count as review_count,
            COALESCE(p.msrp_price, 0) as price,
            b.name as brand_name,
            c.name as category_name,
            c.slug as category_slug,
            p.description
        FROM products p
        JOIN brands b ON p.brand_id = b.id
        JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = true
        AND b.name != 'Unknown Brand'
        AND p.name IS NOT NULL
        AND p.name != ''
        AND (p.review_count > 0 OR p.review_count IS NULL OR p.avg_rating IS NOT NULL)
        ORDER BY review_count DESC NULLS LAST, rating DESC NULLS LAST, p.name
        """
        
        result = await session.execute(text(query))
        products = [dict(row._mapping) for row in result.fetchall()]
        
        # Organize by category
        for product in products:
            category_slug = product['category_slug']
            if category_slug not in self.products_by_category:
                self.products_by_category[category_slug] = []
            self.products_by_category[category_slug].append(product)
        
        self.all_products = products
        print(f"Loaded {len(products)} products across {len(self.products_by_category)} categories")
        
        # Show product distribution
        for category, prods in sorted(self.products_by_category.items()):
            print(f"  {category}: {len(prods)} products")
    
    def _extract_topic_keywords(self, topic: str) -> List[str]:
        """Extract keywords from topic to match relevant products"""
        topic_lower = topic.lower()
        
        # Product type keywords
        keywords = []
        
        # Direct instrument mentions
        instrument_keywords = {
            'guitar': ['guitar', 'electric guitar', 'acoustic guitar', 'bass guitar'],
            'keyboard': ['keyboard', 'piano', 'midi', 'synthesizer', 'synth'],
            'drum': ['drum', 'drums', 'percussion', 'cymbal'],
            'microphone': ['microphone', 'mic', 'recording', 'vocal'],
            'amplifier': ['amp', 'amplifier', 'speaker'],
            'audio': ['audio', 'interface', 'mixer', 'monitor'],
            'string': ['string', 'strings', 'violin', 'viola', 'cello'],
            'brass': ['trumpet', 'trombone', 'saxophone', 'horn'],
            'wind': ['flute', 'clarinet', 'oboe']
        }
        
        for category, terms in instrument_keywords.items():
            if any(term in topic_lower for term in terms):
                keywords.append(category)
        
        # Brand mentions
        brand_keywords = [
            'fender', 'gibson', 'yamaha', 'roland', 'akai', 'arturia', 
            'korg', 'moog', 'shure', 'audio-technica', 'martin', 'taylor'
        ]
        
        for brand in brand_keywords:
            if brand in topic_lower:
                keywords.append(brand)
        
        # Music genre keywords
        genre_keywords = {
            'rock': ['electric-guitars', 'guitar-amps', 'drums'],
            'jazz': ['acoustic-guitars', 'keyboards', 'brass'],
            'classical': ['acoustic-guitars', 'keyboards', 'strings'],
            'electronic': ['keyboards', 'audio-interfaces', 'synthesizers'],
            'country': ['acoustic-guitars', 'harmonica'],
            'blues': ['electric-guitars', 'harmonicas', 'guitar-amps']
        }
        
        for genre, categories in genre_keywords.items():
            if genre in topic_lower:
                keywords.extend(categories)
        
        return keywords
    
    def _select_relevant_products(self, topic: str, template_name: str, max_products: int = 5) -> List[Dict]:
        """Select products that are actually relevant to the topic"""
        keywords = self._extract_topic_keywords(topic)
        topic_lower = topic.lower()
        
        relevant_products = []
        
        # Direct category matching
        category_mapping = {
            'guitar': ['electric-guitars', 'acoustic-guitars', 'bass-guitars'],
            'keyboard': ['keyboards', 'digital-pianos'],
            'drum': ['drums', 'percussion'],
            'microphone': ['microphones'],
            'amp': ['guitar-amps', 'bass-amps'],
            'audio': ['audio-interfaces', 'studio-monitors'],
            'recording': ['microphones', 'audio-interfaces', 'studio-monitors']
        }
        
        # Find products that match topic keywords
        relevant_categories = set()
        for keyword in keywords:
            if keyword in category_mapping:
                relevant_categories.update(category_mapping[keyword])
        
        # Add direct category matches
        for category_slug in relevant_categories:
            if category_slug in self.products_by_category:
                # Take top-rated products from this category
                category_products = self.products_by_category[category_slug][:10]
                relevant_products.extend(category_products)
        
        # Brand-specific matching
        for product in self.all_products[:50]:  # Check top 50 products
            brand_name = product['brand_name'].lower()
            product_name = product['name'].lower()
            
            # Check if brand or product name is mentioned in topic
            if any(keyword in brand_name or keyword in product_name for keyword in keywords):
                if product not in relevant_products:
                    relevant_products.append(product)
        
        # If we don't have enough relevant products, use template-based fallbacks
        if len(relevant_products) < max_products:
            fallback_categories = []
            
            if template_name == 'buying-guide':
                # For buying guides, show popular products from main categories
                fallback_categories = ['electric-guitars', 'keyboards', 'microphones']
            elif template_name == 'review':
                # For reviews, show highly-rated products
                fallback_categories = ['electric-guitars', 'keyboards', 'audio-interfaces']
            elif template_name == 'comparison':
                # For comparisons, show similar products
                fallback_categories = ['electric-guitars', 'keyboards']
            elif template_name == 'artist-spotlight':
                # For artist spotlights, show iconic instruments
                fallback_categories = ['electric-guitars', 'keyboards', 'drums']
            elif template_name == 'instrument-history':
                # For history posts, show classic instruments
                fallback_categories = ['electric-guitars', 'acoustic-guitars', 'keyboards']
            else:
                # General fallback
                fallback_categories = ['electric-guitars', 'keyboards', 'microphones']
            
            for category in fallback_categories:
                if category in self.products_by_category:
                    category_products = self.products_by_category[category][:5]
                    for product in category_products:
                        if product not in relevant_products:
                            relevant_products.append(product)
                            if len(relevant_products) >= max_products:
                                break
                if len(relevant_products) >= max_products:
                    break
        
        # Remove duplicates and limit
        seen_ids = set()
        unique_products = []
        for product in relevant_products:
            if product['id'] not in seen_ids:
                unique_products.append(product)
                seen_ids.add(product['id'])
                if len(unique_products) >= max_products:
                    break
        
        return unique_products
    
    def _format_products_for_prompt(self, products: List[Dict]) -> str:
        """Format products for inclusion in the AI prompt"""
        if not products:
            return ""
        
        product_details = []
        for product in products:
            detail = f"""
Product ID: {product['id']}
Name: {product['brand_name']} {product['name']}
Slug: {product['slug']}
Category: {product['category_name']}
Price: ${product['price']:.0f}
Rating: {product['rating'] or 4.0}/5
Reviews: {product['review_count'] or 0}
Description: {product.get('description', 'High-quality musical instrument')[:100]}...
"""
            product_details.append(detail.strip())
        
        return "\n\n".join(product_details)
    
    async def generate_blog_post(
        self,
        topic: str,
        template_name: str = "buying-guide",
        target_words: int = 4000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a blog post with properly matched products
        """
        
        # Load templates and products if not already loaded
        if not self.templates or not self.all_products:
            await self.initialize()
        
        # Select relevant products for this topic
        relevant_products = self._select_relevant_products(topic, template_name, max_products=5)
        
        print(f"Selected {len(relevant_products)} relevant products for '{topic}':")
        for product in relevant_products:
            print(f"  - {product['brand_name']} {product['name']} (Category: {product['category_name']})")
        
        # Build the generation prompt with specific product data
        prompt = self._build_enhanced_prompt(topic, template_name, relevant_products, target_words)
        
        # Call AI model
        response = self._call_ai_model(prompt)
        
        # Parse and validate response
        try:
            content = json.loads(response)
            return self._validate_and_enhance_content(content, relevant_products)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            raise ValueError("AI response is not valid JSON")
    
    def _build_enhanced_prompt(self, topic: str, template_name: str, products: List[Dict], target_words: int) -> str:
        """Build an enhanced prompt with specific product data"""
        
        # Get base template
        base_template = self.templates.get(template_name, 'Create a comprehensive guide about {topic}.')
        prompt = base_template.format(topic=topic)
        
        # Add specific product information
        product_info = self._format_products_for_prompt(products)
        
        prompt += f"""

TARGET WORD COUNT: {target_words} words (minimum 3000, maximum 5000)

AVAILABLE PRODUCTS (USE THESE SPECIFIC PRODUCTS):
{product_info}

PRODUCT INTEGRATION REQUIREMENTS:
- ONLY use products from the provided list above
- Include product IDs exactly as provided
- Create 2-3 product spotlights using different products from the list
- Reference products naturally throughout the content
- Include specific model names, brands, and features
- For each product spotlight, use the exact Product ID and Slug provided

RESPONSE FORMAT - Return ONLY valid JSON:
{{
  "title": "Engaging title avoiding 'Ultimate Guide' (50-65 chars)",
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
        "id": "EXACT_PRODUCT_ID_FROM_LIST",
        "name": "Exact Brand Name from list",
        "slug": "exact-product-slug",
        "price": "$XXX",
        "rating": 4.5,
        "category": "Product Category",
        "pros": ["Specific feature 1", "Specific feature 2", "Specific feature 3"],
        "cons": ["Minor limitation"],
        "description": "Detailed description of this specific product",
        "affiliate_url": "https://www.getyourmusicgear.com/products/PRODUCT_SLUG?ref=blog&utm_source=blog&utm_campaign=product_spotlight",
        "store_url": "https://www.getyourmusicgear.com/products/PRODUCT_SLUG",
        "cta_text": "See Details on Our Store"
      }}
    }},
    {{
      "type": "content",
      "content": "## Additional Section\\n\\nMore content mentioning other products (800-1200 words)"
    }},
    {{
      "type": "product_spotlight",
      "product": {{
        "id": "DIFFERENT_PRODUCT_ID",
        "name": "Different Product Name",
        "slug": "different-product-slug",
        "price": "$XXX",
        "rating": 4.5,
        "category": "Product Category",
        "pros": ["Feature 1", "Feature 2", "Feature 3"],
        "cons": ["Minor limitation"],
        "description": "Detailed description",
        "affiliate_url": "https://www.getyourmusicgear.com/products/DIFFERENT_SLUG?ref=blog&utm_source=blog&utm_campaign=product_spotlight",
        "store_url": "https://www.getyourmusicgear.com/products/DIFFERENT_SLUG",
        "cta_text": "See Details on Our Store"
      }}
    }},
    {{
      "type": "conclusion",
      "content": "## Final Thoughts\\n\\nSummary and recommendations (300-500 words)"
    }}
  ],
  "tags": ["relevant", "topic", "tags"],
  "category": "{template_name}",
  "featured_products": ["product_id_1", "product_id_2", "product_id_3"]
}}

CRITICAL REQUIREMENTS:
- Use EXACT product IDs, names, and slugs from the provided list
- Create multiple product spotlights with DIFFERENT products
- Write naturally about the specific products provided
- Include detailed product information and features
- Make content engaging and valuable for readers
- Focus on helping readers make informed decisions
- Mention multiple products throughout the content naturally

Topic: {topic}
Template: {template_name}
Target words: {target_words}

Respond with JSON only:"""

        return prompt
    
    def _call_ai_model(self, prompt: str) -> str:
        """Call the AI model to generate content"""
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    messages=[
                        {"role": "system", "content": "You are an expert music journalist and gear reviewer. Always respond with valid JSON only. Focus on the specific products provided."},
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
        
        # Validate product spotlights have correct product data
        for section in content["sections"]:
            if section.get("type") == "product_spotlight" and "product" in section:
                product_data = section["product"]
                
                # Ensure we have the required fields
                required_product_fields = ["id", "name", "slug", "affiliate_url", "store_url"]
                for field in required_product_fields:
                    if field not in product_data:
                        # Try to fix with data from our products list
                        product_id = product_data.get("id")
                        if product_id:
                            matching_product = next((p for p in products if str(p['id']) == str(product_id)), None)
                            if matching_product:
                                product_data["name"] = f"{matching_product['brand_name']} {matching_product['name']}"
                                product_data["slug"] = matching_product['slug']
                                product_data["affiliate_url"] = f"https://www.getyourmusicgear.com/products/{matching_product['slug']}?ref=blog&utm_source=blog&utm_campaign=product_spotlight"
                                product_data["store_url"] = f"https://www.getyourmusicgear.com/products/{matching_product['slug']}"
                                product_data["category"] = matching_product['category_name']
                                product_data["rating"] = 4.0  # Default rating for display
                                product_data["price"] = f"${matching_product['price']:.0f}" if matching_product['price'] else "Check Price"
        
        # Add metadata
        content["generated_at"] = datetime.now().isoformat()
        content["word_count"] = self._estimate_word_count(content)
        content["generation_method"] = "improved_product_matching"
        
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

# Example usage and testing
async def test_improved_generator():
    """Test the improved blog generator"""
    generator = ImprovedBlogGenerator()
    await generator.initialize()
    
    # Test with different topics
    test_topics = [
        ("AKAI MPK Mini MK3 Review: Compact MIDI Powerhouse", "review"),
        ("Best Electric Guitars Under $500: Buyer's Guide", "buying-guide"),
        ("Yamaha vs Roland Digital Pianos: Complete Comparison", "comparison"),
        ("Jimi Hendrix: The Guitar Legend and His Gear", "artist-spotlight"),
        ("The Evolution of the Electric Guitar", "instrument-history")
    ]
    
    for topic, template in test_topics:
        print(f"\n{'='*60}")
        print(f"Testing: {topic} ({template})")
        print('='*60)
        
        try:
            result = await generator.generate_blog_post(topic, template)
            print(f"✅ Generated blog post: {result['title']}")
            print(f"   Word count: {result['word_count']}")
            print(f"   Featured products: {result['featured_products']}")
            
            # Show product spotlights
            for section in result['sections']:
                if section.get('type') == 'product_spotlight':
                    product = section.get('product', {})
                    print(f"   Product spotlight: {product.get('name', 'Unknown')} (ID: {product.get('id', 'N/A')})")
                    
        except Exception as e:
            print(f"❌ Error generating blog post: {e}")

if __name__ == "__main__":
    asyncio.run(test_improved_generator())
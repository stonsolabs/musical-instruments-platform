#!/usr/bin/env python3
"""
Simplified Blog Batch Generator Service
Generates blog batches using the new simplified JSON structure and templates
"""

import asyncio
import json
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import async_session_factory

class SimpleBlogBatchGenerator:
    def __init__(self):
        self.templates = []
        self.products = []
        self.blog_ideas = []
    
    async def initialize(self):
        """Initialize the service by loading all required data"""
        async with async_session_factory() as session:
            await self._load_templates(session)
            await self._load_products(session)
            self._generate_blog_ideas()
    
    async def _load_templates(self, session: AsyncSession):
        """Load blog templates from simplified table"""
        result = await session.execute(text('''
            SELECT id, name, prompt, structure
            FROM blog_templates 
            ORDER BY name
        '''))
        self.templates = [dict(row._mapping) for row in result.fetchall()]
    
    async def _load_products(self, session: AsyncSession):
        """Load quality products from database for blog content"""
        query = """
        SELECT DISTINCT
            p.id,
            p.name,
            p.slug,
            p.avg_rating as rating,
            COALESCE(p.msrp_price, 0) as price,
            b.name as brand_name,
            c.name as category_name,
            c.slug as category_slug
        FROM products p
        JOIN brands b ON p.brand_id = b.id
        JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = true
        AND b.name != 'Unknown Brand'
        AND p.name IS NOT NULL
        AND p.name != ''
        ORDER BY p.avg_rating DESC NULLS LAST, p.name
        LIMIT 300
        """
        result = await session.execute(text(query))
        self.products = [dict(row._mapping) for row in result.fetchall()]
        print(f"Loaded {len(self.products)} available products")
    
    def _generate_blog_ideas(self):
        """Generate diverse blog post ideas using templates and products"""
        ideas = []
        
        # Template-based ideas
        for template in self.templates:
            template_name = template['name']
            
            if template_name == 'buying-guide':
                ideas.extend([
                    f"Acoustic Guitars Under $500: Your Complete Buying Roadmap",
                    f"Electric Guitar Shopping: A Beginner's Smart Approach",
                    f"Recording Bass Guitars: Essential Gear Selection Guide",
                    f"Digital vs Acoustic Keyboards: Making the Right Choice",
                    f"Compact Drum Sets: Perfect Solutions for Limited Space",
                    f"Home Studio Microphones: Professional Sound on Any Budget",
                    f"Guitar Amplifiers Under $300: Power Without Breaking the Bank",
                    f"Audio Interface Selection: Your Gateway to Professional Recording",
                    f"Violin Shopping Made Simple: Quality Instruments for Every Level",
                    f"DJ Equipment Essentials: Building Your First Professional Setup",
                    f"Studio Monitor Selection: Accurate Sound for Home Producers",
                    f"MIDI Controller Guide: Choosing Your Creative Command Center"
                ])
                
            elif template_name == 'review':
                # Create diverse review topics for top-rated products
                top_products = sorted(self.products, key=lambda x: x['rating'] or 0, reverse=True)[:15]
                review_formats = [
                    "Inside Look: {}",
                    "{}: Worth the Hype?", 
                    "Real World Test: {}",
                    "{}: Honest User Experience",
                    "Breaking Down the {}",
                    "{}: What They Don't Tell You",
                    "Living With the {}: 6-Month Review",
                    "{}: Game Changer or Marketing?",
                    "Unboxing Truth: {}",
                    "{}: Professional vs Amateur Perspective"
                ]
                
                for i, product in enumerate(top_products):
                    format_choice = review_formats[i % len(review_formats)]
                    product_name = f"{product['brand_name']} {product['name']}"
                    ideas.append(format_choice.format(product_name))
                    
            elif template_name == 'comparison':
                ideas.extend([
                    f"Fender vs Gibson: The Legendary Guitar Rivalry Decoded",
                    f"Acoustic vs Electric Drums: Sound, Space, and Style Considerations",
                    f"Yamaha vs Kawai Digital Pianos: Touch, Tone, and Technology",
                    f"SM57 vs SM58: Microphone Legends in Different Arenas",
                    f"Martin vs Taylor: Acoustic Guitar Philosophy and Sound",
                    f"Audio-Technica vs Shure: Dynamic Microphone Face-Off",
                    f"Active vs Passive Bass Pickups: Tone Shaping Showdown",
                    f"Tube vs Solid State Amps: The Great Guitar Tone Debate",
                    f"Condenser vs Dynamic Mics: Studio Recording Solutions",
                    f"In-Ear vs Over-Ear Monitors: Professional Audio Choices"
                ])
                
            elif template_name == 'artist-spotlight':
                ideas.extend([
                    f"Jimi Hendrix: Redefining Electric Guitar Forever",
                    f"Ozzy Osbourne's Sonic Arsenal: Heavy Metal's Dark Prince",
                    f"BB King and Lucille: A Blues Love Story",
                    f"John Bonham: Drumming Power That Shook the World",
                    f"Geddy Lee's Triple Threat: Bass, Keys, and Vocals",
                    f"Keith Moon: Chaos and Brilliance Behind the Kit",
                    f"Prince's Purple Rain Setup: Innovation in Every Note",
                    f"Eddie Van Halen: The Tapping Revolution",
                    f"Stevie Ray Vaughan's Texas Blues Fire",
                    f"Les Claypool: Bass Playing Outside the Box",
                    f"Neil Peart: The Professor of Progressive Drumming",
                    f"Tori Amos: Piano Powerhouse and Unconventional Genius"
                ])
                
            elif template_name == 'instrument-history':
                ideas.extend([
                    f"The Evolution of the Electric Guitar",
                    f"Gibson SG: A Rock and Roll Icon's History",
                    f"Fender Telecaster: The First Electric Guitar",
                    f"The History of the Modern Drum Kit",
                    f"Piano Evolution: From Acoustic to Digital",
                    f"The Rise of the Electric Bass Guitar"
                ])
                
            elif template_name == 'gear-tips':
                ideas.extend([
                    f"Guitar Maintenance Secrets: Keeping Your Instrument Stage-Ready",
                    f"Budget Studio Magic: Professional Recording Without Breaking Bank",
                    f"Small Venue Sound: Making Every Performance Count",
                    f"EQ Mastery: Sculpting Your Perfect Guitar Tone",
                    f"Drum Tuning Decoded: From Bedroom to Stadium Sound",
                    f"Microphone Placement Psychology: Capturing the Perfect Performance",
                    f"Cable Management Strategies for Live Musicians",
                    f"Pedal Chain Optimization: Signal Flow for Maximum Impact",
                    f"Temperature and Humidity: Protecting Your Instruments",
                    f"Touring Musician's Survival Kit: Essential Gear Maintenance"
                ])
                
            elif template_name == 'news-feature':
                ideas.extend([
                    f"Affordable Excellence: How Budget Instruments Got Professional",
                    f"Streaming Revolution: Redefining Music Production Standards",
                    f"Vinyl's Unexpected Comeback: Why Analog Still Matters",
                    f"AI Meets Music: Creativity Enhancement or Creative Threat?",
                    f"Pandemic's Silver Lining: Home Studio Revolution",
                    f"Green Music: Sustainable Instrument Manufacturing Takes Center Stage",
                    f"Bedroom Producers Going Global: The New Music Economy",
                    f"Virtual Reality Concerts: The Future of Live Performance?",
                    f"NFTs and Music: Digital Ownership Revolution",
                    f"5G Technology: Transforming Remote Collaboration in Music"
                ])
        
        # Shuffle and store
        random.shuffle(ideas)
        self.blog_ideas = ideas
        print(f"Generated {len(ideas)} blog post ideas")
    
    async def generate_batch_requests(self, 
                                    num_posts: int = 50,
                                    output_file: Optional[str] = None,
                                    word_count_range: tuple = (3000, 5000),
                                    template_distribution: Optional[Dict[str, float]] = None) -> List[Dict]:
        """
        Generate batch requests for OpenAI batch API
        
        Args:
            num_posts: Number of blog posts to generate
            output_file: Output JSONL file path
            word_count_range: Min and max word count (default 3000-5000)
            template_distribution: Custom template distribution (optional)
        """
        
        if not self.templates:
            await self.initialize()
        
        # Default template distribution (more balanced across all types)
        if not template_distribution:
            template_distribution = {
                'buying-guide': 0.25,
                'review': 0.20,
                'comparison': 0.15,
                'instrument-history': 0.15,
                'artist-spotlight': 0.15,
                'gear-tips': 0.07,
                'news-feature': 0.03
            }
        
        requests = []
        used_ideas = set()
        template_counts = {name: 0 for name in template_distribution.keys()}
        
        for i in range(num_posts):
            # Select template based on distribution
            template = self._select_template_by_distribution(template_distribution)
            template_counts[template['name']] += 1
            
            # Select unique topic
            topic = self._select_unique_topic(template['name'], used_ideas)
            used_ideas.add(topic)
            
            # Select relevant products
            products = self._select_relevant_products(template['name'], topic)
            
            # Generate target word count
            target_words = random.randint(word_count_range[0], word_count_range[1])
            
            # Build request
            request = self._build_generation_request(
                custom_id=f"blog_post_{i+1:03d}",
                topic=topic,
                template=template,
                products=products,
                target_words=target_words
            )
            
            requests.append(request)
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                for request in requests:
                    f.write(json.dumps(request) + '\n')
            print(f"Saved {len(requests)} requests to {output_file}")
            
            # Print actual template distribution
            print(f"\n📊 Actual template distribution:")
            for template_name, count in template_counts.items():
                percentage = (count / num_posts) * 100
                print(f"  {template_name}: {count} ({percentage:.1f}%)")
        
        return requests
    
    def _select_template_by_distribution(self, distribution: Dict[str, float]) -> Dict:
        """Select template based on probability distribution"""
        # Normalize distribution to ensure it sums to 1.0
        total = sum(distribution.values())
        normalized_dist = {k: v/total for k, v in distribution.items()}
        
        rand = random.random()
        cumulative = 0
        
        for template_name, probability in normalized_dist.items():
            cumulative += probability
            if rand <= cumulative:
                for template in self.templates:
                    if template['name'] == template_name:
                        return template
        
        # Fallback to random template if distribution fails
        return random.choice(self.templates)
    
    def _select_unique_topic(self, template_name: str, used_ideas: set) -> str:
        """Select a unique topic for the given template"""
        available_ideas = [idea for idea in self.blog_ideas if idea not in used_ideas]
        
        if not available_ideas:
            # Generate fallback topic
            return f"Ultimate Guide to {template_name.replace('-', ' ').title()} - {datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Try to find template-appropriate topics first
        template_keywords = {
            'buying-guide': ['buying', 'guide', 'best', 'under'],
            'review': ['review'],
            'comparison': ['vs', 'compared', 'showdown'],
            'artist-spotlight': ['celebrating', 'spotlight'],
            'instrument-history': ['history', 'evolution'],
            'gear-tips': ['tips', 'maintenance', 'setup'],
            'news-feature': ['rise', 'impact', 'how']
        }
        
        keywords = template_keywords.get(template_name, [])
        
        # First try to find topic matching template
        for idea in available_ideas:
            if any(keyword.lower() in idea.lower() for keyword in keywords):
                return idea
        
        # Otherwise return random available idea
        return random.choice(available_ideas)
    
    def _select_relevant_products(self, template_name: str, topic: str, max_products: int = 5) -> List[Dict]:
        """Select products relevant to the topic with smart fallbacks"""
        relevant_products = []
        
        # Extract keywords from topic
        topic_lower = topic.lower()
        
        # Enhanced keyword matching with category mapping
        product_keywords = {
            'guitar': ['electric-guitars', 'acoustic-guitars', 'guitar-amps'],
            'bass': ['bass-guitars', 'bass-amps'],
            'drum': ['drums', 'percussion'],
            'keyboard': ['keyboards', 'digital-pianos'],
            'piano': ['keyboards', 'digital-pianos', 'acoustic-pianos'],
            'microphone': ['microphones', 'recording'],
            'amp': ['guitar-amps', 'bass-amps'],
            'recording': ['microphones', 'audio-interfaces', 'studio-monitors'],
            'vintage': ['electric-guitars', 'acoustic-guitars', 'guitar-amps'],
            'rock': ['electric-guitars', 'guitar-amps', 'drums'],
            'blues': ['electric-guitars', 'harmonicas', 'guitar-amps'],
            'jazz': ['acoustic-guitars', 'keyboards', 'brass'],
            'classical': ['acoustic-guitars', 'keyboards', 'violins']
        }
        
        # Find direct keyword matches
        matched_categories = set()
        for keyword, categories in product_keywords.items():
            if keyword in topic_lower:
                matched_categories.update(categories)
        
        # Find products matching topic keywords or categories
        for product in self.products:
            product_text = f"{product['name']} {product['brand_name']} {product['category_name']}".lower()
            category_slug = product.get('category_slug', '').lower()
            
            # Direct keyword match
            topic_match = any(keyword in product_text for keyword in product_keywords.keys() if keyword in topic_lower)
            # Category match
            category_match = category_slug in matched_categories
            
            if topic_match or category_match:
                relevant_products.append({
                    'id': str(product['id']),
                    'name': f"{product['brand_name']} {product['name']}",
                    'price': f"${product['price']:.0f}" if product['price'] else "Check Price",
                    'category': product['category_name'],
                    'rating': product['rating'] or 4.0
                })
        
        # If no specific matches, use strategic fallbacks based on template type
        if not relevant_products:
            top_products = sorted(self.products, key=lambda x: x['rating'] or 0, reverse=True)
            
            # Template-specific fallbacks
            if template_name == 'artist-spotlight':
                # For artist posts, show iconic instruments (guitars, keyboards, drums)
                preferred_categories = ['electric-guitars', 'acoustic-guitars', 'keyboards', 'drums']
                fallback_products = [p for p in top_products if p.get('category_slug') in preferred_categories]
            elif template_name == 'instrument-history':
                # For history posts, show classic instruments
                preferred_categories = ['electric-guitars', 'acoustic-guitars', 'keyboards', 'drums']
                fallback_products = [p for p in top_products if p.get('category_slug') in preferred_categories]
            elif template_name == 'news-feature':
                # For news, show trending/popular products
                fallback_products = top_products[:15]  # Top rated across all categories
            else:
                # General fallback - mix of popular instruments
                fallback_products = top_products[:20]
            
            if not fallback_products:
                fallback_products = top_products[:20]
            
            relevant_products = [{
                'id': str(p['id']),
                'name': f"{p['brand_name']} {p['name']}",
                'price': f"${p['price']:.0f}" if p['price'] else "Check Price",
                'category': p['category_name'],
                'rating': p['rating'] or 4.0
            } for p in random.sample(fallback_products, min(max_products, len(fallback_products)))]
        
        return relevant_products[:max_products]
    
    def _build_generation_request(self, custom_id: str, topic: str, template: Dict, 
                                products: List[Dict], target_words: int) -> Dict:
        """Build OpenAI batch API request"""
        
        # Build the simplified prompt
        prompt = f"""
Create a comprehensive {template['name'].replace('-', ' ')} about "{topic}".

CRITICAL REQUIREMENTS:
- Target word count: {target_words} words (minimum 3000, maximum 5000)
- Write in an engaging, expert tone
- Include natural product recommendations with affiliate integration
- Make content evergreen (no specific years unless essential)
- Focus on providing genuine value to readers
- ENFORCE JSON OUTPUT FORMAT - respond ONLY with valid JSON

CONTENT DIVERSITY REQUIREMENTS:
- Write like a seasoned musician talking to a friend, not a robot
- Use conversational, human tone with personality and humor when appropriate
- Mix short punchy sentences with longer explanations. Vary rhythm.
- Include personal anecdotes, band stories, studio experiences, real-world scenarios
- Start with hooks: "Here's what nobody tells you...", "I learned this the hard way...", "After 15 years of playing..."
- Use contractions, colloquialisms, and natural speech patterns
- Include specific brand mentions, model numbers, and technical details from experience
- Reference real artists, songs, and musical contexts that resonate
- Avoid corporate speak, buzzwords, and AI-generated phrases

TITLE CREATIVITY GUIDELINES:
- ABSOLUTELY AVOID these overused phrases: "Ultimate Guide", "Best", "Top", "Complete Guide", "Everything You Need"
- Use UNIQUE angles: storytelling, emotional hooks, contrarian viewpoints, personal experiences
- Consider formats: "Why X Changed Everything", "The Hidden Truth About X", "X Nobody Talks About"  
- Use numbers creatively: "3 Secrets", "The 15-Minute Solution", "7 Signs You Need"
- Ask compelling questions: "Is Your Guitar Holding You Back?", "What If Everything You Know About X is Wrong?"
- Use power words: Revolutionary, Decoded, Unveiled, Transformed, Breakthrough, Inside Story
- Match the template's voice: buying guides = practical, reviews = honest, artist spotlights = inspiring
- Each title should feel like it was written by a different person with a unique perspective

RESPONSE FORMAT:
Respond ONLY with a valid JSON object in this exact structure:

{{
  "title": "Creative, engaging title that avoids generic phrases (50-65 chars)",
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
  "category": "{template['name']}",
  "featured_products": ["product_id1", "product_id2"]
}}

CONTENT GUIDELINES:
- Write comprehensive, detailed sections that reach the target word count
- Use proper markdown formatting (##, ###, -, *, etc.)
- Include specific details, specs, and examples
- Add personal insights and expert knowledge
- Use lists, quotes, and structured content for readability
- Integrate products naturally within the content flow
- Focus on helping readers make informed decisions
- Include relevant anecdotes and stories

"""

        # Add product context if available
        if products:
            product_context = "\n\nAVAILABLE PRODUCTS TO REFERENCE:\n"
            for product in products:
                product_context += f"- {product['name']} (ID: {product['id']}) - {product['price']} - {product['category']}\n"
            
            # Add guidance for non-product topics
            if any(keyword in topic.lower() for keyword in ['history', 'evolution', 'biography', 'story', 'news', 'theory']):
                product_context += """\n
PRODUCT INTEGRATION GUIDANCE FOR NON-PRODUCT TOPICS:
- ONLY recommend products that exist in our database (from the provided product list)
- Use natural language like "I've been playing the [Product Name] for years and..."
- Include specific model numbers and technical specs from our database
- Connect products naturally: "When I'm recording country licks, I reach for my [Product]..."
- Create product spotlights within sections, not as separate blocks
- Use affiliate buttons strategically - 2-3 per article maximum
- Reference products by their exact database names and specifications
- For each product mention, create a product_spotlight section with full details
"""
            
            prompt += product_context

        prompt += f"\n\nTopic: {topic}\nTarget words: {target_words}\n\nRespond with JSON only:"

        return {
            "custom_id": custom_id,
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4.1",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert music journalist and gear reviewer. Always respond with valid JSON only. Never include any text outside the JSON structure."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 8000,
                "temperature": 0.7
            }
        }
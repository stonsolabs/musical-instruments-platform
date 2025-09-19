#!/usr/bin/env python3
"""
Blog Batch Generator Service - Production-ready service for generating blog batches
Handles large-scale blog generation with configurable parameters
"""

import asyncio
import json
import csv
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import async_session_factory

class BlogBatchGeneratorService:
    def __init__(self):
        self.templates = []
        self.products = []
        self.authors = []
        self.blog_ideas = []
    
    async def initialize(self):
        """Initialize the service by loading all required data"""
        async with async_session_factory() as session:
            await self._load_templates(session)
            await self._load_authors(session)
            await self._load_products(session)  # Now async and filtered
            self._generate_blog_ideas()
    
    async def _load_templates(self, session: AsyncSession):
        """Load active blog generation templates"""
        result = await session.execute(text('''
            SELECT id, name, template_type, base_prompt, system_prompt, product_context_prompt
            FROM blog_generation_templates 
            WHERE is_active = true 
            ORDER BY template_type, name
        '''))
        self.templates = result.fetchall()
    
    async def _load_authors(self, session: AsyncSession):
        """Load authors from the database"""
        result = await session.execute(text('SELECT id, name, email FROM authors WHERE is_active = true ORDER BY id'))
        self.authors = result.fetchall()
    
    async def _load_products(self, session: AsyncSession):
        """Load ONLY AVAILABLE products from database"""
        query = """
        SELECT p.id, p.name, p.slug, p.category_id, p.brand_id, p.avg_rating, 
               p.review_count, b.name as brand_name,
               c.name as category_name, c.slug as category_slug
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = true AND (
            EXISTS(
                SELECT 1 FROM product_prices pp 
                WHERE pp.product_id = p.id AND pp.is_available = true
            ) OR 
            (p.content::text LIKE '%store_links%' 
             AND jsonb_path_exists(p.content, '$.store_links ? (@.size() > 0)')) OR
            (p.content::text LIKE '%thomann_info%' 
             AND p.content->>'thomann_info' IS NOT NULL)
        )
        ORDER BY p.avg_rating DESC NULLS LAST, p.review_count DESC
        """
        
        result = await session.execute(text(query))
        self.products = [dict(row._mapping) for row in result.fetchall()]
        print(f"✅ Loaded {len(self.products)} available products for blog generation")
    
    def _generate_blog_ideas(self):
        """Generate comprehensive blog post ideas"""
        # Simplified, focused blog ideas based on Guitar World style
        self.blog_ideas = [
            # Practical Buying Guides
            {"title": "Best Beginner Electric Guitars That Won't Break the Bank", "template": "buying_guide", "category": "31", "focus": "beginner guitars"},
            {"title": "Your First Bass Guitar: What Actually Matters", "template": "buying_guide", "category": "10", "focus": "bass guitars"},
            {"title": "Acoustic Guitars Under $500: Hidden Gems Worth Your Money", "template": "buying_guide", "category": "31", "focus": "budget acoustic"},
            {"title": "Home Practice Amps: From Whisper Quiet to Neighbor-Friendly", "template": "buying_guide", "category": "31", "focus": "practice amps"},
            {"title": "Piano vs Keyboard: Making the Right Choice for Your Space", "template": "buying_guide", "category": "0", "focus": "piano vs keyboard"},
            {"title": "Guitar Setup Guide: From Action to Intonation", "template": "buying_guide", "category": "31", "focus": "guitar setup"},
            {"title": "Bass String Gauges Explained: Find Your Perfect Tension", "template": "buying_guide", "category": "10", "focus": "bass strings"},
            {"title": "Guitar Effects Pedals: Building Your First Pedalboard", "template": "buying_guide", "category": "31", "focus": "effects pedals"},
            {"title": "Acoustic Guitar Maintenance: Keep Your Guitar Sounding Great", "template": "buying_guide", "category": "31", "focus": "guitar maintenance"},
            {"title": "Bass Amp Settings: From Clean to Crunch", "template": "buying_guide", "category": "10", "focus": "bass amp settings"},
            {"title": "Left-Handed Guitar Guide: Finding Your Perfect Match", "template": "buying_guide", "category": "31", "focus": "left-handed guitars"},
            {"title": "Short Scale Bass Guitars: Comfort Meets Tone", "template": "buying_guide", "category": "10", "focus": "short scale bass"},
            {"title": "Baritone Guitars: The Deep End of Six Strings", "template": "buying_guide", "category": "31", "focus": "baritone guitars"},
            {"title": "7-String Guitars: Expanding Your Musical Horizons", "template": "buying_guide", "category": "31", "focus": "7-string guitars"},
            {"title": "Fretless Bass: The Smooth Sound of Expression", "template": "buying_guide", "category": "10", "focus": "fretless bass"},
            {"title": "Home Recording Setup: From Bedroom to Studio", "template": "buying_guide", "category": "0", "focus": "home recording"},
            {"title": "Essential Guitar Accessories: What You Really Need", "template": "buying_guide", "category": "31", "focus": "guitar accessories"},
            {"title": "Bass Guitar Accessories: Complete Your Setup", "template": "buying_guide", "category": "10", "focus": "bass accessories"},
            {"title": "Guitar Cases and Gig Bags: Protect Your Investment", "template": "buying_guide", "category": "31", "focus": "guitar cases"},
            {"title": "Cables and Connectors: The Unsung Heroes of Your Rig", "template": "buying_guide", "category": "0", "focus": "cables"},
            {"title": "Guitar Stands and Hangers: Display and Store Safely", "template": "buying_guide", "category": "31", "focus": "guitar stands"},
            {"title": "Guitar Techniques Every Beginner Should Master", "template": "buying_guide", "category": "31", "focus": "guitar techniques"},
            {"title": "Bass Playing Fundamentals: From Fingers to Slap", "template": "buying_guide", "category": "10", "focus": "bass techniques"},
            {"title": "Acoustic Guitar Fingerpicking: Start Your Journey", "template": "buying_guide", "category": "31", "focus": "fingerpicking"},
            {"title": "Electric Guitar Soloing: Build Your Lead Skills", "template": "buying_guide", "category": "31", "focus": "guitar soloing"},
            {"title": "Bass Groove Creation: Find Your Pocket", "template": "buying_guide", "category": "10", "focus": "bass grooves"},
            
            # Comparisons
            {"title": "Fender vs Gibson: The Ultimate Guitar Brand Showdown", "template": "comparison", "category": "31", "focus": "brand comparison"},
            {"title": "Electric vs Acoustic Guitar: Which is Right for You?", "template": "comparison", "category": "31", "focus": "electric vs acoustic"},
            {"title": "Tube vs Solid State Amps: Battle of the Titans", "template": "comparison", "category": "31", "focus": "amp types"},
            {"title": "4-String vs 5-String Bass: Which Bass is Best for You?", "template": "comparison", "category": "10", "focus": "bass strings"},
            {"title": "Classical vs Steel String Acoustic: The Great Debate", "template": "comparison", "category": "31", "focus": "acoustic types"},
            {"title": "Single Coil vs Humbucker Pickups: The Eternal Debate", "template": "comparison", "category": "31", "focus": "pickup types"},
            {"title": "Maple vs Rosewood Fingerboards: Tone and Feel", "template": "comparison", "category": "31", "focus": "fingerboard woods"},
            {"title": "Active vs Passive Bass Pickups: Power and Control", "template": "comparison", "category": "10", "focus": "bass pickups"},
            {"title": "Nylon vs Steel Strings: Classical vs Modern", "template": "comparison", "category": "31", "focus": "string types"},
            {"title": "Solid Body vs Semi-Hollow: Finding Your Sound", "template": "comparison", "category": "31", "focus": "body types"},
            
            # Reviews
            {"title": "Harley Benton Delta Blues T Review: Budget Telecaster Excellence", "template": "review", "category": "31", "focus": "harley benton"},
            {"title": "Steinberger Spirit XT-2 Bass Review: Headless Innovation", "template": "review", "category": "10", "focus": "steinberger bass"},
            {"title": "Traveler Guitar Pro Series Mod X Review: Portable Perfection", "template": "review", "category": "31", "focus": "travel guitar"},
            {"title": "Höfner Shorty Violin Guitar Review: Unique Design, Unique Sound", "template": "review", "category": "0", "focus": "hofner violin"},
            {"title": "Journey Instruments OT990BL Review: Travel-Ready T-Style", "template": "review", "category": "31", "focus": "journey instruments"},
            {"title": "Harley Benton Guitars: European Quality at Unbeatable Prices", "template": "review", "category": "31", "focus": "harley benton brand"},
            {"title": "Steinberger Innovation: The Future of Guitar Design", "template": "review", "category": "31", "focus": "steinberger innovation"},
            {"title": "Höfner Heritage: From Beatles to Modern Players", "template": "review", "category": "31", "focus": "hofner heritage"},
            {"title": "Traveler Guitars: Revolutionizing Portable Instruments", "template": "review", "category": "31", "focus": "traveler innovation"},
            {"title": "Journey Instruments: Adventure-Ready Musical Gear", "template": "review", "category": "31", "focus": "journey brand"},
            
            # Artist-Inspired Gear Guides (using review template)
            {"title": "Jimi Hendrix Gear Breakdown: How to Get That Iconic Sound", "template": "review", "category": "31", "focus": "hendrix gear"},
            {"title": "Slash's Guitar Setup: From Appetite to Now", "template": "review", "category": "31", "focus": "slash gear"},
            {"title": "Flea's Bass Rig: Red Hot Chili Peppers Sound Secrets", "template": "review", "category": "10", "focus": "flea bass"},
            {"title": "Eddie Van Halen's Guitar Evolution: From Frankenstein to Now", "template": "review", "category": "31", "focus": "van halen gear"},
            {"title": "John Mayer's Acoustic Setup: The Perfect Fingerpicking Sound", "template": "review", "category": "31", "focus": "mayer acoustic"},
            {"title": "Eric Clapton's Guitar Journey: From Blues to Cream", "template": "review", "category": "31", "focus": "clapton gear"},
            {"title": "Jaco Pastorius Bass Technique: The Revolutionary Approach", "template": "review", "category": "10", "focus": "jaco bass"},
            {"title": "Stevie Ray Vaughan's Tone: The Texas Blues Master", "template": "review", "category": "31", "focus": "srv gear"},
            {"title": "Les Paul's Guitar Legacy: The Man and the Instrument", "template": "review", "category": "31", "focus": "les paul legacy"},
            {"title": "Tony Iommi's Heavy Metal Sound: The Birth of Metal Guitar", "template": "review", "category": "31", "focus": "iommi gear"},
            
            # General/Value Content
            {"title": "Best Budget Guitars Under $300: Hidden Gems Revealed", "template": "general", "category": "31", "focus": "budget guitars"},
            {"title": "Affordable Bass Guitars That Don't Compromise on Quality", "template": "general", "category": "10", "focus": "budget bass"},
            {"title": "Best Value Guitar Amps: Great Sound Without Breaking the Bank", "template": "general", "category": "31", "focus": "budget amps"},
            {"title": "Student Instruments That Actually Sound Professional", "template": "general", "category": "0", "focus": "student instruments"},
            {"title": "Used vs New Guitars: When to Save and When to Splurge", "template": "general", "category": "31", "focus": "used vs new"},
            {"title": "Holiday Gift Guide: Best Musical Instruments for Every Budget", "template": "general", "category": "0", "focus": "gift guide"},
            {"title": "Back to School: Essential Instruments for Music Students", "template": "general", "category": "0", "focus": "student gear"},
            {"title": "Summer Music Festival Gear: What You Need to Know", "template": "general", "category": "31", "focus": "festival gear"},
            {"title": "Travel-Friendly Instruments: Make Music Anywhere", "template": "general", "category": "0", "focus": "travel instruments"},
            {"title": "Black Friday Music Gear Deals: What to Look For", "template": "general", "category": "0", "focus": "black friday deals"},
            {"title": "Cyber Monday Music Gear: Best Online Deals", "template": "general", "category": "0", "focus": "cyber monday deals"},
            {"title": "Christmas Gift Ideas for Musicians: Complete Guide", "template": "general", "category": "0", "focus": "christmas gifts"},
            {"title": "New Year's Resolution: Learning a New Instrument", "template": "general", "category": "0", "focus": "new year learning"},
            {"title": "Spring Cleaning: Organizing Your Music Studio", "template": "general", "category": "0", "focus": "studio organization"},
            {"title": "Summer Music Camp Essentials: What to Pack", "template": "general", "category": "0", "focus": "music camp gear"},
        ]
    
    async def generate_batch(
        self, 
        total_posts: int = 50,
        template_distribution: Optional[Dict[str, int]] = None,
        category_focus: Optional[str] = None,
        custom_ideas: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive blog batch
        
        Args:
            total_posts: Number of blog posts to generate
            template_distribution: Custom distribution of template types
            category_focus: Focus on specific category (e.g., "31" for guitars)
            custom_ideas: Custom blog ideas to use instead of generated ones
        
        Returns:
            Dictionary with batch file path and generation statistics
        """
        
        # Use custom ideas if provided, otherwise use generated ones
        ideas_to_use = custom_ideas if custom_ideas else self.blog_ideas
        
        # Filter ideas by category if specified
        if category_focus:
            ideas_to_use = [idea for idea in ideas_to_use if idea.get("category") == category_focus]
        
        # Apply template distribution if specified
        if template_distribution:
            selected_ideas = []
            for template_type, count in template_distribution.items():
                template_ideas = [idea for idea in ideas_to_use if idea["template"] == template_type]
                
                if count <= len(template_ideas):
                    # We have enough ideas for this template type
                    selected_ideas.extend(random.sample(template_ideas, count))
                else:
                    # We need more ideas than available, create variations
                    selected_ideas.extend(template_ideas)  # Use all available
                    remaining = count - len(template_ideas)
                    
                    # Generate variations for the remaining count
                    if template_ideas:  # Only if we have ideas for this template type
                        for i in range(remaining):
                            base_idea = random.choice(template_ideas)
                            varied_idea = self._create_variation(base_idea, i)
                            selected_ideas.append(varied_idea)
                    else:
                        print(f"⚠️  Warning: No ideas available for template type '{template_type}', skipping {remaining} posts")
        else:
            # Select random ideas, allowing repetition if needed
            if total_posts <= len(ideas_to_use):
                selected_ideas = random.sample(ideas_to_use, total_posts)
            else:
                # If we need more posts than available ideas, expand with variations
                selected_ideas = []
                
                # First, use all available ideas
                selected_ideas.extend(ideas_to_use)
                
                # Then generate additional variations
                remaining_posts = total_posts - len(ideas_to_use)
                for i in range(remaining_posts):
                    base_idea = random.choice(ideas_to_use)
                    # Create a variation with different focus areas
                    varied_idea = base_idea.copy()
                    
                    # Generate variations based on template type
                    if base_idea["template"] == "buying_guide":
                        variations = ["for Beginners", "for Professionals", "for Budget-Conscious Buyers", "for Advanced Players", "for Home Studios"]
                        variation = random.choice(variations)
                        varied_idea["title"] = base_idea["title"].replace(": Complete Guide", f": {variation}")
                        varied_idea["focus"] = f"{base_idea.get('focus', 'general')} {variation.lower()}"
                    elif base_idea["template"] == "comparison":
                        variations = ["Head-to-Head", "Detailed Analysis", "Ultimate Showdown", "In-Depth Review", "Comprehensive Comparison"]
                        variation = random.choice(variations)
                        varied_idea["title"] = base_idea["title"].replace("vs", f"{variation}:")
                    elif base_idea["template"] == "review":
                        variations = ["In-Depth Review", "Expert Analysis", "Comprehensive Review", "Detailed Review", "Professional Review"]
                        variation = random.choice(variations)
                        varied_idea["title"] = base_idea["title"].replace("Review", variation)
                    else:
                        # For general and artist_spotlight, add year-agnostic variations
                        variations = ["Complete Guide", "Expert Tips", "Ultimate Guide", "Professional Guide", "Comprehensive Guide"]
                        variation = random.choice(variations)
                        if "Guide" not in base_idea["title"]:
                            varied_idea["title"] = f"{base_idea['title']}: {variation}"
                    
                    selected_ideas.append(varied_idea)
        
        # Generate batch entries
        batch_entries = []
        for i, idea in enumerate(selected_ideas):
            # Find matching template
            template = None
            for t in self.templates:
                if t[2] == idea["template"]:  # template_type
                    template = t
                    break
            
            if not template:
                print(f"⚠️  Warning: No template found for type '{idea['template']}', skipping idea: {idea['title']}")
                continue
            
            # Get relevant products for this idea
            relevant_products = self._get_relevant_products(idea)
            
            # Create custom ID
            custom_id = f"blog-{idea['template']}-{i+1:04d}"
            
            # Build the complete prompt
            full_prompt = self._build_simple_effective_prompt(template, idea, relevant_products)
            
            # Create batch entry
            batch_entry = {
                "custom_id": custom_id,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4.1",
                    "messages": [
                        {
                            "role": "system",
                            "content": template[4]  # system_prompt
                        },
                        {
                            "role": "user",
                            "content": full_prompt
                        }
                    ],
                    "response_format": {"type": "json_object"},
                    "max_tokens": 32768,
                    "temperature": 0.7,
                    "top_p": 1.0,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0
                }
            }
            
            batch_entries.append(batch_entry)
        
        # Save batch file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blog_batch_{timestamp}.jsonl"
        
        with open(filename, 'w') as f:
            for entry in batch_entries:
                f.write(json.dumps(entry) + '\n')
        
        # Generate statistics
        template_counts = {}
        for entry in batch_entries:
            template_type = entry['custom_id'].split('-')[1]
            template_counts[template_type] = template_counts.get(template_type, 0) + 1
        
        return {
            "filename": filename,
            "total_posts": len(batch_entries),
            "template_distribution": template_counts,
            "authors_available": len(self.authors),
            "products_available": len(self.products),
            "generated_at": datetime.now().isoformat()
        }
    
    def _create_variation(self, base_idea: Dict[str, Any], variation_index: int) -> Dict[str, Any]:
        """Create a variation of a base blog idea"""
        varied_idea = base_idea.copy()
        
        # Generate variations based on template type
        if base_idea["template"] == "buying_guide":
            variations = [
                "for Beginners", "for Professionals", "for Budget-Conscious Buyers", 
                "for Advanced Players", "for Home Studios", "for Live Performance",
                "for Recording", "for Practice", "for Students", "for Experts"
            ]
            variation = variations[variation_index % len(variations)]
            varied_idea["title"] = f"{base_idea['title']}: {variation}"
            varied_idea["focus"] = f"{base_idea.get('focus', 'general')} {variation.lower()}"
            
        elif base_idea["template"] == "comparison":
            variations = [
                "Head-to-Head", "Detailed Analysis", "Ultimate Showdown", 
                "In-Depth Review", "Comprehensive Comparison", "Side-by-Side",
                "Battle Royale", "Expert Comparison", "Detailed Breakdown"
            ]
            variation = variations[variation_index % len(variations)]
            varied_idea["title"] = f"{base_idea['title']} - {variation}"
            
        elif base_idea["template"] == "review":
            variations = [
                "In-Depth Review", "Expert Analysis", "Comprehensive Review", 
                "Detailed Review", "Professional Review", "Real-World Test",
                "Honest Review", "Long-Term Review", "Hands-On Review"
            ]
            variation = variations[variation_index % len(variations)]
            varied_idea["title"] = base_idea["title"].replace("Review", variation)
            
        else:  # general
            variations = [
                "Complete Guide", "Expert Tips", "Ultimate Guide", 
                "Professional Guide", "Comprehensive Guide", "Insider's Guide",
                "Master Guide", "Essential Guide", "Advanced Guide"
            ]
            variation = variations[variation_index % len(variations)]
            if "Guide" not in base_idea["title"]:
                varied_idea["title"] = f"{base_idea['title']}: {variation}"
        
        return varied_idea

    def _get_relevant_products(self, idea: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get relevant AVAILABLE products for a blog idea"""
        relevant_products = []
        
        # Filter products by category if specified
        if idea.get("category"):
            category_id = int(idea["category"]) if idea["category"].isdigit() else None
            if category_id:
                category_products = [p for p in self.products if p.get('category_id') == category_id]
            else:
                category_products = self.products
        else:
            category_products = self.products
        
        # Prioritize highly rated products with reviews
        category_products.sort(key=lambda x: (x.get('avg_rating', 0), x.get('review_count', 0)), reverse=True)
        
        # Get a focused sample of the best available products
        sample_size = min(5, len(category_products))  # Reduced to 5 for simpler posts
        if category_products:
            relevant_products = category_products[:sample_size]  # Take top products instead of random
        
        return relevant_products
    
    def _build_simple_effective_prompt(self, template: tuple, idea: Dict[str, Any], products: List[Dict[str, Any]]) -> str:
        """Build simple, effective prompt focused on available products"""
        
        # Build product context with available products only
        product_context = "AVAILABLE PRODUCTS TO FEATURE:\n"
        for product in products:
            product_context += f"- {product['name']} by {product.get('brand_name', 'Unknown')} (ID: {product['id']})\n"
        
        # Simplified, Guitar World-inspired prompt
        complete_prompt = f"""
Write an engaging blog post about: {idea['title']}

STYLE: Write like Guitar World or Drum Helper - conversational, practical, and passionate about music.

FOCUS: {idea.get('focus', 'general')}

{product_context}

RULES:
- Write for real musicians with real needs
- Only recommend the products listed above (they're confirmed available)
- Use conversational tone with personal insights
- Include practical scenarios: home practice, live gigs, studio recording
- Target 1200-1800 words (not overly long)
- Natural product integration - no forced sales pitches
- Make it genuinely helpful and engaging

JSON FORMAT:
{{
    "title": "Engaging title",
    "excerpt": "Hook that makes musicians want to read",
    "content": "Full markdown content with natural flow",
    "seo_title": "SEO title",
    "seo_description": "Meta description",
    "product_recommendations": [
        {{"product_id": 123, "relevance_score": 0.9, "reasoning": "Why this fits"}}
    ]
}}

Respond with ONLY the JSON."""
        
        return complete_prompt
    
    async def get_generation_stats(self) -> Dict[str, Any]:
        """Get statistics about available data for generation"""
        return {
            "templates_available": len(self.templates),
            "authors_available": len(self.authors),
            "products_available": len(self.products),
            "blog_ideas_available": len(self.blog_ideas),
            "template_types": list(set(t[2] for t in self.templates)),
            "product_categories": list(set(p['category_id'] for p in self.products)),
            "author_specializations": [author[1] for author in self.authors]
        }

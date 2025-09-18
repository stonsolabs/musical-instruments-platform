#!/usr/bin/env python3
"""
Generate blog batch from the curated blog_post_ideas.md document.
This creates strategic, high-value content based on researched topics and verified product IDs.
"""

import asyncio
import sys
import os
import json
import uuid
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

# Curated blog post ideas extracted from blogs_docs/blog_post_ideas.md
STRATEGIC_BLOG_IDEAS = [
    # Electric Guitars - High Traffic Potential
    {
        "title": "Best Electric Guitars for Beginners Under $500",
        "type": "Buying_Guide",
        "template": "Ultimate 2025 Buying Guide",
        "product_ids": [262, 267, 264, 305],
        "category": "Electric Guitars",
        "priority": "high"
    },
    {
        "title": "Gibson Les Paul vs. Epiphone: Is the Premium Worth It?",
        "type": "Comparison", 
        "template": "High-Converting Product Battle",
        "product_ids": [297, 279],
        "category": "Electric Guitars",
        "priority": "high"
    },
    {
        "title": "Fender Stratocaster Buying Guide 2025",
        "type": "Buying_Guide",
        "template": "Ultimate 2025 Buying Guide", 
        "product_ids": [376, 620, 646, 1019],
        "category": "Electric Guitars",
        "priority": "high"
    },
    {
        "title": "ESP LTD vs. Schecter: Metal Guitar Comparison",
        "type": "Comparison",
        "template": "High-Converting Product Battle",
        "product_ids": [274, 276, 363, 366],
        "category": "Electric Guitars",
        "priority": "medium"
    },
    {
        "title": "Best Electric Guitars for Jazz Music",
        "type": "Buying_Guide", 
        "template": "Affiliate Roundup: Best Picks",
        "product_ids": [298, 331, 333, 379],
        "category": "Electric Guitars",
        "priority": "medium"
    },
    {
        "title": "PRS SE vs. Standard: Which Should You Buy?",
        "type": "Comparison",
        "template": "High-Converting Product Battle",
        "product_ids": [269, 280, 286, 421],
        "category": "Electric Guitars", 
        "priority": "medium"
    },
    {
        "title": "Best Left-Handed Electric Guitars Under $1000",
        "type": "Roundup",
        "template": "Affiliate Roundup: Best Picks",
        "product_ids": [263, 308, 428],
        "category": "Electric Guitars",
        "priority": "medium"
    },

    # Synthesizers - Growing Market
    {
        "title": "Best Synthesizers for Beginners 2025", 
        "type": "Buying_Guide",
        "template": "Ultimate 2025 Buying Guide",
        "product_ids": [507, 508, 509, 514, 519, 523],
        "category": "Synthesizers",
        "priority": "high"
    },
    {
        "title": "Arturia PolyBrute vs. Moog Subsequent 37",
        "type": "Comparison",
        "template": "High-Converting Product Battle", 
        "product_ids": [506, 521, 964],
        "category": "Synthesizers",
        "priority": "high"
    },
    {
        "title": "Best Budget Synthesizers Under $500",
        "type": "Buying_Guide",
        "template": "Budget Hero Finder",
        "product_ids": [463, 477, 507, 519, 762],
        "category": "Synthesizers",
        "priority": "high"
    },
    {
        "title": "Best Polyphonic Synthesizers 2025",
        "type": "Roundup", 
        "template": "Affiliate Roundup: Best Picks",
        "product_ids": [506, 521, 964, 975, 1152],
        "category": "Synthesizers",
        "priority": "medium"
    },
    {
        "title": "Analog vs. Digital Synthesizers: Complete Guide",
        "type": "Tutorial",
        "template": "Ultimate 2025 Buying Guide",
        "product_ids": [477, 521, 964, 975, 984],
        "category": "Synthesizers", 
        "priority": "medium"
    },

    # Bass Guitars - Strong Affiliate Category
    {
        "title": "Best Bass Guitars for Beginners 2025",
        "type": "Buying_Guide",
        "template": "Ultimate 2025 Buying Guide",
        "product_ids": [482, 484, 551, 675],
        "category": "Bass Guitars",
        "priority": "high"
    },
    {
        "title": "Fender Precision vs. Jazz Bass: Which Is Right for You?",
        "type": "Comparison",
        "template": "High-Converting Product Battle",
        "product_ids": [309, 374, 381, 502],
        "category": "Bass Guitars",
        "priority": "high"
    },
    {
        "title": "Best 5-String Bass Guitars Under $1500",
        "type": "Roundup",
        "template": "Affiliate Roundup: Best Picks", 
        "product_ids": [314, 335, 343, 380, 414],
        "category": "Bass Guitars",
        "priority": "medium"
    },
    {
        "title": "Marcus Miller Bass Guitar Collection Review",
        "type": "Review",
        "template": "Professional Deep Dive Review",
        "product_ids": [306, 335, 343, 348, 362],
        "category": "Bass Guitars",
        "priority": "medium"
    },
    {
        "title": "Music Man StingRay Bass Complete Guide",
        "type": "Review",
        "template": "Professional Deep Dive Review",
        "product_ids": [314, 505, 559, 701],
        "category": "Bass Guitars",
        "priority": "medium"
    },

    # Digital Pianos - High Value Category
    {
        "title": "Best Digital Pianos for Beginners 2025",
        "type": "Buying_Guide",
        "template": "Ultimate 2025 Buying Guide",
        "product_ids": [589, 697, 722, 746, 747],
        "category": "Digital Pianos",
        "priority": "high"
    },
    {
        "title": "Yamaha Clavinova vs. Kawai CA Series Comparison",
        "type": "Comparison",
        "template": "High-Converting Product Battle",
        "product_ids": [359, 370, 581, 596, 612],
        "category": "Digital Pianos",
        "priority": "high"
    },
    {
        "title": "Casio Privia vs. Yamaha Arius: Budget Digital Piano Battle",
        "type": "Comparison", 
        "template": "High-Converting Product Battle",
        "product_ids": [361, 365, 607, 589, 931],
        "category": "Digital Pianos",
        "priority": "medium"
    },
    {
        "title": "Best Portable Digital Pianos Under $1000",
        "type": "Buying_Guide",
        "template": "Budget Hero Finder",
        "product_ids": [570, 578, 697, 865, 988],
        "category": "Digital Pianos",
        "priority": "medium"
    },
    {
        "title": "Best Digital Pianos with Wooden Keys",
        "type": "Roundup",
        "template": "Affiliate Roundup: Best Picks",
        "product_ids": [370, 581, 596, 630, 704], 
        "category": "Digital Pianos",
        "priority": "medium"
    },

    # Acoustic Guitars - Evergreen Content
    {
        "title": "Best Acoustic Guitars for Beginners Under $300",
        "type": "Buying_Guide",
        "template": "Budget Hero Finder", 
        "product_ids": [155, 190, 199, 208, 217],
        "category": "Acoustic Guitars",
        "priority": "high"
    },
    {
        "title": "Taylor vs. Martin: The Ultimate Acoustic Guitar Comparison", 
        "type": "Comparison",
        "template": "High-Converting Product Battle",
        "product_ids": [186, 197, 232, 455, 541],
        "category": "Acoustic Guitars",
        "priority": "high"
    },
    {
        "title": "Best Travel Acoustic Guitars for Musicians on the Go",
        "type": "Roundup",
        "template": "Affiliate Roundup: Best Picks",
        "product_ids": [38, 46, 61, 75, 103, 115, 137, 157],
        "category": "Acoustic Guitars",
        "priority": "medium"
    },
    {
        "title": "Best 12-String Acoustic Guitars 2025",
        "type": "Buying_Guide",
        "template": "Ultimate 2025 Buying Guide",
        "product_ids": [229, 251, 254, 554, 626],
        "category": "Acoustic Guitars",
        "priority": "medium"
    },

    # MIDI Controllers - Production Focus
    {
        "title": "Best MIDI Controllers for Beginners",
        "type": "Buying_Guide", 
        "template": "Ultimate 2025 Buying Guide",
        "product_ids": [476, 486, 515, 525, 527],
        "category": "MIDI Controllers",
        "priority": "medium"
    },
    {
        "title": "Arturia KeyLab vs. Native Instruments Komplete Kontrol",
        "type": "Comparison",
        "template": "High-Converting Product Battle",
        "product_ids": [488, 489, 520, 526, 756],
        "category": "MIDI Controllers", 
        "priority": "medium"
    },

    # Seasonal/Special Content
    {
        "title": "Best Musical Instrument Gifts for Christmas 2025",
        "type": "Roundup",
        "template": "Deal Alert Generator",
        "product_ids": [155, 262, 527, 589, 697],
        "category": "Seasonal",
        "priority": "high"
    },
    {
        "title": "Back to School: Best Instruments for Students", 
        "type": "Buying_Guide",
        "template": "Budget Hero Finder",
        "product_ids": [155, 190, 262, 482, 589],
        "category": "Seasonal",
        "priority": "medium"
    }
]

async def get_template_data(template_name: str) -> Optional[Dict[str, Any]]:
    """Get template information from database"""
    async with async_session_factory() as session:
        result = await session.execute(
            text("""
                SELECT id, base_prompt, system_prompt, product_context_prompt
                FROM blog_generation_templates 
                WHERE name = :name AND is_active = true
            """),
            {"name": template_name}
        )
        row = result.fetchone()
        if not row:
            print(f"❌ Template not found: {template_name}")
            return None
        
        return {
            "id": row[0],
            "base_prompt": row[1],
            "system_prompt": row[2], 
            "product_context_prompt": row[3]
        }

async def get_products_info(product_ids: List[int]) -> List[Dict[str, Any]]:
    """Get product details for the blog generation"""
    async with async_session_factory() as session:
        if not product_ids:
            return []
        
        placeholders = ",".join([f":id_{i}" for i in range(len(product_ids))])
        params = {f"id_{i}": pid for i, pid in enumerate(product_ids)}
        
        result = await session.execute(
            text(f"""
                SELECT id, name, price, category, short_description
                FROM products 
                WHERE id IN ({placeholders}) AND is_active = true
            """),
            params
        )
        
        products = []
        for row in result.fetchall():
            products.append({
                "id": row[0],
                "name": row[1],
                "price": float(row[3]) if row[3] else 0,
                "category": row[4],
                "description": row[5] or ""
            })
        return products

async def create_batch_request(idea: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a batch request for a blog idea"""
    
    # Get template data
    template_data = await get_template_data(idea["template"])
    if not template_data:
        return None
    
    # Get product information 
    products = await get_products_info(idea["product_ids"])
    if not products:
        print(f"❌ No valid products found for: {idea['title']}")
        return None
    
    # Build product context with real product data
    product_context = f"PRODUCTS TO FEATURE (use these exact product IDs):\n\n"
    for product in products:
        product_context += f"Product ID {product['id']}: {product['name']}\n"
        product_context += f"- Price: ${product['price']:.2f}\n"
        product_context += f"- Category: {product['category']}\n"
        if product['description']:
            product_context += f"- Description: {product['description']}\n"
        product_context += "\n"
    
    # Build comprehensive prompt with category context
    user_prompt = f"""
{template_data['base_prompt'].format(category=idea['category'])}

ARTICLE TITLE: {idea['title']}
CONTENT TYPE: {idea['type']}
TARGET AUDIENCE: Musicians, gear enthusiasts, and potential buyers

{product_context}

{template_data['product_context_prompt']}

CRITICAL REQUIREMENTS:
- Use ONLY the product IDs listed above - never substitute, invent, or reference other products
- Create comprehensive content meeting MINIMUM 2500+ word targets for ALL templates
- NEVER reference products by "Product ID X" in the content - always use product names and features
- ALL product references must be properly structured in the product_showcase sections with exact product_id numbers
- Include proper affiliate CTAs like [🛒 Check Latest Price] throughout
- Focus on solving real buyer problems with specific, actionable advice
- Return COMPLETE structured JSON format with all sections - NEVER truncate
- Include meta field with content_type: "{idea['template'].lower().replace(' ', '_')}"
- Ensure JSON is complete and properly closed with all brackets and braces

CONTENT FOCUS: {idea.get('focus', idea['type'])}
"""

    # Create batch request
    custom_id = f"strategic_{idea['category'].lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}"
    
    return {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/chat/completions", 
        "body": {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": template_data['system_prompt']
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "max_tokens": 16384,
            "temperature": 0.7
        }
    }

async def generate_strategic_batch(batch_size: int = 30):
    """Generate strategic batch based on curated blog ideas"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    batch_name = f"strategic_blog_batch_{timestamp}"
    
    print(f"🚀 Generating strategic blog batch: {batch_name}")
    print(f"📊 Target size: {batch_size} posts")
    print(f"📋 Source: Curated blog_post_ideas.md")
    
    # Prioritize high-value content
    high_priority = [idea for idea in STRATEGIC_BLOG_IDEAS if idea.get('priority') == 'high']
    medium_priority = [idea for idea in STRATEGIC_BLOG_IDEAS if idea.get('priority') == 'medium']
    
    # Select posts strategically
    selected_ideas = []
    
    # Always include all high-priority posts
    selected_ideas.extend(high_priority)
    
    # Fill remaining slots with medium priority
    remaining_slots = batch_size - len(selected_ideas)
    if remaining_slots > 0:
        # Shuffle medium priority and take what we need
        random.shuffle(medium_priority)
        selected_ideas.extend(medium_priority[:remaining_slots])
    
    print(f"\n📈 Content mix:")
    print(f"   High Priority: {len(high_priority)} posts")
    print(f"   Medium Priority: {min(remaining_slots, len(medium_priority))} posts") 
    print(f"   Total Selected: {len(selected_ideas)} posts")
    
    # Generate batch requests
    batch_requests = []
    
    for i, idea in enumerate(selected_ideas):
        print(f"\n📝 Creating request {i+1}: {idea['title']}")
        
        request = await create_batch_request(idea)
        if request:
            batch_requests.append(request)
            print(f"   ✅ Template: {idea['template']}")
            print(f"   ✅ Products: {len(idea['product_ids'])}")
            print(f"   ✅ Priority: {idea['priority']}")
        else:
            print(f"   ❌ Failed to create request")
    
    if not batch_requests:
        print("❌ No valid requests generated!")
        return
    
    # Save batch file
    batch_filename = f"/Users/felipe/pprojects/musical-instruments-platform/{batch_name}.jsonl"
    metadata_filename = f"/Users/felipe/pprojects/musical-instruments-platform/{batch_name}_metadata.json"
    
    # Write batch requests (JSONL format)
    with open(batch_filename, 'w') as f:
        for request in batch_requests:
            f.write(json.dumps(request) + '\n')
    
    # Create metadata for tracking
    metadata = {
        "batch_name": batch_name,
        "created_at": datetime.now().isoformat(),
        "total_requests": len(batch_requests),
        "source": "blog_post_ideas.md",
        "strategy": "curated_high_value_content",
        "content_breakdown": {
            "high_priority": len([idea for idea in selected_ideas if idea.get('priority') == 'high']),
            "medium_priority": len([idea for idea in selected_ideas if idea.get('priority') == 'medium'])
        },
        "template_usage": {},
        "category_breakdown": {}
    }
    
    # Add breakdowns
    for idea in selected_ideas:
        template = idea["template"] 
        category = idea["category"]
        
        metadata["template_usage"][template] = metadata["template_usage"].get(template, 0) + 1
        metadata["category_breakdown"][category] = metadata["category_breakdown"].get(category, 0) + 1
    
    with open(metadata_filename, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n🎉 Strategic batch generated successfully!")
    print(f"📁 Batch file: {batch_filename}")
    print(f"📁 Metadata: {metadata_filename}")
    print(f"📊 Total requests: {len(batch_requests)}")
    
    # Show breakdown
    print(f"\n📋 Template breakdown:")
    for template, count in metadata["template_usage"].items():
        print(f"   • {template}: {count} posts")
    
    print(f"\n📂 Category breakdown:")
    for category, count in metadata["category_breakdown"].items():
        print(f"   • {category}: {count} posts")
    
    print(f"\n⚡ Next steps:")
    print(f"   1. Upload {batch_filename} to Azure OpenAI")
    print(f"   2. Start batch processing") 
    print(f"   3. Process results with fixed script")
    print(f"   4. Review high-value content quality")
    
    return batch_filename, metadata_filename

async def main():
    """Main execution function"""
    try:
        batch_size = 30  # Strategic batch size
        await generate_strategic_batch(batch_size)
    except Exception as e:
        print(f"💥 Error generating strategic batch: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
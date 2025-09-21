#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.improved_blog_generator import ImprovedBlogGenerator

async def test_improved_generator():
    """Test the improved blog generator"""
    generator = ImprovedBlogGenerator()
    await generator.initialize()
    
    # Test with AKAI topic to see if we get AKAI products instead of Harley Benton
    topic = "AKAI MPK Mini MK3 Review: Compact MIDI Powerhouse"
    template = "review"
    
    print(f"Testing: {topic}")
    print('='*60)
    
    try:
        result = await generator.generate_blog_post(topic, template)
        print(f"✅ Generated blog post: {result['title']}")
        print(f"   Word count: {result['word_count']}")
        print(f"   Featured products: {result['featured_products']}")
        
        # Show product spotlights
        for i, section in enumerate(result['sections']):
            if section.get('type') == 'product_spotlight':
                product = section.get('product', {})
                print(f"   Product spotlight {i}: {product.get('name', 'Unknown')} (ID: {product.get('id', 'N/A')})")
                print(f"     Category: {product.get('category', 'N/A')}")
                print(f"     Slug: {product.get('slug', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error generating blog post: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_improved_generator())
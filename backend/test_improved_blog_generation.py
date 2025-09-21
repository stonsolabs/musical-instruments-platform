#!/usr/bin/env python3
"""
Test script for improved blog generation with diverse titles and content
"""

import asyncio
import json
from app.services.simple_blog_batch_generator import SimpleBlogBatchGenerator

async def test_improved_generation():
    """Test the improved blog generation with diverse topics"""
    
    print("🚀 Testing improved blog generation...")
    
    # Initialize the generator
    generator = SimpleBlogBatchGenerator()
    await generator.initialize()
    
    print(f"📚 Loaded {len(generator.templates)} templates")
    print(f"🎵 Loaded {len(generator.products)} products")
    print(f"💡 Generated {len(generator.blog_ideas)} diverse topic ideas")
    
    # Show sample ideas from each template
    print("\n📝 Sample topic ideas by template:")
    
    template_samples = {}
    for idea in generator.blog_ideas[:50]:  # First 50 ideas
        # Try to match ideas to templates based on keywords
        for template in generator.templates:
            template_name = template['name']
            if template_name not in template_samples:
                template_samples[template_name] = []
            
            # Add logic to categorize ideas
            if (template_name == 'buying-guide' and any(word in idea.lower() for word in ['guide', 'selection', 'choosing', 'buying', 'roadmap'])):
                if len(template_samples[template_name]) < 3:
                    template_samples[template_name].append(idea)
            elif (template_name == 'review' and any(word in idea.lower() for word in ['inside look', 'worth', 'test', 'experience', 'breaking down'])):
                if len(template_samples[template_name]) < 3:
                    template_samples[template_name].append(idea)
            elif (template_name == 'comparison' and any(word in idea.lower() for word in ['vs', 'showdown', 'rivalry', 'debate', 'face-off'])):
                if len(template_samples[template_name]) < 3:
                    template_samples[template_name].append(idea)
    
    for template_name, samples in template_samples.items():
        if samples:
            print(f"\n  {template_name.upper()}:")
            for sample in samples:
                print(f"    • {sample}")
    
    # Generate a small test batch
    print(f"\n🎯 Generating test batch of 10 posts...")
    
    # Custom distribution for testing
    test_distribution = {
        'buying-guide': 0.3,
        'review': 0.25,
        'comparison': 0.2,
        'artist-spotlight': 0.1,
        'instrument-history': 0.1,
        'gear-tips': 0.05,
        'news-feature': 0.0  # Skip news for this test
    }
    
    requests = await generator.generate_batch_requests(
        num_posts=10,
        output_file='test_diverse_batch.jsonl',
        word_count_range=(3500, 4500),
        template_distribution=test_distribution
    )
    
    print(f"\n✅ Generated {len(requests)} test requests")
    print("📄 Saved to: test_diverse_batch.jsonl")
    
    # Show some sample request titles from the batch
    print(f"\n📋 Sample topics from generated batch:")
    for i, request in enumerate(requests[:5]):
        topic = request['body']['messages'][1]['content'].split('"')[1]
        print(f"  {i+1}. {topic}")
    
    print("\n🎉 Test completed! Check test_diverse_batch.jsonl for full batch.")

if __name__ == "__main__":
    asyncio.run(test_improved_generation())
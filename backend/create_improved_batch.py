#!/usr/bin/env python3
"""
Create improved blog batch file using existing system with better product matching
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.simple_blog_batch_generator import SimpleBlogBatchGenerator

async def main():
    print("🔄 Creating Improved Blog Batch File")
    print("=" * 50)
    
    # Initialize the batch generator
    generator = SimpleBlogBatchGenerator()
    await generator.initialize()
    
    # Parse command line arguments
    num_posts = 100
    if "--num" in sys.argv:
        try:
            idx = sys.argv.index("--num")
            num_posts = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            print("❌ Invalid --num argument")
            return
    
    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"production_batch_{timestamp}.jsonl"
    
    if "--output" in sys.argv:
        try:
            idx = sys.argv.index("--output")
            output_file = sys.argv[idx + 1]
        except (IndexError, ValueError):
            print("❌ Invalid --output argument")
            return
    
    print(f"📊 Configuration:")
    print(f"  Posts to generate: {num_posts}")
    print(f"  Output file: {output_file}")
    
    # Generate batch requests
    print(f"\n🚀 Generating batch requests...")
    
    requests = await generator.generate_batch_requests(
        num_posts=num_posts,
        output_file=output_file,
        word_count_range=(3500, 4500),
        template_distribution={
            'buying-guide': 0.25,    # 25 posts
            'review': 0.20,          # 20 posts  
            'comparison': 0.15,      # 15 posts
            'artist-spotlight': 0.12, # 12 posts
            'instrument-history': 0.10, # 10 posts
            'gear-tips': 0.10,       # 10 posts
            'news-feature': 0.08     # 8 posts
        }
    )
    
    print(f"\n✅ Batch file created successfully!")
    print(f"📁 File: {output_file}")
    print(f"📊 Total requests: {len(requests)}")
    
    # Show file size
    try:
        import os
        file_size = os.path.getsize(output_file)
        print(f"📁 File size: {file_size / 1024 / 1024:.2f} MB")
    except:
        pass
    
    print(f"\n🚀 Next Steps:")
    print(f"1. Upload {output_file} to Azure OpenAI Batch API")
    print(f"2. Wait for batch processing to complete")  
    print(f"3. Download the output file")
    print(f"4. Process results with: python -m app.services.simple_blog_batch_processor <output_file>")

if __name__ == "__main__":
    asyncio.run(main())
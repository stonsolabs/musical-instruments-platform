#!/usr/bin/env python3
"""
Process Azure OpenAI Batch Output and Save Blog Posts
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.simple_blog_batch_processor import SimpleBlogBatchProcessor

async def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python process_azure_batch_output.py <batch_output_file.jsonl>")
        print("📝 Example: python process_azure_batch_output.py batch_output_20241201.jsonl")
        return
    
    batch_file = sys.argv[1]
    
    if not os.path.exists(batch_file):
        print(f"❌ File not found: {batch_file}")
        return
    
    print("🔄 Processing Azure OpenAI Batch Output")
    print("=" * 50)
    print(f"📁 Input file: {batch_file}")
    
    # Check file size and format
    try:
        file_size = os.path.getsize(batch_file) / 1024 / 1024
        print(f"📊 File size: {file_size:.2f} MB")
        
        # Count lines
        with open(batch_file, 'r') as f:
            line_count = sum(1 for line in f)
        print(f"📊 Total responses: {line_count}")
    except Exception as e:
        print(f"⚠️ Could not read file stats: {e}")
    
    # Ask for confirmation
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("🔍 Running in DRY RUN mode - will not save to database")
    else:
        print("⚠️ This will save blog posts to the database")
        print("💡 Add --dry-run flag to test without saving")
    
    print(f"\n🚀 Processing batch output...")
    
    # Initialize processor
    processor = SimpleBlogBatchProcessor()
    
    # Process the batch file
    try:
        result = await processor.process_batch_file(batch_file, dry_run=dry_run)
        
        print(f"\n✅ Batch processing complete!")
        print(f"📊 Results:")
        print(f"  ✅ Successfully processed: {result.get('processed_count', 0)}")
        print(f"  ❌ Errors: {result.get('error_count', 0)}")
        
        if result.get('errors'):
            print(f"\n❌ Errors encountered:")
            for i, error in enumerate(result['errors'][:5], 1):  # Show first 5 errors
                print(f"  {i}. {error}")
            if len(result['errors']) > 5:
                print(f"  ... and {len(result['errors']) - 5} more errors")
        
        # Show success rate
        total = result.get('processed_count', 0) + result.get('error_count', 0)
        if total > 0:
            success_rate = (result.get('processed_count', 0) / total) * 100
            print(f"📊 Success rate: {success_rate:.1f}%")
        
        if not dry_run and result.get('processed_count', 0) > 0:
            print(f"\n🎉 {result.get('processed_count', 0)} blog posts saved to database!")
            print(f"🌐 View your blog at: https://www.getyourmusicgear.com/blog")
    
    except Exception as e:
        print(f"❌ Error processing batch file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
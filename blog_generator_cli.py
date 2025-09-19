#!/usr/bin/env python3
"""
Blog Generator CLI - IMPROVED SYSTEM
Simple, effective blog generation with Guitar World/Drum Helper style
Focuses on available products and engaging content
"""

import asyncio
import sys
import os
import argparse
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.blog_batch_generator_service import BlogBatchGeneratorService
from backend.app.services.blog_batch_processor_service import BlogBatchProcessorService

class BlogGeneratorCLI:
    def __init__(self):
        self.generator_service = BlogBatchGeneratorService()
        self.processor_service = BlogBatchProcessorService()
    
    async def initialize(self):
        """Initialize the services"""
        print("🚀 Initializing Improved Blog Generator...")
        await self.generator_service.initialize()
        await self.processor_service.initialize()
        print("✅ Services initialized successfully!")
    
    async def generate_batch(self, args):
        """Generate a blog batch with specified parameters"""
        print(f"📝 Generating blog batch with {args.posts} posts...")
        
        # Parse template distribution if provided
        template_distribution = None
        if args.template_distribution:
            template_distribution = {}
            for dist in args.template_distribution:
                template_type, count = dist.split(':')
                template_distribution[template_type] = int(count)
        
        # Generate the batch
        result = await self.generator_service.generate_batch(
            total_posts=args.posts,
            template_distribution=template_distribution,
            category_focus=args.category_focus
        )
        
        # Print results
        print(f"\n🎉 Blog batch generated successfully!")
        print(f"📁 File: {result['filename']}")
        print(f"📊 Total posts: {result['total_posts']}")
        print(f"👥 Authors available: {result['authors_available']}")
        print(f"🛍️  Available products: {result['products_available']} (only purchasable items)")
        
        print(f"\n📈 Template distribution:")
        for template_type, count in result['template_distribution'].items():
            print(f"  - {template_type}: {count} posts")
        
        print(f"\n📤 Ready for OpenAI Batch API upload!")
        print(f"💡 Improved: Only available products, Guitar World style content")
        return result
    
    async def show_stats(self):
        """Show generation statistics"""
        stats = await self.generator_service.get_generation_stats()
        
        print("📊 Blog Generation Statistics")
        print("=" * 40)
        print(f"Templates available: {stats['templates_available']}")
        print(f"Authors available: {stats['authors_available']}")
        print(f"Products available: {stats['products_available']}")
        print(f"Blog ideas available: {stats['blog_ideas_available']}")
        
        print(f"\nTemplate types:")
        for template_type in stats['template_types']:
            print(f"  - {template_type}")
        
        print(f"\nProduct categories:")
        for category in stats['product_categories'][:10]:  # Show first 10
            print(f"  - {category}")
        if len(stats['product_categories']) > 10:
            print(f"  ... and {len(stats['product_categories']) - 10} more")
        
        print(f"\nAuthor specializations:")
        for author in stats['author_specializations']:
            print(f"  - {author}")
    
    async def process_batch(self, args):
        """Process a batch results file"""
        print(f"🔄 Processing batch results file: {args.file}")
        
        result = await self.processor_service.process_batch_file(args.file)
        
        print(f"\n🎉 Processing completed!")
        print(f"✅ Successfully processed: {result['processed_count']} blog posts")
        print(f"❌ Errors: {result['error_count']}")
        print(f"📈 Success rate: {result['success_rate']:.1f}%")
        
        if result['errors']:
            print(f"\n⚠️  Errors encountered:")
            for error in result['errors'][:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(result['errors']) > 5:
                print(f"  ... and {len(result['errors']) - 5} more errors")
        
        return result
    
    async def show_processing_stats(self):
        """Show processing statistics"""
        stats = await self.processor_service.get_processing_stats()
        
        print("📊 Blog Processing Statistics")
        print("=" * 40)
        print(f"Total blog posts: {stats['total_posts']}")
        print(f"AI-generated posts: {stats['ai_generated_posts']}")
        
        print(f"\nTemplate distribution:")
        for template_type, count in stats['template_distribution'].items():
            print(f"  - {template_type}: {count} posts")
        
        print(f"\nRecent posts:")
        for post in stats['recent_posts']:
            print(f"  - {post['title']} ({post['created_at'].strftime('%Y-%m-%d %H:%M')})")
    
    async def full_workflow(self, args):
        """Run complete workflow: generate -> process"""
        print("🚀 Running complete blog generation workflow...")
        
        # Step 1: Generate batch
        print("\n📝 Step 1: Generating blog batch...")
        generate_result = await self.generator_service.generate_batch(
            total_posts=args.posts,
            template_distribution=None,
            category_focus=args.category_focus
        )
        
        print(f"✅ Generated {generate_result['total_posts']} blog posts")
        print(f"📁 Batch file: {generate_result['filename']}")
        
        # Step 2: Process batch (simulate - in real workflow, you'd upload to Azure first)
        print(f"\n🔄 Step 2: Processing batch results...")
        print("⚠️  Note: In a real workflow, you would:")
        print("   1. Upload the batch file to Azure OpenAI Batch API")
        print("   2. Wait for processing to complete")
        print("   3. Download the results file")
        print("   4. Run: python blog_generator_cli.py process --file <results_file>")
        
        print(f"\n🎉 Workflow completed!")
        print(f"📁 Ready for upload: {generate_result['filename']}")
        
        return generate_result
    
    async def generate_large_batch(self, args):
        """Generate a large batch (100+ posts) with optimized distribution"""
        print(f"🚀 Generating large batch with {args.posts} posts...")
        
        # Optimized distribution for large batches (improved system)
        template_distribution = {
            "buying_guide": int(args.posts * 0.4),  # 40% buying guides (practical)
            "comparison": int(args.posts * 0.25),   # 25% comparisons (decision help)
            "review": int(args.posts * 0.25),       # 25% reviews (honest insights)
            "general": int(args.posts * 0.1),       # 10% general content (value guides)
        }
        
        # Generate the batch
        result = await self.generator_service.generate_batch(
            total_posts=args.posts,
            template_distribution=template_distribution,
            category_focus=args.category_focus
        )
        
        # Print results
        print(f"\n🎉 Large blog batch generated successfully!")
        print(f"📁 File: {result['filename']}")
        print(f"📊 Total posts: {result['total_posts']}")
        print(f"👥 Authors available: {result['authors_available']}")
        print(f"🛍️  Products available: {result['products_available']}")
        
        print(f"\n📈 Optimized template distribution:")
        for template_type, count in result['template_distribution'].items():
            percentage = (count / result['total_posts']) * 100
            print(f"  - {template_type}: {count} posts ({percentage:.1f}%)")
        
        print(f"\n📤 Ready for Azure OpenAI Batch API upload!")
        print(f"💡 Tip: For batches this large, consider processing in smaller chunks")
        return result
    
    async def generate_seasonal_batch(self, args):
        """Generate seasonal content batch"""
        print(f"🎄 Generating seasonal batch for {args.season}...")
        
        # Seasonal blog ideas
        seasonal_ideas = {
            "holiday": [
                {"title": "Holiday Gift Guide: Best Musical Instruments for Every Budget", "template": "general", "category": "0", "focus": "gift guide"},
                {"title": "Christmas Gift Ideas for Musicians: Complete Guide", "template": "general", "category": "0", "focus": "christmas gifts"},
                {"title": "Black Friday Music Gear Deals: What to Look For", "template": "general", "category": "0", "focus": "black friday deals"},
                {"title": "Cyber Monday Music Gear: Best Online Deals", "template": "general", "category": "0", "focus": "cyber monday deals"},
                {"title": "Learning a New Instrument: Your Musical Journey Starts Here", "template": "general", "category": "0", "focus": "learning instruments"},
            ],
            "back_to_school": [
                {"title": "Back to School: Essential Instruments for Music Students", "template": "general", "category": "0", "focus": "student gear"},
                {"title": "Student Instruments That Actually Sound Professional", "template": "general", "category": "0", "focus": "student instruments"},
                {"title": "Best Budget Guitars for Students: Complete Guide", "template": "buying_guide", "category": "31", "focus": "student guitars"},
                {"title": "Music School Essentials: What Every Student Needs", "template": "buying_guide", "category": "0", "focus": "music school gear"},
            ],
            "summer": [
                {"title": "Summer Music Festival Gear: What You Need to Know", "template": "general", "category": "31", "focus": "festival gear"},
                {"title": "Travel-Friendly Instruments: Make Music Anywhere", "template": "general", "category": "0", "focus": "travel instruments"},
                {"title": "Summer Music Camp Essentials: What to Pack", "template": "general", "category": "0", "focus": "music camp gear"},
                {"title": "Outdoor Performance Gear: Weather-Resistant Instruments", "template": "buying_guide", "category": "0", "focus": "outdoor gear"},
            ]
        }
        
        ideas = seasonal_ideas.get(args.season, seasonal_ideas["holiday"])
        
        # Generate the batch
        result = await self.generator_service.generate_batch(
            total_posts=args.posts,
            custom_ideas=ideas
        )
        
        print(f"\n🎉 Seasonal batch generated successfully!")
        print(f"📁 File: {result['filename']}")
        print(f"📊 Total posts: {result['total_posts']}")
        print(f"🎄 Season: {args.season}")
        
        return result

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Blog Generator CLI - Generate blog batches for your music gear platform")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate batch command
    generate_parser = subparsers.add_parser('generate', help='Generate a blog batch')
    generate_parser.add_argument('--posts', type=int, default=50, help='Number of posts to generate (default: 50)')
    generate_parser.add_argument('--template-distribution', action='append', help='Template distribution (e.g., buying_guide:20,comparison:10)')
    generate_parser.add_argument('--category-focus', help='Focus on specific category (e.g., 31 for guitars)')
    
    # Generate large batch command
    large_parser = subparsers.add_parser('generate-large', help='Generate a large batch (100+ posts) with optimized distribution')
    large_parser.add_argument('--posts', type=int, default=100, help='Number of posts to generate (default: 100)')
    large_parser.add_argument('--category-focus', help='Focus on specific category (e.g., 31 for guitars)')
    
    # Generate seasonal batch command
    seasonal_parser = subparsers.add_parser('generate-seasonal', help='Generate seasonal content batch')
    seasonal_parser.add_argument('--season', choices=['holiday', 'back_to_school', 'summer'], default='holiday', help='Season for content (default: holiday)')
    seasonal_parser.add_argument('--posts', type=int, default=20, help='Number of posts to generate (default: 20)')
    
    # Show stats command
    subparsers.add_parser('stats', help='Show generation statistics')
    
    # Process batch command
    process_parser = subparsers.add_parser('process', help='Process a batch results file')
    process_parser.add_argument('--file', required=True, help='Path to the batch results JSONL file')
    
    # Show processing stats command
    subparsers.add_parser('processing-stats', help='Show processing statistics')
    
    # Full workflow command
    workflow_parser = subparsers.add_parser('workflow', help='Run complete workflow: generate -> process')
    workflow_parser.add_argument('--posts', type=int, default=50, help='Number of posts to generate (default: 50)')
    workflow_parser.add_argument('--category-focus', help='Focus on specific category (e.g., 31 for guitars)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create CLI instance and run command
    cli = BlogGeneratorCLI()
    
    async def run_command():
        await cli.initialize()
        
        if args.command == 'generate':
            await cli.generate_batch(args)
        elif args.command == 'generate-large':
            await cli.generate_large_batch(args)
        elif args.command == 'generate-seasonal':
            await cli.generate_seasonal_batch(args)
        elif args.command == 'stats':
            await cli.show_stats()
        elif args.command == 'process':
            await cli.process_batch(args)
        elif args.command == 'processing-stats':
            await cli.show_processing_stats()
        elif args.command == 'workflow':
            await cli.full_workflow(args)
    
    asyncio.run(run_command())

if __name__ == "__main__":
    main()

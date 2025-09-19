#!/usr/bin/env python3
"""
Simplified Blog Generator CLI
Simple, effective blog generation using the new simplified system
"""

import asyncio
import sys
import os
import argparse
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.simple_blog_batch_generator import SimpleBlogBatchGenerator
from backend.app.services.simple_blog_batch_processor import SimpleBlogBatchProcessor

class SimpleBlogCLI:
    def __init__(self):
        self.generator = SimpleBlogBatchGenerator()
        self.processor = SimpleBlogBatchProcessor()
    
    async def generate_batch(self, args):
        """Generate a blog batch with specified parameters"""
        print(f"📝 Generating {args.posts} blog posts...")
        
        # Parse template distribution if provided
        template_distribution = None
        if args.template_distribution:
            try:
                template_distribution = json.loads(args.template_distribution)
            except json.JSONDecodeError:
                print("❌ Invalid template distribution JSON")
                return
        
        # Generate the batch
        output_file = args.output or f"blog_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        
        try:
            await self.generator.initialize()
            
            requests = await self.generator.generate_batch_requests(
                num_posts=args.posts,
                output_file=output_file,
                word_count_range=(args.min_words, args.max_words),
                template_distribution=template_distribution
            )
            
            print(f"✅ Generated {len(requests)} blog post requests")
            print(f"📁 Saved to: {output_file}")
            print("\n📊 Template breakdown:")
            
            # Show template breakdown
            template_counts = {}
            for request in requests:
                # Extract template from request content more accurately
                content = request['body']['messages'][1]['content']
                
                # Look for the category field in the JSON structure
                if '"category": "buying-guide"' in content:
                    template_counts['buying-guide'] = template_counts.get('buying-guide', 0) + 1
                elif '"category": "review"' in content:
                    template_counts['review'] = template_counts.get('review', 0) + 1
                elif '"category": "comparison"' in content:
                    template_counts['comparison'] = template_counts.get('comparison', 0) + 1
                elif '"category": "artist-spotlight"' in content:
                    template_counts['artist-spotlight'] = template_counts.get('artist-spotlight', 0) + 1
                elif '"category": "instrument-history"' in content:
                    template_counts['instrument-history'] = template_counts.get('instrument-history', 0) + 1
                elif '"category": "gear-tips"' in content:
                    template_counts['gear-tips'] = template_counts.get('gear-tips', 0) + 1
                elif '"category": "news-feature"' in content:
                    template_counts['news-feature'] = template_counts.get('news-feature', 0) + 1
                else:
                    # Fallback to content analysis
                    if 'buying guide' in content.lower():
                        template_counts['buying-guide'] = template_counts.get('buying-guide', 0) + 1
                    elif 'artist spotlight' in content.lower():
                        template_counts['artist-spotlight'] = template_counts.get('artist-spotlight', 0) + 1
                    elif 'instrument history' in content.lower():
                        template_counts['instrument-history'] = template_counts.get('instrument-history', 0) + 1
                    elif 'gear tips' in content.lower():
                        template_counts['gear-tips'] = template_counts.get('gear-tips', 0) + 1
                    elif 'news feature' in content.lower():
                        template_counts['news-feature'] = template_counts.get('news-feature', 0) + 1
                    elif 'comparison' in content.lower():
                        template_counts['comparison'] = template_counts.get('comparison', 0) + 1
                    else:
                        template_counts['review'] = template_counts.get('review', 0) + 1
                    
            for template, count in template_counts.items():
                print(f"  {template}: {count}")
            
            print("\n🚀 Ready to submit to OpenAI Batch API!")
            
        except Exception as e:
            print(f"❌ Error generating batch: {str(e)}")
    
    async def process_batch(self, args):
        """Process OpenAI batch results file"""
        print(f"📤 Processing batch results: {args.file}")
        
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            return
        
        try:
            summary = await self.processor.process_batch_file(
                batch_file_path=args.file,
                dry_run=args.dry_run
            )
            
            print("\n📊 Processing Summary:")
            print(f"✅ Successfully processed: {summary['processed_count']}")
            print(f"❌ Errors: {summary['error_count']}")
            print(f"📈 Success rate: {summary['success_rate']:.1f}%")
            
            if summary['errors']:
                print("\n🚨 First few errors:")
                for error in summary['errors']:
                    print(f"  - {error}")
            
            if not args.dry_run:
                print(f"\n💾 Saved {summary['processed_count']} blog posts to database")
            else:
                print("\n🔍 Dry run completed - no data saved")
                
        except Exception as e:
            print(f"❌ Error processing batch: {str(e)}")
    
    async def get_stats(self, args):
        """Get blog system statistics"""
        print("📊 Blog System Statistics")
        print("=" * 50)
        
        try:
            stats = await self.processor.get_processing_stats()
            
            print(f"📝 Total posts: {stats['total_posts']}")
            print("\n📋 Posts by status:")
            for status, count in stats['status_counts'].items():
                print(f"  {status}: {count}")
            
            print("\n🆕 Recent posts:")
            for post in stats['recent_posts'][:5]:
                category = post.get('category') or 'general'
                created = post['created_at'].strftime('%Y-%m-%d %H:%M') if post['created_at'] else 'Unknown'
                print(f"  [{category}] {post['title']} ({created})")
                
        except Exception as e:
            print(f"❌ Error getting stats: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Simplified Blog Generator CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate blog batch requests')
    gen_parser.add_argument('--posts', type=int, default=50, help='Number of posts to generate (default: 50)')
    gen_parser.add_argument('--output', type=str, help='Output JSONL file path')
    gen_parser.add_argument('--min-words', type=int, default=3000, help='Minimum word count (default: 3000)')
    gen_parser.add_argument('--max-words', type=int, default=5000, help='Maximum word count (default: 5000)')
    gen_parser.add_argument('--template-distribution', type=str, 
                          help='JSON template distribution e.g. \'{"buying-guide": 0.4, "review": 0.3}\'')
    
    # Process command
    proc_parser = subparsers.add_parser('process', help='Process batch results')
    proc_parser.add_argument('--file', type=str, required=True, help='Batch results JSONL file')
    proc_parser.add_argument('--dry-run', action='store_true', help='Validate only, don\'t save to database')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show blog system statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = SimpleBlogCLI()
    
    try:
        if args.command == 'generate':
            asyncio.run(cli.generate_batch(args))
        elif args.command == 'process':
            asyncio.run(cli.process_batch(args))
        elif args.command == 'stats':
            asyncio.run(cli.get_stats(args))
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
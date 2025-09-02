#!/usr/bin/env python3
"""
CLI Script for Thomann Image Downloader
Run the image downloader with command line arguments
"""

import asyncio
import argparse
import sys
from thomann_image_downloader import ThomannImageDownloader

async def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description='Thomann Image Downloader CLI')
    parser.add_argument(
        '--max-products', 
        type=int, 
        help='Maximum number of products to process (default: all)'
    )
    parser.add_argument(
        '--max-concurrent', 
        type=int, 
        default=10,
        help='Maximum concurrent downloads (default: 10)'
    )
    parser.add_argument(
        '--test-mode', 
        action='store_true',
        help='Run in test mode (limited functionality)'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Show what would be processed without actually downloading'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        async with ThomannImageDownloader(
            max_concurrent=args.max_concurrent,
            test_mode=args.test_mode
        ) as downloader:
            
            if args.dry_run:
                print("🔍 DRY RUN MODE - No actual downloads will occur")
                products = await downloader.get_products_with_thomann_links()
                if args.max_products:
                    products = products[:args.max_products]
                
                print(f"📋 Would process {len(products)} products:")
                for i, product in enumerate(products[:10], 1):  # Show first 10
                    print(f"  {i}. {product['name']} - {product['thomann_url']}")
                
                if len(products) > 10:
                    print(f"  ... and {len(products) - 10} more")
                
                return
            
            await downloader.run(max_products=args.max_products)
            
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

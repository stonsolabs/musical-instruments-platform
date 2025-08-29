#!/usr/bin/env python3
"""
Generate batch files from all products in the database.
This script creates Azure OpenAI batch files for processing all products in the database.
"""

import json
import asyncio
import math
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from database import get_async_session
from sqlalchemy import text
from get_config_from_db import get_batch_prompt


async def get_total_product_count() -> int:
    """Get the total number of products in the database."""
    async with await get_async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM products_filled"))
        return result.scalar()


async def get_products_batch(offset: int, limit: int) -> List[tuple]:
    """Get a batch of products from the database."""
    async with await get_async_session() as session:
        result = await session.execute(text("""
            SELECT sku, name, slug, description, msrp_price, url
            FROM products_filled 
            ORDER BY id
            LIMIT :limit OFFSET :offset
        """), {"limit": limit, "offset": offset})
        
        return result.fetchall()


def create_batch_request(product: tuple, azure_prompt: str, deployment_name: str = "gpt-4.1") -> dict:
    """Create a single batch request for a product."""
    sku, name, slug, description, msrp_price, url = product
    
    # Create product input
    product_input = {
        "sku": sku,
        "name": name,
        "slug": slug,
        "description": description,
        "msrp_price": float(msrp_price) if msrp_price else 0.0,
        "url_source": url,
        "image_uri": None
    }
    
    # Create batch request in Azure OpenAI format
    return {
        "custom_id": sku,
        "method": "POST",
        "url": "/chat/completions",
        "body": {
            "model": deployment_name,
            "messages": [
                {
                    "role": "system",
                    "content": azure_prompt
                },
                {
                    "role": "user",
                    "content": f"Process this product: {json.dumps(product_input)}"
                }
            ],
            "response_format": {"type": "json_object"},
            "max_tokens": 4000,
            "temperature": 0.1
        }
    }


async def generate_batch_files(
    batch_size: int = 100,
    max_products: Optional[int] = None,
    deployment_name: str = "gpt-4.1"
) -> None:
    """
    Generate batch files from all products in the database.
    
    Args:
        batch_size: Number of products per batch file
        max_products: Maximum number of products to process (None for all)
        deployment_name: Azure OpenAI deployment name
    """
    
    # Get total product count
    total_products = await get_total_product_count()
    if max_products:
        total_products = min(total_products, max_products)
    
    if total_products == 0:
        print("❌ No products found in database")
        return
    
    print(f"📊 Total products to process: {total_products}")
    print(f"📦 Batch size: {batch_size}")
    print(f"📁 Number of batch files: {math.ceil(total_products / batch_size)}")
    
    # Get Azure prompt
    azure_prompt = get_batch_prompt()
    print(f"📝 System prompt length: {len(azure_prompt)} characters")
    
    # Create batch_files directory if it doesn't exist
    batch_dir = Path("batch_files")
    batch_dir.mkdir(exist_ok=True)
    
    # Generate batch files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_number = 1
    
    for offset in range(0, total_products, batch_size):
        print(f"\n🔄 Processing batch {batch_number} (products {offset + 1}-{min(offset + batch_size, total_products)})...")
        
        # Get products for this batch
        products = await get_products_batch(offset, batch_size)
        
        if not products:
            print(f"⚠️  No products found for batch {batch_number}")
            break
        
        # Create batch requests
        batch_requests = []
        for i, product in enumerate(products, 1):
            print(f"  Processing product {i}/{len(products)}: {product.name[:50]}...")
            batch_request = create_batch_request(product, azure_prompt, deployment_name)
            batch_requests.append(batch_request)
        
        # Write batch file
        filename = batch_dir / f"azure_batch_{batch_number:03d}_{len(products)}_products_{timestamp}.jsonl"
        
        with open(filename, 'w') as f:
            for request in batch_requests:
                f.write(json.dumps(request) + '\n')
        
        print(f"✅ Batch file created: {filename}")
        print(f"📊 Requests in this batch: {len(batch_requests)}")
        
        batch_number += 1
    
    print(f"\n🎉 All batch files generated successfully!")
    print(f"📁 Files saved in: {batch_dir.absolute()}")
    print(f"🔢 Total batch files: {batch_number - 1}")
    print(f"🎯 Deployment name: {deployment_name}")


async def generate_single_large_batch(
    max_products: Optional[int] = None,
    deployment_name: str = "gpt-4.1"
) -> None:
    """
    Generate a single large batch file with all products.
    
    Args:
        max_products: Maximum number of products to process (None for all)
        deployment_name: Azure OpenAI deployment name
    """
    
    # Get total product count
    total_products = await get_total_product_count()
    if max_products:
        total_products = min(total_products, max_products)
    
    if total_products == 0:
        print("❌ No products found in database")
        return
    
    print(f"📊 Total products to process: {total_products}")
    
    # Get Azure prompt
    azure_prompt = get_batch_prompt()
    print(f"📝 System prompt length: {len(azure_prompt)} characters")
    
    # Create batch_files directory if it doesn't exist
    batch_dir = Path("batch_files")
    batch_dir.mkdir(exist_ok=True)
    
    # Get all products
    print("🔄 Fetching all products from database...")
    products = await get_products_batch(0, total_products)
    
    if not products:
        print("❌ No products found")
        return
    
    # Create batch requests
    print("🔄 Creating batch requests...")
    batch_requests = []
    for i, product in enumerate(products, 1):
        if i % 100 == 0:
            print(f"  Processed {i}/{len(products)} products...")
        batch_request = create_batch_request(product, azure_prompt, deployment_name)
        batch_requests.append(batch_request)
    
    # Write single batch file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = batch_dir / f"azure_batch_ALL_{len(products)}_products_{timestamp}.jsonl"
    
    print(f"💾 Writing batch file: {filename}")
    with open(filename, 'w') as f:
        for request in batch_requests:
            f.write(json.dumps(request) + '\n')
    
    print(f"✅ Single large batch file created: {filename}")
    print(f"📊 Total requests: {len(batch_requests)}")
    print(f"🎯 Deployment name: {deployment_name}")


async def main():
    """Main function with command line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate batch files from all products in database")
    parser.add_argument(
        "--mode", 
        choices=["batched", "single"], 
        default="batched",
        help="Generate multiple batch files (batched) or single large file (single)"
    )
    parser.add_argument(
        "--batch-size", 
        type=int, 
        default=100,
        help="Number of products per batch file (for batched mode)"
    )
    parser.add_argument(
        "--max-products", 
        type=int, 
        default=None,
        help="Maximum number of products to process (None for all)"
    )
    parser.add_argument(
        "--deployment", 
        type=str, 
        default="gpt-4.1",
        help="Azure OpenAI deployment name"
    )
    
    args = parser.parse_args()
    
    print("🚀 Starting batch file generation...")
    print(f"📋 Mode: {args.mode}")
    print(f"🎯 Deployment: {args.deployment}")
    
    if args.max_products:
        print(f"📊 Max products: {args.max_products}")
    
    if args.mode == "batched":
        await generate_batch_files(
            batch_size=args.batch_size,
            max_products=args.max_products,
            deployment_name=args.deployment
        )
    else:
        await generate_single_large_batch(
            max_products=args.max_products,
            deployment_name=args.deployment
        )


if __name__ == "__main__":
    asyncio.run(main())

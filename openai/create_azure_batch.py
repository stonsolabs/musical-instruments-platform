#!/usr/bin/env python3
"""
Create batch files in the correct Azure OpenAI format.
Based on Microsoft documentation: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/batch-blob-storage?tabs=python
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from database import get_async_session
from sqlalchemy import text
import argparse


def get_azure_prompt(prompt_file=None, mode=None):
    """Get the prompt formatted for Azure OpenAI batch.
    - If prompt_file provided, load that prompt from file/DB
    - If mode == 'ratings_append', load the ratings append prompt
    - Else, default to the full enrichment prompt
    """
    from get_config_from_db import get_batch_prompt, get_prompt, get_ratings_append_prompt
    if prompt_file:
        return get_prompt(prompt_file)
    if mode == 'ratings_append':
        return get_ratings_append_prompt()
    return get_batch_prompt()


async def create_azure_batch_file(
    num_products=30,
    mode=None,
    prompt_file=None,
    offset=0,
    part_index=None,
    total_parts=None,
    start_id=None,
    return_meta=False,
):
    """Create a batch file in the correct Azure OpenAI format.
    - mode: None (full) or 'ratings_append'
    - prompt_file: optional explicit prompt filename from config_files
    """

    # Get products from database (always from products)
    async with await get_async_session() as session:
        # Join brand/category names if available
        if start_id is not None:
            query = text(
                """
                SELECT p.id AS product_id, p.sku, p.name, p.slug, p.description, p.msrp_price,
                       b.name AS brand_name, c.name AS category_name
                FROM products p
                LEFT JOIN brands b ON p.brand_id = b.id
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.id > :start_id
                ORDER BY p.id
                LIMIT :limit
                """
            )
            params = {"limit": num_products, "start_id": start_id}
        else:
            query = text(
                """
                SELECT p.id AS product_id, p.sku, p.name, p.slug, p.description, p.msrp_price,
                       b.name AS brand_name, c.name AS category_name
                FROM products p
                LEFT JOIN brands b ON p.brand_id = b.id
                LEFT JOIN categories c ON p.category_id = c.id
                ORDER BY p.id
                LIMIT :limit OFFSET :offset
                """
            )
            params = {"limit": num_products, "offset": offset}

        result = await session.execute(query, params)

        products = result.fetchall()
    
    if not products:
        print("❌ No products found")
        return None
    
    print(f"📋 Found {len(products)} products for batch processing")
    
    # Create batch requests
    batch_requests = []
    azure_prompt = get_azure_prompt(prompt_file=prompt_file, mode=mode)
    
    # Use your actual deployment name here
    deployment_name = "gpt-4.1"  # Replace with your actual deployment name
    
    for i, product in enumerate(products, 1):
        print(f"  Processing product {i}/{len(products)}: {product.name}...")
        
        # Create product input
        product_input = {
            "id": getattr(product, "product_id", None),
            "sku": getattr(product, "sku", None),
            "name": product.name,
            "slug": product.slug,
            "description": product.description,
            "msrp_price": float(product.msrp_price) if product.msrp_price else 0.0,
            "brand": getattr(product, "brand_name", None),
            "category": getattr(product, "category_name", None),
        }
        
        # Create batch request in Azure OpenAI format
        custom_id = product_input.get("sku") or product_input.get("slug") or f"idx_{i}"
        if mode == 'ratings_append':
            # Encode multiple identifiers to robustly match later
            parts = []
            if product_input.get("id"):
                parts.append(f"id:{product_input['id']}")
            if product_input.get("sku"):
                parts.append(f"sku:{product_input['sku']}")
            if product_input.get("slug"):
                parts.append(f"slug:{product_input['slug']}")
            parts.append("mode:ratings_append")
            custom_id = "|".join(parts) if parts else f"idx_{i}|mode:ratings_append"

        batch_request = {
            "custom_id": custom_id,
            "method": "POST",
            "url": "/chat/completions",  # Changed from /v1/chat/completions
            "body": {
                "model": deployment_name,  # Use your deployment name
                "messages": [
                    {
                        "role": "system",
                        "content": azure_prompt
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Process this product: {json.dumps(product_input)}"
                            if mode != 'ratings_append' else
                            f"Generate ONLY the new sections to append under content as per the system JSON. Product: {json.dumps(product_input)}"
                        )
                    }
                ],
                "response_format": {"type": "json_object"},
                "max_tokens": 25000 if mode == 'ratings_append' else 4000,
                "temperature": 0.1
            }
        }
        
        batch_requests.append(batch_request)
    
    # Write to file (ensure we write inside openai/batch_files)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "ratings_append" if mode == 'ratings_append' else "full"
    source_label = "products"
    batch_dir = Path(__file__).parent / "batch_files"
    batch_dir.mkdir(parents=True, exist_ok=True)
    # Include offset and zero-padded part index for uniqueness and natural sort order
    if part_index and total_parts:
        width = len(str(total_parts))
        part_str = f"_part{part_index:0{width}d}of{total_parts:0{width}d}"
    else:
        part_str = ""
    # Include id range when available
    ids = [getattr(p, "product_id", None) for p in products if getattr(p, "product_id", None) is not None]
    id_range = ""
    first_id = last_id = None
    if ids:
        first_id = min(ids)
        last_id = max(ids)
        id_range = f"_ids{first_id}-{last_id}"
    filename = str(batch_dir / f"azure_batch_{suffix}_{source_label}_{num_products}{part_str}_offset{offset}{id_range}_{timestamp}.jsonl")
    if part_index and total_parts:
        print(f"🧩 File part {part_index}/{total_parts} | offset={offset} | count={num_products}")

    with open(filename, 'w') as f:
        for request in batch_requests:
            f.write(json.dumps(request) + '\n')
    
    print(f"\n✅ Azure batch file created: {filename}")
    print(f"📊 Total requests: {len(batch_requests)}")
    print(f"📝 System prompt length: {len(azure_prompt)} characters")
    print(f"🔢 Max tokens per request: {25000 if mode == 'ratings_append' else 4000}")
    print(f"🎯 Deployment name: {deployment_name}")
    print(f"🔗 URL format: /chat/completions")
    
    if return_meta:
        return filename, first_id, last_id
    return filename


def create_azure_batch_script():
    """Create a Python script to submit the batch job using Azure Blob Storage."""
    
    script_content = '''#!/usr/bin/env python3
"""
Azure OpenAI Batch Job Submission Script
Based on Microsoft documentation: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/batch-blob-storage?tabs=python
"""

import os
from datetime import datetime
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Configuration - UPDATE THESE VALUES
AZURE_OPENAI_ENDPOINT = "https://getyourmusicgear.openai.azure.com/"  # Your endpoint
STORAGE_ACCOUNT_NAME = "your-storage-account-name"  # Your Azure Blob Storage account
BATCH_INPUT_CONTAINER = "batch-input"
BATCH_OUTPUT_CONTAINER = "batch-output"
BATCH_FILE_NAME = "azure_batch_30_products_20250828_193237.jsonl"  # Your batch file

def submit_batch_job():
    """Submit a batch job using Azure Blob Storage."""
    
    # Setup authentication
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    
    # Create Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_ad_token_provider=token_provider,
        api_version="2025-04-01-preview"
    )
    
    # Construct blob URLs
    input_blob_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{BATCH_INPUT_CONTAINER}/{BATCH_FILE_NAME}"
    output_folder_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{BATCH_OUTPUT_CONTAINER}"
    
    print(f"🚀 Submitting batch job...")
    print(f"📁 Input file: {input_blob_url}")
    print(f"📁 Output folder: {output_folder_url}")
    
    try:
        # Create batch job
        batch_response = client.batches.create(
            input_file_id=None,
            endpoint="/chat/completions",
            completion_window="24h",
            extra_body={
                "input_blob": input_blob_url,
                "output_folder": {
                    "url": output_folder_url,
                }
            }
        )
        
        # Save batch ID
        batch_id = batch_response.id
        print(f"✅ Batch job created successfully!")
        print(f"🆔 Batch ID: {batch_id}")
        print(f"📊 Status: {batch_response.status}")
        
        # Monitor batch job
        monitor_batch_job(client, batch_id)
        
        return batch_id
        
    except Exception as e:
        print(f"❌ Error creating batch job: {str(e)}")
        return None


def monitor_batch_job(client, batch_id):
    """Monitor the batch job status."""
    import time
    
    print(f"📊 Monitoring batch job: {batch_id}")
    
    status = "validating"
    while status not in ("completed", "failed", "canceled"):
        time.sleep(60)  # Check every minute
        batch_response = client.batches.retrieve(batch_id)
        status = batch_response.status
        print(f"{datetime.now()} Batch ID: {batch_id}, Status: {status}")
        
        # Show progress
        if hasattr(batch_response, 'request_counts'):
            counts = batch_response.request_counts
            print(f"  📈 Progress: {counts.completed}/{counts.total} completed, {counts.failed} failed")
    
    # Final status
    if batch_response.status == "completed":
        print(f"🎉 Batch job completed successfully!")
        print(f"📁 Output blob: {batch_response.output_blob}")
        if batch_response.error_blob:
            print(f"📁 Error blob: {batch_response.error_blob}")
    elif batch_response.status == "failed":
        print(f"❌ Batch job failed!")
        if batch_response.errors:
            for error in batch_response.errors.data:
                print(f"  Error code {error.code}: {error.message}")


if __name__ == "__main__":
    # Check environment variables
    if not os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("⚠️  Please set AZURE_OPENAI_ENDPOINT environment variable")
        print("   Example: export AZURE_OPENAI_ENDPOINT=https://getyourmusicgear.openai.azure.com/")
    
    submit_batch_job()
'''
    
    # Write script
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    script_filename = f"submit_azure_batch_{timestamp}.py"
    
    with open(script_filename, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Azure batch submission script created: {script_filename}")
    print(f"📝 Please update the configuration variables in the script before running")
    
    return script_filename


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Create Azure OpenAI batch file")
    parser.add_argument("num", nargs="?", type=int, default=30, help="Number of products")
    parser.add_argument("--mode", choices=["full", "ratings_append"], default="full", help="Prompt/output mode")
    parser.add_argument("--prompt-file", dest="prompt_file", default=None, help="Prompt filename from config_files (overrides mode)")
    parser.add_argument("--offset", type=int, default=0, help="Row offset for pagination")
    args = parser.parse_args()

    print(f"🚀 Creating Azure OpenAI batch file for {args.num} items | source=products | mode={args.mode}")

    mode_arg = None if args.mode == 'full' and not args.prompt_file else ('ratings_append' if args.mode == 'ratings_append' else None)

    # Create batch file
    loop = asyncio.get_event_loop()
    batch_file = loop.run_until_complete(create_azure_batch_file(args.num, mode=mode_arg, prompt_file=args.prompt_file, offset=args.offset))

    if batch_file:
        # Create submission script
        script_file = create_azure_batch_script()

        print(f"\n📋 Next Steps:")
        print(f"1. Upload {batch_file} to your Azure Blob Storage batch-input container")
        print(f"2. Update configuration in {script_file}")
        print(f"3. Run: python3 {script_file}")
        print(f"4. Monitor the batch job progress")


if __name__ == "__main__":
    main()

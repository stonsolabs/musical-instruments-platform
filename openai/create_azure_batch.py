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


def get_azure_prompt():
    """Get the prompt formatted for Azure OpenAI batch."""
    from get_config_from_db import get_batch_prompt
    return get_batch_prompt()


async def create_azure_batch_file(num_products=30):
    """Create a batch file in the correct Azure OpenAI format."""
    
    # Get products from database
    async with await get_async_session() as session:
        result = await session.execute(text("""
            SELECT sku, name, slug, description, msrp_price, url
            FROM products_filled 
            LIMIT :limit
        """), {"limit": num_products})
        
        products = result.fetchall()
    
    if not products:
        print("❌ No products found")
        return None
    
    print(f"📋 Found {len(products)} products for batch processing")
    
    # Create batch requests
    batch_requests = []
    azure_prompt = get_azure_prompt()
    
    # Use your actual deployment name here
    deployment_name = "gpt-4.1"  # Replace with your actual deployment name
    
    for i, product in enumerate(products, 1):
        print(f"  Processing product {i}/{len(products)}: {product.name}...")
        
        # Create product input
        product_input = {
            "sku": product.sku,
            "name": product.name,
            "slug": product.slug,
            "description": product.description,
            "msrp_price": float(product.msrp_price) if product.msrp_price else 0.0,
            "url_source": product.url,
            "image_uri": None
        }
        
        # Create batch request in Azure OpenAI format
        batch_request = {
            "custom_id": product.sku,
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
                        "content": f"Process this product: {json.dumps(product_input)}"
                    }
                ],
                "response_format": {"type": "json_object"},
                "max_tokens": 4000,
                "temperature": 0.1
            }
        }
        
        batch_requests.append(batch_request)
    
    # Write to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"batch_files/azure_batch_{num_products}_products_{timestamp}.jsonl"
    
    with open(filename, 'w') as f:
        for request in batch_requests:
            f.write(json.dumps(request) + '\n')
    
    print(f"\n✅ Azure batch file created: {filename}")
    print(f"📊 Total requests: {len(batch_requests)}")
    print(f"📝 System prompt length: {len(azure_prompt)} characters")
    print(f"🔢 Max tokens per request: 4000")
    print(f"🎯 Deployment name: {deployment_name}")
    print(f"🔗 URL format: /chat/completions")
    
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
    import sys
    
    num_products = 30
    if len(sys.argv) > 1:
        try:
            num_products = int(sys.argv[1])
        except ValueError:
            print("Invalid number of products. Using default: 30")
    
    print(f"🚀 Creating Azure OpenAI batch file for {num_products} products...")
    
    # Create batch file
    batch_file = asyncio.run(create_azure_batch_file(num_products))
    
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

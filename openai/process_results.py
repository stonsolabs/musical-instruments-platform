#!/usr/bin/env python3
"""
Script to process batch results and insert into database.
"""

import asyncio
import json
import sys
from pathlib import Path

from products_filled_parser import ProductsFilledParser


async def process_batch_results(results_file: str) -> None:
    """Process batch results and insert into database."""
    print(f"🔄 Processing batch results from: {results_file}")
    
    if not Path(results_file).exists():
        print(f"❌ Error: Results file not found: {results_file}")
        sys.exit(1)
    
    try:
        parser = ProductsFilledParser()
        
        # Read results file
        with open(results_file, 'r') as f:
            results_lines = f.readlines()
        
        print(f"📊 Found {len(results_lines)} results to process")
        
        success_count = 0
        error_count = 0
        
        for i, line in enumerate(results_lines, 1):
            try:
                result = json.loads(line.strip())
                custom_id = result.get('custom_id', 'unknown')
                
                # Check if this is a successful Azure OpenAI batch result
                # Azure OpenAI successful responses have "error": null
                if result.get('error') is None and result.get('response'):
                    # Extract AI content
                    ai_content = json.loads(result['response']['body']['choices'][0]['message']['content'])
                    
                    print(f"  Processing {i}/{len(results_lines)}: {custom_id}")
                    
                    # Parse and insert into database
                    parse_result = await parser.parse_and_insert(ai_content, custom_id)
                    
                    if parse_result:
                        success_count += 1
                        print(f"    ✅ Successfully inserted")
                    else:
                        error_count += 1
                        print(f"    ❌ Failed to insert")
                else:
                    error_count += 1
                    error_msg = result.get('error', 'Unknown error')
                    print(f"  Skipping {i}/{len(results_lines)}: {custom_id} - Error: {error_msg}")
                    
            except Exception as e:
                error_count += 1
                print(f"  ❌ Error processing result {i}: {str(e)}")
        
        print(f"\n📊 Processing Summary:")
        print(f"  ✅ Successful: {success_count}")
        print(f"  ❌ Errors: {error_count}")
        print(f"  📊 Total: {len(results_lines)}")
        
    except Exception as e:
        print(f"❌ Error processing batch results: {str(e)}")
        sys.exit(1)


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python3 process_results.py <results_file>")
        print("Example: python3 process_results.py batch_results/file-fda18481-516a-4f30-9f5f-827c6e233232.jsonl")
        sys.exit(1)
    
    results_file = sys.argv[1]
    asyncio.run(process_batch_results(results_file))


if __name__ == "__main__":
    main()

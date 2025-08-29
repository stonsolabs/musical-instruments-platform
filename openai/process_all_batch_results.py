#!/usr/bin/env python3
"""
Script to process all batch results and insert into database.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import List

from products_filled_parser import ProductsFilledParser


async def process_all_batch_results() -> None:
    """Process all batch results and insert into database."""
    batch_results_dir = Path("batch_results")
    
    if not batch_results_dir.exists():
        print(f"❌ Error: batch_results directory not found")
        sys.exit(1)
    
    # Find all .jsonl files in batch_results directory
    result_files = list(batch_results_dir.glob("*.jsonl"))
    
    if not result_files:
        print(f"❌ Error: No .jsonl files found in batch_results directory")
        sys.exit(1)
    
    print(f"🔄 Found {len(result_files)} batch result files to process")
    
    total_success = 0
    total_errors = 0
    total_processed = 0
    error_details = []  # Store detailed error information
    
    for i, results_file in enumerate(result_files, 1):
        print(f"\n📁 Processing file {i}/{len(result_files)}: {results_file.name}")
        
        try:
            parser = ProductsFilledParser()
            
            # Read results file
            with open(results_file, 'r') as f:
                results_lines = f.readlines()
            
            print(f"  📊 Found {len(results_lines)} results to process")
            
            success_count = 0
            error_count = 0
            
            for j, line in enumerate(results_lines, 1):
                try:
                    result = json.loads(line.strip())
                    custom_id = result.get('custom_id', 'unknown')
                    
                    # Check if this is a successful Azure OpenAI batch result
                    # Azure OpenAI successful responses have "error": null
                    if result.get('error') is None and result.get('response'):
                        # Extract AI content
                        ai_content = json.loads(result['response']['body']['choices'][0]['message']['content'])
                        
                        if j % 100 == 0:  # Progress indicator every 100 items
                            print(f"    Processing {j}/{len(results_lines)}: {custom_id}")
                        
                        # Parse and insert into database
                        parse_result = await parser.parse_and_insert(ai_content, custom_id)
                        
                        if parse_result:
                            success_count += 1
                        else:
                            error_count += 1
                            error_details.append({
                                'file': results_file.name,
                                'line': j,
                                'custom_id': custom_id,
                                'error_type': 'parse_failure',
                                'error': 'Parser returned False'
                            })
                    else:
                        error_count += 1
                        error_msg = result.get('error', 'Unknown error')
                        error_details.append({
                            'file': results_file.name,
                            'line': j,
                            'custom_id': custom_id,
                            'error_type': 'azure_error',
                            'error': error_msg
                        })
                        if j % 100 == 0:  # Progress indicator every 100 items
                            print(f"    Skipping {j}/{len(results_lines)}: {custom_id} - Error: {error_msg}")
                        
                except Exception as e:
                    error_count += 1
                    error_details.append({
                        'file': results_file.name,
                        'line': j,
                        'custom_id': custom_id,
                        'error_type': 'exception',
                        'error': str(e)
                    })
                    if j % 100 == 0:  # Progress indicator every 100 items
                        print(f"    ❌ Error processing result {j}: {str(e)}")
            
            print(f"  📊 File Summary:")
            print(f"    ✅ Successful: {success_count}")
            print(f"    ❌ Errors: {error_count}")
            print(f"    📊 Total: {len(results_lines)}")
            
            total_success += success_count
            total_errors += error_count
            total_processed += len(results_lines)
            
        except Exception as e:
            print(f"  ❌ Error processing batch results file {results_file.name}: {str(e)}")
    
    print(f"\n🎉 Final Processing Summary:")
    print(f"  📁 Files Processed: {len(result_files)}")
    print(f"  ✅ Total Successful: {total_success}")
    print(f"  ❌ Total Errors: {total_errors}")
    print(f"  📊 Total Processed: {total_processed}")
    print(f"  📈 Success Rate: {(total_success/total_processed*100):.1f}%" if total_processed > 0 else "  📈 Success Rate: 0%")
    
    # Display error details
    if error_details:
        print(f"\n🔍 Error Details ({len(error_details)} errors):")
        print("=" * 80)
        
        # Group errors by type
        error_types = {}
        for error in error_details:
            error_type = error['error_type']
            if error_type not in error_types:
                error_types[error_type] = []
            error_types[error_type].append(error)
        
        for error_type, errors in error_types.items():
            print(f"\n📋 {error_type.upper()} Errors ({len(errors)}):")
            for error in errors[:5]:  # Show first 5 of each type
                print(f"  • {error['custom_id']} (Line {error['line']} in {error['file']})")
                print(f"    Error: {error['error']}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more {error_type} errors")
        
        # Save detailed error log to file
        error_log_file = "batch_processing_errors.json"
        with open(error_log_file, 'w') as f:
            json.dump(error_details, f, indent=2)
        print(f"\n📄 Detailed error log saved to: {error_log_file}")


def main():
    """Main function."""
    print("🚀 Starting batch results processing...")
    asyncio.run(process_all_batch_results())


if __name__ == "__main__":
    main()

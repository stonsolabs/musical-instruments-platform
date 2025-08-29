#!/usr/bin/env python3
"""
Batch file summary and management utility.
Provides information about generated batch files and helps with management.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple


def get_batch_file_info(filepath: Path) -> Dict:
    """Extract information from a batch file."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Count requests
        request_count = len(lines)
        
        # Parse first request to get metadata
        if lines:
            first_request = json.loads(lines[0])
            deployment = first_request.get('body', {}).get('model', 'Unknown')
            custom_id = first_request.get('custom_id', 'Unknown')
            
            return {
                'filename': filepath.name,
                'request_count': request_count,
                'deployment': deployment,
                'sample_sku': custom_id,
                'file_size_mb': filepath.stat().st_size / (1024 * 1024),
                'created': datetime.fromtimestamp(filepath.stat().st_mtime)
            }
    except Exception as e:
        return {
            'filename': filepath.name,
            'error': str(e)
        }


def analyze_batch_files(batch_dir: str = "batch_files") -> Dict:
    """Analyze all batch files in the directory."""
    batch_path = Path(batch_dir)
    
    if not batch_path.exists():
        return {"error": f"Batch directory {batch_dir} does not exist"}
    
    # Get all JSONL files
    batch_files = list(batch_path.glob("*.jsonl"))
    
    if not batch_files:
        return {"error": f"No batch files found in {batch_dir}"}
    
    # Analyze each file
    file_info = []
    total_requests = 0
    total_size_mb = 0
    
    for filepath in sorted(batch_files):
        info = get_batch_file_info(filepath)
        if 'error' not in info:
            total_requests += info['request_count']
            total_size_mb += info['file_size_mb']
        file_info.append(info)
    
    return {
        'summary': {
            'total_files': len(batch_files),
            'total_requests': total_requests,
            'total_size_mb': round(total_size_mb, 2),
            'average_requests_per_file': round(total_requests / len(batch_files), 1),
            'average_file_size_mb': round(total_size_mb / len(batch_files), 2)
        },
        'files': file_info
    }


def print_summary(analysis: Dict):
    """Print a formatted summary of batch files."""
    if 'error' in analysis:
        print(f"❌ {analysis['error']}")
        return
    
    summary = analysis['summary']
    files = analysis['files']
    
    print("📊 BATCH FILES SUMMARY")
    print("=" * 50)
    print(f"📁 Total files: {summary['total_files']}")
    print(f"🔢 Total requests: {summary['total_requests']:,}")
    print(f"💾 Total size: {summary['total_size_mb']} MB")
    print(f"📈 Average requests per file: {summary['average_requests_per_file']}")
    print(f"📏 Average file size: {summary['average_file_size_mb']} MB")
    print()
    
    print("📋 FILE DETAILS")
    print("=" * 50)
    for info in files:
        if 'error' in info:
            print(f"❌ {info['filename']}: {info['error']}")
        else:
            print(f"✅ {info['filename']}")
            print(f"   Requests: {info['request_count']}")
            print(f"   Size: {info['file_size_mb']:.2f} MB")
            print(f"   Deployment: {info['deployment']}")
            print(f"   Sample SKU: {info['sample_sku']}")
            print(f"   Created: {info['created'].strftime('%Y-%m-%d %H:%M:%S')}")
            print()


def get_deployment_stats(analysis: Dict) -> Dict:
    """Get statistics by deployment."""
    if 'error' in analysis:
        return {}
    
    deployments = {}
    for info in analysis['files']:
        if 'error' not in info:
            deployment = info['deployment']
            if deployment not in deployments:
                deployments[deployment] = {
                    'files': 0,
                    'requests': 0,
                    'size_mb': 0
                }
            deployments[deployment]['files'] += 1
            deployments[deployment]['requests'] += info['request_count']
            deployments[deployment]['size_mb'] += info['file_size_mb']
    
    return deployments


def print_deployment_stats(analysis: Dict):
    """Print deployment statistics."""
    deployments = get_deployment_stats(analysis)
    
    if not deployments:
        print("❌ No deployment statistics available")
        return
    
    print("🎯 DEPLOYMENT STATISTICS")
    print("=" * 50)
    for deployment, stats in deployments.items():
        print(f"📊 {deployment}")
        print(f"   Files: {stats['files']}")
        print(f"   Requests: {stats['requests']:,}")
        print(f"   Size: {stats['size_mb']:.2f} MB")
        print()


def main():
    """Main function with command line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze batch files")
    parser.add_argument(
        "--batch-dir", 
        default="batch_files",
        help="Directory containing batch files"
    )
    parser.add_argument(
        "--deployments-only",
        action="store_true",
        help="Show only deployment statistics"
    )
    
    args = parser.parse_args()
    
    print("🔍 Analyzing batch files...")
    analysis = analyze_batch_files(args.batch_dir)
    
    if args.deployments_only:
        print_deployment_stats(analysis)
    else:
        print_summary(analysis)
        print_deployment_stats(analysis)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3.11
"""
Copy Images to Different Container Script
========================================

This script reads all blob image paths from the database and copies them
to a different Azure storage container. Useful for backup, migration,
or creating a mirror of your image storage.
"""

import asyncio
import asyncpg
import os
import json
import subprocess
from datetime import datetime
from typing import List, Dict, Optional
import logging
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Import configuration from config module
from config import DATABASE_URL, AZURE_STORAGE_ACCOUNT, AZURE_STORAGE_CONTAINER

# Azure Storage configuration
SOURCE_ACCOUNT = AZURE_STORAGE_ACCOUNT
SOURCE_CONTAINER = AZURE_STORAGE_CONTAINER
DEST_ACCOUNT = AZURE_STORAGE_ACCOUNT  # Default to same account
DEST_CONTAINER = 'product-images-backup'  # Default destination container

# Allow override via environment variables
import os
if os.getenv('DEST_ACCOUNT'):
    DEST_ACCOUNT = os.getenv('DEST_ACCOUNT')
if os.getenv('DEST_CONTAINER'):
    DEST_CONTAINER = os.getenv('DEST_CONTAINER')

# Threading configuration - much more aggressive for faster processing
MAX_WORKERS = int(os.getenv('MAX_WORKERS', '50'))  # Increased from 10 to 50

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'copy_images_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def get_all_image_urls_from_database() -> List[Dict]:
    """Get all image URLs from the database."""
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Get all products with thomann_main images
        rows = await conn.fetch("""
            SELECT id, name, sku, images
            FROM products 
            WHERE images -> 'thomann_main' ->> 'url' IS NOT NULL
            AND images -> 'thomann_main' ->> 'url' != ''
            AND images -> 'thomann_main' ->> 'url' != 'null'
            ORDER BY id
        """)
        
        image_data = []
        for row in rows:
            try:
                images = row['images']
                if isinstance(images, str):
                    images = json.loads(images)
                
                thomann_main = images.get('thomann_main', {})
                url = thomann_main.get('url', '')
                
                if url and url.startswith('https://getyourmusicgear.blob.core.windows.net/'):
                    # Extract blob path from URL
                    parsed_url = urlparse(url)
                    blob_path = parsed_url.path.lstrip('/')
                    
                    image_data.append({
                        'id': row['id'],
                        'name': row['name'],
                        'sku': row['sku'],
                        'source_url': url,
                        'blob_path': blob_path,
                        'blob_name': blob_path.split('/')[-1]
                    })
                    
            except Exception as e:
                logger.warning(f"Error processing product {row['id']}: {e}")
                continue
        
        logger.info(f"Found {len(image_data)} products with valid image URLs")
        return image_data
        
    finally:
        await conn.close()

def check_blob_exists_in_source(blob_path: str) -> bool:
    """Check if a blob exists in the source container."""
    
    try:
        result = subprocess.run([
            'az', 'storage', 'blob', 'exists',
            '--container-name', SOURCE_CONTAINER,
            '--account-name', SOURCE_ACCOUNT,
            '--name', blob_path,
            '--query', 'exists',
            '--output', 'tsv'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip().lower() == 'true'
        return False
        
    except Exception as e:
        logger.error(f"Error checking blob existence: {e}")
        return False

def check_blob_exists_in_dest(blob_path: str) -> bool:
    """Check if a blob already exists in the destination container."""
    
    try:
        result = subprocess.run([
            'az', 'storage', 'blob', 'exists',
            '--container-name', DEST_CONTAINER,
            '--account-name', DEST_ACCOUNT,
            '--name', blob_path,
            '--query', 'exists',
            '--output', 'tsv'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip().lower() == 'true'
        return False
        
    except Exception as e:
        logger.error(f"Error checking destination blob existence: {e}")
        return False

def copy_blob_to_destination(blob_path: str) -> Dict:
    """Copy a single blob from source to destination container using synchronous copy."""
    
    try:
        # Use az storage blob copy start for asynchronous but reliable copying
        result = subprocess.run([
            'az', 'storage', 'blob', 'copy', 'start',
            '--source-account-name', SOURCE_ACCOUNT,
            '--source-container', SOURCE_CONTAINER,
            '--source-blob', blob_path,
            '--account-name', DEST_ACCOUNT,
            '--destination-container', DEST_CONTAINER,
            '--destination-blob', blob_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            # Wait for copy to complete
            import time
            max_wait = 60  # Wait up to 60 seconds
            
            for _ in range(max_wait):
                time.sleep(1)
                
                # Check copy status
                status_result = subprocess.run([
                    'az', 'storage', 'blob', 'show',
                    '--container-name', DEST_CONTAINER,
                    '--account-name', DEST_ACCOUNT,
                    '--name', blob_path,
                    '--query', 'properties.copy.status',
                    '--output', 'tsv'
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if status_result.returncode == 0:
                    status = status_result.stdout.strip()
                    if status == 'success':
                        return {
                            'status': 'copy_completed',
                            'blob_path': blob_path,
                            'message': 'Copy completed successfully'
                        }
                    elif status == 'failed':
                        return {
                            'status': 'copy_failed',
                            'blob_path': blob_path,
                            'error': 'Copy operation failed'
                        }
                    # If still pending, continue waiting
            
            return {
                'status': 'copy_failed',
                'blob_path': blob_path,
                'error': 'Copy operation timed out'
            }
        else:
            return {
                'status': 'copy_failed',
                'blob_path': blob_path,
                'error': result.stderr
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'blob_path': blob_path,
            'error': str(e)
        }

def copy_blob_with_azcopy(blob_path: str) -> Dict:
    """Fast copy using azcopy - much faster than Azure CLI."""
    
    try:
        # Construct source and destination URLs
        source_url = f"https://{SOURCE_ACCOUNT}.blob.core.windows.net/{SOURCE_CONTAINER}/{blob_path}"
        dest_url = f"https://{DEST_ACCOUNT}.blob.core.windows.net/{DEST_CONTAINER}/{blob_path}"
        
        # Use azcopy with optimized settings for speed
        result = subprocess.run([
            'azcopy', 'cp', source_url, dest_url,
            '--recursive=false',
            '--overwrite=ifSourceNewer',
            '--log-level=ERROR',  # Reduce logging overhead
            '--check-md5=LogOnly'  # Skip MD5 verification for speed
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            return {
                'status': 'copy_completed',
                'blob_path': blob_path,
                'message': 'Copy completed with azcopy (fast)'
            }
        else:
            return {
                'status': 'copy_failed',
                'blob_path': blob_path,
                'error': result.stderr
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'blob_path': blob_path,
            'error': str(e)
        }

def copy_blob_fast(blob_path: str) -> Dict:
    """Try azcopy first, fallback to Azure CLI if needed."""
    
    # Try azcopy first (much faster)
    azcopy_result = copy_blob_with_azcopy(blob_path)
    if azcopy_result['status'] == 'copy_completed':
        return azcopy_result
    
    # Fallback to Azure CLI if azcopy fails
    return copy_blob_to_destination(blob_path)

def process_single_image_threaded(image_data: Dict) -> Dict:
    """Process a single image for copying using threads."""
    
    product_id = image_data['id']
    name = image_data['name']
    blob_path = image_data['blob_path']
    
    try:
        # Check if source blob exists
        if not check_blob_exists_in_source(blob_path):
            return {
                'id': product_id,
                'name': name,
                'blob_path': blob_path,
                'status': 'source_not_found',
                'error': 'Source blob does not exist'
            }
        
        # Check if already exists in destination
        if check_blob_exists_in_dest(blob_path):
            return {
                'id': product_id,
                'name': name,
                'blob_path': blob_path,
                'status': 'already_exists',
                'message': 'Blob already exists in destination'
            }
        
        # Use fast copy method (azcopy first, Azure CLI fallback)
        copy_result = copy_blob_fast(blob_path)
        
        if copy_result['status'] == 'copy_completed':
            return {
                'id': product_id,
                'name': name,
                'blob_path': blob_path,
                'status': 'copy_completed',
                'message': copy_result['message']
            }
        else:
            return {
                'id': product_id,
                'name': name,
                'blob_path': blob_path,
                'status': 'copy_failed',
                'error': copy_result['error']
            }
                
    except Exception as e:
        return {
            'id': product_id,
            'name': name,
            'blob_path': blob_path,
            'status': 'error',
            'error': str(e)
        }

async def process_single_image(image_data: Dict) -> Dict:
    """Process a single image for copying."""
    
    product_id = image_data['id']
    name = image_data['name']
    blob_path = image_data['blob_path']
    
    try:
        # Check if source blob exists
        if not check_blob_exists_in_source(blob_path):
            return {
                'id': product_id,
                'name': name,
                'blob_path': blob_path,
                'status': 'source_not_found',
                'error': 'Source blob does not exist'
            }
        
        # Check if already exists in destination
        if check_blob_exists_in_dest(blob_path):
            return {
                'id': product_id,
                'name': name,
                'blob_path': blob_path,
                'status': 'already_exists',
                'message': 'Blob already exists in destination'
            }
        
        # Try to copy the blob
        copy_success = copy_blob_to_destination(blob_path)
        
        if copy_success:
            return {
                'id': product_id,
                'name': name,
                'blob_path': blob_path,
                'status': 'copy_started',
                'message': 'Copy operation started successfully'
            }
        else:
            # Try azcopy as fallback
            azcopy_success = copy_blob_with_azcopy(blob_path)
            
            if azcopy_success:
                return {
                    'id': product_id,
                    'name': name,
                    'blob_path': blob_path,
                    'status': 'copy_completed',
                    'message': 'Copy completed with azcopy'
                }
            else:
                return {
                    'id': product_id,
                    'name': name,
                    'blob_path': blob_path,
                    'status': 'copy_failed',
                    'error': 'Both copy methods failed'
                }
                
    except Exception as e:
        logger.error(f"Error processing image for product {product_id}: {e}")
        return {
            'id': product_id,
            'name': name,
            'blob_path': blob_path,
            'status': 'error',
            'error': str(e)
        }

async def create_destination_container():
    """Create the destination container if it doesn't exist."""
    
    try:
        # Check if container exists
        result = subprocess.run([
            'az', 'storage', 'container', 'exists',
            '--account-name', DEST_ACCOUNT,
            '--name', DEST_CONTAINER,
            '--query', 'exists',
            '--output', 'tsv'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0 and result.stdout.strip().lower() == 'true':
            logger.info(f"Destination container {DEST_CONTAINER} already exists")
            return True
        
        # Create container
        logger.info(f"Creating destination container {DEST_CONTAINER}...")
        result = subprocess.run([
            'az', 'storage', 'container', 'create',
            '--account-name', DEST_ACCOUNT,
            '--name', DEST_CONTAINER,
            '--public-access', 'blob'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            logger.info(f"Successfully created container {DEST_CONTAINER}")
            return True
        else:
            logger.error(f"Failed to create container: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Error creating destination container: {e}")
        return False

async def main():
    """Main function."""
    
    if not DATABASE_URL:
        logger.error("DATABASE_URL environment variable not set")
        return
    
    logger.info("🚀 STARTING IMAGE COPY TO DIFFERENT CONTAINER")
    logger.info(f"Source: {SOURCE_ACCOUNT}/{SOURCE_CONTAINER}")
    logger.info(f"Destination: {DEST_ACCOUNT}/{DEST_CONTAINER}")
    
    try:
        # Create destination container if needed
        if not await create_destination_container():
            logger.error("Failed to create destination container. Exiting.")
            return
        
        # Get all image URLs from database
        image_data_list = await get_all_image_urls_from_database()
        
        if not image_data_list:
            logger.info("✅ No images found to copy!")
            return
        
        # Process images using threads for much faster execution
        results = []
        total = len(image_data_list)
        
        # Use configured threading
        logger.info(f"Using {MAX_WORKERS} concurrent threads for faster processing")
        
        logger.info(f"Starting to process {total} images using {MAX_WORKERS} threads...")
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all tasks
            future_to_image = {
                executor.submit(process_single_image_threaded, image_data): image_data 
                for image_data in image_data_list
            }
            
            # Process completed tasks
            completed = 0
            for future in as_completed(future_to_image):
                image_data = future_to_image[future]
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1
                    
                    # Progress update every 50 items
                    if completed % 50 == 0 or completed == total:
                        logger.info(f"📊 Progress: {completed}/{total} ({((completed)/total)*100:.1f}%)")
                        
                except Exception as e:
                    logger.error(f"Error processing {image_data.get('name', 'Unknown')}: {e}")
                    results.append({
                        'id': image_data.get('id'),
                        'name': image_data.get('name'),
                        'blob_path': image_data.get('blob_path'),
                        'status': 'error',
                        'error': str(e)
                    })
                    completed += 1
        
        # Analyze results
        copy_started = sum(1 for r in results if r['status'] == 'copy_started')
        copy_completed = sum(1 for r in results if r['status'] == 'copy_completed')
        already_exists = sum(1 for r in results if r['status'] == 'already_exists')
        source_not_found = sum(1 for r in results if r['status'] == 'source_not_found')
        copy_failed = sum(1 for r in results if r['status'] == 'copy_failed')
        errors = sum(1 for r in results if r['status'] == 'error')
        
        logger.info(f"\n📊 FINAL RESULTS:")
        logger.info(f"🚀 Copy started: {copy_started}")
        logger.info(f"✅ Copy completed: {copy_completed}")
        logger.info(f"⏭️  Already exists: {already_exists}")
        logger.info(f"❌ Source not found: {source_not_found}")
        logger.info(f"💥 Copy failed: {copy_failed}")
        logger.info(f"💥 Errors: {errors}")
        logger.info(f"📋 Total processed: {total}")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"copy_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'source': f"{SOURCE_ACCOUNT}/{SOURCE_CONTAINER}",
                'destination': f"{DEST_ACCOUNT}/{DEST_CONTAINER}",
                'summary': {
                    'total': total,
                    'copy_started': copy_started,
                    'copy_completed': copy_completed,
                    'already_exists': already_exists,
                    'source_not_found': source_not_found,
                    'copy_failed': copy_failed,
                    'errors': errors
                },
                'results': results
            }, f, indent=2)
        
        logger.info(f"📄 Results saved: {results_file}")
        
        # Show next steps
        logger.info(f"\n🚀 NEXT STEPS:")
        logger.info(f"1. Monitor copy progress with: az storage blob list --container-name {DEST_CONTAINER} --account-name {DEST_ACCOUNT}")
        logger.info(f"2. Check copy status for specific blobs")
        logger.info(f"3. Verify copy completion")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

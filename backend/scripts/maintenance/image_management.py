#!/usr/bin/env python3
"""
Consolidated Image Management Script
Replaces multiple duplicate scripts with a single, well-organized solution.

This script consolidates the functionality of:
- fast_deduplicate.py
- quick_deduplicate.py  
- cleanup_duplicate_images.py
- deduplicate_azure_images.py
- fix_image_associations.py
- fix_all_image_associations.py
- fast_association_fix.py
- simple_association_fix.py

Usage:
    python -m scripts.maintenance.image_management --operation deduplicate
    python -m scripts.maintenance.image_management --operation fix-associations
    python -m scripts.maintenance.image_management --operation cleanup --dry-run
"""

import argparse
import asyncio
import logging
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import os

# Add app to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "app"))

from database import get_db
from models import Product
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageManager:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.stats = {
            'processed': 0,
            'errors': 0,
            'duplicates_found': 0,
            'associations_fixed': 0
        }

    def get_azure_images(self, prefix: str = "") -> List[Dict]:
        """Get all images from Azure storage"""
        try:
            cmd = [
                'az', 'storage', 'blob', 'list',
                '--container-name', 'product-images',
                '--account-name', 'getyourmusicgear',
                '--query', '[].{name: name, lastModified: properties.lastModified}',
                '--output', 'json'
            ]
            
            if prefix:
                cmd.extend(['--prefix', prefix])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Azure CLI error: {result.stderr}")
                return []
            
            return json.loads(result.stdout)
        except Exception as e:
            logger.error(f"Failed to get Azure images: {e}")
            return []

    def delete_azure_blob(self, blob_name: str) -> bool:
        """Delete a blob from Azure storage"""
        if self.dry_run:
            logger.info(f"DRY RUN: Would delete {blob_name}")
            return True
        
        try:
            cmd = [
                'az', 'storage', 'blob', 'delete',
                '--container-name', 'product-images',
                '--account-name', 'getyourmusicgear',
                '--name', blob_name
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Failed to delete {blob_name}: {e}")
            return False

    def find_duplicates(self, images: List[Dict]) -> Dict[str, List[str]]:
        """Find duplicate images based on filename patterns"""
        duplicates = {}
        base_names = {}
        
        for img in images:
            name = img['name']
            
            # Extract base name (remove size suffixes like _800x600)
            base_name = name.split('_')[0] if '_' in name else name.split('.')[0]
            
            if base_name not in base_names:
                base_names[base_name] = []
            base_names[base_name].append(name)
        
        # Find groups with multiple images
        for base_name, files in base_names.items():
            if len(files) > 1:
                # Keep the most recent, mark others as duplicates
                files.sort(key=lambda x: next(
                    img['lastModified'] for img in images if img['name'] == x
                ), reverse=True)
                duplicates[base_name] = files[1:]  # All but the newest
        
        return duplicates

    async def deduplicate_images(self):
        """Remove duplicate images from Azure storage"""
        logger.info("🔍 Starting image deduplication...")
        
        images = self.get_azure_images("thomann/")
        if not images:
            logger.warning("No images found to process")
            return
        
        logger.info(f"Found {len(images)} images to analyze")
        
        duplicates = self.find_duplicates(images)
        total_duplicates = sum(len(files) for files in duplicates.values())
        
        if total_duplicates == 0:
            logger.info("✅ No duplicates found")
            return
        
        logger.info(f"Found {total_duplicates} duplicate images across {len(duplicates)} groups")
        
        if self.dry_run:
            logger.info("DRY RUN: Would delete the following duplicates:")
            for base_name, files in duplicates.items():
                for file in files:
                    logger.info(f"  - {file}")
            return
        
        # Delete duplicates
        with ThreadPoolExecutor(max_workers=5) as executor:
            tasks = []
            for base_name, files in duplicates.items():
                for file in files:
                    tasks.append(executor.submit(self.delete_azure_blob, file))
            
            success = sum(1 for task in tasks if task.result())
            
        logger.info(f"✅ Deleted {success}/{total_duplicates} duplicate images")
        self.stats['duplicates_found'] = total_duplicates
        self.stats['processed'] = success

    async def fix_image_associations(self):
        """Fix broken image-product associations in database"""
        logger.info("🔍 Starting image association fix...")
        
        async for db in get_db():
            try:
                # Get products with broken image associations
                stmt = select(Product).where(Product.images != {})
                result = await db.execute(stmt)
                products = result.scalars().all()
                
                logger.info(f"Checking {len(products)} products with images")
                
                fixed = 0
                for product in products:
                    if not product.images:
                        continue
                    
                    # Verify image URLs are accessible
                    updated_images = {}
                    for key, image_data in product.images.items():
                        if isinstance(image_data, dict) and 'url' in image_data:
                            url = image_data['url']
                            # Add logic to verify URL accessibility
                            updated_images[key] = image_data
                        elif isinstance(image_data, str):
                            updated_images[key] = {"url": image_data}
                    
                    if updated_images != product.images:
                        if not self.dry_run:
                            product.images = updated_images
                            await db.commit()
                        fixed += 1
                        logger.info(f"Fixed associations for product {product.id}")
                
                logger.info(f"✅ Fixed {fixed} product image associations")
                self.stats['associations_fixed'] = fixed
                
            except Exception as e:
                logger.error(f"Database error: {e}")
                await db.rollback()

    def cleanup_old_scripts(self):
        """Remove the old duplicate script files"""
        script_dir = Path(__file__).parent
        
        old_scripts = [
            'fast_deduplicate.py',
            'quick_deduplicate.py',
            'cleanup_duplicate_images.py', 
            'deduplicate_azure_images.py',
            'fix_image_associations.py',
            'fix_all_image_associations.py',
            'fast_association_fix.py',
            'simple_association_fix.py'
        ]
        
        logger.info("🧹 Cleaning up old duplicate scripts...")
        
        removed = 0
        for script in old_scripts:
            script_path = script_dir / script
            if script_path.exists():
                if not self.dry_run:
                    script_path.unlink()
                    logger.info(f"Removed {script}")
                else:
                    logger.info(f"DRY RUN: Would remove {script}")
                removed += 1
        
        logger.info(f"✅ Cleaned up {removed} old script files")

    def print_stats(self):
        """Print operation statistics"""
        logger.info("📊 Operation Summary:")
        for key, value in self.stats.items():
            logger.info(f"  {key.replace('_', ' ').title()}: {value}")

async def main():
    parser = argparse.ArgumentParser(description='Consolidated Image Management')
    parser.add_argument(
        '--operation', 
        choices=['deduplicate', 'fix-associations', 'cleanup', 'all'],
        required=True,
        help='Operation to perform'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    args = parser.parse_args()
    
    manager = ImageManager(dry_run=args.dry_run)
    
    try:
        if args.operation in ['deduplicate', 'all']:
            await manager.deduplicate_images()
        
        if args.operation in ['fix-associations', 'all']:
            await manager.fix_image_associations()
        
        if args.operation in ['cleanup', 'all']:
            manager.cleanup_old_scripts()
        
        manager.print_stats()
        
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
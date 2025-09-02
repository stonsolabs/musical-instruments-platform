#!/usr/bin/env python3
"""
Associate Images by Product ID Script
Easy association of Azure Storage images with database records using product ID.
Works with the new naming convention: thomann/{product_id}_{timestamp}.jpg
"""

import asyncio
import asyncpg
import json
import os
import re
from azure.storage.blob import BlobServiceClient
from typing import Dict, List
from dotenv import load_dotenv
from datetime import datetime

class ImageAssociatorByID:
    def __init__(self):
        load_dotenv()
        
        # Database connection
        self.db_url = os.getenv('DATABASE_URL')
        if not self.db_url:
            raise ValueError("DATABASE_URL not found in environment variables")
        
        # Azure Storage connection
        self.storage_connection = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if not self.storage_connection:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING not found in environment variables")
        
        self.container_name = os.getenv('AZURE_STORAGE_CONTAINER', 'product-images')
        self.blob_client = BlobServiceClient.from_connection_string(self.storage_connection)
    
    def get_images_by_product_id(self) -> Dict[int, List[Dict]]:
        """Get all Thomann images grouped by product ID"""
        container_client = self.blob_client.get_container_client(self.container_name)
        
        images_by_id = {}
        blob_list = container_client.list_blobs(name_starts_with="thomann/")
        
        for blob in blob_list:
            # Extract info from blob name: thomann/{product_id}_{timestamp}.jpg
            blob_name = blob.name
            match = re.match(r'thomann/(\d+)_(\d{8}_\d{6})\.jpg$', blob_name)
            
            if match:
                product_id = int(match.group(1))
                timestamp = match.group(2)
                
                if product_id not in images_by_id:
                    images_by_id[product_id] = []
                
                images_by_id[product_id].append({
                    'blob_name': blob_name,
                    'product_id': product_id,
                    'timestamp': timestamp,
                    'timestamp_dt': datetime.strptime(timestamp, '%Y%m%d_%H%M%S'),
                    'size': blob.size,
                    'last_modified': blob.last_modified,
                    'url': f"https://{self.blob_client.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}"
                })
        
        return images_by_id
    
    async def get_products_needing_association(self, product_ids: List[int]) -> List[Dict]:
        """Get products that need image association"""
        conn = await asyncpg.connect(self.db_url)
        try:
            # Convert list to tuple for SQL IN clause
            id_tuple = tuple(product_ids)
            
            query = """
            SELECT 
                p.id,
                p.sku,
                p.name,
                p.content,
                p.images
            FROM products p
            WHERE p.id = ANY($1)
            AND (p.images IS NULL 
                 OR p.images = '{}' 
                 OR p.images = 'null' 
                 OR p.images->>'thomann_main' IS NULL)
            """
            
            rows = await conn.fetch(query, product_ids)
            
            products = []
            for row in rows:
                # Parse content if it's a string
                content = row['content'] or {}
                if isinstance(content, str):
                    try:
                        content = json.loads(content)
                    except (json.JSONDecodeError, TypeError):
                        content = {}
                
                # Extract Thomann URL
                thomann_url = content.get('store_links', {}).get('Thomann', '')
                
                products.append({
                    'id': row['id'],
                    'sku': row['sku'],
                    'name': row['name'],
                    'thomann_url': thomann_url,
                    'images': row['images'] or {}
                })
            
            return products
            
        finally:
            await conn.close()
    
    async def update_product_image_association(self, product_id: int, image_url: str, thomann_url: str) -> bool:
        """Update the database with the image association"""
        conn = await asyncpg.connect(self.db_url)
        try:
            # Create the image metadata structure
            image_data = {
                "thomann_main": {
                    "url": image_url,
                    "source": "thomann",
                    "source_url": thomann_url,
                    "downloaded_at": datetime.utcnow().isoformat(),
                    "type": "main_product_image"
                }
            }
            
            # Update the images column
            update_query = """
                UPDATE products 
                SET images = $1, updated_at = NOW()
                WHERE id = $2
            """
            
            await conn.execute(update_query, json.dumps(image_data), product_id)
            return True
            
        except Exception as e:
            print(f"❌ Error updating product {product_id}: {e}")
            return False
        finally:
            await conn.close()
    
    async def associate_images(self, dry_run: bool = True):
        """Main function to associate images by product ID"""
        print("🔗 Starting Image Association by Product ID...")
        print("=" * 60)
        
        if dry_run:
            print("🧪 DRY RUN MODE - No database changes will be made")
        else:
            print("⚡ LIVE MODE - Database will be updated")
        print()
        
        # Get images grouped by product ID
        print("☁️ Fetching images from Azure Storage...")
        images_by_id = self.get_images_by_product_id()
        
        # Get products that need association
        print("📊 Checking which products need association...")
        product_ids = list(images_by_id.keys())
        products = await self.get_products_needing_association(product_ids)
        
        # Create lookup
        products_by_id = {p['id']: p for p in products}
        
        # Find matches
        associations_needed = []
        for product_id, images in images_by_id.items():
            if product_id in products_by_id:
                # Get the most recent image
                latest_image = max(images, key=lambda x: x['timestamp_dt'])
                
                associations_needed.append({
                    'product': products_by_id[product_id],
                    'image': latest_image,
                    'total_images': len(images)
                })
        
        print(f"📈 ANALYSIS RESULTS:")
        print(f"Total images in storage: {sum(len(imgs) for imgs in images_by_id.values())}")
        print(f"Unique products with images: {len(images_by_id)}")
        print(f"Products needing association: {len(associations_needed)}")
        print()
        
        if not associations_needed:
            print("✅ No products need association!")
            return
        
        print(f"🔗 Products to be associated (showing first 10):")
        for i, item in enumerate(associations_needed[:10], 1):
            product = item['product']
            image = item['image']
            print(f"  {i:2d}. ID:{product['id']} - {product['name'][:50]}...")
            print(f"      └── Image: {image['blob_name']} ({item['total_images']} total)")
        
        if len(associations_needed) > 10:
            print(f"      ... and {len(associations_needed) - 10} more")
        
        print()
        
        if dry_run:
            print("🧪 DRY RUN - No changes made. Run with --live to apply associations.")
            return
        
        # Confirm before proceeding
        print("⚠️  This will update the database with image associations.")
        print("   Type 'yes' to proceed:")
        
        proceed = input().strip().lower()
        if proceed != 'yes':
            print("❌ Operation cancelled.")
            return
        
        # Apply the associations
        print("\n🔄 Applying associations...")
        success_count = 0
        error_count = 0
        
        for i, item in enumerate(associations_needed, 1):
            product = item['product']
            image = item['image']
            
            print(f"  [{i:3d}/{len(associations_needed)}] Associating product {product['id']}...")
            
            success = await self.update_product_image_association(
                product['id'], 
                image['url'], 
                product['thomann_url']
            )
            
            if success:
                success_count += 1
                print(f"      ✅ Success")
            else:
                error_count += 1
                print(f"      ❌ Failed")
        
        print(f"\n🎯 RESULTS:")
        print(f"✅ Successfully associated: {success_count}")
        print(f"❌ Errors: {error_count}")
        print(f"📊 Success rate: {(success_count/len(associations_needed)*100):.1f}%")
        
        if success_count > 0:
            print(f"\n✨ Database updated! {success_count} products now have image associations.")

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Associate images with database records by product ID')
    parser.add_argument('--live', action='store_true', help='Actually update the database (default is dry-run)')
    parser.add_argument('--auto-confirm', action='store_true', help='Skip confirmation prompt for automation')
    
    args = parser.parse_args()
    
    associator = ImageAssociatorByID()
    
    # Override input for automation
    if args.auto_confirm and args.live:
        import builtins
        original_input = builtins.input
        builtins.input = lambda x='': 'yes'
        
        try:
            await associator.associate_images(dry_run=False)
        finally:
            builtins.input = original_input
    else:
        await associator.associate_images(dry_run=not args.live)

if __name__ == "__main__":
    asyncio.run(main())

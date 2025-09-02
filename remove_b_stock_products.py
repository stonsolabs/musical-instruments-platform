#!/usr/bin/env python3.11
"""
Script to safely remove B-Stock products from the database.
Creates a backup before deletion and shows impact statistics.
"""

import asyncio
import asyncpg
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class BStockRemover:
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        if not self.db_url:
            raise ValueError("DATABASE_URL environment variable not set")
    
    async def backup_b_stock_products(self):
        """Create a backup of B-Stock products before deletion"""
        conn = await asyncpg.connect(self.db_url)
        try:
            print("📦 Creating backup of B-Stock products...")
            
            # Fetch all B-Stock products
            b_stock_products = await conn.fetch('''
                SELECT *
                FROM products 
                WHERE 
                    LOWER(name) LIKE '%b-stock%' 
                    OR LOWER(sku) LIKE '%b_stock%'
                    OR LOWER(content->'store_links'->>'Thomann') LIKE '%b_stock%'
                ORDER BY id
            ''')
            
            # Convert to JSON-serializable format
            backup_data = []
            for product in b_stock_products:
                product_dict = dict(product)
                # Convert datetime objects to strings
                if 'created_at' in product_dict and product_dict['created_at']:
                    product_dict['created_at'] = product_dict['created_at'].isoformat()
                if 'updated_at' in product_dict and product_dict['updated_at']:
                    product_dict['updated_at'] = product_dict['updated_at'].isoformat()
                # Convert Decimal to float for JSON serialization
                if 'msrp_price' in product_dict and product_dict['msrp_price']:
                    product_dict['msrp_price'] = float(product_dict['msrp_price'])
                if 'avg_rating' in product_dict and product_dict['avg_rating']:
                    product_dict['avg_rating'] = float(product_dict['avg_rating'])
                backup_data.append(product_dict)
            
            # Save backup to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"b_stock_products_backup_{timestamp}.json"
            
            with open(backup_filename, 'w') as f:
                json.dump({
                    'backup_date': datetime.now().isoformat(),
                    'total_products': len(backup_data),
                    'products': backup_data
                }, f, indent=2, default=str)
            
            print(f"✅ Backup saved to: {backup_filename}")
            print(f"📊 Backed up {len(backup_data)} B-Stock products")
            
            return len(backup_data)
            
        finally:
            await conn.close()
    
    async def analyze_impact(self):
        """Analyze the impact of removing B-Stock products"""
        conn = await asyncpg.connect(self.db_url)
        try:
            print("\n🔍 Analyzing removal impact...")
            
            # Current statistics
            current_stats = await conn.fetchrow('''
                SELECT 
                    COUNT(*) as total_products,
                    COUNT(CASE WHEN images IS NOT NULL AND images != '{}' AND images != 'null' THEN 1 END) as with_images
                FROM products
            ''')
            
            # B-Stock statistics
            b_stock_stats = await conn.fetchrow('''
                SELECT 
                    COUNT(*) as total_b_stock,
                    COUNT(CASE WHEN images IS NOT NULL AND images != '{}' AND images != 'null' THEN 1 END) as b_stock_with_images
                FROM products 
                WHERE 
                    LOWER(name) LIKE '%b-stock%' 
                    OR LOWER(sku) LIKE '%b_stock%'
                    OR LOWER(content->'store_links'->>'Thomann') LIKE '%b_stock%'
            ''')
            
            # Calculate after-removal statistics
            remaining_products = current_stats['total_products'] - b_stock_stats['total_b_stock']
            remaining_with_images = current_stats['with_images'] - b_stock_stats['b_stock_with_images']
            
            print(f"\n📊 BEFORE REMOVAL:")
            print(f"   Total products: {current_stats['total_products']:,}")
            print(f"   Products with images: {current_stats['with_images']:,} ({current_stats['with_images']/current_stats['total_products']*100:.1f}%)")
            
            print(f"\n📊 B-STOCK TO REMOVE:")
            print(f"   Total B-Stock: {b_stock_stats['total_b_stock']:,}")
            print(f"   B-Stock with images: {b_stock_stats['b_stock_with_images']:,}")
            print(f"   B-Stock without images: {b_stock_stats['total_b_stock'] - b_stock_stats['b_stock_with_images']:,}")
            
            print(f"\n📊 AFTER REMOVAL:")
            print(f"   Total products: {remaining_products:,}")
            print(f"   Products with images: {remaining_with_images:,} ({remaining_with_images/remaining_products*100:.1f}%)")
            
            print(f"\n✨ IMPROVEMENT:")
            old_percentage = current_stats['with_images']/current_stats['total_products']*100
            new_percentage = remaining_with_images/remaining_products*100
            improvement = new_percentage - old_percentage
            print(f"   Image coverage: {old_percentage:.1f}% → {new_percentage:.1f}% (+{improvement:.1f}%)")
            
            return b_stock_stats['total_b_stock']
            
        finally:
            await conn.close()
    
    async def remove_b_stock_products(self, dry_run=True):
        """Remove B-Stock products from the database"""
        conn = await asyncpg.connect(self.db_url)
        try:
            if dry_run:
                print("\n🧪 DRY RUN MODE - No products will be deleted")
                return 0
            
            print("\n🗑️  Removing B-Stock products...")
            
            # Delete B-Stock products
            result = await conn.execute('''
                DELETE FROM products 
                WHERE 
                    LOWER(name) LIKE '%b-stock%' 
                    OR LOWER(sku) LIKE '%b_stock%'
                    OR LOWER(content->'store_links'->>'Thomann') LIKE '%b_stock%'
            ''')
            
            # Extract number of deleted rows
            deleted_count = int(result.split()[-1])
            
            print(f"✅ Successfully removed {deleted_count:,} B-Stock products")
            
            return deleted_count
            
        finally:
            await conn.close()
    
    async def run(self, dry_run=True):
        """Run the complete B-Stock removal process"""
        print("🧹 B-Stock Products Removal Tool")
        print("=" * 50)
        
        try:
            # Create backup
            backup_count = await self.backup_b_stock_products()
            
            # Analyze impact
            b_stock_count = await self.analyze_impact()
            
            # Remove products
            deleted_count = await self.remove_b_stock_products(dry_run=dry_run)
            
            if dry_run:
                print(f"\n🧪 DRY RUN COMPLETE")
                print(f"📦 {backup_count:,} products backed up")
                print(f"🗑️  {b_stock_count:,} products ready for removal")
                print(f"\n💡 To actually remove B-Stock products, run:")
                print(f"   python3.11 remove_b_stock_products.py --live")
            else:
                print(f"\n✅ REMOVAL COMPLETE")
                print(f"📦 {backup_count:,} products backed up")
                print(f"🗑️  {deleted_count:,} products removed")
                print(f"\n🎸 Your database is now cleaner and more focused!")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            raise

async def main():
    import sys
    
    # Check for --live flag
    live_mode = '--live' in sys.argv
    
    if live_mode:
        print("⚠️  LIVE MODE - Products will be permanently deleted!")
        response = input("Are you sure you want to remove all B-Stock products? (yes/no): ")
        if response.lower() != 'yes':
            print("🛑 Operation cancelled")
            return
    
    remover = BStockRemover()
    await remover.run(dry_run=not live_mode)

if __name__ == "__main__":
    asyncio.run(main())

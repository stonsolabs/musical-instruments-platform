#!/usr/bin/env python3
"""
Database Manager for PostgreSQL
Saves crawled products to Azure PostgreSQL database
"""

import os
import asyncio
import asyncpg
from datetime import datetime
from typing import Dict, Optional, List

class DatabaseManager:
    """Database manager for PostgreSQL"""
    
    def __init__(self):
        # Prioritize Azure database URL from .env file
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check if we have Azure database URL in .env file
        azure_db_url = None
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('DATABASE_URL=') and 'getyourmusicgear' in line:
                        azure_db_url = line.split('=', 1)[1].strip()
                        break
        except:
            pass
        
        self.database_url = azure_db_url or os.getenv('DATABASE_URL')
        self.conn = None
        
        if not self.database_url:
            print("⚠️  WARNING: DATABASE_URL not found. Using in-memory storage only.")
            self.in_memory_urls = set()
        else:
            print(f"🔍 Using database: {self.database_url[:50]}...")
    
    async def __aenter__(self):
        """Async context manager entry"""
        if self.database_url:
            try:
                # Fix DSN format for asyncpg (remove +asyncpg suffix if present)
                fixed_url = self.database_url.replace('postgresql+asyncpg://', 'postgresql://')
                self.conn = await asyncpg.connect(fixed_url)
                await self._create_tables()
                print("✅ Connected to PostgreSQL database")
            except Exception as e:
                print(f"❌ Failed to connect to database: {e}")
                print("⚠️  Falling back to in-memory storage")
                self.database_url = None
                self.in_memory_urls = set()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.conn:
            await self.conn.close()
    
    async def _create_tables(self):
        """Check if products table exists and has correct structure"""
        # Check if table exists
        table_exists = await self.conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'products'
            );
        """)
        
        if not table_exists:
            print("❌ Products table does not exist. Please create it first.")
            return
        
        # Check if we have the columns we need
        columns = await self.conn.fetch("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'products'
        """)
        
        column_names = [row['column_name'] for row in columns]
        
        # We need at least: id, name, sku, brand_id, category_id
        required_columns = ['id', 'name', 'sku', 'brand_id', 'category_id']
        missing_columns = [col for col in required_columns if col not in column_names]
        
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            return
        
        # Check if we need to add the 'url' column
        if 'url' not in column_names:
            print("⚠️ Adding missing 'url' column to products table...")
            try:
                await self.conn.execute("ALTER TABLE products ADD COLUMN url TEXT")
                print("✅ Added 'url' column to products table")
            except Exception as e:
                print(f"⚠️ Could not add 'url' column: {e}")
        
        print("✅ Products table structure is compatible")
    
    async def product_exists(self, url: str) -> bool:
        """Check if product URL has been crawled"""
        if not self.database_url or not self.conn:
            return url in getattr(self, 'in_memory_urls', set())
        
        try:
            # Check by URL first, then by SKU as fallback
            exists = await self.conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM products WHERE url = $1)",
                url
            )
            
            if not exists:
                # Fallback: check by SKU
                sku = url.split('/')[-1] if url else 'unknown'
                exists = await self.conn.fetchval(
                    "SELECT EXISTS(SELECT 1 FROM products WHERE sku = $1)",
                    sku
                )
            
            return exists
        except Exception as e:
            print(f"❌ Error checking product existence: {e}")
            return False
    
    async def save_product(self, url: str, name: str, brand: str, description: str, 
                          specifications: Dict, images: List[str], price: str, json_ld: Dict) -> bool:
        """Save product to database, return True if saved, False if already exists"""
        if not self.database_url or not self.conn:
            print("❌ No database connection available")
            return False
        
        try:
            # Clean and validate price
            if price and price.strip():
                # Remove currency symbols and clean up
                price = price.replace('£', '').replace('€', '').replace('$', '').replace(',', '').strip()
                try:
                    price = float(price)
                except ValueError:
                    price = 0.0
            else:
                price = 0.0
            
            # Use the category_id from the crawler context
            category_id = getattr(self, 'current_category_id', 0)  # Default to 0 if not set
            
            # Try to extract brand_id from brand name or use a mapping
            brand_id = self._get_brand_id(brand)
            
            # Create SKU from URL
            sku = url.split('/')[-1].split('?')[0].replace('.html', '')
            if not sku:
                sku = f"product_{hash(url) % 1000000}"
            
            # Create a unique slug from the SKU to avoid conflicts
            slug = sku.lower().replace('_', '-').replace('.', '-')[:100]
            
            # Convert specifications to JSON
            specifications_json = json.dumps(specifications) if specifications else '{}'
            
            # Convert JSON-LD to string
            json_ld_json = json.dumps(json_ld) if json_ld else '{}'
            
            # First check if product already exists
            result = await self.conn.fetchrow("SELECT id FROM products WHERE sku = $1 OR slug = $2", sku, slug)
            if result:
                print(f"⏭️ Product already exists, skipping: {name} (SKU: {sku})")
                return False
            
            # Insert new product only
            await self.conn.execute("""
                INSERT INTO products (
                    sku, name, slug, brand_id, category_id, description, 
                    specifications, images, msrp_price, ai_generated_content, 
                    avg_rating, review_count, is_active, created_at, updated_at,
                    openai_processing_status, category_attributes, url
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, $14, $15, $16)
            """, sku, name, slug, brand_id, category_id, description, 
                 specifications_json, images, price, json_ld_json, 0, 0, True, 'pending', '{}', url)
            
            print(f"✅ Successfully saved NEW product: {name} (SKU: {sku}, Category: {category_id}, Brand: {brand_id})")
            return True
            
        except Exception as e:
            print(f"❌ Error saving product to database: {e}")
            print(f"   URL: {url}")
            print(f"   SKU: {sku}")
            print(f"   Name: {name}")
            # Save to in-memory as fallback
            getattr(self, 'in_memory_urls', set()).add(url)
            return False
    
    def _get_brand_id(self, brand_name: str) -> int:
        """Get brand_id based on brand name"""
        if not brand_name:
            return 1
        
        # Simple brand mapping - in a real implementation, you'd have a brands table
        brand_mapping = {
            'fender': 2,
            'gibson': 3,
            'ibanez': 4,
            'yamaha': 5,
            'roland': 6,
            'korg': 7,
            'casio': 8,
            'martin': 9,
            'taylor': 10,
            'prs': 11,
            'esp': 12,
            'schecter': 13,
            'jackson': 14,
            'gretsch': 15,
            'epiphone': 16,
            'squier': 17,
            'harley benton': 18,
            'cort': 19,
            'godin': 20,
            'guild': 21,
            'höfner': 22,
            'kramer': 23,
            'music man': 24,
            'suhr': 25,
            'takamine': 26,
            'thomann': 27,
            'alesis': 28,
            'arturia': 29,
            'behringer': 30,
            'clavia nord': 31,
            'kurzweil': 32,
            'moog': 33,
            'novation': 34,
            'akai professional': 35,
            'kawai': 36,
            'm-audio': 37,
            'native instruments': 38,
            'nux': 39,
            'mellotron': 40,
            'rhodes': 41,
            'charvel': 42,
            'marcus miller': 43,
        }
        
        # Try exact match first
        brand_lower = brand_name.lower().strip()
        if brand_lower in brand_mapping:
            return brand_mapping[brand_lower]
        
        # Try partial matches
        for brand_key, brand_id in brand_mapping.items():
            if brand_key in brand_lower or brand_lower in brand_key:
                return brand_id
        
        # Default to 1 for unknown brands
        return 1
    
    async def get_stats(self) -> Dict:
        """Get database statistics"""
        if not self.database_url or not self.conn:
            return {"total": len(getattr(self, 'in_memory_urls', set()))}
        
        try:
            stats = {}
            
            # Total count
            stats['total'] = await self.conn.fetchval("SELECT COUNT(*) FROM products")
            
            # By brand_id
            brands = await self.conn.fetch("""
                SELECT brand_id, COUNT(*) as count 
                FROM products 
                GROUP BY brand_id
            """)
            stats['by_brand'] = {f"brand_{row['brand_id']}": row['count'] for row in brands}
            
            # By category_id
            categories = await self.conn.fetch("""
                SELECT category_id, COUNT(*) as count 
                FROM products 
                WHERE category_id IS NOT NULL
                GROUP BY category_id
            """)
            stats['by_category'] = {f"category_{row['category_id']}": row['count'] for row in categories}
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting database stats: {e}")
            return {"error": str(e)}

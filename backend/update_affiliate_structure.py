#!/usr/bin/env python3
"""
Script to update existing blog posts with enhanced affiliate link structure
Add store_url and cta_text to existing product spotlights
"""

import asyncio
import json
import re
from typing import Dict, List, Any
from sqlalchemy import text
from app.database import async_session_factory

class AffiliateStructureUpdater:
    def __init__(self):
        self.products = {}
        
    async def initialize(self):
        """Load all products from database"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT p.id, p.name, p.slug, COALESCE(p.msrp_price, 0) as price,
                       p.avg_rating, b.name as brand_name, c.name as category_name
                FROM products p
                JOIN brands b ON p.brand_id = b.id
                JOIN categories c ON p.category_id = c.id
                WHERE p.is_active = true
                ORDER BY p.avg_rating DESC NULLS LAST
            '''))
            
            for row in result.fetchall():
                product_data = dict(row._mapping)
                self.products[str(product_data['id'])] = product_data
            
            print(f"Loaded {len(self.products)} products")
    
    async def update_post_affiliate_structure(self, post_id: int, dry_run: bool = True):
        """Update affiliate structure in a specific post"""
        async with async_session_factory() as session:
            # Get the post
            result = await session.execute(text('''
                SELECT id, title, content_json
                FROM blog_posts
                WHERE id = :post_id
            '''), {'post_id': post_id})
            
            row = result.fetchone()
            if not row:
                print(f"Post {post_id} not found")
                return False
            
            post_id, title, content_json = row
            
            if not content_json:
                print(f"Post {post_id} has no content_json")
                return False
            
            # Track changes
            changes_made = False
            updated_content = content_json.copy()
            
            # Update product spotlights in sections
            sections = updated_content.get('sections', [])
            
            for i, section in enumerate(sections):
                if section.get('type') == 'product_spotlight' and 'product' in section:
                    product = section['product']
                    product_id = product.get('id')
                    
                    if product_id and product_id in self.products:
                        real_product = self.products[product_id]
                        
                        # Add new affiliate structure if not already present
                        if 'store_url' not in product or 'cta_text' not in product:
                            # Update affiliate URL with tracking
                            current_url = product.get('affiliate_url', '')
                            if '?ref=blog' not in current_url:
                                base_url = f"https://www.getyourmusicgear.com/products/{real_product['slug']}"
                                sections[i]['product']['affiliate_url'] = f"{base_url}?ref=blog&utm_source=blog&utm_campaign=product_spotlight"
                                sections[i]['product']['store_url'] = base_url
                                sections[i]['product']['cta_text'] = "See Details on Our Store"
                                
                                changes_made = True
                                print(f"  ✅ Updated affiliate structure for: {real_product['brand_name']} {real_product['name']}")
            
            # Update quick picks sections too
            for i, section in enumerate(sections):
                if section.get('type') == 'quick_picks' and 'products' in section:
                    products_list = section['products']
                    for j, product in enumerate(products_list):
                        product_id = product.get('id')
                        if product_id and product_id in self.products:
                            real_product = self.products[product_id]
                            
                            if 'store_url' not in product or 'cta_text' not in product:
                                base_url = f"https://www.getyourmusicgear.com/products/{real_product['slug']}"
                                sections[i]['products'][j]['affiliate_url'] = f"{base_url}?ref=blog&utm_source=blog&utm_campaign=quick_picks"
                                sections[i]['products'][j]['store_url'] = base_url
                                sections[i]['products'][j]['cta_text'] = "See Details"
                                
                                changes_made = True
                                print(f"  ✅ Updated quick pick: {real_product['brand_name']} {real_product['name']}")
            
            if changes_made:
                print(f"📝 Post {post_id}: {title}")
                
                if not dry_run:
                    # Save changes
                    await session.execute(text('''
                        UPDATE blog_posts 
                        SET content_json = :content_json
                        WHERE id = :post_id
                    '''), {
                        'post_id': post_id,
                        'content_json': json.dumps(updated_content)
                    })
                    await session.commit()
                    print(f"  ✅ Updated post {post_id}")
                else:
                    print(f"  🔍 Dry run - would update post {post_id}")
                
                return True
            else:
                return False
    
    async def update_all_posts(self, dry_run: bool = True):
        """Update affiliate structure in all posts"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT id FROM blog_posts 
                WHERE content_json IS NOT NULL
                ORDER BY id DESC
            '''))
            
            post_ids = [row[0] for row in result.fetchall()]
            print(f"Found {len(post_ids)} posts to check")
            
            updated_count = 0
            for post_id in post_ids:
                if await self.update_post_affiliate_structure(post_id, dry_run=dry_run):
                    updated_count += 1
            
            print(f"\n🎉 {updated_count} posts {'would be' if dry_run else 'were'} updated")
    
    async def analyze_current_structure(self):
        """Analyze current affiliate link structure"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT id, title, content_json
                FROM blog_posts 
                WHERE content_json IS NOT NULL
                ORDER BY id DESC
                LIMIT 20
            '''))
            
            with_store_url = 0
            without_store_url = 0
            total_spotlights = 0
            
            for row in result.fetchall():
                post_id, title, content_json = row
                
                sections = content_json.get('sections', [])
                for section in sections:
                    if section.get('type') == 'product_spotlight' and 'product' in section:
                        total_spotlights += 1
                        product = section['product']
                        
                        if 'store_url' in product and 'cta_text' in product:
                            with_store_url += 1
                        else:
                            without_store_url += 1
            
            print(f"\n📊 Affiliate Structure Analysis:")
            print(f"  Total product spotlights: {total_spotlights}")
            print(f"  With enhanced structure: {with_store_url}")
            print(f"  Need updating: {without_store_url}")

async def main():
    print("🔗 Affiliate Structure Updater")
    print("=" * 50)
    
    updater = AffiliateStructureUpdater()
    await updater.initialize()
    
    # Analyze current state
    print("\n📊 Analyzing current affiliate structure...")
    await updater.analyze_current_structure()
    
    # Update all posts (dry run first)
    print("\n🔍 Running dry run to update affiliate structure...")
    await updater.update_all_posts(dry_run=True)
    
    # Ask for confirmation
    print("\n❓ Do you want to apply these changes? (y/N)")
    import sys
    if "--apply" in sys.argv:
        print("✅ Applying changes...")
        await updater.update_all_posts(dry_run=False)
        print("🎉 All posts updated with enhanced affiliate structure!")
    else:
        print("ℹ️  Dry run completed. Use --apply flag to apply changes.")

if __name__ == "__main__":
    asyncio.run(main())
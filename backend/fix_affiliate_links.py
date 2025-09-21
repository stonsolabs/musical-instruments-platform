#!/usr/bin/env python3
"""
Script to fix affiliate links in existing blog posts
Replace example.com links with proper product URLs
"""

import asyncio
import json
import re
from typing import Dict, List, Any
from sqlalchemy import text
from app.database import async_session_factory

class AffiliateLinkFixer:
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
    
    async def fix_post_affiliate_links(self, post_id: int, dry_run: bool = True):
        """Fix affiliate links in a specific post"""
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
            
            # Fix product spotlights in sections
            sections = updated_content.get('sections', [])
            
            for i, section in enumerate(sections):
                if section.get('type') == 'product_spotlight' and 'product' in section:
                    product = section['product']
                    
                    # Check if has example.com link
                    affiliate_url = product.get('affiliate_url', '')
                    if 'example.com' in affiliate_url:
                        # Extract product ID from the URL or find product by name
                        product_id = product.get('id')
                        
                        if product_id and product_id in self.products:
                            # Use actual product data
                            real_product = self.products[product_id]
                            new_url = f"https://www.getyourmusicgear.com/products/{real_product['slug']}"
                            
                            # Update the affiliate URL
                            sections[i]['product']['affiliate_url'] = new_url
                            
                            # Also update other product details to match database
                            sections[i]['product']['name'] = f"{real_product['brand_name']} {real_product['name']}"
                            sections[i]['product']['price'] = f"${real_product['price']:.0f}" if real_product['price'] else "Check Price"
                            sections[i]['product']['rating'] = real_product['avg_rating'] or 4.0
                            
                            changes_made = True
                            print(f"  ✅ Fixed product spotlight: {real_product['brand_name']} {real_product['name']}")
                        else:
                            # Try to find product by matching name
                            product_name = product.get('name', '')
                            matched_product = self._find_product_by_name(product_name)
                            
                            if matched_product:
                                new_url = f"https://www.getyourmusicgear.com/products/{matched_product['slug']}"
                                sections[i]['product']['affiliate_url'] = new_url
                                sections[i]['product']['id'] = str(matched_product['id'])
                                sections[i]['product']['name'] = f"{matched_product['brand_name']} {matched_product['name']}"
                                sections[i]['product']['price'] = f"${matched_product['price']:.0f}" if matched_product['price'] else "Check Price"
                                sections[i]['product']['rating'] = matched_product['avg_rating'] or 4.0
                                
                                changes_made = True
                                print(f"  ✅ Matched and fixed: {matched_product['brand_name']} {matched_product['name']}")
                            else:
                                print(f"  ⚠️ Could not find product match for: {product_name}")
            
            # Fix content that mentions example.com
            for i, section in enumerate(sections):
                if 'content' in section:
                    content = section['content']
                    if 'example.com' in content:
                        # Replace generic example.com links
                        updated_content_text = re.sub(
                            r'https?://example\.com/[^\s\)]*',
                            'https://www.getyourmusicgear.com/products',
                            content
                        )
                        if updated_content_text != content:
                            sections[i]['content'] = updated_content_text
                            changes_made = True
                            print(f"  ✅ Fixed example.com links in content")
            
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
                print(f"📝 Post {post_id}: No changes needed")
                return False
    
    def _find_product_by_name(self, product_name: str) -> Dict:
        """Find product by matching name"""
        if not product_name:
            return None
            
        product_name_lower = product_name.lower()
        
        # Try exact brand + name match
        for product in self.products.values():
            full_name = f"{product['brand_name']} {product['name']}".lower()
            if product_name_lower == full_name:
                return product
        
        # Try partial matches
        best_match = None
        best_score = 0
        
        for product in self.products.values():
            full_name = f"{product['brand_name']} {product['name']}".lower()
            
            # Calculate simple word overlap
            name_words = set(product_name_lower.split())
            product_words = set(full_name.split())
            
            common_words = name_words.intersection(product_words)
            if len(common_words) >= 2:  # At least 2 words match
                score = len(common_words) / max(len(name_words), len(product_words))
                if score > best_score:
                    best_score = score
                    best_match = product
        
        return best_match if best_score > 0.5 else None
    
    async def fix_all_posts(self, dry_run: bool = True):
        """Fix affiliate links in all posts"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT id FROM blog_posts 
                WHERE content_json IS NOT NULL
                AND content_json::text LIKE '%example.com%'
                ORDER BY id DESC
            '''))
            
            post_ids = [row[0] for row in result.fetchall()]
            print(f"Found {len(post_ids)} posts with example.com links")
            
            fixed_count = 0
            for post_id in post_ids:
                if await self.fix_post_affiliate_links(post_id, dry_run=dry_run):
                    fixed_count += 1
            
            print(f"\n🎉 {fixed_count} posts {'would be' if dry_run else 'were'} updated")
    
    async def analyze_current_links(self):
        """Analyze current affiliate link status"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT id, title, content_json
                FROM blog_posts 
                WHERE content_json IS NOT NULL
                ORDER BY id DESC
                LIMIT 20
            '''))
            
            example_count = 0
            proper_count = 0
            total_spotlights = 0
            
            for row in result.fetchall():
                post_id, title, content_json = row
                
                sections = content_json.get('sections', [])
                for section in sections:
                    if section.get('type') == 'product_spotlight' and 'product' in section:
                        total_spotlights += 1
                        affiliate_url = section['product'].get('affiliate_url', '')
                        
                        if 'example.com' in affiliate_url:
                            example_count += 1
                        elif 'getyourmusicgear.com' in affiliate_url:
                            proper_count += 1
            
            print(f"\n📊 Affiliate Link Analysis:")
            print(f"  Total product spotlights: {total_spotlights}")
            print(f"  Using example.com: {example_count}")
            print(f"  Using proper URLs: {proper_count}")
            print(f"  Other/missing: {total_spotlights - example_count - proper_count}")

async def main():
    print("🔗 Affiliate Link Fixer")
    print("=" * 50)
    
    fixer = AffiliateLinkFixer()
    await fixer.initialize()
    
    # Analyze current state
    print("\n📊 Analyzing current affiliate links...")
    await fixer.analyze_current_links()
    
    # Fix all posts (dry run first)
    print("\n🔍 Running dry run to fix affiliate links...")
    await fixer.fix_all_posts(dry_run=True)
    
    # Ask for confirmation
    print("\n❓ Do you want to apply these changes? (y/N)")
    import sys
    if "--apply" in sys.argv:
        print("✅ Applying changes...")
        await fixer.fix_all_posts(dry_run=False)
        print("🎉 All affiliate links updated!")
    else:
        print("ℹ️  Dry run completed. Use --apply flag to apply changes.")

if __name__ == "__main__":
    asyncio.run(main())
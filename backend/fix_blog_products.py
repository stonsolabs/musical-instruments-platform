#!/usr/bin/env python3
"""
Script to fix existing blog posts product integration issues
"""

import asyncio
import json
import re
from typing import Dict, List, Any
from sqlalchemy import text
from app.database import async_session_factory

class BlogProductFixer:
    def __init__(self):
        self.products = []
        self.categories_map = {}
        
    async def initialize(self):
        """Load all products from database"""
        async with async_session_factory() as session:
            # Load products
            result = await session.execute(text('''
                SELECT p.id, p.name, p.slug, COALESCE(p.msrp_price, 0) as price,
                       p.avg_rating, b.name as brand_name, c.name as category_name,
                       c.slug as category_slug
                FROM products p
                JOIN brands b ON p.brand_id = b.id
                JOIN categories c ON p.category_id = c.id
                WHERE p.is_active = true
                ORDER BY p.avg_rating DESC NULLS LAST
            '''))
            
            self.products = [dict(row._mapping) for row in result.fetchall()]
            print(f"Loaded {len(self.products)} products")
            
            # Create category mapping
            for product in self.products:
                cat = product['category_slug']
                if cat not in self.categories_map:
                    self.categories_map[cat] = []
                self.categories_map[cat].append(product)
    
    def find_matching_products(self, mentioned_product_name: str, category_hint: str = None) -> List[Dict]:
        """Find products in our database that match a mentioned product"""
        matches = []
        
        # Normalize the mentioned name
        normalized_mention = re.sub(r'[^\w\s]', '', mentioned_product_name.lower())
        
        for product in self.products:
            # Check brand and product name matches
            full_name = f"{product['brand_name']} {product['name']}".lower()
            normalized_product = re.sub(r'[^\w\s]', '', full_name)
            
            # Look for keyword matches
            mention_words = set(normalized_mention.split())
            product_words = set(normalized_product.split())
            
            # Calculate match score
            common_words = mention_words.intersection(product_words)
            if len(common_words) >= 2:  # At least 2 words match
                score = len(common_words) / len(mention_words)
                matches.append((product, score))
        
        # Sort by score and return top matches
        matches.sort(key=lambda x: x[1], reverse=True)
        return [match[0] for match in matches[:3]]
    
    def get_diverse_products_for_topic(self, topic: str, limit: int = 3) -> List[Dict]:
        """Get diverse products suitable for a topic"""
        topic_lower = topic.lower()
        
        # Topic-based product selection
        if any(word in topic_lower for word in ['guitar', 'string']):
            categories = ['electric-guitars', 'acoustic-guitars']
        elif any(word in topic_lower for word in ['bass', 'low']):
            categories = ['electric-basses']
        elif any(word in topic_lower for word in ['keyboard', 'piano', 'keys']):
            categories = ['digital-pianos', 'keyboards']
        elif any(word in topic_lower for word in ['drum', 'percussion']):
            categories = ['drums']
        elif any(word in topic_lower for word in ['microphone', 'mic', 'recording']):
            categories = ['microphones']
        else:
            # General mix
            categories = ['electric-guitars', 'acoustic-guitars', 'digital-pianos', 'electric-basses']
        
        # Select diverse products from chosen categories
        selected = []
        for category in categories:
            if category in self.categories_map:
                # Take top-rated products from each category
                cat_products = self.categories_map[category][:5]
                if cat_products:
                    selected.extend(cat_products[:2])  # Top 2 from each category
        
        # Remove duplicates and limit
        seen_ids = set()
        unique_products = []
        for product in selected:
            if product['id'] not in seen_ids:
                unique_products.append(product)
                seen_ids.add(product['id'])
                if len(unique_products) >= limit:
                    break
        
        return unique_products
    
    async def fix_post_products(self, post_id: int, dry_run: bool = True):
        """Fix products in a specific post"""
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
                return
            
            post_id, title, content_json = row
            print(f"\\nFixing post {post_id}: {title}")
            
            if not content_json:
                print("No content_json found")
                return
            
            # Get diverse products for this topic
            topic_products = self.get_diverse_products_for_topic(title, limit=3)
            
            # Update featured_products
            updated_content = content_json.copy()
            updated_content['featured_products'] = [str(p['id']) for p in topic_products]
            
            # Fix product spotlights in sections
            sections = updated_content.get('sections', [])
            product_index = 0
            
            for i, section in enumerate(sections):
                if section.get('type') == 'product_spotlight':
                    if product_index < len(topic_products):
                        product = topic_products[product_index]
                        
                        # Create proper product spotlight
                        sections[i]['product'] = {
                            'id': str(product['id']),
                            'name': f"{product['brand_name']} {product['name']}",
                            'price': f"${product['price']:.0f}" if product['price'] else "Check Price",
                            'rating': product['avg_rating'] or 4.0,
                            'pros': [
                                "High-quality construction",
                                "Great sound quality",
                                "Professional features"
                            ],
                            'cons': [
                                "Price point for beginners"
                            ],
                            'affiliate_url': f"https://www.getyourmusicgear.com/products/{product['slug']}"
                        }
                        product_index += 1
                    else:
                        # Remove extra product spotlights
                        sections[i] = {
                            'type': 'content',
                            'content': '## Additional Considerations\\n\\nThere are many factors to consider when making your choice...'
                        }
            
            print(f"Updated featured products: {[p['brand_name'] + ' ' + p['name'] for p in topic_products]}")
            
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
                print(f"✅ Updated post {post_id}")
            else:
                print(f"🔍 Dry run - would update post {post_id}")
    
    async def fix_all_posts(self, dry_run: bool = True):
        """Fix products in all posts"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT id FROM blog_posts 
                WHERE content_json IS NOT NULL
                ORDER BY id DESC
            '''))
            
            post_ids = [row[0] for row in result.fetchall()]
            print(f"Found {len(post_ids)} posts to fix")
            
            for post_id in post_ids:
                await self.fix_post_products(post_id, dry_run=dry_run)
    
    async def analyze_current_products(self):
        """Analyze what products are currently mentioned"""
        async with async_session_factory() as session:
            result = await session.execute(text('''
                SELECT id, title, content_json
                FROM blog_posts 
                WHERE content_json IS NOT NULL
                ORDER BY id DESC
                LIMIT 20
            '''))
            
            product_mentions = {}
            
            for row in result.fetchall():
                post_id, title, content_json = row
                
                # Check featured products
                featured = content_json.get('featured_products', [])
                for product_id in featured:
                    if product_id not in product_mentions:
                        product_mentions[product_id] = 0
                    product_mentions[product_id] += 1
                
                # Check product spotlights
                sections = content_json.get('sections', [])
                for section in sections:
                    if section.get('type') == 'product_spotlight' and 'product' in section:
                        product_name = section['product'].get('name', 'Unknown')
                        if product_name not in product_mentions:
                            product_mentions[product_name] = 0
                        product_mentions[product_name] += 1
            
            print("\\nProduct mention frequency:")
            for product, count in sorted(product_mentions.items(), key=lambda x: x[1], reverse=True):
                print(f"  {product}: {count} times")

async def main():
    print("🔧 Blog Product Fixer")
    print("=" * 50)
    
    fixer = BlogProductFixer()
    await fixer.initialize()
    
    # Analyze current state
    print("\\n📊 Analyzing current product mentions...")
    await fixer.analyze_current_products()
    
    # Fix all posts (dry run first)
    print("\\n🔍 Running dry run to fix all posts...")
    await fixer.fix_all_posts(dry_run=True)
    
    # Ask for confirmation
    print("\\n❓ Do you want to apply these changes? (y/N)")
    import sys
    if "--apply" in sys.argv:
        print("✅ Applying changes...")
        await fixer.fix_all_posts(dry_run=False)
        print("🎉 All posts updated!")
    else:
        print("ℹ️  Dry run completed. Use --apply flag to apply changes.")

if __name__ == "__main__":
    asyncio.run(main())
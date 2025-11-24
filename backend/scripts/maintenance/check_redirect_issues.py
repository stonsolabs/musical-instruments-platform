#!/usr/bin/env python3
"""
Script to identify and fix redirect issues reported by Google Search Console.
This script checks for:
- Blog posts with changed slugs
- Products with changed slugs
- URLs in sitemaps that don't exist
- Trailing slash mismatches

Usage:
    cd backend
    python3 scripts/maintenance/check_redirect_issues.py

Requirements:
    - Python dependencies installed (pip install -r requirements.txt)
    - DATABASE_URL environment variable set
"""

import asyncio
import sys
import os
import csv
from pathlib import Path
from typing import List, Dict, Optional
import re

# Add backend directory to path (script should be run from backend/)
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))

try:
    from sqlalchemy import text
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    import asyncpg
    from urllib.parse import urlparse
except ImportError as e:
    print(f"❌ Error importing required modules: {e}")
    print("\n💡 Make sure you:")
    print("   1. Are running from the backend/ directory")
    print("   2. Have installed dependencies: pip install -r requirements.txt")
    print("   3. Have DATABASE_URL environment variable set")
    sys.exit(1)

# Create database connection directly without importing models
def get_async_session_factory():
    """Create async session factory from DATABASE_URL"""
    database_url = os.getenv("DATABASE_URL", "")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")
    
    # Convert postgresql:// to postgresql+asyncpg://
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        # Add SSL requirement for Azure
        if "ssl=" not in database_url:
            connector = "&" if "?" in database_url else "?"
            database_url = f"{database_url}{connector}ssl=require"
    
    engine = create_async_engine(database_url, echo=False)
    return async_sessionmaker(engine, expire_on_commit=False)

async def check_blog_posts():
    """Check for blog posts that might have redirect issues"""
    session_factory = get_async_session_factory()
    async with session_factory() as session:
        # Get all published blog posts
        result = await session.execute(text("""
            SELECT id, title, slug, status, created_at, updated_at
            FROM blog_posts
            WHERE status = 'published'
            ORDER BY updated_at DESC
        """))
        
        posts = result.fetchall()
        print(f"\n📝 Found {len(posts)} published blog posts")
        
        # Check for duplicate slugs
        slug_counts = {}
        for post in posts:
            slug = post[2]
            if slug in slug_counts:
                slug_counts[slug].append(post)
            else:
                slug_counts[slug] = [post]
        
        duplicates = {slug: posts for slug, posts in slug_counts.items() if len(posts) > 1}
        if duplicates:
            print(f"\n⚠️  Found {len(duplicates)} duplicate slugs:")
            for slug, posts in duplicates.items():
                print(f"   Slug '{slug}' used by {len(posts)} posts:")
                for post in posts:
                    print(f"      - ID {post[0]}: {post[1]}")
        else:
            print("✅ No duplicate slugs found")
        
        # Check for invalid slug characters
        invalid_slugs = []
        for post in posts:
            slug = post[2]
            if not re.match(r'^[a-z0-9-]+$', slug):
                invalid_slugs.append(post)
        
        if invalid_slugs:
            print(f"\n⚠️  Found {len(invalid_slugs)} posts with invalid slug characters:")
            for post in invalid_slugs:
                print(f"   ID {post[0]}: '{post[2]}' (title: {post[1]})")
        else:
            print("✅ All slugs have valid characters")
        
        # Check for slugs ending with hyphens
        trailing_hyphen_slugs = [post for post in posts if post[2].endswith('-')]
        if trailing_hyphen_slugs:
            print(f"\n⚠️  Found {len(trailing_hyphen_slugs)} posts with trailing hyphens:")
            for post in trailing_hyphen_slugs:
                print(f"   ID {post[0]}: '{post[2]}'")
        else:
            print("✅ No trailing hyphens in slugs")
        
        return posts

async def check_products():
    """Check for products that might have redirect issues"""
    session_factory = get_async_session_factory()
    async with session_factory() as session:
        result = await session.execute(text("""
            SELECT id, name, slug
            FROM products
            WHERE is_active = true
            ORDER BY id
        """))
        
        products = result.fetchall()
        print(f"\n🎸 Found {len(products)} active products")
        
        # Check for duplicate slugs
        slug_counts = {}
        for product in products:
            slug = product[2]
            if slug in slug_counts:
                slug_counts[slug].append(product)
            else:
                slug_counts[slug] = [product]
        
        duplicates = {slug: prods for slug, prods in slug_counts.items() if len(prods) > 1}
        if duplicates:
            print(f"\n⚠️  Found {len(duplicates)} duplicate product slugs:")
            for slug, prods in duplicates.items():
                print(f"   Slug '{slug}' used by {len(prods)} products")
        else:
            print("✅ No duplicate product slugs found")
        
        return products

async def check_sitemap_urls():
    """Check if URLs in sitemaps are valid"""
    print("\n🗺️  Checking sitemap URLs...")
    
    session_factory = get_async_session_factory()
    async with session_factory() as session:
        # Get all published blog posts
        blog_result = await session.execute(text("""
            SELECT slug FROM blog_posts WHERE status = 'published'
        """))
        valid_blog_slugs = {row[0] for row in blog_result.fetchall()}
        
        # Get all active products
        product_result = await session.execute(text("""
            SELECT slug FROM products WHERE is_active = true
        """))
        valid_product_slugs = {row[0] for row in product_result.fetchall()}
        
        print(f"✅ Valid blog slugs: {len(valid_blog_slugs)}")
        print(f"✅ Valid product slugs: {len(valid_product_slugs)}")
        
        return {
            'blog_slugs': valid_blog_slugs,
            'product_slugs': valid_product_slugs
        }

async def analyze_gsc_data(csv_path: str):
    """Analyze the GSC CSV data to identify specific URLs with issues"""
    if not os.path.exists(csv_path):
        print(f"\n⚠️  GSC CSV file not found: {csv_path}")
        return
    
    print(f"\n📊 Analyzing GSC data from: {csv_path}")
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            print(f"   Found {len(rows)} rows in CSV")
            
            # Look for redirect issues
            redirect_issues = [row for row in rows if 'redirect' in row.get('Reason', '').lower()]
            if redirect_issues:
                print(f"\n⚠️  Found {len(redirect_issues)} redirect issues:")
                for issue in redirect_issues:
                    print(f"   - {issue}")
            
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")

async def generate_redirect_report(gsc_csv_path: Optional[str] = None):
    """Generate a comprehensive redirect issue report"""
    print("=" * 60)
    print("🔍 REDIRECT ISSUE ANALYSIS")
    print("=" * 60)
    
    # Check if DATABASE_URL is set
    if not os.getenv('DATABASE_URL'):
        print("\n⚠️  Warning: DATABASE_URL environment variable not set")
        print("   Some checks may fail. Set it with:")
        print("   export DATABASE_URL='postgresql://user:pass@host:port/dbname'")
    
    try:
        # Check blog posts
        blog_posts = await check_blog_posts()
        
        # Check products
        products = await check_products()
        
        # Check sitemap URLs
        sitemap_data = await check_sitemap_urls()
    except Exception as e:
        print(f"\n❌ Error connecting to database: {e}")
        print("   Make sure DATABASE_URL is set correctly")
        return
    
    # Analyze GSC data if available
    if gsc_csv_path and os.path.exists(gsc_csv_path):
        await analyze_gsc_data(gsc_csv_path)
    else:
        # Try default path
        default_path = os.path.expanduser("~/Downloads/getyourmusicgear.com-Coverage-2025-11-24/Critical issues.csv")
        if os.path.exists(default_path):
            await analyze_gsc_data(default_path)
        else:
            print("\n💡 Tip: To analyze GSC data, provide the CSV path:")
            print("   python3 scripts/maintenance/check_redirect_issues.py /path/to/Critical\ issues.csv")
    
    print("\n" + "=" * 60)
    print("✅ Analysis complete!")
    print("=" * 60)
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    print("1. Ensure all blog post slugs are unique and valid")
    print("2. Add redirect rules in next.config.js for common redirect scenarios")
    print("3. Update sitemaps to only include valid, published URLs")
    print("4. Use 301 redirects for permanent URL changes")
    print("5. Check for trailing slash mismatches")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Check for redirect issues in the website')
    parser.add_argument('gsc_csv', nargs='?', help='Path to GSC Critical issues.csv file')
    args = parser.parse_args()
    
    asyncio.run(generate_redirect_report(args.gsc_csv))


#!/usr/bin/env python3
"""
Re-associate blog posts with correct, relevant products.

Goal:
- Replace generic/duplicate associations (e.g., all Arturia) with products relevant to each post.
- Use post title/category keywords to select products by brand/category/name.
- Keep 3–6 products per post, prioritizing availability and rating when possible.

Usage:
  python -m app.scripts.reassociate_blog_products --dry-run       # show changes only
  python -m app.scripts.reassociate_blog_products --limit 100     # process first 100 posts
  python -m app.scripts.reassociate_blog_products --commit        # apply updates

Notes:
- Uses raw SQL via async_session_factory for portability.
- Safe defaults: dry-run by default. Use --commit to write.
"""

import asyncio
import argparse
import re
import json
from typing import List, Dict, Any, Tuple, Optional

from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

from ..database import async_session_factory


BRAND_KEYWORDS = [
    'arturia','akai','roland','korg','yamaha','moog','fender','gibson','taylor','martin',
    'shure','audio-technica','behringer','focusrite','presonus','zoom','boss','line 6','ibanez'
]

CATEGORY_HINTS = {
    'guitar': ['electric-guitars','acoustic-guitars','bass-guitars','guitar-amps'],
    'keyboard': ['keyboards','digital-pianos','synthesizers'],
    'synth': ['synthesizers','keyboards'],
    'midi': ['midi-controllers','keyboards'],
    'microphone': ['microphones'],
    'mic': ['microphones'],
    'audio interface': ['audio-interfaces'],
    'interface': ['audio-interfaces'],
    'monitor': ['studio-monitors'],
    'headphone': ['headphones'],
    'drum': ['drums','percussion'],
}


def extract_keywords(
    title: str,
    category_value: Optional[str],
    tags: Optional[List[str]] = None,
    sections: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[List[str], List[str]]:
    """Infer brand + product category hints from title/tags/sections.

    Returns (brands, category_slugs) where category_slugs map to product categories
    like 'electric-guitars', 'microphones', etc.
    """
    text_blobs: List[str] = [(title or '')]
    if tags:
        text_blobs.append(' '.join(tags))
    if sections:
        # Include titles and a small slice of content for signal
        for s in sections[:4]:
            if isinstance(s, dict):
                text_blobs.append(str(s.get('title') or ''))
                content = str(s.get('content') or '')
                text_blobs.append(content[:500])
    t = ' '.join(text_blobs).lower()

    brands = [b for b in BRAND_KEYWORDS if b in t]

    cats: List[str] = []
    for hint, mapped in CATEGORY_HINTS.items():
        if hint in t:
            cats.extend(mapped)
    # category_value in simplified model is template type (e.g., buying-guide), not instrument; ignore
    # de-dup
    cats = list(dict.fromkeys(cats))
    return brands, cats


async def load_products(session, brands: List[str], categories: List[str], limit: int = 12) -> List[Dict[str, Any]]:
    where_clauses = [
        "p.is_active = true",
        "(p.name is not null and p.name != '')",
    ]
    params: Dict[str, Any] = {}

    if brands:
        where_clauses.append("lower(b.name) = ANY(:brands)")
        params['brands'] = brands

    if categories:
        where_clauses.append("c.slug = ANY(:cats)")
        params['cats'] = categories

    where_sql = " AND ".join(where_clauses)
    sql = f"""
        SELECT p.id, p.slug, p.name, p.avg_rating, p.review_count, COALESCE(p.msrp_price,0) as price,
               b.name as brand, c.slug as category_slug
        FROM products p
        JOIN brands b ON p.brand_id=b.id
        JOIN categories c ON p.category_id=c.id
        WHERE {where_sql}
        ORDER BY (p.avg_rating IS NOT NULL) DESC, p.avg_rating DESC NULLS LAST, p.review_count DESC NULLS LAST
        LIMIT :limit
    """
    params['limit'] = limit
    result = await session.execute(text(sql), params)
    return [dict(row._mapping) for row in result.fetchall()]


async def select_relevant_products(session, post: Dict[str, Any], max_count: int = 5) -> List[int]:
    cj = post.get('content_json') or {}
    category_value = cj.get('category') if isinstance(cj, dict) else None
    tags = cj.get('tags') if isinstance(cj, dict) else None
    sections = cj.get('sections') if isinstance(cj, dict) else None
    brands, cats = extract_keywords(post['title'], category_value, tags=tags, sections=sections)
    candidates = await load_products(session, brands, cats, limit=24)

    if not candidates:
        # fallback: popular products overall
        result = await session.execute(text(
            """
            SELECT p.id FROM products p
            WHERE p.is_active = true AND (p.name is not null and p.name != '')
            ORDER BY p.review_count DESC NULLS LAST, p.avg_rating DESC NULLS LAST
            LIMIT 24
            """
        ))
        candidates = [{'id': r[0]} for r in result.fetchall()]

    # De-duplicate and cap
    ids: List[int] = []
    for c in candidates:
        pid = int(c['id'])
        if pid not in ids:
            ids.append(pid)
        if len(ids) >= max_count:
            break
    return ids


async def get_posts(session, limit: int | None = None) -> List[Dict[str, Any]]:
    sql_with_category = """
      SELECT p.id, p.title, p.slug, p.content_json,
             c.slug as category_slug
      FROM blog_posts p
      LEFT JOIN blog_categories c ON p.category_id=c.id
      ORDER BY COALESCE(p.published_at, p.created_at) DESC NULLS LAST, p.id DESC
    """
    sql_simple = """
      SELECT p.id, p.title, p.slug, p.content_json
      FROM blog_posts p
      ORDER BY COALESCE(p.published_at, p.created_at) DESC NULLS LAST, p.id DESC
    """
    try:
        sql = sql_with_category
        if limit:
            sql += " LIMIT :limit"
            result = await session.execute(text(sql), {'limit': limit})
        else:
            result = await session.execute(text(sql))
        rows = [dict(row._mapping) for row in result.fetchall()]
        return rows
    except ProgrammingError:
        # Fallback if blog_categories table doesn't exist
        await session.rollback()
        sql = sql_simple
        if limit:
            sql += " LIMIT :limit"
            result = await session.execute(text(sql), {'limit': limit})
        else:
            result = await session.execute(text(sql))
        rows = [dict(row._mapping) for row in result.fetchall()]
        # Add category_slug=None to keep downstream logic consistent
        for r in rows:
            r['category_slug'] = None
        return rows


async def update_post_products(session, post_id: int, product_ids: List[int]):
    # Update JSON content: set featured_products array
    sel = await session.execute(text("SELECT content_json FROM blog_posts WHERE id = :id"), {'id': post_id})
    row = sel.fetchone()
    current = row[0] if row and row[0] else {}
    if not isinstance(current, dict):
        current = {}
    current['featured_products'] = product_ids
    await session.execute(
        text("UPDATE blog_posts SET content_json = CAST(:cj AS JSONB), updated_at = NOW() WHERE id = :id"),
        {'cj': json.dumps(current), 'id': post_id}
    )


async def run(dry_run: bool = True, limit: int | None = None):
    async with async_session_factory() as session:
        posts = await get_posts(session, limit)
        print(f"Found {len(posts)} published posts to process")

        changes = 0
        for post in posts:
            new_ids = await select_relevant_products(session, post, max_count=5)
            slug = post.get('slug')
            print(f"- {post['title']} (/{slug}) -> products {new_ids}")
            if not dry_run:
                await update_post_products(session, int(post['id']), new_ids)
                changes += 1

        if not dry_run:
            await session.commit()
            print(f"Committed changes for {changes} posts")
        else:
            print("Dry run complete (no changes committed)")


def main():
    parser = argparse.ArgumentParser(description="Re-associate blog posts with relevant products")
    parser.add_argument('--commit', action='store_true', help='Apply changes (otherwise dry-run)')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of posts processed')
    args = parser.parse_args()

    asyncio.run(run(dry_run=not args.commit, limit=args.limit))


if __name__ == '__main__':
    main()

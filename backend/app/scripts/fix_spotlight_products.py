#!/usr/bin/env python3
"""
Audit and fix product_spotlight sections so they show the correct products
based on content_json.featured_products and the products table.

Logic:
- For each post, read content_json.featured_products (list of product ids)
- Load product name/slug for those ids
- Examine content_json.sections and find product_spotlight sections
  * Normalize to an array field: products: [{id,name,slug,affiliate_url,store_url}]
  * If missing/incorrect (ids/slugs not matching featured_products), rewrite to use the featured list (up to max_n)
- If there are no product_spotlight sections but featured_products exist, insert one after the intro or as the second section.

Usage:
  .venv/bin/python -m backend.app.scripts.fix_spotlight_products --dry-run --limit 50
  .venv/bin/python -m backend.app.scripts.fix_spotlight_products --commit
"""

import asyncio
import argparse
from typing import Any, Dict, List, Optional

from sqlalchemy import text

from ..database import async_session_factory


async def fetch_posts(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    async with async_session_factory() as session:
        sql = """
          SELECT id, title, slug, content_json
          FROM blog_posts
          ORDER BY COALESCE(published_at, created_at) DESC
        """
        if limit:
            res = await session.execute(text(sql + " LIMIT :limit"), {"limit": limit})
        else:
            res = await session.execute(text(sql))
        rows = res.fetchall()
        posts: List[Dict[str, Any]] = []
        for r in rows:
            cj = r[3] or {}
            if not isinstance(cj, dict):
                cj = {}
            posts.append({
                'id': r[0], 'title': r[1], 'slug': r[2], 'content_json': cj
            })
        return posts


async def fetch_products_by_ids(ids: List[int]) -> Dict[int, Dict[str, Any]]:
    if not ids:
        return {}
    async with async_session_factory() as session:
        res = await session.execute(text(
            """
            SELECT p.id, p.name, p.slug
            FROM products p
            WHERE p.id = ANY(:ids)
            """
        ), {"ids": ids})
        out: Dict[int, Dict[str, Any]] = {}
        for row in res.fetchall():
            out[int(row[0])] = {"id": int(row[0]), "name": row[1], "slug": row[2]}
        return out


def desired_spotlight_products(featured_ids: List[int], prod_map: Dict[int, Dict[str, Any]], max_n: int = 3) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for pid in featured_ids:
        info = prod_map.get(int(pid))
        if not info:
            continue
        slug = info.get('slug')
        item = {
            'id': int(pid),
            'name': info.get('name'),
            'slug': slug,
            'affiliate_url': f"/products/{slug}" if slug else None,
            'store_url': f"/products/{slug}" if slug else None,
        }
        out.append(item)
        if len(out) >= max_n:
            break
    return out


def normalize_spotlight_section(sec: Dict[str, Any]) -> Dict[str, Any]:
    if 'products' in sec and isinstance(sec['products'], list):
        return sec
    if 'product' in sec and isinstance(sec['product'], dict):
        sec['products'] = [sec['product']]
        sec.pop('product', None)
    return sec


def needs_update(sec: Dict[str, Any], desired: List[Dict[str, Any]]) -> bool:
    cur = sec.get('products') or []
    cur_ids: List[int] = []
    for p in cur:
        if not isinstance(p, dict):
            continue
        pid = p.get('id')
        try:
            cur_ids.append(int(pid))
        except Exception:
            # tolerate string ids; treat as mismatch to force update
            return True
    want_ids = [int(d['id']) for d in desired]
    return not cur_ids or cur_ids[:len(want_ids)] != want_ids


async def apply_updates(post_id: int, new_cj: Dict[str, Any]):
    async with async_session_factory() as session:
        await session.execute(text("UPDATE blog_posts SET content_json = CAST(:cj AS JSONB), updated_at = NOW() WHERE id = :id"),
                              {"cj": __import__('json').dumps(new_cj), "id": post_id})
        await session.commit()


async def run(dry_run: bool = True, limit: Optional[int] = None):
    posts = await fetch_posts(limit)
    changed = 0
    for p in posts:
        cj = p['content_json'] or {}
        featured = cj.get('featured_products') or []
        if not isinstance(featured, list) or not featured:
            continue
        # Normalize ids
        try:
            featured_ids = [int(x) for x in featured if str(x).isdigit() or isinstance(x, int)]
        except Exception:
            continue
        if not featured_ids:
            continue
        prod_map = await fetch_products_by_ids(featured_ids)
        desired = desired_spotlight_products(featured_ids, prod_map, max_n=3)
        if not desired:
            continue
        sections = cj.get('sections') or []
        updated_sections = []
        found_spotlight = False
        any_updated = False
        for sec in sections:
            if not isinstance(sec, dict) or sec.get('type') != 'product_spotlight':
                updated_sections.append(sec)
                continue
            found_spotlight = True
            sec = normalize_spotlight_section(sec)
            if needs_update(sec, desired):
                new_sec = {**sec, 'products': desired}
                updated_sections.append(new_sec)
                any_updated = True
            else:
                updated_sections.append(sec)
        if not found_spotlight:
            # Insert a spotlight after the intro if possible, else as second section
            insert_idx = 1
            if sections and isinstance(sections[0], dict) and sections[0].get('type') == 'intro':
                insert_idx = 1
            else:
                insert_idx = min(1, len(sections))
            new_sec = {'type': 'product_spotlight', 'products': desired}
            sections = sections[:insert_idx] + [new_sec] + sections[insert_idx:]
            cj['sections'] = sections
            any_updated = True
        else:
            if any_updated:
                cj['sections'] = updated_sections

        if any_updated:
            changed += 1
            print(f"Fix: /{p['slug']} -> spotlight products { [d['id'] for d in desired] }")
            if not dry_run:
                await apply_updates(int(p['id']), cj)

    if dry_run:
        print(f"Dry run complete. Would update {changed} posts.")
    else:
        print(f"Updated {changed} posts.")


def main():
    parser = argparse.ArgumentParser(description='Fix product_spotlight sections based on featured_products')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--commit', action='store_true')
    parser.add_argument('--limit', type=int, default=None)
    args = parser.parse_args()
    asyncio.run(run(dry_run=not args.commit, limit=args.limit))


if __name__ == '__main__':
    main()

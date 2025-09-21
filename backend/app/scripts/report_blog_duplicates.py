#!/usr/bin/env python3
"""
Report likely duplicate blog posts and suggest a canonical to keep/check.

Heuristics:
- Normalize titles (lowercase, strip punctuation/extra whitespace)
- Also strip common lead phrases ("the hidden truth about", "why", "inside") to catch near-duplicates
- Group posts that share a normalized key
- Pick canonical per group: published_at desc, then highest content_json.word_count, then created_at desc

Usage:
  .venv/bin/python -m backend.app.scripts.report_blog_duplicates --limit 200   # optional
  .venv/bin/python -m backend.app.scripts.report_blog_duplicates --json > dupes.json
"""

import asyncio
import argparse
import json
import re
from typing import Any, Dict, List

from sqlalchemy import text

from ..database import async_session_factory


LEAD_PHRASES = [
    r"^the hidden truth about\s+",
    r"^why\s+",
    r"^inside\s+",
]


def normalize_title(title: str) -> str:
    t = (title or '').strip().lower()
    # remove lead phrases
    for pat in LEAD_PHRASES:
        t = re.sub(pat, '', t)
    # remove punctuation
    t = re.sub(r"[^a-z0-9\s-]", '', t)
    # collapse whitespace
    t = re.sub(r"\s+", ' ', t).strip()
    return t


async def fetch_posts(limit: int | None = None) -> List[Dict[str, Any]]:
    async with async_session_factory() as session:
        sql = """
            SELECT id, title, slug, content_json, published_at, created_at
            FROM blog_posts
            ORDER BY COALESCE(published_at, created_at) DESC
        """
        if limit:
            sql += " LIMIT :limit"
            result = await session.execute(text(sql), {'limit': limit})
        else:
            result = await session.execute(text(sql))
        rows = result.fetchall()
        posts: List[Dict[str, Any]] = []
        for row in rows:
            cj = row[3] or {}
            if not isinstance(cj, dict):
                cj = {}
            posts.append({
                'id': row[0],
                'title': row[1],
                'slug': row[2],
                'content_json': cj,
                'published_at': row[4],
                'created_at': row[5],
            })
        return posts


def pick_canonical(group: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Prefer published_at desc, then word_count desc, then created_at desc
    def score(p: Dict[str, Any]) -> tuple:
        wc = 0
        try:
            wc = int(p.get('content_json', {}).get('word_count') or 0)
        except Exception:
            wc = 0
        return (
            1 if p.get('published_at') else 0,
            wc,
            p.get('created_at') or 0,
        )
    return sorted(group, key=score, reverse=True)[0]


async def main():
    parser = argparse.ArgumentParser(description='Report likely duplicate blog posts')
    parser.add_argument('--limit', type=int, default=None)
    parser.add_argument('--json', action='store_true', help='Output JSON only')
    args = parser.parse_args()

    posts = await fetch_posts(args.limit)
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for p in posts:
        key = normalize_title(p['title'])
        if not key:
            continue
        groups.setdefault(key, []).append(p)

    dupes = {k: v for k, v in groups.items() if len(v) > 1}
    report: List[Dict[str, Any]] = []
    for k, items in dupes.items():
        canonical = pick_canonical(items)
        alternates = [i for i in items if i['id'] != canonical['id']]
        report.append({
            'key': k,
            'canonical': {'id': canonical['id'], 'title': canonical['title'], 'slug': canonical['slug']},
            'alternates': [{'id': a['id'], 'title': a['title'], 'slug': a['slug']} for a in alternates],
            'count': len(items)
        })

    if args.json:
        print(json.dumps({'duplicate_groups': report}, default=str))
        return

    print(f"Total posts: {len(posts)}")
    print(f"Duplicate groups: {len(report)}\n")
    for grp in sorted(report, key=lambda x: x['count'], reverse=True)[:50]:
        print(f"- Key: {grp['key']} (x{grp['count']})")
        print(f"  Canonical: {grp['canonical']['title']} /{grp['canonical']['slug']}")
        for alt in grp['alternates']:
            print(f"  Alt:       {alt['title']} /{alt['slug']}")
        print()

if __name__ == '__main__':
    asyncio.run(main())


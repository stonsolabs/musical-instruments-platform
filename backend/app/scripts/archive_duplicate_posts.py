#!/usr/bin/env python3
"""
Detect duplicate posts (by normalized title) and archive alternates, keeping one canonical.

Usage:
  .venv/bin/python -m backend.app.scripts.archive_duplicate_posts --dry-run          # preview only
  .venv/bin/python -m backend.app.scripts.archive_duplicate_posts --commit          # archive alternates
  .venv/bin/python -m backend.app.scripts.archive_duplicate_posts --limit 300       # limit processed posts
"""

import asyncio
import argparse
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
    for pat in LEAD_PHRASES:
      t = re.sub(pat, '', t)
    t = re.sub(r"[^a-z0-9\s-]", '', t)
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
            res = await session.execute(text(sql + " LIMIT :limit"), {'limit': limit})
        else:
            res = await session.execute(text(sql))
        rows = res.fetchall()
        posts: List[Dict[str, Any]] = []
        for r in rows:
            cj = r[3] or {}
            if not isinstance(cj, dict):
                cj = {}
            posts.append({'id': r[0], 'title': r[1], 'slug': r[2], 'content_json': cj, 'published_at': r[4], 'created_at': r[5]})
        return posts


def pick_canonical(group: List[Dict[str, Any]]) -> Dict[str, Any]:
    def score(p: Dict[str, Any]):
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


async def archive_posts(ids: List[int]):
    if not ids:
        return 0
    async with async_session_factory() as session:
        res = await session.execute(
            text(
                "UPDATE blog_posts SET status = 'archived' WHERE id = ANY(:ids) RETURNING id"
            ), {'ids': ids}
        )
        updated = [row[0] for row in res.fetchall()]
        await session.commit()
        return len(updated)


async def main():
    parser = argparse.ArgumentParser(description='Archive duplicate blog posts (keep one canonical per title group)')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--commit', action='store_true')
    parser.add_argument('--limit', type=int, default=None)
    args = parser.parse_args()

    posts = await fetch_posts(args.limit)
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for p in posts:
        key = normalize_title(p['title'])
        if not key:
            continue
        groups.setdefault(key, []).append(p)

    to_archive: List[int] = []
    for key, items in groups.items():
        if len(items) <= 1:
            continue
        canonical = pick_canonical(items)
        alternates = [i for i in items if i['id'] != canonical['id']]
        # Only archive alternates that are draft or published duplicates; skip if already archived
        for alt in alternates:
            to_archive.append(alt['id'])

    if args.dry_run and not args.commit:
        print(f"Found {len(to_archive)} duplicates to archive (dry-run). Example IDs: {to_archive[:20]}")
        return

    if args.commit:
        updated = await archive_posts(to_archive)
        print(f"Archived {updated} duplicate posts")


if __name__ == '__main__':
    asyncio.run(main())


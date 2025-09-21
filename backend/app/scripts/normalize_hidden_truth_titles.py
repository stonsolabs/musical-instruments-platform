#!/usr/bin/env python3
"""
Report and optionally normalize titles that start with 'The Hidden Truth About ...'

Changes only the title; slug remains unchanged to avoid breaking links.

Usage:
  .venv/bin/python -m backend.app.scripts.normalize_hidden_truth_titles --dry-run
  .venv/bin/python -m backend.app.scripts.normalize_hidden_truth_titles --commit
"""

import asyncio
import argparse
import re
from typing import List, Dict, Any

from sqlalchemy import text

from ..database import async_session_factory


PAT = re.compile(r"^\s*the\s+hidden\s+truth\s+about\s+", re.IGNORECASE)


async def find_targets() -> List[Dict[str, Any]]:
    async with async_session_factory() as session:
        res = await session.execute(text(
            """
            SELECT id, title, slug
            FROM blog_posts
            WHERE title ILIKE 'The Hidden Truth About %'
            ORDER BY id DESC
            """
        ))
        return [ { 'id': r[0], 'title': r[1], 'slug': r[2] } for r in res.fetchall() ]


def normalize_title(t: str) -> str:
    new = PAT.sub('', t).strip()
    # Capitalize first letter
    if new:
        return new[0].upper() + new[1:]
    return t


async def apply_updates(ids_titles: List[Dict[str, Any]]):
    async with async_session_factory() as session:
        for item in ids_titles:
            await session.execute(text("UPDATE blog_posts SET title = :title, updated_at = NOW() WHERE id = :id"),
                                  { 'title': item['new_title'], 'id': item['id'] })
        await session.commit()


async def run(commit: bool):
    rows = await find_targets()
    if not rows:
        print("No titles to normalize.")
        return
    changes = []
    for r in rows:
        nt = normalize_title(r['title'])
        if nt != r['title']:
            changes.append({ 'id': r['id'], 'old_title': r['title'], 'new_title': nt, 'slug': r['slug'] })
    if not changes:
        print("Nothing to change.")
        return
    if not commit:
        print(f"[Dry run] Would change {len(changes)} titles. Examples:")
        for ex in changes[:10]:
            print(f"- {ex['old_title']} -> {ex['new_title']} /{ex['slug']}")
        return
    await apply_updates(changes)
    print(f"Updated {len(changes)} titles.")


def main():
    parser = argparse.ArgumentParser(description='Normalize titles starting with The Hidden Truth About ...')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    asyncio.run(run(commit=args.commit and not args.dry_run))


if __name__ == '__main__':
    main()


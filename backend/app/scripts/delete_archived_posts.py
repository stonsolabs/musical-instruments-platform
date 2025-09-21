#!/usr/bin/env python3
"""
Hard-delete archived blog posts.

Deletes posts where status = 'archived' in batches to avoid timeouts.

Usage:
  .venv/bin/python -m backend.app.scripts.delete_archived_posts --dry-run
  .venv/bin/python -m backend.app.scripts.delete_archived_posts --commit
  .venv/bin/python -m backend.app.scripts.delete_archived_posts --batch 200 --commit
"""

import asyncio
import argparse
from typing import List

from sqlalchemy import text

from ..database import async_session_factory


async def list_archived_ids(limit: int | None = None) -> List[int]:
    async with async_session_factory() as session:
        sql = "SELECT id FROM blog_posts WHERE status = 'archived' ORDER BY id DESC"
        if limit:
            sql += " LIMIT :limit"
            res = await session.execute(text(sql), {"limit": limit})
        else:
            res = await session.execute(text(sql))
        return [row[0] for row in res.fetchall()]


async def delete_ids(ids: List[int]) -> int:
    if not ids:
        return 0
    async with async_session_factory() as session:
        # Delete in a single statement for this batch; rely on FK ON DELETE CASCADE if configured
        await session.execute(text("DELETE FROM blog_posts WHERE id = ANY(:ids)"), {"ids": ids})
        await session.commit()
        return len(ids)


async def run(commit: bool, batch_size: int):
    # Get all archived IDs
    ids = await list_archived_ids()
    total = len(ids)
    if not commit:
        print(f"[Dry run] Archived posts found: {total}")
        print(f"Example IDs: {ids[:20]}")
        return

    # Delete in batches
    deleted = 0
    for i in range(0, total, batch_size):
        batch = ids[i:i+batch_size]
        n = await delete_ids(batch)
        deleted += n
        print(f"Deleted {deleted}/{total} archived posts...")
    print(f"Done. Deleted {deleted} archived posts.")


def main():
    parser = argparse.ArgumentParser(description='Delete archived blog posts')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--commit', action='store_true')
    parser.add_argument('--batch', type=int, default=200)
    args = parser.parse_args()
    asyncio.run(run(commit=args.commit and not args.dry_run, batch_size=max(1, args.batch)))


if __name__ == '__main__':
    main()


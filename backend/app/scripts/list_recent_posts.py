#!/usr/bin/env python3
"""
List recent posts (by published_at/created_at desc) to spot-check after changes.

Usage:
  .venv/bin/python -m backend.app.scripts.list_recent_posts --limit 15
"""

import asyncio
import argparse
from sqlalchemy import text
from typing import Any, Dict, List

from ..database import async_session_factory


async def list_recent(limit: int = 15) -> List[Dict[str, Any]]:
    async with async_session_factory() as session:
        res = await session.execute(text(
            """
            SELECT id, title, slug, published_at, created_at
            FROM blog_posts
            ORDER BY COALESCE(published_at, created_at) DESC
            LIMIT :limit
            """
        ), {"limit": limit})
        rows = res.fetchall()
        return [
            {"id": r[0], "title": r[1], "slug": r[2], "published_at": r[3], "created_at": r[4]}
            for r in rows
        ]


def main():
    parser = argparse.ArgumentParser(description='List recent posts')
    parser.add_argument('--limit', type=int, default=15)
    args = parser.parse_args()
    posts = asyncio.run(list_recent(args.limit))
    print("Recent posts to spot-check:")
    for p in posts:
        print(f"- /blog/{p['slug']}")


if __name__ == '__main__':
    main()


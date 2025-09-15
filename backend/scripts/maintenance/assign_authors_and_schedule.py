"""
Assign realistic (fake) authors to posts and stagger publication.

Usage examples:

1) Assign authors to all drafts without author_name:
   python -m backend.scripts.maintenance.assign_authors_and_schedule --assign-authors

2) Publish a daily batch of 5 drafts (run via cron daily):
   python -m backend.scripts.maintenance.assign_authors_and_schedule --publish-batch 5

3) Backfill-publish 20 drafts with dates spread over the last 14 days:
   python -m backend.scripts.maintenance.assign_authors_and_schedule --publish-batch 20 --backfill-days 14

Notes:
- Uses blogs_docs/authors.json as the author pool.
- Does not create new tables; writes to blog_posts.author_name and author_email.
"""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from sqlalchemy import text

from backend.app.database import async_session_factory


def load_authors(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    random.shuffle(data)
    return data


async def assign_authors(authors: List[Dict[str, Any]], limit: int | None = None) -> int:
    count = 0
    async with async_session_factory() as session:
        # Fetch posts missing author_name or with generic team byline
        res = await session.execute(
            text(
                """
                SELECT id FROM blog_posts
                WHERE (author_name IS NULL OR author_name = '' OR author_name = 'GetYourMusicGear Team')
                ORDER BY id DESC
                """
            )
        )
        rows = [r[0] for r in res.fetchall()]
        if limit:
            rows = rows[:limit]
        for pid in rows:
            a = random.choice(authors)
            await session.execute(
                text(
                    "UPDATE blog_posts SET author_name = :name, author_email = :email WHERE id = :id"
                ),
                {"name": a.get("name"), "email": a.get("email"), "id": pid},
            )
            count += 1
        await session.commit()
    return count


def random_past_datetime(days_back: int) -> datetime:
    now = datetime.utcnow()
    delta_days = random.randint(0, max(days_back, 1))
    dt = now - timedelta(days=delta_days)
    # randomize hour/minute for natural spread
    return dt.replace(hour=random.randint(9, 21), minute=random.choice([0, 15, 30, 45]), second=0, microsecond=0)


async def publish_batch(batch_size: int, backfill_days: int | None = None) -> int:
    published = 0
    async with async_session_factory() as session:
        # Oldest drafts first for steady cadence
        res = await session.execute(
            text(
                """
                SELECT id FROM blog_posts
                WHERE status = 'draft'
                ORDER BY created_at ASC
                LIMIT :limit
                """
            ),
            {"limit": batch_size},
        )
        rows = [r[0] for r in res.fetchall()]
        for pid in rows:
            if backfill_days and backfill_days > 0:
                pub_at = random_past_datetime(backfill_days)
            else:
                pub_at = datetime.utcnow()
            await session.execute(
                text(
                    "UPDATE blog_posts SET status = 'published', published_at = :published_at WHERE id = :id"
                ),
                {"published_at": pub_at, "id": pid},
            )
            published += 1
        await session.commit()
    return published


async def main_async(args) -> None:
    authors_path = Path(args.authors)
    if not authors_path.exists():
        raise SystemExit(f"Authors file not found: {authors_path}")
    authors = load_authors(authors_path)

    if args.assign_authors:
        num = await assign_authors(authors, limit=args.assign_limit)
        print(f"Assigned authors to {num} posts")

    if args.publish_batch:
        num = await publish_batch(args.publish_batch, backfill_days=args.backfill_days)
        print(f"Published {num} posts{' with backfilled dates' if args.backfill_days else ''}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--authors", default="blogs_docs/authors.json")
    ap.add_argument("--assign-authors", action="store_true")
    ap.add_argument("--assign-limit", type=int)
    ap.add_argument("--publish-batch", type=int)
    ap.add_argument("--backfill-days", type=int, help="Distribute published_at across the past N days")
    args = ap.parse_args()

    import asyncio
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()


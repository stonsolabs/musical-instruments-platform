"""
Seed or upsert additional blog categories used by AI templates.

Run:
  ENVIRONMENT=production python -m backend.scripts.data.seed_blog_categories

This script is idempotent: it upserts by slug.
"""
from __future__ import annotations

import asyncio
from typing import List, Dict
from sqlalchemy import text

from backend.app.database import async_session_factory


CATEGORIES: List[Dict[str, str]] = [
    {
        "name": "Comparisons",
        "slug": "comparisons",
        "description": "Head-to-head comparisons and buying decisions",
        "icon": "⚖️",
        "color": "#2563EB",
        "sort_order": 5,
    },
    {
        "name": "Deals",
        "slug": "deals",
        "description": "Best-value picks, budgets and seasonal offers",
        "icon": "💸",
        "color": "#059669",
        "sort_order": 6,
    },
    {
        "name": "Artist Spotlight",
        "slug": "artist-spotlight",
        "description": "Profiles of artists and their gear",
        "icon": "🎤",
        "color": "#7C3AED",
        "sort_order": 7,
    },
    {
        "name": "News",
        "slug": "news",
        "description": "New releases and important updates",
        "icon": "📰",
        "color": "#111827",
        "sort_order": 8,
    },
    {
        "name": "Quizzes",
        "slug": "quizzes",
        "description": "Interactive quizzes to find your gear",
        "icon": "❓",
        "color": "#F59E0B",
        "sort_order": 9,
    },
]


async def upsert_categories() -> None:
    async with async_session_factory() as session:
        for cat in CATEGORIES:
            exists = await session.execute(
                text("SELECT id FROM blog_categories WHERE slug = :slug"),
                {"slug": cat["slug"]},
            )
            if exists.scalar() is None:
                await session.execute(
                    text(
                        """
                        INSERT INTO blog_categories (name, slug, description, icon, color, sort_order, is_active)
                        VALUES (:name, :slug, :description, :icon, :color, :sort_order, true)
                        """
                    ),
                    {
                        "name": cat["name"],
                        "slug": cat["slug"],
                        "description": cat.get("description"),
                        "icon": cat.get("icon"),
                        "color": cat.get("color"),
                        "sort_order": cat.get("sort_order", 0),
                    },
                )
        await session.commit()


def main() -> None:
    asyncio.run(upsert_categories())


if __name__ == "__main__":
    main()


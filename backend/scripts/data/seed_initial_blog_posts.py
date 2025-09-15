"""
Create 10 initial blog posts with product associations.

Run:
  ENVIRONMENT=production python -m backend.scripts.data.seed_initial_blog_posts

Notes:
- Uses existing products by ID; adjust IDs if your DB differs.
- Looks up blog category IDs by slug (creates a minimal fallback to 'buying-guide').
- Posts are created as drafts by default; flip `auto_publish` to True to set `published_at`.
"""
from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import text

from backend.app.database import async_session_factory
from pathlib import Path
import json


# Helper content blocks (short, human-toned, SEO-aware)
def buying_guide_md(title: str, category_name: str) -> str:
    return f"""
## Why This {category_name} Guide Matters
Picking the right {category_name.lower()} can feel overwhelming. We cut through specs and marketing to show real differences that affect your sound, feel, and workflow.

## Key Considerations
- Playability: neck/profile and action matter more than raw specs
- Sound: pickups/samples, tone shaping, and dynamics
- Reliability: hardware, electronics, serviceability
- Budget: buy for today, with a clear upgrade path

## Top Recommendations
We hand-picked models that balance tone, feel, and value. Each pick includes who it fits and why.

## By Budget
- Budget: honest performance for practice and first recordings
- Mid-Range: gig-ready reliability and fuller tones
- Premium: pro-grade builds and classic voicings

## Final Advice
Try to match the instrument to your hands, ears, and context (home, studio, live). When in doubt, pick comfort and tuning stability first—great recordings follow.
""".strip()


def comparison_md(title: str) -> str:
    return f"""
## Introduction
These models are often compared for good reason: they target similar players but differ in feel, tone, and value. Here’s the verdict that saves you time.

## Quick Verdict
| Category | Winner | Why |
|---|---|---|
| Sound Quality | — | Depends on genre and pickups/voicing |
| Build Quality | — | Hardware and fretwork consistency |
| Value | — | What you get per dollar |
| Ease of Use | — | Setup, ergonomics, and controls |

## Sound & Performance
Focus on how tones sit in a mix and respond to touch. Subtle differences in midrange and transient snap often decide the right choice.

## Build & Playability
Fretwork, nut, and bridge quality determine tuning stability and confidence on stage.

## Who Should Buy Which
Match use-cases (beginner, studio, live) and genres to strengths. Always consider setup and string choice as force multipliers.
""".strip()


def tutorial_md(topic: str, level: str) -> str:
    return f"""
## What You’ll Learn
Practical steps to master {topic.lower()} with minimal friction. No fluff—just techniques that stick.

## Prerequisites
- {level} familiarity with your instrument
- Metronome or DAW for timing

## Step-by-Step
1. Warmups targeting accuracy before speed
2. Core technique with slow, deliberate reps
3. Musical application in simple grooves or chord cycles

## Common Mistakes
- Rushing reps without relaxed hands
- Ignoring micro-timing drift

## Gear That Helps
Transparent practice tools and comfortable, reliable instruments accelerate progress.

## Next Steps
Record short clips weekly. Review tone, timing, and touch.
""".strip()


POSTS: List[Dict[str, Any]] = [
    {
        "title": "Best Electric Guitars 2025: Complete Buying Guide for Every Budget",
        "slug": "best-electric-guitars-2025-buying-guide",
        "category_slug": "buying-guide",
        "excerpt": "Discover the top electric guitars of 2025 with clear picks for beginners, gigging players, and pros.",
        "seo_title": "Best Electric Guitars 2025 — Buying Guide",
        "seo_description": "Expert electric guitar picks by budget and skill level with real-world advice.",
        "content": buying_guide_md("Best Electric Guitars 2025", "Electric Guitar"),
        # Curated to models with real market demand and present in CSV
        "products": [645, 568, 5079, 966, 3167],
    },
    {
        "title": "Digital Piano Buying Guide 2025: Home Studio & Performance",
        "slug": "digital-piano-buying-guide-2025",
        "category_slug": "buying-guide",
        "excerpt": "Find the right digital piano with clear guidance on touch, tone, and connectivity.",
        "seo_title": "Best Digital Pianos 2025 — Guide",
        "seo_description": "Digital pianos compared for home, studio, and stage with honest recommendations.",
        "content": buying_guide_md("Digital Piano Buying Guide 2025", "Digital Piano"),
        # Curated to high-demand models found in CSV
        "products": [573, 865, 589, 722],
    },
    {
        "title": "Bass Guitar Showdown 2025: Fender Player II vs Yamaha TRBX vs Budget Alternatives",
        "slug": "bass-guitar-comparison-fender-yamaha-2025",
        "category_slug": "comparisons",
        "excerpt": "Head-to-head differences that actually matter for your tone, hands, and budget.",
        "seo_title": "Fender Player II vs Yamaha TRBX — 2025",
        "seo_description": "Direct bass comparison with verdicts by use-case and budget.",
        "content": comparison_md("Bass Guitar Showdown 2025"),
        "products": [381, 1143, 309],
    },
    {
        "title": "Best Acoustic Guitars for Singer-Songwriters (2025)",
        "slug": "acoustic-guitars-singer-songwriters-2025",
        "category_slug": "buying-guide",
        "excerpt": "Studio-ready tone, live reliability, and inspiring feel for writers and performers.",
        "seo_title": "Singer-Songwriter Acoustic Guitars 2025",
        "seo_description": "Acoustic guitars chosen for recording and live performance confidence.",
        "content": buying_guide_md("Acoustic Guitars for Singer-Songwriters", "Acoustic Guitar"),
        "products": [1184],
    },
    {
        "title": "Harley Benton vs Premium Brands 2025: When Budget Guitars Excel",
        "slug": "harley-benton-vs-premium-brands-2025",
        "category_slug": "comparisons",
        "excerpt": "How far have budget guitars come—and when do they beat premium picks?",
        "seo_title": "Harley Benton vs Premium Brands (2025)",
        "seo_description": "Value analysis with honest tradeoffs and upgrade paths.",
        "content": comparison_md("Harley Benton vs Premium Brands 2025"),
        "products": [253, 376, 619],
    },
    {
        "title": "Complete Home Recording Setup (2025): Essential Gear for Beginners",
        "slug": "home-recording-setup-essential-gear-2025",
        "category_slug": "buying-guide",
        "excerpt": "From interface to monitors, what you actually need to record well at home.",
        "seo_title": "Home Recording Setup Guide (2025)",
        "seo_description": "Beginner-friendly recording gear picks with clear upgrade paths.",
        "content": buying_guide_md("Home Recording Setup 2025", "Recording"),
        "products": [],
    },
    {
        "title": "Electric Guitar Setup Guide for Beginners",
        "slug": "electric-guitar-setup-guide-beginners",
        "category_slug": "tutorial",
        "excerpt": "Lower action, better intonation, and a guitar that stays in tune.",
        "seo_title": "Beginner Electric Guitar Setup Guide",
        "seo_description": "Step-by-step setup with tools and tips that actually help.",
        "content": tutorial_md("Electric Guitar Setup", "Beginner"),
        "products": [253, 376],
    },
    {
        "title": "MIDI Controller Buying Guide 2025: Keys, Pads, and Workflow",
        "slug": "midi-controller-buying-guide-2025",
        "category_slug": "buying-guide",
        "excerpt": "Find the right size, feel, and controls for your DAW and music.",
        "seo_title": "Best MIDI Controllers 2025 — Guide",
        "seo_description": "Weighted, synth-action, pads and knobs—what matters and why.",
        "content": buying_guide_md("MIDI Controller Buying Guide 2025", "MIDI Controller"),
        "products": [476, 486, 515, 525, 527],
    },
    {
        "title": "Studio Monitor Placement & Room Treatment Basics",
        "slug": "studio-monitor-placement-room-treatment",
        "category_slug": "tutorial",
        "excerpt": "Translate your mixes with simple acoustic wins and smart placement.",
        "seo_title": "Studio Monitors: Placement & Treatment",
        "seo_description": "Fix monitoring first. Simple steps for better mixes.",
        "content": tutorial_md("Studio Monitor Placement", "Beginner"),
        "products": [],
    },
    {
        "title": "Guitar Amp Modeling vs Real Amps (2025)",
        "slug": "guitar-amp-modeling-vs-real-amps-2025",
        "category_slug": "comparisons",
        "excerpt": "Tone, feel, convenience, and cost—what’s best for your context?",
        "seo_title": "Modelers vs Amps (2025)",
        "seo_description": "Modern modeling against tubes in studio and stage scenarios.",
        "content": comparison_md("Amp Modeling vs Real Amps"),
        "products": [],
    },
    {
        "title": "Best Synthesizers for Beginners (2025)",
        "slug": "best-synthesizers-beginners-2025",
        "category_slug": "buying-guide",
        "excerpt": "Friendly workflows, inspiring sounds, and room to grow.",
        "seo_title": "Best Beginner Synths (2025)",
        "seo_description": "Beginner synth picks with real learning potential and value.",
        "content": buying_guide_md("Best Synthesizers for Beginners", "Synthesizer"),
        "products": [507, 508, 509, 514, 519, 523],
    },
]


async def get_category_id(session, slug: str) -> Optional[int]:
    res = await session.execute(text("SELECT id FROM blog_categories WHERE slug = :slug"), {"slug": slug})
    row = res.fetchone()
    if row:
        return int(row[0])
    return None


async def create_post(
    session,
    *,
    title: str,
    slug: str,
    excerpt: str,
    content: str,
    category_id: Optional[int],
    seo_title: Optional[str],
    seo_description: Optional[str],
    products: List[int],
    auto_publish: bool = False,
) -> int:
    published_at = datetime.utcnow() if auto_publish else None
    result = await session.execute(
        text(
            """
            INSERT INTO blog_posts (
              title, slug, excerpt, content, category_id, status, seo_title, seo_description, reading_time, featured, published_at
            ) VALUES (
              :title, :slug, :excerpt, :content, :category_id, :status, :seo_title, :seo_description, :reading_time, false, :published_at
            ) RETURNING id
            """
        ),
        {
            "title": title,
            "slug": slug,
            "excerpt": excerpt,
            "content": content,
            "category_id": category_id,
            "status": "published" if auto_publish else "draft",
            "seo_title": seo_title,
            "seo_description": seo_description,
            "reading_time": max(1, round(len(content.split()) / 200)),
            "published_at": published_at,
        },
    )
    post_id = int(result.fetchone()[0])

    # Attach products (positioned order)
    for idx, pid in enumerate(products):
        await session.execute(
            text(
                """
                INSERT INTO blog_post_products (blog_post_id, product_id, position, context)
                VALUES (:post_id, :product_id, :position, :context)
                ON CONFLICT DO NOTHING
                """
            ),
            {
                "post_id": post_id,
                "product_id": pid,
                "position": idx,
                "context": "featured" if idx == 0 else "recommended",
            },
        )

    return post_id


async def seed_posts() -> None:
    async with async_session_factory() as session:
        # Optional: filter product associations to curated list if present
        curated_path = Path("blogs_docs/curated_products.json")
        curated_ids = set()
        if curated_path.exists():
            try:
                curated = json.loads(curated_path.read_text(encoding="utf-8"))
                curated_ids = set(curated.get("product_ids", []))
            except Exception:
                curated_ids = set()
        # ensure extra categories exist if needed
        # (user may already have run seed_blog_categories)
        for slug in {p["category_slug"] for p in POSTS}:
            if await get_category_id(session, slug) is None:
                # fallback to buying-guide id when slug missing
                pass

        created = []
        for post in POSTS:
            # skip if slug exists
            exists = await session.execute(text("SELECT id FROM blog_posts WHERE slug = :slug"), {"slug": post["slug"]})
            if exists.scalar() is not None:
                continue

            category_id = await get_category_id(session, post["category_slug"]) or await get_category_id(session, "buying-guide")

            # Optionally filter products by curated IDs
            post_products = post.get("products", [])
            if curated_ids:
                post_products = [pid for pid in post_products if pid in curated_ids]

            pid = await create_post(
                session,
                title=post["title"],
                slug=post["slug"],
                excerpt=post["excerpt"],
                content=post["content"],
                category_id=category_id,
                seo_title=post.get("seo_title"),
                seo_description=post.get("seo_description"),
                products=post_products,
                auto_publish=False,
            )
            created.append(pid)

        await session.commit()
        print(f"Seeded {len(created)} blog posts: {created}")


def main() -> None:
    asyncio.run(seed_posts())


if __name__ == "__main__":
    main()

#!/usr/bin/env python3.11
"""
Cleanup Images JSON
===================

Prune products.images to keep only the main image under a clean prefix.

Rules:
- Keep only one key: thomann_main
- The kept URL must live under the clean prefix (default: 'images/')
- Drop any other image keys and any URLs outside the clean prefix
- Do not invent URLs; only normalize/retain what's already valid

Behavior:
- By default runs in dry-run mode (no DB changes). Use --apply to write changes.
- Prints a summary of pruned records.

Env required:
- DATABASE_URL

Usage:
  DATABASE_URL=postgresql://... \
  python -m backend.scripts.maintenance.cleanup_images_json --clean-prefix images/ --apply
"""

from __future__ import annotations

import os
import re
import json
import argparse
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

import asyncpg


def normalize_images(obj: Any) -> Dict[str, Any]:
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, str):
        try:
            v = json.loads(obj)
            return v if isinstance(v, dict) else {}
        except Exception:
            return {}
    return {}


def extract_blob_rel_from_url(url: str) -> Optional[str]:
    if not url or not isinstance(url, str):
        return None
    m = re.search(r"/([A-Za-z0-9\-]+)/(.+)$", url)
    return m.group(2) if m else None


def is_under_clean_prefix(url: str, clean_prefix: str) -> bool:
    rel = extract_blob_rel_from_url(url) or ""
    return rel.startswith(clean_prefix)


def pick_main_under_clean(images: Dict[str, Any], clean_prefix: str) -> Optional[Dict[str, Any]]:
    """Return a normalized thomann_main dict if its URL is under clean prefix.
    If not, try to find any entry under clean_prefix and use it as main.
    """
    # 1) Prefer existing thomann_main if valid
    th = images.get('thomann_main')
    if isinstance(th, str):
        th = {"url": th}
    if isinstance(th, dict) and is_under_clean_prefix(th.get('url', ''), clean_prefix):
        return {
            "url": th.get('url'),
            "source": th.get('source', 'thomann'),
            "type": "main",
            "updated_by": "cleanup_images_json",
            "updated_at": datetime.utcnow().isoformat(),
        }

    # 2) Otherwise, search any other image entries for a valid clean URL
    for k, v in images.items():
        if k == 'thomann_main':
            continue
        if isinstance(v, str):
            url = v
        elif isinstance(v, dict):
            url = v.get('url')
        else:
            continue
        if isinstance(url, str) and is_under_clean_prefix(url, clean_prefix):
            return {
                "url": url,
                "source": (v.get('source') if isinstance(v, dict) else 'thomann') or 'thomann',
                "type": "main",
                "updated_by": "cleanup_images_json",
                "updated_at": datetime.utcnow().isoformat(),
            }

    return None


async def main():
    parser = argparse.ArgumentParser(description='Prune products.images to keep only main image under clean prefix')
    parser.add_argument('--clean-prefix', default='images/', help="Blob path prefix to keep (default: images/)")
    parser.add_argument('--apply', action='store_true', help='Apply DB changes (default: dry-run)')
    args = parser.parse_args()

    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print('❌ DATABASE_URL not set')
        return 1

    conn = await asyncpg.connect(db_url)
    try:
        rows = await conn.fetch("SELECT id, images FROM products ORDER BY id")
        total = len(rows)
        prunable = 0
        changed = 0

        update_sql = (
            """
            UPDATE products
            SET images = $1::jsonb, updated_at = NOW()
            WHERE id = $2
            """
        )

        for r in rows:
            pid = r['id']
            images = normalize_images(r['images'])
            if not images:
                continue

            # Detect if there are extra keys or non-clean URLs present
            keys = list(images.keys())
            has_extra_keys = len(keys) > 1
            has_non_clean = False
            for v in images.values():
                url = v if isinstance(v, str) else (v.get('url') if isinstance(v, dict) else '')
                if isinstance(url, str) and url and not is_under_clean_prefix(url, args.clean_prefix):
                    has_non_clean = True
                    break

            # If nothing to prune, skip
            if not has_extra_keys and not has_non_clean:
                continue

            prunable += 1

            # Build minimized images object
            main_entry = pick_main_under_clean(images, args.clean_prefix)
            if not main_entry:
                # No valid clean URL found; set images to empty
                new_images = {}
            else:
                new_images = {"thomann_main": main_entry}

            if args.apply:
                await conn.execute(update_sql, json.dumps(new_images), pid)
                changed += 1
            else:
                # Dry-run: show a small preview for first few
                if changed < 5:
                    print(f"Would update product {pid}: {keys} -> {list(new_images.keys())}")
                changed += 1

        print("\n📊 Cleanup summary:")
        print(f"  Total products: {total}")
        print(f"  Prunable: {prunable}")
        print(f"  {'Updated' if args.apply else 'Would update'}: {changed}")

    finally:
        await conn.close()

    return 0


if __name__ == '__main__':
    import asyncio
    raise SystemExit(asyncio.run(main()))


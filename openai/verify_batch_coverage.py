#!/usr/bin/env python3
"""
Verify that generated batch files cover all rows from the products table.

Usage:
  python3 openai/verify_batch_coverage.py                 # scans openai/batch_files
  python3 openai/verify_batch_coverage.py ./some/dir      # scans a custom directory
"""

import sys
from pathlib import Path
import json
import asyncio
from sqlalchemy import text
from database import get_async_session


async def count_products() -> int:
    async with await get_async_session() as session:
        res = await session.execute(text("SELECT COUNT(*) FROM products"))
        return int(res.scalar() or 0)


def scan_files(base: Path) -> tuple[int, int, set[str]]:
    files = sorted(base.glob("*.jsonl"))
    total_lines = 0
    total_files = 0
    ids: set[str] = set()
    for f in files:
        total_files += 1
        with f.open() as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                total_lines += 1
                try:
                    obj = json.loads(line)
                    cid = obj.get("custom_id")
                    if cid:
                        ids.add(cid)
                except Exception:
                    pass
    return total_files, total_lines, ids


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else (Path(__file__).parent / "batch_files")
    if not base.exists():
        print(f"❌ Directory not found: {base}")
        raise SystemExit(1)
    total_files, total_lines, ids = scan_files(base)
    print(f"📁 Files scanned: {total_files}")
    print(f"🧾 Total requests (lines): {total_lines}")
    print(f"🔑 Unique custom_ids: {len(ids)}")
    expected = asyncio.run(count_products())
    print(f"🗄️  Products in DB: {expected}")
    diff = expected - len(ids)
    if diff == 0:
        print("✅ Coverage looks complete (unique custom_ids == products)")
    elif diff > 0:
        print(f"⚠️  Missing {diff} products (by unique custom_id)")
    else:
        print(f"⚠️  {abs(diff)} more requests than products (duplicates or extras)")


if __name__ == "__main__":
    main()


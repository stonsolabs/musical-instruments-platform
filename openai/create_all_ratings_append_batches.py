#!/usr/bin/env python3
"""
Generate Azure OpenAI batch files for ALL products in chunks using ratings/append mode.

Usage examples:
  # Create batches in fixed-size chunks
  python3 openai/create_all_ratings_append_batches.py --chunk 500

  # Auto-calc chunk size to produce at most 7 files
  python3 openai/create_all_ratings_append_batches.py --max-files 7

  # Limit the total processed rows if needed
  python3 openai/create_all_ratings_append_batches.py --max-files 7 --max 5000

This produces multiple files under openai/batch_files/ with suffix ratings_append.
"""

import asyncio
from datetime import datetime
from pathlib import Path
import argparse
from sqlalchemy import text
from database import get_async_session
from create_azure_batch import create_azure_batch_file


async def count_rows() -> int:
    async with await get_async_session() as session:
        res = await session.execute(text("SELECT COUNT(*) FROM products"))
        return int(res.scalar() or 0)


async def run(chunk=None, max_total=None, max_files=None):
    total = await count_rows()
    if max_total is not None:
        total = min(total, max_total)
    if total <= 0:
        print("❌ No rows found to batch")
        return

    # Decide chunk size
    if max_files and max_files > 0:
        import math
        chunk = max(1, math.ceil(total / max_files))
        print(f"📦 Total rows: {total} | source=products | max_files={max_files} -> chunk={chunk}")
    else:
        if not chunk or chunk <= 0:
            chunk = 500
        print(f"📦 Total rows: {total} | source=products | chunk={chunk}")
    # Compute total parts for labeling
    import math
    total_parts = max(1, math.ceil(total / chunk))
    offset = 0
    created = []
    part_index = 1
    last_id = None
    processed = 0
    while processed < total:
        take = min(chunk, total - processed)
        if last_id is None:
            print(f"➡️  Creating batch for first {take} rows (ORDER BY id)")
        else:
            print(f"➡️  Creating batch after id>{last_id} for next {take}")
        result = await create_azure_batch_file(
            num_products=take,
            mode="ratings_append",
            prompt_file=None,
            offset=offset,  # kept for filename clarity
            part_index=part_index,
            total_parts=total_parts,
            start_id=last_id if last_id is not None else None,
            return_meta=True,
        )
        if result:
            filename, first_id, new_last_id = result
            created.append(filename)
            # Estimate how many we actually wrote by id range if available; else assume 'take'
            if first_id is not None and new_last_id is not None:
                wrote = new_last_id - (last_id or 0)
                # In rare cases of non-contiguous ids, fall back to 'take'
                if wrote <= 0 or wrote > take:
                    wrote = take
            else:
                wrote = take
            processed += wrote
            offset += take
            last_id = new_last_id if new_last_id is not None else last_id
        else:
            break
        part_index += 1
    print(f"✅ Created {len(created)} batch files")
    for f in created:
        print(f"  - {f}")


def main():
    parser = argparse.ArgumentParser(description="Create ratings/append batch files for all products")
    parser.add_argument("--chunk", type=int, default=None, help="Chunk size per batch file (overridden by --max-files if set)")
    parser.add_argument("--max", dest="max_total", type=int, default=None, help="Optional cap for total rows")
    parser.add_argument("--max-files", dest="max_files", type=int, default=None, help="Maximum number of files to generate (auto-chunks)")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args.chunk, args.max_total, args.max_files))


if __name__ == "__main__":
    main()

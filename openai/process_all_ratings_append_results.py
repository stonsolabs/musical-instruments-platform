#!/usr/bin/env python3
"""
Process ALL ratings/append result files in a directory and merge into products.content.

Usage:
  python3 openai/process_all_ratings_append_results.py                # defaults to batch_results
  python3 openai/process_all_ratings_append_results.py ./some/dir
  python3 openai/process_all_ratings_append_results.py --test         # test mode: process only first row of each file
  python3 openai/process_all_ratings_append_results.py ./some/dir --test
"""

import sys
from pathlib import Path
import asyncio
from process_ratings_append_results import process_file  # reuse per-file logic


def main():
    # Parse arguments
    test_mode = "--test" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != "--test"]
    
    base = Path(args[0]) if args else Path("batch_results")
    if not base.exists():
        print(f"❌ Directory not found: {base}")
        raise SystemExit(1)
    files = sorted(base.glob("*.jsonl"))
    if not files:
        print(f"❌ No .jsonl files in {base}")
        raise SystemExit(1)
    
    mode_text = "TEST MODE (first row only)" if test_mode else "FULL MODE"
    print(f"🔎 Found {len(files)} results to process in {base} ({mode_text})")
    
    for i, f in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing {f.name}")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(process_file(f, test_mode))
    print("\n🎉 Finished processing all ratings/append results")


if __name__ == "__main__":
    main()


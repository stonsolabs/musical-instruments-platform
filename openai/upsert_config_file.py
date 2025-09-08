#!/usr/bin/env python3
"""
Upsert a config file (prompt/schema) into the `config_files` table.

Usage examples:
  python3 openai/upsert_config_file.py --file openai/batch_prompt_ratings_append.txt
  python3 openai/upsert_config_file.py --file openai/batch_prompt.txt --as-name batch_prompt.txt
"""

import argparse
from pathlib import Path
from datetime import datetime
import asyncio
from sqlalchemy import text
from database import get_async_session


async def upsert_config(filename_key: str, content: str) -> None:
    async with await get_async_session() as session:
        await session.execute(
            text(
                """
                INSERT INTO config_files (filename, content, created_at, updated_at)
                VALUES (:filename, :content, NOW(), NOW())
                ON CONFLICT (filename)
                DO UPDATE SET content = EXCLUDED.content, updated_at = NOW();
                """
            ),
            {"filename": filename_key, "content": content},
        )
        await session.commit()


def main():
    parser = argparse.ArgumentParser(description="Upsert a config file into config_files table")
    parser.add_argument("--file", required=True, help="Path to local file to upload")
    parser.add_argument("--as-name", dest="as_name", default=None, help="Filename key to store as (default: basename)")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        raise SystemExit(f"File not found: {file_path}")

    content = file_path.read_text()
    filename_key = args.as_name or file_path.name

    print(f"🆙 Upserting config: {filename_key} (size={len(content)} chars)")
    asyncio.run(upsert_config(filename_key, content))
    print("✅ Done")


if __name__ == "__main__":
    main()


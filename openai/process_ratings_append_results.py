#!/usr/bin/env python3
"""
Process Azure OpenAI batch results for ratings/append mode and merge into products.content.

Usage:
  python3 openai/process_ratings_append_results.py path/to/results.jsonl [--test]
  python3 openai/process_ratings_append_results.py path/to/results.jsonl --test  # Process only first row for testing

Assumptions:
  - Each result line has `custom_id` in the form "<sku>|ratings_append"
  - The model returns JSON: {"content_append": { ...keys to merge into products.content... }}
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Any, Dict
from sqlalchemy import text
from database import get_async_session


def deep_merge_fill_missing(existing: Any, patch: Any) -> Any:
    """Merge that only fills missing or null values and never overwrites concrete data.
    - Dicts: recurse; add keys that are missing or None.
    - Lists: keep existing if non-empty; if empty/missing, use patch.
    - Scalars: keep existing if it is not None/empty string; else use patch.
    """
    if isinstance(existing, dict) and isinstance(patch, dict):
        out = dict(existing)
        for k, v in patch.items():
            if k not in out or out[k] is None:
                out[k] = v
            else:
                out[k] = deep_merge_fill_missing(out[k], v)
        return out
    if isinstance(existing, list):
        # If we already have content, keep it; otherwise use patch
        return existing if existing else (patch if isinstance(patch, list) else existing)
    # Scalars
    if existing is None or (isinstance(existing, str) and existing.strip() == ""):
        return patch
    return existing


async def merge_by_identifiers(ident: Dict[str, str], content_append: Dict[str, Any]) -> bool:
    async with await get_async_session() as session:
        row = None
        # Priority: id -> sku -> slug
        if ident.get("id"):
            res = await session.execute(text("SELECT id, content FROM products WHERE id = :id"), {"id": int(ident["id"])})
            row = res.fetchone()
        if not row and ident.get("sku"):
            res = await session.execute(text("SELECT id, content FROM products WHERE sku = :sku"), {"sku": ident["sku"]})
            row = res.fetchone()
        if not row and ident.get("slug"):
            res = await session.execute(text("SELECT id, content FROM products WHERE slug = :slug"), {"slug": ident["slug"]})
            row = res.fetchone()
        if not row:
            print(f"  ⚠️  Product not found for identifiers: {ident}")
            return False

        current = row.content or {}
        new_content = deep_merge_fill_missing(current, content_append)

        await session.execute(
            text("UPDATE products SET content = :content, updated_at = NOW() WHERE id = :id"),
            {"content": json.dumps(new_content), "id": row.id},
        )
        await session.commit()
        
        # Show detailed info in test mode
        if "--test" in sys.argv:
            print(f"  ✅ Updated product ID: {row.id}")
            print(f"  📝 Added keys: {list(content_append.keys())}")
            print(f"  🔍 Sample content: {str(content_append)[:200]}...")
        
        return True


def parse_custom_id(custom_id: str) -> Dict[str, str]:
    # Accept legacy format: "<sku>|..." or just "<sku>"
    out: Dict[str, str] = {}
    if not custom_id:
        return out
    parts = custom_id.split("|")
    for idx, token in enumerate(parts):
        if ":" in token:
            k, v = token.split(":", 1)
            out[k] = v
        else:
            # First bare token is treated as SKU for legacy
            if idx == 0 and "sku" not in out and "id" not in out and "slug" not in out:
                out["sku"] = token
    return out


async def process_file(results_path: Path, test_mode: bool = False) -> None:
    lines = results_path.read_text().splitlines()
    if test_mode:
        lines = lines[:1]  # Process only first line in test mode
        print(f"📄 Processing {results_path.name} in TEST MODE (first line only)")
    else:
        print(f"📄 Processing {results_path.name} with {len(lines)} lines")
    ok = err = 0
    for i, line in enumerate(lines, 1):
        try:
            obj = json.loads(line)
            custom_id = obj.get("custom_id") or ""
            if obj.get("error") is not None:
                err += 1
                continue
            body = obj.get("response", {}).get("body", {})
            content_text = body.get("choices", [{}])[0].get("message", {}).get("content")
            if not content_text:
                err += 1
                if test_mode:
                    print(f"  ❌ No content in response for line {i}")
                continue
            
            # Check if response was truncated due to token limit
            finish_reason = body.get("choices", [{}])[0].get("finish_reason")
            if finish_reason == "length":
                err += 1
                if test_mode:
                    print(f"  ❌ Response truncated due to token limit for line {i}")
                continue
            
            try:
                payload = json.loads(content_text)
            except json.JSONDecodeError as json_err:
                err += 1
                if test_mode:
                    print(f"  ❌ JSON decode error for line {i}: {json_err}")
                    print(f"  📄 Content preview: {content_text[:200]}...")
                continue
            append = payload.get("content_append")
            if not isinstance(append, dict):
                err += 1
                continue
            # Prefer identifiers inside the payload if present; fallback to custom_id tokens
            ident_payload = payload.get("identifiers") or {}
            ident = {}
            for k in ("id", "sku", "slug"):
                v = ident_payload.get(k)
                if v is not None and v != "":
                    ident[k] = v
            if not ident:
                ident = parse_custom_id(custom_id)
            merged = await merge_by_identifiers(ident, append)
            ok += 1 if merged else 0
        except Exception as e:
            err += 1
            if test_mode:  # Show detailed error in test mode
                print(f"  ❌ Error on line {i}: {e}")
                print(f"  📄 Line content: {line[:200]}...")
    print(f"✅ Merged: {ok} | ❌ Errors: {err}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 openai/process_ratings_append_results.py <results.jsonl> [--test]")
        sys.exit(1)
    
    # Parse arguments - filter out --test and get the file path
    args = [arg for arg in sys.argv[1:] if arg != "--test"]
    test_mode = "--test" in sys.argv
    
    if not args:
        print("Usage: python3 openai/process_ratings_append_results.py <results.jsonl> [--test]")
        sys.exit(1)
    
    path = Path(args[0])
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)
    
    # Use the older asyncio pattern for Python 3.6 compatibility
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_file(path, test_mode))


if __name__ == "__main__":
    main()

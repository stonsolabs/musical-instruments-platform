#!/usr/bin/env python3.11
"""
Reconcile And Move Product Images
=================================

Goal:
- Build a clean folder with exactly one correct blob per product.
- Update DB URLs to point to the clean folder.
- Leave source blobs intact (optional delete plan is generated; no deletes by default).

What it does:
1) Lists blobs under --source-prefix (default: thomann/)
2) For each product:
   - If DB references a source blob that exists: copy it to --clean-prefix and update DB
   - Else, if any source blob starts with "{product_id}_": pick newest, copy to --clean-prefix, update DB
3) Writes plans:
   - delete_plan.txt: redundant blobs per product (older duplicates) in source prefix
   - orphan_blobs.txt: source blobs that do not match any product id

Safety:
- Defaults to --dry-run; pass --apply to actually copy and update DB
- Concurrency is configurable
- --resume skips copies for destinations that already exist and still updates DB URLs

Env:
- AZURE_STORAGE_CONNECTION_STRING (required)
- AZURE_BLOB_CONTAINER (required)
- DATABASE_URL (required)

Usage (example):
  AZURE_STORAGE_CONNECTION_STRING=... \
  AZURE_BLOB_CONTAINER=product-images \
  DATABASE_URL=postgresql://... \
  python -m backend.scripts.maintenance.reconcile_and_move_images \
    --apply --concurrency 8 --source-prefix thomann/ --clean-prefix images/
    --rename-in-clean --resume
"""

from __future__ import annotations

import os
import re
import json
import argparse
import concurrent.futures
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set, DefaultDict
from collections import defaultdict

import asyncpg
from azure.storage.blob import BlobServiceClient, ContainerClient


def require_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Environment variable {name} is required")
    return v


def parse_account_name_from_conn_str(conn_str: str) -> Optional[str]:
    m = re.search(r"AccountName=([^;]+)", conn_str)
    return m.group(1) if m else None


def list_blobs(container: ContainerClient, prefix: str) -> List[str]:
    names: List[str] = []
    for i, blob in enumerate(container.list_blobs(name_starts_with=prefix or None), 1):
        names.append(blob.name)
        if i % 5000 == 0:
            print(f"   ...listed {i} blobs")
    return names


def newest_blob(blobs: List[str]) -> Optional[str]:
    if not blobs:
        return None
    def ts(name: str) -> datetime:
        base = name.split("/")[-1]
        m = re.match(r"^\d+_(\d{8}_\d{6})", base)
        if not m:
            return datetime.min
        try:
            return datetime.strptime(m.group(1), "%Y%m%d_%H%M%S")
        except Exception:
            return datetime.min
    return sorted(blobs, key=ts)[-1]


def extract_timestamp_from_blob_name(name: str) -> Optional[str]:
    """Extract YYYYMMDD_HHMMSS from blob filename if present."""
    base = name.split("/")[-1]
    m = re.match(r"^.+_(\d{8}_\d{6})\.[A-Za-z0-9]+$", base)
    return m.group(1) if m else None


def extract_blob_rel_from_url(url: str) -> Optional[str]:
    if not url or not isinstance(url, str):
        return None
    m = re.search(r"/([A-Za-z0-9\-]+)/(.+)$", url)
    # The second group is the container-relative blob path
    return m.group(2) if m else None


def make_image_json(url: str, note: str) -> str:
    return json.dumps({
        "url": url,
        "source": "thomann",
        "type": "main",
        "updated_by": "reconcile_and_move_images",
        "updated_note": note,
        "updated_at": datetime.utcnow().isoformat(),
    })


async def fetch_products(db_url: str) -> List[dict]:
    conn = await asyncpg.connect(db_url)
    try:
        rows = await conn.fetch("SELECT id, sku, name, images FROM products ORDER BY id")
        out: List[dict] = []
        for r in rows:
            out.append({
                "id": r["id"],
                "sku": r["sku"],
                "name": r["name"],
                "images": r["images"],
            })
        return out
    finally:
        await conn.close()


def normalize_images(images: Any) -> Dict[str, Any]:
    if images is None:
        return {}
    if isinstance(images, dict):
        return images
    if isinstance(images, str):
        try:
            obj = json.loads(images)
            return obj if isinstance(obj, dict) else {}
        except Exception:
            return {}
    return {}


def collect_db_references(products: List[dict]) -> Dict[str, Set[int]]:
    """Map container-relative blob path -> set(product_ids) referenced in DB."""
    ref: DefaultDict[str, Set[int]] = defaultdict(set)
    for p in products:
        pid = p["id"]
        images = normalize_images(p.get("images"))
        th = images.get("thomann_main")
        url = th if isinstance(th, str) else (th.get("url") if isinstance(th, dict) else None)
        blob_rel = extract_blob_rel_from_url(url) if url else None
        if blob_rel:
            ref[blob_rel].add(pid)
    return ref


def plan_moves(
    products: List[dict],
    source_blobs: List[str],
    source_prefix: str,
    clean_prefix: str,
    referenced_map: Dict[str, Set[int]],
    rename_in_clean: bool,
) -> Tuple[List[Dict[str, Any]], Dict[int, List[str]], List[str]]:
    """Create move/update plan.

    Returns:
      - actions: list of {product_id, src_blob, dest_blob, reason}
      - dupes_by_pid: map pid -> list of redundant source blobs (candidates not selected)
      - orphans: source blobs without a product_id
    """
    by_pid: DefaultDict[int, List[str]] = defaultdict(list)
    orphans: List[str] = []
    pid_re = re.compile(r"^" + re.escape(source_prefix) + r"(\d+)_")

    for name in source_blobs:
        m = pid_re.match(name)
        if m:
            by_pid[int(m.group(1))].append(name)
        else:
            # If the blob is referenced by any product in DB, treat it as candidate for that pid
            if name in referenced_map:
                for pid in referenced_map[name]:
                    by_pid[pid].append(name)
            else:
                orphans.append(name)

    # Current DB associations
    actions: List[Dict[str, Any]] = []
    dupes_by_pid: Dict[int, List[str]] = {}

    for p in products:
        pid = p["id"]
        images = normalize_images(p.get("images"))
        th = images.get("thomann_main")
        url = th if isinstance(th, str) else (th.get("url") if isinstance(th, dict) else None)
        src_blob_rel = extract_blob_rel_from_url(url) if url else None

        if src_blob_rel and not src_blob_rel.startswith(source_prefix):
            # If already in clean or other prefix, skip planning
            continue

        candidate_blobs = by_pid.get(pid, [])
        chosen_src: Optional[str] = None
        reason: str = ""

        if src_blob_rel and src_blob_rel in candidate_blobs:
            chosen_src = src_blob_rel
            reason = "promote_existing_db_blob"
        elif candidate_blobs:
            chosen_src = newest_blob(candidate_blobs)
            reason = "associate_newest_candidate"
        else:
            # No candidate to associate
            dupes_by_pid[pid] = []
            continue

        # Build destination path under clean prefix, keep the filename
        src_filename = chosen_src.split("/")[-1]
        if rename_in_clean:
            # Determine extension and timestamp
            ext = "jpg"
            if "." in src_filename:
                ext = src_filename.rsplit(".", 1)[-1] or "jpg"
            ts = extract_timestamp_from_blob_name(chosen_src) or datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            dest_filename = f"{pid}_{ts}.{ext}"
        else:
            dest_filename = src_filename

        dest_blob = f"{clean_prefix}{dest_filename}"

        # Duplicates (all others except chosen)
        dupes = [b for b in candidate_blobs if b != chosen_src]
        dupes_by_pid[pid] = dupes

        actions.append({
            "product_id": pid,
            "src_blob": chosen_src,
            "dest_blob": dest_blob,
            "reason": reason,
            "current_url": url or "",
        })

    return actions, dupes_by_pid, orphans


async def perform_copy_and_update(
    container: ContainerClient,
    account_name: str,
    db_url: str,
    actions: List[Dict[str, Any]],
    concurrency: int,
    resume_existing: bool,
):
    """Copy selected blobs to clean prefix and update DB URLs (async-friendly)."""

    def copy_one(src_blob: str, dest_blob: str) -> Tuple[str, str, bool, str]:
        try:
            src_client = container.get_blob_client(src_blob)
            dest_client = container.get_blob_client(dest_blob)
            data = src_client.download_blob().readall()
            dest_client.upload_blob(data, overwrite=True)
            return src_blob, dest_blob, True, ""
        except Exception as e:
            return src_blob, dest_blob, False, str(e)

    # Pre-scan destinations in resume mode to skip already-copied files
    preexisting_updates: List[Tuple[int, str]] = []
    pending_actions: List[Dict[str, Any]] = []
    skipped = 0
    if resume_existing:
        for a in actions:
            dest_client = container.get_blob_client(a["dest_blob"])
            try:
                if dest_client.exists():
                    # Destination already present; mark for DB update only
                    url = f"https://{account_name}.blob.core.windows.net/{container.container_name}/{a['dest_blob']}"
                    preexisting_updates.append((a["product_id"], url))
                    skipped += 1
                    continue
            except Exception:
                pass
            pending_actions.append(a)
        if skipped:
            print(f"   ↩️  Resume: skipping {skipped} already-existing destination files")
    else:
        pending_actions = actions

    loop = __import__("asyncio").get_running_loop()
    # Run copies via default thread pool executor to avoid blocking the event loop
    tasks = [loop.run_in_executor(None, copy_one, a["src_blob"], a["dest_blob"]) for a in pending_actions]

    results: List[Tuple[str, str, bool, str]] = []
    total = len(tasks)
    done_count = 0
    for fut in __import__("asyncio").as_completed(tasks):
        res = await fut
        results.append(res)
        done_count += 1
        if done_count % 50 == 0:
            print(f"   ...copied {done_count}/{total}")

    # Build URL updates for successes
    updates: List[Tuple[int, str]] = []
    # Map dest by index of action to get correct pairings
    # results may be out of order; build a quick lookup by (src,dest)
    result_ok_set = {(src, dest) for (src, dest, ok, _) in results if ok}
    for a in pending_actions:
        pair = (a["src_blob"], a["dest_blob"])
        if pair in result_ok_set:
            url = f"https://{account_name}.blob.core.windows.net/{container.container_name}/{a['dest_blob']}"
            updates.append((a["product_id"], url))

    # Merge preexisting updates (from resume)
    updates = preexisting_updates + updates

    # Apply DB updates
    conn = await asyncpg.connect(db_url)
    try:
        sql = (
            """
            UPDATE products
            SET images = jsonb_set(
                COALESCE(images, '{}'::jsonb),
                '{thomann_main}',
                $1::jsonb
            ), updated_at = NOW()
            WHERE id = $2
            """
        )
        for pid, url in updates:
            payload = make_image_json(url, "moved_to_clean_folder")
            await conn.execute(sql, payload, pid)
    finally:
        await conn.close()

    return results, updates


async def main():
    parser = argparse.ArgumentParser(description="Reconcile product images and move to an images folder")
    parser.add_argument("--source-prefix", default="thomann/", help="Source prefix to scan (default: thomann/)")
    parser.add_argument("--clean-prefix", default="images/", help="Destination clean prefix (default: images/)")
    parser.add_argument("--concurrency", type=int, default=8, help="Copy concurrency (default: 8)")
    parser.add_argument("--apply", action="store_true", help="Apply copies and DB updates (otherwise dry-run)")
    parser.add_argument("--rename-in-clean", action="store_true", help="Rename in clean folder to {product_id}_{YYYYMMDD_HHMMSS}.ext")
    parser.add_argument("--resume", action="store_true", help="Skip copy if destination already exists and still update DB")
    args = parser.parse_args()

    conn_str = require_env("AZURE_STORAGE_CONNECTION_STRING")
    container_name = require_env("AZURE_BLOB_CONTAINER")
    db_url = require_env("DATABASE_URL")
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME") or parse_account_name_from_conn_str(conn_str) or ""

    if not account_name:
        raise RuntimeError("AZURE_STORAGE_ACCOUNT_NAME not set and could not parse from connection string")

    # SDK clients
    svc = BlobServiceClient.from_connection_string(conn_str)
    container = svc.get_container_client(container_name)

    print("📦 Listing source blobs...")
    source_blobs = list_blobs(container, args.source_prefix)
    # Exclude blobs already under the clean prefix from source set
    if args.clean_prefix:
        source_blobs = [n for n in source_blobs if not n.startswith(args.clean_prefix)]
    print(f"   Found {len(source_blobs)} blobs under '{args.source_prefix}'")

    print("🔌 Loading products from DB...")
    products = await fetch_products(db_url)
    print(f"   Loaded {len(products)} products")

    print("🧠 Planning moves/associations...")
    referenced_map = collect_db_references(products)
    actions, dupes_by_pid, orphans = plan_moves(
        products, source_blobs, args.source_prefix, args.clean_prefix, referenced_map, args.rename_in_clean
    )
    print(f"   Planned {len(actions)} copy+update actions")
    print(f"   Orphan blobs (no product id): {len(orphans)}")

    # Write plans
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"reconcile_{ts}"
    with open(f"{base}_actions.json", "w") as f:
        json.dump(actions, f, indent=2)
    with open(f"{base}_delete_plan.txt", "w") as f:
        for pid, dupes in dupes_by_pid.items():
            for b in dupes:
                f.write(f"{b}\n")
    with open(f"{base}_orphans.txt", "w") as f:
        for b in orphans:
            f.write(f"{b}\n")

    print("📄 Plans written:")
    print(f"  - {base}_actions.json (copy + DB updates)")
    print(f"  - {base}_delete_plan.txt (redundant source blobs)")
    print(f"  - {base}_orphans.txt (blobs without product id)")

    if not args.apply:
        print("\n💡 Dry-run complete. Re-run with --apply to copy and update DB.")
        return 0

    print("🚚 Copying selected blobs and updating DB URLs...")
    results, updates = await perform_copy_and_update(container, account_name, db_url, actions, args.concurrency, args.resume)
    ok = sum(1 for _, _, s, _ in results if s)
    fail = len(results) - ok
    print(f"   Copy completed: {ok} ok, {fail} failed")
    print(f"   DB updates applied: {len(updates)}")

    print("\n✅ Reconcile and move completed.")
    return 0


if __name__ == "__main__":
    import asyncio
    raise SystemExit(asyncio.run(main()))

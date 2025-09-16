#!/usr/bin/env python3
"""
Validate Product Image References vs Azure Blob Storage
======================================================

This script cross-checks the `products.images` JSON against Azure Blob Storage
and reports inconsistencies. It handles these cases:

- OK: DB URL points to an existing blob
- wrong_blob_reference: DB URL blob missing, but there are blobs for the product ID in storage
- blob_missing_entirely: DB URL blob missing and no blobs exist for the product ID
- no_images_json: `images` column is null/empty/corrupted
- missing_thomann_main: `images` JSON exists but lacks `thomann_main`
- empty_or_null_url: `thomann_main.url` is empty/null

Outputs:
- JSON report with categorized issues
- CSV summary (product_id, sku, issue, current_url, suggested_new_url)
- Text file of product IDs that need re-download

Usage:
  DATABASE_URL=postgresql://... \
  python -m backend.scripts.maintenance.validate_product_images \
    --account-name getyourmusicgear \
    --container product-images

Requires:
- Azure CLI logged in with access to the storage account
- `az storage blob list` permissions to enumerate blobs
"""

from __future__ import annotations

import os
import re
import json
import csv
import argparse
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional, Set, DefaultDict
from collections import defaultdict

import asyncpg


def list_all_blob_names_sdk(conn_str: str, container: str, prefix: Optional[str] = "thomann/") -> List[str]:
    """List all blob names using Azure Storage SDK (handles full pagination)."""
    try:
        from azure.storage.blob import ContainerClient

        cc = ContainerClient.from_connection_string(conn_str, container)
        names: List[str] = []
        it = cc.list_blobs(name_starts_with=prefix or None)
        for i, blob in enumerate(it, 1):
            names.append(blob.name)
            if i % 2000 == 0:
                print(f"   ...listed {i} blobs via SDK")
        return names
    except Exception as e:
        print(f"❌ SDK listing failed: {e}")
        return []


def list_all_blob_names_cli(account_name: str, container: str, prefix: Optional[str] = "thomann/") -> List[str]:
    """List all blob names in the given container using Azure CLI."""
    try:
        cmd = [
            "az",
            "storage",
            "blob",
            "list",
            "--container-name",
            container,
            "--account-name",
            account_name,
            "--auth-mode","login",
            "--query",
            "[].name",
            "--output",
            "json",
        ]
        if prefix:
            cmd.extend(["--prefix", prefix])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr or "Failed to list blobs")
        return json.loads(result.stdout)
    except Exception as e:
        print(f"❌ Failed to list blobs: {e}")
        return []


def list_all_blob_names(account_name: str, container: str, prefix: Optional[str], use_sdk: bool) -> List[str]:
    """Auto-select listing method: SDK if available/desired, otherwise CLI."""
    if use_sdk:
        conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not conn_str:
            print("⚠️  --use-sdk specified but AZURE_STORAGE_CONNECTION_STRING is not set; falling back to CLI")
        else:
            names = list_all_blob_names_sdk(conn_str, container, prefix)
            if names:
                return names
            print("⚠️  SDK listing returned 0; falling back to CLI")
    # CLI fallback
    return list_all_blob_names_cli(account_name, container, prefix)


def build_blob_indexes(blob_names: List[str]) -> Tuple[Set[str], DefaultDict[int, List[str]]]:
    """Build quick lookup structures from blob names.

    Returns:
      - all_blobs: set of full blob names (e.g., 'thomann/1234_20240101_120000.jpg')
      - blobs_by_product: map of product_id -> list of blob names for that product
    """
    all_blobs: Set[str] = set(blob_names)
    blobs_by_product: DefaultDict[int, List[str]] = defaultdict(list)

    for name in blob_names:
        if name.startswith("thomann/"):
            filename = name[len("thomann/"):]
            m = re.match(r"^(\d+)_", filename)
            if m:
                pid = int(m.group(1))
                blobs_by_product[pid].append(name)

    return all_blobs, blobs_by_product


def extract_blob_from_url(url: str) -> Optional[str]:
    """Extract container-relative blob name from a URL.

    Example: https://acct.blob.core.windows.net/product-images/thomann/123_20240101_010101.jpg
    -> thomann/123_20240101_010101.jpg
    """
    if not url or not isinstance(url, str):
        return None
    m = re.search(r"/product-images/(.+)$", url)
    return m.group(1) if m else None


def build_blob_url(account_name: str, container: str, blob_name: str) -> str:
    return f"https://{account_name}.blob.core.windows.net/{container}/{blob_name}"


def newest_blob_for_product(blob_names: List[str]) -> Optional[str]:
    """Pick the newest blob for a product by extracting timestamp in name.

    Assumes pattern: thomann/{product_id}_YYYYMMDD_HHMMSS.ext. Falls back to last lexicographic.
    """
    if not blob_names:
        return None

    def parse_ts(name: str) -> datetime:
        # name is like 'thomann/123_20240101_121314.jpg'
        base = name.split("/")[-1]
        # take the part after first underscore and before extension
        m = re.match(r"^\d+_(\d{8}_\d{6})", base)
        if not m:
            return datetime.min
        ts_str = m.group(1)
        try:
            return datetime.strptime(ts_str, "%Y%m%d_%H%M%S")
        except Exception:
            return datetime.min

    return sorted(blob_names, key=parse_ts)[-1]


async def fetch_products(conn) -> List[dict]:
    rows = await conn.fetch(
        """
        SELECT id, sku, name, images
        FROM products
        ORDER BY id
        """
    )
    products: List[dict] = []
    for r in rows:
        products.append({
            "id": r["id"],
            "sku": r["sku"],
            "name": r["name"],
            "images": r["images"],
        })
    return products


def normalize_images(images: Any) -> Dict[str, Any]:
    if images is None:
        return {}
    if isinstance(images, dict):
        return images
    if isinstance(images, str):
        try:
            parsed = json.loads(images)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}
    return {}


async def main():
    parser = argparse.ArgumentParser(description="Validate product image references vs Azure Blob Storage")
    parser.add_argument("--account-name", default=os.getenv("AZURE_STORAGE_ACCOUNT_NAME", "getyourmusicgear"))
    parser.add_argument("--container", default=os.getenv("AZURE_BLOB_CONTAINER", "product-images"))
    parser.add_argument("--out-prefix", default="image_validation")
    parser.add_argument("--prefix", default="thomann/", help="Blob name prefix to list (default: thomann/)")
    parser.add_argument("--use-sdk", action="store_true", help="Use Azure Storage SDK for full blob listing (handles >5000)")
    parser.add_argument("--fix-db", action="store_true", help="Apply DB fixes for wrong_blob_reference using suggested URLs")
    parser.add_argument("--fix-concurrency", type=int, default=10, help="Max concurrent DB updates when --fix-db is set")
    parser.add_argument("--fix-dry-run", action="store_true", help="Show what would be updated without writing")
    args = parser.parse_args()

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL environment variable not set")
        return 1

    print("📦 Listing blobs from Azure Storage...")
    # Prefer SDK automatically if connection string is available, else CLI
    auto_use_sdk = args.use_sdk or bool(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
    blob_names = list_all_blob_names(args.account_name, args.container, args.prefix, auto_use_sdk)
    if len(blob_names) == 5000 and not auto_use_sdk:
        print("⚠️  Retrieved exactly 5000 blobs via CLI; results may be truncated. Consider setting AZURE_STORAGE_CONNECTION_STRING and using --use-sdk for full listing.")
    print(f"   Found {len(blob_names)} blobs in container '{args.container}'")

    all_blobs, blobs_by_product = build_blob_indexes(blob_names)

    print("🔌 Connecting to database...")
    conn = await asyncpg.connect(db_url)
    try:
        products = await fetch_products(conn)
    finally:
        await conn.close()

    print(f"📋 Validating {len(products)} products...")

    categories: Dict[str, List[Dict[str, Any]]] = {
        "ok": [],
        "wrong_blob_reference": [],
        "blob_missing_entirely": [],
        "no_images_json": [],
        "missing_thomann_main": [],
        "empty_or_null_url": [],
    }

    # Helper lists for outputs
    re_download_ids: List[int] = []

    for p in products:
        pid = p["id"]
        sku = p["sku"]
        name = p["name"]
        images = normalize_images(p.get("images"))

        if not images:
            categories["no_images_json"].append({"id": pid, "sku": sku, "name": name})
            re_download_ids.append(pid)
            continue

        th = images.get("thomann_main")
        if not th:
            categories["missing_thomann_main"].append({"id": pid, "sku": sku, "name": name})
            re_download_ids.append(pid)
            continue

        # thomann_main may be a dict or a string URL
        url = th if isinstance(th, str) else th.get("url")
        if not url or str(url).lower() == "null":
            categories["empty_or_null_url"].append({"id": pid, "sku": sku, "name": name})
            re_download_ids.append(pid)
            continue

        blob_rel = extract_blob_from_url(url)
        if not blob_rel:
            # Not a blob URL in expected format; treat as missing
            categories["wrong_blob_reference"].append(
                {
                    "id": pid,
                    "sku": sku,
                    "name": name,
                    "issue": "URL not in expected blob format",
                    "current_url": url,
                    "suggested_new_url": build_blob_url(
                        args.account_name,
                        args.container,
                        newest_blob_for_product(blobs_by_product.get(pid, [])) or "",
                    )
                    if blobs_by_product.get(pid)
                    else None,
                }
            )
            if not blobs_by_product.get(pid):
                re_download_ids.append(pid)
            continue

        if blob_rel in all_blobs:
            # OK
            categories["ok"].append({"id": pid, "sku": sku, "name": name, "url": url})
            continue

        # Blob missing - do we have any blob for this product id?
        candidate_blobs = blobs_by_product.get(pid, [])
        if candidate_blobs:
            newest = newest_blob_for_product(candidate_blobs)
            suggested_url = build_blob_url(args.account_name, args.container, newest) if newest else None
            categories["wrong_blob_reference"].append(
                {
                    "id": pid,
                    "sku": sku,
                    "name": name,
                    "issue": f"DB points to missing blob: {blob_rel}",
                    "current_url": url,
                    "suggested_new_url": suggested_url,
                }
            )
            # No re-download needed if a correct blob exists; DB can be fixed
        else:
            categories["blob_missing_entirely"].append(
                {
                    "id": pid,
                    "sku": sku,
                    "name": name,
                    "issue": f"No blobs found in storage for product_id={pid}",
                    "current_url": url,
                }
            )
            re_download_ids.append(pid)

    # Summaries
    summary = {k: len(v) for k, v in categories.items()}
    total = sum(summary.values())

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{args.out_prefix}_{ts}"
    json_path = f"{base}.json"
    csv_path = f"{base}.csv"
    ids_path = f"{base}_redownload_ids.txt"

    # Save JSON report
    with open(json_path, "w") as f:
        json.dump({"timestamp": ts, "summary": summary, "categories": categories}, f, indent=2)

    # Save CSV summary (issues only)
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id", "sku", "issue", "current_url", "suggested_new_url"])
        for key in ("wrong_blob_reference", "blob_missing_entirely", "no_images_json", "missing_thomann_main", "empty_or_null_url"):
            for item in categories[key]:
                writer.writerow(
                    [
                        item.get("id"),
                        item.get("sku"),
                        item.get("issue", key),
                        item.get("current_url", ""),
                        item.get("suggested_new_url", ""),
                    ]
                )

    # Save re-download IDs
    if re_download_ids:
        with open(ids_path, "w") as f:
            for pid in sorted(set(re_download_ids)):
                f.write(f"{pid}\n")

    # Console summary
    print("\n📊 Image validation results:")
    for k in ("ok", "wrong_blob_reference", "blob_missing_entirely", "no_images_json", "missing_thomann_main", "empty_or_null_url"):
        print(f"  - {k}: {summary.get(k, 0)}")

    print("\n📄 Outputs:")
    print(f"  - JSON report: {json_path}")
    print(f"  - CSV summary: {csv_path}")
    if re_download_ids:
        print(f"  - Re-download IDs: {ids_path}")
    else:
        print("  - Re-download IDs: (none)")

    # Guidance
    print("\n🚀 Next steps:")
    print("  - For 'wrong_blob_reference': update DB to suggested_new_url (no download needed)")
    print("  - For 'blob_missing_entirely' and other missing cases: feed IDs into your downloader")

    # Optional DB fix phase
    if args.fix_db:
        print("\n🛠️  Applying DB fixes for wrong_blob_reference...")

        # Prepare tasks for updates
        fixes: List[Dict[str, Any]] = [
            item for item in categories["wrong_blob_reference"]
            if item.get("suggested_new_url")
        ]

        if not fixes:
            print("  - No fixable entries found.")
            return 0

        # Build image JSON payloads
        def make_image_json(url: str) -> str:
            return json.dumps(
                {
                    "url": url,
                    "source": "thomann",
                    "fixed_at": datetime.utcnow().isoformat(),
                    "type": "main",
                }
            )

        # Update query
        update_sql = (
            """
            UPDATE products
            SET images = jsonb_set(
                COALESCE(images, '{}'::jsonb),
                '{thomann_main}',
                $1::jsonb
            ),
            updated_at = NOW()
            WHERE id = $2
            """
        )

        async def worker(worker_id: int, queue: "asyncio.Queue[Tuple[int, str]]"):
            pool = await asyncpg.create_pool(db_url, min_size=1, max_size=1)
            try:
                while True:
                    try:
                        pid, new_url = await queue.get()
                    except Exception:
                        break
                    try:
                        if args.fix_dry_run:
                            print(f"  [dry-run] would update product {pid} -> {new_url}")
                        else:
                            async with pool.acquire() as con:
                                await con.execute(update_sql, make_image_json(new_url), pid)
                            print(f"  ✔ updated product {pid}")
                    except Exception as e:
                        print(f"  ✖ failed to update product {pid}: {e}")
                    finally:
                        queue.task_done()
            finally:
                await pool.close()

        # Build queue
        import asyncio

        q: "asyncio.Queue[Tuple[int, str]]" = asyncio.Queue()
        for item in fixes:
            q.put_nowait((int(item["id"]), str(item["suggested_new_url"])))

        workers = [asyncio.create_task(worker(i + 1, q)) for i in range(max(1, args.fix_concurrency))]

        await q.join()
        for w in workers:
            w.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

        print("\n✅ DB fixes complete")

    return 0


if __name__ == "__main__":
    import asyncio

    raise SystemExit(asyncio.run(main()))

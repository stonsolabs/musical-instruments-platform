#!/usr/bin/env python3.11
"""
Image Maintenance Pipeline
==========================

One-stop CLI to:
- Validate product image URLs vs Azure Blob Storage (clean prefix)
- Download missing images (targeted) via Thomann crawler
- Reconcile: move/copy from source prefix (thomann/) to clean prefix (images/) and update DB
- Final validation

Usage examples
--------------

Environment (required):
  export DATABASE_URL='postgresql://...'
  export AZURE_STORAGE_CONNECTION_STRING='...'
  export AZURE_BLOB_CONTAINER='product-images'
  export AZURE_STORAGE_ACCOUNT_NAME='getyourmusicgear'

Run full pipeline (validate -> download missing -> reconcile -> validate):
  IPROYAL_PROXY_URL='http://user:pass@geo.iproyal.com:12321' \
  python -m backend.scripts.maintenance.image_pipeline --full-run --download-concurrency 6 --reconcile-concurrency 8

Validate only (clean prefix):
  python -m backend.scripts.maintenance.image_pipeline --validate-only

Download-only from a specific IDs file:
  IPROYAL_PROXY_URL='http://user:pass@geo.iproyal.com:12321' \
  python -m backend.scripts.maintenance.image_pipeline --download-only --ids-file image_validation_YYYYMMDD_HHMMSS_redownload_ids.txt

Notes
-----
- Clean prefix defaults to `images/`; source prefix defaults to `thomann/`.
- Uses Azure Storage SDK for blob listing (pagination) via the underlying validator script.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parents[3]


def _env_required(name: str):
    v = os.getenv(name)
    if not v:
        raise SystemExit(f"❌ Required environment variable not set: {name}")
    return v


def run(cmd: list[str], env: Optional[dict] = None) -> subprocess.CompletedProcess:
    print(f"➜ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=str(REPO_ROOT), env=env or os.environ.copy(), text=True)


def latest_missing_ids_file() -> Optional[Path]:
    files = sorted(REPO_ROOT.glob('image_validation_*_redownload_ids.txt'))
    return files[-1] if files else None


def step_validate(clean_prefix: str) -> Path:
    print("\n🔎 Step: Validate against clean prefix")
    _env_required('DATABASE_URL')
    _env_required('AZURE_STORAGE_CONNECTION_STRING')
    _env_required('AZURE_BLOB_CONTAINER')
    _env_required('AZURE_STORAGE_ACCOUNT_NAME')

    cmd = [
        sys.executable, '-m', 'backend.scripts.maintenance.validate_product_images',
        '--use-sdk', '--prefix', clean_prefix
    ]
    res = run(cmd)
    if res.returncode != 0:
        raise SystemExit("❌ Validation step failed")
    ids = latest_missing_ids_file()
    if not ids:
        print("✅ No re-download IDs file produced (everything OK)")
        return Path('')
    print(f"🗂️  Missing IDs file: {ids.name}")
    return ids


def step_download_missing(ids_file: Path, download_concurrency: int) -> None:
    print("\n📥 Step: Download missing product images (targeted)")
    _env_required('DATABASE_URL')
    _env_required('AZURE_STORAGE_CONNECTION_STRING')
    _env_required('AZURE_BLOB_CONTAINER')
    if not os.getenv('IPROYAL_PROXY_URL'):
        raise SystemExit("❌ IPROYAL_PROXY_URL environment variable is required for downloading")

    if not ids_file.exists():
        raise SystemExit(f"❌ IDs file not found: {ids_file}")

    cmd = [
        sys.executable, '-m', 'backend.scripts.crawlers.enhanced_thomann_crawler',
        '--input-file', str(ids_file),
        '--max-concurrent', str(download_concurrency)
    ]
    res = run(cmd)
    if res.returncode != 0:
        raise SystemExit("❌ Download step failed")


def step_reconcile(source_prefix: str, clean_prefix: str, reconcile_concurrency: int, resume: bool, rename: bool) -> None:
    print("\n🔀 Step: Reconcile to clean prefix and update DB")
    _env_required('DATABASE_URL')
    _env_required('AZURE_STORAGE_CONNECTION_STRING')
    _env_required('AZURE_BLOB_CONTAINER')

    cmd = [
        sys.executable, '-m', 'backend.scripts.maintenance.reconcile_and_move_images',
        '--source-prefix', source_prefix,
        '--clean-prefix', clean_prefix,
        '--concurrency', str(reconcile_concurrency),
        '--apply'
    ]
    if resume:
        cmd.append('--resume')
    if rename:
        cmd.append('--rename-in-clean')

    res = run(cmd)
    if res.returncode != 0:
        raise SystemExit("❌ Reconcile step failed")


def main():
    parser = argparse.ArgumentParser(description='Image maintenance pipeline')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('--full-run', action='store_true', help='Validate -> download missing -> reconcile -> validate')
    g.add_argument('--validate-only', action='store_true')
    g.add_argument('--download-only', action='store_true')
    g.add_argument('--reconcile-only', action='store_true')

    parser.add_argument('--ids-file', help='IDs file to download (defaults to latest generated)')
    parser.add_argument('--download-concurrency', type=int, default=6)
    parser.add_argument('--reconcile-concurrency', type=int, default=8)
    parser.add_argument('--source-prefix', default='thomann/')
    parser.add_argument('--clean-prefix', default='images/')
    parser.add_argument('--resume', action='store_true', help='Skip copy if destination exists; still update DB')
    parser.add_argument('--rename-in-clean', action='store_true', help='Rename to {product_id}_{YYYYMMDD_HHMMSS}.ext in clean prefix')

    args = parser.parse_args()

    if args.validate_only:
        step_validate(args.clean_prefix)
        return

    if args.download_only:
        ids = Path(args.ids_file) if args.ids_file else latest_missing_ids_file()
        if not ids:
            raise SystemExit('❌ No IDs file specified and none found from previous validation')
        step_download_missing(ids, args.download_concurrency)
        return

    if args.reconcile_only:
        step_reconcile(args.source_prefix, args.clean_prefix, args.reconcile_concurrency, args.resume, args.rename_in_clean)
        return

    # Default: full run
    if not args.full_run:
        print("ℹ️ No mode selected; defaulting to --full-run")

    ids = step_validate(args.clean_prefix)
    if ids and ids.exists():
        step_download_missing(ids, args.download_concurrency)
        step_reconcile(args.source_prefix, args.clean_prefix, args.reconcile_concurrency, resume=True, rename=args.rename_in_clean or True)
        step_validate(args.clean_prefix)
    else:
        print("✅ Nothing to download; proceeding to reconcile and final validation")
        step_reconcile(args.source_prefix, args.clean_prefix, args.reconcile_concurrency, resume=True, rename=args.rename_in_clean or True)
        step_validate(args.clean_prefix)


if __name__ == '__main__':
    main()


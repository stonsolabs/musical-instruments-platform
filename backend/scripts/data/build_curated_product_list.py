"""
Build a curated product ID list from internal docs so batch generation only targets
high-demand products that people actually search for.

Sources:
- blogs_docs/best-selling-products-by-retailer.md (names)
- blogs_docs/blog_post_ideas.md (explicit product ID lists)
- blogs_docs/getyourmusicgear_public_products.csv (ID/name mapping)

Run:
  python -m backend.scripts.data.build_curated_product_list \
    --csv blogs_docs/getyourmusicgear_public_products.csv \
    --best blogs_docs/best-selling-products-by-retailer.md \
    --ideas blogs_docs/blog_post_ideas.md \
    --out blogs_docs/curated_products.json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


def load_csv_map(csv_path: Path) -> Tuple[Dict[str, int], Dict[int, str]]:
    name_to_id: Dict[str, int] = {}
    id_to_name: Dict[int, str] = {}
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            pid = int(r["id"])  # guaranteed
            name = r["name"].strip()
            id_to_name[pid] = name
            key = normalize_name(name)
            name_to_id[key] = pid
    return name_to_id, id_to_name


def normalize_name(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9\s]+", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_best_selling(md_path: Path, name_to_id: Dict[str, int]) -> List[Tuple[int, str]]:
    txt = md_path.read_text(encoding="utf-8", errors="ignore")
    # capture **Product Name** markers
    names = re.findall(r"\*\*([^\*]+)\*\*", txt)
    found: List[Tuple[int, str]] = []
    for raw in names:
        key = normalize_name(raw)
        pid = name_to_id.get(key)
        if pid:
            found.append((pid, raw.strip()))
    return found


def parse_ideas_ids(md_path: Path) -> List[int]:
    txt = md_path.read_text(encoding="utf-8", errors="ignore")
    ids: List[int] = []
    for match in re.finditer(r"Featured Products:\s*\[([^\]]+)\]", txt):
        blob = match.group(1)
        for num in re.findall(r"\d+", blob):
            ids.append(int(num))
    return ids


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, type=Path)
    ap.add_argument("--best", required=True, type=Path)
    ap.add_argument("--ideas", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    name_to_id, id_to_name = load_csv_map(args.csv)
    best_pairs = parse_best_selling(args.best, name_to_id)
    idea_ids = parse_ideas_ids(args.ideas)

    curated_ids = {pid for pid, _ in best_pairs}
    curated_ids.update(idea_ids)

    # Compose output data
    data = {
        "product_ids": sorted(curated_ids),
        "by_name": [
            {"id": pid, "name": name} for pid, name in sorted(best_pairs, key=lambda x: x[1].lower())
        ],
        "source_counts": {
            "best_selling_matched": len(best_pairs),
            "ideas_ids": len(idea_ids),
            "unique_total": len(curated_ids),
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote curated list with {len(curated_ids)} unique IDs to {args.out}")


if __name__ == "__main__":
    main()


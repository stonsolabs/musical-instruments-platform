"""
Build JSONL files for Azure/OpenAI Batch generation.

Creates 500-request-per-file JSONL with one chat completion request per line.

Run examples:
  python -m backend.scripts.data.build_batch_requests --csv blogs_docs/getyourmusicgear_public_products.csv --out openai/batch/buying_guides_500.jsonl --type buying_guide
  python -m backend.scripts.data.build_batch_requests --csv blogs_docs/getyourmusicgear_public_products.csv --out openai/batch/comparisons_500.jsonl --type comparison

Notes:
- Uses product id+name from the CSV. If brand/category names are needed, enrich CSV or join via DB.
- Prompts align with AI_BLOG_SYSTEM and blogs_docs/openai-batch-generation-prompts.md
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path
from typing import List, Dict, Any


SYSTEM_PROMPT = (
    "You are an expert music gear writer with 20+ years of experience. "
    "Your tone is authoritative, practical, SEO-conscious, and conversion friendly. "
    "NEVER invent specifications; only use provided product info. Output strict JSON only."
)


def load_products(csv_path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "id": int(r["id"]),
                "name": r["name"],
                "slug": r["slug"],
                "brand_id": int(r["brand_id"]) if r.get("brand_id") else None,
                "category_id": int(r["category_id"]) if r.get("category_id") else None,
            })
    return rows


def pick_products(products: List[Dict[str, Any]], n: int, category_id: int | None = None) -> List[Dict[str, Any]]:
    pool = [p for p in products if (category_id is None or p.get("category_id") == category_id)] or products
    return random.sample(pool, k=min(n, len(pool)))


def build_buying_guide_prompt(title: str, category: str, featured: List[Dict[str, Any]]) -> str:
    product_list = "\n".join([f"- {p['name']} (ID: {p['id']})" for p in featured])
    return (
        f"Write a comprehensive 2,000-word buying guide titled '{title}' focusing on {category}.\n\n"
        "Structure: Hook intro, quick recommendations, buying considerations, detailed reviews for each featured product, comparison matrix, genre-specific picks, conclusion.\n"
        "For each product: why it made the list, specs, sound/feel, who it's for, pros/cons (4-6), and a clear value proposition.\n\n"
        f"Products to feature (use only these, do not invent):\n{product_list}\n\n"
        "SEO: target phrase in H1, natural secondary keywords, meta description < 160 chars, suggest schema.org types.\n"
        "Affiliate: include 'Check Latest Price' CTAs without prices."
    )


def build_comparison_prompt(title: str, category: str, featured: List[Dict[str, Any]]) -> str:
    names = ", ".join([p["name"] for p in featured])
    product_list = "\n".join([f"- {p['name']} (ID: {p['id']})" for p in featured])
    return (
        f"Create a detailed 1,800-word comparison: {names} — Which {category} Should You Buy?\n\n"
        "Include: intro, quick verdict table, spec comparison, sound & performance, build & ergonomics, value analysis, user experience, final recommendations by use-case and budget.\n\n"
        f"Products (use only these):\n{product_list}\n"
        "Never invent specifications; focus on real buyer-relevant differences."
    )


def make_jsonl(records: List[Dict[str, Any]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def build_records(products: List[Dict[str, Any]], kind: str, total: int) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for i in range(1, total + 1):
        if kind == "buying_guide":
            featured = pick_products(products, n=5)
            title = f"Buying Guide #{i}: Finding the Right Instrument"
            user = build_buying_guide_prompt(title, "musical instruments", featured)
        elif kind == "comparison":
            featured = pick_products(products, n=3)
            title = f"Comparison #{i}: Which Model Fits You"
            user = build_comparison_prompt(title, "instrument", featured)
        else:
            raise ValueError("Unknown type. Use 'buying_guide' or 'comparison'.")

        # Minimal, provider-agnostic batch request format
        body = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7,
            "max_tokens": 4000,
        }
        records.append({
            "custom_id": f"blog-{kind}-{i:04d}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": body,
        })
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--type", required=True, choices=["buying_guide", "comparison"]) 
    parser.add_argument("--total", type=int, default=500)
    parser.add_argument("--curated", type=Path, help="Optional curated_products.json to restrict selection")
    args = parser.parse_args()

    products = load_products(args.csv)
    if args.curated and args.curated.exists():
        curated = json.loads(args.curated.read_text(encoding="utf-8"))
        allow = set(curated.get("product_ids", []))
        if allow:
            products = [p for p in products if p["id"] in allow]
    records = build_records(products, args.type, args.total)
    make_jsonl(records, args.out)
    print(f"Wrote {len(records)} requests to {args.out}")


if __name__ == "__main__":
    main()

Batch JSONL Files
------------------

This folder holds JSONL files for Azure/OpenAI Batch processing. Each file contains 500 chat completion requests (one per line) aligned with our blog generation templates and SEO/conversion guidelines.

Build files locally:

```bash
python -m backend.scripts.data.build_batch_requests --csv blogs_docs/getyourmusicgear_public_products.csv --out openai/batch/buying_guides_500.jsonl --type buying_guide --total 500
python -m backend.scripts.data.build_batch_requests --csv blogs_docs/getyourmusicgear_public_products.csv --out openai/batch/comparisons_500.jsonl --type comparison --total 500
```

Then follow the Admin Batch endpoints in `AI_BLOG_SYSTEM.md` to upload, start, and process results.


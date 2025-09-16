GetYourMusicGear – Architecture & Context (Summary) (moved to docs/)
===================================================================

Overview
--------

- Backend: FastAPI (Python, SQLAlchemy, PostgreSQL) in `backend/`
- Frontend: Next.js + TypeScript + Tailwind in `frontend/`
- Frontend calls backend via local proxy API: `/api/proxy/v1/...` (no direct Azure calls).

Notable Enhancements (2025-09)
------------------------------

- Admin Auth & Docs
  - SSO bridge on API domain issues `X-Admin-Token` to avoid third‑party cookie loops; docs iframe allowed via CSP `frame-ancestors`.
  - Robust Azure AD claim parsing and `ADMIN_EMAILS` multi-admin support.
- Compare Page UX
  - Mobile-fit fixes; subtle difference dots + legend; product names linked; warranty section removed.
- Trending
  - Votes influence trending: views + 3×comparisons + 2×vote_score.
- Affiliate Fetch
  - Use `GET /products/{id}/affiliate-urls` when no store links are provided (POST only when sending links).
- AI Blog System
  - **Structured JSON Generation**: All 24 templates now generate structured JSON format with sections, headers, and product integration
  - **Professional Content**: Removed all AI mentions and emoticons, content appears completely human-written
  - **Enhanced Templates**: 24 active templates covering all content types (reviews, guides, comparisons, tutorials, seasonal, artist spotlights, etc.)
  - **Batch Processing**: Comprehensive batch generation system for 86+ posts using OpenAI batch API (50% cost savings)
- Blog Main Page
  - Added “Most Read” and “Popular Tags” sections for better internal linking and discovery.
- Technical SEO
  - Canonicals, OG/Twitter, robots, JSON‑LD (BlogPosting/Product/BreadcrumbList/WebSite SearchAction).

Frontend
--------

- Pages (SSR): `/`, `/products`, `/products/[slug]`, `/compare`, `/blog/*`, `/privacy`, `/terms`, `/contact`
- Components: layout (Header/Footer), product (Gallery/Info/Specifications/ContentSections/Voting), compare (CompareSearch/ComparisonTable), affiliate (AffiliateButtons), blog (BlogManager/BlogAIGenerator/BlogPostEditor/BlogPostCard/BlogProductShowcase), misc (InstrumentRequestForm)
- Styling: Tailwind with tokens (`brand.*`, `store.thomann`, `store.gear4music`); CTAs standardized as `btn-primary` / `btn-secondary`.
- Affiliate buttons: vertical (`space-y-3`), label "View at [Store]", consistent branding via Tailwind tokens. Logo sizes: compact 32px, full 40px.
- Product & Compare views:
  - Product detail: no prices; shows professional ratings (0-100 scale), community votes (🤘/👎); comprehensive content from `product.content` including Q&A, setup tips, warranty info, audience fit analysis, accessory recommendations. Rich content organized in sections: Overview & Guidance, Technical & Professional Analysis, and expandable details sections.
  - Listing images (Product grid): clicking opens product detail page. All store links resolve via EnhancedAffiliateService with priority scoring and exclusivity rules.
  - Compare: Comprehensive comparison with professional ratings, community votes, detailed specifications table, Q&A section (moved to end), removed "Additional Information" metadata section, fixed tab navigation (Overview, Differences, Specifications, Analysis, Reviews, Clear All).
- Autocomplete: Hero & CompareSearch; debounced; thumbnails when available; keyboard navigation (Up/Down/Enter/Esc).
- Nav highlighting: precise per category/sort.

Frontend Data Access
-------------------

- Proxy API route: `frontend/pages/api/proxy/[...path].ts`
  - Target: `NEXT_PUBLIC_API_BASE_URL + '/api/' + path`
  - Adds `X-API-Key` (server env); forwards body; returns JSON/text.
- `src/lib/api.ts`:
  - `PROXY_BASE = '/api/proxy/v1'`
  - SSR-safe `apiFetch()` builds absolute URLs using `NEXT_PUBLIC_APP_ORIGIN` (or `VERCEL_URL`/`http://localhost:3000`).
- Endpoints used: `/products`, `/products/{id}`, `/search/autocomplete`, `/compare`, `/trending/instruments`, `/categories`, `/brands`, `/products/{id}/affiliate-urls` (GET) and `/products/{id}/affiliate-stores` (POST with links), `/instrument-requests`, `/voting/products/{id}/vote`, `/voting/products/{id}/stats`, `/blog/*` (categories, posts, templates, generate, clone-rewrite, generation-history, tags/popular, ai-posts).
  - Voting: submit via `/api/proxy/v1/voting/products/{id}/vote` with `{ vote_type: 'up'|'down' }`; after submit, refetch `/api/proxy/v1/voting/products/{id}/stats` and update UI live.
  - `fetchProduct(slugOrId)`: tries `/products?slugs=<slug>`, then `/search/autocomplete` match, then `/products/{id}` if numeric.
  - `fetchProducts(...)` normalizes backend pagination into SearchResult: `{ products, total, page, per_page, total_pages }`.

Backend
-------

- API routers (prefix `/api/v1`): products, compare, trending, search, voting, affiliate_stores, instrument_requests, blog (AI), admin (protected), docs (protected).
- Business logic:
  - EnhancedAffiliateService: 
    * Brand exclusivity rules: If a brand has an exclusive store relationship, only that store is shown for products of that brand
    * Regional preferences: Stores can have different priority scores based on user region
    * Priority scoring: Combines store priority, regional boosts, brand exclusivity boosts, and store link availability
    * Affiliate URL generation: Automatically adds affiliate parameters and handles domain-specific affiliate IDs
    * Store filtering: Only shows active stores with affiliate programs and visible buttons
  - TrendingService: trending instruments and comparisons (views + comparisons + votes).
  - Vote utils: aggregates thumbs_up_count, thumbs_down_count, total_votes, vote_score.
  - Content enrichment: Backend returns all rich content fields (qa, setup_tips, audience_fit, professional_ratings, etc.) via get_clean_content() function
  - BlogAIGenerator: AI-powered blog generation with provider routing (OpenAI/Azure), specialized templates, clone & rewrite flow, guaranteed attachment of selected products, and tracking

Database (Key Tables)
---------------------

- brands: id, name (unique), slug (unique), logo_url, website_url, description, created_at
  - Unknown brand entries (`name='Unknown Brand'` or `slug='unknown-brand'`) are filtered out server-side and hidden from the Brand filter UI.
- categories: id, name, slug (unique), parent_id (self FK), description, image_url, is_active, created_at
- products: id, sku (unique), name, slug (unique), brand_id (FK), category_id (FK), description, images (JSON), content (JSON; narratives/specs/store_links/QA/localized), avg_rating, review_count, is_active, category_attributes (JSON), last_crawled, OpenAI fields, created_at, updated_at
- affiliate_stores: id, name, slug (unique), website_url, logo_url, affiliate settings (has_affiliate_program, affiliate_id, affiliate_parameters, domain_affiliate_ids), priority, show_affiliate_buttons, regional settings (available_regions, regional_priority, primary_region), fallbacks, created_at, updated_at
- product_prices: id, product_id (FK), store_id (FK), price, currency, affiliate_url, is_available, last_checked, created_at, updated_at, unique(product_id, store_id)
- brand_exclusivities: id, brand_name, store_id (FK to affiliate_stores), is_exclusive (boolean), regions (JSON), priority_boost, created_at, updated_at
- comparison_views: id, product_ids (ARRAY[int]), user_ip, user_country, created_at
- affiliate_clicks: id, product_id, store_id, user_ip, user_country, referrer, created_at
- product_votes: id, product_id, user_ip, vote_type ('up'/'down'), created_at, updated_at, unique(product_id, user_ip)
- crawler tables: crawler_sessions, crawler_metrics, crawler_config, crawler_jobs; products_filled (crawler output)
- openai_batches: id, batch_id (unique), filename, product_count, status, openai_job_id, result_file
- blog_categories: id, name (unique), slug (unique), description, icon, color, sort_order, is_active, created_at, updated_at
- blog_posts: id, title, slug (unique), excerpt, content, featured_image, category_id (FK), author_name, status, seo_title, seo_description, reading_time, view_count, featured, published_at, created_at, updated_at, generated_by_ai, generation_prompt, generation_model, generation_params (JSON), ai_notes
- blog_tags: id, name (unique), slug (unique), created_at
- blog_post_tags: id, blog_post_id (FK), tag_id (FK), created_at, unique(blog_post_id, tag_id)
- blog_post_products: id, blog_post_id (FK), product_id (FK to products), position, context, ai_context, relevance_score, mentioned_in_sections (JSON), created_at, unique(blog_post_id, product_id)
- blog_content_sections: id, blog_post_id (FK), section_type, section_title, section_content, section_order, products_featured (JSON), ai_generated, created_at
- blog_generation_templates: id, name (unique), description, category_id (FK), template_type, base_prompt, system_prompt, product_context_prompt, required_product_types (JSON), min_products, max_products, suggested_tags (JSON), seo_title_template, seo_description_template, content_structure (JSON), is_active, created_at, updated_at
- blog_generation_history: id, blog_post_id (FK), template_id (FK), generation_status, prompt_used, model_used, tokens_used, generation_time_ms, error_message, generation_metadata (JSON), created_at

Environment
-----------

- Frontend (`frontend/.env.local`):
  - `NEXT_PUBLIC_API_BASE_URL=https://getyourmusicgear-api.azurewebsites.net`
  - `API_KEY=<your api key>` (used by proxy)
  - `NEXT_PUBLIC_APP_ORIGIN=https://getyourmusicgear.com` (or `http://localhost:3000` for dev SSR)
- Backend: see `backend/app/config.py`
  - `OPENAI_API_KEY=<openai key>` (required for AI blog generation)

Store Exclusivity & Affiliate Logic
------------------------------------

The EnhancedAffiliateService implements a sophisticated affiliate store selection system:

1. **Brand Exclusivity**: When a brand has an exclusive relationship with a store (is_exclusive=True in brand_exclusivities table), only that store will be shown for products of that brand. This ensures compliance with exclusive retailer agreements.

2. **Priority Scoring System**: 
   - Base priority: Each store has a base priority score
   - Regional boost: Stores can have higher priority in specific regions
   - Brand preference: Non-exclusive brand preferences add priority boost
   - Store link availability: Products with direct store URLs get +100 priority
   - Primary region match: Stores get +50 priority in their primary region

3. **Affiliate URL Generation**:
   - Uses store's affiliate_parameters and domain_affiliate_ids
   - Supports domain-specific affiliate IDs (e.g., different IDs for thomann.de vs thomann.co.uk)
   - Handles special cases like Thomann's RediR™ system for regional redirects
   - Falls back to store's base URL if no specific product URL available

4. **Store Filtering**:
   - Only shows stores with is_active=True, has_affiliate_program=True, show_affiliate_buttons=True
   - Respects regional availability (available_regions field)
   - Caches results to avoid duplicate API calls

Extending Safely
----------------

- Always use proxy for frontend HTTP calls
- Keep CTAs to `btn-primary` / `btn-secondary`  
- Keep affiliate buttons vertical with consistent "View at [Store]" labeling
- Avoid prices in product/compare views
- Add store tokens to Tailwind for consistent branding
- Content sections properly organized: Overview & Guidance, Technical Analysis, expandable details
- Hide Price Range filter (backend price filtering removed); keep fields dormant until API support returns
- Compare page: comprehensive comparison table with community votes, professional ratings, Q&A moved to end

AI Blog System
--------------

The platform features an advanced, human‑tone AI-powered blog system with rich structure, admin controls, and SEO‑first presentation.

Core features
- Human editorial style: prompts enforce natural tone (contractions, varied sentences), concrete scenarios, no “AI” telltales.
- Structured JSON output (stored in `blog_posts.structured_content`) drives flexible rendering and components.
- Templates for multiple formats: Buying Guide, Review, Comparison, Tutorial, History, Deals/Value, Quiz, New Release, Artist Spotlight.
- Product integration: AI recommendations with context + guaranteed attachment of editor‑selected products.
- Draft preview: `/admin/blog/preview/{id}` renders full post (markdown + components) before publish.
- SEO: BlogPosting + FAQPage JSON‑LD, conditional `noindex`, internal linking, Related Posts.

Architecture
- Templates: DB‑backed (`blog_generation_templates`) with UI editor; seed script updates or inserts if new.
- AI Service: BlogAIGenerator builds prompts (with human style + schema), calls providers, validates JSON, saves posts.
- Content Structure: `structured_content.sections` with `section_type` powering components (pros/cons, specs, comparison).
- Tracking: Full generation history + batch jobs (Azure OpenAI batch supported).

Frontend (blog)
- Post page: markdown rendering (ReactMarkdown + GFM), sticky TOC, Pros/Cons, Specs, Comparison Table, Key Takeaways, FAQs, Related Posts, author box, newsletter CTA.
- Blog index: hero featured + two secondary; sticky category chips; Most Read + Popular Tags sidebar; paginated grid.
- Admin: BlogManager (filters, badges Draft/Published/noindex, bulk Publish/Draft/Archive/Noindex), AI Generator, AI Batch, Templates Manager (view/edit prompts and structure).

Key endpoints
- Public: `/blog/posts`, `/blog/posts/{slug}`, `/blog/categories`, `/blog/tags/popular`, `/blog/search`, `/blog/ai-posts/{id}` (rich AI details).
- Admin (protected):
  - Templates: `GET /admin/blog/templates`, `PUT /admin/blog/templates/{id}`
  - Generate: `POST /admin/blog/generate`, `POST /admin/blog/clone-rewrite`
  - Batch: `POST /admin/blog/batch/create`, `POST /admin/blog/batch/{batch_id}/upload`, `POST /admin/blog/batch/{file_id}/start`, `GET /admin/blog/batch/{azure_batch_id}/status`, `POST /admin/blog/batch/{azure_batch_id}/download`, `POST /admin/blog/batch/process`
  - Bulk ops: `POST /admin/blog/posts/publish-batch`, `POST /admin/blog/posts/status-batch` (draft/archive), `POST /admin/blog/posts/seo-batch` (noindex)

DB highlights
- `blog_posts`: enhanced with AI fields, `structured_content JSONB`, `noindex BOOLEAN`.
- `blog_post_products`: `ai_context`, `relevance_score`, `mentioned_in_sections`.
- `blog_content_sections`: section metadata (type/title/content/order), section‑level product references.
- `blog_generation_history`: prompt, model, tokens, timing, metadata.
- `blog_batch_jobs`, `blog_batch_processing_history`: Azure/OpenAI batch tracking, results import.

Rendering contract (selected section types)
- `pros_cons`: `{ pros: string[], cons: string[] }` → ProsCons component.
- `comparison_table`: `{ headers: string[], rows: string[][] }` → ComparisonTable.
- `specs`: `{ specs: [{ label, value }, ...] }` → SpecsList.
- Fallback: `{ content: markdown }` rendered via ReactMarkdown.
- Top-level extras: `best_features: string[]`, `faqs: [{ q, a }]`, `key_takeaways: markdown`.

Generation defaults and style
- Target 2000 words by default; prompt enforces deep sections (pros/cons, specs, who‑it’s‑for, tips/mistakes, comparison, key takeaways, FAQs).
- Human‑style guardrails: contractions, varied sentences, concrete claims, banned generic AI phrases, no hallucinated specs.

Admin UX
- Draft preview route for safe review.
- Templates Manager: edit prompts, structure, min/max products, tags/types.
- Batch Manager: build, upload, start, check status, download, process Azure/OpenAI batch jobs.

SEO
- JSON‑LD: BlogPosting + FAQPage; canonical + OG/Twitter; conditional `noindex` per post.
- Related Posts and Popular Tags improve internal linking.

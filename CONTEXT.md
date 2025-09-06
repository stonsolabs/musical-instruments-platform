GetYourMusicGear – Architecture & Context (Summary)
==================================================

Overview
--------

- Backend: FastAPI (Python, SQLAlchemy, PostgreSQL) in `backend/`
- Frontend: Next.js + TypeScript + Tailwind in `frontend/` (renamed from `frontend_v2`)
- Frontend calls backend via local proxy API: `/api/proxy/v1/...` (no direct Azure calls).

Frontend
--------

- Pages (SSR): `/`, `/products`, `/products/[slug]`, `/compare`, `/blog/*`, `/privacy`, `/terms`, `/contact`
- Components: layout (Header/Footer), product (Gallery/Info/Specifications/ContentSections/Voting), compare (CompareSearch/ComparisonTable), affiliate (AffiliateButtons), misc (BuyMeACoffeeButton, InstrumentRequestForm)
- Styling: Tailwind with tokens (`brand.*`, `store.thomann`, `store.gear4music`); CTAs standardized as `btn-primary` / `btn-secondary`.
- Affiliate buttons: vertical (`space-y-2`), label “View price at …”, placed on the right (product & compare summary), consistent branding via Tailwind tokens. Logo sizes: compact 28px, full 40px.
- Product & Compare views:
  - Product detail: no prices; shows votes (🤘/👎); content sections from `product.content` (Overview, Usage, Customer Feedback, Care, Why Choose This, Technical Analysis, Professional Assessment) as collapsibles; specs grouped by key prefix.
  - Listing images (Product grid), Trending images, and Blog product images: clicking an image opens the top-priority affiliate store (based on backend EnhancedAffiliateService + provided store_links), with fallback to Thomann URL or product detail. All explicit store links (e.g., in any “Where to Buy” list) also resolve via the affiliate service before opening.
  - Compare: Summary (dynamic columns; badges, quick facts per product, right-side affiliate buttons with preloaded affiliate stores), Specs Table (grouped rows, sticky feature column, difference badges), Q&A (per-product blocks). Prices are hidden.
- Autocomplete: Hero & CompareSearch; debounced; thumbnails when available; keyboard navigation (Up/Down/Enter/Esc).
- Nav highlighting: precise per category/sort.
- BuyMeACoffee: programmatic script injection component in Footer; Contact page linked from footer.

Frontend Data Access
-------------------

- Proxy API route: `frontend/pages/api/proxy/[...path].ts`
  - Target: `NEXT_PUBLIC_API_BASE_URL + '/api/' + path`
  - Adds `X-API-Key` (server env); forwards body; returns JSON/text.
- `src/lib/api.ts`:
  - `PROXY_BASE = '/api/proxy/v1'`
  - SSR-safe `apiFetch()` builds absolute URLs using `NEXT_PUBLIC_APP_ORIGIN` (or `VERCEL_URL`/`http://localhost:3000`).
- Endpoints used: `/products`, `/products/{id}`, `/search/autocomplete`, `/compare`, `/trending/instruments`, `/categories`, `/brands`, `/products/{id}/affiliate-stores`, `/instrument-requests`, `/voting/products/{id}/vote`, `/voting/products/{id}/stats`.
  - Voting: submit via `/api/proxy/v1/voting/products/{id}/vote` with `{ vote_type: 'up'|'down' }`; after submit, refetch `/api/proxy/v1/voting/products/{id}/stats` and update UI live.
  - `fetchProduct(slugOrId)`: tries `/products?slugs=<slug>`, then `/search/autocomplete` match, then `/products/{id}` if numeric.
  - `fetchProducts(...)` normalizes backend pagination into SearchResult: `{ products, total, page, per_page, total_pages }`.

Backend
-------

- API routers (prefix `/api/v1`): products, compare, trending, search, voting, affiliate_stores, instrument_requests, blog.
- Business logic:
  - EnhancedAffiliateService: brand exclusivity, regional prefs, affiliate URL construction (from content.store_links + fallbacks).
  - TrendingService: trending instruments and comparisons.
  - Vote utils: aggregates thumbs_up_count, thumbs_down_count, total_votes, vote_score.

Database (Key Tables)
---------------------

- brands: id, name (unique), slug (unique), logo_url, website_url, description, created_at
  - Unknown brand entries (`name='Unknown Brand'` or `slug='unknown-brand'`) are filtered out server-side and hidden from the Brand filter UI.
- categories: id, name, slug (unique), parent_id (self FK), description, image_url, is_active, created_at
- products: id, sku (unique), name, slug (unique), brand_id (FK), category_id (FK), description, images (JSON), content (JSON; narratives/specs/store_links/QA/localized), avg_rating, review_count, is_active, category_attributes (JSON), last_crawled, OpenAI fields, created_at, updated_at
- affiliate_stores: id, name, slug (unique), website_url, logo_url, affiliate settings (has_affiliate_program, affiliate_id, parameters), regions, fallbacks, created_at, updated_at
- product_prices: id, product_id (FK), store_id (FK), price, currency, affiliate_url, is_available, last_checked, created_at, updated_at, unique(product_id, store_id)
- brand_exclusivities: brand_name + store_id exclusivity
- comparison_views: id, product_ids (ARRAY[int]), user_ip, user_country, created_at
- affiliate_clicks: id, product_id, store_id, user_ip, user_country, referrer, created_at
- product_votes: id, product_id, user_ip, vote_type ('up'/'down'), created_at, updated_at, unique(product_id, user_ip)
- crawler tables: crawler_sessions, crawler_metrics, crawler_config, crawler_jobs; products_filled (crawler output)
- openai_batches: id, batch_id (unique), filename, product_count, status, openai_job_id, result_file

Environment
-----------

- Frontend (`frontend/.env.local`):
  - `NEXT_PUBLIC_API_BASE_URL=https://getyourmusicgear-api.azurewebsites.net`
  - `API_KEY=<your api key>` (used by proxy)
  - `NEXT_PUBLIC_APP_ORIGIN=https://getyourmusicgear.com` (or `http://localhost:3000` for dev SSR)
- Backend: see `backend/app/config.py`

Extending Safely
----------------

- Always use proxy for frontend HTTP calls
- Keep CTAs to `btn-primary` / `btn-secondary`
- Keep affiliate buttons vertical/right-side
- Avoid prices in product/compare views
- Add store tokens to Tailwind for consistent branding
- Group specs by category; optionally add icons/tabs (Overview, Specs, Q&A)
 - Hide Price Range filter (backend price filtering removed); keep fields dormant until API support returns
 - Compare page: includes top header badges (e.g., “Professional Rating: coming soon”, “AI Summary & Specs”); per-product badges under titles when content exists

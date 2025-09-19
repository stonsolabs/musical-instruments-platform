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
- **NEW SIMPLIFIED BLOG SYSTEM (2025-09-19)**
  - ✅ **Complete System Overhaul**: Replaced complex 6+ table system with simple 2-table structure
  - ✅ **Guitar Center Inspired Design**: Modern, clean homepage with search, filtering, featured posts
  - ✅ **7 Template Types**: buying-guide, review, comparison, artist-spotlight, instrument-history, gear-tips, news-feature
  - ✅ **3000-5000 Word Articles**: High-quality, comprehensive content with natural affiliate integration
  - ✅ **GPT-4.1 Integration**: Latest model with 8000 max tokens to prevent truncation
  - ✅ **Simplified CLI**: Easy batch generation and processing with `simple_blog_cli.py`
- Blog Main Page
  - Added "Most Read" and "Popular Tags" sections for better internal linking and discovery.
- Technical SEO
  - Canonicals, OG/Twitter, robots, JSON‑LD (BlogPosting/Product/BreadcrumbList/WebSite SearchAction).

Frontend
--------

- Pages (SSR): `/`, `/products`, `/products/[slug]`, `/compare`, `/blog/*`, `/privacy`, `/terms`, `/contact`
- Components: layout (Header/Footer), product (Gallery/Info/Specifications/ContentSections/Voting), compare (CompareSearch/ComparisonTable), affiliate (AffiliateButtons), blog (SimpleBlogRenderer/SimpleBlogHomepage), misc (InstrumentRequestForm)
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
- Endpoints used: `/products`, `/products/{id}`, `/search/autocomplete`, `/compare`, `/trending/instruments`, `/categories`, `/brands`, `/products/{id}/affiliate-urls` (GET) and `/products/{id}/affiliate-stores` (POST with links), `/instrument-requests`, `/voting/products/{id}/vote`, `/voting/products/{id}/stats`, `/blog/*` (simplified endpoints).
  - Voting: submit via `/api/proxy/v1/voting/products/{id}/vote` with `{ vote_type: 'up'|'down' }`; after submit, refetch `/api/proxy/v1/voting/products/{id}/stats` and update UI live.
  - `fetchProduct(slugOrId)`: tries `/products?slugs=<slug>`, then `/search/autocomplete` match, then `/products/{id}` if numeric.
  - `fetchProducts(...)` normalizes backend pagination into SearchResult: `{ products, total, page, per_page, total_pages }`.

Backend
-------

- API routers (prefix `/api/v1`): products, compare, trending, search, voting, affiliate_stores, instrument_requests, blog (simplified), admin (protected), docs (protected).
- Business logic:
  - EnhancedAffiliateService: 
    * Brand exclusivity rules: If a brand has an exclusive relationship with a store, only that store is shown for products of that brand
    * Regional preferences: Stores can have different priority scores based on user region
    * Priority scoring: Combines store priority, regional boosts, brand exclusivity boosts, and store link availability
    * Affiliate URL generation: Automatically adds affiliate parameters and handles domain-specific affiliate IDs
    * Store filtering: Only shows active stores with affiliate programs and visible buttons
  - TrendingService: trending instruments and comparisons (views + comparisons + votes).
  - Vote utils: aggregates thumbs_up_count, thumbs_down_count, total_votes, vote_score.
  - Content enrichment: Backend returns all rich content fields (qa, setup_tips, audience_fit, professional_ratings, etc.) via get_clean_content() function
  - SimpleBlogGenerator: Simplified AI-powered blog generation with GPT-4.1, 7 template types, natural affiliate integration

Database (Key Tables)
---------------------

- brands: id, name (unique), slug (unique), logo_url, website_url, description, created_at
  - Unknown brand entries (`name='Unknown Brand'` or `slug='unknown-brand'`) are filtered out server-side and hidden from the Brand filter UI.
- categories: id, name, slug (unique), parent_id (self FK), description, image_url, is_active, created_at
- products: id, sku (unique), name, slug (unique), brand_id (FK), category_id (FK), description, images (JSON), content (JSON; English-only content with basic_info, technical_analysis, purchase_decision, etc.), avg_rating, review_count, is_active, category_attributes (JSON), last_crawled, OpenAI fields, created_at, updated_at
- affiliate_stores: id, name, slug (unique), website_url, logo_url, affiliate settings (has_affiliate_program, affiliate_id, affiliate_parameters, domain_affiliate_ids), priority, show_affiliate_buttons, regional settings (available_regions, regional_priority, primary_region), fallbacks, created_at, updated_at
- product_prices: id, product_id (FK), store_id (FK), price, currency, affiliate_url, is_available, last_checked, created_at, updated_at, unique(product_id, store_id)
- brand_exclusivities: id, brand_name, store_id (FK to affiliate_stores), is_exclusive (boolean), regions (JSON), priority_boost, created_at, updated_at
- comparison_views: id, product_ids (ARRAY[int]), user_ip, user_country, created_at
- affiliate_clicks: id, product_id, store_id, user_ip, user_country, referrer, created_at
- product_votes: id, product_id, user_ip, vote_type ('up'/'down'), created_at, updated_at, unique(product_id, user_ip)
- crawler tables: crawler_sessions, crawler_metrics, crawler_config, crawler_jobs; products_filled (crawler output)
- openai_batches: id, batch_id (unique), filename, product_count, status, openai_job_id, result_file

**SIMPLIFIED BLOG TABLES:**
- blog_posts: id, title, slug (unique), excerpt, content_json (JSONB - stores all content), seo_title, seo_description, author_name, status, published_at, created_at, updated_at
- blog_templates: id, name (unique), prompt, structure (JSONB), created_at

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

SIMPLIFIED BLOG SYSTEM (2025-09-19)
===================================

The platform now features a completely redesigned, simplified blog system that replaces the previous complex structure with a clean, maintainable solution.

## ✅ Key Improvements

**Database Simplification:**
- Reduced from 6+ complex tables to just 2 simple tables
- Single JSONB column (`content_json`) stores all blog content
- Eliminated unnecessary complexity while maintaining functionality

**Template Types (7 Available):**
1. **buying-guide** - Product recommendations & comparisons (25% distribution)
2. **review** - In-depth product reviews (20% distribution)  
3. **comparison** - Side-by-side analysis (15% distribution)
4. **instrument-history** - Evolution stories (Gibson SG, Telecaster) (15% distribution)
5. **artist-spotlight** - Celebrating musicians (Ozzy, Hendrix) (15% distribution)
6. **gear-tips** - Practical advice & maintenance (7% distribution)
7. **news-feature** - Industry news & updates (3% distribution)

**Content Quality:**
- 3000-5000 words per article (comprehensive, in-depth content)
- GPT-4.1 integration with 8000 max tokens (no truncation)
- Natural affiliate product integration throughout content
- Evergreen content (no specific years unless essential)

**Guitar Center Inspired Design:**
- Modern homepage with hero search section
- Category filtering and featured posts grid
- Clean, professional layout optimized for user engagement
- Newsletter signup and modern UI components

## 🛠️ Technical Architecture

**Backend Services:**
- `SimpleBlogGenerator`: Core generation logic with template support
- `SimpleBlogBatchGenerator`: Bulk generation for OpenAI Batch API
- `SimpleBlogBatchProcessor`: Processes batch results and saves to database

**Frontend Components:**
- `SimpleBlogRenderer`: Clean, efficient content rendering
- `SimpleBlogHomepage`: Guitar Center inspired homepage layout
- Support for all section types (intro, product_spotlight, content, conclusion)

**Generation Options:**
- **CLI Tool**: `backend/app/scripts/blog/simple_blog_cli.py`
- **UI Components**: `BlogBatchGenerator.tsx`, `BlogAIGenerator.tsx`, `BlogBatchManager.tsx`
- Generate batches: `python simple_blog_cli.py generate --posts 100`
- Process results: `python simple_blog_cli.py process --file results.jsonl`
- View stats: `python simple_blog_cli.py stats`

**Smart Product Integration:**
- **Database Selection**: Only loads active products with store availability
- **Keyword Matching**: Enhanced system matches products to topics (rock→guitars, recording→microphones)
- **Template-Specific Fallbacks**: Artist posts show iconic instruments, history shows classic gear
- **Non-Product Topics**: For posts like "History of Blues" or "Music Theory", system intelligently selects relevant products (blues guitars, educational keyboards)
- **Always Shows Products**: Even purely educational content includes "Recommended Instruments" sections

## 📋 Usage Commands

**Generate Blog Batch:**
```bash
cd backend/app/scripts/blog
python simple_blog_cli.py generate --posts 100 --template-distribution '{"buying-guide": 0.28, "review": 0.25, "comparison": 0.18, "instrument-history": 0.15, "gear-tips": 0.09, "artist-spotlight": 0.04, "news-feature": 0.01}'
```

**Process OpenAI Results:**
```bash
python simple_blog_cli.py process --file batch_results.jsonl
```

**View System Statistics:**
```bash
python simple_blog_cli.py stats
```

**Custom Distribution Example:**
```bash
python simple_blog_cli.py generate --posts 50 --min-words 3500 --max-words 4500 --template-distribution '{"artist-spotlight": 0.4, "instrument-history": 0.3, "buying-guide": 0.2, "review": 0.1}'
```

## 🗂️ File Structure

```
backend/app/
├── services/
│   ├── simple_blog_generator.py (NEW)
│   ├── simple_blog_batch_generator.py (NEW)
│   └── simple_blog_batch_processor.py (NEW)
├── scripts/blog/
│   ├── simple_blog_cli.py (CLI tool)
│   └── simplify_blog_system.sql (migration script)
└── alembic/versions/
    └── 012_simplify_blog_system.py (database migration)

frontend/src/components/
├── SimpleBlogRenderer.tsx (NEW - replaces EnhancedBlogRenderer)
└── SimpleBlogHomepage.tsx (NEW - Guitar Center inspired)

docs/
├── SIMPLIFIED_BLOG_JSON_FORMAT.md (NEW - documentation)
└── SIMPLIFIED_BLOG_SYSTEM.md (NEW - complete guide)
```

## 📊 JSON Structure

The simplified system uses a clean JSON structure stored in `blog_posts.content_json`:

```json
{
  "title": "Best Acoustic Guitars Under $500",
  "excerpt": "Discover top-quality acoustic guitars...",
  "seo_title": "Best Affordable Acoustic Guitars - Expert Reviews",
  "seo_description": "Find the perfect acoustic guitar under $500...",
  "sections": [
    {
      "type": "intro",
      "content": "Finding a great acoustic guitar on a budget..."
    },
    {
      "type": "product_spotlight",
      "product": {
        "id": "12345",
        "name": "Yamaha FG830",
        "price": "$299",
        "rating": 4.5,
        "pros": ["Great tone", "Solid construction"],
        "cons": ["Basic tuning pegs"],
        "affiliate_url": "https://..."
      }
    },
    {
      "type": "content", 
      "content": "## Detailed Analysis\n\nWhen evaluating..."
    },
    {
      "type": "conclusion",
      "content": "## Final Thoughts\n\nChoosing the right..."
    }
  ],
  "tags": ["acoustic-guitars", "budget", "beginner"],
  "category": "buying-guide",
  "featured_products": ["12345", "67890"]
}
```

## 🎯 Benefits

1. **90% Complexity Reduction**: From 6+ tables to 2 simple tables
2. **Better Performance**: Single JSON parse, no complex database joins
3. **Easier Maintenance**: Simple structure, clear code organization  
4. **Natural Affiliate Integration**: Products seamlessly integrated in content flow
5. **Modern Design**: Guitar Center inspired, mobile-responsive interface
6. **Flexible Content**: Easy to add new section types and templates
7. **Quality Content**: 3000-5000 word comprehensive articles
8. **SEO Optimized**: Evergreen content with proper meta tags and structure

The simplified blog system is now production-ready and generates high-quality, engaging content perfect for affiliate monetization while maintaining an excellent user experience.
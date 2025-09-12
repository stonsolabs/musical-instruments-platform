GetYourMusicGear – Architecture & Context (Summary)
==================================================

Overview
--------

- Backend: FastAPI (Python, SQLAlchemy, PostgreSQL) in `backend/`
- Frontend: Next.js + TypeScript + Tailwind in `frontend/`
- Frontend calls backend via local proxy API: `/api/proxy/v1/...` (no direct Azure calls).

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
- Endpoints used: `/products`, `/products/{id}`, `/search/autocomplete`, `/compare`, `/trending/instruments`, `/categories`, `/brands`, `/products/{id}/affiliate-stores`, `/instrument-requests`, `/voting/products/{id}/vote`, `/voting/products/{id}/stats`, `/blog/*` (categories, posts, templates, generate, generation-history, ai-posts).
  - Voting: submit via `/api/proxy/v1/voting/products/{id}/vote` with `{ vote_type: 'up'|'down' }`; after submit, refetch `/api/proxy/v1/voting/products/{id}/stats` and update UI live.
  - `fetchProduct(slugOrId)`: tries `/products?slugs=<slug>`, then `/search/autocomplete` match, then `/products/{id}` if numeric.
  - `fetchProducts(...)` normalizes backend pagination into SearchResult: `{ products, total, page, per_page, total_pages }`.

Backend
-------

- API routers (prefix `/api/v1`): products, compare, trending, search, voting, affiliate_stores, instrument_requests, blog (with AI generation).
- Business logic:
  - EnhancedAffiliateService: 
    * Brand exclusivity rules: If a brand has an exclusive store relationship, only that store is shown for products of that brand
    * Regional preferences: Stores can have different priority scores based on user region
    * Priority scoring: Combines store priority, regional boosts, brand exclusivity boosts, and store link availability
    * Affiliate URL generation: Automatically adds affiliate parameters and handles domain-specific affiliate IDs
    * Store filtering: Only shows active stores with affiliate programs and visible buttons
  - TrendingService: trending instruments and comparisons.
  - Vote utils: aggregates thumbs_up_count, thumbs_down_count, total_votes, vote_score.
  - Content enrichment: Backend returns all rich content fields (qa, setup_tips, audience_fit, professional_ratings, etc.) via get_clean_content() function
  - BlogAIGenerator: AI-powered blog generation service with OpenAI integration, specialized prompt templates, smart product selection, and comprehensive generation tracking

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

The platform features an advanced AI-powered blog system for generating engaging, SEO-optimized content:

**Core Features**:
- AI-generated blog posts using OpenAI GPT models with specialized prompts
- Smart product integration based on relevance scoring and context analysis
- Multiple content templates: Buying Guides, Product Reviews, Comparisons, Tutorials, Historical Articles
- Structured content sections with AI-generated product recommendations
- SEO optimization with auto-generated titles, descriptions, and meta tags
- Generation history tracking with performance metrics

**Architecture**:
- **Templates**: Pre-built prompt templates for different blog types with customizable parameters
- **AI Service**: BlogAIGenerator handles OpenAI API integration, prompt building, and response parsing
- **Product Association**: Smart product selection based on categories, ratings, and relevance scores
- **Content Sections**: Structured content with sections that can reference specific products
- **Generation Tracking**: Complete audit trail of AI generations with token usage and performance metrics

**Frontend Components**:
- `BlogAIGenerator`: Full-featured AI generation interface with template selection and customization
- `BlogManager`: Admin dashboard for managing posts and viewing generation history
- `BlogPostEditor`: Manual blog creation with product integration
- Enhanced `BlogPostCard` and `BlogProductShowcase` for displaying AI-generated content

**API Endpoints**:
- `/blog/templates` - Manage generation templates
- `/blog/generate` - Trigger AI blog generation
- `/blog/generation-history` - View generation audit trail
- `/blog/ai-posts/{id}` - Fetch AI-generated posts with enhanced metadata

**Database Schema**:
The blog system uses 9 specialized tables to support AI generation, content structure, product associations, and generation tracking. Key features include AI context fields, relevance scoring, section-based content organization, and comprehensive generation history.

**Azure Batch API Integration**:
- **Batch Processing**: Efficient bulk blog generation using Azure OpenAI Batch API with 50% cost savings
- **Azure Storage**: Automatic file management with batch request/response storage in Azure Blob Storage
- **Workflow Management**: Complete batch lifecycle tracking from creation to post publication
- **Admin Dashboard**: Secure admin-only access via Azure App Service Authentication
- **Environment Configuration**: Comprehensive environment variable setup for Azure services

**Batch System Tables**:
- `blog_batch_jobs`: Tracks batch creation, Azure job status, file paths, and completion metrics
- `blog_batch_processing_history`: Records batch processing results with success/failure analytics

**Admin Security**:
- Azure App Service Authentication with Azure AD integration
- Admin-only routes protected by email verification
- Comprehensive logging and audit trails
- Environment-based admin access control

**Protected Documentation**:
- `/docs` frontend page with Azure AD authentication
- `/api/v1/docs/` backend endpoints (Swagger UI, ReDoc, OpenAPI schema)
- Admin-only access with same authentication as admin panel
- Interactive API testing with full endpoint coverage
- Complete schema documentation including security schemes and rate limits

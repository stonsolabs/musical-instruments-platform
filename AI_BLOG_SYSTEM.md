# AI Blog System - Technical Documentation

## Overview

The GetYourMusicGear platform features an advanced AI-powered blog system that generates high-quality, SEO-optimized content about musical instruments and gear. The system integrates products from the catalog, produces structured content, supports a secure admin workflow, and maintains comprehensive generation tracking. It also includes a Clone & Rewrite tool and optional Azure OpenAI Batch processing for scale.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────────┐
│   Frontend      │    │    Backend       │    │   AI Providers         │
│                 │    │                  │    │                        │
│ BlogManager     │◄──►│ BlogAIGenerator  │◄──►│ OpenAI / Azure OpenAI  │
│ BlogAIGenerator │    │ BlogBatchGenerator│   │ (Batch optional)       │
│ BlogPostEditor  │    │ Prompt Templates │    │                        │
└─────────────────┘    └──────────────────┘    └────────────────────────┘
          │                       │
          │                       │
          ▼                       ▼
┌─────────────────────────────────────────────────────────┐
│                Database Schema                          │
│                                                         │
│ • blog_generation_templates (prompt templates)         │
│ • blog_posts (enhanced with AI fields)                 │
│ • blog_post_products (with AI context & relevance)     │
│ • blog_content_sections (structured content)           │
│ • blog_generation_history (audit trail)                │
│ • blog_batch_jobs + blog_batch_processing_history      │
└─────────────────────────────────────────────────────────┘
```

## Security & Access

- Admin-only generation endpoints are protected. Two auth modes exist:
  - Azure App Service Authentication (production): endpoints in `backend/app/api/v1/admin.py` use `require_azure_admin`.
  - Admin API key (dev/local or generic admin mode): endpoints in `backend/app/api/v1/blog.py` use `require_admin` and accept `X-Admin-Key`.
- Frontend admin UI stores a short-lived token in `sessionStorage` and calls the admin endpoints.

See `ADMIN_SETUP.md` and `AZURE_APP_SERVICE_SETUP.md` for environment-specific configuration.

## Core Components

### 1. Blog Generation Templates

Pre-built prompt templates for different content types:

- **Buying Guide**: Comprehensive purchase advice with price ranges and recommendations
- **Product Review**: In-depth analysis with pros/cons and value assessment
- **Product Comparison**: Head-to-head analysis of multiple instruments
- **Tutorial**: Educational content with step-by-step instructions
- **Historical Article**: Cultural and technical evolution of instruments

**Database**: `blog_generation_templates`
```sql
CREATE TABLE blog_generation_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    template_type VARCHAR(50) CHECK (template_type IN ('general', 'buying_guide', 'review', 'comparison', 'tutorial', 'history')),
    base_prompt TEXT NOT NULL,
    system_prompt TEXT,
    product_context_prompt TEXT,
    required_product_types JSONB, -- ["guitars", "keyboards", etc.]
    min_products INTEGER DEFAULT 0,
    max_products INTEGER DEFAULT 10,
    suggested_tags JSONB, -- ["buying-guide", "beginner", etc.]
    seo_title_template VARCHAR(255),
    seo_description_template TEXT,
    content_structure JSONB, -- {"sections": [...]}
    is_active BOOLEAN DEFAULT TRUE
);
```

### 2. AI Generation Service

**File**: `backend/app/services/blog_ai_generator.py`

Core functionality:
- OpenAI API integration with error handling
- Smart product selection based on categories and ratings
- Prompt building with dynamic variable substitution
- Response parsing and validation
- Database record creation with full audit trail

**Key Methods**:
- `generate_blog_post()` - Main generation orchestration
- `_select_relevant_products()` - Intelligent product selection
- `_build_generation_prompt()` - Dynamic prompt construction
- `_call_ai_generation()` - OpenAI API interaction
- `_parse_ai_response()` - JSON parsing and validation

Also available:
- `clone_and_rewrite()` - Fetch a source article, extract content, then rewrite with AI and optional product integration.

### 3. Specialized Prompt Templates

**File**: `backend/app/services/blog_prompt_templates.py`

Each template includes:
- **System Prompt**: 20+ years music gear expertise persona
- **Base Prompt**: Template-specific instructions with variables
- **Product Context**: How to integrate products meaningfully
- **Content Structure**: Expected sections and organization
- **SEO Templates**: Title and description patterns

**Example - Buying Guide Template**:
```python
{
    "base_prompt": """Write a comprehensive buying guide for {category} instruments. 
    Structure with: Introduction, Key Considerations, Budget Breakdown, 
    Top Recommendations, Advanced Features, Maintenance, Conclusion...""",
    
    "product_context_prompt": """For each product, explain why it's recommended, 
    key features, who it's best for, how it compares to alternatives...""",
    
    "content_structure": {
        "sections": ["introduction", "key_considerations", "budget_breakdown", ...]
    }
}
```

### 4. Enhanced Product Association

Products are intelligently selected and associated with AI context:

**Database**: `blog_post_products` (enhanced)
```sql
ALTER TABLE blog_post_products ADD COLUMN ai_context TEXT;
ALTER TABLE blog_post_products ADD COLUMN relevance_score DECIMAL(3,2);
ALTER TABLE blog_post_products ADD COLUMN mentioned_in_sections JSONB;
```

**AI Context Examples**:
- "Recommended for beginners due to easy playability and affordable price point"
- "Featured as professional-grade alternative with superior build quality"
- "Included for comparison showing different tonal characteristics"

**Relevance Scoring**: 0.00-1.00 based on:
- Category match
- Price range fit
- Feature alignment
- Rating/review quality

### 5. Structured Content Sections

**Database**: `blog_content_sections`
```sql
CREATE TABLE blog_content_sections (
    id SERIAL PRIMARY KEY,
    blog_post_id INTEGER REFERENCES blog_posts(id),
    section_type VARCHAR(100), -- 'introduction', 'buying_guide', etc.
    section_title VARCHAR(255),
    section_content TEXT NOT NULL,
    section_order INTEGER DEFAULT 0,
    products_featured JSONB, -- Array of product IDs in this section
    ai_generated BOOLEAN DEFAULT FALSE
);
```

Enables:
- Granular content organization
- Section-specific product recommendations
- Targeted content updates
- Analytics on section performance

### 6. Generation History & Audit Trail

**Database**: `blog_generation_history`
```sql
CREATE TABLE blog_generation_history (
    id SERIAL PRIMARY KEY,
    blog_post_id INTEGER REFERENCES blog_posts(id),
    template_id INTEGER REFERENCES blog_generation_templates(id),
    generation_status VARCHAR(50), -- 'pending', 'generating', 'completed', 'failed'
    prompt_used TEXT,
    model_used VARCHAR(100),
    tokens_used INTEGER,
    generation_time_ms INTEGER,
    error_message TEXT,
    generation_metadata JSONB
);
```

Tracks:
- Complete prompt used for generation
- Model version and parameters
- Token consumption and costs
- Generation time and performance
- Success/failure rates
- Error details for debugging

## Frontend Components

### 1. BlogAIGenerator Component

**File**: `frontend/src/components/BlogAIGenerator.tsx`

Features:
- Template selection with visual previews
- Product search and selection interface
- Custom prompt additions
- Advanced AI parameters (temperature, model selection)
- Real-time generation progress
- Result preview and success feedback

**UI Flow**:
1. Select generation template
2. Choose featured products (with min/max validation)
3. Set target word count and customizations
4. Configure AI parameters
5. Generate and track progress
6. Preview results

### 2. BlogManager Dashboard

**File**: `frontend/src/components/BlogManager.tsx`

Admin interface featuring:
- **Statistics**: Total posts, published count, AI-generated count, total views
- **Dual Tabs**: Blog posts grid + Generation history timeline
- **Quick Actions**: Launch AI generator or manual editor
- **Generation History**: Status tracking, error details, prompt viewing

### 3. Enhanced BlogPostEditor

**File**: `frontend/src/components/BlogPostEditor.tsx` (existing, enhanced)

Supports both manual and AI-assisted creation:
- Product search and association
- Tag management
- SEO optimization fields
- Preview mode
- Draft/publish workflow

## API Endpoints

The platform exposes read endpoints for all users and protected admin endpoints for generation and management. Both variants exist to support different deployments.

### Public Read Endpoints
- `GET /blog/categories` - List blog categories
- `GET /blog/posts` - List blog posts (with filtering)
- `GET /blog/posts/{slug}` - Get single blog post
- `GET /blog/search` - Search blog posts
- `GET /blog/ai-posts/{id}` - Fetch AI post with enhanced metadata

### Admin Endpoints (Admin key mode)
- `GET /blog/templates` - List generation templates
- `POST /blog/templates` - Create new template
- `POST /blog/generate` - Generate blog post with AI
- `GET /blog/generation-history` - View generation audit trail

Authentication: send `X-Admin-Key` header. See ADMIN_SETUP.md.

### Admin Endpoints (Azure App Service auth)
- `GET /admin/blog/templates`
- `POST /admin/blog/generate`
- `POST /admin/blog/clone-rewrite`
- `GET /admin/blog/generation-history`
- Batch generation flow:
  - `POST /admin/blog/batch/create`
  - `POST /admin/blog/batch/{batch_id}/upload`
  - `POST /admin/blog/batch/{file_id}/start`
  - `GET  /admin/blog/batch/{azure_batch_id}/status`
  - `POST /admin/blog/batch/{azure_batch_id}/download`
  - `POST /admin/blog/batch/process`
  - `GET  /admin/blog/batches`

Authentication: Azure App Service injected headers; see AZURE_APP_SERVICE_AUTH.md.

## Installation & Setup

### 1. Database Migration

Run the enhancement script:
```bash
cd backend
python scripts/migrations/enhance_blog_for_ai.py
```

### 2. Environment Configuration

Minimum for OpenAI:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

Optional Azure OpenAI (for provider=azure_openai and/or Batch):
```env
# Core
AZURE_OPENAI_ENDPOINT=https://<resource-name>.openai.azure.com
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_API_VERSION=2024-07-01-preview
AZURE_OPENAI_DEPLOYMENT=<chat-model-deployment>
AZURE_OPENAI_DEPLOYMENT_NAME=<chat-model-deployment>

# Azure Storage for Batch (optional, recommended)
AZURE_STORAGE_CONNECTION_STRING=...
# or
AZURE_STORAGE_ACCOUNT_NAME=...
AZURE_STORAGE_ACCOUNT_KEY=...
AZURE_STORAGE_CONTAINER=blog-batch-files
```

Admin auth:
```env
# For admin key mode
ADMIN_API_KEY=your-super-secret-admin-key
# For Azure App Service admin mode
ADMIN_EMAIL=admin@getyourmusicgear.com
```

### 3. Install Dependencies

Backend includes the OpenAI SDK and Azure dependencies in `requirements.txt`. Ensure your environment has them installed via your normal setup flow.

### 4. Template Setup

- Run the migration script above to create the schema.
- Optionally seed additional templates oriented for affiliate conversions:

```bash
# from repo root
ENVIRONMENT=production python -m backend.scripts.data.seed_blog_generation_templates
```

This upserts several practical templates such as Roundups, Deals, Quiz, New Release, and Artist Spotlight.

## Usage Examples

### Generate a Buying Guide

```typescript
// Admin-key mode (frontend proxy) example
const request: BlogGenerationRequest = {
  template_id: 1, // Buying Guide template
  category_id: 5, // Electric Guitars
  product_ids: [123, 456, 789], // Featured products
  target_word_count: 1200,
  include_seo_optimization: true,
  auto_publish: false,
  generation_params: {
    model: 'gpt-4o',
    temperature: 0.7
  }
};

const result = await fetch('/api/proxy/v1/blog/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(request)
});
```

Admin endpoints with Azure auth (direct):
```bash
curl -X POST "https://<api>/api/v1/admin/blog/generate" \
  -H "Content-Type: application/json" \
  -d '{
        "template_id": 1,
        "category_id": 5,
        "product_ids": [123,456,789],
        "target_word_count": 1200,
        "generation_params": {"model": "gpt-4o", "temperature": 0.7},
        "provider": "openai"
      }'
```

### Create Custom Template

```sql
INSERT INTO blog_generation_templates (
  name, template_type, base_prompt, min_products, max_products
) VALUES (
  'Maintenance Guide',
  'tutorial',
  'Write a comprehensive maintenance guide for {category} instruments...',
  2, 5
);
```

## AI Prompting Strategy

### System Prompt (Expert Persona)
```
You are an expert music gear writer with 20+ years of experience.
You have extensive knowledge of:
- Musical instruments across all categories
- Music gear technology and specifications
- Sound engineering and production
- Brand histories and market positioning
- Price points and value propositions

Your writing is informative, engaging, honest, and SEO-conscious.
```

### Dynamic Prompt Building
Variables are substituted based on context:
- `{category}` - Instrument category
- `{product_name}` - Specific product being reviewed
- `{word_count}` - Target length
- `{skill_level}` - Target audience level

### Product Integration
Products are described with:
- Technical specifications
- Sound characteristics
- Build quality assessment
- Target audience fit
- Value proposition
- Competitive positioning

## Performance & Monitoring

### Token Usage Tracking
- Average tokens per post type
- Cost analysis per generation
- Optimization opportunities

### Generation Success Rates
- Template-specific success metrics
- Common failure modes
- Error categorization

### Content Quality Metrics
- Reading time accuracy
- SEO score tracking
- User engagement correlation

## Future Enhancements

### Planned Features
1. **Multi-language Support**: Generate content in different languages
2. **A/B Testing**: Generate multiple variants for testing
3. **Content Updates**: AI-powered content refreshing
4. **Image Integration**: AI-generated featured images
5. **Social Media**: Auto-generate social posts
6. **Analytics Integration**: Track performance metrics

### Scaling Considerations
1. **Batch Generation**: Process multiple posts simultaneously
2. **Caching Layer**: Cache common prompt patterns
3. **Rate Limiting**: Manage OpenAI API usage
4. **Content Moderation**: Automated quality checks

## Security & Best Practices

### API Security
- API key validation for generation endpoints
- Rate limiting on AI generation requests
- Input sanitization for custom prompts

### Content Safety
- OpenAI moderation checks
- Blacklist filtering for inappropriate content
- Manual review workflow for sensitive topics

### Cost Management
- Token usage monitoring and alerts
- Generation quotas per user/time period
- Model selection based on complexity needs

## Clone & Rewrite

Endpoint: `POST /admin/blog/clone-rewrite` (Azure admin). Admin-key mode does not include this route by default.

Payload fields:
- `source_url` (string, required) — URL to fetch and rewrite
- `title` (optional) — Override generated title
- `category_id` (optional)
- `product_ids` (optional list[int]) — Products to integrate
- `custom_instructions` (optional)
- `target_word_count` (int)
- `include_seo_optimization` (bool)
- `auto_publish` (bool)
- `generation_params` (object)
- `provider` — `openai` | `azure_openai`

Notes:
- Fetching uses `aiohttp`; extraction uses `BeautifulSoup` with a simple heuristic (`article/main/body`).
- The output goes through the same JSON parse/validation and DB persistence paths as standard generation.

## Azure Batch Generation (optional)

Use when generating many posts at once. Flow:
- Build a `.jsonl` with chat completions requests using your templates and products
- Upload to Azure OpenAI Files API
- Start Batch job, poll status, download results, and process into posts

Key endpoints: see Admin Endpoints (Azure) above.

Environment variables: see Installation step 2 for Azure and Storage settings.

Outputs:
- Batch job records in `blog_batch_jobs`
- Result processing summary in `blog_batch_processing_history`

## Providers & Models

Supported provider enum: `openai`, `azure_openai`, `anthropic`, `perplexity`.
- Current implementation focuses on OpenAI and Azure OpenAI. Other providers may require additional wiring.
- Models: defaults to `gpt-4o` with JSON response formatting. You can override in `generation_params.model`.

## Troubleshooting

- JSON parse errors: generator falls back to a lenient parser and will still save a draft; check `generation_history.error_message`.
- Missing templates: ensure migrations ran and/or run the seed script.
- Auth failures: for admin-key mode, verify `X-Admin-Key`; for Azure mode, verify authenticated admin email matches `ADMIN_EMAIL`.

This AI blog system provides a robust foundation for generating high-quality, engaging content that drives traffic and showcases your musical instrument expertise while maintaining full control, security, and tracking capabilities.

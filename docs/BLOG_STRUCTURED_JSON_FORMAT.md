# Blog Structured JSON Format (moved to docs/)

This document outlines the enhanced JSON structure for blog content generation that provides better control over sections, headers, and content organization.

## Overview

Instead of generating raw HTML/Markdown, the AI now generates structured JSON that clearly separates:
- **Metadata** (title, SEO, reading time)
- **Content sections** (with types, titles, and HTML content)
- **Product integration** (specific product placements and context)
- **Structured elements** (FAQs, comparisons, etc.)

## JSON Structure

```json
{
  "title": "Main blog post title",
  "excerpt": "Brief 1-2 sentence summary for previews",
  "seo_title": "SEO-optimized title (60 chars max)",
  "seo_description": "SEO meta description (155 chars max)", 
  "featured_image_alt": "Alt text for featured image",
  "reading_time": 8,
  "sections": [
    {
      "type": "introduction",
      "title": "Getting Started with Studio Monitors",
      "content": "<p>When building your first home studio...</p>",
      "products_mentioned": [1, 2, 3]
    },
    {
      "type": "comparison_table",
      "title": "Quick Comparison", 
      "content": "<table class='comparison-table'>...</table>",
      "products_mentioned": [1, 2, 3, 4]
    },
    {
      "type": "product_showcase",
      "title": "Top Picks",
      "content": "<p>After extensive testing, these are our top recommendations...</p>",
      "products": [
        {
          "product_id": 1,
          "context": "Best overall choice for beginners due to balanced sound and affordable price",
          "position": 1
        },
        {
          "product_id": 2, 
          "context": "Premium option with exceptional build quality and professional features",
          "position": 2
        }
      ]
    },
    {
      "type": "buying_guide",
      "title": "What to Look For",
      "content": "<h3>Key Specifications</h3><p>When choosing studio monitors...</p>"
    },
    {
      "type": "faqs",
      "title": "Frequently Asked Questions",
      "content": "<div class='faq-section'>...</div>",
      "faqs": [
        {
          "question": "What size monitors do I need for a small room?",
          "answer": "For rooms under 10x12 feet, 5-inch monitors are typically ideal..."
        },
        {
          "question": "Do I need a subwoofer with studio monitors?",
          "answer": "It depends on your room size and the type of music you're producing..."
        }
      ]
    },
    {
      "type": "conclusion",
      "title": "Final Thoughts",
      "content": "<p>Choosing the right studio monitors is crucial...</p>"
    }
  ],
  "tags": ["studio_monitors", "home_studio", "audio_equipment", "buying_guide"],
  "meta": {
    "content_type": "buying_guide",
    "expertise_level": "beginner",
    "target_audience": ["home_studio_owners", "music_producers", "podcasters"],
    "key_benefits": ["save_money", "avoid_mistakes", "professional_results"],
    "estimated_read_time": 8
  }
}
```

## Section Types

### Core Content Sections

| Type | Purpose | Required Fields |
|------|---------|-----------------|
| `introduction` | Hook readers and set context | `content` |
| `comparison_table` | Quick product comparison | `content`, `products_mentioned` |
| `product_showcase` | Detailed product features | `content`, `products[]` |
| `buying_guide` | Educational content | `content` |
| `pros_cons` | Product advantages/disadvantages | `content` |
| `use_cases` | Scenario-based recommendations | `content` |
| `faqs` | Common questions | `content`, `faqs[]` |
| `conclusion` | Summary and final thoughts | `content` |

### Specialized Sections

| Type | Purpose | Use Case |
|------|---------|----------|
| `build_analysis` | Construction quality review | Product reviews |
| `performance_testing` | Technical performance | Reviews, comparisons |
| `competitive_comparison` | vs. other products | Reviews, roundups |
| `budget_guide` | Price range recommendations | Buying guides |
| `shopping_tips` | Where/how to buy | Educational content |
| `common_mistakes` | What to avoid | Guides, tutorials |

## Product Integration

### Product References
Products can be referenced in two ways:

1. **Mentioned in content** (`products_mentioned`): Simple array of product IDs referenced in the section
2. **Featured products** (`products`): Detailed objects with context and positioning

### Product Context
Each featured product includes:
- `product_id`: Database ID of the product
- `context`: Why this product is recommended (replaces AI context)
- `position`: Display order (1 = first, 2 = second, etc.)

## Benefits of This Structure

### 1. **Better Content Organization**
- Clear section hierarchy
- Consistent content types
- Easy to reorder/modify sections

### 2. **Enhanced Product Integration** 
- Specific product placement control
- Context for each recommendation
- Clear product-to-content mapping

### 3. **Improved SEO Control**
- Separate SEO title/description
- Structured content for featured snippets
- Better internal linking opportunities

### 4. **Frontend Flexibility**
- Render sections with custom components
- Different layouts per section type
- Progressive enhancement possible

### 5. **Content Management**
- Easy editing of individual sections
- A/B testing different section orders
- Template reusability

## Implementation Notes

### Backend Processing
1. **Template System**: Enhanced prompts generate structured JSON
2. **Validation**: JSON schema validation ensures correct format
3. **Storage**: Sections stored as structured data in database
4. **API**: Endpoints serve structured content to frontend

### Frontend Rendering
1. **Section Components**: React components for each section type
2. **Product Integration**: Automatic product card insertion
3. **SEO**: Meta tags from structured data
4. **Performance**: Lazy loading of product details

### Content Quality
1. **Consistency**: Standardized section types ensure uniform quality
2. **Completeness**: Required sections prevent missing content
3. **Context**: Product context ensures relevant recommendations
4. **SEO**: Structured format optimizes for search engines

## Migration Strategy

### Phase 1: Template Updates
- Update existing templates with new JSON format
- Test generation with structured prompts
- Validate JSON output quality

### Phase 2: Frontend Components  
- Create section-specific React components
- Implement product showcase widgets
- Add FAQ structured data

### Phase 3: Content Migration
- Convert existing posts to structured format
- Update APIs to serve structured content
- Implement editing interface for structured content

### Phase 4: Optimization
- A/B test section orders
- Optimize conversion rates
- Enhance SEO performance

This structured approach provides much better control over content generation while maintaining natural, human-like output that doesn't reveal AI involvement.

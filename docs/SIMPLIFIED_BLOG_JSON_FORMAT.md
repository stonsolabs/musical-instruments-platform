# Simplified Blog JSON Format

## Overview
The new simplified blog system uses a single JSONB column `content_json` to store all blog content. This replaces the complex multi-table structure with a clean, simple format.

## JSON Structure

```json
{
  "title": "Best Acoustic Guitars Under $500",
  "excerpt": "Discover top-quality acoustic guitars that won't break the bank.",
  "seo_title": "Best Affordable Acoustic Guitars - Expert Reviews & Guide",
  "seo_description": "Find the perfect acoustic guitar under $500 with our expert reviews and buying guide.",
  
  "sections": [
    {
      "type": "intro",
      "content": "Finding a great acoustic guitar on a budget can be challenging..."
    },
    {
      "type": "quick_picks",
      "title": "Our Top Picks",
      "products": [
        {
          "id": "12345",
          "name": "Yamaha FG830",
          "price": "$299",
          "reason": "Best overall value with solid spruce top",
          "affiliate_url": "https://example.com/yamaha-fg830"
        }
      ]
    },
    {
      "type": "content",
      "content": "## What to Look For\n\nWhen shopping for an acoustic guitar..."
    },
    {
      "type": "product_spotlight",
      "product": {
        "id": "12346",
        "name": "Fender CD-60S",
        "price": "$199",
        "rating": 4.5,
        "pros": ["Great tone", "Comfortable neck"],
        "cons": ["Basic tuning pegs"],
        "affiliate_url": "https://example.com/fender-cd60s"
      }
    },
    {
      "type": "content",
      "content": "## Final Thoughts\n\nChoosing the right acoustic guitar..."
    }
  ],
  
  "tags": ["acoustic-guitars", "budget", "beginner"],
  "category": "buying-guide",
  "featured_products": ["12345", "12346"]
}
```

## Section Types

### Basic Sections
- `intro` - Introduction/hook
- `content` - Regular markdown content
- `conclusion` - Final thoughts

### Product Integration Sections
- `quick_picks` - Top recommendations grid
- `product_spotlight` - Detailed product review
- `comparison` - Product comparison table
- `affiliate_banner` - Call-to-action banner

### Interactive Sections  
- `pros_cons` - Pros and cons list
- `faq` - Frequently asked questions
- `tips` - Expert tips and advice

## Key Benefits

1. **Simple Structure** - Easy to understand and modify
2. **Flexible Content** - Mix text and products seamlessly  
3. **SEO Friendly** - Clean structure for search engines
4. **Affiliate Ready** - Built-in product integration
5. **Fast Rendering** - Single JSON parse, no complex joins

## Migration Notes

- Old `structured_content` renamed to `content_json`
- All complex tables removed
- Product relationships stored directly in JSON
- Categories and tags now in JSON instead of separate tables
# OpenAI Batch Generation Prompts - GetYourMusicGear.com

This document provides structured prompts for your Azure OpenAI Batch API to generate high-converting affiliate blog posts using your product database.

## Batch Processing Overview

Use these prompts with your `blog_generation_templates` and `BlogAIGenerator` service to create scalable content that:
- Integrates your actual products (5,926 items across 76 brands)
- Optimizes for affiliate conversions
- Follows SEO best practices
- Maintains consistent quality and structure

---

## Template 1: Ultimate Buying Guide Prompts

### System Prompt for All Buying Guides:
```json
{
  "role": "system",
  "content": "You are an expert music gear writer with 20+ years of experience reviewing and recommending musical instruments. You have extensive knowledge of major brands like Fender, Gibson, Yamaha, Harley Benton, and understand both professional and beginner needs. Your writing is authoritative, honest, SEO-optimized, and designed to help readers make informed purchasing decisions. You naturally integrate affiliate product recommendations where they genuinely solve reader problems."
}
```

### Buying Guide Prompt Template:
```json
{
  "role": "user", 
  "content": "Write a comprehensive 2,500-word buying guide titled '{TITLE}' focusing on {CATEGORY} instruments. Structure as follows:\n\n1. **Hook Introduction (150 words)**: Address the pain point of choosing the right {CATEGORY}. End with value proposition.\n\n2. **Quick Recommendations Summary (200 words)**:\n   - Best Overall: {PRODUCT_1_NAME} (ID: {PRODUCT_1_ID})\n   - Best Budget: {PRODUCT_2_NAME} (ID: {PRODUCT_2_ID})\n   - Best Premium: {PRODUCT_3_NAME} (ID: {PRODUCT_3_ID})\n   Include brief reasoning and price ranges.\n\n3. **Buying Considerations (400 words)**:\n   - Key technical specifications\n   - Skill level matching\n   - Budget breakdowns ($200-400, $400-800, $800+)\n   - Common mistakes to avoid\n\n4. **Detailed Product Reviews (1200 words)**:\n   For each featured product, include:\n   - Why it made our list\n   - Key specifications\n   - Sound characteristics\n   - Build quality assessment\n   - Who it's perfect for\n   - Pros and cons (4-5 each)\n   - Current pricing and availability\n   - [🛒 Check Latest Price] call-to-action\n\n5. **Comparison Matrix (300 words)**:\n   Side-by-side comparison table of key specs and features\n\n6. **Genre-Specific Recommendations (200 words)**:\n   - Rock/Metal\n   - Blues/Jazz\n   - Country/Folk\n   - Recording/Studio\n\n7. **Conclusion & Final Advice (150 words)**:\n   Clear winner recommendations with compelling purchase reasoning\n\n**Products to feature:**\n{PRODUCT_LIST}\n\n**SEO Requirements:**\n- Target keyword: '{PRIMARY_KEYWORD}'\n- Include secondary keywords: {SECONDARY_KEYWORDS}\n- Natural keyword density 1-2%\n- Meta description under 160 characters\n- Use schema markup suggestions\n\n**Affiliate Integration:**\n- Include 'Check Latest Price' for each product\n- Compare pricing across multiple retailers\n- Mention seasonal deals and price trends\n- Add value-focused purchase urgency\n\nWrite in engaging, expert tone with specific technical details and real-world playing examples."
}
```

---

## Template 2: Product Comparison Prompts

### Head-to-Head Comparison Prompt:
```json
{
  "role": "user",
  "content": "Create a detailed 2,000-word comparison article: '{PRODUCT_A_NAME}' vs '{PRODUCT_B_NAME}' - Which {CATEGORY} Should You Buy in 2025?\n\n**Structure:**\n\n1. **Introduction (200 words)**:\n   - Why these models are commonly compared\n   - Key differences at a glance\n   - Who should read this comparison\n\n2. **Quick Verdict Table (150 words)**:\n   | Category | Winner | Reason |\n   |----------|--------|---------|\n   | Sound Quality | [A/B] | [Brief reason] |\n   | Build Quality | [A/B] | [Brief reason] |\n   | Value for Money | [A/B] | [Brief reason] |\n   | Ease of Use | [A/B] | [Brief reason] |\n   | Recording | [A/B] | [Brief reason] |\n\n3. **Specifications Comparison (300 words)**:\n   Detailed side-by-side spec table with explanations\n\n4. **Sound & Performance Analysis (600 words)**:\n   - Tonal characteristics of each\n   - Recording quality comparison\n   - Live performance differences\n   - Genre suitability\n   - Real-world playing examples\n\n5. **Build Quality & Design (300 words)**:\n   - Materials and construction\n   - Hardware quality\n   - Durability expectations\n   - Aesthetic differences\n\n6. **Value Analysis (250 words)**:\n   - Price-to-performance ratio\n   - Long-term investment value\n   - Resale value considerations\n   - Hidden costs (setup, maintenance)\n\n7. **User Experience (200 words)**:\n   - Setup and learning curve\n   - Customer support comparison\n   - Warranty differences\n   - User community and resources\n\n**Products:**\n- Product A: {PRODUCT_A_NAME} (ID: {PRODUCT_A_ID})\n- Product B: {PRODUCT_B_NAME} (ID: {PRODUCT_B_ID})\n\n**Target Keywords:** '{PRODUCT_A_NAME} vs {PRODUCT_B_NAME}', '{CATEGORY} comparison', 'best {CATEGORY} 2025'\n\n**Affiliate Strategy:**\n- Include current pricing for both\n- Mention where to buy (multiple retailers)\n- Add urgency with stock levels/deals\n- Suggest complementary accessories\n- Provide clear purchase recommendations\n\nEnd with definitive recommendation based on different use cases and budgets."
}
```

---

## Template 3: Product Review Prompts

### In-Depth Review Prompt:
```json
{
  "role": "user",
  "content": "Write a comprehensive 1,800-word review: '{PRODUCT_NAME} Review: Is It Worth Buying in 2025?'\n\n**Structure:**\n\n1. **Hook Introduction (150 words)**:\n   - Address specific problem this product solves\n   - Include product name and main benefit\n   - Compelling reason to keep reading\n\n2. **Quick Answer/TL;DR (100 words)**:\n   - 3-sentence verdict summary\n   - Price range and retailer links\n   - Who this product is perfect for\n\n3. **Product Overview & Specifications (300 words)**:\n   - Complete technical specifications\n   - What makes it special/different\n   - Build quality and materials analysis\n   - Manufacturing details and quality control\n\n4. **Performance Deep Dive (500 words)**:\n   - Sound quality detailed analysis\n   - Real-world testing scenarios\n   - Recording quality assessment\n   - Live performance characteristics\n   - Comparison to similar products\n\n5. **User Experience (250 words)**:\n   - Setup process and difficulty\n   - Learning curve assessment\n   - Daily use considerations\n   - Maintenance requirements\n\n6. **Pros & Cons Analysis (200 words)**:\n   **✅ Pros (5-6 points):**\n   - [Specific strengths with examples]\n   \n   **❌ Cons (3-4 points):**\n   - [Honest limitations with context]\n\n7. **Value Assessment (150 words)**:\n   - Price-to-performance analysis\n   - Comparison to competitors at same price\n   - Long-term value proposition\n   - Who gets the best value\n\n8. **Purchase Decision Guide (150 words)**:\n   - Who should buy this\n   - Who should look elsewhere\n   - Alternative recommendations\n   - Best deals and where to buy\n\n**Product Details:**\n- Name: {PRODUCT_NAME}\n- ID: {PRODUCT_ID}\n- Category: {CATEGORY}\n- Brand: {BRAND_NAME}\n- Price Range: {PRICE_RANGE}\n\n**SEO Optimization:**\n- Primary keyword: '{PRODUCT_NAME} review'\n- Long-tail targets: '{PRODUCT_NAME} vs alternatives', 'is {PRODUCT_NAME} worth it'\n- Include FAQ section with common questions\n- Optimize for featured snippets\n\n**Affiliate Integration:**\n- Multiple 'Check Latest Price' CTAs\n- Compare pricing across 2-3 retailers\n- Bundle/accessory recommendations\n- Seasonal deal mentions\n\nWrite with personal experience tone, specific examples, and honest assessment that builds trust while driving conversions."
}
```

---

## Template 4: Budget vs Premium Analysis

### Value Comparison Prompt:
```json
{
  "role": "user",
  "content": "Create a 1,500-word analysis: 'Budget vs Premium {CATEGORY}: When to Save vs When to Spend in 2025'\n\n**Featured Products:**\n- Budget Champion: {BUDGET_PRODUCT_NAME} (ID: {BUDGET_ID}) - ${BUDGET_PRICE}\n- Premium Leader: {PREMIUM_PRODUCT_NAME} (ID: {PREMIUM_ID}) - ${PREMIUM_PRICE}\n- Sweet Spot: {MID_RANGE_PRODUCT_NAME} (ID: {MID_ID}) - ${MID_PRICE}\n\n**Structure:**\n\n1. **The Budget vs Premium Dilemma (200 words)**:\n   - Common customer confusion\n   - When price reflects quality vs marketing\n   - Framework for making the decision\n\n2. **Budget Category Analysis (400 words)**:\n   - What you get for ${BUDGET_PRICE}\n   - Manufacturing compromises and smart savings\n   - Performance expectations and limitations\n   - Who benefits most from budget options\n   - Featured: {BUDGET_PRODUCT_NAME} detailed review\n\n3. **Premium Category Analysis (400 words)**:\n   - Premium features and their real-world value\n   - Build quality differences that matter\n   - Professional use case justifications\n   - Long-term ownership considerations\n   - Featured: {PREMIUM_PRODUCT_NAME} detailed review\n\n4. **The Sweet Spot Alternative (300 words)**:\n   - Mid-range options that balance value and performance\n   - Featured: {MID_RANGE_PRODUCT_NAME}\n   - When middle-ground makes most sense\n\n5. **Decision Matrix (200 words)**:\n   | Your Situation | Recommended Choice | Why |\n   |----------------|--------------------|-----|\n   | Beginner, tight budget | Budget | Learning fundamentals |\n   | Hobbyist, regular player | Mid-range | Best long-term value |\n   | Professional/serious amateur | Premium | Performance justifies cost |\n   | Recording artist | Premium | Studio-quality needed |\n\n**Target Keywords:** 'budget vs premium {CATEGORY}', 'best value {CATEGORY}', '{CATEGORY} price guide'\n\n**Conversion Strategy:**\n- Clear purchase recommendations for each budget\n- Current deal alerts and pricing\n- Total cost of ownership analysis\n- Upgrade path suggestions\n\nEnd with actionable advice based on reader's specific situation and budget."
}
```

---

## Template 5: Seasonal Deal & Roundup Prompts

### Black Friday / Seasonal Deals Prompt:
```json
{
  "role": "user",
  "content": "Write a 2,000-word seasonal deals guide: 'Black Friday Music Gear Deals 2025: Best {CATEGORY} Discounts & Buying Strategy'\n\n**Deal Categories:**\n\n1. **Lightning Deals (300 words)**:\n   - Time-sensitive offers under $200\n   - Featured budget products with % savings\n   - Inventory warnings and urgency\n\n2. **Mid-Range Steals (400 words)**:\n   - $200-800 products with significant discounts\n   - Compare regular vs sale pricing\n   - Why these deals are exceptional\n\n3. **Premium Bargains (400 words)**:\n   - High-end gear rarely discounted\n   - Professional instruments with limited-time pricing\n   - Investment opportunities\n\n4. **Bundle Deals (300 words)**:\n   - Complete starter packages\n   - Multi-item savings analysis\n   - Total value calculations\n\n5. **Shopping Strategy (300 words)**:\n   - When to buy vs wait\n   - Price tracking and historical trends\n   - Retailer comparison for best deals\n\n6. **Avoid These Traps (200 words)**:\n   - Fake discounts and marketing tricks\n   - Products to avoid even on sale\n   - Quality vs price red flags\n\n7. **Deal Deadlines & Action Items (100 words)**:\n   - Specific end dates\n   - Stock level warnings\n   - Clear next steps for readers\n\n**Products to Feature:** {SEASONAL_PRODUCT_LIST}\n\n**Urgency Elements:**\n- Limited stock notifications\n- Deal expiration countdowns\n- 'Only X left at this price'\n- Historical price comparisons\n\n**Affiliate Optimization:**\n- Track deal-specific affiliate links\n- Compare savings across retailers\n- Bundle recommendations for higher cart values\n- Email signup for deal alerts\n\nCreate genuine urgency while providing real value and honest deal assessment."
}
```

---

## Template 6: Tutorial-Style Content Prompts

### Setup & How-To Guide Prompt:
```json
{
  "role": "user",
  "content": "Create a comprehensive tutorial: '{PRODUCT_CATEGORY} Setup Guide 2025: From Unboxing to First Performance'\n\n**Tutorial Structure:**\n\n1. **What You'll Need (200 words)**:\n   - Main instrument: {FEATURED_PRODUCT} (ID: {PRODUCT_ID})\n   - Essential accessories and why\n   - Optional upgrades for better experience\n   - Tools and workspace requirements\n\n2. **Unboxing & Initial Inspection (250 words)**:\n   - What should be included\n   - Quality check points\n   - Red flags for returns/exchanges\n   - First impressions that matter\n\n3. **Basic Setup Process (400 words)**:\n   - Step-by-step setup instructions\n   - Common beginner mistakes\n   - Adjustment procedures\n   - Safety considerations\n\n4. **Optimization & Fine-Tuning (350 words)**:\n   - Professional setup techniques\n   - Personal preference adjustments\n   - Performance optimization tips\n   - Troubleshooting common issues\n\n5. **First Practice Session (300 words)**:\n   - Realistic expectations for beginners\n   - Essential exercises to try\n   - Progress tracking suggestions\n   - When to seek professional help\n\n6. **Maintenance & Care (200 words)**:\n   - Daily care routine\n   - Long-term maintenance schedule\n   - Storage and transportation\n   - When to replace parts/upgrade\n\n**Product Integration:**\n- Featured instrument: {FEATURED_PRODUCT_NAME}\n- Recommended accessories with affiliate links\n- Upgrade suggestions as skills develop\n- Troubleshooting with product-specific solutions\n\n**SEO Targets:** '{PRODUCT_CATEGORY} setup guide', 'how to setup {FEATURED_PRODUCT}', '{CATEGORY} beginner guide'\n\n**Conversion Strategy:**\n- Problem → Product solution format\n- Accessory upsells throughout content\n- 'Complete setup' bundle suggestions\n- Follow-up content recommendations\n\nMake actionable with specific steps, realistic timelines, and clear success metrics."
}
```

---

## Batch Generation Variables

### Product Data Integration:
For each prompt, populate these variables from your database:

```json
{
  "PRODUCT_1_NAME": "Fender Player II Stratocaster MN ACB",
  "PRODUCT_1_ID": 376,
  "PRODUCT_2_NAME": "Harley Benton SC-Custom III Purple Burst", 
  "PRODUCT_2_ID": 253,
  "PRODUCT_3_NAME": "Gibson Les Paul Standard 60 Fd VCS",
  "PRODUCT_3_ID": 619,
  "CATEGORY": "Electric Guitars",
  "BRAND_NAME": "Fender/Gibson/Harley Benton",
  "PRICE_RANGE": "$300-2500",
  "PRIMARY_KEYWORD": "best electric guitars 2025",
  "SECONDARY_KEYWORDS": ["electric guitar buying guide", "Fender vs Gibson", "budget electric guitars"]
}
```

### Content Variations:
Create multiple variations by changing:
- Target audience (beginner/intermediate/professional)
- Budget ranges ($0-300, $300-800, $800+)
- Use cases (home recording, live performance, practice)
- Genres (rock, jazz, country, metal)

---

## Batch Processing Workflow

1. **Prepare Product Lists**: Query your database for relevant products by category
2. **Generate Variable Sets**: Create JSON objects with product data for each post
3. **Build Batch Requests**: Use templates with populated variables
4. **Process with Azure OpenAI Batch API**: Submit through your blog system
5. **Parse and Store**: Use your existing `_parse_ai_response()` and database insertion

### Sample Batch Request Format:
```json
{
  "custom_id": "blog-post-electric-guitars-guide-001",
  "method": "POST",
  "url": "/v1/chat/completions",
  "body": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system", 
        "content": "[System prompt from templates above]"
      },
      {
        "role": "user",
        "content": "[Populated prompt template with your product data]"
      }
    ],
    "response_format": {"type": "json_object"},
    "temperature": 0.7,
    "max_tokens": 4000
  }
}
```

This batch system will generate high-quality, product-integrated content at scale while maintaining consistency with your affiliate marketing goals and SEO requirements.
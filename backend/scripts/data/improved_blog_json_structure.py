#!/usr/bin/env python3
"""
Improved Blog JSON Structure for Better Affiliate Integration
This script defines the new standardized JSON structure for blog posts with comprehensive affiliate integration.
"""

# New standardized JSON structure for blog posts
IMPROVED_JSON_STRUCTURE = """
RESPOND ONLY WITH VALID JSON IN THIS EXACT FORMAT:
{
  "title": "SEO-optimized blog post title (60 chars max)",
  "excerpt": "Compelling 1-2 sentence summary (150-200 chars)",
  "seo_title": "SEO title (60 chars max)",
  "seo_description": "SEO meta description (155 chars max)",
  "featured_image_alt": "Descriptive alt text for featured image",
  "reading_time": 12,
  "word_count": 2800,
  "sections": [
    {
      "type": "introduction",
      "title": "Hook readers with compelling opening",
      "content": "Engaging introduction that addresses pain points and promises value",
      "affiliate_placement": "none"
    },
    {
      "type": "product_showcase_inline",
      "title": "Top Pick: [Product Name]",
      "content": "Detailed product analysis with pros/cons and use cases",
      "products": [
        {
          "product_id": 1,
          "context": "Why this is the top choice with specific benefits",
          "position": 1,
          "affiliate_placement": "inline",
          "cta_text": "Check Latest Price"
        }
      ],
      "affiliate_placement": "inline"
    },
    {
      "type": "comparison_table",
      "title": "Quick Comparison",
      "content": "Side-by-side comparison of featured products",
      "headers": ["Feature", "Product A", "Product B", "Product C"],
      "rows": [
        ["Price Range", "$300-400", "$500-600", "$700-800"],
        ["Best For", "Beginners", "Intermediate", "Professional"]
      ],
      "products_mentioned": [1, 2, 3],
      "affiliate_placement": "below_table"
    },
    {
      "type": "buying_guide",
      "title": "What to Look For",
      "content": "Comprehensive buying criteria with specific recommendations",
      "affiliate_placement": "none"
    },
    {
      "type": "product_showcase_inline",
      "title": "Budget Pick: [Product Name]",
      "content": "Detailed analysis of budget-friendly option",
      "products": [
        {
          "product_id": 2,
          "context": "Best value proposition and who it's perfect for",
          "position": 2,
          "affiliate_placement": "inline",
          "cta_text": "View at Store"
        }
      ],
      "affiliate_placement": "inline"
    },
    {
      "type": "pros_cons",
      "title": "Pros & Cons Analysis",
      "pros": ["Specific advantage 1", "Specific advantage 2", "Specific advantage 3"],
      "cons": ["Specific limitation 1", "Specific limitation 2"],
      "content": "Balanced analysis of trade-offs",
      "affiliate_placement": "none"
    },
    {
      "type": "product_showcase_inline",
      "title": "Premium Choice: [Product Name]",
      "content": "In-depth analysis of high-end option",
      "products": [
        {
          "product_id": 3,
          "context": "Why professionals choose this and what makes it worth the investment",
          "position": 3,
          "affiliate_placement": "inline",
          "cta_text": "Shop Now"
        }
      ],
      "affiliate_placement": "inline"
    },
    {
      "type": "use_cases",
      "title": "Who Should Buy What",
      "content": "Clear recommendations by user type, skill level, and budget",
      "products_mentioned": [1, 2, 3],
      "affiliate_placement": "none"
    },
    {
      "type": "faqs",
      "title": "Frequently Asked Questions",
      "content": "Address common concerns and questions",
      "faqs": [
        {
          "question": "What's the most important factor when choosing?",
          "answer": "Detailed answer with specific guidance and product recommendations"
        }
      ],
      "affiliate_placement": "none"
    },
    {
      "type": "conclusion",
      "title": "Final Recommendations",
      "content": "Clear final verdict with specific product recommendations and next steps",
      "products_mentioned": [1, 2, 3],
      "affiliate_placement": "none"
    }
  ],
  "tags": ["buying_guide", "2025", "expert_picks", "comparison"],
  "meta": {
    "content_type": "comprehensive_guide",
    "expertise_level": "all_levels",
    "target_audience": ["beginners", "intermediate", "professionals"],
    "key_benefits": ["save_money", "avoid_mistakes", "find_perfect_match", "expert_guidance"],
    "estimated_read_time": 12,
    "affiliate_integration": "comprehensive"
  },
  "product_recommendations": [
    {
      "product_id": 1,
      "relevance_score": 0.95,
      "reasoning": "Top overall choice for most users due to balance of features and value",
      "suggested_context": "top_pick",
      "suggested_sections": ["product_showcase_inline", "comparison_table", "conclusion"],
      "affiliate_placement": "inline"
    },
    {
      "product_id": 2,
      "relevance_score": 0.90,
      "reasoning": "Best budget option that doesn't compromise on quality",
      "suggested_context": "budget_pick",
      "suggested_sections": ["product_showcase_inline", "comparison_table", "use_cases"],
      "affiliate_placement": "inline"
    },
    {
      "product_id": 3,
      "relevance_score": 0.88,
      "reasoning": "Premium choice for professionals and serious enthusiasts",
      "suggested_context": "premium_choice",
      "suggested_sections": ["product_showcase_inline", "comparison_table", "conclusion"],
      "affiliate_placement": "inline"
    }
  ]
}

CRITICAL REQUIREMENTS:
- Target 2500-3000 words for comprehensive coverage
- Include 3-5 inline product showcases with affiliate CTAs
- Every product mention should have clear affiliate integration
- Use specific, actionable language that drives conversions
- Include comparison tables and detailed analysis
- Address different user types and budgets
- Provide clear next steps and purchase guidance
"""

# Section types with affiliate integration
SECTION_TYPES = {
    "introduction": {
        "description": "Hook readers with compelling opening",
        "affiliate_placement": "none",
        "required_fields": ["title", "content"]
    },
    "product_showcase_inline": {
        "description": "Detailed product analysis with inline affiliate components",
        "affiliate_placement": "inline",
        "required_fields": ["title", "content", "products"],
        "products_structure": {
            "product_id": "integer - database product ID",
            "context": "string - why this product is recommended",
            "position": "integer - ranking position",
            "affiliate_placement": "string - inline, below, above",
            "cta_text": "string - call-to-action text"
        }
    },
    "comparison_table": {
        "description": "Side-by-side product comparison with affiliate placement",
        "affiliate_placement": "below_table",
        "required_fields": ["title", "content", "headers", "rows", "products_mentioned"]
    },
    "buying_guide": {
        "description": "Comprehensive buying criteria and recommendations",
        "affiliate_placement": "none",
        "required_fields": ["title", "content"]
    },
    "pros_cons": {
        "description": "Balanced analysis of advantages and limitations",
        "affiliate_placement": "none",
        "required_fields": ["title", "content", "pros", "cons"]
    },
    "use_cases": {
        "description": "Clear recommendations by user type and budget",
        "affiliate_placement": "none",
        "required_fields": ["title", "content", "products_mentioned"]
    },
    "faqs": {
        "description": "Address common concerns with product recommendations",
        "affiliate_placement": "none",
        "required_fields": ["title", "content", "faqs"]
    },
    "conclusion": {
        "description": "Final recommendations with clear next steps",
        "affiliate_placement": "none",
        "required_fields": ["title", "content", "products_mentioned"]
    }
}

# Affiliate placement options
AFFILIATE_PLACEMENTS = {
    "none": "No affiliate components in this section",
    "inline": "Inline product showcase with CTAs",
    "below": "Affiliate components below content",
    "above": "Affiliate components above content",
    "below_table": "Affiliate components below comparison table",
    "sidebar": "Affiliate components in sidebar"
}

# CTA text variations for different contexts
CTA_VARIATIONS = {
    "top_pick": "Check Latest Price",
    "budget_pick": "View at Store", 
    "premium_choice": "Shop Now",
    "comparison": "Compare Prices",
    "review": "Read Full Review",
    "deal": "Grab This Deal",
    "general": "Learn More"
}

def validate_blog_json_structure(json_data):
    """Validate that the JSON follows the improved structure"""
    required_fields = ["title", "excerpt", "seo_title", "seo_description", "sections", "tags", "meta"]
    
    for field in required_fields:
        if field not in json_data:
            return False, f"Missing required field: {field}"
    
    # Validate sections
    if not isinstance(json_data["sections"], list):
        return False, "Sections must be an array"
    
    for i, section in enumerate(json_data["sections"]):
        if "type" not in section:
            return False, f"Section {i} missing type"
        
        section_type = section["type"]
        if section_type not in SECTION_TYPES:
            return False, f"Section {i} has invalid type: {section_type}"
        
        # Check required fields for this section type
        required_section_fields = SECTION_TYPES[section_type]["required_fields"]
        for field in required_section_fields:
            if field not in section:
                return False, f"Section {i} ({section_type}) missing required field: {field}"
    
    return True, "Valid structure"

def get_affiliate_placement_guidance(section_type, context=""):
    """Get guidance on where to place affiliate components"""
    placement = SECTION_TYPES.get(section_type, {}).get("affiliate_placement", "none")
    
    guidance = {
        "none": "Focus on content quality, no affiliate components needed",
        "inline": "Include inline product showcase with detailed analysis and CTAs",
        "below": "Add affiliate components after the main content",
        "above": "Add affiliate components before the main content", 
        "below_table": "Add affiliate components after comparison table",
        "sidebar": "Include affiliate components in sidebar"
    }
    
    return placement, guidance.get(placement, "No specific guidance")

if __name__ == "__main__":
    print("📋 Improved Blog JSON Structure")
    print("=" * 50)
    print(f"Section types: {len(SECTION_TYPES)}")
    print(f"Affiliate placements: {len(AFFILIATE_PLACEMENTS)}")
    print(f"CTA variations: {len(CTA_VARIATIONS)}")
    print("\n✅ Structure ready for implementation!")

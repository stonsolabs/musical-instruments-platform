export interface BlogCategory {
  id: number;
  name: string;
  slug: string;
  description?: string;
  icon?: string;
  color?: string;
  sort_order: number;
  is_active: boolean;
}

export interface BlogTag {
  id: number;
  name: string;
  slug: string;
}

export interface BlogPostProduct {
  id: number;
  product_id: number;
  position: number;
  context?: string;
  product_name?: string;
  product_slug?: string;
  product_brand?: string;
}

export interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt?: string;
  content: string;
  featured_image?: string;
  category?: BlogCategory;
  author_name: string;
  status: string;
  seo_title?: string;
  seo_description?: string;
  reading_time?: number;
  view_count: number;
  featured: boolean;
  published_at?: string;
  created_at: string;
  updated_at: string;
  tags: BlogTag[];
  products: BlogPostProduct[];
}

export interface BlogPostSummary {
  id: number;
  title: string;
  slug: string;
  excerpt?: string;
  featured_image?: string;
  category?: BlogCategory;
  author_name: string;
  reading_time?: number;
  view_count: number;
  featured: boolean;
  published_at?: string;
  tags: BlogTag[];
}

// AI-enhanced blog types
export interface BlogGenerationTemplate {
  id: number;
  name: string;
  description?: string;
  category_id?: number;
  template_type: 'general' | 'buying_guide' | 'review' | 'comparison' | 'tutorial' | 'history';
  base_prompt: string;
  system_prompt?: string;
  product_context_prompt?: string;
  required_product_types: string[];
  min_products: number;
  max_products: number;
  suggested_tags: string[];
  seo_title_template?: string;
  seo_description_template?: string;
  content_structure: any;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface EnhancedBlogPostProduct extends BlogPostProduct {
  ai_context?: string;
  relevance_score?: number;
  mentioned_in_sections: string[];
}

export interface BlogContentSection {
  id: number;
  blog_post_id: number;
  section_type: string;
  section_title?: string;
  section_content: string;
  section_order: number;
  products_featured: number[];
  ai_generated: boolean;
  created_at: string;
}

export interface BlogGenerationHistory {
  id: number;
  blog_post_id?: number;
  template_id?: number;
  generation_status: 'pending' | 'generating' | 'completed' | 'failed' | 'cancelled';
  prompt_used?: string;
  model_used?: string;
  tokens_used?: number;
  generation_time_ms?: number;
  error_message?: string;
  generation_metadata: any;
  created_at: string;
}

export interface AIBlogPost extends BlogPost {
  generated_by_ai: boolean;
  generation_prompt?: string;
  generation_model?: string;
  generation_params: any;
  ai_notes?: string;
  products: EnhancedBlogPostProduct[];
  sections: BlogContentSection[];
  generation_history: BlogGenerationHistory[];
}

export interface BlogGenerationRequest {
  template_id: number;
  title?: string;
  category_id?: number;
  product_ids: number[];
  custom_prompt_additions?: string;
  target_word_count: number;
  include_seo_optimization: boolean;
  auto_publish: boolean;
  generation_params: {
    model?: string;
    temperature?: number;
    max_tokens?: number;
  };
}

export interface BlogGenerationResult {
  success: boolean;
  blog_post_id?: number;
  generation_history_id?: number;
  generated_content?: string;
  generated_title?: string;
  generated_excerpt?: string;
  seo_title?: string;
  seo_description?: string;
  tokens_used?: number;
  generation_time_ms?: number;
  error_message?: string;
  warnings?: string[];
}
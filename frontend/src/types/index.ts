export interface Brand {
  id: number;
  name: string;
  slug: string;
  logo_url?: string;
  website_url?: string;
  description?: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  parent_id?: number;
  description?: string;
  image_url?: string;
  is_active: boolean;
}

export interface ProductPrice {
  id: number;
  store: {
    id: number;
    name: string;
    slug: string;
  };
  price: number;
  currency: string;
  affiliate_url: string;
  last_checked: string;
  is_available: boolean;
}

export interface ProductSpecifications {
  [key: string]: string | number | boolean;
}

export interface ProductContent {
  specifications?: ProductSpecifications;
  store_links?: Record<string, string>;
  warranty_info?: string;
  qa?: Record<string, any>;
  sources?: any[];
  dates?: Record<string, string>;
  content_metadata?: Record<string, any>;
  related_products?: any[];
  localized_content?: Record<string, any>;
  // Enrichment fields (optional)
  professional_ratings?: {
    playability?: number;
    sound?: number;
    build?: number;
    value?: number;
    overall_score?: number;
    notes?: string;
  };
  audience_fit?: {
    beginners?: boolean;
    intermediate?: boolean;
    professionals?: boolean;
    learning_curve?: string;
    suitable_genres?: string[];
    studio_live_role?: string;
  };
  comparison_helpers?: {
    standout_strengths?: string[];
    key_tradeoffs?: string[];
    best_for?: string[];
    not_ideal_for?: string[];
  };
  category_specific?: {
    metrics?: Record<string, number>;
  };
  accessory_recommendations?: Array<{ name: string; why: string }>;
  setup_tips?: string[];
  quick_badges?: Record<string, boolean>;
}

export interface VoteStats {
  thumbs_up_count: number;
  thumbs_down_count: number;
}

export interface Product {
  id: number;
  sku: string;
  name: string;
  slug: string;
  brand: Brand;
  category: Category;
  description?: string;
  images?: string[];
  msrp_price?: number;
  specifications?: ProductSpecifications;
  content?: ProductContent;
  ai_content?: {
    qa?: Array<{question: string; answer: string}>;
    dates?: Record<string, string>;
    sources?: string[];
    store_links?: Record<string, string>;
    warranty_info?: string;
    specifications?: ProductSpecifications;
    content_metadata?: Record<string, any>;
    related_products?: any[];
    localized_content?: Record<string, {
      basic_info?: string;
      usage_guidance?: string;
      customer_reviews?: string;
      maintenance_care?: string;
      purchase_decision?: string;
      technical_analysis?: string;
      professional_assessment?: string;
    }>;
  };
  avg_rating?: number;
  review_count: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  vote_stats?: VoteStats;
  thomann_info?: {
    url: string;
  };
  prices?: ProductPrice[];
}

export interface ProductComparison {
  products: Product[];
  common_specs: string[];
  comparison_matrix: Record<string, Record<string, any>>;
}

export interface SearchResult {
  products: Product[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface TrendingProduct {
  product: Product;
  trending_score: number;
  price_change?: number;
  popularity_increase?: number;
}

export interface AffiliateStore {
  id: number;
  name: string;
  slug: string;
  logo_url?: string;
  website_url: string;
  description?: string;
  is_active: boolean;
  has_affiliate_program: boolean;
  show_affiliate_buttons: boolean;
  priority: number;
  affiliate_base_url?: string;
  affiliate_id?: string;
  affiliate_parameters?: Record<string, any>;
}

// Extended store shape returned by product affiliate endpoints
export interface AffiliateStoreWithUrl extends AffiliateStore {
  original_url?: string;
  affiliate_url?: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

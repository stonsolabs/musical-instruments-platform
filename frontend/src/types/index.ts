export interface Brand {
  id: number;
  name: string;
  slug: string;
  logo_url?: string;
  description?: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  parent_id?: number;
  image_url?: string;
}

export interface ProductPrice {
  id: number;
  store: {
    id: number;
    name: string;
    logo_url?: string;
    website_url: string;
  };
  price: number;
  currency: string;
  affiliate_url: string;
  last_checked: string;
  is_available: boolean;
}

export interface Product {
  id: number;
  sku: string;
  name: string;
  slug: string;
  brand: Brand;
  category: Category;
  description?: string;
  specifications: Record<string, any>;
  images: string[];
  msrp_price?: number;
  best_price?: ProductPrice;
  prices?: ProductPrice[];
  avg_rating: number;
  review_count: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  ai_content?: {
    summary?: string;
    pros?: string[];
    cons?: string[];
    best_for?: string[];
    genres?: string[];
    skill_level?: string;
    use_cases?: string;
    recommendations?: string;
  };
}

export interface SearchResponse {
  products: Product[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    pages: number;
  };
  filters_applied: {
    q?: string;
    category?: string;
    brand?: string;
    min_price?: number;
    max_price?: number;
    sort_by: string;
  };
}

export interface ComparisonResponse {
  products: Product[];
  common_specs: string[];
  comparison_matrix: Record<string, Record<string, any>>;
  generated_at: string;
}

export interface SearchAutocompleteProduct {
  id: number;
  name: string;
  slug: string;
  brand: Brand;
  category: Category;
  avg_rating: number;
  review_count: number;
  best_price?: {
    price: number;
    currency: string;
    store: {
      id: number;
      name: string;
      slug: string;
    };
    affiliate_url: string;
  };
  rank: number;
  search_highlight: string;
}

export interface SearchAutocompleteResponse {
  query: string;
  results: SearchAutocompleteProduct[];
  total: number;
}



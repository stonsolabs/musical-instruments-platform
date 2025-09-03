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

export interface ThomannInfo {
  has_direct_url: boolean;
  url: string;
  fallback_search_url: string;
}

// Comprehensive AI-generated content interfaces
export interface BasicInfo {
  overview: string;
  key_features: string[];
  target_skill_level: string;
  country_of_origin: string;
  release_year: string;
}

export interface SoundCharacteristics {
  tonal_profile: string;
  output_level: string;
  best_genres: string[];
  pickup_positions?: Record<string, string>;
}

export interface BuildQuality {
  construction_type: string;
  hardware_quality: string;
  finish_quality: string;
  expected_durability: string;
}

export interface Playability {
  neck_profile: string;
  action_setup: string;
  comfort_rating: string;
  weight_category: string;
}

export interface TechnicalAnalysis {
  sound_characteristics: SoundCharacteristics;
  build_quality: BuildQuality;
  playability: Playability;
}

export interface PurchaseReason {
  title: string;
  description: string;
}

export interface UserType {
  user_type: string;
  reason: string;
}

export interface PurchaseDecision {
  why_buy: PurchaseReason[];
  why_not_buy: PurchaseReason[];
  best_for: UserType[];
  not_ideal_for: UserType[];
}

export interface SuitableMusicStyles {
  excellent: string[];
  good: string[];
  limited: string[];
}

export interface SkillDevelopment {
  learning_curve: string;
  growth_potential: string;
}

export interface UsageGuidance {
  recommended_amplifiers: string[];
  suitable_music_styles: SuitableMusicStyles;
  skill_development: SkillDevelopment;
}

export interface CareInstructions {
  daily: string;
  weekly: string;
  monthly: string;
  annual: string;
}

export interface UpgradePotential {
  easy_upgrades: string[];
  recommended_budget: string;
}

export interface MaintenanceCare {
  maintenance_level: string;
  common_issues: string[];
  care_instructions: CareInstructions;
  upgrade_potential: UpgradePotential;
}

export interface ExpertRating {
  build_quality: number | string;
  sound_quality: number | string;
  value_for_money: number | string;
  versatility: number | string;
}

export interface ProfessionalAssessment {
  expert_rating: ExpertRating;
  standout_features: string[];
  notable_limitations: string[];
  competitive_position: string;
}

export interface ContentMetadata {
  generated_date: string;
  content_version: string;
  seo_keywords: string[];
  readability_score: string;
  word_count: string;
}

export interface ComprehensiveAIContent {
  basic_info: BasicInfo;
  technical_analysis: TechnicalAnalysis;
  purchase_decision: PurchaseDecision;
  usage_guidance: UsageGuidance;
  maintenance_care: MaintenanceCare;
  professional_assessment: ProfessionalAssessment;
  content_metadata: ContentMetadata;
}

export interface VoteStats {
  thumbs_up_count: number;
  thumbs_down_count: number;
  total_votes: number;
  vote_score: number;
  user_vote?: 'up' | 'down' | null;
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
  prices?: ProductPrice[];
  avg_rating: number;
  review_count: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  ai_content?: ComprehensiveAIContent;
  vote_stats?: VoteStats;
  thomann_info?: ThomannInfo;
  content?: {
    store_links?: Record<string, string>;
    specifications?: Record<string, any>;
    [key: string]: any;
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
  images: string[];
  prices?: {
    id: number;
    price: number;
    currency: string;
    store: {
      id: number;
      name: string;
      slug: string;
    };
    affiliate_url: string;
    is_available: boolean;
    last_checked?: string;
  }[];
  rank: number;
  search_highlight: string;
}

export interface SearchAutocompleteResponse {
  query: string;
  results: SearchAutocompleteProduct[];
  total: number;
}

// New interfaces for enhanced backend features

export interface AffiliateStore {
  id: number;
  name: string;
  slug: string;
  website_url: string;
  logo_url?: string;
  description?: string;
  has_affiliate_program: boolean;
  affiliate_base_url?: string;
  affiliate_id?: string;
  domain_affiliate_ids?: Record<string, string>;
  available_regions: string[];
  primary_region: string;
  regional_priority?: Record<string, number>;
  use_store_fallback: boolean;
  store_fallback_url?: string;
  priority: number;
  show_affiliate_buttons: boolean;
  is_active: boolean;
}

export interface TrendingProduct {
  id: number;
  name: string;
  slug: string;
  brand: Brand;
  category: Category;
  images: string[];
  prices?: ProductPrice[];
  avg_rating: number;
  review_count: number;
  view_count: number;
  comparison_count: number;
  trending_score: number;
  content?: {
    store_links?: Record<string, string>;
    specifications?: Record<string, any>;
    [key: string]: any;
  };
}

export interface TrendingResponse {
  products: TrendingProduct[];
  total: number;
  period: string;
  generated_at: string;
}

export interface TrendingComparison {
  products: Product[];
  comparison_count: number;
  last_compared: string;
}

export interface TrendingComparisonsResponse {
  comparisons: TrendingComparison[];
  total: number;
  period: string;
  generated_at: string;
}

export interface AffiliateStoreWithUrl extends AffiliateStore {
  affiliate_url: string;
  is_exclusive: boolean;
  regional_score: number;
}

export interface ProductAffiliateStoresResponse {
  product_id: number;
  stores: AffiliateStoreWithUrl[];
  user_region: string;
  total_stores: number;
}

export interface ProductAffiliateUrlsResponse {
  product_id: number;
  affiliate_urls: Array<{
    store: AffiliateStore;
    affiliate_url: string;
    is_exclusive: boolean;
    regional_score: number;
  }>;
  user_region: string;
}



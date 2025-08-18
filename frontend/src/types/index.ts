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
  build_quality: string;
  sound_quality: string;
  value_for_money: string;
  versatility: string;
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
  ai_content?: ComprehensiveAIContent;
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



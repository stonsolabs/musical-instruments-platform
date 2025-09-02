// API configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export const getApiBaseUrl = (): string => {
  return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
};

// Get the base URL for server-side requests
export const getServerBaseUrl = (): string => {
  return process.env.VERCEL_URL 
    ? `https://${process.env.VERCEL_URL}` 
    : process.env.NEXT_PUBLIC_DOMAIN || 'http://localhost:3000';
};

// API client for client-side calls (no API key exposed)
export const apiClient = {
  async fetch(endpoint: string, options: RequestInit = {}) {
    const response = await fetch(`/api/proxy${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return response.json();
  },

  async get(endpoint: string) {
    return this.fetch(endpoint, { method: 'GET' });
  },

  async post(endpoint: string, data?: any) {
    return this.fetch(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  },

  async put(endpoint: string, data?: any) {
    return this.fetch(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  },

  async delete(endpoint: string) {
    return this.fetch(endpoint, { method: 'DELETE' });
  },

  // Search autocomplete functionality (previously duplicated across components)
  async searchAutocomplete(query: string, limit: number = 8) {
    if (typeof window === 'undefined') {
      return { results: [] };
    }
    
    try {
      const response = await fetch(`/api/proxy/search/autocomplete?q=${encodeURIComponent(query)}&limit=${limit}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Autocomplete API call failed:', error);
      return { results: [] };
    }
  },

  // Product search functionality
  async searchProducts(params: Record<string, any>) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        searchParams.append(key, String(value));
      }
    });
    
    return this.get(`/products?${searchParams.toString()}`);
  },

  // Get single product
  async getProduct(productId: string) {
    return this.get(`/products/${productId}`);
  },

  // Compare products - updated to match backend implementation
  async compareProducts(productIds: number[]) {
    return this.post(`/compare`, { product_ids: productIds });
  },

  // Get affiliate stores
  async getAffiliateStores(filters?: Record<string, any>) {
    const searchParams = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          searchParams.append(key, String(value));
        }
      });
    }
    return this.get(`/affiliate-stores?${searchParams.toString()}`);
  },

  // Get affiliate store by ID
  async getAffiliateStore(storeId: number) {
    return this.get(`/affiliate-stores/${storeId}`);
  },

  // Track product view
  async trackProductView(productId: number) {
    return this.post(`/trending/track/view/${productId}`);
  },

  // Track comparison (temporarily disabled to fix comparison page)
  async trackComparison(productIds: number[]) {
    if (productIds.length < 2) {
      console.warn('Comparison tracking needs at least 2 products, skipping...');
      return Promise.resolve(); // Don't fail if we don't have enough products
    }
    
    // TODO: Fix endpoint URL and re-enable tracking
    console.log('🔍 Comparison tracking disabled temporarily - products:', productIds);
    return Promise.resolve(); // Return success without actually tracking
  },

  // Get trending instruments
  async getTrendingInstruments(limit?: number, categoryId?: number) {
    const searchParams = new URLSearchParams();
    if (limit) searchParams.append('limit', String(limit));
    if (categoryId) searchParams.append('category_id', String(categoryId));
    return this.get(`/trending/instruments?${searchParams.toString()}`);
  },

  // Get trending comparisons
  async getTrendingComparisons(limit?: number) {
    const searchParams = new URLSearchParams();
    if (limit) searchParams.append('limit', String(limit));
    return this.get(`/trending/comparisons?${searchParams.toString()}`);
  },

  // Get trending by category
  async getTrendingByCategory(categoryId: number, limit?: number) {
    const searchParams = new URLSearchParams();
    if (limit) searchParams.append('limit', String(limit));
    return this.get(`/trending/by-category?category_id=${categoryId}&${searchParams.toString()}`);
  },

  // Get product affiliate stores
  async getProductAffiliateStores(productId: number, userRegion?: string) {
    const searchParams = new URLSearchParams();
    if (userRegion) searchParams.append('user_region', userRegion);
    return this.post(`/products/${productId}/affiliate-stores`, { user_region: userRegion });
  },

  // Get affiliate URLs for product
  async getProductAffiliateUrls(productId: number, userRegion?: string) {
    const searchParams = new URLSearchParams();
    if (userRegion) searchParams.append('user_region', userRegion);
    return this.get(`/products/${productId}/affiliate-urls?${searchParams.toString()}`);
  },

  // Vote on a product
  async voteOnProduct(productId: number, voteType: 'up' | 'down') {
    return this.post(`/voting/products/${productId}/vote`, { vote_type: voteType });
  },

  // Get product vote stats
  async getProductVoteStats(productId: number) {
    return this.get(`/voting/products/${productId}/stats`);
  },

  // Get most voted products
  async getMostVotedProducts(limit?: number, sortBy?: 'vote_score' | 'total_votes' | 'thumbs_up_count') {
    const searchParams = new URLSearchParams();
    if (limit) searchParams.append('limit', String(limit));
    if (sortBy) searchParams.append('sort_by', sortBy);
    return this.get(`/voting/products/most-voted?${searchParams.toString()}`);
  }
};

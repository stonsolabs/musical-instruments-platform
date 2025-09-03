// Server-side API configuration
const getServerApiUrl = (): string => {
  return process.env.SERVER_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
};

// Server-side API client for direct backend calls
export const serverApi = {
  async fetch(endpoint: string, options: RequestInit = {}) {
    const apiUrl = getServerApiUrl();
    const url = `${apiUrl}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': process.env.API_KEY || '',
        ...options.headers,
      },
      // Cache for 5 minutes for better performance
      next: { revalidate: 300 },
    });
    
    if (!response.ok) {
      console.error(`Server API error: ${response.status} ${response.statusText} for ${url}`);
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

  // Get trending products for homepage
  async getTrendingProducts(limit: number = 12) {
    try {
      return await this.get(`/trending/instruments?limit=${limit}`);
    } catch (error) {
      console.error('Failed to fetch trending products:', error);
      return { products: [] };
    }
  },

  // Get most voted products
  async getMostVotedProducts(limit: number = 12) {
    try {
      return await this.get(`/voting/products/most-voted?limit=${limit}&sort_by=vote_score`);
    } catch (error) {
      console.error('Failed to fetch most voted products:', error);
      return { products: [] };
    }
  },

  // Get products by category
  async getProductsByCategory(categoryId: number, limit: number = 12) {
    try {
      return await this.get(`/products?category_id=${categoryId}&limit=${limit}`);
    } catch (error) {
      console.error('Failed to fetch products by category:', error);
      return { products: [] };
    }
  },

  // Get single product
  async getProduct(productSlug: string) {
    try {
      return await this.get(`/products/${productSlug}`);
    } catch (error) {
      console.error('Failed to fetch product:', error);
      return null;
    }
  },

  // Search products
  async searchProducts(params: Record<string, any>) {
    try {
      const searchParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          searchParams.append(key, String(value));
        }
      });
      return await this.get(`/products?${searchParams.toString()}`);
    } catch (error) {
      console.error('Failed to search products:', error);
      return { products: [], total: 0 };
    }
  },

  // Compare products
  async compareProducts(productIds: number[]) {
    try {
      return await this.post('/compare', productIds);
    } catch (error) {
      console.error('Failed to compare products:', error);
      return { products: [], comparison: null };
    }
  },

  // Get categories
  async getCategories() {
    try {
      return await this.get('/categories');
    } catch (error) {
      console.error('Failed to fetch categories:', error);
      return { categories: [] };
    }
  },

  // Get brands
  async getBrands() {
    try {
      return await this.get('/brands');
    } catch (error) {
      console.error('Failed to fetch brands:', error);
      return { brands: [] };
    }
  }
};
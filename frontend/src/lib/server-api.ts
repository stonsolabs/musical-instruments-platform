// Server-side API configuration
const getServerApiUrl = (): string => {
  return process.env.SERVER_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
};

const getApiKey = (): string => {
  return process.env.API_KEY || process.env.NEXT_PUBLIC_API_KEY || '';
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
        'X-API-Key': getApiKey(),
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

  // Get trending products for homepage (using correct backend endpoint)
  async getTrendingProducts(limit: number = 12) {
    try {
      const response = await this.get(`/api/v1/trending/instruments?limit=${limit}`);
      // Backend returns {trending_instruments: [...], total: X}
      // Convert to format expected by frontend: {products: [...]}
      return {
        products: response.trending_instruments || [],
        total: response.total || 0
      };
    } catch (error) {
      console.error('Failed to fetch trending products:', error);
      return { products: [] };
    }
  },

  // Get most voted products (using correct backend endpoint)
  async getMostVotedProducts(limit: number = 12) {
    try {
      return await this.get(`/api/v1/products?sort_by=rating&limit=${limit}`);
    } catch (error) {
      console.error('Failed to fetch most voted products:', error);
      return { products: [] };
    }
  },

  // Get products by category (using correct backend endpoint)
  async getProductsByCategory(categoryId: number, limit: number = 12) {
    try {
      return await this.get(`/api/v1/products?category_id=${categoryId}&limit=${limit}`);
    } catch (error) {
      console.error('Failed to fetch products by category:', error);
      return { products: [] };
    }
  },

  // Get single product (using correct backend endpoint)
  async getProduct(productSlug: string) {
    try {
      return await this.get(`/api/v1/products/${productSlug}`);
    } catch (error) {
      console.error('Failed to fetch product:', error);
      return null;
    }
  },

  // Search products (using correct backend endpoint)
  async searchProducts(params: Record<string, any>) {
    try {
      const searchParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          searchParams.append(key, String(value));
        }
      });
      return await this.get(`/api/v1/products?${searchParams.toString()}`);
    } catch (error) {
      console.error('Failed to search products:', error);
      return { products: [], total: 0 };
    }
  },

  // Compare products by slugs (using correct backend endpoint)
  async compareProductsBySlugs(slugs: string[]) {
    try {
      const slugsParam = slugs.join(',');
      return await this.get(`/api/v1/products?slugs=${slugsParam}&limit=100`);
    } catch (error) {
      console.error('Failed to compare products:', error);
      return { products: [] };
    }
  },

  // Compare products by IDs (using correct backend endpoint)
  async compareProducts(productIds: number[]) {
    try {
      return await this.post('/api/v1/compare', productIds);
    } catch (error) {
      console.error('Failed to compare products:', error);
      return { products: [], comparison: null };
    }
  },

  // Get categories (using correct backend endpoint)
  async getCategories() {
    try {
      return await this.get('/api/v1/categories');
    } catch (error) {
      console.error('Failed to fetch categories:', error);
      return { categories: [] };
    }
  },

  // Get brands (using correct backend endpoint)
  async getBrands() {
    try {
      return await this.get('/api/v1/brands');
    } catch (error) {
      console.error('Failed to fetch brands:', error);
      return { brands: [] };
    }
  }
};
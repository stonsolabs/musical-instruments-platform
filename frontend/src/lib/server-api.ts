// Simple, direct server-side API client - no proxy needed!
const getApiConfig = () => {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  const apiKey = process.env.API_KEY;
  
  if (!baseUrl) {
    throw new Error('NEXT_PUBLIC_API_BASE_URL environment variable is required');
  }
  
  if (!apiKey) {
    throw new Error('API_KEY environment variable is required');
  }
  
  return { baseUrl, apiKey };
};

export const serverApi = {
  async fetch(endpoint: string, options: RequestInit = {}) {
    const { baseUrl, apiKey } = getApiConfig();
    const url = `${baseUrl}/api/v1${endpoint}`;

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'X-API-Key': apiKey,
          'Content-Type': 'application/json',
          ...(options.headers as Record<string, string>),
        },
        next: { revalidate: 300 }, // Built-in Next.js caching
      });

      if (!response.ok) {
        console.error('Direct API fetch failed', { url, status: response.status });
        throw new Error(`HTTP ${response.status}`);
      }

      return response.json();
    } catch (err) {
      console.error('Direct API fetch error', { url, err });
      throw err;
    }
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

  async getTrendingProducts(limit: number = 12) {
    try {
      const response = await this.get(`/trending/instruments?limit=${limit}`);
      return {
        products: response.trending_instruments || [],
        total: response.total || 0,
      };
    } catch (error) {
      console.error('Failed to fetch trending products:', error);
      return { products: [] };
    }
  },

  async getMostVotedProducts(limit: number = 12) {
    try {
      return await this.get(`/products?sort_by=rating&limit=${limit}`);
    } catch (error) {
      console.error('Failed to fetch most voted products:', error);
      return { products: [] };
    }
  },

  async getProductsByCategory(categoryId: number, limit: number = 12) {
    try {
      return await this.get(`/products?category_id=${categoryId}&limit=${limit}`);
    } catch (error) {
      console.error('Failed to fetch products by category:', error);
      return { products: [] };
    }
  },

  async getProduct(productSlug: string) {
    try {
      const result = await this.get(`/products?slugs=${productSlug}&limit=1`);
      return result.products && result.products.length > 0 ? result.products[0] : null;
    } catch (error) {
      console.error('Failed to fetch product:', error);
      return null;
    }
  },

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

  async compareProductsBySlugs(slugs: string[]) {
    try {
      const slugsParam = slugs.join(',');
      return await this.get(`/products?slugs=${slugsParam}&limit=100`);
    } catch (error) {
      console.error('Failed to compare products:', error);
      return { products: [] };
    }
  },

  async compareProducts(productIds: number[]) {
    try {
      return await this.post('/compare', productIds);
    } catch (error) {
      console.error('Failed to compare products:', error);
      return { products: [], comparison: null };
    }
  },

  async getCategories() {
    try {
      return await this.get('/categories');
    } catch (error) {
      console.error('Failed to fetch categories:', error);
      return { categories: [] };
    }
  },

  async getBrands() {
    try {
      return await this.get('/brands');
    } catch (error) {
      console.error('Failed to fetch brands:', error);
      return { brands: [] };
    }
  },
};
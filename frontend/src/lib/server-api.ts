// Simplified server-side API client using the working proxy
export const serverApi = {
  async fetch(endpoint: string, options: RequestInit = {}) {
    // For development, we need to avoid circular calls to localhost
    const isDev = process.env.NODE_ENV === 'development';
    
    let baseUrl: string;
    if (isDev) {
      // In development, call the production API directly to avoid circular calls
      baseUrl = 'https://www.getyourmusicgear.com';
    } else {
      // In production, use the proxy route
      const domain = process.env.VERCEL_URL || process.env.NEXT_PUBLIC_DOMAIN || 'www.getyourmusicgear.com';
      baseUrl = domain.startsWith('http') ? domain : `https://${domain}`;
    }
    
    const url = `${baseUrl}/api/proxy${endpoint}`;

    try {
      console.log('🔍 Server API: Fetching', { url, endpoint });
      
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...(options.headers as Record<string, string>),
        },
        next: { revalidate: 300 }, // Built-in Next.js caching
      });

      console.log('📡 Server API response:', { 
        url, 
        status: response.status, 
        ok: response.ok,
        headers: Object.fromEntries(response.headers.entries())
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Server API fetch failed', { url, status: response.status, errorText });
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log('✅ Server API success:', { 
        url, 
        dataType: typeof data,
        hasProducts: !!data.products,
        productCount: data.products?.length || 0
      });
      
      return data;
    } catch (err) {
      console.error('🚨 Server API fetch error', { url, endpoint, err });
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
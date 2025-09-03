// Server-side API configuration
const getServerApiUrl = (): string => {
  // For server-side calls, we need to determine the base URL
  // In production, use the domain; in development, use localhost
  let baseUrl: string;
  
  if (process.env.VERCEL_URL) {
    // VERCEL_URL doesn't include protocol, add https://
    baseUrl = `https://${process.env.VERCEL_URL}`;
  } else if (process.env.NEXT_PUBLIC_DOMAIN) {
    // NEXT_PUBLIC_DOMAIN might already include protocol
    baseUrl = process.env.NEXT_PUBLIC_DOMAIN.startsWith('http') 
      ? process.env.NEXT_PUBLIC_DOMAIN 
      : `https://${process.env.NEXT_PUBLIC_DOMAIN}`;
  } else {
    // Development fallback
    baseUrl = 'http://localhost:3000';
  }
    
  const proxyUrl = `${baseUrl}/api/proxy`;
  
  console.log('🌐 Server API URL (USING INTERNAL PROXY):', proxyUrl, {
    VERCEL_URL: process.env.VERCEL_URL,
    NEXT_PUBLIC_DOMAIN: process.env.NEXT_PUBLIC_DOMAIN,
    NODE_ENV: process.env.NODE_ENV,
    finalBaseUrl: baseUrl
  });
  
  return proxyUrl;
};

const getApiKey = (): string => {
  return process.env.API_KEY || process.env.NEXT_PUBLIC_API_KEY || '';
};

// Server-side API client for direct backend calls
export const serverApi = {
  async fetch(endpoint: string, options: RequestInit = {}) {
    const apiUrl = getServerApiUrl();
    const url = `${apiUrl}${endpoint}`;
    const isUsingProxy = apiUrl.includes('/api/proxy');
    
    console.log('🌐 Server API call:', {
      endpoint,
      url,
      isUsingProxy,
      environment: process.env.NODE_ENV
    });
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...options.headers as Record<string, string>,
    };
    
    // Only add API key if not using proxy (proxy handles authentication)
    if (!isUsingProxy) {
      headers['X-API-Key'] = getApiKey();
    }
    
    const response = await fetch(url, {
      ...options,
      headers,
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
      const response = await this.get(`/trending/instruments?limit=${limit}`);
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
      return await this.get(`/products?sort_by=rating&limit=${limit}`);
    } catch (error) {
      console.error('Failed to fetch most voted products:', error);
      return { products: [] };
    }
  },

  // Get products by category (using correct backend endpoint)
  async getProductsByCategory(categoryId: number, limit: number = 12) {
    try {
      return await this.get(`/products?category_id=${categoryId}&limit=${limit}`);
    } catch (error) {
      console.error('Failed to fetch products by category:', error);
      return { products: [] };
    }
  },

  // Get single product by slug (using search endpoint with slugs filter)
  async getProduct(productSlug: string) {
    try {
      const result = await this.get(`/products?slugs=${productSlug}&limit=1`);
      return result.products && result.products.length > 0 ? result.products[0] : null;
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
      return await this.get(`/products?${searchParams.toString()}`);
    } catch (error) {
      console.error('Failed to search products:', error);
      return { products: [], total: 0 };
    }
  },

  // Compare products by slugs (using correct backend endpoint)
  async compareProductsBySlugs(slugs: string[]) {
    try {
      const slugsParam = slugs.join(',');
      return await this.get(`/products?slugs=${slugsParam}&limit=100`);
    } catch (error) {
      console.error('Failed to compare products:', error);
      return { products: [] };
    }
  },

  // Compare products by IDs (using correct backend endpoint)
  async compareProducts(productIds: number[]) {
    try {
      return await this.post('/compare', productIds);
    } catch (error) {
      console.error('Failed to compare products:', error);
      return { products: [], comparison: null };
    }
  },

  // Get categories (using correct backend endpoint)
  async getCategories() {
    try {
      return await this.get('/categories');
    } catch (error) {
      console.error('Failed to fetch categories:', error);
      return { categories: [] };
    }
  },

  // Get brands (using correct backend endpoint)
  async getBrands() {
    try {
      return await this.get('/brands');
    } catch (error) {
      console.error('Failed to fetch brands:', error);
      return { brands: [] };
    }
  }
};
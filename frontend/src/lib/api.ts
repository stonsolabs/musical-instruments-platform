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

  // Compare products
  async compareProducts(productSlugs: string[]) {
    return this.get(`/compare?products=${productSlugs.join(',')}`);
  }
};

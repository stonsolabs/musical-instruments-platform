import { Product, ProductComparison, SearchResult, TrendingProduct, AffiliateStore, AffiliateStoreWithUrl, Category, Brand } from '@/types';

const PROXY_BASE = '/api/proxy/v1';

function abs(path: string): string {
  if (typeof window !== 'undefined') return path; // client can use relative
  
  // For server-side calls, go directly to Azure backend if it's a proxy path
  if (path.startsWith('/api/proxy/v1/')) {
    const azureBase = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';
    return azureBase + '/api/v1' + path.replace('/api/proxy/v1', '');
  }
  
  const origin = process.env.NEXT_PUBLIC_APP_ORIGIN
    || (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : 'http://localhost:3000');
  return origin.replace(/\/$/, '') + path;
}

async function apiFetch(pathWithQuery: string, init?: RequestInit) {
  const url = abs(pathWithQuery);
  console.log(`[API DEBUG] Server-side fetch URL: ${url}`);
  return fetch(url, init);
}

const getHeaders = () => {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  // For server-side calls, include the API key directly
  if (typeof window === 'undefined' && process.env.API_KEY) {
    headers['X-API-Key'] = process.env.API_KEY;
  }
  
  return headers;
};

export async function fetchProducts(params: {
  page?: number;
  per_page?: number; // alias for limit
  limit?: number;
  category?: string; // slug
  brand?: string; // slug
  search?: string; // alias for query
  query?: string;
  slugs?: string[]; // optional for exact slug filtering
  sort_by?: 'name' | 'rating' | 'popularity' | 'price';
  sort_order?: 'asc' | 'desc';
}): Promise<SearchResult> {
  const searchParams = new URLSearchParams();
  if (params.page) searchParams.append('page', String(params.page));
  const limit = params.limit ?? params.per_page;
  if (limit) searchParams.append('limit', String(limit));
  if (params.category) searchParams.append('category', params.category);
  if (params.brand) searchParams.append('brand', params.brand);
  const query = params.query ?? params.search;
  if (query) searchParams.append('query', query);
  if (params.slugs && params.slugs.length) searchParams.append('slugs', params.slugs.join(','));
  if (params.sort_by) searchParams.append('sort_by', params.sort_by);
  if (params.sort_order) searchParams.append('sort_order', params.sort_order);

  const response = await apiFetch(`${PROXY_BASE}/products?${searchParams.toString()}`, {
    headers: getHeaders(),
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch products: ${response.statusText}`);
  }
 
  const data = await response.json();
  // Normalize backend shape to SearchResult
  const pagination = data.pagination || {};
  return {
    products: data.products || [],
    total: pagination.total ?? data.total ?? (data.products ? data.products.length : 0),
    page: pagination.page ?? data.page ?? 1,
    per_page: pagination.limit ?? data.per_page ?? params.limit ?? params.per_page ?? 10,
    total_pages: pagination.pages ?? data.total_pages ?? Math.ceil((pagination.total ?? data.total ?? 0) / (pagination.limit ?? data.per_page ?? params.limit ?? params.per_page ?? 10)),
  } as SearchResult;
}

export async function fetchProduct(slugOrId: string | number): Promise<Product> {
  // Prefer fetching by slug when a non-numeric value is provided, otherwise by id
  const isNumericId = typeof slugOrId === 'number' || /^\d+$/.test(String(slugOrId));

  try {
    if (!isNumericId) {
      // Try fetch by slugs param first (exact match support)
      const url = `${PROXY_BASE}/products?slugs=${encodeURIComponent(String(slugOrId))}`;
      const res = await apiFetch(url, { headers: getHeaders() });
      if (res.ok) {
        const data: SearchResult = await res.json();
        const exact = data.products?.find(p => p.slug === String(slugOrId));
        if (exact) return exact;
        if (data.products && data.products.length > 0) return data.products[0];
      }
      // If query didn’t return a product, fall through to id endpoint in case API supports slug there in future
      // Fallback to search by slug token
      const searchRes = await apiFetch(`${PROXY_BASE}/search/autocomplete?q=${encodeURIComponent(String(slugOrId))}&limit=20`, { headers: getHeaders() });
      if (searchRes.ok) {
        const results: any = await searchRes.json();
        const list = Array.isArray(results?.results) ? results.results : [];
        const match = list.find((p: any) => p.slug === String(slugOrId));
        if (match) return match;
      }
    }

    const idPath = isNumericId ? String(slugOrId) : String(slugOrId);
    const resById = await apiFetch(`${PROXY_BASE}/products/${idPath}`, { headers: getHeaders() });
    if (!resById.ok) {
      const errorText = await resById.text();
      console.error('API Error:', resById.status, resById.statusText, errorText);
      throw new Error(`Failed to fetch product: ${resById.statusText}`);
    }
    return resById.json();
  } catch (err) {
    console.error('Error fetching product:', err);
    throw err;
  }
}

export async function fetchProductComparison(productIds: number[]): Promise<ProductComparison> {
  const response = await apiFetch(`${PROXY_BASE}/compare`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(productIds),
  });
  
  if (!response.ok) {
    throw new Error(`Failed to compare products: ${response.statusText}`);
  }

  return response.json();
}

export async function fetchTrendingProducts(limit: number = 10): Promise<TrendingProduct[]> {
  try {
    // First try the dedicated trending endpoint
    const response = await apiFetch(`${PROXY_BASE}/trending/instruments?limit=${limit}`, {
      headers: getHeaders(),
    });
    
    if (response.ok) {
      const data = await response.json();
      const trendingInstruments = data.trending_instruments || [];
      
      // If we have trending data, return it
      if (trendingInstruments.length > 0) {
        return trendingInstruments;
      }
    }
  } catch (error) {
    console.warn('Trending endpoint failed, falling back to products:', error);
  }

  // Fallback to products endpoint with high ratings
  const response = await apiFetch(`${PROXY_BASE}/products?limit=${limit}&sort_by=rating&sort_order=desc`, {
    headers: getHeaders(),
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch trending products: ${response.statusText}`);
  }

  const data: SearchResult = await response.json();
  
  // Convert products to trending products format
  return data.products.map(product => ({
    product,
    trending_score: Math.random() * 10, // Mock trending score
    price_change: Math.random() * 20 - 10, // Mock price change
    popularity_increase: Math.random() * 100 // Mock popularity increase
  }));
}

export async function fetchCategories(): Promise<Category[]> {
  const response = await apiFetch(`${PROXY_BASE}/categories`, {
    headers: getHeaders(),
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch categories: ${response.statusText}`);
  }

  return response.json();
}

export async function fetchBrands(): Promise<Brand[]> {
  const response = await apiFetch(`${PROXY_BASE}/brands`, {
    headers: getHeaders(),
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch brands: ${response.statusText}`);
  }

  return response.json();
}

export async function fetchAffiliateStores(): Promise<AffiliateStore[]> {
  const response = await apiFetch(`${PROXY_BASE}/affiliate-stores`, {
    headers: getHeaders(),
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch affiliate stores: ${response.statusText}`);
  }

  return response.json();
}

export async function searchProducts(query: string, limit: number = 10): Promise<Product[]> {
  // Use autocomplete endpoint; it returns { query, results, total }
  const response = await apiFetch(`${PROXY_BASE}/search/autocomplete?q=${encodeURIComponent(query)}&limit=${limit}`, {
    headers: getHeaders(),
  });
  if (!response.ok) {
    throw new Error(`Failed to search products: ${response.statusText}`);
  }
  const data = await response.json();
  return data.results || [];
}

export async function fetchProductAffiliateStores(productId: number, storeLinks?: Record<string, { product_url: string }>): Promise<{ affiliate_stores: AffiliateStoreWithUrl[] }> {
  const response = await apiFetch(`${PROXY_BASE}/products/${productId}/affiliate-stores`, {
    method: storeLinks ? 'POST' : 'GET',
    headers: getHeaders(),
    body: storeLinks ? JSON.stringify(storeLinks) : undefined,
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch affiliate stores: ${response.statusText}`);
  }

  return response.json();
}

export async function generateAffiliateUrls(productId: number): Promise<{ affiliate_urls: Array<{ store: AffiliateStore; affiliate_url: string; original_url?: string }> }> {
  const response = await apiFetch(`${PROXY_BASE}/products/${productId}/affiliate-urls`, {
    headers: getHeaders(),
  });
  
  if (!response.ok) {
    throw new Error(`Failed to generate affiliate URLs: ${response.statusText}`);
  }

  return response.json();
}

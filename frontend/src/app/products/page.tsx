'use client';

import React, { useCallback, useEffect, useMemo, useState, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { Product, SearchResponse, Category, Brand } from '../../types';

// Inline utility functions
const formatPrice = (price: number, currency: string = 'EUR'): string => {
  try {
    return new Intl.NumberFormat('en-GB', { style: 'currency', currency }).format(price);
  } catch {
    return `${currency} ${price.toFixed(2)}`;
  }
};

const formatRating = (rating: number): string => {
  return Number.isFinite(rating) ? rating.toFixed(1) : '0.0';
};

// Inline API client
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = {
  async searchProducts(params: any): Promise<SearchResponse> {
    if (typeof window === 'undefined') {
      return { products: [], pagination: { page: 1, limit: 20, total: 0, pages: 0 } };
    }
    
    const sp = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== '') sp.append(k, String(v));
    });
    
    const response = await fetch(`${API_BASE_URL}/api/v1/products?${sp.toString()}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  },

  async getCategories(): Promise<Category[]> {
    if (typeof window === 'undefined') return [];
    
    const response = await fetch(`${API_BASE_URL}/api/v1/categories`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  },

  async getBrands(): Promise<Brand[]> {
    if (typeof window === 'undefined') return [];
    
    const response = await fetch(`${API_BASE_URL}/api/v1/brands`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  }
};

function ProductsPageContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [brands, setBrands] = useState<Brand[]>([]);
  const [pagination, setPagination] = useState<SearchResponse['pagination']>({ page: 1, limit: 20, total: 0, pages: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedProducts, setSelectedProducts] = useState<number[]>([]);
  const [searchQuery, setSearchQuery] = useState('');

  // Get current filters from URL
  const currentFilters = useMemo(() => ({
    query: searchParams.get('query') || '',
    category: searchParams.get('category') || '',
    brand: searchParams.get('brand') || '',
    price_min: searchParams.get('price_min') || '',
    price_max: searchParams.get('price_max') || '',
    sort_by: searchParams.get('sort_by') || 'name',
    page: parseInt(searchParams.get('page') || '1'),
  }), [searchParams]);

  const loadProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.searchProducts({
        ...currentFilters,
        limit: 20,
      });
      setProducts(data.products);
      setPagination(data.pagination);
    } catch (e) {
      setError('Failed to load products.');
    } finally {
      setLoading(false);
    }
  }, [currentFilters]);

  const loadCategoriesAndBrands = useCallback(async () => {
    try {
      const [categoriesData, brandsData] = await Promise.all([
        apiClient.getCategories(),
        apiClient.getBrands()
      ]);
      setCategories(categoriesData);
      setBrands(brandsData);
    } catch (e) {
      console.error('Failed to load categories/brands:', e);
    }
  }, []);

  useEffect(() => {
    loadProducts();
    loadCategoriesAndBrands();
  }, [loadProducts, loadCategoriesAndBrands]);

  // Debounced search
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchQuery !== currentFilters.query) {
        updateFilters({ query: searchQuery });
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [searchQuery, currentFilters.query]);

  const updateFilters = (newFilters: Partial<typeof currentFilters>) => {
    const params = new URLSearchParams(searchParams.toString());
    Object.entries(newFilters).forEach(([key, value]) => {
      if (value) {
        params.set(key, value.toString());
      } else {
        params.delete(key);
      }
    });
    params.set('page', '1'); // Reset to first page
    router.push(`/products?${params.toString()}`);
  };

  const toggleProductSelection = (productId: number) => {
    setSelectedProducts(prev => 
      prev.includes(productId) 
        ? prev.filter(id => id !== productId)
        : [...prev, productId]
    );
  };

  const compareSelected = () => {
    if (selectedProducts.length >= 2) {
      router.push(`/compare?ids=${selectedProducts.join(',')}`);
    }
  };

  // Check if comparing across different categories
  const selectedProductCategories = products
    .filter(p => selectedProducts.includes(p.id))
    .map(p => p.category.name);
  const hasDifferentCategories = new Set(selectedProductCategories).size > 1;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Ad Space - Top */}
      <section className="py-4 bg-white border-b">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-orange-400 to-red-500 rounded-lg p-4 text-white text-center">
            <p className="text-sm">🎵 Find the best deals on musical instruments</p>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="mb-6">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
            <li>/</li>
            <li className="text-gray-900">Products</li>
          </ol>
        </nav>

        <div className="grid lg:grid-cols-4 gap-8">
          {/* Sidebar Filters */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sticky top-24">
              <h2 className="text-lg font-semibold text-gray-900 mb-6">Filters</h2>
              
              {/* Search */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
                <input
                  type="text"
                  placeholder="Search instruments..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Categories */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                <select
                  value={currentFilters.category}
                  onChange={(e) => updateFilters({ category: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Categories</option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.slug}>
                      {category.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Brands */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Brand</label>
                <select
                  value={currentFilters.brand}
                  onChange={(e) => updateFilters({ brand: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Brands</option>
                  {brands.map((brand) => (
                    <option key={brand.id} value={brand.slug}>
                      {brand.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Price Range */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Price Range</label>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    placeholder="Min"
                    value={currentFilters.price_min}
                    onChange={(e) => updateFilters({ price_min: e.target.value })}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <input
                    type="number"
                    placeholder="Max"
                    value={currentFilters.price_max}
                    onChange={(e) => updateFilters({ price_max: e.target.value })}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Sort */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
                <select
                  value={currentFilters.sort_by}
                  onChange={(e) => updateFilters({ sort_by: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="name">Name</option>
                  <option value="price">Price</option>
                  <option value="rating">Rating</option>
                  <option value="popularity">Popularity</option>
                </select>
              </div>

              {/* Clear Filters */}
              <button
                onClick={() => router.push('/products')}
                className="w-full py-2 px-4 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Clear Filters
              </button>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Musical Instruments</h1>
                <p className="text-gray-600 mt-1">
                  {pagination.total} products found
                </p>
              </div>
              
              {/* Compare Selected */}
              {selectedProducts.length > 0 && (
                <button
                  onClick={compareSelected}
                  disabled={selectedProducts.length < 2}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400"
                >
                  Compare ({selectedProducts.length})
                </button>
              )}
            </div>

            {/* Category Disclaimer */}
            {hasDifferentCategories && selectedProducts.length >= 2 && (
              <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-start">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-yellow-800">
                      Cross-Category Comparison
                    </h3>
                    <div className="mt-2 text-sm text-yellow-700">
                      <p>
                        You're comparing products across different categories ({selectedProductCategories.join(', ')}), 
                        which could give unexpected results. Consider comparing products within the same category for more accurate comparisons.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Ad Space - Middle */}
            <section className="mb-6">
              <div className="bg-gradient-to-r from-green-400 to-blue-500 rounded-lg p-4 text-white text-center">
                <p className="text-sm">🎵 Free shipping on orders over €199</p>
              </div>
            </section>

            {/* Products Grid */}
            {loading ? (
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
                    <div className="h-48 bg-gray-200 rounded-lg mb-4"></div>
                    <div className="h-4 bg-gray-200 rounded mb-2"></div>
                    <div className="h-6 bg-gray-200 rounded mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded"></div>
                  </div>
                ))}
              </div>
            ) : error ? (
              <div className="text-center py-12">
                <div className="text-red-600 mb-4">⚠️ {error}</div>
                <button 
                  onClick={() => loadProducts()} 
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Try Again
                </button>
              </div>
            ) : products.length > 0 ? (
              <>
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {products.map((product) => (
                    <div key={product.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                      <div className="relative">
                        <div className="aspect-square bg-gray-200 rounded-lg mb-4 flex items-center justify-center">
                          <span className="text-gray-400 text-4xl">🎸</span>
                        </div>
                        <button
                          onClick={() => toggleProductSelection(product.id)}
                          className={`absolute top-2 right-2 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                            selectedProducts.includes(product.id)
                              ? 'bg-blue-600 border-blue-600 text-white'
                              : 'bg-white border-gray-300 text-gray-400 hover:border-blue-600'
                          }`}
                        >
                          {selectedProducts.includes(product.id) && (
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          )}
                        </button>
                      </div>
                      
                      <div className="space-y-3">
                        <div>
                          <p className="text-sm text-gray-600 mb-1">{product.brand.name}</p>
                          <h3 className="font-semibold text-gray-900 line-clamp-2 mb-2">{product.name}</h3>
                        </div>

                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            {product.avg_rating > 0 && (
                              <>
                                <span className="text-yellow-500">★</span>
                                <span className="text-sm font-medium">{formatRating(product.avg_rating)}</span>
                                <span className="text-sm text-gray-500">({product.review_count})</span>
                              </>
                            )}
                          </div>
                          <span className="text-sm text-gray-600">{product.category.name}</span>
                        </div>

                        <div className="flex items-center justify-between">
                          <span className="text-lg font-bold text-green-600">
                            {product.best_price ? formatPrice(product.best_price.price, product.best_price.currency) : 
                             product.msrp_price ? formatPrice(product.msrp_price) : '—'}
                          </span>
                        </div>

                        <div className="flex gap-2">
                          <Link 
                            href={`/products/${product.slug}-${product.id}`}
                            className="flex-1 text-center bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm"
                          >
                            View Details
                          </Link>
                          <button 
                            onClick={() => toggleProductSelection(product.id)}
                            className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm"
                          >
                            {selectedProducts.includes(product.id) ? 'Remove' : 'Add'}
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Pagination */}
                {pagination.pages > 1 && (
                  <div className="mt-8 flex justify-center">
                    <nav className="flex items-center space-x-2">
                      {pagination.page > 1 && (
                        <button
                          onClick={() => updateFilters({ page: pagination.page - 1 })}
                          className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                        >
                          Previous
                        </button>
                      )}
                      
                      {Array.from({ length: Math.min(5, pagination.pages) }, (_, i) => {
                        const page = i + 1;
                        return (
                          <button
                            key={page}
                            onClick={() => updateFilters({ page })}
                            className={`px-3 py-2 border rounded-lg transition-colors ${
                              page === pagination.page
                                ? 'bg-blue-600 text-white border-blue-600'
                                : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                            }`}
                          >
                            {page}
                          </button>
                        );
                      })}
                      
                      {pagination.page < pagination.pages && (
                        <button
                          onClick={() => updateFilters({ page: pagination.page + 1 })}
                          className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                        >
                          Next
                        </button>
                      )}
                    </nav>
                  </div>
                )}
              </>
            ) : (
              <div className="text-center py-12">
                <div className="text-gray-500 mb-4">No products found matching your criteria.</div>
                <button 
                  onClick={() => router.push('/products')} 
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Clear Filters
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ProductsPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ProductsPageContent />
    </Suspense>
  );
}
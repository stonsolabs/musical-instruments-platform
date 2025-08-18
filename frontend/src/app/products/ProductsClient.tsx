'use client';

import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { Product, SearchResponse, Category, Brand } from '@/types';
import { getApiBaseUrl } from '@/lib/api';
import FloatingCompareButton from '@/components/FloatingCompareButton';
import PageLayout from '@/components/PageLayout';
import AdSidebar from '@/components/AdSidebar';
import AffiliateButton from '@/components/AffiliateButton';

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

const API_BASE_URL = getApiBaseUrl();

const apiClient = {
  async searchProducts(params: any): Promise<SearchResponse> {
    const sp = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== '') sp.append(k, String(v));
    });
    
    const response = await fetch(`/api/proxy/products?${sp.toString()}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  },
};

interface ProductsClientProps {
  initialProducts: Product[];
  initialPagination: SearchResponse['pagination'];
  categories: Category[];
  brands: Brand[];
}

export default function ProductsClient({
  initialProducts,
  initialPagination,
  categories,
  brands,
}: ProductsClientProps) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>(initialProducts);
  const [pagination, setPagination] = useState(initialPagination);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedProducts, setSelectedProducts] = useState<number[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showMobileFilters, setShowMobileFilters] = useState(false);

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

  // Set initial search query from URL
  useEffect(() => {
    setSearchQuery(currentFilters.query);
  }, [currentFilters.query]);

  const loadProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      console.log('🔍 Loading products with filters:', currentFilters);
      const data = await apiClient.searchProducts({
        ...currentFilters,
        limit: 20,
      });
      console.log('✅ Products loaded:', data.products.length, 'products');
      setProducts(data.products);
      setPagination(data.pagination);
    } catch (e) {
      setError('Failed to load products.');
      console.error('Load products error:', e);
    } finally {
      setLoading(false);
    }
  }, [currentFilters]);

  // Load products when filters change
  useEffect(() => {
    // Skip initial load since we have server-side data
    if (products.length === 0 && !loading) {
      return;
    }
    
    // Check if filters have actually changed from the initial state
    const hasActiveFilters = Object.values(currentFilters).some(value => 
      value !== '' && value !== 'name' && value !== 1
    );
    
    console.log('🔍 Filter check - hasActiveFilters:', hasActiveFilters, 'currentFilters:', currentFilters);
    
    if (hasActiveFilters) {
      console.log('🔍 Filters active, loading products...');
      
      const loadProductsWithFilters = async () => {
        setLoading(true);
        setError(null);
        try {
          console.log('🔍 Loading products with filters:', currentFilters);
          const data = await apiClient.searchProducts({
            ...currentFilters,
            limit: 20,
          });
          console.log('✅ Products loaded:', data.products.length, 'products');
          setProducts(data.products);
          setPagination(data.pagination);
        } catch (e) {
          setError('Failed to load products.');
          console.error('Load products error:', e);
        } finally {
          setLoading(false);
        }
      };
      
      loadProductsWithFilters();
    }
  }, [currentFilters, products.length, loading]);

  // Debounced search
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchQuery !== currentFilters.query) {
        console.log('🔍 Search query changed:', searchQuery);
        updateFilters({ query: searchQuery });
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [searchQuery, currentFilters.query]);

  const updateFilters = (newFilters: Partial<typeof currentFilters>) => {
    const params = new URLSearchParams(searchParams.toString());
    
    // Update each filter
    Object.entries(newFilters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.set(key, value.toString());
      } else {
        params.delete(key);
      }
    });
    
    // Reset to first page when filters change
    params.set('page', '1');
    
    // Ensure we have proper defaults
    if (!params.has('limit')) params.set('limit', '20');
    if (!params.has('sort_by')) params.set('sort_by', 'name');
    
    const newUrl = `/products?${params.toString()}`;
    console.log('🔍 Updating filters:', newFilters, 'New URL:', newUrl);
    router.push(newUrl);
  };

  const toggleProductSelection = (productId: number) => {
    console.log('🔍 Toggling product selection for ID:', productId);
    setSelectedProducts(prev => {
      const newSelection = prev.includes(productId) 
        ? prev.filter(id => id !== productId)
        : [...prev, productId];
      console.log('🔍 Updated selected products:', newSelection);
      return newSelection;
    });
  };

  const compareSelected = () => {
    if (selectedProducts.length >= 1) {
      // Get the product slugs for the selected products
      const selectedProductObjects = products.filter(product => selectedProducts.includes(product.id));
      const selectedProductSlugs = selectedProductObjects.map(product => product.slug).join(',');
      
      // Debug logging
      console.log('🔍 Compare selected products:', selectedProducts);
      console.log('🔍 Selected product objects:', selectedProductObjects);
      console.log('🔍 Selected product slugs:', selectedProductSlugs);
      
      if (selectedProductSlugs.length === 0) {
        console.error('❌ No valid product slugs found for selected products');
        return;
      }
      
      // URL encode the slugs to handle special characters
      const encodedSlugs = encodeURIComponent(selectedProductSlugs);
      console.log('🔍 Encoded slugs:', encodedSlugs);
      
      const compareUrl = `/compare?products=${encodedSlugs}`;
      console.log('🔍 Navigating to compare URL:', compareUrl);
      
      // Use router.push to navigate
      router.push(compareUrl);
    } else {
      console.warn('⚠️ No products selected for comparison');
    }
  };

  // Check if comparing across different categories
  const selectedProductCategories = products
    .filter(p => selectedProducts.includes(p.id))
    .map(p => p.category.name);
  const hasDifferentCategories = new Set(selectedProductCategories).size > 1;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid lg:grid-cols-5 gap-6 xl:gap-8">
        {/* Sidebar Filters */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 lg:p-6 sticky top-24 max-h-[calc(100vh-6rem)] overflow-y-auto hidden lg:block">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 lg:mb-6">Filters</h2>
            
            {/* Search */}
            <div className="mb-4 lg:mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
              <input
                type="text"
                placeholder="Search instruments..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              />
            </div>

            {/* Categories */}
            <div className="mb-4 lg:mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
              <select
                value={currentFilters.category}
                onChange={(e) => updateFilters({ category: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
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
            <div className="mb-4 lg:mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">Brand</label>
              <select
                value={currentFilters.brand}
                onChange={(e) => updateFilters({ brand: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
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
            <div className="mb-4 lg:mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">Price Range (€)</label>
              <div className="grid grid-cols-2 gap-2">
                <input
                  type="number"
                  placeholder="Min"
                  value={currentFilters.price_min}
                  onChange={(e) => updateFilters({ price_min: e.target.value || undefined })}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                />
                <input
                  type="number"
                  placeholder="Max"
                  value={currentFilters.price_max}
                  onChange={(e) => updateFilters({ price_max: e.target.value || undefined })}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                />
              </div>
            </div>

            {/* Sort */}
            <div className="mb-4 lg:mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
              <select
                value={currentFilters.sort_by}
                onChange={(e) => updateFilters({ sort_by: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              >
                <option value="name">Name</option>
                <option value="price">Price</option>
                <option value="rating">Rating</option>
                <option value="popularity">Popularity</option>
              </select>
            </div>

            {/* Clear Filters */}
            <button
              onClick={() => {
                setSearchQuery('');
                router.push('/products');
              }}
              className="w-full py-2 px-4 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm"
            >
              Clear All Filters
            </button>
          </div>
        </div>

        {/* Mobile Filters Panel */}
        {showMobileFilters && (
          <div className="lg:hidden fixed inset-0 z-50 bg-black bg-opacity-50">
            <div className="absolute right-0 top-0 h-full w-80 bg-white shadow-xl p-6 overflow-y-auto">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
                <button
                  onClick={() => setShowMobileFilters(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              {/* Mobile Filter Content - Same as desktop but with mobile styling */}
              <div className="space-y-6">
                {/* Search */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
                  <input
                    type="text"
                    placeholder="Search instruments..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  />
                </div>

                {/* Categories */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                  <select
                    value={currentFilters.category}
                    onChange={(e) => updateFilters({ category: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
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
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Brand</label>
                  <select
                    value={currentFilters.brand}
                    onChange={(e) => updateFilters({ brand: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
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
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Price Range (€)</label>
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="number"
                      placeholder="Min"
                      value={currentFilters.price_min}
                      onChange={(e) => updateFilters({ price_min: e.target.value || undefined })}
                      className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                    />
                    <input
                      type="number"
                      placeholder="Max"
                      value={currentFilters.price_max}
                      onChange={(e) => updateFilters({ price_max: e.target.value || undefined })}
                      className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                    />
                  </div>
                </div>

                {/* Sort */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
                  <select
                    value={currentFilters.sort_by}
                    onChange={(e) => updateFilters({ sort_by: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  >
                    <option value="name">Name</option>
                    <option value="price">Price</option>
                    <option value="rating">Rating</option>
                    <option value="popularity">Popularity</option>
                  </select>
                </div>

                {/* Clear Filters */}
                <button
                  onClick={() => {
                    setSearchQuery('');
                    router.push('/products');
                    setShowMobileFilters(false);
                  }}
                  className="w-full py-2 px-4 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm"
                >
                  Clear All Filters
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="lg:col-span-3">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <p className="text-gray-600">
                {pagination.total} products found
                {Object.keys(currentFilters).some(key => currentFilters[key as keyof typeof currentFilters]) && (
                  <span className="ml-2 text-sm text-blue-600">
                    (Filters applied)
                  </span>
                )}
              </p>
            </div>
            <div className="flex items-center gap-2">
              {/* Mobile Filter Button */}
              <button
                onClick={() => setShowMobileFilters(!showMobileFilters)}
                className="lg:hidden flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.207A1 1 0 013 6.5V4z" />
                </svg>
                Filters
              </button>
              
              <span className="text-sm text-gray-500">Selected: {selectedProducts.length}</span>
              {selectedProducts.length > 0 && (
                <button
                  onClick={() => setSelectedProducts([])}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Clear
                </button>
              )}
            </div>
          </div>

          {/* Products Grid */}
          {!loading && products.length > 0 ? (
            <>
              <div className="grid sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-4 lg:gap-6">
                {products.map((product) => (
                  <div key={product.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
                    <div className="relative">
                      <div className="h-48 bg-gray-200 flex items-center justify-center">
                        <span className="text-gray-400 text-2xl">🎸</span>
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
                    
                    <div className="p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-gray-600">{product.brand?.name || 'Brand'}</span>
                        <div className="flex items-center gap-1">
                          <span className="text-yellow-500">★★★★★</span>
                          <span className="text-sm font-medium">{formatRating(product.avg_rating || 0)}</span>
                        </div>
                      </div>
                      <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">{product.name}</h3>
                      <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                        {product.description || "High-quality musical instrument with excellent craftsmanship and sound."}
                      </p>
                      
                      <div className="space-y-2">
                        {product.prices && product.prices.length > 0 ? (
                          <>
                            {/* Show only stores that are actually associated with this product */}
                            {product.prices
                              .slice(0, 3) // Show max 3 stores to avoid clutter
                              .map((price) => {
                                const isThomann = price.store.name.toLowerCase().includes('thomann');
                                const isGear4Music = price.store.name.toLowerCase().includes('gear4music');
                                
                                if (isThomann) {
                                  return (
                                    <AffiliateButton
                                      key={price.id}
                                      store="thomann"
                                      href={price.affiliate_url}
                                      className={!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}
                                    >
                                      {formatPrice(price.price, price.currency)} at {price.store.name}
                                      {!price.is_available && ' (Out of Stock)'}
                                    </AffiliateButton>
                                  );
                                } else if (isGear4Music) {
                                  return (
                                    <AffiliateButton
                                      key={price.id}
                                      store="gear4music"
                                      href={price.affiliate_url}
                                      className={!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}
                                    >
                                      {formatPrice(price.price, price.currency)} at {price.store.name}
                                      {!price.is_available && ' (Out of Stock)'}
                                    </AffiliateButton>
                                  );
                                } else {
                                  return (
                                    <a 
                                      key={price.id}
                                      href={price.affiliate_url}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className={`block w-full text-center py-2 rounded-lg transition-colors text-sm font-medium ${
                                        price.is_available 
                                          ? 'bg-gray-800 text-white hover:bg-gray-700' 
                                          : 'bg-gray-300 text-gray-600 cursor-not-allowed'
                                      }`}
                                    >
                                      {formatPrice(price.price, price.currency)} at {price.store.name}
                                      {!price.is_available && ' (Out of Stock)'}
                                    </a>
                                  );
                                }
                              })
                            }
                            
                            {/* Show more stores link if there are more than 3 */}
                            {product.prices.length > 3 && (
                              <div className="text-center py-2 text-sm text-gray-500">
                                +{product.prices.length - 3} more stores available
                              </div>
                            )}
                          </>
                        ) : (
                          <>
                            {/* Default affiliate store links when no prices available */}
                            <div className="space-y-2 mb-2">
                              <AffiliateButton
                                store="thomann"
                                href={`https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(product.name)}&aff=123`}
                                className="mb-2"
                              />
                              <AffiliateButton
                                store="gear4music"
                                href={`https://gear4music.com/search?search=${encodeURIComponent(product.name)}&aff=123`}
                              />
                            </div>
                          </>
                        )}
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

              {/* Ad Sidebar */}
      <div className="lg:col-span-1">
        <div className="sticky top-24">
          <AdSidebar compact={true} />
        </div>
      </div>
      </div>
      
      {/* Floating Compare Button */}
      <FloatingCompareButton
        selectedCount={selectedProducts.length}
        onCompare={compareSelected}
        isVisible={selectedProducts.length >= 1}
      />
    </div>
  );
}

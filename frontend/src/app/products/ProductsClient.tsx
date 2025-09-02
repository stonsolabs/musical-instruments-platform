'use client';

import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { Product, SearchResponse, Category, Brand } from '@/types';
import { getApiBaseUrl } from '@/lib/api';
import FloatingCompareButton from '@/components/FloatingCompareButton';
import SpecificationsComparison from '@/components/SpecificationsComparison';
import AffiliateButton from '@/components/AffiliateButton';
import { CompactProductVoting } from '@/components/ProductVoting';
import HydrationSafe from '@/components/HydrationSafe';

import { formatPrice, formatRating } from '@/lib/utils';

const API_BASE_URL = getApiBaseUrl();

import { apiClient } from '@/lib/api';

interface ProductsClientProps {
  initialProducts: Product[];
  initialPagination: SearchResponse['pagination'];
  categories: Category[];
  brands: Brand[];
}

// Error Boundary Component
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ProductsClient Error Boundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="text-center py-12">
          <div className="text-red-600 mb-4">Something went wrong loading the products.</div>
          <button 
            onClick={() => this.setState({ hasError: false })} 
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default function ProductsClient({
  initialProducts,
  initialPagination,
  categories,
  brands,
}: ProductsClientProps) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>(initialProducts || []);
  const [pagination, setPagination] = useState(initialPagination || { page: 1, limit: 20, total: 0, pages: 0 });
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

  const loadProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      console.log('🔍 Loading products with filters:', currentFilters);
      
      // Prepare API parameters
      const apiParams: any = {
        limit: 20,
        page: currentFilters.page,
        sort_by: currentFilters.sort_by,
      };
      
      // Add optional parameters only if they have values
      if (currentFilters.query) apiParams.query = currentFilters.query;
      if (currentFilters.category) apiParams.category = currentFilters.category;
      if (currentFilters.brand) apiParams.brand = currentFilters.brand;
      if (currentFilters.price_min) apiParams.price_min = currentFilters.price_min;
      if (currentFilters.price_max) apiParams.price_max = currentFilters.price_max;
      
      console.log('🔍 API Parameters:', apiParams);
      
      const data = await apiClient.searchProducts(apiParams);
      console.log('✅ Products loaded:', data.products.length, 'products');
      console.log('✅ Pagination:', data.pagination);
      console.log('✅ Sample product:', data.products[0]);
      
      setProducts(data.products || []);
      setPagination(data.pagination || { page: 1, limit: 20, total: 0, pages: 0 });
    } catch (e) {
      console.error('❌ Load products error:', e);
      setError(`Failed to load products: ${e instanceof Error ? e.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  }, [currentFilters]);

  // Load products when filters change
  useEffect(() => {
    // Check if we have any active filters
    const hasActiveFilters = currentFilters.query || 
                            currentFilters.category || 
                            currentFilters.brand || 
                            currentFilters.price_min || 
                            currentFilters.price_max ||
                            currentFilters.sort_by !== 'name' ||
                            currentFilters.page > 1;
    
    console.log('🔍 Filter check - hasActiveFilters:', hasActiveFilters, 'currentFilters:', currentFilters);
    
    // Always load products when filters change, but be smart about it
    if (hasActiveFilters) {
      console.log('🔍 Active filters detected, loading products...');
      loadProducts();
    } else if (products.length === 0) {
      // If no products loaded and no filters, load initial products
      console.log('🔍 No products loaded, loading initial products...');
      setProducts(initialProducts || []);
      setPagination(initialPagination || { page: 1, limit: 20, total: 0, pages: 0 });
    }
  }, [currentFilters, loadProducts, products.length, initialProducts, initialPagination]);

  // Debounced search
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchQuery !== currentFilters.query) {
        console.log('🔍 Search query changed:', searchQuery);
        updateFilters({ query: searchQuery });
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [searchQuery, currentFilters.query, updateFilters]);

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
      // Get the product slugs for the selected products (similar to main page handleCompare)
      const selectedProductObjects = products.filter(product => selectedProducts.includes(product.id));
      const validProducts = selectedProductObjects.filter(product => product !== null);
      
      if (validProducts.length >= 1) {
        // Create URL with product slugs for SEO (user only sees slugs)
        const productSlugs = validProducts.map(product => product.slug);
        const slugsString = productSlugs.join(',');
        
        // Debug logging
        console.log('🔍 Compare selected products:', selectedProducts);
        console.log('🔍 Valid product objects:', validProducts);
        console.log('🔍 Product slugs string:', slugsString);
        
        // Navigate to compare page
        window.location.href = `/compare?products=${slugsString}`;
      } else {
        console.warn('⚠️ No valid products selected for comparison');
      }
    } else {
      console.warn('⚠️ No products selected for comparison');
    }
  };

  // Check if comparing across different categories
  const selectedProductCategories = products
    .filter(p => selectedProducts.includes(p.id))
    .map(p => p.category?.name || 'Unknown')
    .filter(Boolean);
  const hasDifferentCategories = new Set(selectedProductCategories).size > 1;

  return (
    <ErrorBoundary>
      <HydrationSafe
        fallback={
          <div className="animate-pulse">
            <div className="grid lg:grid-cols-4 gap-8">
              <div className="lg:col-span-1">
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-96"></div>
              </div>
              <div className="lg:col-span-3">
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {[...Array(6)].map((_, i) => (
                    <div key={i} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <div className="h-48 bg-gray-200 rounded-lg mb-4"></div>
                      <div className="h-4 bg-gray-200 rounded mb-2"></div>
                      <div className="h-6 bg-gray-200 rounded mb-2"></div>
                      <div className="h-4 bg-gray-200 rounded"></div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        }
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-4 gap-6 xl:gap-8">
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
                    {categories?.map((category) => (
                      <option key={category.id} value={category.slug}>
                        {category.name}
                      </option>
                    )) || []}
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
                    {brands?.map((brand) => (
                      <option key={brand.id} value={brand.slug}>
                        {brand.name}
                      </option>
                    )) || []}
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

            {/* Main Content */}
            <div className="lg:col-span-3">
              {/* Header */}
              <div className="flex items-center justify-between mb-6">
                <div>
                  <p className="text-gray-600">
                    {pagination?.total || 0} products found
                    {Object.keys(currentFilters).some(key => currentFilters[key as keyof typeof currentFilters]) && (
                      <span className="ml-2 text-sm text-blue-600">
                        (Filters applied)
                      </span>
                    )}
                  </p>
                  {error && (
                    <p className="text-red-600 text-sm mt-1">
                      Error: {error}
                    </p>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  {/* Debug Button */}
                  {process.env.NODE_ENV !== 'production' && (
                    <button
                      onClick={() => {
                        console.log('🔍 Debug: Current filters:', currentFilters);
                        console.log('🔍 Debug: Products count:', products.length);
                        console.log('🔍 Debug: Loading state:', loading);
                        loadProducts();
                      }}
                      className="px-3 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50"
                    >
                      Debug API
                    </button>
                  )}
                  
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
              {!loading && products && products.length > 0 ? (
                <>
                  <div className="grid sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-4 lg:gap-6">
                    {products.map((product) => (
                      <div key={product.id} className={`bg-white rounded-lg shadow-sm border overflow-hidden hover:shadow-md transition-all duration-200 ${
                        selectedProducts.includes(product.id) 
                          ? 'border-blue-500 shadow-lg ring-2 ring-blue-200' 
                          : 'border-gray-200'
                      }`}>
                        <div className="relative">
                          <div 
                            className="h-48 bg-white flex items-center justify-center cursor-pointer relative group overflow-hidden border border-gray-200"
                            onClick={() => toggleProductSelection(product.id)}
                          >
                            {product.images && product.images.length > 0 ? (
                              <img 
                                src={product.images[0]} 
                                alt={product.name}
                                className="w-full h-full scale-105"
                                style={{ backgroundColor: 'white' }}
                              />
                            ) : (
                              <span className="text-gray-400 text-2xl">🎸</span>
                            )}
                            {/* Selection overlay */}
                            <div className={`absolute inset-0 flex items-center justify-center transition-all duration-200 ${
                              selectedProducts.includes(product.id)
                                ? 'bg-blue-500 bg-opacity-20'
                                : 'bg-black bg-opacity-0 group-hover:bg-opacity-10'
                            }`}>
                              {selectedProducts.includes(product.id) && (
                                <div className="w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center shadow-lg">
                                  <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                  </svg>
                                </div>
                              )}
                            </div>
                            {/* Selection indicator */}
                            <div className={`absolute top-2 right-2 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                              selectedProducts.includes(product.id)
                                ? 'bg-blue-600 border-blue-600 text-white'
                                : 'bg-white border-gray-300 text-gray-400 group-hover:border-blue-600'
                            }`}>
                              {selectedProducts.includes(product.id) && (
                                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                </svg>
                              )}
                            </div>
                          </div>
                        </div>
                        
                        <div className="p-4">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm text-gray-600">{product.brand?.name || 'Brand'}</span>
                          </div>
                          
                          {/* Voting Component - Only render if vote_stats exists */}
                          {product.vote_stats && (
                            <div className="flex items-center justify-center mb-3">
                              <CompactProductVoting 
                                productId={product.id}
                                initialStats={product.vote_stats}
                                className=""
                              />
                            </div>
                          )}
                          
                          <Link href={`/products/${product.slug}-${product.id}`} className="block">
                            <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 hover:text-accent-600 transition-colors cursor-pointer">{product.name}</h3>
                          </Link>
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
                                        <a
                                          key={price.id}
                                          href={price.affiliate_url}
                                          target="_blank"
                                          rel="noopener noreferrer"
                                          className={`fp-table__button fp-table__button--thomann ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                                        >
                                          <span>View Price at</span>
                                          <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
                                        </a>
                                      );
                                    } else if (isGear4Music) {
                                      return (
                                        <a
                                          key={price.id}
                                          href={price.affiliate_url}
                                          target="_blank"
                                          rel="noopener noreferrer"
                                          className={`fp-table__button fp-table__button--gear4music ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                                        >
                                          <span>View Price at</span>
                                          <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
                                        </a>
                                      );
                                    } else {
                                      return (
                                        <a 
                                          key={price.id}
                                          href={price.affiliate_url}
                                          target="_blank"
                                          rel="noopener noreferrer"
                                          className={`fp-table__button ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                                        >
                                          <span>View Price at</span>
                                          <span className="font-medium">{price.store.name}</span>
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
                                  <a
                                    href={product.content?.store_links?.['Thomann'] || product.content?.store_links?.['thomann'] || `https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(product.name)}&aff=123`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="fp-table__button fp-table__button--thomann"
                                  >
                                    <span>View Price at</span>
                                    <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
                                  </a>
                                  <a
                                    href={product.content?.store_links?.['gear4music'] || product.content?.store_links?.['Gear4music'] || `https://gear4music.com/search?search=${encodeURIComponent(product.name)}&aff=123`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="fp-table__button fp-table__button--gear4music"
                                  >
                                    <span>View Price at</span>
                                    <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
                                  </a>
                                </div>
                              </>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Specifications Comparison - Show when products are selected */}
                  {selectedProducts.length >= 1 && (
                    <div className="mt-8">
                      <SpecificationsComparison 
                        products={products.filter(p => selectedProducts.includes(p.id))}
                        isCollapsible={true}
                        defaultCollapsed={true}
                        className=""
                      />
                    </div>
                  )}

                  {/* Pagination */}
                  {pagination && pagination.pages > 1 && (
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
          
          {/* Floating Compare Button */}
          <FloatingCompareButton
            selectedCount={selectedProducts.length}
            onCompare={compareSelected}
            isVisible={selectedProducts.length >= 1}
          />
        </div>
      </HydrationSafe>
    </ErrorBoundary>
  );
}

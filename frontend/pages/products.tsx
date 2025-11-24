import { GetServerSideProps } from 'next';
import Head from 'next/head';
import Link from 'next/link';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { Product, Category, Brand, SearchResult } from '../src/types';
import { fetchProducts, fetchCategories, fetchBrands } from '../src/lib/api';
import ProductCard from '../src/components/ProductCard';
import ProductFilters from '../src/components/ProductFilters';
import ProductSort from '../src/components/ProductSort';
import Pagination from '../src/components/Pagination';
import { ComparisonProvider } from '../src/components/FloatingCompareButton';

interface ProductsPageProps {
  initialProducts: SearchResult;
  categories: Category[];
  brands: Brand[];
}

export default function ProductsPage({ initialProducts, categories, brands }: ProductsPageProps) {
  const router = useRouter();
  const [products, setProducts] = useState<SearchResult>(initialProducts);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    category: '',
    brand: '',
    search: '',
    priceMin: '',
    priceMax: '',
  });
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // Sync URL parameters with component state when route changes
  useEffect(() => {
    const { query } = router;
    setFilters({
      category: (query.category as string) || '',
      brand: (query.brand as string) || '',
      search: (query.search as string) || '',
      priceMin: (query.priceMin as string) || '',
      priceMax: (query.priceMax as string) || '',
    });
    setSortBy((query.sort_by as string) || 'name');
    setSortOrder((query.sort_order as 'asc' | 'desc') || 'asc');
  }, [router.query]);

  // Update products when initial data changes (from getServerSideProps)
  useEffect(() => {
    setProducts(initialProducts);
  }, [initialProducts]);

  const handleFiltersChange = async (newFilters: typeof filters) => {
    setFilters(newFilters);
    setLoading(true);
    
    try {
      const data = await fetchProducts({
        category: newFilters.category || undefined,
        brand: newFilters.brand || undefined,
        query: newFilters.search || undefined,
        sort_by: sortBy as any,
        sort_order: sortOrder,
        limit: 10,
        page: 1,
      });
      setProducts(data);
    } catch (error) {
      console.error('Error updating filters:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSortChange = async (newSortBy: string, newSortOrder: 'asc' | 'desc') => {
    setSortBy(newSortBy);
    setSortOrder(newSortOrder);
    setLoading(true);
    
    try {
      const data = await fetchProducts({
        category: filters.category || undefined,
        brand: filters.brand || undefined,
        query: filters.search || undefined,
        sort_by: newSortBy as any,
        sort_order: newSortOrder,
        limit: 10,
        page: 1,
      });
      setProducts(data);
    } catch (error) {
      console.error('Error updating sort:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = async (page: number) => {
    setLoading(true);
    
    try {
      const data = await fetchProducts({
        category: filters.category || undefined,
        brand: filters.brand || undefined,
        query: filters.search || undefined,
        sort_by: sortBy as any,
        sort_order: sortOrder,
        page,
        limit: 10,
      });
      setProducts(data);
    } catch (error) {
      console.error('Error changing page:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Musical Instruments - GetYourMusicGear</title>
        <meta name="description" content="Browse and compare musical instruments from top brands. Find guitars, basses, pianos, drums, and more with expert reviews and best prices." />
        <link rel="canonical" href={`https://www.getyourmusicgear.com/products${router.query.category ? `?category=${router.query.category}` : ''}${router.query.brand ? `${router.query.category ? '&' : '?'}brand=${router.query.brand}` : ''}${router.query.search ? `${(router.query.category || router.query.brand) ? '&' : '?'}search=${router.query.search}` : ''}`} />
        <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
        <meta property="og:url" content={`https://www.getyourmusicgear.com/products${router.query.category ? `?category=${router.query.category}` : ''}`} />
      </Head>

      <ComparisonProvider>
        <div className="min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Page Header */}
          <div className="mb-8">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                Musical Instruments
              </h1>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-6">
                Discover and compare the best musical instruments from top brands worldwide
              </p>
              {/* Stats */}
              <div className="flex items-center justify-center gap-8 text-sm text-gray-500">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span>{products.total} Products Available</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span>Expert Reviews & Comparisons</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span>Best Affiliate Prices</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-col lg:flex-row gap-8">
            {/* Sidebar Filters */}
            <div className="lg:w-64 flex-shrink-0">
              <ProductFilters
                categories={categories}
                brands={brands}
                filters={filters}
                onFiltersChange={handleFiltersChange}
              />
            </div>

            {/* Main Content */}
            <div className="flex-1">
              {/* Enhanced Header with Stats and Controls */}
              <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
                <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
                  <div className="flex-1">
                    <h2 className="text-2xl font-semibold text-gray-900 mb-2">Browse Products</h2>
                    <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                      <span className="flex items-center space-x-2">
                        <span className="font-medium">Showing {products.products.length} of {products.total}</span>
                      </span>
                      {filters.category && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
                          Category: {filters.category}
                        </span>
                      )}
                      {filters.brand && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-50 text-green-700">
                          Brand: {filters.brand}
                        </span>
                      )}
                      {filters.search && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-50 text-purple-700">
                          Search: "{filters.search}"
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <ProductSort
                      sortBy={sortBy}
                      sortOrder={sortOrder}
                      onSortChange={handleSortChange}
                    />
                  </div>
                </div>
              </div>

              {/* Products Grid */}
              {loading ? (
                <div className="text-center py-12">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-primary mx-auto mb-4"></div>
                  <p className="text-gray-600">Loading products...</p>
                  <p className="text-sm text-gray-500 mt-2">Finding the best instruments for you</p>
                </div>
              ) : (
                <>
                  {/* Enhanced Products Grid with better spacing */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {products.products.map((product) => (
                      <ProductCard key={product.id} product={product} />
                    ))}
                  </div>
                  
                  {/* Enhanced Pagination */}
                  {products.total_pages > 1 && (
                    <div className="mt-16 bg-white rounded-lg shadow-sm border p-6">
                      <div className="flex items-center justify-between mb-4">
                        <p className="text-sm text-gray-600">
                          Page {products.page} of {products.total_pages} 
                          <span className="ml-2 text-gray-500">({products.total} total products)</span>
                        </p>
                      </div>
                      <Pagination
                        currentPage={products.page}
                        totalPages={products.total_pages}
                        onPageChange={handlePageChange}
                      />
                    </div>
                  )}

                  {/* Call to Action for More Products */}
                  {products.products.length > 0 && products.page === products.total_pages && (
                    <div className="mt-12 text-center">
                      <div className="bg-gradient-to-r from-brand-primary to-brand-secondary rounded-lg p-8 text-white">
                        <h3 className="text-2xl font-bold mb-2">Can't find what you're looking for?</h3>
                        <p className="mb-6 opacity-90">Let us know what instrument you need and we'll help you find it</p>
                        <Link href="/contact" className="btn-secondary bg-white text-brand-primary hover:bg-gray-100">
                          Request an Instrument
                        </Link>
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
        </div>
      </ComparisonProvider>
    </>
  );
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  try {
    const allowedSort = ['name', 'rating', 'popularity', 'price'] as const;
    const requestedSort = (query.sort_by as string) || 'name';
    const sortBy = (allowedSort as readonly string[]).includes(requestedSort)
      ? (requestedSort as (typeof allowedSort)[number])
      : 'name';

    const [products, categories, brands] = await Promise.all([
      fetchProducts({
        page: query.page ? parseInt(query.page as string) : 1,
        per_page: 10,
        category: query.category as string,
        brand: query.brand as string,
        search: query.search as string,
        sort_by: sortBy,
        sort_order: (query.sort_order as 'asc' | 'desc') || 'asc',
      }),
      fetchCategories(),
      fetchBrands(),
    ]);

    return {
      props: {
        initialProducts: products,
        categories: categories.filter(cat => cat.is_active),
        brands,
      },
    };
  } catch (error) {
    console.error('Error fetching products data:', error);
    
    return {
      props: {
        initialProducts: {
          products: [],
          total: 0,
          page: 1,
          per_page: 10,
          total_pages: 0,
        },
        categories: [],
        brands: [],
      },
    };
  }
};

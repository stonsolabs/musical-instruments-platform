import React, { Suspense } from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { Product, SearchResponse, Category, Brand } from '@/types';
import ProductsClient from './ProductsClient';
import { serverApi } from '@/lib/server-api';

// Force dynamic rendering since we use searchParams
export const dynamic = 'force-dynamic';

// Generate metadata for SEO
export async function generateMetadata({ searchParams }: {
  searchParams: { [key: string]: string | string[] | undefined }
}): Promise<Metadata> {
  const query = searchParams.query as string || '';
  const category = searchParams.category as string || '';
  const brand = searchParams.brand as string || '';

  let title = 'Products';
  let description = 'Browse our extensive collection of products. Find guitars, pianos, drums, and more from top brands.';

  if (query) {
    title = `${query}`;
    description = `Find ${query} and other products. Compare prices and features from multiple retailers.`;
  } else if (category && brand) {
    title = `${brand} ${category}`;
    description = `Browse ${brand} ${category} products. Compare prices and find the best deals.`;
  } else if (category) {
    title = `${category}`;
    description = `Explore our ${category} collection. Find the perfect product with detailed comparisons and reviews.`;
  } else if (brand) {
    title = `${brand} Products`;
    description = `Browse ${brand} products. Compare models and find the best prices.`;
  }

  return {
    title,
    description,
    keywords: `musical instruments, ${query || category || brand || 'guitars, pianos, drums'}, music equipment, buy instruments online`,
    openGraph: {
      title,
      description,
      type: 'website',
      url: 'https://getyourmusicgear.com/products',
    },
    twitter: {
      card: 'summary',
      title,
      description,
    },
  };
}

interface ProductsPageProps {
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function ProductsPage({ searchParams }: ProductsPageProps) {
  // Convert searchParams for server API
  const searchFilters: Record<string, any> = {};
  Object.entries(searchParams).forEach(([key, value]) => {
    if (value && typeof value === 'string') {
      searchFilters[key] = value;
    }
  });

  // Set defaults
  if (!searchFilters.limit) searchFilters.limit = 20;
  if (!searchFilters.page) searchFilters.page = 1;
  if (!searchFilters.sort_by) searchFilters.sort_by = 'name';

  // Fetch data on the server with error handling
  const [productsData, categoriesData, brandsData] = await Promise.allSettled([
    serverApi.searchProducts(searchFilters),
    serverApi.getCategories(),
    serverApi.getBrands(),
  ]);

  const products = productsData.status === 'fulfilled' && productsData.value?.products 
    ? productsData.value 
    : { products: [], pagination: { page: 1, limit: 20, total: 0, pages: 0 }, filters_applied: { sort_by: 'name' } };

  const categories = categoriesData.status === 'fulfilled' && categoriesData.value?.categories
    ? categoriesData.value.categories 
    : [];

  const brands = brandsData.status === 'fulfilled' && brandsData.value?.brands
    ? brandsData.value.brands 
    : [];

  // Generate structured data for SEO
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'Products',
    description: 'Browse our extensive collection of products from top brands.',
    url: 'https://getyourmusicgear.com/products',
    mainEntity: {
      '@type': 'ItemList',
      numberOfItems: products.pagination.total,
      itemListElement: products.products.map((product, index) => ({
        '@type': 'Product',
        position: index + 1,
        name: product.name,
        brand: {
          '@type': 'Brand',
          name: product.brand?.name || 'Unknown Brand',
        },
        category: product.category?.name || 'Unknown Category',
        url: `https://getyourmusicgear.com/products/${product.slug}`,
        offers: product.prices && product.prices.length > 0 ? {
          '@type': 'Offer',
          price: product.prices[0].price,
          priceCurrency: product.prices[0].currency,
          availability: 'https://schema.org/InStock',
        } : undefined,
        aggregateRating: product.avg_rating > 0 ? {
          '@type': 'AggregateRating',
          ratingValue: product.avg_rating,
          reviewCount: product.review_count,
        } : undefined,
      })),
    },
  };

  return (
    <>
      {/* Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />

      <div className="min-h-screen bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Breadcrumb */}
          <nav className="mb-6" aria-label="Breadcrumb">
            <ol className="flex items-center space-x-2 text-sm text-gray-600">
              <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
              <li>/</li>
              <li className="text-gray-900" aria-current="page">Products</li>
            </ol>
          </nav>

          {/* Page Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              {searchParams.category ? 
                (searchParams.category as string).split('-').map(word => 
                  word.charAt(0).toUpperCase() + word.slice(1)
                ).join(' ') : 
                'Products'
              }
            </h1>
            <p className="text-lg text-gray-600">
              {products.pagination.total} products found
              {searchParams.category && (
                <span className="ml-2">
                  in {(searchParams.category as string).split('-').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                  ).join(' ')}
                </span>
              )}
            </p>
          </div>

          {/* Client-side interactive component */}
          <Suspense fallback={
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
          }>
            <ProductsClient
              initialProducts={products.products}
              initialPagination={products.pagination}
              categories={categories}
              brands={brands}
            />
          </Suspense>
        </div>
      </div>
    </>
  );
}
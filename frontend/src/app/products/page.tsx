import React, { Suspense } from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { Product, SearchResponse, Category, Brand } from '@/types';
import ProductsClient from './ProductsClient';
import { API_BASE_URL } from '@/lib/api';

// Force dynamic rendering since we use searchParams
export const dynamic = 'force-dynamic';

async function fetchProducts(searchParams: { [key: string]: string | string[] | undefined }): Promise<SearchResponse> {
  try {
    const params = new URLSearchParams();
    
    // Convert searchParams to URLSearchParams
    Object.entries(searchParams).forEach(([key, value]) => {
      if (value && typeof value === 'string') {
        params.append(key, value);
      }
    });

    // Set defaults
    if (!params.has('limit')) params.set('limit', '20');
    if (!params.has('page')) params.set('page', '1');
    if (!params.has('sort_by')) params.set('sort_by', 'name');

    // Use proxy route instead of direct backend call
    const response = await fetch(`/api/proxy/products?${params.toString()}`, {
      next: { revalidate: 300 }, // Revalidate every 5 minutes
    });

    if (!response.ok) {
      console.error(`API Error: ${response.status} ${response.statusText}`);
      return {
        products: [],
        pagination: { page: 1, limit: 20, total: 0, pages: 0 },
        filters_applied: { sort_by: 'name' }
      };
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching products:', error);
    return {
      products: [],
      pagination: { page: 1, limit: 20, total: 0, pages: 0 },
      filters_applied: { sort_by: 'name' }
    };
  }
}

async function fetchCategories(): Promise<Category[]> {
  try {
    const response = await fetch(`/api/proxy/categories`, {
      next: { revalidate: 3600 }, // Revalidate every hour
    });

    if (!response.ok) {
      console.error(`Categories API Error: ${response.status} ${response.statusText}`);
      return [];
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching categories:', error);
    return [];
  }
}

async function fetchBrands(): Promise<Brand[]> {
  try {
    const response = await fetch(`/api/proxy/brands`, {
      next: { revalidate: 3600 }, // Revalidate every hour
    });

    if (!response.ok) {
      console.error(`Brands API Error: ${response.status} ${response.statusText}`);
      return [];
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching brands:', error);
    return [];
  }
}

// Generate metadata for SEO
export async function generateMetadata({ searchParams }: {
  searchParams: { [key: string]: string | string[] | undefined }
}): Promise<Metadata> {
  const query = searchParams.query as string || '';
  const category = searchParams.category as string || '';
  const brand = searchParams.brand as string || '';

  let title = 'Musical Instruments';
  let description = 'Browse our extensive collection of musical instruments. Find guitars, pianos, drums, and more from top brands.';

  if (query) {
    title = `${query} - Musical Instruments`;
    description = `Find ${query} and other musical instruments. Compare prices and features from multiple retailers.`;
  } else if (category && brand) {
    title = `${brand} ${category} - Musical Instruments`;
    description = `Browse ${brand} ${category} instruments. Compare prices and find the best deals.`;
  } else if (category) {
    title = `${category} - Musical Instruments`;
    description = `Explore our ${category} collection. Find the perfect instrument with detailed comparisons and reviews.`;
  } else if (brand) {
    title = `${brand} Instruments - Musical Instruments`;
    description = `Browse ${brand} musical instruments. Compare models and find the best prices.`;
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
  // Fetch data on the server
  const [productsData, categories, brands] = await Promise.all([
    fetchProducts(searchParams),
    fetchCategories(),
    fetchBrands(),
  ]);

  // Generate structured data for SEO
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'Musical Instruments',
    description: 'Browse our extensive collection of musical instruments from top brands.',
    url: 'https://getyourmusicgear.com/products',
    mainEntity: {
      '@type': 'ItemList',
      numberOfItems: productsData.pagination.total,
      itemListElement: productsData.products.map((product, index) => ({
        '@type': 'Product',
        position: index + 1,
        name: product.name,
        brand: {
          '@type': 'Brand',
          name: product.brand.name,
        },
        category: product.category.name,
        url: `https://getyourmusicgear.com/products/${product.slug}-${product.id}`,
        offers: product.best_price ? {
          '@type': 'Offer',
          price: product.best_price.price,
          priceCurrency: product.best_price.currency,
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
              Musical Instruments
            </h1>
            <p className="text-lg text-gray-600">
              Discover {productsData.pagination.total} musical instruments from top brands. 
              Compare prices, read reviews, and find your perfect instrument.
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
              initialProducts={productsData.products}
              initialPagination={productsData.pagination}
              categories={categories}
              brands={brands}
            />
          </Suspense>
        </div>
      </div>
    </>
  );
}
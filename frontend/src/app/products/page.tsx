import React, { Suspense } from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { Product, SearchResponse, Category, Brand } from '@/types';
import ProductsClient from './ProductsClient';
import { API_BASE_URL, getServerBaseUrl } from '@/lib/api';

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

    // For server-side requests, call Azure API directly with API key
    const apiUrl = 'https://getyourmusicgear-api.azurewebsites.net/api/v1/products';
    const apiKey = process.env.API_KEY;

    if (!apiKey) {
      console.error('API_KEY environment variable is not set');
      return { 
        products: [], 
        pagination: { page: 1, limit: 20, total: 0, pages: 0 },
        filters_applied: { sort_by: 'name' }
      };
    }

    console.log('🔍 Server-side fetching products:', `${apiUrl}?${params.toString()}`);

    const response = await fetch(`${apiUrl}?${params.toString()}`, {
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json',
      },
      next: { revalidate: 300 }, // Revalidate every 5 minutes
    });

    if (!response.ok) {
      console.error(`API Error: ${response.status} ${response.statusText}`);
      const errorText = await response.text();
      console.error('Error response:', errorText);
      return {
        products: [],
        pagination: { page: 1, limit: 20, total: 0, pages: 0 },
        filters_applied: { sort_by: 'name' }
      };
    }

    const data = await response.json();
    console.log('✅ Server-side products fetched:', data.products?.length || 0, 'products');
    
    // Ensure data structure consistency
    const normalizedData: SearchResponse = {
      products: data.products || [],
      pagination: data.pagination || { page: 1, limit: 20, total: 0, pages: 0 },
      filters_applied: data.filters_applied || { sort_by: 'name' }
    };
    
    // Normalize product data to ensure all required fields exist
    normalizedData.products = normalizedData.products.map(product => ({
      id: product.id || 0,
      sku: product.sku || '',
      name: product.name || 'Unknown Product',
      slug: product.slug || 'unknown-product',
      brand: product.brand || { id: 0, name: 'Unknown Brand', slug: 'unknown-brand' },
      category: product.category || { id: 0, name: 'Unknown Category', slug: 'unknown-category' },
      description: product.description || '',
      specifications: product.specifications || {},
      images: product.images || [],
      msrp_price: product.msrp_price,
      best_price: product.best_price,
      prices: product.prices || [],
      avg_rating: product.avg_rating || 0,
      review_count: product.review_count || 0,
      is_active: product.is_active !== undefined ? product.is_active : true,
      created_at: product.created_at || new Date().toISOString(),
      updated_at: product.updated_at || new Date().toISOString(),
      ai_content: product.ai_content,
      vote_stats: product.vote_stats,
      thomann_info: product.thomann_info,
      content: product.content || {}
    }));
    
    return normalizedData;
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
    const apiUrl = 'https://getyourmusicgear-api.azurewebsites.net/api/v1/categories';
    const apiKey = process.env.API_KEY;

    if (!apiKey) {
      console.error('API_KEY environment variable is not set');
      return [];
    }

    const response = await fetch(apiUrl, {
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json',
      },
      next: { revalidate: 3600 }, // Revalidate every hour
    });

    if (!response.ok) {
      console.error(`Categories API Error: ${response.status} ${response.statusText}`);
      return [];
    }

    const data = await response.json();
    console.log('✅ Server-side categories fetched:', data?.length || 0, 'categories');
    
    // Ensure data structure consistency
    return (data || []).map((category: any) => ({
      id: category.id || 0,
      name: category.name || 'Unknown Category',
      slug: category.slug || 'unknown-category',
      description: category.description || '',
      parent_id: category.parent_id,
      image_url: category.image_url
    }));
  } catch (error) {
    console.error('Error fetching categories:', error);
    return [];
  }
}

async function fetchBrands(): Promise<Brand[]> {
  try {
    const apiUrl = 'https://getyourmusicgear-api.azurewebsites.net/api/v1/brands';
    const apiKey = process.env.API_KEY;

    if (!apiKey) {
      console.error('API_KEY environment variable is not set');
      return [];
    }

    const response = await fetch(apiUrl, {
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json',
      },
      next: { revalidate: 3600 }, // Revalidate every hour
    });

    if (!response.ok) {
      console.error(`Brands API Error: ${response.status} ${response.statusText}`);
      return [];
    }

    const data = await response.json();
    console.log('✅ Server-side brands fetched:', data?.length || 0, 'brands');
    
    // Ensure data structure consistency
    return (data || []).map((brand: any) => ({
      id: brand.id || 0,
      name: brand.name || 'Unknown Brand',
      slug: brand.slug || 'unknown-brand',
      logo_url: brand.logo_url,
      description: brand.description || ''
    }));
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
  // Fetch data on the server with error handling
  let productsData: SearchResponse;
  let categories: Category[] = [];
  let brands: Brand[] = [];

  try {
    [productsData, categories, brands] = await Promise.all([
      fetchProducts(searchParams),
      fetchCategories(),
      fetchBrands(),
    ]);
  } catch (error) {
    console.error('Error fetching data:', error);
    // Provide fallback data
    productsData = {
      products: [],
      pagination: { page: 1, limit: 20, total: 0, pages: 0 },
      filters_applied: { sort_by: 'name' }
    };
    categories = [];
    brands = [];
  }

  // Generate structured data for SEO
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'Products',
    description: 'Browse our extensive collection of products from top brands.',
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
          name: product.brand?.name || 'Unknown Brand',
        },
        category: product.category?.name || 'Unknown Category',
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
              {productsData.pagination.total} products found
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
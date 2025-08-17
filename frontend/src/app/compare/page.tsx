import React, { Suspense } from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import type { ComparisonResponse, Product } from '@/types';
import CompareClient from './CompareClient';
import SearchAutocomplete from '@/components/SearchAutocomplete';

import { API_BASE_URL, apiClient } from '@/lib/api';

// Force dynamic rendering since we use searchParams
export const dynamic = 'force-dynamic';

async function fetchProductIdsFromSlugs(productSlugs: string[]): Promise<number[]> {
  if (productSlugs.length === 0) return [];
  
  try {
    // Fetch product IDs from slugs using the products API
    const response = await fetch(`/api/proxy/products?slugs=${productSlugs.join(',')}&limit=100`);
    if (!response.ok) {
      console.error(`Products API Error: ${response.status} ${response.statusText}`);
      return [];
    }
    
    const data = await response.json();
    return data.products.map((product: any) => product.id);
  } catch (error) {
    console.error('Error fetching product IDs:', error);
    return [];
  }
}

async function fetchComparison(productIds: number[]): Promise<ComparisonResponse | null> {
  if (productIds.length < 1) {
    return null;
  }

  try {
    // Use the IDs directly to fetch comparison data
    const response = await fetch(`/api/proxy/compare`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(productIds),
      next: { revalidate: 300 }, // Revalidate every 5 minutes
    });
    
    if (!response.ok) {
      console.error(`Compare API Error: ${response.status} ${response.statusText}`);
      return null;
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching comparison:', error);
    return null;
  }
}

// Generate metadata for SEO
export async function generateMetadata({ searchParams }: {
  searchParams: { [key: string]: string | string[] | undefined }
}): Promise<Metadata> {
  const productsParam = searchParams.products as string;
  const productSlugs = productsParam ? productsParam.split(',').filter(slug => slug.trim()) : [];
  
  if (productSlugs.length < 1) {
    return {
      title: 'Compare Musical Instruments',
      description: 'Compare musical instruments side by side. Find the best deals and features across different brands and models.',
      keywords: 'compare musical instruments, instrument comparison, music gear comparison',
    };
  }

  // Fetch product IDs from slugs internally
  const productIds = await fetchProductIdsFromSlugs(productSlugs);
  if (productIds.length < 1) {
    return {
      title: 'Compare Musical Instruments',
      description: 'Compare musical instruments side by side. Find the best deals and features across different brands and models.',
      keywords: 'compare musical instruments, instrument comparison, music gear comparison',
    };
  }

  // Try to fetch product data for better metadata
  const comparisonData = await fetchComparison(productIds);
  
  if (comparisonData && comparisonData.products.length > 0) {
    const productNames = comparisonData.products.map(p => p.name).join(' vs ');
    const brands = Array.from(new Set(comparisonData.products.map(p => p.brand.name))).join(', ');
    
    return {
      title: `Compare: ${productNames} - Musical Instruments`,
      description: `Compare ${productNames}. Side-by-side comparison of specifications, prices, and reviews from ${brands}.`,
      keywords: `compare ${productNames.toLowerCase()}, ${brands.toLowerCase()}, musical instruments comparison`,
      openGraph: {
        title: `Compare: ${productNames}`,
        description: `Side-by-side comparison of ${productNames}. Find the best deals and features.`,
        type: 'website',
        url: 'https://getyourmusicgear.com/compare',
      },
      twitter: {
        card: 'summary',
        title: `Compare: ${productNames}`,
        description: `Side-by-side comparison of ${productNames}.`,
      },
    };
  }

  return {
    title: 'Compare Musical Instruments',
    description: 'Compare musical instruments side by side. Find the best deals and features across different brands and models.',
    keywords: 'compare musical instruments, instrument comparison, music gear comparison',
  };
}

interface ComparePageProps {
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function ComparePage({ searchParams }: ComparePageProps) {
  const productsParam = searchParams.products as string;
  const productSlugs = productsParam ? productsParam.split(',').filter(slug => slug.trim()) : [];
  
  // Fetch product IDs from slugs internally
  const productIds = await fetchProductIdsFromSlugs(productSlugs);
  
  // Fetch comparison data on the server
  const comparisonData = await fetchComparison(productIds);

  // Generate structured data for SEO
  const structuredData = comparisonData ? {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: 'Musical Instruments Comparison',
    description: 'Compare musical instruments side by side',
    url: 'https://getyourmusicgear.com/compare',
    mainEntity: {
      '@type': 'ItemList',
      numberOfItems: comparisonData.products.length,
      itemListElement: comparisonData.products.map((product, index) => ({
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
  } : null;

  // Handle case where no valid product IDs are provided
  if (productIds.length < 1) {
    return (
      <>
        {/* Basic structured data for empty state */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ 
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'WebPage',
              name: 'Compare Musical Instruments',
              description: 'Compare musical instruments side by side',
              url: 'https://getyourmusicgear.com/compare',
            })
          }}
        />
        
      <div className="min-h-screen bg-gradient-to-b from-blue-600 to-blue-400">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
              <h1 className="text-3xl font-bold text-white mb-4">Compare Musical Instruments</h1>
              <p className="text-lg text-blue-100 mb-8">
                Search and select at least one instrument to see detailed information and comparison options
              </p>
              
              {/* Compare Interface */}
              <div className="max-w-4xl mx-auto mb-8">
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Compare Instruments</h2>
                  
                  {/* Search Fields */}
                  <div className="flex flex-col md:flex-row items-center gap-6 mb-8">
                    <div className="flex-1 w-full">
                      <label className="block text-sm font-medium text-gray-700 mb-2">Instrument 1</label>
                      <SearchAutocomplete 
                        placeholder="Search for guitars, pianos, drums..."
                        className="w-full"
                        onSearch={(query) => {
                          // Handle instrument 1 selection
                          console.log('Instrument 1 selected:', query);
                          // You can add logic here to store the selected instrument
                        }}
                      />
                    </div>
                    
                    <div className="text-gray-400 font-semibold text-xl">vs</div>
                    
                    <div className="flex-1 w-full">
                      <label className="block text-sm font-medium text-gray-700 mb-2">Instrument 2</label>
                      <SearchAutocomplete 
                        placeholder="Search for guitars, pianos, drums..."
                        className="w-full"
                        onSearch={(query) => {
                          // Handle instrument 2 selection
                          console.log('Instrument 2 selected:', query);
                          // You can add logic here to store the selected instrument
                        }}
                      />
                    </div>
                  </div>
                  
                  {/* Add Another Instrument */}
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors cursor-pointer">
                    <div className="flex items-center justify-center gap-2 text-gray-600">
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                      <span className="font-medium">Add another instrument</span>
                    </div>
                  </div>
                  
                  {/* Compare Button */}
                  <div className="mt-6 text-center">
                    <button className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors text-lg">
                      Compare 1 Instruments
                    </button>
                  </div>
                </div>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link 
                  href="/products" 
                  className="inline-flex items-center gap-2 bg-white text-blue-600 px-6 py-3 rounded-lg hover:bg-gray-100 transition-colors font-semibold"
                >
                  Browse All Products
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </Link>
                <Link 
                  href="/products?category=electric-guitars" 
                  className="inline-flex items-center gap-2 bg-white text-blue-600 px-6 py-3 rounded-lg hover:bg-gray-100 transition-colors font-semibold"
                >
                  Popular Categories
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </Link>
              </div>
            </div>
        </div>
      </div>
      </>
    );
  }

  return (
    <>
      {/* Structured Data */}
      {structuredData && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />
      )}

    <div className="min-h-screen bg-gray-50">
      {/* Ad Space - Top */}
      <section className="py-4 bg-white border-b">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-4 text-white text-center">
            <p className="text-sm">🎵 Compare prices across Europe's top music stores</p>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="mb-8" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
            <li>/</li>
            <li><Link href="/compare" className="hover:text-blue-600">Compare</Link></li>
            {comparisonData && comparisonData.products.length > 0 && (
              <>
                <li>/</li>
                <li className="text-gray-900 font-medium" aria-current="page">
                  {comparisonData.products.map((product, index) => (
                    <span key={product.id}>
                      {index > 0 && <span className="mx-2">VS</span>}
                      {product.name}
                    </span>
                  ))}
                </li>
              </>
            )}
          </ol>
        </nav>

          {/* Client-side interactive component */}
          <Suspense fallback={
            <div className="animate-pulse">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="aspect-square bg-gray-200 rounded-lg mb-4"></div>
                  <div className="space-y-3">
                      <div className="h-4 bg-gray-200 rounded"></div>
                      <div className="h-6 bg-gray-200 rounded"></div>
                      <div className="h-4 bg-gray-200 rounded"></div>
                        </div>
                      </div>
                    ))}
              </div>
            </div>
          }>
            <CompareClient
              productSlugs={productSlugs}
              productIds={productIds}
              initialData={comparisonData}
            />
          </Suspense>
            </div>
      </div>
    </>
  );
}
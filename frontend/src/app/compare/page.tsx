import React, { Suspense } from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import type { ComparisonResponse, Product } from '@/types';
import CompareClient from './CompareClient';

import { API_BASE_URL } from '@/lib/api';

// Force dynamic rendering since we use searchParams
export const dynamic = 'force-dynamic';

async function fetchComparison(productIds: number[]): Promise<ComparisonResponse | null> {
  if (productIds.length < 2) {
    return null;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/compare`, {
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
  const idsParam = searchParams.ids as string;
  const ids = idsParam ? idsParam.split(',').map(id => parseInt(id)).filter(id => !isNaN(id)) : [];
  
  if (ids.length < 2) {
    return {
      title: 'Compare Musical Instruments',
      description: 'Compare musical instruments side by side. Find the best deals and features across different brands and models.',
      keywords: 'compare musical instruments, instrument comparison, music gear comparison',
    };
  }

  // Try to fetch product data for better metadata
  const comparisonData = await fetchComparison(ids);
  
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
  const idsParam = searchParams.ids as string;
  const ids = idsParam ? idsParam.split(',').map(id => parseInt(id)).filter(id => !isNaN(id)) : [];
  
  // Fetch comparison data on the server
  const comparisonData = await fetchComparison(ids);

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

  // Handle case where no valid IDs are provided
  if (ids.length < 2) {
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
        
        <div className="min-h-screen bg-gray-50">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">Compare Musical Instruments</h1>
              <p className="text-lg text-gray-600 mb-8">
                Select at least two instruments to see a detailed side-by-side comparison
              </p>
              <Link 
                href="/products" 
                className="inline-flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Browse Products
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
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
          <nav className="mb-6" aria-label="Breadcrumb">
            <ol className="flex items-center space-x-2 text-sm text-gray-600">
              <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
              <li>/</li>
              <li className="text-gray-900" aria-current="page">Compare</li>
            </ol>
          </nav>

          {/* Page Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Compare Musical Instruments
            </h1>
            {comparisonData && comparisonData.products.length > 0 && (
              <p className="text-lg text-gray-600">
                Comparing {comparisonData.products.length} instruments side by side. 
                Find the perfect match for your needs.
              </p>
            )}
          </div>

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
              productIds={ids}
              initialData={comparisonData}
            />
          </Suspense>
        </div>
      </div>
    </>
  );
}
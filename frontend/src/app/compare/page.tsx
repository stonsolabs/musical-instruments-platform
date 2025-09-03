import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { serverApi } from '@/lib/server-api';
import CompareClient from './CompareClient';
import CompareSearchInterface from './CompareSearchInterface';
import type { ComparisonResponse } from '@/types';

export const dynamic = 'force-dynamic';

export const metadata: Metadata = {
  title: 'Compare Musical Instruments - Find the Perfect Match',
  description: 'Compare musical instruments side by side with detailed specifications, prices, and expert reviews.',
};

interface ComparePageProps {
  searchParams: { products?: string };
}

export default async function ComparePage({ searchParams }: ComparePageProps) {
  const productSlugs = searchParams.products 
    ? decodeURIComponent(searchParams.products).split(',').filter(slug => slug.trim()) 
    : [];

  // Simple server-side data fetching - much cleaner!
  let products: any[] = [];

  if (productSlugs.length > 0) {
    try {
      console.log('🔍 Fetching products:', productSlugs);
      const response = await serverApi.compareProductsBySlugs(productSlugs);
      products = response.products || [];
      console.log(`✅ Found ${products.length} products`);
    } catch (error) {
      console.error('Failed to fetch products:', error);
      products = []; // Fail gracefully
    }
  }

  // Handle case where no valid product slugs are provided
  if (productSlugs.length < 1) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-primary-600 to-primary-400">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-white mb-4">Compare Musical Instruments</h1>
            <p className="text-lg text-primary-100 mb-8">
              Search and select at least one instrument to see detailed information and comparison options
            </p>
            
            {/* Compare Interface */}
            <CompareSearchInterface />
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/products" 
                className="inline-flex items-center gap-2 bg-white text-primary-600 px-6 py-3 rounded-lg hover:bg-primary-50 transition-colors font-semibold"
              >
                Browse All Products
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
              <Link 
                href="/products?category=electric-guitars" 
                className="inline-flex items-center gap-2 bg-white text-primary-600 px-6 py-3 rounded-lg hover:bg-primary-50 transition-colors font-semibold"
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
    );
  }

  return (
    <div className="min-h-screen bg-primary-50">
      {/* Ad Space - Top */}
      <section className="py-4 bg-white border-b">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-primary-500 to-accent-600 rounded-lg p-4 text-white text-center">
            <p className="text-sm">🎵 Compare prices across Europe's top music stores</p>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="mb-8" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-primary-600">
            <li><Link href="/" className="hover:text-primary-800">Home</Link></li>
            <li>/</li>
            <li><Link href="/compare" className="hover:text-primary-800">Compare</Link></li>
            {productSlugs.length > 0 && (
              <>
                <li>/</li>
                <li className="text-primary-900 font-medium" aria-current="page">
                  {productSlugs.map((slug, index) => (
                    <span key={slug}>
                      {index > 0 && <span className="mx-2">VS</span>}
                      {slug.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </span>
                  ))}
                </li>
              </>
            )}
          </ol>
        </nav>

        {/* Much simpler - just pass the products directly */}
        <CompareClient
          products={products}
          productSlugs={productSlugs}
        />
      </div>
    </div>
  );
}
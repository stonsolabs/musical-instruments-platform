'use client';

import React from 'react';
import Link from 'next/link';
import CompareClient from './CompareClient';
import UnifiedSearchAutocomplete from '@/components/UnifiedSearchAutocomplete';

export default function ComparePage() {
  // Get search params from URL on client side
  const [searchParams] = React.useState(() => {
    if (typeof window !== 'undefined') {
      const urlParams = new URLSearchParams(window.location.search);
      return {
        products: urlParams.get('products') || ''
      };
    }
    return { products: '' };
  });
  
  const productSlugs = searchParams.products ? decodeURIComponent(searchParams.products).split(',').filter(slug => slug.trim()) : [];
  
  // Debug logging
  console.log('🔍 Compare page - searchParams:', searchParams);
  console.log('🔍 Compare page - raw products param:', searchParams.products);
  console.log('🔍 Compare page - decoded productSlugs:', productSlugs);

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
              <div className="max-w-4xl mx-auto mb-8">
                <div className="bg-white rounded-xl shadow-elegant border border-primary-200 p-8">
                  <h2 className="text-2xl font-bold text-primary-900 mb-6 text-center">Compare Instruments</h2>
                  
                  {/* Search Fields */}
                  <div className="flex flex-col md:flex-row items-center gap-6 mb-8">
                    <div className="flex-1 w-full">
                      <label className="block text-sm font-medium text-primary-700 mb-2">Instrument 1</label>
                      <UnifiedSearchAutocomplete 
                        variant="product-select"
                        placeholder="Search for guitars, pianos, drums..."
                        className="w-full"
                        onProductSelect={(product) => {
                          // Handle instrument 1 selection
                          console.log('Instrument 1 selected:', product);
                          // You can add logic here to store the selected instrument
                        }}
                      />
                    </div>
                    
                    <div className="text-primary-400 font-semibold text-xl">vs</div>
                    
                    <div className="flex-1 w-full">
                      <label className="block text-sm font-medium text-primary-700 mb-2">Instrument 2</label>
                      <UnifiedSearchAutocomplete 
                        variant="product-select"
                        placeholder="Search for guitars, pianos, drums..."
                        className="w-full"
                        onProductSelect={(product) => {
                          // Handle instrument 2 selection
                          console.log('Instrument 2 selected:', product);
                          // You can add logic here to store the selected instrument
                        }}
                      />
                    </div>
                  </div>
                  
                  {/* Add Another Instrument */}
                  <div className="border-2 border-dashed border-primary-300 rounded-lg p-6 text-center hover:border-primary-400 transition-colors cursor-pointer">
                    <div className="flex items-center justify-center gap-2 text-primary-600">
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                      <span className="font-medium">Add another instrument</span>
                    </div>
                  </div>
                  
                  {/* Compare Button */}
                  <div className="mt-6 text-center">
                    <button className="bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors text-lg">
                      Compare 1 Instruments
                    </button>
                  </div>
                </div>
              </div>
              
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

        {/* Client-side interactive component */}
        <CompareClient
          productSlugs={productSlugs}
          productIds={[]}
          initialData={null}
        />
      </div>
    </div>
  );
}
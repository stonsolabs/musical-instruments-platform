'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import type { ComparisonResponse, Product } from '@/types';
import { apiClient } from '@/lib/api';
import ComprehensiveComparison from '@/components/ComprehensiveComparison';
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

// Helper function to generate common specifications across products
const generateCommonSpecs = (products: Product[]): string[] => {
  if (products.length === 0) return [];
  
  // Get all specification keys from all products
  const allSpecs = new Set<string>();
  products.forEach(product => {
    if (product.specifications) {
      Object.keys(product.specifications).forEach(key => allSpecs.add(key));
    }
  });
  
  // Filter to only specs that appear in at least one product
  const commonSpecs = Array.from(allSpecs).filter(spec => {
    return products.some(product => 
      product.specifications && 
      product.specifications[spec] !== undefined && 
      product.specifications[spec] !== null &&
      product.specifications[spec] !== ''
    );
  });
  
  return commonSpecs.sort();
};

// Helper function to generate comparison matrix
const generateComparisonMatrix = (products: Product[]): {[spec: string]: {[productId: string]: any}} => {
  const matrix: {[spec: string]: {[productId: string]: any}} = {};
  const commonSpecs = generateCommonSpecs(products);
  
  commonSpecs.forEach(spec => {
    matrix[spec] = {};
    products.forEach(product => {
      const value = product.specifications && product.specifications[spec];
      matrix[spec][String(product.id)] = value || 'N/A';
    });
  });
  
  return matrix;
};

interface CompareClientProps {
  productSlugs: string[];
  productIds: number[];
  initialData: ComparisonResponse | null;
}

export default function CompareClient({ productSlugs, productIds, initialData }: CompareClientProps) {
  const [data, setData] = useState<ComparisonResponse | null>(initialData);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(!initialData && productSlugs.length >= 1);

  // Load data if not provided by server
  useEffect(() => {
    if (!initialData && productSlugs.length >= 1) {
      const loadData = async () => {
        try {
          // Fetch products directly using slugs
          console.log('🔍 Fetching products with slugs:', productSlugs);
          const response = await fetch(`/api/proxy/products?slugs=${productSlugs.join(',')}&limit=100`);
          console.log('📡 Response status:', response.status);
          
          if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ API Error:', errorText);
            throw new Error(`Failed to fetch products: ${response.status} ${response.statusText}`);
          }
          
          const productsData = await response.json();
          console.log('✅ Products data received:', productsData);
          
          if (!productsData.products || productsData.products.length === 0) {
            throw new Error('No products found for the provided slugs');
          }

          // Create comparison data structure
          const comparisonData: ComparisonResponse = {
            products: productsData.products,
            common_specs: generateCommonSpecs(productsData.products),
            comparison_matrix: generateComparisonMatrix(productsData.products),
            generated_at: new Date().toISOString()
          };
          
          setData(comparisonData);
          
          // Track comparison analytics
          if (typeof window !== 'undefined') {
            console.log('Comparison loaded:', comparisonData.products.map(p => p.name));
          }
        } catch (e) {
          setError('Failed to load comparison');
          console.error('Comparison error:', e);
        } finally {
          setLoading(false);
        }
      };
      loadData();
    }
  }, [productSlugs, productIds, initialData]);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading comparison...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">⚠️ {error}</div>
        <button 
          onClick={() => window.location.reload()} 
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  if (!data || data.products.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 mb-4">No comparison data available.</div>
        <Link 
          href="/products"
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Browse Products
        </Link>
      </div>
    );
  }

  // Handle single product display
  const isSingleProduct = data.products.length === 1;

  // Check if comparing across different categories
  const hasDifferentCategories = new Set(data.products.map(p => p.category.name)).size > 1;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid lg:grid-cols-6 gap-6 xl:gap-8">
        {/* Main Content */}
        <div className="lg:col-span-5">
          {/* Product Header Cards - Aligned with specs table */}
          <div className={`grid gap-6 mb-8 relative ${isSingleProduct ? 'grid-cols-1 max-w-2xl mx-auto' : 'grid-cols-1 md:grid-cols-2'}`}>
            {data.products.map((product, index) => (
              <div key={product.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                {/* VS indicator between cards */}
                {index === 0 && data.products.length > 1 && (
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 bg-white border border-gray-200 rounded-full px-4 py-2 shadow-md">
                    <span className="text-gray-600 font-semibold text-sm">VS</span>
                  </div>
                )}
                <div className="aspect-square bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg mb-4 flex items-center justify-center overflow-hidden">
                  {product.images && product.images.length > 0 ? (
                    <img 
                      src={product.images[0]} 
                      alt={product.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <span className="text-gray-400 text-4xl">🎸</span>
                  )}
                </div>
                
                <div className="space-y-3">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">{product.brand.name}</p>
                    <h3 className="font-semibold text-gray-900 line-clamp-2">{product.name}</h3>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {product.avg_rating > 0 && (
                        <>
                          <span className="text-yellow-500">★</span>
                          <span className="text-sm font-medium">{formatRating(product.avg_rating)}</span>
                          <span className="text-sm text-gray-500">({product.review_count})</span>
                        </>
                      )}
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-blue-600">{product.prices?.length || 0}</div>
                      <div className="text-xs text-gray-500">Store{product.prices?.length !== 1 ? 's' : ''}</div>
                    </div>
                  </div>

                  {/* Store Buttons - Show all available stores */}
                  <div className="space-y-2">
                    {product.prices && product.prices.length > 0 ? (
                      <>
                        {/* All Store Buttons */}
                        {product.prices.map((price) => {
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
                                Buy at {price.store.name}
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
                                Buy at {price.store.name}
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
                                Buy at {price.store.name}
                                {!price.is_available && ' (Out of Stock)'}
                              </a>
                            );
                          }
                        })}
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
                        <Link 
                          href={`/products/${product.slug}-${product.id}`}
                          className="block w-full text-center bg-gray-800 text-white py-2 rounded-lg hover:bg-gray-700 transition-colors text-sm"
                        >
                          View Details
                        </Link>
                      </>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Category Warning */}
          {hasDifferentCategories && (
            <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-yellow-800">
                    Cross-Category Comparison
                  </h3>
                  <div className="mt-2 text-sm text-yellow-700">
                    <p>
                      You're comparing products across different categories. 
                      Some specifications might not be directly comparable.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Promo Section */}
          <section className="py-4 mb-8">
            <div className="bg-gradient-to-r from-orange-400 to-red-500 rounded-lg p-6 text-white text-center">
              <h3 className="text-lg font-bold mb-2">🎉 Special Offers</h3>
              <p className="mb-4">Exclusive deals and promotions from our partner stores</p>
              <Link href="/deals" className="inline-block bg-white text-orange-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
                View All Deals
              </Link>
            </div>
          </section>

          {/* Specifications Comparison */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Specifications Comparison</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead>
                    <tr className="border-b border-gray-200 bg-gray-50">
                      <th className="text-left py-4 px-6 font-semibold text-gray-900 w-1/4 text-lg">Specification</th>
                      {data.products.map((product) => (
                        <th key={product.id} className="text-left py-4 px-6 font-semibold text-gray-900 text-lg">
                          <div className="flex items-center gap-2">
                            <span className="text-2xl">🎸</span>
                            <div>
                              <div className="font-bold">{product.brand.name}</div>
                              <div className="text-sm font-normal text-gray-600">{product.name}</div>
                            </div>
                          </div>
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {/* Basic Specifications */}
                    <tr className="border-b border-gray-100">
                      <td className="py-4 px-6 font-medium text-gray-900">Brand</td>
                      {data.products.map((product) => (
                        <td key={product.id} className="py-4 px-6 text-gray-700">{product.brand.name}</td>
                      ))}
                    </tr>
                    <tr className="border-b border-gray-100">
                      <td className="py-4 px-6 font-medium text-gray-900">Category</td>
                      {data.products.map((product) => (
                        <td key={product.id} className="py-4 px-6 text-gray-700">{product.category.name}</td>
                      ))}
                    </tr>
                    <tr className="border-b border-gray-100">
                      <td className="py-4 px-6 font-medium text-gray-900">Average Rating</td>
                      {data.products.map((product) => (
                        <td key={product.id} className="py-4 px-6 text-gray-700">
                          <div className="flex items-center gap-2">
                            <span className="text-yellow-500">★</span>
                            <span>{formatRating(product.avg_rating)}</span>
                            <span className="text-sm text-gray-500">({product.review_count} reviews)</span>
                          </div>
                        </td>
                      ))}
                    </tr>
                    <tr className="border-b border-gray-100">
                      <td className="py-4 px-6 font-medium text-gray-900">Available Stores</td>
                      {data.products.map((product) => (
                        <td key={product.id} className="py-4 px-6 text-gray-700">
                          <span className="font-semibold text-blue-600">{product.prices?.length || 0}</span> stores
                        </td>
                      ))}
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Stores Comparison */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mt-8">
            <div className="p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">🏪 Available Stores</h3>
              <div className="space-y-6">
                {data.products.map((product) => (
                  <div key={product.id} className="border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                        <span className="text-gray-500 text-lg">🎸</span>
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{product.brand.name} {product.name}</h3>
                        <p className="text-sm text-gray-600">Available at {product.prices?.length || 0} stores</p>
                      </div>
                    </div>
                    
                    {product.prices && product.prices.length > 0 ? (
                      <div className="space-y-3">
                        {product.prices.map((price) => (
                          <div key={price.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 bg-gray-100 rounded flex items-center justify-center">
                                <span className="text-gray-500 text-sm">🏪</span>
                              </div>
                              <div>
                                <p className="font-medium text-gray-900">{price.store.name}</p>
                                <p className="text-sm text-gray-600">
                                  Last checked: {new Date(price.last_checked).toLocaleDateString()}
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center gap-4">
                              <div className="text-right">
                                <div className="text-sm text-gray-500">
                                  {price.is_available ? 'In Stock' : 'Out of Stock'}
                                </div>
                              </div>
                              <a 
                                href={price.affiliate_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="bg-gray-800 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                              >
                                Buy Now
                              </a>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-gray-500">No stores available.</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Comprehensive AI-Generated Comparison */}
          <ComprehensiveComparison products={data.products} />

          {/* Add more to comparison */}
          <div className="mt-8">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Add More Instruments to Compare</h3>
              <div className="max-w-2xl">
                <p className="text-gray-600 mb-4">
                  Want to compare more instruments? Search and add them to your comparison.
                </p>
                <Link
                  href="/products"
                  className="inline-flex items-center px-6 py-3 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-600 hover:text-white transition-colors font-semibold"
                >
                  Browse All Products
                  <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Ad Sidebar */}
        <div className="lg:col-span-1">
          <div className="sticky top-24">
            <AdSidebar />
          </div>
        </div>
      </div>
    </div>
  );
}

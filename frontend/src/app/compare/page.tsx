'use client';

import React, { useEffect, useMemo, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import type { ComparisonResponse, Product } from '../../types';

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

// Inline API client
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = {
  async compareProducts(productIds: number[]): Promise<ComparisonResponse> {
    if (typeof window === 'undefined') {
      throw new Error('API calls are not available during build time');
    }
    
    const response = await fetch(`${API_BASE_URL}/api/v1/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(productIds),
    });
    
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  }
};

function ComparePageContent() {
  const searchParams = useSearchParams();
  const [data, setData] = useState<ComparisonResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState('specs');

  const ids = useMemo(() => {
    const q = searchParams.get('ids');
    if (!q) return [] as number[];
    return q.split(',').map((s) => Number(s)).filter((n) => Number.isFinite(n));
  }, [searchParams]);

  useEffect(() => {
    const run = async () => {
      if (ids.length < 2) {
        setLoading(false);
        return;
      }
      try {
        const res = await apiClient.compareProducts(ids);
        setData(res);
      } catch (e) {
        setError('Failed to load comparison');
      } finally {
        setLoading(false);
      }
    };
    run();
  }, [ids]);

  const bestPrice = (p: Product) => p.best_price ? formatPrice(p.best_price.price, p.best_price.currency) : (p.msrp_price ? formatPrice(p.msrp_price) : '—');

  const tabs = [
    { id: 'specs', label: 'Specifications', icon: '⚙️' },
    { id: 'prices', label: 'Prices', icon: '💰' },
    { id: 'reviews', label: 'Reviews', icon: '⭐' },
    { id: 'analysis', label: 'AI Analysis', icon: '🤖' },
  ];

  if (ids.length < 2) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Compare Products</h1>
            <p className="text-gray-600 mb-8">Select at least two products to compare</p>
            <Link href="/" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
              Go to Homepage
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Check if comparing across different categories
  const hasDifferentCategories = data?.products && new Set(data.products.map(p => p.category.name)).size > 1;

  return (
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
        <nav className="mb-6">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
            <li>/</li>
            <li className="text-gray-900">Compare</li>
          </ol>
        </nav>

        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading comparison...</p>
          </div>
        )}

        {error && (
          <div className="text-center py-12">
            <div className="text-red-600 mb-4">⚠️ {error}</div>
            <button 
              onClick={() => window.location.reload()} 
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        )}

        {!loading && !error && data && (
          <>
            {/* Product Header Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {data.products.map((product) => (
                <div key={product.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <div className="aspect-square bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg mb-4 flex items-center justify-center">
                    <span className="text-gray-400 text-4xl">🎸</span>
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
                      <span className="text-lg font-bold text-green-600">{bestPrice(product)}</span>
                    </div>

                    <div className="flex gap-2">
                      <Link 
                        href={`/products/${product.slug}-${product.id}`}
                        className="flex-1 text-center bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm"
                      >
                        View Details
                      </Link>
                      <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                        Swap
                      </button>
                    </div>

                    {/* Store buttons */}
                    {product.best_price && (
                      <div className="mt-4">
                        <p className="text-sm font-medium text-gray-700 mb-2">Find it on:</p>
                        <a 
                          href={product.best_price.affiliate_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block w-full bg-orange-500 text-white text-center py-2 rounded-lg hover:bg-orange-600 transition-colors text-sm font-medium"
                        >
                          Thomann - {bestPrice(product)}
                        </a>
                      </div>
                    )}

                    {/* User interaction buttons */}
                    <div className="flex gap-2 mt-4">
                      <button className="flex-1 py-2 px-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                        Had ✓
                      </button>
                      <button className="flex-1 py-2 px-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                        Have ✓
                      </button>
                      <button className="flex-1 py-2 px-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                        Want ❤
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Ad Space - Middle */}
            <section className="py-4 mb-8">
              <div className="bg-gradient-to-r from-green-400 to-blue-500 rounded-lg p-6 text-white text-center">
                <h3 className="text-lg font-bold mb-2">🎵 Price Alert</h3>
                <p className="mb-4">Get notified when prices drop on these instruments</p>
                <button className="bg-white text-green-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
                  Set Alert
                </button>
              </div>
            </section>

            {/* Comparison Tabs */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              {/* Tab Navigation */}
              <div className="border-b border-gray-200">
                <nav className="flex space-x-8 px-6">
                  {tabs.map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                        activeTab === tab.id
                          ? 'border-blue-500 text-blue-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }`}
                    >
                      <span className="mr-2">{tab.icon}</span>
                      {tab.label}
                    </button>
                  ))}
                </nav>
              </div>

              {/* Tab Content */}
              <div className="p-6">
                {activeTab === 'specs' && (
                  <div className="overflow-x-auto">
                    <table className="min-w-full">
                      <thead>
                        <tr className="border-b border-gray-200 bg-gray-50">
                          <th className="text-left py-3 px-4 font-semibold text-gray-900 w-1/4">Specification</th>
                          {data.products.map((product) => (
                            <th key={product.id} className="text-left py-3 px-4 font-semibold text-gray-900">
                              {product.name}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {/* Basic Product Info */}
                        <tr className="border-b border-gray-100 bg-gray-50">
                          <td className="py-3 px-4 font-medium text-gray-700">Brand</td>
                          {data.products.map((product) => (
                            <td key={product.id} className="py-3 px-4 text-gray-900">{product.brand.name}</td>
                          ))}
                        </tr>
                        <tr className="border-b border-gray-100">
                          <td className="py-3 px-4 font-medium text-gray-700">Category</td>
                          {data.products.map((product) => (
                            <td key={product.id} className="py-3 px-4 text-gray-900">{product.category.name}</td>
                          ))}
                        </tr>
                        <tr className="border-b border-gray-100 bg-gray-50">
                          <td className="py-3 px-4 font-medium text-gray-700">SKU</td>
                          {data.products.map((product) => (
                            <td key={product.id} className="py-3 px-4 text-gray-900">{product.sku}</td>
                          ))}
                        </tr>
                        <tr className="border-b border-gray-100">
                          <td className="py-3 px-4 font-medium text-gray-700">Average Rating</td>
                          {data.products.map((product) => (
                            <td key={product.id} className="py-3 px-4 text-gray-900">
                              {product.avg_rating > 0 ? (
                                <div className="flex items-center gap-1">
                                  <span className="text-yellow-500">★</span>
                                  <span>{formatRating(product.avg_rating)}</span>
                                </div>
                              ) : '—'}
                            </td>
                          ))}
                        </tr>
                        <tr className="border-b border-gray-100 bg-gray-50">
                          <td className="py-3 px-4 font-medium text-gray-700">Review Count</td>
                          {data.products.map((product) => (
                            <td key={product.id} className="py-3 px-4 text-gray-900">{product.review_count}</td>
                          ))}
                        </tr>
                        <tr className="border-b border-gray-100">
                          <td className="py-3 px-4 font-medium text-gray-700">MSRP</td>
                          {data.products.map((product) => (
                            <td key={product.id} className="py-3 px-4 text-gray-900">
                              {product.msrp_price ? formatPrice(product.msrp_price) : '—'}
                            </td>
                          ))}
                        </tr>
                        <tr className="border-b border-gray-100 bg-gray-50">
                          <td className="py-3 px-4 font-medium text-gray-700">Best Price</td>
                          {data.products.map((product) => (
                            <td key={product.id} className="py-3 px-4 text-gray-900">
                              {product.best_price ? formatPrice(product.best_price.price, product.best_price.currency) : '—'}
                            </td>
                          ))}
                        </tr>
                        <tr className="border-b border-gray-100">
                          <td className="py-3 px-4 font-medium text-gray-700">Status</td>
                          {data.products.map((product) => (
                            <td key={product.id} className="py-3 px-4 text-gray-900">
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                product.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                              }`}>
                                {product.is_active ? 'Active' : 'Inactive'}
                              </span>
                            </td>
                          ))}
                        </tr>
                        <tr className="border-b border-gray-100 bg-gray-50">
                          <td className="py-3 px-4 font-medium text-gray-700">Created</td>
                          {data.products.map((product) => (
                            <td key={product.id} className="py-3 px-4 text-gray-900">
                              {new Date(product.created_at).toLocaleDateString()}
                            </td>
                          ))}
                        </tr>
                        <tr className="border-b border-gray-100">
                          <td className="py-3 px-4 font-medium text-gray-700">Last Updated</td>
                          {data.products.map((product) => (
                            <td key={product.id} className="py-3 px-4 text-gray-900">
                              {new Date(product.updated_at).toLocaleDateString()}
                            </td>
                          ))}
                        </tr>

                        {/* Specifications */}
                        {data.common_specs.map((spec, index) => (
                          <tr key={spec} className={`border-b border-gray-100 ${index % 2 === 0 ? 'bg-gray-50' : ''}`}>
                            <td className="py-3 px-4 font-medium text-gray-700 capitalize">
                              {spec.replace(/_/g, ' ')}
                            </td>
                            {data.products.map((product) => (
                              <td key={product.id} className="py-3 px-4 text-gray-900">
                                {String(data.comparison_matrix[spec]?.[String(product.id)] ?? 'N/A')}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}

                {activeTab === 'prices' && (
                  <div className="space-y-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Detailed Price Comparison</h3>
                    {data.products.map((product) => (
                      <div key={product.id} className="border border-gray-200 rounded-lg p-4">
                        <h4 className="font-medium text-gray-900 mb-3">{product.name}</h4>
                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {product.prices && product.prices.length > 0 ? (
                            product.prices.map((price) => (
                              <div key={price.id} className="border border-gray-200 rounded-lg p-3">
                                <div className="flex items-center justify-between mb-2">
                                  <span className="font-medium text-gray-900">{price.store.name}</span>
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                    price.is_available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                  }`}>
                                    {price.is_available ? 'In Stock' : 'Out of Stock'}
                                  </span>
                                </div>
                                <div className="text-lg font-bold text-green-600 mb-2">
                                  {formatPrice(price.price, price.currency)}
                                </div>
                                <div className="text-xs text-gray-500 mb-3">
                                  Last checked: {new Date(price.last_checked).toLocaleDateString()}
                                </div>
                                <a 
                                  href={price.affiliate_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="block w-full text-center bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm"
                                >
                                  Buy at {price.store.name}
                                </a>
                              </div>
                            ))
                          ) : (
                            <div className="col-span-full text-center py-8 text-gray-500">
                              No price information available for this product.
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'reviews' && (
                  <div className="space-y-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">User Reviews</h3>
                    {data.products.map((product) => (
                      <div key={product.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="font-medium text-gray-900">{product.name}</h4>
                          <div className="flex items-center gap-2">
                            <span className="text-yellow-500">★</span>
                            <span className="font-medium">{formatRating(product.avg_rating)}</span>
                            <span className="text-gray-500">({product.review_count} reviews)</span>
                          </div>
                        </div>
                        <p className="text-gray-600 text-sm">
                          {product.ai_content?.summary || "This instrument has received positive reviews from musicians worldwide."}
                        </p>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'analysis' && (
                  <div className="space-y-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Analysis</h3>
                    {data.products.map((product) => (
                      <div key={product.id} className="border border-gray-200 rounded-lg p-4">
                        <h4 className="font-medium text-gray-900 mb-3">{product.name}</h4>
                        <div className="space-y-3">
                          {product.ai_content?.pros && (
                            <div>
                              <h5 className="text-sm font-medium text-green-700 mb-1">Pros:</h5>
                              <p className="text-sm text-gray-700">{product.ai_content.pros}</p>
                            </div>
                          )}
                          {product.ai_content?.cons && (
                            <div>
                              <h5 className="text-sm font-medium text-red-700 mb-1">Cons:</h5>
                              <p className="text-sm text-gray-700">{product.ai_content.cons}</p>
                            </div>
                          )}
                          {product.ai_content?.summary && (
                            <div>
                              <h5 className="text-sm font-medium text-blue-700 mb-1">Summary:</h5>
                              <p className="text-sm text-gray-700">{product.ai_content.summary}</p>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Add more to comparison */}
            <div className="mt-8 text-center">
              <Link 
                href="/products"
                className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 font-medium"
              >
                <span>Add more to comparison</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default function ComparePage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ComparePageContent />
    </Suspense>
  );
}



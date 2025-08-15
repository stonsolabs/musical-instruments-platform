'use client';

import React, { useEffect, useMemo, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import type { Product } from '@/types';
import { trackProductView, trackEvent } from '@/components/Analytics';
import { getApiBaseUrl } from '@/lib/api';

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

const API_BASE_URL = getApiBaseUrl();

const apiClient = {
  async getProduct(productId: number): Promise<Product> {
    if (typeof window === 'undefined') {
      throw new Error('API calls are not available during build time');
    }
    
    const response = await fetch(`${API_BASE_URL}/api/v1/products/${productId}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  }
};

export default function ProductDetailPage() {
  const params = useParams();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedImage, setSelectedImage] = useState(0);
  const [activeTab, setActiveTab] = useState('overview');

  const productId = useMemo(() => {
    const slug = (params?.slug as string) || '';
    const idPart = slug.split('-').pop();
    const idNum = Number(idPart);
    return Number.isFinite(idNum) ? idNum : null;
  }, [params?.slug]);

  useEffect(() => {
    const load = async () => {
      if (!productId) {
        setError('Invalid product ID');
        setLoading(false);
        return;
      }
      try {
        const data = await apiClient.getProduct(productId);
        setProduct(data);
        
        // Track product view
        trackProductView(
          data.id.toString(),
          data.name,
          data.category?.name || 'unknown',
          data.best_price?.price
        );
      } catch (e) {
        setError('Product not found');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [productId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto" />
          <p className="mt-4 text-gray-600">Loading product...</p>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Product Not Found</h1>
          <Link href="/products" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">Browse All Products</Link>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📋' },
    { id: 'specs', label: 'Specifications', icon: '⚙️' },
    { id: 'prices', label: 'Prices', icon: '💰' },
    { id: 'reviews', label: 'Reviews', icon: '⭐' },
    { id: 'ai-analysis', label: 'AI Analysis', icon: '🤖' },
  ];

  const bestPrice = product.best_price ? formatPrice(product.best_price.price, product.best_price.currency) : 
                   product.msrp_price ? formatPrice(product.msrp_price) : '—';

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
        <nav className="flex items-center space-x-2 text-sm text-gray-600 mb-6">
          <Link href="/" className="hover:text-blue-600">Home</Link>
          <span>/</span>
          <Link href="/products" className="hover:text-blue-600">Products</Link>
          <span>/</span>
          <Link href={`/products?category=${product.category.slug}`} className="hover:text-blue-600">{product.category.name}</Link>
          <span>/</span>
          <span className="text-gray-900">{product.name}</span>
        </nav>

        {/* Product Header */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-8">
          <div className="grid lg:grid-cols-2 gap-8 p-8">
            {/* Images */}
            <div>
              <div className="aspect-square bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg overflow-hidden mb-4 flex items-center justify-center">
                <span className="text-gray-400 text-6xl">🎸</span>
              </div>
              {product.images?.length > 0 && (
                <div className="flex items-center gap-2 overflow-x-auto">
                  {product.images.map((img, idx) => (
                    <button 
                      key={idx} 
                      onClick={() => setSelectedImage(idx)} 
                      className={`w-16 h-16 rounded border-2 flex-shrink-0 ${
                        idx === selectedImage ? 'border-blue-600' : 'border-gray-200'
                      }`}
                    >
                      <div className="w-full h-full bg-gray-100 rounded flex items-center justify-center">
                        <span className="text-gray-400 text-sm">{idx + 1}</span>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Product Info */}
            <div className="space-y-6">
              <div>
                <div className="flex items-center gap-4 mb-3">
                  <Link href={`/products?brand=${product.brand.slug}`} className="text-blue-600 hover:text-blue-800 font-medium">
                    {product.brand.name}
                  </Link>
                  <span className="text-sm text-gray-500">SKU: {product.sku}</span>
                </div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
                <div className="flex items-center gap-4">
                  {product.avg_rating > 0 && (
                    <div className="flex items-center gap-2">
                      <span className="text-yellow-500">★</span>
                      <span className="font-medium">{formatRating(product.avg_rating)}</span>
                      <span className="text-gray-500">({product.review_count} reviews)</span>
                    </div>
                  )}
                  <span className="text-sm text-gray-600">{product.category.name}</span>
                </div>
              </div>

              {/* Best Price */}
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-green-700 font-medium">Best Price</p>
                    <p className="text-2xl font-bold text-green-600">{bestPrice}</p>
                  </div>
                  {product.best_price && (
                    <a 
                      href={product.best_price.affiliate_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors"
                    >
                      Buy Now
                    </a>
                  )}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="flex gap-3">
                <Link 
                  href={`/compare?ids=${product.id}`}
                  className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors text-center font-medium"
                >
                  Compare
                </Link>
                <button className="px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                  Add to List
                </button>
                <button className="px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                  ❤
                </button>
              </div>

              {/* Description */}
              {product.description && (
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Description</h3>
                  <p className="text-gray-700 leading-relaxed">{product.description}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Tabs */}
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
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* AI Summary */}
                {product.ai_content?.summary && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h3 className="font-semibold text-blue-900 mb-2">AI Summary</h3>
                    <p className="text-blue-800">{product.ai_content.summary}</p>
                  </div>
                )}

                {/* Key Specifications */}
                {product.specifications && Object.keys(product.specifications).length > 0 && (
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-4">Key Specifications</h3>
                    <div className="grid md:grid-cols-2 gap-4">
                      {Object.entries(product.specifications).slice(0, 8).map(([key, value]) => (
                        <div key={key} className="flex justify-between py-2 border-b border-gray-100">
                          <span className="font-medium text-gray-700 capitalize">{key.replace(/_/g, ' ')}</span>
                          <span className="text-gray-900">{String(value)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Product Details */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-3">Product Details</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Brand:</span>
                        <span className="font-medium">{product.brand.name}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Category:</span>
                        <span className="font-medium">{product.category.name}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">SKU:</span>
                        <span className="font-medium">{product.sku}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Added:</span>
                        <span className="font-medium">{new Date(product.created_at).toLocaleDateString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Last Updated:</span>
                        <span className="font-medium">{new Date(product.updated_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="font-semibold text-gray-900 mb-3">Rating & Reviews</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Average Rating:</span>
                        <div className="flex items-center gap-1">
                          <span className="text-yellow-500">★</span>
                          <span className="font-medium">{formatRating(product.avg_rating)}</span>
                        </div>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Review Count:</span>
                        <span className="font-medium">{product.review_count}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">MSRP:</span>
                        <span className="font-medium">{product.msrp_price ? formatPrice(product.msrp_price) : '—'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Status:</span>
                        <span className={`font-medium ${product.is_active ? 'text-green-600' : 'text-red-600'}`}>
                          {product.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'specs' && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-4">Full Specifications</h3>
                {product.specifications && Object.keys(product.specifications).length > 0 ? (
                  <div className="grid md:grid-cols-2 gap-4">
                    {Object.entries(product.specifications).map(([key, value]) => (
                      <div key={key} className="flex justify-between py-3 border-b border-gray-100">
                        <span className="font-medium text-gray-700 capitalize">{key.replace(/_/g, ' ')}</span>
                        <span className="text-gray-900">{String(value)}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No specifications available for this product.</p>
                )}
              </div>
            )}

            {activeTab === 'prices' && (
              <div className="space-y-6">
                <h3 className="font-semibold text-gray-900 mb-4">Price Comparison</h3>
                {product.prices && product.prices.length > 0 ? (
                  <div className="space-y-4">
                    {product.prices.map((price, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-4">
                            <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                              <span className="text-gray-500 text-lg">🏪</span>
                            </div>
                            <div>
                              <h4 className="font-medium text-gray-900">{price.store.name}</h4>
                              <p className="text-sm text-gray-600">
                                Last checked: {new Date(price.last_checked).toLocaleDateString()}
                              </p>
                            </div>
                          </div>
                          <div className="flex items-center gap-4">
                            <div className="text-right">
                              <div className="text-2xl font-bold text-green-600">
                                {formatPrice(price.price, price.currency)}
                              </div>
                              <div className="text-sm text-gray-500">
                                {price.is_available ? 'In Stock' : 'Out of Stock'}
                              </div>
                            </div>
                            <a 
                              href={price.affiliate_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                            >
                              Buy Now
                            </a>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No price information available for this product.</p>
                )}
              </div>
            )}

            {activeTab === 'reviews' && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-4">Reviews & Ratings</h3>
                <div className="bg-gray-50 rounded-lg p-6 text-center">
                  <div className="text-4xl mb-2">⭐</div>
                  <div className="text-2xl font-bold text-gray-900 mb-1">{formatRating(product.avg_rating)}</div>
                  <div className="text-gray-600 mb-4">Based on {product.review_count} reviews</div>
                  <p className="text-gray-500">Review system coming soon...</p>
                </div>
              </div>
            )}

            {activeTab === 'ai-analysis' && (
              <div className="space-y-6">
                <h3 className="font-semibold text-gray-900 mb-4">AI Analysis</h3>
                {product.ai_content ? (
                  <div className="space-y-4">
                    {product.ai_content.summary && (
                      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <h4 className="font-medium text-blue-900 mb-2">Summary</h4>
                        <p className="text-blue-800">{product.ai_content.summary}</p>
                      </div>
                    )}
                    {product.ai_content.pros && (
                      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                        <h4 className="font-medium text-green-900 mb-2">Pros</h4>
                        <p className="text-green-800">{product.ai_content.pros}</p>
                      </div>
                    )}
                    {product.ai_content.cons && (
                      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                        <h4 className="font-medium text-red-900 mb-2">Cons</h4>
                        <p className="text-red-800">{product.ai_content.cons}</p>
                      </div>
                    )}
                    {product.ai_content.use_cases && (
                      <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                        <h4 className="font-medium text-purple-900 mb-2">Best Use Cases</h4>
                        <p className="text-purple-800">{product.ai_content.use_cases}</p>
                      </div>
                    )}
                    {product.ai_content.recommendations && (
                      <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                        <h4 className="font-medium text-orange-900 mb-2">Recommendations</h4>
                        <p className="text-orange-800">{product.ai_content.recommendations}</p>
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="text-gray-500">No AI analysis available for this product.</p>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}



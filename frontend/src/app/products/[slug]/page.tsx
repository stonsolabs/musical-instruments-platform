'use client';

import React, { useEffect, useMemo, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import type { Product } from '@/types';
import { trackProductView, trackEvent } from '@/components/Analytics';
import { getApiBaseUrl } from '@/lib/api';
import ComprehensiveProductDetails from '@/components/ComprehensiveProductDetails';
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

const API_BASE_URL = getApiBaseUrl();

const apiClient = {
  async getProduct(productId: number): Promise<Product> {
    if (typeof window === 'undefined') {
      throw new Error('API calls are not available during build time');
    }
    
    const response = await fetch(`/api/proxy/products/${productId}`);
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
                {product.images && product.images.length > 0 ? (
                  <img 
                    src={product.images[selectedImage]} 
                    alt={`${product.name} - Image ${selectedImage + 1}`}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <span className="text-gray-400 text-6xl">🎸</span>
                )}
              </div>
              {product.images && product.images.length > 0 && (
                <div className="flex items-center gap-2 overflow-x-auto">
                  {product.images.map((img, idx) => (
                    <button 
                      key={idx} 
                      onClick={() => setSelectedImage(idx)} 
                      className={`w-16 h-16 rounded border-2 flex-shrink-0 overflow-hidden ${
                        idx === selectedImage ? 'border-blue-600' : 'border-gray-200'
                      }`}
                    >
                      <img 
                        src={img} 
                        alt={`${product.name} thumbnail ${idx + 1}`}
                        className="w-full h-full object-cover"
                      />
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

              {/* Store Availability */}
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <div>
                  <p className="text-sm text-gray-700 font-medium mb-3">Available at {product.prices?.length || 0} Store{product.prices?.length !== 1 ? 's' : ''}</p>
                  {product.prices && product.prices.length > 0 ? (
                    <div className="space-y-2">
                      {product.prices.slice(0, 3).map((price) => {
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
                              {price.store.name}
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
                              {price.store.name}
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
                              {price.store.name}
                              {!price.is_available && ' (Out of Stock)'}
                            </a>
                          );
                        }
                      })}
                      {product.prices.length > 3 && (
                        <p className="text-xs text-gray-500 text-center">
                          +{product.prices.length - 3} more stores available
                        </p>
                      )}
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500">No stores available</p>
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

        {/* Comprehensive Product Details */}
        <ComprehensiveProductDetails product={product} />
      </div>
    </div>
  );
}

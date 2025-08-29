'use client';

import React, { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import dynamicImport from 'next/dynamic';
import { Product, SearchAutocompleteProduct } from '@/types';
import { getApiBaseUrl, getServerBaseUrl } from '@/lib/api';

// Lazy load heavy components
const UnifiedSearchAutocomplete = dynamicImport(() => import('@/components/UnifiedSearchAutocomplete'), {
  loading: () => <div className="animate-pulse h-12 bg-gray-200 rounded-lg"></div>
});
const AffiliateButton = dynamicImport(() => import('@/components/AffiliateButton'), {
  loading: () => <div className="animate-pulse h-10 bg-gray-200 rounded-lg"></div>
});

import { formatPrice } from '@/lib/utils';
import { apiClient } from '@/lib/api';

export default function HomePageClient() {
  const [selectedProducts, setSelectedProducts] = useState<SearchAutocompleteProduct[]>([null as any]);
  const [popularProducts, setPopularProducts] = useState<Product[]>([]);
  const [topRatedProducts, setTopRatedProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  // Load popular and top-rated products
  useEffect(() => {
    const loadProducts = async () => {
      try {
        console.log('🔍 Loading popular and top-rated products...');
        const [popular, topRated] = await Promise.all([
          apiClient.searchProducts({ page: 1, limit: 6, sort_by: 'popularity' }),
          apiClient.searchProducts({ page: 1, limit: 6, sort_by: 'rating' })
        ]);
        console.log('📊 Popular products loaded:', popular.products?.length || 0);
        console.log('📊 Top rated products loaded:', topRated.products?.length || 0);
        setPopularProducts(popular.products || []);
        setTopRatedProducts(topRated.products || []);
      } catch (error) {
        console.error('❌ Error loading products:', error);
        // Silent fail with empty arrays - better UX than console errors
        setPopularProducts([]);
        setTopRatedProducts([]);
      } finally {
        setLoading(false);
      }
    };
    loadProducts();
  }, []);

  const addSearchField = () => {
    if (selectedProducts.length < 5) {
      // Add an empty slot for a new product
      setSelectedProducts([...selectedProducts, null as any]);
    }
  };

  const removeSearchField = (index: number) => {
    if (selectedProducts.length > 1) {
      const newProducts = selectedProducts.filter((_, i) => i !== index);
      setSelectedProducts(newProducts);
    }
  };

  const handleProductSelect = (index: number, product: SearchAutocompleteProduct) => {
    const newProducts = [...selectedProducts];
    newProducts[index] = product;
    setSelectedProducts(newProducts);
  };

  const handleCompare = () => {
    const validProducts = selectedProducts.filter(product => product !== null);
    if (validProducts.length >= 1) {
      // Create URL with product slugs for SEO (user only sees slugs)
      const productSlugs = validProducts.map(product => product.slug);
      const slugsString = productSlugs.join(',');
      window.location.href = `/compare?products=${slugsString}`;
    }
  };

  // Popular comparisons using real products from database
  const popularComparisons = [
    { 
      title: 'Fender Player Stratocaster vs Gibson Les Paul Studio', 
      products: 'fender-player-stratocaster-mim,gibson-les-paul-studio-ebony', 
      category: 'Electric Guitars',
      description: 'Compare two iconic electric guitars perfect for beginners and intermediate players'
    },
    { 
      title: 'Roland FP-30X vs Yamaha P-125a Digital Piano', 
      products: 'roland-fp-30x-digital-piano,yamaha-p-125a-digital-piano', 
      category: 'Pianos & Keyboards',
      description: 'Find the perfect digital piano for your home studio or practice space'
    },
    { 
      title: 'Taylor 214ce vs Martin D-28 Standard', 
      products: 'taylor-214ce-grand-auditorium,martin-d-28-standard', 
      category: 'Acoustic Guitars',
      description: 'Compare premium acoustic guitars for serious musicians'
    },
    { 
      title: 'Roland TD-17KV vs Alesis Nitro Mesh Kit', 
      products: 'roland-td-17kv-electronic-drum-kit,alesis-nitro-mesh-kit', 
      category: 'Drums & Percussion',
      description: 'Choose the right electronic drum kit for your practice needs'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-accent-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-gradient-to-r from-primary-600/10 to-accent-600/10"></div>
        
        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-primary-900 mb-6">
              Find Your Perfect
              <span className="block text-accent-600">Musical Instrument</span>
            </h1>
            <p className="text-xl text-primary-700 mb-8 max-w-3xl mx-auto">
              Compare prices, read expert reviews, and discover the best deals on musical instruments from Europe's top retailers.
            </p>

            {/* Product Comparison Tool */}
            <div className="bg-white rounded-2xl shadow-xl border border-primary-200 p-8 mb-12 max-w-4xl mx-auto">
              <h2 className="text-2xl font-bold text-primary-900 mb-6">Compare Instruments</h2>
              
              <div className="space-y-4 mb-6">
                {selectedProducts.map((product, index) => (
                  <div key={index} className="flex items-center gap-4">
                    <div className="flex-1">
                      <Suspense fallback={<div className="animate-pulse h-12 bg-gray-200 rounded-lg"></div>}>
                        <UnifiedSearchAutocomplete
                          placeholder={`Search for instrument ${index + 1}...`}
                          onProductSelect={(selectedProduct) => handleProductSelect(index, selectedProduct)}
                          selectedProduct={product}
                        />
                      </Suspense>
                    </div>
                    {selectedProducts.length > 1 && (
                      <button
                        onClick={() => removeSearchField(index)}
                        className="p-2 text-primary-600 hover:text-primary-800 hover:bg-primary-100 rounded-lg transition-colors"
                        aria-label="Remove product"
                      >
                        ✕
                      </button>
                    )}
                  </div>
                ))}
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <button
                  onClick={addSearchField}
                  disabled={selectedProducts.length >= 5}
                  className="px-6 py-3 border-2 border-dashed border-primary-300 text-primary-600 hover:border-primary-400 hover:text-primary-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  + Add Another Instrument
                </button>
                <button
                  onClick={handleCompare}
                  disabled={selectedProducts.filter(p => p !== null).length < 1}
                  className="flex-1 bg-primary-600 text-white py-3 px-6 rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                >
                  Compare Instruments
                </button>
              </div>
            </div>

            {/* Popular Comparisons */}
            <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
              {popularComparisons.map((comparison, index) => (
                <Link
                  key={index}
                  href={`/compare?products=${comparison.products}`}
                  className="bg-white rounded-xl p-6 shadow-lg border border-primary-200 hover:shadow-xl transition-shadow text-left group"
                >
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="font-semibold text-primary-900 group-hover:text-primary-700 transition-colors">
                      {comparison.title}
                    </h3>
                    <span className="text-2xl">→</span>
                  </div>
                  <p className="text-sm text-primary-600 mb-2">{comparison.description}</p>
                  <span className="inline-block bg-primary-100 text-primary-700 text-xs px-2 py-1 rounded-full">
                    {comparison.category}
                  </span>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Popular Products Section */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-primary-900 text-center mb-12">Popular Instruments</h2>
          
          {loading ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-gray-100 rounded-xl p-6 animate-pulse">
                  <div className="h-48 bg-gray-200 rounded-lg mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {popularProducts.map((product) => (
                <Link
                  key={product.id}
                  href={`/products/${product.slug}-${product.id}`}
                  className="bg-white rounded-xl shadow-lg border border-primary-200 hover:shadow-xl transition-shadow group"
                >
                  <div className="aspect-square bg-gradient-to-br from-primary-100 to-primary-200 rounded-t-xl overflow-hidden flex items-center justify-center">
                    {product.images && product.images.length > 0 ? (
                      <img 
                        src={product.images[0]} 
                        alt={product.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    ) : (
                      <span className="text-primary-400 text-4xl">🎸</span>
                    )}
                  </div>
                  <div className="p-6">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-sm text-primary-600 font-medium">{product.brand.name}</span>
                      {product.avg_rating > 0 && (
                        <div className="flex items-center gap-1">
                          <span className="text-warning-500 text-sm">★</span>
                          <span className="text-sm text-primary-600">{product.avg_rating.toFixed(1)}</span>
                        </div>
                      )}
                    </div>
                    <h3 className="font-semibold text-primary-900 mb-2 group-hover:text-primary-700 transition-colors">
                      {product.name}
                    </h3>
                    <p className="text-sm text-primary-600 mb-3">{product.category.name}</p>
                    {product.best_price && (
                      <div className="flex items-center justify-between">
                        <span className="text-lg font-bold text-primary-900">
                          {formatPrice(product.best_price.price, product.best_price.currency)}
                        </span>
                        <span className="text-sm text-primary-600">from {product.best_price.store.name}</span>
                      </div>
                    )}
                  </div>
                </Link>
              ))}
            </div>
          )}
          
          <div className="text-center mt-12">
            <Link
              href="/products"
              className="inline-flex items-center gap-2 bg-primary-600 text-white px-8 py-3 rounded-lg hover:bg-primary-700 transition-colors font-medium"
            >
              Browse All Products
              <span>→</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Top Rated Products Section */}
      <section className="py-16 bg-primary-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-primary-900 text-center mb-12">Top Rated Instruments</h2>
          
          {loading ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-white rounded-xl p-6 animate-pulse shadow-lg">
                  <div className="h-48 bg-gray-200 rounded-lg mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {topRatedProducts.map((product) => (
                <Link
                  key={product.id}
                  href={`/products/${product.slug}-${product.id}`}
                  className="bg-white rounded-xl shadow-lg border border-primary-200 hover:shadow-xl transition-shadow group"
                >
                  <div className="aspect-square bg-gradient-to-br from-primary-100 to-primary-200 rounded-t-xl overflow-hidden flex items-center justify-center relative">
                    {product.images && product.images.length > 0 ? (
                      <img 
                        src={product.images[0]} 
                        alt={product.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    ) : (
                      <span className="text-primary-400 text-4xl">🎸</span>
                    )}
                    {product.avg_rating >= 4.5 && (
                      <div className="absolute top-2 right-2 bg-warning-500 text-white text-xs px-2 py-1 rounded-full font-medium">
                        ⭐ Top Rated
                      </div>
                    )}
                  </div>
                  <div className="p-6">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-sm text-primary-600 font-medium">{product.brand.name}</span>
                      {product.avg_rating > 0 && (
                        <div className="flex items-center gap-1">
                          <span className="text-warning-500 text-sm">★</span>
                          <span className="text-sm text-primary-600">{product.avg_rating.toFixed(1)}</span>
                          <span className="text-xs text-primary-500">({product.review_count})</span>
                        </div>
                      )}
                    </div>
                    <h3 className="font-semibold text-primary-900 mb-2 group-hover:text-primary-700 transition-colors">
                      {product.name}
                    </h3>
                    <p className="text-sm text-primary-600 mb-3">{product.category.name}</p>
                    {product.best_price && (
                      <div className="flex items-center justify-between">
                        <span className="text-lg font-bold text-primary-900">
                          {formatPrice(product.best_price.price, product.best_price.currency)}
                        </span>
                        <span className="text-sm text-primary-600">from {product.best_price.store.name}</span>
                      </div>
                    )}
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-primary-900 text-center mb-12">Why Choose Get Your Music Gear?</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🔍</span>
              </div>
              <h3 className="text-xl font-semibold text-primary-900 mb-3">Expert Reviews</h3>
              <p className="text-primary-600">Get detailed, AI-powered reviews and comparisons to make informed decisions.</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">💰</span>
              </div>
              <h3 className="text-xl font-semibold text-primary-900 mb-3">Best Prices</h3>
              <p className="text-primary-600">Compare prices from Europe's top music stores to find the best deals.</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">⚡</span>
              </div>
              <h3 className="text-xl font-semibold text-primary-900 mb-3">Quick Comparison</h3>
              <p className="text-primary-600">Compare up to 5 instruments side-by-side with detailed specifications.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}




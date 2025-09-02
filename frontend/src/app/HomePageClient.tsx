'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import dynamicNext from 'next/dynamic';
import { Product, SearchAutocompleteProduct } from '@/types';
import { CompactProductVoting } from '@/components/ProductVoting';
import { formatPrice } from '@/lib/utils';
import { apiClient } from '@/lib/api';

// Dynamic imports but WITH server-side rendering (no ssr: false)
const UnifiedSearchAutocomplete = dynamicNext(() => import('@/components/UnifiedSearchAutocomplete'), {
  loading: () => <div className="animate-pulse h-12 bg-white rounded-lg border border-gray-200"></div>
});
const AffiliateButton = dynamicNext(() => import('@/components/AffiliateButton'), {
  loading: () => <div className="animate-pulse h-10 bg-white rounded-lg border border-gray-200"></div>
});

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
      title: 'Fender Player Precision Bass vs Yamaha TRBX304', 
      products: 'fender-player-precision-bass,yamaha-trbx304-bass', 
      category: 'Bass Guitars',
      description: 'Entry-level bass guitars that deliver professional sound quality'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <section className="relative py-16 lg:py-24 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/10"></div>
        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 mb-6">
              Find Your Perfect 
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"> Instrument</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Compare musical instruments from top retailers, read expert reviews, and find the best deals on guitars, pianos, drums, and more.
            </p>
            
            {/* Multi-Product Comparison Interface */}
            <div className="max-w-4xl mx-auto mb-12">
              <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Compare Up to 5 Instruments</h2>
                
                {/* Search Fields */}
                <div className="space-y-4 mb-6">
                  {selectedProducts.map((product, index) => (
                    <div key={index} className="flex items-center gap-4">
                      <div className="flex-1">
                        <UnifiedSearchAutocomplete 
                          variant="product-select"
                          placeholder={`Search for instrument ${index + 1}...`}
                          className="w-full"
                          onProductSelect={(selectedProduct) => handleProductSelect(index, selectedProduct)}
                          selectedProduct={product}
                        />
                      </div>
                      {selectedProducts.length > 1 && (
                        <button
                          onClick={() => removeSearchField(index)}
                          className="p-2 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors"
                          aria-label="Remove search field"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                      )}
                    </div>
                  ))}
                </div>
                
                {/* Action Buttons */}
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                  {selectedProducts.length < 5 && (
                    <button
                      onClick={addSearchField}
                      className="flex items-center gap-2 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                      Add Another Instrument
                    </button>
                  )}
                  
                  <button
                    onClick={handleCompare}
                    disabled={selectedProducts.filter(p => p !== null).length < 1}
                    className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-lg"
                  >
                    Compare {selectedProducts.filter(p => p !== null).length} Instrument{selectedProducts.filter(p => p !== null).length !== 1 ? 's' : ''}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Popular Comparisons */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Popular Comparisons</h2>
            <p className="text-lg text-gray-600">See how the most sought-after instruments stack up against each other</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            {popularComparisons.map((comparison, index) => (
              <div key={index} className="bg-gray-50 rounded-xl p-6 hover:shadow-lg transition-shadow">
                <div className="mb-4">
                  <span className="text-sm font-medium text-blue-600 bg-blue-100 px-3 py-1 rounded-full">
                    {comparison.category}
                  </span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{comparison.title}</h3>
                <p className="text-gray-600 text-sm mb-4">{comparison.description}</p>
                <Link 
                  href={`/compare?products=${comparison.products}`}
                  className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium"
                >
                  Compare Now
                  <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Product Sections */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          {loading ? (
            <div className="animate-pulse">
              <div className="h-8 bg-gray-200 rounded w-64 mx-auto mb-4"></div>
              <div className="h-4 bg-gray-200 rounded w-96 mx-auto mb-12"></div>
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
          ) : (
            <>
              {/* Popular Products */}
              {popularProducts.length > 0 && (
                <div className="mb-16">
                  <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">Popular Instruments</h2>
                    <p className="text-lg text-gray-600">Most searched and compared instruments this month</p>
                  </div>
                  
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                    {popularProducts.slice(0, 6).map((product) => (
                      <div key={product.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
                        <div className="relative h-48 bg-gray-100">
                          {product.images && product.images.length > 0 && (
                            <Image
                              src={product.images[0].image_url}
                              alt={product.images[0].alt_text || product.name}
                              fill
                              className="object-cover"
                              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                            />
                          )}
                        </div>
                        
                        <div className="p-6">
                          <div className="mb-2">
                            <span className="text-xs font-medium text-blue-600 bg-blue-100 px-2 py-1 rounded-full">
                              {product.category.name}
                            </span>
                          </div>
                          
                          <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                            {product.name}
                          </h3>
                          
                          <p className="text-sm text-gray-600 mb-4">{product.brand.name}</p>
                          
                          {product.best_price && (
                            <div className="mb-4">
                              <div className="text-2xl font-bold text-green-600">
                                {formatPrice(product.best_price.price, product.best_price.currency)}
                              </div>
                              <div className="text-sm text-gray-500">
                                Best price from {product.best_price.store_name}
                              </div>
                            </div>
                          )}
                          
                          <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-2">
                              {product.avg_rating > 0 && (
                                <>
                                  <span className="text-yellow-500">★</span>
                                  <span className="text-sm font-medium">{product.avg_rating.toFixed(1)}</span>
                                  <span className="text-xs text-gray-500">({product.review_count})</span>
                                </>
                              )}
                            </div>
                            <CompactProductVoting
                              productId={product.id}
                              initialUpvotes={product.vote_stats?.thumbs_up_count || 0}
                              initialDownvotes={product.vote_stats?.thumbs_down_count || 0}
                            />
                          </div>
                          
                          <div className="flex gap-2">
                            <Link
                              href={`/products/${product.slug}-${product.id}`}
                              className="flex-1 text-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                            >
                              View Details
                            </Link>
                            {product.best_price && (
                              <AffiliateButton
                                store={product.best_price.store_name.toLowerCase().replace(/\s+/g, '_')}
                                href={product.best_price.affiliate_url}
                                className="px-4 py-2 text-sm"
                              >
                                Buy Now
                              </AffiliateButton>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="text-center">
                    <Link
                      href="/products?sort_by=popularity"
                      className="inline-flex items-center gap-2 px-6 py-3 bg-white text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium"
                    >
                      View All Popular Products
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </Link>
                  </div>
                </div>
              )}

              {/* Top-Rated Products */}
              {topRatedProducts.length > 0 && (
                <div>
                  <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">Top-Rated Instruments</h2>
                    <p className="text-lg text-gray-600">Customer favorites with the highest ratings</p>
                  </div>
                  
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                    {topRatedProducts.slice(0, 6).map((product) => (
                      <div key={product.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
                        <div className="relative h-48 bg-gray-100">
                          {product.images && product.images.length > 0 && (
                            <Image
                              src={product.images[0].image_url}
                              alt={product.images[0].alt_text || product.name}
                              fill
                              className="object-cover"
                              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                            />
                          )}
                        </div>
                        
                        <div className="p-6">
                          <div className="mb-2">
                            <span className="text-xs font-medium text-green-600 bg-green-100 px-2 py-1 rounded-full">
                              ⭐ Top Rated
                            </span>
                          </div>
                          
                          <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                            {product.name}
                          </h3>
                          
                          <p className="text-sm text-gray-600 mb-4">{product.brand.name}</p>
                          
                          {product.best_price && (
                            <div className="mb-4">
                              <div className="text-2xl font-bold text-green-600">
                                {formatPrice(product.best_price.price, product.best_price.currency)}
                              </div>
                              <div className="text-sm text-gray-500">
                                Best price from {product.best_price.store_name}
                              </div>
                            </div>
                          )}
                          
                          <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-2">
                              {product.avg_rating > 0 && (
                                <>
                                  <span className="text-yellow-500">★</span>
                                  <span className="text-sm font-medium">{product.avg_rating.toFixed(1)}</span>
                                  <span className="text-xs text-gray-500">({product.review_count})</span>
                                </>
                              )}
                            </div>
                            <CompactProductVoting
                              productId={product.id}
                              initialUpvotes={product.vote_stats?.thumbs_up_count || 0}
                              initialDownvotes={product.vote_stats?.thumbs_down_count || 0}
                            />
                          </div>
                          
                          <div className="flex gap-2">
                            <Link
                              href={`/products/${product.slug}-${product.id}`}
                              className="flex-1 text-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                            >
                              View Details
                            </Link>
                            {product.best_price && (
                              <AffiliateButton
                                store={product.best_price.store_name.toLowerCase().replace(/\s+/g, '_')}
                                href={product.best_price.affiliate_url}
                                className="px-4 py-2 text-sm"
                              >
                                Buy Now
                              </AffiliateButton>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="text-center">
                    <Link
                      href="/products?sort_by=rating"
                      className="inline-flex items-center gap-2 px-6 py-3 bg-white text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium"
                    >
                      View All Top-Rated Products
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </Link>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </section>

      {/* Categories Grid */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Shop by Category</h2>
            <p className="text-lg text-gray-600">Find the perfect instrument for your musical journey</p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {[
              { name: 'Electric Guitars', slug: 'electric-guitars', emoji: '🎸' },
              { name: 'Acoustic Guitars', slug: 'steel-string-acoustic-guitars', emoji: '🎼' },
              { name: 'Bass Guitars', slug: 'electric-basses', emoji: '🎸' },
              { name: 'Digital Pianos', slug: 'digital-pianos', emoji: '🎹' },
              { name: 'Keyboards', slug: 'keyboards', emoji: '🎹' },
              { name: 'Drum Sets', slug: 'drum-sets', emoji: '🥁' },
            ].map((category) => (
              <Link
                key={category.slug}
                href={`/products?category=${category.slug}`}
                className="group p-6 bg-gray-50 rounded-xl text-center hover:bg-blue-50 hover:border-blue-200 border border-transparent transition-all"
              >
                <div className="text-4xl mb-3">{category.emoji}</div>
                <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors text-sm">
                  {category.name}
                </h3>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
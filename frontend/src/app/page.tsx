'use client';

import React, { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import dynamicImport from 'next/dynamic';
import { Product, SearchAutocompleteProduct } from '@/types';
import { getApiBaseUrl, getServerBaseUrl } from '@/lib/api';

// Force dynamic rendering since this is a client component
export const dynamic = 'force-dynamic';

// Lazy load heavy components
const UnifiedSearchAutocomplete = dynamicImport(() => import('@/components/UnifiedSearchAutocomplete'), {
  loading: () => <div className="animate-pulse h-12 bg-gray-200 rounded-lg"></div>
});
const AffiliateButton = dynamicImport(() => import('@/components/AffiliateButton'), {
  loading: () => <div className="animate-pulse h-10 bg-gray-200 rounded-lg"></div>
});

import { formatPrice } from '@/lib/utils';
import { apiClient } from '@/lib/api';

export default function HomePage() {
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
      products: 'taylor-214ce-deluxe-grand-auditorium,martin-d-28-standard', 
      category: 'Acoustic Guitars',
      description: 'Discover the differences between these premium acoustic guitars'
    },
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-700 text-white hero-content" aria-labelledby="hero-heading">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left side - Text content */}
            <div className="text-center lg:text-left">
              <h1 id="hero-heading" className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
                Find Your Perfect Musical Instrument
              </h1>
              <p className="text-2xl md:text-3xl font-semibold mb-4">
                Expert Reviews, Detailed Comparisons, and Trusted Recommendations
              </p>
              <p className="text-xl text-gray-200 mb-8">
                Discover the ideal instrument for your musical journey with comprehensive reviews, detailed specifications, and expert guidance from trusted music retailers worldwide
              </p>
            </div>

            {/* Right side - Dynamic search interface */}
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20" role="search" aria-labelledby="compare-heading">
              <h2 id="compare-heading" className="text-2xl font-bold mb-6 text-center">Compare Instruments</h2>
              
              <div className="space-y-4">
                {selectedProducts.map((product, index) => (
                  <div key={index} className="relative">
                    <div className="flex items-center gap-3">
                      <div className="flex-1">
                        <UnifiedSearchAutocomplete
                          variant="product-select"
                          placeholder={`Search instrument ${index + 1}`}
                          className="w-full"
                          onProductSelect={(selectedProduct) => handleProductSelect(index, selectedProduct)}
                        />
                      </div>
                      {selectedProducts.length > 1 && (
                        <button
                          onClick={() => removeSearchField(index)}
                          className="w-8 h-8 rounded-full bg-red-500 text-white flex items-center justify-center hover:bg-red-600 transition-colors"
                        >
                          ×
                        </button>
                      )}
                    </div>
                    {index < selectedProducts.length - 1 && (
                      <div className="text-center text-white/80 text-sm font-medium mt-2">vs</div>
                    )}
                  </div>
                ))}
                
                {selectedProducts.length < 5 && (
                  <button
                    onClick={addSearchField}
                    className="w-full py-3 px-4 border-2 border-dashed border-white/40 rounded-lg text-white/80 hover:border-white/60 hover:text-white transition-colors"
                  >
                    + Add another instrument
                  </button>
                )}
              </div>

              <button
                onClick={handleCompare}
                className="w-full mt-6 bg-gray-800 hover:bg-gray-700 text-white font-semibold py-4 px-6 rounded-lg transition-colors"
              >
                Compare {selectedProducts.filter(product => product !== null).length} Instrument{selectedProducts.filter(product => product !== null).length !== 1 ? 's' : ''}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Ad Space - Top Banner */}
      <section className="py-6 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-orange-400 to-orange-600 rounded-lg p-6 text-white text-center">
            <h3 className="text-xl font-bold mb-2">🎵 Special Offer!</h3>
            <p className="mb-4">Get 15% off on all Fender guitars this month</p>
            <button className="bg-white text-orange-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
              Shop Now
            </button>
          </div>
        </div>
      </section>

      {/* Popular Instruments Right Now */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">Trending Musical Instruments</h2>
          {loading ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-white rounded-lg shadow-elegant border border-gray-200 p-6 animate-pulse">
                  <div className="h-48 bg-gray-200 rounded-lg mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-6 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {popularProducts.map((product, index) => (
                <div key={product.id} className="bg-white rounded-lg shadow-elegant border border-gray-200 p-6 hover:shadow-md transition-shadow">
                  <Link href={`/products/${product.slug}-${product.id}`} className="block">
                    <div className="h-48 bg-gray-200 rounded-lg mb-4 overflow-hidden">
                      {product.images && product.images.length > 0 ? (
                        <Image 
                          src={product.images[0]} 
                          alt={`${product.name} - ${product.brand?.name || 'Musical Instrument'}`}
                          width={400}
                          height={192}
                          className="w-full h-full object-contain hover:scale-105 transition-transform duration-300"
                          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                          priority={index < 3}
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center">
                          <span className="text-gray-400 text-2xl" role="img" aria-label="Musical instrument">🎸</span>
                        </div>
                      )}
                    </div>
                  </Link>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">{product.brand?.name || 'Brand'}</span>
                    <span className="text-sm text-gray-500">1000+ watching</span>
                  </div>
                  <Link href={`/products/${product.slug}-${product.id}`} className="block">
                    <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 hover:text-orange-600 transition-colors cursor-pointer">{product.name}</h3>
                  </Link>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <span className="text-yellow-500">★</span>
                      <span className="text-sm font-medium">{product.avg_rating?.toFixed(1) || '4.5'}</span>
                    </div>
                  </div>
                  <div className="space-y-2">
                    {product.prices && product.prices.length > 0 ? (
                      <>
                        {/* Show only stores that are actually associated with this product */}
                        {product.prices
                          .slice(0, 2) // Show max 2 stores to avoid clutter
                          .map((price) => {
                            const isThomann = price.store.name.toLowerCase().includes('thomann');
                            const isGear4Music = price.store.name.toLowerCase().includes('gear4music');
                            
                            if (isThomann) {
                              return (
                                <a
                                  key={price.id}
                                  href={price.affiliate_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className={`fp-table__button fp-table__button--thomann ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                                >
                                  <span>View Price at</span>
                                  <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" />
                                </a>
                              );
                            } else if (isGear4Music) {
                              return (
                                <a
                                  key={price.id}
                                  href={price.affiliate_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className={`fp-table__button fp-table__button--gear4music ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                                >
                                  <span>View Price at</span>
                                  <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" />
                                </a>
                              );
                            } else {
                              return (
                                <a 
                                  key={price.id}
                                  href={price.affiliate_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className={`fp-table__button ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                                >
                                  <span>View Price at</span>
                                  <span className="font-medium">{price.store.name}</span>
                                </a>
                              );
                            }
                          })
                        }
                        
                        {/* Show more stores link if there are more than 2 */}
                        {product.prices.length > 2 && (
                          <Link 
                            href={`/products/${product.slug}-${product.id}`}
                            className="block w-full text-center py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm"
                          >
                            View All {product.prices.length} Stores
                          </Link>
                        )}
                      </>
                    ) : (
                      <div className="space-y-2">
                        <a
                          href={`https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(product.name)}&aff=123`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="fp-table__button fp-table__button--thomann"
                        >
                          <span>View Price at</span>
                          <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" />
                        </a>
                        <a
                          href={`https://gear4music.com/search?search=${encodeURIComponent(product.name)}&aff=123`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="fp-table__button fp-table__button--gear4music"
                        >
                          <span>View Price at</span>
                          <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" />
                        </a>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Popular Comparisons */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">Popular Instrument Comparisons</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {popularComparisons.map((comparison, index) => (
              <Link
                key={index}
                href={`/compare?products=${comparison.products}`}
                className="group block bg-white rounded-xl shadow-elegant border border-gray-200 overflow-hidden hover:shadow-lg transition-all"
              >
                <div className="h-48 bg-gradient-to-br from-gray-500 to-orange-600 flex items-center justify-center relative overflow-hidden">
                  <div className="absolute inset-0 bg-black/10 group-hover:bg-black/20 transition-colors"></div>
                  <div className="text-white text-4xl font-bold relative z-10 group-hover:scale-110 transition-transform duration-300">VS</div>
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-xs font-semibold text-orange-600 uppercase tracking-wide">{comparison.category}</span>
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-orange-600 transition-colors">
                    {comparison.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4">
                    {comparison.description}
                  </p>
                  <div className="flex items-center text-orange-600 font-medium group-hover:text-orange-700">
                    Compare Now
                    <svg className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Ad Space - Middle Banner */}
      <section className="py-6 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-green-400 to-gray-500 rounded-lg p-6 text-white text-center">
            <h3 className="text-xl font-bold mb-2">🎵 Thomann Special</h3>
            <p className="mb-4">Free shipping on orders over €199</p>
            <button className="bg-white text-green-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
              Learn More
            </button>
          </div>
        </div>
      </section>

      {/* Top Rated Instruments */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">Highest Rated Instruments</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {topRatedProducts.slice(0, 3).map((product) => (
              <div key={product.id} className="bg-white rounded-lg shadow-elegant border border-gray-200 p-6">
                <Link href={`/products/${product.slug}-${product.id}`} className="block">
                  <div className="h-48 bg-gray-200 rounded-lg mb-4 overflow-hidden">
                    {product.images && product.images.length > 0 ? (
                      <Image 
                        src={product.images[0]} 
                        alt={`${product.name} - ${product.brand?.name || 'Musical Instrument'}`}
                        width={400}
                        height={192}
                        className="w-full h-full object-contain hover:scale-105 transition-transform duration-300"
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        loading="lazy"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <span className="text-gray-400 text-2xl" role="img" aria-label="Musical instrument">🎸</span>
                      </div>
                    )}
                  </div>
                </Link>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">{product.brand?.name || 'Brand'}</span>
                  <div className="flex items-center gap-1">
                    <span className="text-yellow-500">★★★★★</span>
                    <span className="text-sm font-medium">{product.avg_rating?.toFixed(1) || '4.8'}</span>
                  </div>
                </div>
                <Link href={`/products/${product.slug}-${product.id}`} className="block">
                  <h3 className="font-semibold text-gray-900 mb-2 hover:text-orange-600 transition-colors cursor-pointer">{product.name}</h3>
                </Link>
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                  {product.description || "Exceptional quality instrument with outstanding reviews from musicians worldwide."}
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">({product.review_count || 150} reviews)</span>
                </div>
                <div className="space-y-2 mt-4">
                  {product.prices && product.prices.length > 0 ? (
                    <>
                      {/* Show only stores that are actually associated with this product */}
                      {product.prices
                        .slice(0, 2) // Show max 2 stores to avoid clutter
                        .map((price) => {
                          const isThomann = price.store.name.toLowerCase().includes('thomann');
                          const isGear4Music = price.store.name.toLowerCase().includes('gear4music');
                          
                          if (isThomann) {
                            return (
                              <a
                                key={price.id}
                                href={price.affiliate_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className={`fp-table__button fp-table__button--thomann ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                              >
                                <span>View Price at</span>
                                <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" />
                              </a>
                            );
                          } else if (isGear4Music) {
                            return (
                              <a
                                key={price.id}
                                href={price.affiliate_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className={`fp-table__button fp-table__button--gear4music ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                              >
                                <span>View Price at</span>
                                <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" />
                              </a>
                            );
                          } else {
                            return (
                              <a 
                                key={price.id}
                                href={price.affiliate_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className={`fp-table__button ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                              >
                                <span>View Price at</span>
                                <span className="font-medium">{price.store.name}</span>
                              </a>
                            );
                          }
                        })
                      }
                      
                      {/* Show more stores link if there are more than 2 */}
                      {product.prices.length > 2 && (
                        <Link 
                          href={`/products/${product.slug}-${product.id}`}
                          className="block w-full text-center py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm"
                        >
                          View All {product.prices.length} Stores
                        </Link>
                      )}
                    </>
                  ) : (
                    <div className="space-y-2">
                      <a
                        href={`https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(product.name)}&aff=123`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="fp-table__button fp-table__button--thomann"
                      >
                        <span>View Price at</span>
                        <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" />
                      </a>
                      <a
                        href={`https://gear4music.com/search?search=${encodeURIComponent(product.name)}&aff=123`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="fp-table__button fp-table__button--gear4music"
                      >
                        <span>View Price at</span>
                        <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" />
                      </a>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}



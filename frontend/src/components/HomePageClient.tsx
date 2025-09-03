'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import dynamic from 'next/dynamic';
import { Product, SearchAutocompleteProduct } from '@/types';
import { CompactProductVoting } from '@/components/ProductVoting';
import { formatPrice } from '@/lib/utils';
import { apiClient } from '@/lib/api';

const UnifiedSearchAutocomplete = dynamic(() => import('@/components/UnifiedSearchAutocomplete'), {
  loading: () => <div className="animate-pulse h-12 bg-white rounded-lg border border-gray-200"></div>,
  ssr: false
});

interface HomePageClientProps {
  initialPopularProducts?: Product[];
  initialTopRatedProducts?: Product[];
}

export default function HomePageClient({ 
  initialPopularProducts = [], 
  initialTopRatedProducts = [] 
}: HomePageClientProps) {
  const [selectedProducts, setSelectedProducts] = useState<SearchAutocompleteProduct[]>([null as any]);
  const [popularProducts, setPopularProducts] = useState<Product[]>(initialPopularProducts);
  const [topRatedProducts, setTopRatedProducts] = useState<Product[]>(initialTopRatedProducts);
  const [loading, setLoading] = useState(initialPopularProducts.length === 0);

  // Load popular and top-rated products if not provided server-side
  useEffect(() => {
    // Only load client-side if we have no server-side data
    if (initialPopularProducts.length === 0 && initialTopRatedProducts.length === 0) {
      const loadProducts = async () => {
        try {
          console.log('🔍 Client-side fallback: Loading popular and top-rated products...');
          const [popular, topRated] = await Promise.all([
            apiClient.searchProducts({ page: 1, limit: 6, sort_by: 'popularity' }),
            apiClient.searchProducts({ page: 1, limit: 6, sort_by: 'rating' })
          ]);
          console.log('📊 Client-side: Popular products loaded:', popular.products?.length || 0);
          console.log('📊 Client-side: Top rated products loaded:', topRated.products?.length || 0);
          setPopularProducts(popular.products || []);
          setTopRatedProducts(topRated.products || []);
        } catch (error) {
          console.error('❌ Client-side error loading products:', error);
          setPopularProducts([]);
          setTopRatedProducts([]);
        } finally {
          setLoading(false);
        }
      };
      loadProducts();
    } else {
      // We have server-side data, use it and stop loading
      console.log('✅ Using server-side data:', { 
        popular: initialPopularProducts.length, 
        topRated: initialTopRatedProducts.length 
      });
      setLoading(false);
    }
  }, [initialPopularProducts.length, initialTopRatedProducts.length]);

  const addSearchField = () => {
    if (selectedProducts.length < 5) {
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
      <section className="bg-gradient-to-br from-primary-900 via-primary-800 to-primary-700 text-white hero-content" aria-labelledby="hero-heading">
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
              <p className="text-xl text-primary-200 mb-8">
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
                          className="w-8 h-8 rounded-full bg-error-500 text-white flex items-center justify-center hover:bg-error-600 transition-colors"
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
                className="w-full mt-6 bg-primary-800 hover:bg-primary-700 text-white font-semibold py-4 px-6 rounded-lg transition-colors"
              >
                Compare {selectedProducts.filter(product => product !== null).length} Instrument{selectedProducts.filter(product => product !== null).length !== 1 ? 's' : ''}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Ad Space - Top Banner */}
      <section className="py-6 bg-primary-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-accent-400 to-accent-600 rounded-lg p-6 text-white text-center">
            <h3 className="text-xl font-bold mb-2">🎵 Special Offer!</h3>
            <p className="mb-4">Get 15% off on all Fender guitars this month</p>
            <button className="bg-white text-accent-600 px-6 py-2 rounded-lg font-semibold hover:bg-primary-50 transition-colors">
              Shop Now
            </button>
          </div>
        </div>
      </section>

      {/* Popular Instruments Right Now */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-primary-900">Trending Musical Instruments</h2>
          {loading ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-white rounded-lg shadow-elegant border border-primary-200 p-6 animate-pulse">
                  <div className="h-64 bg-primary-200 rounded-lg mb-4"></div>
                  <div className="h-4 bg-primary-200 rounded mb-2"></div>
                  <div className="h-6 bg-primary-200 rounded mb-2"></div>
                  <div className="h-4 bg-primary-200 rounded"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {popularProducts.map((product, index) => (
                <div key={product.id} className="bg-white rounded-lg shadow-elegant border border-primary-200 p-6 hover:shadow-md transition-shadow">
                  <Link href={`/products/${product.slug}-${product.id}`} className="block">
                    <div className="h-64 bg-primary-200 rounded-lg mb-4 overflow-hidden">
                      {product.images && product.images.length > 0 ? (
                        <Image 
                          src={product.images[0]} 
                          alt={`${product.name} - ${product.brand?.name || 'Musical Instrument'}`}
                          width={400}
                          height={256}
                          className="w-full h-full object-contain hover:scale-105 transition-transform duration-300"
                          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                          priority={index < 3}
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center">
                          <span className="text-primary-400 text-2xl" role="img" aria-label="Musical instrument">🎸</span>
                        </div>
                      )}
                    </div>
                  </Link>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-primary-600">{product.brand?.name || 'Brand'}</span>
                    <span className="text-sm text-primary-500">1000+ watching</span>
                  </div>
                  <Link href={`/products/${product.slug}-${product.id}`} className="block">
                    <h3 className="font-semibold text-primary-900 mb-2 line-clamp-2 hover:text-accent-600 transition-colors cursor-pointer">{product.name}</h3>
                  </Link>
                  <div className="flex items-center justify-center mb-4">
                    <CompactProductVoting 
                      productId={product.id}
                      initialStats={product.vote_stats}
                      className=""
                    />
                  </div>
                  <div className="space-y-2">
                    {product.prices && product.prices.length > 0 ? (
                      <>
                        {product.prices
                          .slice(0, 2)
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
                                  <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
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
                                  <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
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
                        
                        {product.prices.length > 2 && (
                          <Link 
                            href={`/products/${product.slug}-${product.id}`}
                            className="block w-full text-center py-2 border border-primary-300 text-primary-700 rounded-lg hover:bg-primary-50 transition-colors text-sm"
                          >
                            View All {product.prices.length} Stores
                          </Link>
                        )}
                      </>
                    ) : (
                      <div className="space-y-2">
                        <a
                          href={product.content?.store_links?.['Thomann'] || product.content?.store_links?.['thomann'] || product.thomann_info?.url || `https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(product.name)}&aff=123`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="fp-table__button fp-table__button--thomann"
                        >
                          <span>View Price at</span>
                          <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" />
                        </a>
                        <a
                          href={product.content?.store_links?.['gear4music'] || product.content?.store_links?.['Gear4music'] || `https://gear4music.com/search?search=${encodeURIComponent(product.name)}&aff=123`}
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
      <section className="py-16 bg-primary-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-primary-900">Popular Instrument Comparisons</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {popularComparisons.map((comparison, index) => (
              <Link
                key={index}
                href={`/compare?products=${comparison.products}`}
                className="group block bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden hover:shadow-lg transition-all"
              >
                <div className="h-48 bg-white flex items-center justify-center relative overflow-hidden border border-gray-200">
                  <div className="absolute inset-0 bg-black/10 group-hover:bg-black/20 transition-colors"></div>
                  <div className="text-white text-4xl font-bold relative z-10 group-hover:scale-110 transition-transform duration-300">VS</div>
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-xs font-semibold text-accent-600 uppercase tracking-wide">{comparison.category}</span>
                  </div>
                  <h3 className="font-semibold text-primary-900 mb-2 group-hover:text-accent-600 transition-colors">
                    {comparison.title}
                  </h3>
                  <p className="text-primary-600 text-sm mb-4">
                    {comparison.description}
                  </p>
                  <div className="flex items-center text-accent-600 font-medium group-hover:text-accent-700">
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
          <div className="bg-gradient-to-r from-success-400 to-primary-500 rounded-lg p-6 text-white text-center">
            <h3 className="text-xl font-bold mb-2">🎵 Thomann Special</h3>
            <p className="mb-4">Free shipping on orders over €199</p>
            <button className="bg-white text-success-600 px-6 py-2 rounded-lg font-semibold hover:bg-primary-50 transition-colors">
              Learn More
            </button>
          </div>
        </div>
      </section>

      {/* Top Rated Instruments */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-primary-900">Highest Rated Instruments</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {topRatedProducts.slice(0, 3).map((product) => (
              <div key={product.id} className="bg-white rounded-lg shadow-elegant border border-primary-200 p-6">
                <Link href={`/products/${product.slug}-${product.id}`} className="block">
                  <div className="h-64 bg-primary-200 rounded-lg mb-4 overflow-hidden">
                    {product.images && product.images.length > 0 ? (
                      <Image 
                        src={product.images[0]} 
                        alt={`${product.name} - ${product.brand?.name || 'Musical Instrument'}`}
                        width={400}
                        height={256}
                        className="w-full h-full object-contain hover:scale-105 transition-transform duration-300"
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        loading="lazy"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <span className="text-primary-400 text-2xl" role="img" aria-label="Musical instrument">🎸</span>
                      </div>
                    )}
                  </div>
                </Link>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-primary-600">{product.brand?.name || 'Brand'}</span>
                </div>
                <Link href={`/products/${product.slug}-${product.id}`} className="block">
                  <h3 className="font-semibold text-primary-900 mb-2 hover:text-accent-600 transition-colors cursor-pointer">{product.name}</h3>
                </Link>
                <p className="text-primary-600 text-sm mb-4 line-clamp-2">
                  {product.description || "Exceptional quality instrument with outstanding reviews from musicians worldwide."}
                </p>
                <div className="space-y-2 mt-4">
                  {product.prices && product.prices.length > 0 ? (
                    <>
                      {product.prices
                        .slice(0, 2)
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
                      
                      {product.prices.length > 2 && (
                        <Link 
                          href={`/products/${product.slug}-${product.id}`}
                          className="block w-full text-center py-2 border border-primary-300 text-primary-700 rounded-lg hover:bg-primary-50 transition-colors text-sm"
                        >
                          View All {product.prices.length} Stores
                        </Link>
                      )}
                    </>
                  ) : (
                    <div className="space-y-2">
                      <a
                        href={product.content?.store_links?.['Thomann'] || product.content?.store_links?.['thomann'] || product.thomann_info?.url || `https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(product.name)}&aff=123`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="fp-table__button fp-table__button--thomann"
                      >
                        <span>View Price at</span>
                        <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" />
                      </a>
                      <a
                        href={product.content?.store_links?.['gear4music'] || product.content?.store_links?.['Gear4music'] || `https://gear4music.com/search?search=${encodeURIComponent(product.name)}&aff=123`}
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
                <div className="flex items-center justify-between mt-4">
                  <span className="text-sm text-primary-500">({product.review_count || 150} reviews)</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Blog Section */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-primary-900 mb-4">Expert Instrument Guides & Reviews</h2>
            <p className="text-lg text-primary-600 max-w-2xl mx-auto">
              Discover comprehensive buying guides, detailed instrument reviews, and expert insights to help you make informed decisions
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                title: "Best Electric Guitars for Beginners in 2025",
                excerpt: "Discover the perfect electric guitar to start your musical journey with our comprehensive guide.",
                image: "/images/blog-electric-guitars.jpg",
                category: "Buying Guide",
                date: "Jan 15, 2025",
                href: "/blog/best-electric-guitars-beginners-2025"
              },
              {
                title: "How to Choose the Right Digital Piano",
                excerpt: "Everything you need to know about selecting the perfect digital piano for your needs and budget.",
                image: "/images/blog-digital-piano.jpg",
                category: "Buying Guide",
                date: "Jan 12, 2025",
                href: "/blog/how-choose-right-digital-piano"
              },
              {
                title: "Top 10 Studio Monitors Under €500",
                excerpt: "Professional-quality studio monitors that won't break the bank for home recording setups.",
                image: "/images/blog-studio-monitors.jpg",
                category: "Reviews",
                date: "Jan 10, 2025",
                href: "/blog/top-10-studio-monitors-under-500"
              }
            ].map((post, index) => (
              <Link
                key={index}
                href={post.href}
                className="group block bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden hover:shadow-lg hover:border-primary-300 transition-all duration-300"
              >
                <div className="h-48 bg-white flex items-center justify-center relative overflow-hidden border border-gray-200">
                  <div className="absolute inset-0 bg-black/10 group-hover:bg-black/20 transition-colors"></div>
                  <div className="text-white text-4xl font-bold relative z-10 group-hover:scale-110 transition-transform duration-300">
                    📝
                  </div>
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-xs font-semibold text-accent-600 uppercase tracking-wide">{post.category}</span>
                    <span className="text-xs text-primary-500">•</span>
                    <span className="text-xs text-primary-500">{post.date}</span>
                  </div>
                  <h3 className="text-xl font-bold text-primary-900 mb-3 group-hover:text-accent-600 transition-colors line-clamp-2">
                    {post.title}
                  </h3>
                  <p className="text-primary-600 mb-4 line-clamp-3">
                    {post.excerpt}
                  </p>
                  <div className="flex items-center text-accent-600 font-medium group-hover:text-accent-700">
                    Read More
                    <svg className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </Link>
            ))}
          </div>
          
          <div className="text-center mt-8">
            <Link
              href="/blog"
              className="inline-flex items-center px-6 py-3 border border-accent-600 text-accent-600 rounded-lg hover:bg-accent-600 hover:text-white transition-colors font-semibold"
            >
              View All Blog Posts
              <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="py-16 bg-primary-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4 text-primary-900">Stay Updated with the Latest</h2>
          <p className="text-primary-600 mb-8 text-lg">
            Get expert instrument reviews, buying guides, and industry insights delivered to your inbox
          </p>
          <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <input
              type="email"
              placeholder="Enter your email"
              className="flex-1 px-4 py-3 border border-primary-300 rounded-lg focus:ring-2 focus:ring-accent-500 focus:border-transparent"
            />
            <button className="bg-accent-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-accent-700 transition-colors">
              Subscribe
            </button>
          </div>
        </div>
      </section>

      {/* Ad Space - Bottom Banner */}
      <section className="py-6 bg-primary-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-accent-400 to-accent-600 rounded-lg p-6 text-white text-center">
            <h3 className="text-xl font-bold mb-2">🎵 Sale</h3>
            <p className="mb-4">Up to 40% off on selected instruments</p>
            <button className="bg-white text-accent-600 px-6 py-2 rounded-lg font-semibold hover:bg-primary-50 transition-colors">
              Shop Sale
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
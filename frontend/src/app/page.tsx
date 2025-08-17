'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Product, SearchAutocompleteProduct } from '@/types';
import { getApiBaseUrl } from '@/lib/api';
import ProductSearchAutocomplete from '@/components/ProductSearchAutocomplete';

// Force dynamic rendering since this is a client component
export const dynamic = 'force-dynamic';

const API_BASE_URL = getApiBaseUrl();

async function searchProducts(params: any): Promise<{ products: Product[] }> {
  if (typeof window === 'undefined') {
    // Return empty results during build
    return { products: [] };
  }
  
  try {
    const sp = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== '') sp.append(k, String(v));
    });
    
    const response = await fetch(`/api/proxy/products?${sp.toString()}`);
    if (!response.ok) throw new Error('Failed to fetch');
    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    return { products: [] };
  }
}

export default function HomePage() {
  const [selectedProducts, setSelectedProducts] = useState<SearchAutocompleteProduct[]>([null as any]);
  const [popularProducts, setPopularProducts] = useState<Product[]>([]);
  const [topRatedProducts, setTopRatedProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  // Load popular and top-rated products
  useEffect(() => {
    const loadProducts = async () => {
      try {
        const [popular, topRated] = await Promise.all([
          searchProducts({ page: 1, limit: 6, sort_by: 'popularity' }),
          searchProducts({ page: 1, limit: 6, sort_by: 'rating' })
        ]);
        setPopularProducts(popular.products);
        setTopRatedProducts(topRated.products);
      } catch (error) {
        console.error('Failed to load products:', error);
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

  // Pre-created popular comparisons (these would be populated with real data)
  const popularComparisons = [
    { title: 'Fender Stratocaster vs Gibson Les Paul', products: 'fender-stratocaster,gibson-les-paul', image: '/images/comparison-1.jpg' },
    { title: 'Yamaha vs Roland Keyboards', products: 'yamaha-keyboard,roland-keyboard', image: '/images/comparison-2.jpg' },
    { title: 'Pearl vs Tama Drums', products: 'pearl-drums,tama-drums', image: '/images/comparison-3.jpg' },
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-700 text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left side - Text content */}
            <div className="text-center lg:text-left">
              <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
                Search, compare, save
              </h1>
              <h2 className="text-2xl md:text-3xl font-semibold mb-4">
                Find your next instrument today
              </h2>
              <p className="text-xl text-gray-200 mb-8">
                At GetYourMusicGear you can compare prices on thousands of instruments from Europe's top music stores
              </p>
            </div>

            {/* Right side - Dynamic search interface */}
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
              <h3 className="text-2xl font-bold mb-6 text-center">Compare Instruments</h3>
              
              <div className="space-y-4">
                {selectedProducts.map((product, index) => (
                  <div key={index} className="relative">
                    <div className="flex items-center gap-3">
                      <div className="flex-1">
                        <ProductSearchAutocomplete
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

      {/* Shop by Category - Baum Guitars Style */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Shop by Category</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Explore our comprehensive collection of musical instruments across all categories
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { 
                name: 'Electric Guitars', 
                description: 'From classic to modern electric guitars',
                href: '/products?category=electric-guitars',
                image: '/images/electric-guitars.jpg',
                color: 'from-red-500 to-red-600'
              },
              { 
                name: 'Acoustic Guitars', 
                description: 'Beautiful acoustic and classical guitars',
                href: '/products?category=acoustic-guitars',
                image: '/images/acoustic-guitars.jpg',
                color: 'from-amber-500 to-amber-600'
              },
              { 
                name: 'Digital Keyboards', 
                description: 'Professional keyboards and pianos',
                href: '/products?category=digital-keyboards',
                image: '/images/keyboards.jpg',
                color: 'from-blue-500 to-blue-600'
              },
              { 
                name: 'Synthesizers', 
                description: 'Analog and digital synthesizers',
                href: '/products?category=synthesizers',
                image: '/images/synthesizers.jpg',
                color: 'from-purple-500 to-purple-600'
              },
              { 
                name: 'Amplifiers', 
                description: 'Guitar and bass amplifiers',
                href: '/products?category=amplifiers',
                image: '/images/amplifiers.jpg',
                color: 'from-green-500 to-green-600'
              },
              { 
                name: 'Audio Interfaces', 
                description: 'Professional audio recording gear',
                href: '/products?category=audio-interfaces',
                image: '/images/audio-interfaces.jpg',
                color: 'from-indigo-500 to-indigo-600'
              },
            ].map((category) => (
              <Link
                key={category.name}
                href={category.href}
                className="group block bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg hover:border-gray-300 transition-all duration-300"
              >
                <div className={`h-48 bg-gradient-to-br ${category.color} flex items-center justify-center relative overflow-hidden`}>
                  <div className="absolute inset-0 bg-black/10 group-hover:bg-black/20 transition-colors"></div>
                  <div className="text-white text-6xl font-bold relative z-10 group-hover:scale-110 transition-transform duration-300">
                    {category.name === 'Electric Guitars' && '🎸'}
                    {category.name === 'Acoustic Guitars' && '🎸'}
                    {category.name === 'Digital Keyboards' && '🎹'}
                    {category.name === 'Synthesizers' && '🎹'}
                    {category.name === 'Amplifiers' && '🔊'}
                    {category.name === 'Audio Interfaces' && '🎛️'}
                  </div>
                </div>
                <div className="p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                    {category.name}
                  </h3>
                  <p className="text-gray-600 mb-4">
                    {category.description}
                  </p>
                  <div className="flex items-center text-blue-600 font-medium group-hover:text-blue-700">
                    Shop {category.name}
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

      {/* Ad Space - Top Banner */}
      <section className="py-4 bg-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-orange-400 to-red-500 rounded-lg p-6 text-white text-center">
            <h3 className="text-xl font-bold mb-2">🎵 Special Offer!</h3>
            <p className="mb-4">Get 15% off on all Fender guitars this month</p>
            <button className="bg-white text-orange-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Shop Now
            </button>
          </div>
        </div>
      </section>

      {/* Popular Comparisons */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Popular Comparisons</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {popularComparisons.map((comparison, index) => (
              <Link
                key={index}
                href={`/compare?products=${comparison.products}`}
                className="group bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-all"
              >
                <div className="h-48 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                  <div className="text-white text-4xl font-bold">VS</div>
                </div>
                <div className="p-6">
                  <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                    {comparison.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4">
                    See detailed comparison of these popular instruments
                  </p>
                  <div className="flex items-center text-blue-600 font-medium">
                    Compare Now
                    <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
      <section className="py-4 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-green-400 to-blue-500 rounded-lg p-6 text-white text-center">
            <h3 className="text-xl font-bold mb-2">🎵 Thomann Special</h3>
            <p className="mb-4">Free shipping on orders over €199</p>
            <button className="bg-white text-green-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Learn More
            </button>
          </div>
        </div>
      </section>

      {/* Popular Products */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Popular Instruments Right Now</h2>
          {loading ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
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
                <div key={product.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                  <div className="h-48 bg-gray-200 rounded-lg mb-4 flex items-center justify-center">
                    <span className="text-gray-400 text-2xl">🎸</span>
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">{product.brand?.name || 'Brand'}</span>
                    <span className="text-sm text-gray-500">1000+ watching</span>
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">{product.name}</h3>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <span className="text-yellow-500">★</span>
                      <span className="text-sm font-medium">{product.avg_rating?.toFixed(1) || '4.5'}</span>
                    </div>
                  </div>
                  <div className="space-y-2">
                    {product.prices && product.prices.length > 0 ? (
                      <>
                        {/* All Store Buttons */}
                        {product.prices
                          .slice(0, 3) // Show max 3 stores to avoid clutter
                          .map((price) => (
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
                              €{price.price.toFixed(2)} at {price.store.name}
                              {!price.is_available && ' (Out of Stock)'}
                            </a>
                          ))
                        }
                        
                        {/* Show more stores link if there are more than 3 */}
                        {product.prices.length > 3 && (
                          <Link 
                            href={`/products/${product.slug}-${product.id}`}
                            className="block w-full text-center py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm"
                          >
                            View All {product.prices.length} Stores
                          </Link>
                        )}
                      </>
                    ) : (
                      <Link 
                        href={`/products/${product.slug}-${product.id}`}
                        className="block w-full text-center bg-gray-800 text-white py-2 rounded-lg hover:bg-gray-700 transition-colors"
                      >
                        View Details
                      </Link>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Top Rated Products with Reviews */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Top Rated Instruments</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {topRatedProducts.slice(0, 3).map((product) => (
              <div key={product.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="h-48 bg-gray-200 rounded-lg mb-4 flex items-center justify-center">
                  <span className="text-gray-400 text-2xl">🎸</span>
                </div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">{product.brand?.name || 'Brand'}</span>
                  <div className="flex items-center gap-1">
                    <span className="text-yellow-500">★★★★★</span>
                    <span className="text-sm font-medium">{product.avg_rating?.toFixed(1) || '4.8'}</span>
                  </div>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{product.name}</h3>
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                  {product.description || "Excellent quality instrument with outstanding reviews from musicians worldwide."}
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">({product.review_count || 150} reviews)</span>
                </div>
                <div className="space-y-2 mt-4">
                  {product.prices && product.prices.length > 0 ? (
                    <>
                      {/* All Store Buttons */}
                      {product.prices
                        .slice(0, 3) // Show max 3 stores to avoid clutter
                        .map((price) => (
                          <a 
                            key={price.id}
                            href={price.affiliate_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={`block w-full text-center py-2 rounded-lg transition-colors text-sm font-medium ${
                              price.is_available 
                                ? 'bg-blue-600 text-white hover:bg-blue-700' 
                                : 'bg-gray-300 text-gray-600 cursor-not-allowed'
                            }`}
                          >
                            €{price.price.toFixed(2)} at {price.store.name}
                            {!price.is_available && ' (Out of Stock)'}
                          </a>
                        ))
                      }
                      
                      {/* Show more stores link if there are more than 3 */}
                      {product.prices.length > 3 && (
                        <Link 
                          href={`/products/${product.slug}-${product.id}`}
                          className="block w-full text-center py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm"
                        >
                          View All {product.prices.length} Stores
                        </Link>
                      )}
                    </>
                  ) : (
                    <Link 
                      href={`/products/${product.slug}-${product.id}`}
                      className="block w-full text-center bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      View Details
                    </Link>
                  )}
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
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Latest from Our Blog</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Stay updated with the latest instrument reviews, buying guides, and industry insights
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
                className="group block bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg hover:border-gray-300 transition-all duration-300"
              >
                <div className="h-48 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center relative overflow-hidden">
                  <div className="absolute inset-0 bg-black/10 group-hover:bg-black/20 transition-colors"></div>
                  <div className="text-white text-4xl font-bold relative z-10 group-hover:scale-110 transition-transform duration-300">
                    📝
                  </div>
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">{post.category}</span>
                    <span className="text-xs text-gray-500">•</span>
                    <span className="text-xs text-gray-500">{post.date}</span>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors line-clamp-2">
                    {post.title}
                  </h3>
                  <p className="text-gray-600 mb-4 line-clamp-3">
                    {post.excerpt}
                  </p>
                  <div className="flex items-center text-blue-600 font-medium group-hover:text-blue-700">
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
              className="inline-flex items-center px-6 py-3 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-600 hover:text-white transition-colors font-semibold"
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
      <section className="py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Stay Updated</h2>
          <p className="text-gray-600 mb-8 text-lg">
            Get the latest instrument news, deals, and reviews delivered to your inbox
          </p>
          <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <input
              type="email"
              placeholder="Enter your email"
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
              Subscribe
            </button>
          </div>
        </div>
      </section>

      {/* Ad Space - Bottom Banner */}
      <section className="py-4 bg-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-purple-400 to-pink-500 rounded-lg p-6 text-white text-center">
            <h3 className="text-xl font-bold mb-2">🎵 Gear4Music Sale</h3>
            <p className="mb-4">Up to 40% off on selected instruments</p>
            <button className="bg-white text-purple-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Shop Sale
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}



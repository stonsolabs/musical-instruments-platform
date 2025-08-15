'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Product } from '../types';

// API client with proper environment variable handling
const getApiBaseUrl = (): string => {
  // Priority: Environment variable > window.location.origin (for production) > localhost (for development)
  const envApiUrl = process.env.NEXT_PUBLIC_API_URL;
  
  if (envApiUrl) {
    return envApiUrl;
  }
  
  // In production (when window is available), use the same origin as the frontend
  if (typeof window !== 'undefined') {
    return window.location.origin;
  }
  
  // Fallback for build time
  return 'http://localhost:8000';
};

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
    
    const response = await fetch(`${API_BASE_URL}/api/v1/products?${sp.toString()}`);
    if (!response.ok) throw new Error('Failed to fetch');
    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    return { products: [] };
  }
}

export default function HomePage() {
  const [searchItems, setSearchItems] = useState(['', '']);
  const [showThirdField, setShowThirdField] = useState(false);
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
    if (searchItems.length < 5) {
      setSearchItems([...searchItems, '']);
      if (searchItems.length === 2) {
        setShowThirdField(true);
      }
    }
  };

  const removeSearchField = (index: number) => {
    if (searchItems.length > 2) {
      const newItems = searchItems.filter((_, i) => i !== index);
      setSearchItems(newItems);
      if (newItems.length === 2) {
        setShowThirdField(false);
      }
    }
  };

  const updateSearchItem = (index: number, value: string) => {
    const newItems = [...searchItems];
    newItems[index] = value;
    setSearchItems(newItems);
  };

  const handleCompare = () => {
    const validItems = searchItems.filter(item => item.trim() !== '');
    if (validItems.length >= 2) {
      const queryString = validItems.join(',');
      window.location.href = `/compare?ids=${queryString}`;
    }
  };

  // Pre-created popular comparisons
  const popularComparisons = [
    { title: 'Fender Stratocaster vs Gibson Les Paul', ids: '1,2', image: '/images/comparison-1.jpg' },
    { title: 'Yamaha vs Roland Keyboards', ids: '3,4', image: '/images/comparison-2.jpg' },
    { title: 'Pearl vs Tama Drums', ids: '5,6', image: '/images/comparison-3.jpg' },
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-900 via-blue-800 to-purple-900 text-white">
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
              <p className="text-xl text-blue-100 mb-8">
                At MusicEurope you can compare prices on thousands of instruments from Europe's top music stores
              </p>
            </div>

            {/* Right side - Dynamic search interface */}
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
              <h3 className="text-2xl font-bold mb-6 text-center">Compare Instruments</h3>
              
              <div className="space-y-4">
                {searchItems.map((item, index) => (
                  <div key={index} className="relative">
                    <div className="flex items-center gap-3">
                      <input
                        type="text"
                        placeholder={`Search instrument ${index + 1}`}
                        value={item}
                        onChange={(e) => updateSearchItem(index, e.target.value)}
                        className="flex-1 px-4 py-3 rounded-lg border-0 bg-white/90 text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-400 focus:bg-white transition-all"
                      />
                      {searchItems.length > 2 && (
                        <button
                          onClick={() => removeSearchField(index)}
                          className="w-8 h-8 rounded-full bg-red-500 text-white flex items-center justify-center hover:bg-red-600 transition-colors"
                        >
                          ×
                        </button>
                      )}
                    </div>
                    {index < searchItems.length - 1 && (
                      <div className="text-center text-white/80 text-sm font-medium mt-2">vs</div>
                    )}
                  </div>
                ))}
                
                {searchItems.length < 5 && (
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
                className="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-6 rounded-lg transition-colors"
              >
                Compare {searchItems.filter(item => item.trim() !== '').length} Instruments
              </button>
            </div>
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
                href={`/compare?ids=${comparison.ids}`}
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

      {/* Category Icons */}
      <section className="py-12 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-6">
            {[
              { name: 'Electric Guitars', icon: '', href: '/products?category=electric' },
              { name: 'Acoustic Guitars', icon: '', href: '/products?category=acoustic' },
              { name: 'Bass Guitars', icon: '', href: '/products?category=bass' },
              { name: 'Drums', icon: '', href: '/products?category=drums' },
              { name: 'Keyboards', icon: '', href: '/products?category=keyboards' },
              { name: 'Amplifiers', icon: '', href: '/products?category=amplifiers' },
              { name: 'Accessories', icon: '', href: '/products?category=accessories' },
            ].map((category) => (
              <Link
                key={category.name}
                href={category.href}
                className="group text-center p-4 rounded-lg hover:bg-white hover:shadow-md transition-all"
              >
                <div className="text-3xl mb-2 group-hover:scale-110 transition-transform">
                  {category.icon}
                </div>
                <div className="text-sm font-medium text-gray-700 group-hover:text-gray-900">
                  {category.name}
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
                    <span className="text-lg font-bold text-green-600">
                      €{product.best_price?.price?.toFixed(2) || product.msrp_price?.toFixed(2) || '299'}
                    </span>
                  </div>
                  <div className="flex gap-2">
                    <Link 
                      href={`/products/${product.slug}-${product.id}`}
                      className="flex-1 text-center bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      View Details
                    </Link>
                    <Link 
                      href={`/compare?ids=${product.id}`}
                      className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      Compare
                    </Link>
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
                  <span className="text-lg font-bold text-green-600">
                    €{product.best_price?.price?.toFixed(2) || product.msrp_price?.toFixed(2) || '399'}
                  </span>
                  <span className="text-sm text-gray-500">({product.review_count || 150} reviews)</span>
                </div>
                <Link 
                  href={`/products/${product.slug}-${product.id}`}
                  className="block mt-4 text-center bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Read Reviews
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="py-16 bg-white">
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



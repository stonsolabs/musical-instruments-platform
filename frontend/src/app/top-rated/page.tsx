'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Product, SearchResponse } from '@/types';
import { CompactProductVoting } from '@/components/ProductVoting';
import { formatPrice } from '@/lib/utils';
import { apiClient } from '@/lib/api';

export default function TopRatedPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTopRatedProducts = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch most voted products
        const data = await apiClient.getMostVotedProducts(50, 'vote_score');
        
        setProducts(data.products);
      } catch (e) {
        console.error('Failed to load top rated products:', e);
        setError('Failed to load top rated products');
      } finally {
        setLoading(false);
      }
    };

    loadTopRatedProducts();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-primary-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-primary-600">Loading top rated instruments...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-primary-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center py-12">
            <div className="text-red-600 mb-4">⚠️ {error}</div>
            <button 
              onClick={() => window.location.reload()} 
              className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-primary-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">⭐ Top Rated Instruments</h1>
            <p className="text-lg text-primary-100">
              Discover the highest rated musical instruments as voted by our community
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {products.length > 0 ? (
          <>
            <div className="mb-6">
              <p className="text-gray-600">
                {products.length} top rated instruments found
              </p>
            </div>

            {/* Products Grid */}
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {products.map((product) => (
                <div key={product.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-all duration-200">
                  <div className="relative">
                    <Link href={`/products/${product.slug}-${product.id}`} className="block">
                      <div className="h-48 bg-white flex items-center justify-center overflow-hidden border border-gray-200">
                        {product.images && product.images.length > 0 ? (
                          <img 
                            src={product.images[0]} 
                            alt={product.name}
                            className="w-full h-full scale-105"
                            style={{ backgroundColor: 'white' }}
                          />
                        ) : (
                          <span className="text-gray-400 text-2xl">🎸</span>
                        )}
                      </div>
                    </Link>
                  </div>
                  
                  <div className="p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-gray-600">{product.brand?.name || 'Brand'}</span>
                    </div>
                    
                    {/* Voting Component */}
                    <div className="flex items-center justify-center mb-3">
                      <CompactProductVoting 
                        productId={product.id}
                        initialStats={product.vote_stats}
                        className=""
                      />
                    </div>

                    <Link href={`/products/${product.slug}-${product.id}`} className="block">
                      <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 hover:text-accent-600 transition-colors cursor-pointer">{product.name}</h3>
                    </Link>
                    
                    <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                      {product.description || "High-quality musical instrument with excellent craftsmanship and sound."}
                    </p>
                    
                    <div className="space-y-2">
                      {product.prices && product.prices.length > 0 ? (
                        <>
                          {product.prices
                            .slice(0, 3)
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
                        </>
                      ) : (
                        <>
                          <a
                            href={`https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(product.name)}&aff=123`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="fp-table__button fp-table__button--thomann"
                          >
                            <span>View Price at</span>
                            <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
                          </a>
                          <a
                            href={`https://gear4music.com/search?search=${encodeURIComponent(product.name)}&aff=123`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="fp-table__button fp-table__button--gear4music"
                          >
                            <span>View Price at</span>
                            <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
                          </a>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-500 mb-4">No top rated instruments found.</div>
            <Link 
              href="/products"
              className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors"
            >
              Browse All Products
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
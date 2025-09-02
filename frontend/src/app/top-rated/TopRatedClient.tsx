'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import { CompactProductVoting } from '@/components/ProductVoting';

interface VoteStats {
  thumbs_up_count: number;
  thumbs_down_count: number;
  total_votes: number;
  vote_score: number;
}

interface TopRatedProduct {
  id: number;
  name: string;
  slug: string;
  brand: {
    id: number;
    name: string;
    slug: string;
  };
  category: {
    id: number;
    name: string;
    slug: string;
  };
  vote_stats: VoteStats;
  images: any;
  msrp_price?: number;
}

interface TopRatedResponse {
  products: TopRatedProduct[];
  total: number;
  sort_by: string;
  limit: number;
}

export default function TopRatedClient() {
  const [products, setProducts] = useState<TopRatedProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<'vote_score' | 'total_votes' | 'thumbs_up_count'>('vote_score');

  useEffect(() => {
    loadTopRatedProducts();
  }, [sortBy]);

  const loadTopRatedProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      const response: TopRatedResponse = await apiClient.getMostVotedProducts(50, sortBy);
      setProducts(response.products);
    } catch (err) {
      console.error('Failed to load top rated products:', err);
      setError('Failed to load top rated products');
    } finally {
      setLoading(false);
    }
  };

  const getSortLabel = (sort: string) => {
    switch (sort) {
      case 'vote_score': return 'Highest Score';
      case 'total_votes': return 'Most Votes';
      case 'thumbs_up_count': return 'Most Liked';
      default: return 'Score';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading top rated products...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <div className="text-red-500 text-xl mb-4">⚠️ Error</div>
            <p className="text-gray-600">{error}</p>
            <button 
              onClick={loadTopRatedProducts}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Top Rated Instruments
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Discover the highest-rated musical instruments based on votes from our community of musicians. 
            These are the instruments that players love most.
          </p>
          <div className="mt-8 flex justify-center">
            <div className="bg-white bg-opacity-20 rounded-lg px-6 py-3">
              <span className="text-blue-100">🎵 Community Choice • Musician Approved • Top Quality</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Controls */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              {products.length} Top Rated Products
            </h2>
            <p className="text-gray-600 mt-1">
              Sorted by {getSortLabel(sortBy).toLowerCase()}
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            <label htmlFor="sort-select" className="text-sm font-medium text-gray-700">
              Sort by:
            </label>
            <select
              id="sort-select"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm bg-white"
            >
              <option value="vote_score">Highest Score</option>
              <option value="total_votes">Most Votes</option>
              <option value="thumbs_up_count">Most Liked</option>
            </select>
          </div>
        </div>

        {/* Products Grid */}
        {products.length > 0 ? (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map((product, index) => (
              <div key={product.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-all duration-200">
                {/* Rank Badge */}
                <div className="relative">
                  <div className="absolute top-3 left-3 z-10">
                    <div className={`rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold text-white ${
                      index === 0 ? 'bg-yellow-500' : 
                      index === 1 ? 'bg-gray-400' : 
                      index === 2 ? 'bg-yellow-600' : 
                      'bg-blue-500'
                    }`}>
                      {index + 1}
                    </div>
                  </div>

                  {/* Product Image */}
                  <div className="h-48 bg-gray-200 flex items-center justify-center">
                    {product.images && Object.values(product.images).length > 0 ? (
                      <img 
                        src={Object.values(product.images)[0] as string} 
                        alt={product.name}
                        className="w-full h-full object-contain"
                      />
                    ) : (
                      <span className="text-gray-400 text-2xl">🎸</span>
                    )}
                  </div>
                </div>
                
                <div className="p-4">
                  {/* Brand */}
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">{product.brand.name}</span>
                    <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                      {product.category.name}
                    </span>
                  </div>

                  {/* Product Name */}
                  <Link href={`/products/${product.slug}-${product.id}`} className="block">
                    <h3 className="font-semibold text-gray-900 mb-3 line-clamp-2 hover:text-blue-600 transition-colors cursor-pointer">
                      {product.name}
                    </h3>
                  </Link>

                  {/* Voting Stats */}
                  <div className="mb-4">
                    <CompactProductVoting 
                      productId={product.id}
                      initialStats={product.vote_stats}
                      className="justify-center"
                    />
                    <div className="text-center mt-2">
                      <div className="text-sm text-gray-600">
                        Score: <span className="font-semibold text-blue-600">{product.vote_stats.vote_score}</span>
                      </div>
                      <div className="text-xs text-gray-500">
                        {product.vote_stats.total_votes} votes
                      </div>
                    </div>
                  </div>

                  {/* Price */}
                  {product.msrp_price && (
                    <div className="text-center">
                      <span className="text-lg font-bold text-gray-900">
                        €{product.msrp_price.toFixed(0)}
                      </span>
                    </div>
                  )}

                  {/* View Product Button */}
                  <div className="mt-4">
                    <Link 
                      href={`/products/${product.slug}-${product.id}`}
                      className="block w-full bg-blue-600 text-white text-center py-2 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                    >
                      View Details
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">🎵</div>
            <h3 className="text-xl font-semibold text-gray-600 mb-2">No voted products yet</h3>
            <p className="text-gray-500 mb-6">
              Be the first to vote on your favorite instruments!
            </p>
            <Link 
              href="/products"
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Browse Products
            </Link>
          </div>
        )}

        {/* Voting Information */}
        <div className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">How does voting work?</h3>
          <div className="text-blue-800 space-y-2">
            <p>• <strong>Vote Score:</strong> Thumbs up count minus thumbs down count</p>
            <p>• <strong>Total Votes:</strong> All votes received (both up and down)</p>
            <p>• <strong>Most Liked:</strong> Products with the highest number of thumbs up</p>
          </div>
          <div className="mt-4 text-sm text-blue-700">
            Your vote helps other musicians discover great instruments! Vote on any product page to contribute to the rankings.
          </div>
        </div>
      </div>
    </div>
  );
}

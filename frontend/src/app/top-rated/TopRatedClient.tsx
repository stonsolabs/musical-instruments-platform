'use client';

import React from 'react';
import Link from 'next/link';
import { Product } from '@/types';
import { VotingProductCard } from '@/components/ProductCard';

interface TopRatedClientProps {
  initialProducts: Product[];
}

export default function TopRatedClient({ initialProducts }: TopRatedClientProps) {
  const products = initialProducts;

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

            {/* Products Grid - Using centralized ProductCard */}
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {products.map((product) => (
                <VotingProductCard key={product.id} product={product} />
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

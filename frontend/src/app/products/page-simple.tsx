'use client';

import React, { useState } from 'react';
import Link from 'next/link';

export default function ProductsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  
  // Sample products
  const products = [
    { id: 1, name: 'Fender Stratocaster', brand: 'Fender', price: 599, rating: 4.8, category: 'Electric Guitar' },
    { id: 2, name: 'Gibson Les Paul', brand: 'Gibson', price: 899, rating: 4.9, category: 'Electric Guitar' },
    { id: 3, name: 'Yamaha P-125', brand: 'Yamaha', price: 649, rating: 4.7, category: 'Keyboard' },
    { id: 4, name: 'Taylor 814ce', brand: 'Taylor', price: 2499, rating: 4.9, category: 'Acoustic Guitar' },
    { id: 5, name: 'Pearl Export', brand: 'Pearl', price: 799, rating: 4.6, category: 'Drums' },
    { id: 6, name: 'Roland TD-17KV', brand: 'Roland', price: 1299, rating: 4.8, category: 'Electronic Drums' },
  ];

  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    product.brand.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <nav className="mb-6">
            <ol className="flex items-center space-x-2 text-sm text-gray-600">
              <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
              <li>/</li>
              <li className="text-gray-900">Products</li>
            </ol>
          </nav>

          <h1 className="text-3xl font-bold text-gray-900 mb-4">Musical Instruments</h1>
          
          {/* Search */}
          <div className="max-w-md">
            <input
              type="text"
              placeholder="Search instruments..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Products Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProducts.map((product) => (
            <div key={product.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className="h-48 bg-gray-200 rounded-lg mb-4 flex items-center justify-center">
                <span className="text-gray-400 text-2xl">🎸</span>
              </div>
              
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-600">{product.brand}</p>
                  <h3 className="font-semibold text-gray-900">{product.name}</h3>
                  <p className="text-sm text-gray-500">{product.category}</p>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-yellow-500">★</span>
                    <span className="text-sm font-medium">{product.rating}</span>
                  </div>
                  <span className="text-lg font-bold text-green-600">€{product.price}</span>
                </div>

                <div className="flex gap-2">
                  <Link 
                    href={`/products/${product.id}`}
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
            </div>
          ))}
        </div>

        {filteredProducts.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-600">No products found matching your search.</p>
          </div>
        )}
      </div>
    </div>
  );
}

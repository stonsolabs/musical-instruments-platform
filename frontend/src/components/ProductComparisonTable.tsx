import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

interface Product {
  id: string;
  name: string;
  slug: string;
  brand: string;
  price: number;
  originalPrice?: number;
  image: string;
  rating: number;
  reviewCount: number;
  affiliateUrl: string;
  features: {
    [key: string]: string | boolean | number;
  };
  pros: string[];
  cons: string[];
  bestFor: string;
}

interface ProductComparisonTableProps {
  products: Product[];
  features: {
    key: string;
    label: string;
    type: 'text' | 'boolean' | 'number' | 'rating';
  }[];
  title?: string;
  description?: string;
}

export default function ProductComparisonTable({ 
  products, 
  features, 
  title = "Product Comparison", 
  description = "Compare the top products in this category" 
}: ProductComparisonTableProps) {
  return (
    <div className="my-12">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">{title}</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">{description}</p>
      </div>

      <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        {/* Table Header */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6 bg-gray-50 border-b border-gray-200">
          <div className="text-center">
            <h3 className="font-semibold text-gray-900">Features</h3>
          </div>
          {products.map((product) => (
            <div key={product.id} className="text-center">
              <div className="relative h-24 w-24 mx-auto mb-3 bg-white rounded-lg shadow-sm overflow-hidden">
                <Image
                  src={product.image}
                  alt={product.name}
                  fill
                  className="object-cover"
                />
              </div>
              <h3 className="font-semibold text-gray-900 text-sm mb-1">{product.name}</h3>
              <p className="text-xs text-gray-600 mb-2">{product.brand}</p>
              <div className="flex items-center justify-center gap-1 mb-2">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className={`text-xs ${i < Math.floor(product.rating) ? 'text-yellow-400' : 'text-gray-300'}`}>
                    ★
                  </span>
                ))}
                <span className="text-xs text-gray-600">({product.reviewCount})</span>
              </div>
              <div className="flex items-center justify-center gap-2">
                <span className="font-bold text-gray-900">€{product.price}</span>
                {product.originalPrice && (
                  <span className="text-xs text-gray-500 line-through">€{product.originalPrice}</span>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Features Comparison */}
        <div className="divide-y divide-gray-200">
          {features.map((feature) => (
            <div key={feature.key} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4 hover:bg-gray-50">
              <div className="flex items-center">
                <span className="font-medium text-gray-900">{feature.label}</span>
              </div>
              {products.map((product) => (
                <div key={product.id} className="flex items-center justify-center">
                  {feature.type === 'boolean' ? (
                    <span className={`text-lg ${product.features[feature.key] ? 'text-green-500' : 'text-red-500'}`}>
                      {product.features[feature.key] ? '✓' : '✗'}
                    </span>
                  ) : feature.type === 'rating' ? (
                    <div className="flex items-center gap-1">
                      {[...Array(5)].map((_, i) => (
                        <span key={i} className={`text-sm ${i < (product.features[feature.key] as number) ? 'text-yellow-400' : 'text-gray-300'}`}>
                          ★
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span className="text-sm text-gray-700">{product.features[feature.key]}</span>
                  )}
                </div>
              ))}
            </div>
          ))}
        </div>

        {/* Pros and Cons */}
        <div className="grid md:grid-cols-2 gap-6 p-6 bg-gray-50">
          {products.map((product) => (
            <div key={product.id} className="space-y-4">
              <h4 className="font-semibold text-gray-900">{product.name}</h4>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h5 className="font-medium text-green-700 mb-2">Pros</h5>
                  <ul className="space-y-1">
                    {product.pros.map((pro, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                        <span className="text-green-500 mt-0.5">✓</span>
                        {pro}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div>
                  <h5 className="font-medium text-red-700 mb-2">Cons</h5>
                  <ul className="space-y-1">
                    {product.cons.map((con, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                        <span className="text-red-500 mt-0.5">✗</span>
                        {con}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div>
                <h5 className="font-medium text-blue-700 mb-1">Best For</h5>
                <p className="text-sm text-gray-600">{product.bestFor}</p>
              </div>

              <Link
                href={product.affiliateUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="block w-full bg-blue-600 text-white text-center py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Check Price & Reviews
              </Link>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="p-4 bg-gray-100 border-t border-gray-200">
          <p className="text-xs text-gray-500 text-center">
            Affiliate links - We may earn a commission from qualifying purchases
          </p>
        </div>
      </div>
    </div>
  );
}

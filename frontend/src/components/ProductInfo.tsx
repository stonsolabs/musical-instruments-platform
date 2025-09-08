import React from 'react';
import { Product, AffiliateStoreWithUrl } from '../types';
import { formatPrice, getRatingStars } from '../lib/utils';
import { StarIcon } from '@heroicons/react/20/solid';
import { StarIcon as StarOutlineIcon } from '@heroicons/react/24/outline';
import { ProductDetailButtons } from './AffiliateButtons';
import ProductVoting from './ProductVoting';

interface ProductInfoProps {
  product: Product;
  preloadedStores?: AffiliateStoreWithUrl[];
}

export default function ProductInfo({ product, preloadedStores = [] }: ProductInfoProps) {
  const { full, half, empty } = getRatingStars(product.avg_rating || 0);

  return (
    <div className="space-y-6">
      {/* 1. OVERVIEW SECTION */}
      <div className="card p-6">
        <div className="flex items-center space-x-2 mb-3">
          <span className="text-sm font-medium text-brand-blue bg-blue-50 px-2 py-1 rounded-full">
            {product.category.name}
          </span>
          <span className="text-sm text-gray-500">by</span>
          <span className="text-sm font-medium text-gray-900">
            {product.brand.name}
          </span>
        </div>
        
        <h1 className="text-3xl font-bold text-gray-900 mb-3">
          {product.name}
        </h1>
        
        {product.description && (
          <p className="text-gray-600 leading-relaxed mb-4">
            {product.description}
          </p>
        )}

        {/* Highlights / Badges from content */}
        {(product.content?.quick_badges || (product.content as any)?.comparison_helpers) && (
          <div className="space-y-3">
            {product.content?.quick_badges && (
              <div>
                <h4 className="text-sm font-semibold text-gray-700 mb-2">Key Features</h4>
                <div className="flex flex-wrap gap-2">
                  {Object.entries(product.content.quick_badges).filter(([,v]) => !!v).map(([k]) => (
                    <span key={k} className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200 capitalize">
                      {k.replace(/_/g, ' ')}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {(product.content as any)?.comparison_helpers?.standout_strengths && (
              <div>
                <h4 className="text-sm font-semibold text-gray-700 mb-2">Standout Strengths</h4>
                <ul className="list-disc pl-5 text-sm text-gray-700">
                  {(product.content as any).comparison_helpers.standout_strengths.slice(0,4).map((s: string, i: number) => (
                    <li key={`hi-${i}`}>{s}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Performance Metrics & Purchase Section */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance & Reviews</h3>
        
        {/* Rating & Reviews */}
        <div className="flex items-center space-x-4 mb-6">
          <div className="flex items-center">
            {[...Array(full)].map((_, i) => (
              <StarIcon key={`full-${i}`} className="h-5 w-5 text-yellow-400" />
            ))}
            {[...Array(half)].map((_, i) => (
              <StarIcon key={`half-${i}`} className="h-5 w-5 text-yellow-400" />
            ))}
            {[...Array(empty)].map((_, i) => (
              <StarOutlineIcon key={`empty-${i}`} className="h-5 w-5 text-gray-300" />
            ))}
          </div>
          
          <div className="text-sm text-gray-600">
            <span className="font-medium">{product.avg_rating?.toFixed(1) || '0.0'}</span>
            <span className="mx-1">•</span>
            <span>{product.review_count} reviews</span>
          </div>
          
          {product.vote_stats && (
            <div className="flex items-center space-x-2 text-sm">
              <span className="font-medium text-green-600">🤘 {product.vote_stats.thumbs_up_count}</span>
              <span className="text-gray-400">👎 {product.vote_stats.thumbs_down_count}</span>
            </div>
          )}
        </div>

        {/* Quality Badges */}
        <div className="flex flex-wrap gap-2 mb-6">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200">
            🏆 Professional Grade
          </span>
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-200">
            ✓ Quality Tested
          </span>
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-50 text-purple-700 border border-purple-200">
            🚀 Popular Choice
          </span>
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-50 text-purple-700 border border-purple-200">
            Professional Rating: coming soon
          </span>
        </div>

        {/* Purchase Options */}
        <div>
          <h4 className="text-sm font-semibold text-gray-900 mb-3 uppercase tracking-wide">🛒 Available at</h4>
          <ProductDetailButtons product={product} preloadedStores={preloadedStores} />
        </div>
      </div>

      {/* 2. SPECIFICATIONS SECTION */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          📊 Key Specifications
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="flex justify-between py-2 border-b border-gray-200 last:border-0">
            <span className="text-gray-600 font-medium">Product ID:</span>
            <span className="text-gray-900 font-semibold">{product.sku}</span>
          </div>
          
          {product.content?.specifications && (
            <>
              {Object.entries(product.content.specifications).slice(0, 8).map(([key, value]) => (
                <div key={key} className="flex justify-between py-2 border-b border-gray-200 last:border-0">
                  <span className="text-gray-600 font-medium capitalize">
                    {key.replace(/_/g, ' ')}:
                  </span>
                  <span className="text-gray-900 font-semibold text-right">
                    {String(value)}
                  </span>
                </div>
              ))}
            </>
          )}
        </div>
      </div>

      {/* 3. ADDITIONAL INFORMATION SECTION */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Community Feedback</h3>
        <ProductVoting
          productId={product.id}
          initialUpvotes={product.vote_stats?.thumbs_up_count ?? 0}
          initialDownvotes={product.vote_stats?.thumbs_down_count ?? 0}
        />
      </div>

      {/* Additional Info removed per requirements */}
    </div>
  );
}

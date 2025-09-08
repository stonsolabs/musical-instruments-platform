import React from 'react';
import { ProductComparison } from '../types';
import { getProductImageUrl, formatPrice, getRatingStars } from '../lib/utils';
import { StarIcon } from '@heroicons/react/20/solid';
import { StarIcon as StarOutlineIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';

interface ComparisonGridProps {
  comparison: ProductComparison;
}

export default function ComparisonGrid({ comparison }: ComparisonGridProps) {
  const { products, common_specs, comparison_matrix } = comparison;

  if (products.length === 0) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {products.map((product) => {
        const { full, half, empty } = getRatingStars(product.avg_rating || 0);
        
        const badges = (product as any).content?.quick_badges as undefined | Record<string, boolean>;
        return (
          <div key={product.id} className="card hover:shadow-lg transition-shadow">
            {/* Product Header */}
            <div className="p-4 border-b border-gray-200">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-16 h-16 bg-gray-100 rounded-lg overflow-hidden">
                  <img
                    src={getProductImageUrl(product)}
                    alt={product.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.display = 'none';
                    }}
                  />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 text-sm leading-tight">
                    {product.name}
                  </h3>
                  <p className="text-xs text-gray-500">{product.brand.name}</p>
                  <p className="text-xs text-gray-400">{product.category.name}</p>
                </div>
              </div>
              
              {/* Rating */}
              <div className="flex items-center space-x-1 mb-2">
                {[...Array(full)].map((_, i) => (
                  <StarIcon key={`full-${i}`} className="w-4 h-4 text-yellow-400" />
                ))}
                {[...Array(half)].map((_, i) => (
                  <StarIcon key={`half-${i}`} className="w-4 h-4 text-yellow-400" />
                ))}
                {[...Array(empty)].map((_, i) => (
                  <StarOutlineIcon key={`empty-${i}`} className="w-4 h-4 text-gray-300" />
                ))}
                <span className="ml-2 text-xs text-gray-600">
                  {product.avg_rating?.toFixed(1) || '0.0'} ({product.review_count})
                </span>
              </div>
              
              {/* Price hidden (not focusing on prices now) */}
            </div>

            {/* Specifications */}
            <div className="p-4">
              <h4 className="font-medium text-gray-900 mb-3">Key Specifications</h4>
              <div className="space-y-2">
                {common_specs.slice(0, 4).map((spec) => (
                  <div key={spec} className="flex justify-between text-sm">
                    <span className="text-gray-600 capitalize">
                      {spec.replace(/_/g, ' ')}:
                    </span>
                    <span className="font-medium text-gray-900">
                      {product.content?.specifications?.[spec] || 'N/A'}
                    </span>
                  </div>
                ))}
              </div>
              {badges && Object.values(badges).some(Boolean) && (
                <div className="flex flex-wrap gap-2 mt-3">
                  {Object.entries(badges).filter(([,v]) => !!v).map(([k]) => (
                    <span key={k} className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200 capitalize">
                      {k.replace(/_/g,' ')}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Actions */}
            <div className="p-4 border-t border-gray-200 space-y-2">
              <Link
                href={`/products/${product.slug}`}
                className="btn-primary w-full text-center text-sm"
              >
                View Details
              </Link>
              <button className="btn-secondary w-full text-sm">
                Remove from Compare
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}

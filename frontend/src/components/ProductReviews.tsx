import React from 'react';
import { Product } from '../types';
import { StarIcon } from '@heroicons/react/20/solid';

interface ProductReviewsProps {
  product: Product;
}

export default function ProductReviews({ product }: ProductReviewsProps) {
  // Reviews functionality coming soon - for now show rating summary only

  const averageRating = product.avg_rating || 0;
  const reviewCount = product.review_count || 0;

  if (reviewCount === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No reviews yet for this product.</p>
        <p className="text-sm text-gray-400 mt-2">Be the first to share your experience!</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="font-display text-2xl font-bold text-gray-900 uppercase tracking-wide">Customer Reviews</h2>
      
      {/* Review Summary */}
      <div className="card p-6">
        <div className="flex items-center space-x-6">
          <div className="text-center">
            <div className="text-4xl font-bold text-gray-900">{averageRating.toFixed(1)}</div>
            <div className="flex items-center justify-center mt-1">
              {[...Array(5)].map((_, i) => (
                <StarIcon
                  key={i}
                  className={`w-5 h-5 ${
                    i < Math.floor(averageRating)
                      ? 'text-yellow-400'
                      : 'text-gray-300'
                  }`}
                />
              ))}
            </div>
            <div className="text-sm text-gray-600 mt-1">{reviewCount} reviews</div>
          </div>
          
          <div className="flex-1">
            <div className="mt-6 pt-6 border-t border-gray-200 text-center">
              <p className="text-gray-500 mb-2">Detailed reviews coming soon!</p>
              <p className="text-sm text-gray-400">We're working on implementing a full review system.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

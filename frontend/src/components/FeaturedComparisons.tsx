import React from 'react';
import Link from 'next/link';
import { Product } from '../types';
import { getProductImageUrl } from '../lib/utils';

interface FeaturedComparisonsProps {
  comparisons: Array<{
    id: string;
    title: string;
    description: string;
    category: string;
    product1: Product;
    product2: Product;
  }>;
}

export default function FeaturedComparisons({ comparisons }: FeaturedComparisonsProps) {
  if (!comparisons || comparisons.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No featured comparisons available at the moment.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {comparisons.map((comparison) => (
        <div key={comparison.id} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xs font-medium text-blue-700 bg-blue-50 px-2 py-1 rounded-full uppercase tracking-wide">
              {comparison.category}
            </span>
          </div>
          <Link href={`/compare?products=${comparison.product1.slug},${comparison.product2.slug}`} className="block">
            <h3 className="font-display text-lg font-bold text-gray-900 mb-2 leading-snug hover:text-blue-600">
              {comparison.title}
            </h3>
            <p className="text-gray-600 text-sm mb-1 hover:text-gray-800">
              {comparison.description}
            </p>
          </Link>
        </div>
      ))}
    </div>
  );
}

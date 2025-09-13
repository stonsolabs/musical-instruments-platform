import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { TrendingProduct } from '../types';
import { getProductImageUrl, formatPrice, getCategoryIcon } from '../lib/utils';
import { HandThumbDownIcon } from '@heroicons/react/24/outline';
import { ProductCardButtons } from './AffiliateButtons';
import { openTopAffiliate } from '../lib/affiliate';

interface TrendingProductsProps {
  products: TrendingProduct[];
}

export default function TrendingProducts({ products }: TrendingProductsProps) {
  if (!products || products.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No trending products available at the moment.</p>
      </div>
    );
  }

  const openPriorityStore = (product: any, e: React.MouseEvent) => {
    openTopAffiliate(product, e);
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {products.map((trendingProduct) => {
        const product = trendingProduct.product;
        const imageUrl = getProductImageUrl(product);
        
        return (
          <Link
            key={product.id}
            href={`/products/${product.slug}`}
            className="group bg-white border border-gray-200 rounded-lg hover:shadow-xl hover:border-gray-300 transition-all duration-300 transform hover:-translate-y-1 overflow-hidden"
          >
            {/* Product Image */}
            <div className="aspect-square bg-gray-50 overflow-hidden relative cursor-pointer" onClick={(e)=>openPriorityStore(product, e)} title="View at top store">
              <Image
                src={imageUrl}
                alt={product.name}
                width={300}
                height={300}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                sizes="(max-width: 640px) 50vw, (max-width: 1024px) 25vw, 20vw"
                loading="lazy"
              />
              {/* Trending Badge - cooler style */}
              <div className="absolute top-3 right-3 px-2 py-1 rounded-full text-xs font-medium uppercase tracking-wide bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-glow">
                Trending
              </div>
            </div>

            {/* Product Info */}
            <div className="p-4">
              {/* Product Name - Make it more prominent */}
              <h3 className="font-display font-bold text-lg text-gray-900 mb-2 line-clamp-2 group-hover:text-brand-primary transition-colors uppercase tracking-wide">
                {product.name}
              </h3>

              {/* Category and Brand */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-1 text-sm text-gray-500 uppercase tracking-wide">
                  <span>{getCategoryIcon(product.category.name)}</span>
                  <span>{product.category.name}</span>
                </div>
                <span className="text-sm font-medium text-brand-primary uppercase tracking-wide">
                  {product.brand.name}
                </span>
              </div>

              {/* Rating */}
              {/* <div className="flex items-center mb-3">
                <div className="flex items-center">
                  {[...Array(full)].map((_, i) => (
                    <StarIcon key={`full-${i}`} className="h-4 w-4 text-yellow-400" />
                  ))}
                  {[...Array(half)].map((_, i) => (
                    <StarIcon key={`half-${i}`} className="h-4 w-4 text-yellow-400" />
                  ))}
                  {[...Array(empty)].map((_, i) => (
                    <StarOutlineIcon key={`empty-${i}`} className="h-4 w-4 text-gray-300" />
                  ))}
                </div>
                <span className="ml-2 text-sm text-gray-500">
                  ({product.review_count})
                </span>
              </div> */}

              {/* Voting System */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <button className="flex items-center space-x-1 text-gray-600 hover:text-brand-primary transition-colors">
                    <span className="text-lg">🤘</span>
                    <span className="text-sm font-medium">{product.vote_stats?.thumbs_up_count || 0}</span>
                  </button>
                  <button className="flex items-center space-x-1 text-gray-400 hover:text-brand-red transition-colors">
                    <HandThumbDownIcon className="w-4 h-4" />
                    <span className="text-sm font-medium">{product.vote_stats?.thumbs_down_count || 0}</span>
                  </button>
                </div>
              </div>

              {/* Affiliate Buttons */}
              <div className="mb-3">
                <ProductCardButtons product={product} />
              </div>

              {/* Trending Score */}
              {/* {trendingProduct.trending_score && (
                <div className="mt-2 text-xs text-gray-500">
                  Trending score: {trendingProduct.trending_score.toFixed(1)}
                </div>
              )} */}
            </div>
          </Link>
        );
      })}
    </div>
  );
}

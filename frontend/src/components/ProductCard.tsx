import React from 'react';
import Link from 'next/link';
import { Product } from '../types';
import { getProductImageUrl, formatPrice, getCategoryIcon } from '../lib/utils';
import { openTopAffiliate } from '../lib/affiliate';
import { HandThumbDownIcon } from '@heroicons/react/24/outline';
import { ProductCompareCheckbox } from './FloatingCompareButton';

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  const imageUrl = getProductImageUrl(product);

  const onImageClick = () => openTopAffiliate(product as any);

  return (
    <div className="group relative">
      <div className="card hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
        {/* Product Image */}
        <div className="aspect-square bg-gray-100 overflow-hidden relative cursor-pointer" onClick={onImageClick} title="View at top store">
          <img
            src={imageUrl}
            alt={product.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.style.display = 'none';
            }}
          />
          
          {/* Overlay with quick action */}
          <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
            <Link
              href={`/products/${product?.slug}`}
              className="bg-white bg-opacity-90 hover:bg-opacity-100 text-gray-800 px-4 py-2 rounded-lg transition-all duration-200 hover:scale-110 font-medium"
              title="View Details"
            >
              View Details
            </Link>
          </div>
          
          {/* Compare Button - Top Right */}
          <div className="absolute top-2 right-2">
            <ProductCompareCheckbox product={product} />
          </div>
          
          {/* Product badges */}
          <div className="absolute top-2 left-2 flex flex-col space-y-1">
            {(product?.vote_stats?.thumbs_up_count || 0) > 10 && (
              <span className="bg-blue-500 text-white px-2 py-1 text-xs rounded-full font-medium">
                Popular
              </span>
            )}
          </div>
        </div>

        {/* Product Info */}
        <div className="p-4">
          {/* Category and Brand */}
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-1 text-sm text-gray-500">
              <span>{getCategoryIcon(product?.category?.name || '')}</span>
              <span className="truncate">{product?.category?.name || 'Unknown Category'}</span>
            </div>
            <span className="text-sm font-medium text-brand-primary truncate ml-2">
              {product?.brand?.name || 'Unknown Brand'}
            </span>
          </div>

          {/* Product Name */}
          <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 min-h-[2.5rem]">
            <Link href={`/products/${product?.slug}`} className="hover:text-brand-primary transition-colors">
              {product?.name || 'Unknown Product'}
            </Link>
          </h3>

          {/* Product Overview */}
          {product?.description && (
            <p className="text-xs text-gray-600 line-clamp-2 mb-3">
              {product.description}
            </p>
          )}

          {/* Key Specifications (most important first) */}
          {product?.content?.specifications && (
            <div className="mb-3">
              <div className="text-xs text-gray-500 font-medium mb-1">Key Specs:</div>
              <ul className="text-xs text-gray-600 space-y-1">
                {Object.entries(product.content.specifications).slice(0,3).map(([key, value]) => (
                  <li key={String(key)} className="flex justify-between">
                    <span className="capitalize font-medium">{String(key).replace(/_/g,' ')}:</span> 
                    <span className="text-gray-900">{String(value)}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Community Voting Section */}
          <div className="bg-gray-50 rounded-lg p-3 mb-4">
            <div className="flex items-center justify-between text-xs">
              <span className="text-gray-500">Community:</span>
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-1 text-gray-600">
                  <span className="text-sm">🤘</span>
                  <span className="font-medium">{product.vote_stats?.thumbs_up_count || 0}</span>
                </div>
                <div className="flex items-center space-x-1 text-gray-400">
                  <HandThumbDownIcon className="w-3 h-3" />
                  <span className="font-medium">{product.vote_stats?.thumbs_down_count || 0}</span>
                </div>
              </div>
            </div>
          </div>

          {/* View Details Link */}
          <div className="text-center">
              <Link
              href={`/products/${product?.slug}`}
              className="inline-flex items-center text-brand-primary hover:text-brand-orange font-medium transition-colors"
            >
              View Details
              <svg className="ml-2 w-4 h-4 transform hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

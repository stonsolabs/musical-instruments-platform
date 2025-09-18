import React, { useState, useEffect } from 'react';
import { Product } from '../types';
import { fetchProduct } from '../lib/api';
import { openTopAffiliate } from '../lib/affiliate';
import { ProductCardButtons } from './AffiliateButtons';
import { StarIcon } from '@heroicons/react/20/solid';
import { StarIcon as StarOutlineIcon } from '@heroicons/react/24/outline';
import { getRatingStars, getProductImageUrl } from '../lib/utils';
import { ShoppingCartIcon, ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline';

interface InlineProductShowcaseProps {
  productId: number;
  context: string;
  position: number;
  ctaText?: string;
  layout?: 'horizontal' | 'vertical' | 'compact';
  showFullDetails?: boolean;
}

export default function InlineProductShowcase({ 
  productId, 
  context, 
  position, 
  ctaText = "Check Latest Price",
  layout = 'horizontal',
  showFullDetails = true
}: InlineProductShowcaseProps) {
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProductDetails = async () => {
      try {
        setLoading(true);
        const productData = await fetchProduct(productId.toString());
        setProduct(productData);
      } catch (err) {
        console.error(`Failed to fetch product ${productId}:`, err);
        setError('Product not found');
      } finally {
        setLoading(false);
      }
    };

    fetchProductDetails();
  }, [productId]);

  if (loading) {
    return (
      <div className={`my-8 p-6 bg-gray-50 rounded-lg border border-gray-200 ${layout === 'horizontal' ? 'flex items-center space-x-6' : 'space-y-4'}`}>
        <div className="animate-pulse">
          <div className="bg-gray-200 h-32 w-32 rounded-lg"></div>
        </div>
        <div className="flex-1 space-y-3">
          <div className="bg-gray-200 h-4 rounded w-3/4"></div>
          <div className="bg-gray-200 h-6 rounded w-1/2"></div>
          <div className="bg-gray-200 h-10 rounded w-1/3"></div>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="my-8 p-6 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-red-600">Product not available</p>
      </div>
    );
  }

  const { full, half, empty } = getRatingStars(product.avg_rating || 0);
  const imageUrl = getProductImageUrl(product);
  
  const openPriorityStore = (e: React.MouseEvent) => openTopAffiliate(product as any, e);

  const layoutClasses = {
    horizontal: 'flex flex-col md:flex-row items-start md:items-center space-y-4 md:space-y-0 md:space-x-6',
    vertical: 'flex flex-col space-y-4',
    compact: 'flex items-center space-x-4'
  };

  const imageClasses = {
    horizontal: 'w-full md:w-48 h-48 md:h-32 flex-shrink-0',
    vertical: 'w-full h-48',
    compact: 'w-20 h-20 flex-shrink-0'
  };

  return (
    <div className={`my-8 p-6 bg-gradient-to-br from-white to-gray-50 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-300 ${layoutClasses[layout]}`}>
      {/* Product Image */}
      <div className={`${imageClasses[layout]} bg-gray-100 rounded-lg overflow-hidden cursor-pointer relative group`} onClick={openPriorityStore}>
        <img
          src={imageUrl}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.style.display = 'none';
          }}
        />
        
        {/* Quick Action Overlay */}
        <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
          <div className="bg-white/90 backdrop-blur-sm rounded-lg px-3 py-2 text-sm font-medium text-gray-900">
            Quick View
          </div>
        </div>
      </div>

      {/* Product Details */}
      <div className="flex-1 space-y-3">
        {/* Brand and Category */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">{product.category.name}</span>
          <span className="text-sm font-medium text-brand-primary">
            {product.brand.name}
          </span>
        </div>

        {/* Product Name */}
        <h3 className="text-xl font-bold text-gray-900 leading-tight">
          {product.name}
        </h3>

        {/* Context */}
        <p className="text-gray-700 leading-relaxed">
          {context}
        </p>

        {/* Rating */}
        <div className="flex items-center space-x-2">
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
          <span className="text-sm text-gray-500">
            {product.avg_rating?.toFixed(1)} ({product.review_count || 0} reviews)
          </span>
        </div>

        {/* Key Features (if showFullDetails) */}
        {showFullDetails && product.content?.comparison_helpers?.standout_strengths && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-gray-900">Key Features:</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              {product.content.comparison_helpers.standout_strengths.slice(0, 3).map((feature: string, index: number) => (
                <li key={index} className="flex items-center">
                  <span className="w-1.5 h-1.5 bg-brand-primary rounded-full mr-2"></span>
                  {feature}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-3 pt-2">
          <button
            onClick={openPriorityStore}
            className="flex-1 flex items-center justify-center space-x-2 py-3 px-6 bg-gradient-to-r from-green-500 to-green-600 text-white font-bold rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
          >
            <ShoppingCartIcon className="w-5 h-5" />
            <span>{ctaText}</span>
          </button>
          
          <a
            href={`/products/${product.slug}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center space-x-2 py-3 px-6 bg-white border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
          >
            <ArrowTopRightOnSquareIcon className="w-4 h-4" />
            <span>Full Review</span>
          </a>
        </div>

        {/* Affiliate Buttons (if showFullDetails) */}
        {showFullDetails && (
          <div className="pt-2">
            <ProductCardButtons product={product} />
          </div>
        )}
      </div>
    </div>
  );
}

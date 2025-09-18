import React, { useState, useEffect } from 'react';
import { Product } from '../types';
import { fetchProduct } from '../lib/api';
import AffiliateButtons from './AffiliateButtons';
import { StarIcon } from '@heroicons/react/20/solid';
import { StarIcon as StarOutlineIcon } from '@heroicons/react/24/outline';
import { getRatingStars, getProductImageUrl } from '../lib/utils';
import { ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline';

interface InlineProductShowcaseProps {
  productId: number;
  context: string;
  position: number;
  ctaText?: string;
  layout?: 'horizontal' | 'vertical' | 'compact';
  showFullDetails?: boolean;
  minimal?: boolean;
}

export default function InlineProductShowcase({ 
  productId, 
  context, 
  position, 
  ctaText = "View Product",
  layout = 'horizontal',
  showFullDetails = true,
  minimal = false
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
  
  // Store opening handled via AffiliateButtons

  const layoutClasses = {
    horizontal: 'flex flex-col lg:flex-row items-start lg:items-center gap-4 lg:gap-6',
    vertical: 'flex flex-col gap-4',
    compact: 'flex items-center gap-4'
  };

  const imageClasses = {
    horizontal: 'w-full lg:w-48 h-48 lg:h-32 flex-shrink-0',
    vertical: 'w-full h-48',
    compact: 'w-20 h-20 flex-shrink-0'
  };

  // Minimal presentation: name + single store button + optional full review link
  if (minimal) {
    return (
      <div className="my-4 p-4 bg-white rounded-lg border border-gray-200">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div className="min-w-0">
            <h4 className="text-base sm:text-lg font-semibold text-gray-900 truncate">{product.name}</h4>
            {context && (
              <p className="text-sm text-gray-600 mt-1 line-clamp-2">{context}</p>
            )}
          </div>
          <div className="flex items-center gap-2 sm:min-w-[180px]">
            <AffiliateButtons product={product} variant="compact" maxButtons={1} />
            <a
              href={`/products/${product.slug}`}
              className="hidden sm:inline-flex items-center justify-center px-3 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 text-sm"
              title="Full Review"
            >
              <ArrowTopRightOnSquareIcon className="w-4 h-4 mr-1" />
              Full Review
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
      <div className={`my-6 p-4 sm:p-6 bg-white rounded-xl border border-gray-200 ${layoutClasses[layout]}`}>
      {/* Product Image */}
      <div className={`${imageClasses[layout]} bg-gray-100 rounded-lg overflow-hidden`}>
        <img
          src={imageUrl}
          alt={product.name}
          className="w-full h-full object-cover"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.style.display = 'none';
          }}
        />
      </div>

      {/* Product Details */}
      <div className="flex-1 min-w-0 space-y-3">
        {/* Brand and Category */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">{product.category.name}</span>
          <span className="text-sm font-medium text-brand-primary">
            {product.brand.name}
          </span>
        </div>

        {/* Product Name */}
        <h3 className="text-lg sm:text-xl font-bold text-gray-900 leading-tight break-words">
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

        {/* CTA Buttons (streamlined) */}
        <div className="flex flex-col sm:flex-row gap-3 pt-2 w-full">
          {/* Primary: top affiliate/store button (compact) */}
          <div className="flex-1">
            <AffiliateButtons product={product} variant="compact" maxButtons={1} />
          </div>
          {/* Secondary: full review link */}
          <a
            href={`/products/${product.slug}`}
            className="inline-flex items-center justify-center px-4 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
          >
            <ArrowTopRightOnSquareIcon className="w-4 h-4 mr-2" />
            Full Review
          </a>
        </div>
      </div>
    </div>
  );
}

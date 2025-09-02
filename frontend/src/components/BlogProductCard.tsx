import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

interface BlogProductCardProps {
  product: {
    id: string;
    name: string;
    slug: string;
    brand: string;
    category: string;
    price: number;
    originalPrice?: number;
    image: string;
    rating: number;
    reviewCount: number;
    affiliateUrl: string;
    features: string[];
    description: string;
    storeLinks?: {
      amazon?: string;
      thomann?: string;
      sweetwater?: string;
      guitarCenter?: string;
      musiciansFriend?: string;
    };
  };
  position?: 'left' | 'right' | 'center';
  variant?: 'compact' | 'detailed';
}

export default function BlogProductCard({ 
  product, 
  position = 'center', 
  variant = 'detailed' 
}: BlogProductCardProps) {
  const discount = product.originalPrice ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100) : 0;

  if (variant === 'compact') {
    return (
      <div className={`my-8 ${position === 'left' ? 'float-left mr-6' : position === 'right' ? 'float-right ml-6' : ''} w-80`}>
        <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
          {/* Product Image */}
          <div className="relative h-48 bg-gray-100">
            <Image
              src={product.image}
              alt={product.name}
              fill
              className=""
              style={{ backgroundColor: 'white' }}
            />
            {discount > 0 && (
              <div className="absolute top-2 left-2 bg-red-600 text-white px-2 py-1 rounded text-xs font-bold">
                -{discount}%
              </div>
            )}
          </div>

          {/* Product Info */}
          <div className="p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">{product.brand}</span>
              <span className="text-xs text-gray-500">•</span>
              <span className="text-xs text-gray-500">{product.category}</span>
            </div>
            
            <h3 className="font-bold text-gray-900 mb-2 line-clamp-2">{product.name}</h3>
            
            {/* Rating */}
            <div className="flex items-center gap-2 mb-3">
              <div className="flex items-center gap-1">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className={`text-sm ${i < Math.floor(product.rating) ? 'text-yellow-400' : 'text-gray-300'}`}>
                    ★
                  </span>
                ))}
              </div>
              <span className="text-sm text-gray-600">({product.reviewCount})</span>
            </div>

            {/* Price */}
            <div className="flex items-center gap-2 mb-4">
              <span className="text-xl font-bold text-gray-900">€{product.price}</span>
              {product.originalPrice && (
                <span className="text-sm text-gray-500 line-through">€{product.originalPrice}</span>
              )}
            </div>

            {/* Key Features */}
            <div className="mb-4">
              <ul className="text-sm text-gray-600 space-y-1">
                {product.features.slice(0, 3).map((feature, index) => (
                  <li key={index} className="flex items-center gap-2">
                    <span className="text-green-500">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>

            {/* CTA Button */}
            <div className="grid grid-cols-2 gap-2">
              {product.storeLinks?.amazon && (
                <Link
                  href={product.storeLinks.amazon}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-gradient-to-r from-orange-500 to-yellow-500 text-white text-center py-2 px-3 rounded-lg font-semibold hover:from-orange-600 hover:to-yellow-600 transition-all shadow-lg text-xs"
                >
                  🛒 Amazon
                </Link>
              )}
              {product.storeLinks?.thomann && (
                <Link
                  href={product.storeLinks.thomann}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-gradient-to-r from-blue-600 to-blue-700 text-white text-center py-2 px-3 rounded-lg font-semibold hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg text-xs"
                >
                  🎵 Thomann
                </Link>
              )}
              {product.storeLinks?.sweetwater && (
                <Link
                  href={product.storeLinks.sweetwater}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-gradient-to-r from-green-600 to-green-700 text-white text-center py-2 px-3 rounded-lg font-semibold hover:from-green-700 hover:to-green-800 transition-all shadow-lg text-xs"
                >
                  🎸 Sweetwater
                </Link>
              )}
              {!product.storeLinks && (
                <Link
                  href={product.affiliateUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-center py-2 px-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg text-xs"
                >
                  Check Price
                </Link>
              )}
            </div>
            
            <p className="text-xs text-gray-500 text-center mt-2">
              Affiliate link - We may earn a commission
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="my-12 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-8 border border-blue-200">
      <div className="text-center mb-6">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">Recommended Product</h3>
        <p className="text-gray-600">Our top pick for this category</p>
      </div>

      <div className="grid md:grid-cols-2 gap-8 items-center">
        {/* Product Image */}
        <div className="relative">
          <div className="relative h-80 bg-white rounded-lg shadow-lg overflow-hidden">
            <Image
              src={product.image}
              alt={product.name}
              fill
              className=""
              style={{ backgroundColor: 'white' }}
            />
            {discount > 0 && (
              <div className="absolute top-4 left-4 bg-red-600 text-white px-3 py-2 rounded-lg text-sm font-bold">
                Save {discount}%
              </div>
            )}
          </div>
        </div>

        {/* Product Details */}
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <span className="text-sm font-semibold text-blue-600 uppercase tracking-wide">{product.brand}</span>
            <span className="text-gray-400">•</span>
            <span className="text-sm text-gray-600">{product.category}</span>
          </div>

          <h2 className="text-2xl font-bold text-gray-900">{product.name}</h2>

          {/* Rating */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1">
              {[...Array(5)].map((_, i) => (
                <span key={i} className={`text-lg ${i < Math.floor(product.rating) ? 'text-yellow-400' : 'text-gray-300'}`}>
                  ★
                </span>
              ))}
            </div>
            <span className="text-gray-600">({product.reviewCount} reviews)</span>
          </div>

          {/* Price */}
          <div className="flex items-center gap-3">
            <span className="text-3xl font-bold text-gray-900">€{product.price}</span>
            {product.originalPrice && (
              <span className="text-lg text-gray-500 line-through">€{product.originalPrice}</span>
            )}
          </div>

          {/* Description */}
          <p className="text-gray-600 leading-relaxed">{product.description}</p>

          {/* Key Features */}
          <div>
            <h4 className="font-semibold text-gray-900 mb-2">Key Features:</h4>
            <ul className="space-y-2">
              {product.features.map((feature, index) => (
                <li key={index} className="flex items-center gap-3 text-gray-600">
                  <span className="text-green-500 text-lg">✓</span>
                  {feature}
                </li>
              ))}
            </ul>
          </div>

          {/* CTA Buttons */}
          <div className="space-y-3 pt-4">
            {/* Store Buttons */}
            <div className="grid grid-cols-2 gap-2">
              {product.storeLinks?.amazon && (
                <Link
                  href={product.storeLinks.amazon}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-gradient-to-r from-orange-500 to-yellow-500 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-orange-600 hover:to-yellow-600 transition-all shadow-lg text-sm"
                >
                  🛒 Amazon
                </Link>
              )}
              {product.storeLinks?.thomann && (
                <Link
                  href={product.storeLinks.thomann}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-gradient-to-r from-blue-600 to-blue-700 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg text-sm"
                >
                  🎵 Thomann
                </Link>
              )}
              {product.storeLinks?.sweetwater && (
                <Link
                  href={product.storeLinks.sweetwater}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-gradient-to-r from-green-600 to-green-700 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-green-700 hover:to-green-800 transition-all shadow-lg text-sm"
                >
                  🎸 Sweetwater
                </Link>
              )}
              {!product.storeLinks && (
                <Link
                  href={product.affiliateUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg text-sm"
                >
                  Check Latest Price
                </Link>
              )}
            </div>
            
            {/* Review Link */}
            <Link
              href={`/products/${product.slug}`}
              className="block w-full bg-gray-100 text-gray-900 text-center py-3 px-6 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
            >
              Read Full Review
            </Link>
          </div>

          <p className="text-xs text-gray-500 text-center">
            Affiliate link - We may earn a commission from qualifying purchases
          </p>
        </div>
      </div>
    </div>
  );
}

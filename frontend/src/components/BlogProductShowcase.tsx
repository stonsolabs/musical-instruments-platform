import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

interface Product {
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
  pros?: string[];
  cons?: string[];
  bestFor?: string;
  isRecommended?: boolean;
  badge?: string;
  storeLinks?: {
    amazon?: string;
    thomann?: string;
    sweetwater?: string;
    guitarCenter?: string;
    musiciansFriend?: string;
  };
}

interface BlogProductShowcaseProps {
  products: Product[];
  style?: 'featured' | 'grid' | 'carousel' | 'comparison' | 'recommended';
  title?: string;
  subtitle?: string;
  showComparison?: boolean;
  maxProducts?: number;
}

export default function BlogProductShowcase({ 
  products, 
  style = 'featured',
  title,
  subtitle,
  showComparison = false,
  maxProducts = 3
}: BlogProductShowcaseProps) {
  const displayProducts = products.slice(0, maxProducts);
  const discount = (product: Product) => 
    product.originalPrice ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100) : 0;

  // Featured Style - Large showcase with recommended product
  if (style === 'featured') {
    const recommended = displayProducts.find(p => p.isRecommended) || displayProducts[0];
    const others = displayProducts.filter(p => p.id !== recommended.id);

    return (
      <div className="my-12 bg-gradient-to-br from-blue-50 via-white to-purple-50 rounded-2xl p-8 border border-blue-100 shadow-lg">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-3">{title || 'Featured Products'}</h2>
          {subtitle && <p className="text-lg text-gray-600">{subtitle}</p>}
        </div>

        {/* Recommended Product */}
        <div className="bg-white rounded-xl p-6 shadow-md border border-gray-100 mb-8">
          <div className="flex items-center gap-3 mb-4">
            <span className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-3 py-1 rounded-full text-sm font-bold">
              ⭐ Recommended
            </span>
            {recommended.badge && (
              <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-bold">
                {recommended.badge}
              </span>
            )}
          </div>

          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div className="relative">
              <div className="relative h-80 bg-gray-100 rounded-lg overflow-hidden shadow-lg">
                <Image
                  src={recommended.image}
                  alt={recommended.name}
                  fill
                  className=""
                  style={{ backgroundColor: 'white' }}
                />
                {discount(recommended) > 0 && (
                  <div className="absolute top-4 left-4 bg-red-600 text-white px-3 py-2 rounded-lg text-sm font-bold">
                    Save {discount(recommended)}%
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <span className="text-sm font-semibold text-blue-600 uppercase tracking-wide">{recommended.brand}</span>
                <span className="text-gray-400">•</span>
                <span className="text-sm text-gray-600">{recommended.category}</span>
              </div>

              <h3 className="text-2xl font-bold text-gray-900">{recommended.name}</h3>

              <div className="flex items-center gap-3">
                <div className="flex items-center gap-1">
                  {[...Array(5)].map((_, i) => (
                    <span key={i} className={`text-lg ${i < Math.floor(recommended.rating) ? 'text-yellow-400' : 'text-gray-300'}`}>
                      ★
                    </span>
                  ))}
                </div>
                <span className="text-gray-600">({recommended.reviewCount} reviews)</span>
              </div>

              <div className="flex items-center gap-3">
                <span className="text-3xl font-bold text-gray-900">€{recommended.price}</span>
                {recommended.originalPrice && (
                  <span className="text-lg text-gray-500 line-through">€{recommended.originalPrice}</span>
                )}
              </div>

              <p className="text-gray-600 leading-relaxed">{recommended.description}</p>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-semibold text-green-700 mb-2">Pros</h4>
                  <ul className="space-y-1">
                    {(recommended.pros || recommended.features.slice(0, 3)).map((pro, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-center gap-2">
                        <span className="text-green-500">✓</span>
                        {pro}
                      </li>
                    ))}
                  </ul>
                </div>
                {recommended.cons && (
                  <div>
                    <h4 className="font-semibold text-red-700 mb-2">Cons</h4>
                    <ul className="space-y-1">
                      {recommended.cons.map((con, index) => (
                        <li key={index} className="text-sm text-gray-600 flex items-center gap-2">
                          <span className="text-red-500">✗</span>
                          {con}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              <div className="space-y-3 pt-4">
                {/* Store Buttons */}
                <div className="grid grid-cols-2 gap-2">
                  {recommended.storeLinks?.amazon && (
                    <Link
                      href={recommended.storeLinks.amazon}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-gradient-to-r from-orange-500 to-yellow-500 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-orange-600 hover:to-yellow-600 transition-all shadow-lg text-sm"
                    >
                      🛒 Amazon
                    </Link>
                  )}
                  {recommended.storeLinks?.thomann && (
                    <Link
                      href={recommended.storeLinks.thomann}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-gradient-to-r from-blue-600 to-blue-700 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg text-sm"
                    >
                      🎵 Thomann
                    </Link>
                  )}
                  {recommended.storeLinks?.sweetwater && (
                    <Link
                      href={recommended.storeLinks.sweetwater}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-gradient-to-r from-green-600 to-green-700 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-green-700 hover:to-green-800 transition-all shadow-lg text-sm"
                    >
                      🎸 Sweetwater
                    </Link>
                  )}
                  {recommended.storeLinks?.guitarCenter && (
                    <Link
                      href={recommended.storeLinks.guitarCenter}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-gradient-to-r from-red-600 to-red-700 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-red-700 hover:to-red-800 transition-all shadow-lg text-sm"
                    >
                      🎼 Guitar Center
                    </Link>
                  )}
                  {recommended.storeLinks?.musiciansFriend && (
                    <Link
                      href={recommended.storeLinks.musiciansFriend}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-gradient-to-r from-purple-600 to-purple-700 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-purple-700 hover:to-purple-800 transition-all shadow-lg text-sm"
                    >
                      🎵 Musician's Friend
                    </Link>
                  )}
                  {!recommended.storeLinks && (
                    <Link
                      href={recommended.affiliateUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg text-sm"
                    >
                      Check Best Price
                    </Link>
                  )}
                </div>
                
                {/* Review Link */}
                <Link
                  href={`/products/${recommended.slug}`}
                  className="block w-full bg-gray-100 text-gray-900 text-center py-3 px-6 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
                >
                  Read Full Review
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Other Products Grid */}
        {others.length > 0 && (
          <div className="grid md:grid-cols-2 gap-6">
            {others.map((product) => (
              <div key={product.id} className="bg-white rounded-lg p-6 shadow-md border border-gray-100 hover:shadow-lg transition-shadow">
                <div className="flex items-center gap-3 mb-4">
                  <div className="relative h-20 w-20 bg-gray-100 rounded-lg overflow-hidden">
                    <Image
                      src={product.image}
                      alt={product.name}
                      fill
                      className=""
                  style={{ backgroundColor: 'white' }}
                    />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold text-gray-900">{product.name}</h4>
                    <p className="text-sm text-gray-600">{product.brand}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <div className="flex items-center gap-1">
                        {[...Array(5)].map((_, i) => (
                          <span key={i} className={`text-xs ${i < Math.floor(product.rating) ? 'text-yellow-400' : 'text-gray-300'}`}>
                            ★
                          </span>
                        ))}
                      </div>
                      <span className="text-xs text-gray-600">({product.reviewCount})</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <span className="text-xl font-bold text-gray-900">€{product.price}</span>
                    {product.originalPrice && (
                      <span className="text-sm text-gray-500 line-through">€{product.originalPrice}</span>
                    )}
                  </div>
                  {discount(product) > 0 && (
                    <span className="bg-red-100 text-red-800 px-2 py-1 rounded text-xs font-bold">
                      -{discount(product)}%
                    </span>
                  )}
                </div>

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
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  // Grid Style - Clean grid layout
  if (style === 'grid') {
    return (
      <div className="my-12">
        {title && (
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">{title}</h2>
            {subtitle && <p className="text-lg text-gray-600">{subtitle}</p>}
          </div>
        )}

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {displayProducts.map((product) => (
            <div key={product.id} className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-shadow">
              <div className="relative h-48 bg-gray-100">
                <Image
                  src={product.image}
                  alt={product.name}
                  fill
                  className=""
                  style={{ backgroundColor: 'white' }}
                />
                {discount(product) > 0 && (
                  <div className="absolute top-3 left-3 bg-red-600 text-white px-2 py-1 rounded-lg text-xs font-bold">
                    -{discount(product)}%
                  </div>
                )}
                {product.isRecommended && (
                  <div className="absolute top-3 right-3 bg-yellow-500 text-white px-2 py-1 rounded-lg text-xs font-bold">
                    ⭐ Top Pick
                  </div>
                )}
              </div>

              <div className="p-6">
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">{product.brand}</span>
                  <span className="text-gray-400">•</span>
                  <span className="text-xs text-gray-500">{product.category}</span>
                </div>

                <h3 className="font-bold text-gray-900 mb-3 line-clamp-2">{product.name}</h3>

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

                <div className="flex items-center gap-2 mb-4">
                  <span className="text-xl font-bold text-gray-900">€{product.price}</span>
                  {product.originalPrice && (
                    <span className="text-sm text-gray-500 line-through">€{product.originalPrice}</span>
                  )}
                </div>

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
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Carousel Style - Horizontal scroll
  if (style === 'carousel') {
    return (
      <div className="my-12">
        {title && (
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">{title}</h2>
            {subtitle && <p className="text-lg text-gray-600">{subtitle}</p>}
          </div>
        )}

        <div className="flex gap-6 overflow-x-auto pb-4 scrollbar-hide">
          {displayProducts.map((product) => (
            <div key={product.id} className="flex-shrink-0 w-80 bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
              <div className="relative h-48 bg-gray-100">
                <Image
                  src={product.image}
                  alt={product.name}
                  fill
                  className=""
                  style={{ backgroundColor: 'white' }}
                />
                {discount(product) > 0 && (
                  <div className="absolute top-3 left-3 bg-red-600 text-white px-2 py-1 rounded-lg text-xs font-bold">
                    -{discount(product)}%
                  </div>
                )}
                {product.isRecommended && (
                  <div className="absolute top-3 right-3 bg-yellow-500 text-white px-2 py-1 rounded-lg text-xs font-bold">
                    ⭐ Top Pick
                  </div>
                )}
              </div>

              <div className="p-6">
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">{product.brand}</span>
                  <span className="text-gray-400">•</span>
                  <span className="text-xs text-gray-500">{product.category}</span>
                </div>

                <h3 className="font-bold text-gray-900 mb-3 line-clamp-2">{product.name}</h3>

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

                <div className="flex items-center gap-2 mb-4">
                  <span className="text-xl font-bold text-gray-900">€{product.price}</span>
                  {product.originalPrice && (
                    <span className="text-sm text-gray-500 line-through">€{product.originalPrice}</span>
                  )}
                </div>

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
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Recommended Style - Single recommended product with alternatives
  if (style === 'recommended') {
    const recommended = displayProducts.find(p => p.isRecommended) || displayProducts[0];
    const alternatives = displayProducts.filter(p => p.id !== recommended.id);

    return (
      <div className="my-12 bg-gradient-to-r from-green-50 to-blue-50 rounded-2xl p-8 border border-green-200">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-3">{title || 'Our Top Recommendation'}</h2>
          {subtitle && <p className="text-lg text-gray-600">{subtitle}</p>}
        </div>

        {/* Main Recommendation */}
        <div className="bg-white rounded-xl p-8 shadow-lg border border-gray-100 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <span className="bg-gradient-to-r from-green-500 to-blue-600 text-white px-4 py-2 rounded-full text-sm font-bold">
              🏆 Best Overall
            </span>
            {recommended.badge && (
              <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-bold">
                {recommended.badge}
              </span>
            )}
          </div>

          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div className="relative">
              <div className="relative h-80 bg-gray-100 rounded-lg overflow-hidden shadow-lg">
                <Image
                  src={recommended.image}
                  alt={recommended.name}
                  fill
                  className=""
                  style={{ backgroundColor: 'white' }}
                />
                {discount(recommended) > 0 && (
                  <div className="absolute top-4 left-4 bg-red-600 text-white px-3 py-2 rounded-lg text-sm font-bold">
                    Save {discount(recommended)}%
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-2xl font-bold text-gray-900">{recommended.name}</h3>
              <p className="text-gray-600 leading-relaxed">{recommended.description}</p>

              <div className="flex items-center gap-3">
                <span className="text-3xl font-bold text-gray-900">€{recommended.price}</span>
                {recommended.originalPrice && (
                  <span className="text-lg text-gray-500 line-through">€{recommended.originalPrice}</span>
                )}
              </div>

              <div className="flex items-center gap-3">
                <div className="flex items-center gap-1">
                  {[...Array(5)].map((_, i) => (
                    <span key={i} className={`text-lg ${i < Math.floor(recommended.rating) ? 'text-yellow-400' : 'text-gray-300'}`}>
                      ★
                    </span>
                  ))}
                </div>
                <span className="text-gray-600">({recommended.reviewCount} reviews)</span>
              </div>

              {recommended.bestFor && (
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">Perfect For:</h4>
                  <p className="text-blue-800">{recommended.bestFor}</p>
                </div>
              )}

              <div className="grid grid-cols-2 gap-2">
                {recommended.storeLinks?.amazon && (
                  <Link
                    href={recommended.storeLinks.amazon}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-gradient-to-r from-orange-500 to-yellow-500 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-orange-600 hover:to-yellow-600 transition-all shadow-lg text-sm"
                  >
                    🛒 Amazon
                  </Link>
                )}
                {recommended.storeLinks?.thomann && (
                  <Link
                    href={recommended.storeLinks.thomann}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-gradient-to-r from-blue-600 to-blue-700 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg text-sm"
                  >
                    🎵 Thomann
                  </Link>
                )}
                {recommended.storeLinks?.sweetwater && (
                  <Link
                    href={recommended.storeLinks.sweetwater}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-gradient-to-r from-green-600 to-green-700 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-green-700 hover:to-green-800 transition-all shadow-lg text-sm"
                  >
                    🎸 Sweetwater
                  </Link>
                )}
                {!recommended.storeLinks && (
                  <Link
                    href={recommended.affiliateUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-gradient-to-r from-green-600 to-blue-600 text-white text-center py-3 px-4 rounded-lg font-semibold hover:from-green-700 hover:to-blue-700 transition-all shadow-lg text-sm"
                  >
                    Get Best Price
                  </Link>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Alternative Options */}
        {alternatives.length > 0 && (
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-6 text-center">Alternative Options</h3>
            <div className="grid md:grid-cols-2 gap-6">
              {alternatives.map((product, index) => (
                <div key={product.id} className="bg-white rounded-lg p-6 shadow-md border border-gray-100">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="relative h-16 w-16 bg-gray-100 rounded-lg overflow-hidden">
                      <Image
                        src={product.image}
                        alt={product.name}
                        fill
                        className=""
                  style={{ backgroundColor: 'white' }}
                      />
                    </div>
                    <div className="flex-1">
                      <h4 className="font-bold text-gray-900">{product.name}</h4>
                      <p className="text-sm text-gray-600">{product.brand}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-lg font-bold text-gray-900">€{product.price}</span>
                        {product.originalPrice && (
                          <span className="text-sm text-gray-500 line-through">€{product.originalPrice}</span>
                        )}
                      </div>
                    </div>
                  </div>

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
                    {!product.storeLinks && (
                      <Link
                        href={product.affiliateUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-gray-100 text-gray-900 text-center py-2 px-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors text-xs"
                      >
                        View Alternative
                      </Link>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }

  // Default fallback
  return (
    <div className="my-12">
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {displayProducts.map((product) => (
          <div key={product.id} className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
            <h3 className="font-bold text-gray-900 mb-2">{product.name}</h3>
            <p className="text-gray-600 mb-4">{product.description}</p>
            <Link
              href={product.affiliateUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="block w-full bg-blue-600 text-white text-center py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Check Price
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import type { Product } from '@/types';
import { trackProductView, trackEvent } from '@/components/Analytics';
import { formatPrice, formatRating } from '@/lib/utils';
import ComprehensiveProductDetails from '@/components/ComprehensiveProductDetails';
import TechnicalSpecifications from '@/components/TechnicalSpecifications';
import ProductOverview from '@/components/ProductOverview';

interface ProductDetailClientProps {
  product: Product;
}

export default function ProductDetailClient({ product }: ProductDetailClientProps) {
  const [selectedImage, setSelectedImage] = useState(0);
  const [showSimilarProducts, setShowSimilarProducts] = useState(true);

  useEffect(() => {
    // Track product view
    trackProductView(
      product.id.toString(),
      product.name,
      product.category?.name || 'unknown',
      product.best_price?.price
    );
  }, [product]);

  return (
    <div className="min-h-screen bg-primary-50">
      {/* Ad Space - Top */}
      <section className="py-4 bg-white border-b">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-primary-600 to-accent-600 rounded-lg p-4 text-white text-center">
            <p className="text-sm">🎵 Compare prices across Europe's top music stores</p>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="flex items-center space-x-2 text-sm text-primary-600 mb-6">
          <Link href="/" className="hover:text-primary-800">Home</Link>
          <span>/</span>
          <Link href="/products" className="hover:text-primary-800">Products</Link>
          <span>/</span>
          <Link href={`/products?category=${product.category.slug}`} className="hover:text-primary-800">{product.category.name}</Link>
          <span>/</span>
          <span className="text-primary-900">{product.name}</span>
        </nav>

        {/* Product Header */}
        <div className="bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden mb-8">
          <div className="grid lg:grid-cols-2 gap-8 p-8">
            {/* Images */}
            <div>
              <div className="aspect-square bg-gradient-to-br from-primary-100 to-primary-200 rounded-lg overflow-hidden mb-4 flex items-center justify-center">
                {product.images && product.images.length > 0 ? (
                  <img 
                    src={product.images[selectedImage]} 
                    alt={`${product.name} - Image ${selectedImage + 1}`}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <span className="text-primary-400 text-6xl">🎸</span>
                )}
              </div>
              {product.images && product.images.length > 0 && (
                <div className="flex items-center gap-2 overflow-x-auto">
                  {product.images.map((img, idx) => (
                    <button 
                      key={idx} 
                      onClick={() => setSelectedImage(idx)} 
                      className={`w-16 h-16 rounded border-2 flex-shrink-0 overflow-hidden ${
                        idx === selectedImage ? 'border-primary-600' : 'border-primary-200'
                      }`}
                    >
                      <img 
                        src={img} 
                        alt={`${product.name} thumbnail ${idx + 1}`}
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Product Info */}
            <div className="space-y-6">
              <div>
                <div className="flex items-center gap-4 mb-3">
                  <Link href={`/products?brand=${product.brand.slug}`} className="text-primary-600 hover:text-primary-800 font-medium">
                    {product.brand.name}
                  </Link>
                  <span className="text-sm text-primary-500">SKU: {product.sku}</span>
                </div>
                <h1 className="text-3xl font-bold text-primary-900 mb-2">{product.name}</h1>
                <div className="flex items-center gap-4">
                  {product.avg_rating > 0 && (
                    <div className="flex items-center gap-2">
                      <span className="text-warning-500">★</span>
                      <span className="font-medium">{formatRating(product.avg_rating)}</span>
                      <span className="text-primary-500">({product.review_count} reviews)</span>
                    </div>
                  )}
                  <span className="text-sm text-primary-600">{product.category.name}</span>
                </div>
              </div>

              {/* Expert Ratings - Prominent display */}
              {product.ai_content && (
                <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-primary-900 mb-3">Expert Ratings</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div className="text-center p-3 bg-white rounded-lg border border-primary-200">
                      <div className="text-xl font-bold text-success-600">{product.ai_content.professional_assessment.expert_rating.build_quality}/10</div>
                      <div className="text-xs text-primary-600">Build Quality</div>
                    </div>
                    <div className="text-center p-3 bg-white rounded-lg border border-primary-200">
                      <div className="text-xl font-bold text-accent-600">{product.ai_content.professional_assessment.expert_rating.sound_quality}/10</div>
                      <div className="text-xs text-primary-600">Sound Quality</div>
                    </div>
                    <div className="text-center p-3 bg-white rounded-lg border border-primary-200">
                      <div className="text-xl font-bold text-warning-600">{product.ai_content.professional_assessment.expert_rating.value_for_money}/10</div>
                      <div className="text-xs text-primary-600">Value</div>
                    </div>
                    <div className="text-center p-3 bg-white rounded-lg border border-primary-200">
                      <div className="text-xl font-bold text-primary-600">{product.ai_content.professional_assessment.expert_rating.versatility}/10</div>
                      <div className="text-xs text-primary-600">Versatility</div>
                    </div>
                  </div>
                </div>
              )}

              {/* Store Availability */}
              <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
                <div>
                  <p className="text-sm text-primary-700 font-medium mb-3">Available at {product.prices?.length || 0} Store{product.prices?.length !== 1 ? 's' : ''}</p>
                  {product.prices && product.prices.length > 0 ? (
                    <div className="space-y-2">
                      {product.prices.slice(0, 3).map((price) => {
                        const isThomann = price.store.name.toLowerCase().includes('thomann');
                        const isGear4Music = price.store.name.toLowerCase().includes('gear4music');
                        
                        if (isThomann) {
                          return (
                            <a
                              key={price.id}
                              href={price.affiliate_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className={`fp-table__button fp-table__button--thomann ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                              onClick={() => trackEvent('affiliate_click', { store: 'thomann', product_id: product.id })}
                            >
                              <span>View Price at</span>
                              <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" />
                            </a>
                          );
                        } else if (isGear4Music) {
                          return (
                            <a
                              key={price.id}
                              href={price.affiliate_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className={`fp-table__button fp-table__button--gear4music ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                              onClick={() => trackEvent('affiliate_click', { store: 'gear4music', product_id: product.id })}
                            >
                              <span>View Price at</span>
                              <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" />
                            </a>
                          );
                        } else {
                          return (
                            <a
                              key={price.id}
                              href={price.affiliate_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className={`fp-table__button ${!price.is_available ? 'opacity-50 cursor-not-allowed' : ''}`}
                              onClick={() => trackEvent('affiliate_click', { store: price.store.name, product_id: product.id })}
                            >
                              <span>View Price at</span>
                              <span className="font-medium">{price.store.name}</span>
                            </a>
                          );
                        }
                      })}
                      {product.prices.length > 3 && (
                        <p className="text-xs text-primary-500 text-center">
                          +{product.prices.length - 3} more stores available
                        </p>
                      )}
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <a
                        href={`https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(product.name)}&aff=123`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="fp-table__button fp-table__button--thomann"
                        onClick={() => trackEvent('affiliate_click', { store: 'thomann', product_id: product.id })}
                      >
                        <span>View Price at</span>
                        <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" />
                      </a>
                      <a
                        href={`https://gear4music.com/search?search=${encodeURIComponent(product.name)}&aff=123`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="fp-table__button fp-table__button--gear4music"
                        onClick={() => trackEvent('affiliate_click', { store: 'gear4music', product_id: product.id })}
                      >
                        <span>View Price at</span>
                        <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" />
                      </a>
                    </div>
                  )}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="flex gap-3">
                <Link 
                  href={`/compare?products=${product.slug}`}
                  className="flex-1 bg-primary-600 text-white py-3 px-4 rounded-lg hover:bg-primary-700 transition-colors text-center font-medium"
                  onClick={() => trackEvent('compare_click', { product_id: product.id })}
                >
                  Compare
                </Link>
                <button className="px-4 py-3 border border-primary-300 text-primary-700 rounded-lg hover:bg-primary-50 transition-colors">
                  Add to List
                </button>
                <button className="px-4 py-3 border border-primary-300 text-primary-700 rounded-lg hover:bg-primary-50 transition-colors">
                  ❤
                </button>
              </div>

              {/* Description */}
              {product.description && (
                <div>
                  <h3 className="font-semibold text-primary-900 mb-2">Description</h3>
                  <p className="text-primary-700 leading-relaxed">{product.description}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Overview */}
        <ProductOverview product={product} />

        {/* Technical Specifications */}
        <TechnicalSpecifications product={product} />

        {/* Comprehensive Product Details */}
        <ComprehensiveProductDetails product={product} />

        {/* Reviews Section */}
        <div className="bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden mt-8 mb-8">
          <div className="p-8">
            <h2 className="text-2xl font-bold text-primary-900 mb-6 flex items-center gap-2">
              <span className="text-2xl">⭐</span>
              Customer Reviews
            </h2>
            <div className="space-y-6">
              <div className="flex items-center gap-4">
                <div className="text-center">
                  <div className="text-4xl font-bold text-primary-900">{formatRating(product.avg_rating)}</div>
                  <div className="flex items-center justify-center gap-1 mt-1">
                    {[...Array(5)].map((_, i) => (
                      <span key={i} className={`text-lg ${i < Math.floor(product.avg_rating) ? 'text-warning-500' : 'text-primary-300'}`}>
                        ★
                      </span>
                    ))}
                  </div>
                  <div className="text-sm text-primary-600 mt-1">{product.review_count} reviews</div>
                </div>
                <div className="flex-1">
                  <div className="text-sm text-primary-600">
                    {product.avg_rating >= 4.5 && "Excellent customer satisfaction with outstanding quality and performance"}
                    {product.avg_rating >= 4.0 && product.avg_rating < 4.5 && "Very good customer satisfaction with reliable performance"}
                    {product.avg_rating >= 3.5 && product.avg_rating < 4.0 && "Good customer satisfaction with solid performance"}
                    {product.avg_rating < 3.5 && "Mixed customer reviews with some concerns"}
                  </div>
                </div>
              </div>
              
              {/* Review Summary */}
              <div className="bg-primary-50 rounded-lg p-4">
                <h3 className="font-semibold text-primary-900 mb-3">What customers say</h3>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-primary-600">Build Quality</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-primary-200 rounded-full h-2">
                        <div className="bg-success-500 h-2 rounded-full" style={{ width: `${(product.ai_content?.professional_assessment.expert_rating.build_quality || 0) * 10}%` }}></div>
                      </div>
                      <span className="text-sm font-medium">{product.ai_content?.professional_assessment.expert_rating.build_quality || 0}/10</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-primary-600">Sound Quality</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-primary-200 rounded-full h-2">
                        <div className="bg-accent-500 h-2 rounded-full" style={{ width: `${(product.ai_content?.professional_assessment.expert_rating.sound_quality || 0) * 10}%` }}></div>
                      </div>
                      <span className="text-sm font-medium">{product.ai_content?.professional_assessment.expert_rating.sound_quality || 0}/10</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-primary-600">Value for Money</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-primary-200 rounded-full h-2">
                        <div className="bg-warning-500 h-2 rounded-full" style={{ width: `${(product.ai_content?.professional_assessment.expert_rating.value_for_money || 0) * 10}%` }}></div>
                      </div>
                      <span className="text-sm font-medium">{product.ai_content?.professional_assessment.expert_rating.value_for_money || 0}/10</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-primary-600">Versatility</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-primary-200 rounded-full h-2">
                        <div className="bg-primary-500 h-2 rounded-full" style={{ width: `${(product.ai_content?.professional_assessment.expert_rating.versatility || 0) * 10}%` }}></div>
                      </div>
                      <span className="text-sm font-medium">{product.ai_content?.professional_assessment.expert_rating.versatility || 0}/10</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Similar Products */}
        {showSimilarProducts && (
          <div className="bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden mt-8">
            <div className="p-8">
              <h2 className="text-2xl font-bold text-primary-900 mb-6">Similar Products</h2>
              <p className="text-primary-600 mb-4">Discover other great options in this category</p>
              <Link 
                href={`/products?category=${product.category.slug}`}
                className="inline-flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors"
              >
                Browse {product.category.name}
                <span>→</span>
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

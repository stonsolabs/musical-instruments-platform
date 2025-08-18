'use client';

import React, { useEffect, useMemo, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import type { Product } from '@/types';
import { trackProductView, trackEvent } from '@/components/Analytics';
import { getApiBaseUrl } from '@/lib/api';

// Inline utility functions
const formatPrice = (price: number, currency: string = 'EUR'): string => {
  try {
    return new Intl.NumberFormat('en-GB', { style: 'currency', currency }).format(price);
  } catch {
    return `${currency} ${price.toFixed(2)}`;
  }
};

const formatRating = (rating: number): string => {
  return Number.isFinite(rating) ? rating.toFixed(1) : '0.0';
};

const API_BASE_URL = getApiBaseUrl();

const apiClient = {
  async getProduct(productId: number): Promise<Product> {
    if (typeof window === 'undefined') {
      throw new Error('API calls are not available during build time');
    }
    
    const response = await fetch(`/api/proxy/products/${productId}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  }
};

export default function ProductDetailPage() {
  const params = useParams();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedImage, setSelectedImage] = useState(0);

  const productId = useMemo(() => {
    const slug = (params?.slug as string) || '';
    const idPart = slug.split('-').pop();
    const idNum = Number(idPart);
    return Number.isFinite(idNum) ? idNum : null;
  }, [params?.slug]);

  useEffect(() => {
    const load = async () => {
      if (!productId) {
        setError('Invalid product ID');
        setLoading(false);
        return;
      }
      try {
        const data = await apiClient.getProduct(productId);
        setProduct(data);
        
        // Track product view
        trackProductView(
          data.id.toString(),
          data.name,
          data.category?.name || 'unknown',
          data.best_price?.price
        );
      } catch (e) {
        setError('Product not found');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [productId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto" />
          <p className="mt-4 text-gray-600">Loading product...</p>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Product Not Found</h1>
          <Link href="/products" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">Browse All Products</Link>
        </div>
      </div>
    );
  }



  return (
    <div className="min-h-screen bg-gray-50">
      {/* Ad Space - Top */}
      <section className="py-4 bg-white border-b">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-4 text-white text-center">
            <p className="text-sm">🎵 Compare prices across Europe's top music stores</p>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="flex items-center space-x-2 text-sm text-gray-600 mb-6">
          <Link href="/" className="hover:text-blue-600">Home</Link>
          <span>/</span>
          <Link href="/products" className="hover:text-blue-600">Products</Link>
          <span>/</span>
          <Link href={`/products?category=${product.category.slug}`} className="hover:text-blue-600">{product.category.name}</Link>
          <span>/</span>
          <span className="text-gray-900">{product.name}</span>
        </nav>

        {/* Product Header */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-8">
          <div className="grid lg:grid-cols-2 gap-8 p-8">
            {/* Images */}
            <div>
              <div className="aspect-square bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg overflow-hidden mb-4 flex items-center justify-center">
                <span className="text-gray-400 text-6xl">🎸</span>
              </div>
              {product.images?.length > 0 && (
                <div className="flex items-center gap-2 overflow-x-auto">
                  {product.images.map((img, idx) => (
                    <button 
                      key={idx} 
                      onClick={() => setSelectedImage(idx)} 
                      className={`w-16 h-16 rounded border-2 flex-shrink-0 ${
                        idx === selectedImage ? 'border-blue-600' : 'border-gray-200'
                      }`}
                    >
                      <div className="w-full h-full bg-gray-100 rounded flex items-center justify-center">
                        <span className="text-gray-400 text-sm">{idx + 1}</span>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Product Info */}
            <div className="space-y-6">
              <div>
                <div className="flex items-center gap-4 mb-3">
                  <Link href={`/products?brand=${product.brand.slug}`} className="text-blue-600 hover:text-blue-800 font-medium">
                    {product.brand.name}
                  </Link>
                  <span className="text-sm text-gray-500">SKU: {product.sku}</span>
                </div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
                <div className="flex items-center gap-4">
                  {product.avg_rating > 0 && (
                    <div className="flex items-center gap-2">
                      <span className="text-yellow-500">★</span>
                      <span className="font-medium">{formatRating(product.avg_rating)}</span>
                      <span className="text-gray-500">({product.review_count} reviews)</span>
                    </div>
                  )}
                  <span className="text-sm text-gray-600">{product.category.name}</span>
                </div>
              </div>

              {/* Store Availability */}
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <div>
                  <p className="text-sm text-gray-700 font-medium mb-3">Available at {product.prices?.length || 0} Store{product.prices?.length !== 1 ? 's' : ''}</p>
                  {product.prices && product.prices.length > 0 ? (
                    <div className="space-y-2">
                      {product.prices.slice(0, 3).map((price) => (
                        <a
                          key={price.id}
                          href={price.affiliate_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className={`block w-full text-center py-2 rounded-lg transition-colors text-sm font-medium ${
                            price.is_available
                              ? 'bg-gray-800 text-white hover:bg-gray-700'
                              : 'bg-gray-300 text-gray-600 cursor-not-allowed'
                          }`}
                        >
                          {price.store.name}
                          {!price.is_available && ' (Out of Stock)'}
                        </a>
                      ))}
                      {product.prices.length > 3 && (
                        <p className="text-xs text-gray-500 text-center">
                          +{product.prices.length - 3} more stores available
                        </p>
                      )}
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500">No stores available</p>
                  )}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="flex gap-3">
                <Link 
                  href={`/compare?ids=${product.id}`}
                  className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors text-center font-medium"
                >
                  Compare
                </Link>
                <button className="px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                  Add to List
                </button>
                <button className="px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                  ❤
                </button>
              </div>

              {/* Description */}
              {product.description && (
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Description</h3>
                  <p className="text-gray-700 leading-relaxed">{product.description}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Product Content - All AI-Generated Sections */}
        <div className="space-y-8">
          {/* Basic Info Section */}
          {product.ai_generated_content?.basic_info && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">📋 Basic Information</h3>
              
              {/* Overview */}
              {product.ai_generated_content.basic_info.overview && (
                <div className="mb-6">
                  <h4 className="font-semibold text-gray-900 mb-3">Overview</h4>
                  <p className="text-gray-700 leading-relaxed">{product.ai_generated_content.basic_info.overview}</p>
                </div>
              )}

              {/* Key Features */}
              {product.ai_generated_content.basic_info.key_features && (
                <div className="mb-6">
                  <h4 className="font-semibold text-gray-900 mb-3">Key Features</h4>
                  <div className="grid md:grid-cols-2 gap-2">
                    {product.ai_generated_content.basic_info.key_features.map((feature: string, index: number) => (
                      <div key={index} className="flex items-start gap-2">
                        <span className="text-blue-600 mt-1">•</span>
                        <span className="text-gray-700">{feature}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Additional Basic Info */}
              <div className="grid md:grid-cols-3 gap-6">
                {product.ai_generated_content.basic_info.target_skill_level && (
                  <div>
                    <h5 className="font-medium text-gray-900 mb-2">Target Skill Level</h5>
                    <p className="text-gray-700">{product.ai_generated_content.basic_info.target_skill_level}</p>
                  </div>
                )}
                {product.ai_generated_content.basic_info.country_of_origin && (
                  <div>
                    <h5 className="font-medium text-gray-900 mb-2">Country of Origin</h5>
                    <p className="text-gray-700">{product.ai_generated_content.basic_info.country_of_origin}</p>
                  </div>
                )}
                {product.ai_generated_content.basic_info.release_year && (
                  <div>
                    <h5 className="font-medium text-gray-900 mb-2">Release Year</h5>
                    <p className="text-gray-700">{product.ai_generated_content.basic_info.release_year}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Technical Analysis Section */}
          {product.ai_generated_content?.technical_analysis && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">🔧 Technical Analysis</h3>
              
              {/* Sound Characteristics */}
              {product.ai_generated_content.technical_analysis.sound_characteristics && (
                <div className="mb-6">
                  <h4 className="font-semibold text-gray-900 mb-4">Sound Characteristics</h4>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      {product.ai_generated_content.technical_analysis.sound_characteristics.tonal_profile && (
                        <div className="mb-4">
                          <h5 className="font-medium text-gray-900 mb-2">Tonal Profile</h5>
                          <p className="text-gray-700">{product.ai_generated_content.technical_analysis.sound_characteristics.tonal_profile}</p>
                        </div>
                      )}
                      {product.ai_generated_content.technical_analysis.sound_characteristics.output_level && (
                        <div className="mb-4">
                          <h5 className="font-medium text-gray-900 mb-2">Output Level</h5>
                          <p className="text-gray-700">{product.ai_generated_content.technical_analysis.sound_characteristics.output_level}</p>
                        </div>
                      )}
                    </div>
                    <div>
                      {product.ai_generated_content.technical_analysis.sound_characteristics.best_genres && (
                        <div>
                          <h5 className="font-medium text-gray-900 mb-2">Best Genres</h5>
                          <div className="flex flex-wrap gap-2">
                            {product.ai_generated_content.technical_analysis.sound_characteristics.best_genres.map((genre: string, index: number) => (
                              <span key={index} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">{genre}</span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Pickup Positions */}
                  {product.ai_generated_content.technical_analysis.sound_characteristics.pickup_positions && (
                    <div className="mt-4">
                      <h5 className="font-medium text-gray-900 mb-3">Pickup Positions</h5>
                      <div className="space-y-2">
                        {Object.entries(product.ai_generated_content.technical_analysis.sound_characteristics.pickup_positions).map(([position, description]) => (
                          <div key={position} className="bg-gray-50 p-3 rounded-lg">
                            <span className="font-medium text-gray-900 capitalize">{position.replace(/_/g, ' ')}: </span>
                            <span className="text-gray-700">{String(description)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Build Quality & Playability */}
              <div className="grid md:grid-cols-2 gap-6">
                {product.ai_generated_content.technical_analysis.build_quality && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Build Quality</h4>
                    <div className="space-y-3">
                      {Object.entries(product.ai_generated_content.technical_analysis.build_quality).map(([key, value]) => (
                        <div key={key} className="flex justify-between py-2 border-b border-gray-100">
                          <span className="font-medium text-gray-700 capitalize">{key.replace(/_/g, ' ')}</span>
                          <span className="text-gray-900">{String(value)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {product.ai_generated_content.technical_analysis.playability && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Playability</h4>
                    <div className="space-y-3">
                      {Object.entries(product.ai_generated_content.technical_analysis.playability).map(([key, value]) => (
                        <div key={key} className="flex justify-between py-2 border-b border-gray-100">
                          <span className="font-medium text-gray-700 capitalize">{key.replace(/_/g, ' ')}</span>
                          <span className="text-gray-900">{String(value)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Purchase Decision Section */}
          {product.ai_generated_content?.purchase_decision && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">🛒 Purchase Decision</h3>
              
              <div className="grid md:grid-cols-2 gap-8">
                {/* Why Buy */}
                {product.ai_generated_content.purchase_decision.why_buy && (
                  <div>
                    <h4 className="font-semibold text-green-700 mb-4">✅ Why You Should Buy</h4>
                    <div className="space-y-4">
                      {product.ai_generated_content.purchase_decision.why_buy.map((item: any, index: number) => (
                        <div key={index} className="bg-green-50 border-l-4 border-green-500 p-4">
                          <h5 className="font-medium text-green-900 mb-2">{item.title}</h5>
                          <p className="text-green-700 text-sm">{item.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Why Not Buy */}
                {product.ai_generated_content.purchase_decision.why_not_buy && (
                  <div>
                    <h4 className="font-semibold text-red-700 mb-4">❌ Potential Drawbacks</h4>
                    <div className="space-y-4">
                      {product.ai_generated_content.purchase_decision.why_not_buy.map((item: any, index: number) => (
                        <div key={index} className="bg-red-50 border-l-4 border-red-500 p-4">
                          <h5 className="font-medium text-red-900 mb-2">{item.title}</h5>
                          <p className="text-red-700 text-sm">{item.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="grid md:grid-cols-2 gap-8 mt-8">
                {/* Best For */}
                {product.ai_generated_content.purchase_decision.best_for && (
                  <div>
                    <h4 className="font-semibold text-blue-700 mb-4">🎯 Best For</h4>
                    <div className="space-y-3">
                      {product.ai_generated_content.purchase_decision.best_for.map((item: any, index: number) => (
                        <div key={index} className="bg-blue-50 p-3 rounded-lg">
                          <h5 className="font-medium text-blue-900">{item.user_type}</h5>
                          <p className="text-blue-700 text-sm mt-1">{item.reason}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Not Ideal For */}
                {product.ai_generated_content.purchase_decision.not_ideal_for && (
                  <div>
                    <h4 className="font-semibold text-orange-700 mb-4">⚠️ Not Ideal For</h4>
                    <div className="space-y-3">
                      {product.ai_generated_content.purchase_decision.not_ideal_for.map((item: any, index: number) => (
                        <div key={index} className="bg-orange-50 p-3 rounded-lg">
                          <h5 className="font-medium text-orange-900">{item.user_type}</h5>
                          <p className="text-orange-700 text-sm mt-1">{item.reason}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Usage Guidance Section */}
          {product.ai_generated_content?.usage_guidance && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">🎵 Usage Guidance</h3>
              
              <div className="grid md:grid-cols-2 gap-8">
                {/* Recommended Amplifiers */}
                {product.ai_generated_content.usage_guidance.recommended_amplifiers && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Recommended Amplifiers</h4>
                    <div className="space-y-2">
                      {product.ai_generated_content.usage_guidance.recommended_amplifiers.map((amp: string, index: number) => (
                        <div key={index} className="flex items-start gap-2">
                          <span className="text-blue-600 mt-1">•</span>
                          <span className="text-gray-700">{amp}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Skill Development */}
                {product.ai_generated_content.usage_guidance.skill_development && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Skill Development</h4>
                    <div className="space-y-3">
                      {Object.entries(product.ai_generated_content.usage_guidance.skill_development).map(([key, value]) => (
                        <div key={key}>
                          <h5 className="font-medium text-gray-700 capitalize">{key.replace(/_/g, ' ')}</h5>
                          <p className="text-gray-600 text-sm">{String(value)}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Music Styles */}
              {product.ai_generated_content.usage_guidance.suitable_music_styles && (
                <div className="mt-6">
                  <h4 className="font-semibold text-gray-900 mb-4">Suitable Music Styles</h4>
                  <div className="grid md:grid-cols-3 gap-6">
                    {Object.entries(product.ai_generated_content.usage_guidance.suitable_music_styles).map(([level, genres]) => (
                      <div key={level}>
                        <h5 className={`font-medium mb-2 capitalize ${
                          level === 'excellent' ? 'text-green-700' : 
                          level === 'good' ? 'text-blue-700' : 'text-orange-700'
                        }`}>{level}</h5>
                        <div className="space-y-1">
                          {Array.isArray(genres) && genres.map((genre: string, index: number) => (
                            <span key={index} className={`inline-block px-2 py-1 rounded text-xs mr-1 mb-1 ${
                              level === 'excellent' ? 'bg-green-100 text-green-800' : 
                              level === 'good' ? 'bg-blue-100 text-blue-800' : 'bg-orange-100 text-orange-800'
                            }`}>{genre}</span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Maintenance & Care Section */}
          {product.ai_generated_content?.maintenance_care && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">🔧 Maintenance & Care</h3>
              
              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  {product.ai_generated_content.maintenance_care.maintenance_level && (
                    <div className="mb-6">
                      <h4 className="font-semibold text-gray-900 mb-2">Maintenance Level</h4>
                      <p className="text-gray-700">{product.ai_generated_content.maintenance_care.maintenance_level}</p>
                    </div>
                  )}

                  {product.ai_generated_content.maintenance_care.common_issues && (
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-3">Common Issues</h4>
                      <div className="space-y-2">
                        {product.ai_generated_content.maintenance_care.common_issues.map((issue: string, index: number) => (
                          <div key={index} className="flex items-start gap-2">
                            <span className="text-orange-600 mt-1">⚠️</span>
                            <span className="text-gray-700">{issue}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div>
                  {product.ai_generated_content.maintenance_care.upgrade_potential && (
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-3">Upgrade Potential</h4>
                      {product.ai_generated_content.maintenance_care.upgrade_potential.easy_upgrades && (
                        <div className="mb-4">
                          <h5 className="font-medium text-gray-700 mb-2">Easy Upgrades</h5>
                          <div className="space-y-1">
                            {product.ai_generated_content.maintenance_care.upgrade_potential.easy_upgrades.map((upgrade: string, index: number) => (
                              <div key={index} className="flex items-start gap-2">
                                <span className="text-green-600 mt-1">✓</span>
                                <span className="text-gray-700 text-sm">{upgrade}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      {product.ai_generated_content.maintenance_care.upgrade_potential.recommended_budget && (
                        <div>
                          <h5 className="font-medium text-gray-700 mb-2">Recommended Budget</h5>
                          <p className="text-gray-600 text-sm">{product.ai_generated_content.maintenance_care.upgrade_potential.recommended_budget}</p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>

              {/* Care Instructions */}
              {product.ai_generated_content.maintenance_care.care_instructions && (
                <div className="mt-6">
                  <h4 className="font-semibold text-gray-900 mb-4">Care Instructions</h4>
                  <div className="grid md:grid-cols-2 gap-6">
                    {Object.entries(product.ai_generated_content.maintenance_care.care_instructions).map(([frequency, instruction]) => (
                      <div key={frequency} className="bg-gray-50 p-4 rounded-lg">
                        <h5 className="font-medium text-gray-900 mb-2 capitalize">{frequency}</h5>
                        <p className="text-gray-700 text-sm">{String(instruction)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Professional Assessment Section */}
          {product.ai_generated_content?.professional_assessment && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">⭐ Professional Assessment</h3>
              
              {/* Expert Ratings */}
              {product.ai_generated_content.professional_assessment.expert_rating && (
                <div className="mb-8">
                  <h4 className="font-semibold text-gray-900 mb-4">Expert Ratings</h4>
                  <div className="grid md:grid-cols-2 gap-6">
                    {Object.entries(product.ai_generated_content.professional_assessment.expert_rating).map(([aspect, rating]) => (
                      <div key={aspect} className="flex justify-between items-center py-3 border-b border-gray-100">
                        <span className="font-medium text-gray-700 capitalize">{aspect.replace(/_/g, ' ')}</span>
                        <div className="flex items-center gap-2">
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-600 h-2 rounded-full" 
                              style={{ width: `${(Number(rating) / 10) * 100}%` }}
                            ></div>
                          </div>
                          <span className="font-semibold text-gray-900">{rating}/10</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="grid md:grid-cols-2 gap-8">
                {/* Standout Features */}
                {product.ai_generated_content.professional_assessment.standout_features && (
                  <div>
                    <h4 className="font-semibold text-green-700 mb-3">🌟 Standout Features</h4>
                    <div className="space-y-2">
                      {product.ai_generated_content.professional_assessment.standout_features.map((feature: string, index: number) => (
                        <div key={index} className="flex items-start gap-2">
                          <span className="text-green-600 mt-1">✓</span>
                          <span className="text-gray-700">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Notable Limitations */}
                {product.ai_generated_content.professional_assessment.notable_limitations && (
                  <div>
                    <h4 className="font-semibold text-orange-700 mb-3">⚠️ Notable Limitations</h4>
                    <div className="space-y-2">
                      {product.ai_generated_content.professional_assessment.notable_limitations.map((limitation: string, index: number) => (
                        <div key={index} className="flex items-start gap-2">
                          <span className="text-orange-600 mt-1">⚠️</span>
                          <span className="text-gray-700">{limitation}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Competitive Position */}
              {product.ai_generated_content.professional_assessment.competitive_position && (
                <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-900 mb-2">Market Position</h4>
                  <p className="text-blue-800">{product.ai_generated_content.professional_assessment.competitive_position}</p>
                </div>
              )}
            </div>
          )}

          {/* Full Specifications Section */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-6">Full Specifications</h3>
            {product.specifications && Object.keys(product.specifications).length > 0 ? (
              <div className="grid md:grid-cols-2 gap-4">
                {Object.entries(product.specifications).map(([key, value]) => (
                  <div key={key} className="flex justify-between py-3 border-b border-gray-100">
                    <span className="font-medium text-gray-700 capitalize">{key.replace(/_/g, ' ')}</span>
                    <span className="text-gray-900">{String(value)}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No specifications available for this product.</p>
            )}
          </div>

          {/* Stores Section */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-6">Available Stores</h3>
            {product.prices && product.prices.length > 0 ? (
              <div className="space-y-4">
                {product.prices.map((price, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                          <span className="text-gray-500 text-lg">🏪</span>
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-900">{price.store.name}</h4>
                          <p className="text-sm text-gray-600">
                            Last checked: {new Date(price.last_checked).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <div className="text-sm text-gray-500">
                            {price.is_available ? 'In Stock' : 'Out of Stock'}
                          </div>
                        </div>
                        <a 
                          href={price.affiliate_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="bg-gray-800 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                        >
                          Buy Now
                        </a>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No stores available for this product.</p>
            )}
          </div>

          {/* Reviews Section */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-6">Reviews & Ratings</h3>
            <div className="bg-gray-50 rounded-lg p-6 text-center">
              <div className="text-4xl mb-2">⭐</div>
              <div className="text-2xl font-bold text-gray-900 mb-1">{formatRating(product.avg_rating)}</div>
              <div className="text-gray-600 mb-4">Based on {product.review_count} reviews</div>
              <p className="text-gray-500">Review system coming soon...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}



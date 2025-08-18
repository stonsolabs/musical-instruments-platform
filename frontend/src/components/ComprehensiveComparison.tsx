'use client';

import React from 'react';
import { Product } from '@/types';

interface ComprehensiveComparisonProps {
  products: Product[];
}

// Helper function to generate dynamic grid classes based on product count
const getGridClasses = (productCount: number): string => {
  if (productCount === 1) return 'grid-cols-1 max-w-2xl mx-auto';
  if (productCount === 2) return 'grid-cols-1 md:grid-cols-2';
  if (productCount === 3) return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3';
  if (productCount === 4) return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4';
  if (productCount >= 5) return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4';
  return 'grid-cols-1';
};

export default function ComprehensiveComparison({ products }: ComprehensiveComparisonProps) {
  if (products.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <p className="text-gray-500 text-center">No products to compare.</p>
      </div>
    );
  }

  const hasAIContent = products.some(product => product.ai_content);

  if (!hasAIContent) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <p className="text-gray-500 text-center">Detailed comparison information not available for these products.</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Basic Information Comparison */}
      <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Basic Information Comparison</h2>
        <div className={`grid gap-6 ${getGridClasses(products.length)}`}>
          {products.map((product) => (
            <div key={product.id} className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-3">{product.name}</h3>
              {product.ai_content ? (
                <div className="space-y-3">
                  <div>
                    <span className="text-sm font-medium text-gray-500">Overview</span>
                    <p className="text-sm text-gray-700 mt-1 line-clamp-3">
                      {product.ai_content.basic_info.overview}
                    </p>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-500">Skill Level</span>
                    <p className="text-sm text-gray-700">{product.ai_content.basic_info.target_skill_level}</p>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-500">Origin</span>
                    <p className="text-sm text-gray-700">{product.ai_content.basic_info.country_of_origin}</p>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-500">Key Features</span>
                    <ul className="text-sm text-gray-700 mt-1 space-y-1">
                      {product.ai_content.basic_info.key_features.slice(0, 3).map((feature, index) => (
                        <li key={index} className="flex items-start gap-1">
                          <span className="text-blue-600 mt-1">•</span>
                          <span>{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-gray-500">No detailed information available</p>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Technical Analysis Comparison */}
      <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Technical Analysis Comparison</h2>
        
        {/* Sound Characteristics */}
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <span className="text-2xl">🎵</span>
            Sound Characteristics
          </h3>
          <div className={`grid gap-6 ${getGridClasses(products.length)}`}>
            {products.map((product) => (
              <div key={product.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <h4 className="font-semibold text-gray-900 mb-3 text-lg">{product.name}</h4>
                {product.ai_content ? (
                  <div className="space-y-4">
                    <div>
                      <span className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Tonal Profile</span>
                      <p className="text-sm text-gray-700 mt-2 leading-relaxed">
                        {product.ai_content.technical_analysis.sound_characteristics.tonal_profile}
                      </p>
                    </div>
                    <div>
                      <span className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Output Level</span>
                      <div className="mt-2">
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {product.ai_content.technical_analysis.sound_characteristics.output_level}
                        </span>
                      </div>
                    </div>
                    <div>
                      <span className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Best Genres</span>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {product.ai_content.technical_analysis.sound_characteristics.best_genres.slice(0, 4).map((genre, index) => (
                          <span key={index} className="px-3 py-1 bg-gradient-to-r from-purple-100 to-blue-100 text-purple-800 text-xs rounded-full font-medium">
                            {genre}
                          </span>
                        ))}
                      </div>
                    </div>
                    {product.ai_content.technical_analysis.sound_characteristics.pickup_positions && (
                      <div>
                        <span className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Pickup Positions</span>
                        <div className="mt-2 space-y-1">
                          {Object.entries(product.ai_content.technical_analysis.sound_characteristics.pickup_positions as Record<string, string>).slice(0, 3).map(([position, description]) => (
                            <div key={position} className="text-xs text-gray-600">
                              <span className="font-medium">{position}:</span> {description}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">No technical data available</p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Build Quality */}
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <span className="text-2xl">🔧</span>
            Build Quality & Construction
          </h3>
          <div className={`grid gap-6 ${getGridClasses(products.length)}`}>
            {products.map((product) => (
              <div key={product.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <h4 className="font-semibold text-gray-900 mb-3 text-lg">{product.name}</h4>
                {product.ai_content ? (
                  <div className="space-y-4">
                    <div>
                      <span className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Construction Type</span>
                      <p className="text-sm text-gray-700 mt-2">
                        {product.ai_content.technical_analysis.build_quality.construction_type}
                      </p>
                    </div>
                    <div>
                      <span className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Hardware Quality</span>
                      <div className="mt-2">
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {product.ai_content.technical_analysis.build_quality.hardware_quality}
                        </span>
                      </div>
                    </div>
                    <div>
                      <span className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Durability</span>
                      <p className="text-sm text-gray-700 mt-2">
                        {product.ai_content.technical_analysis.build_quality.expected_durability}
                      </p>
                    </div>

                  </div>
                ) : (
                  <p className="text-sm text-gray-500">No build quality data available</p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Playability & Ergonomics */}
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <span className="text-2xl">🎯</span>
            Playability & Ergonomics
          </h3>
          <div className={`grid gap-6 ${getGridClasses(products.length)}`}>
            {products.map((product) => (
              <div key={product.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <h4 className="font-semibold text-gray-900 mb-3 text-lg">{product.name}</h4>
                {product.ai_content ? (
                  <div className="space-y-4">
                    <div>
                      <span className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Neck Profile</span>
                      <p className="text-sm text-gray-700 mt-2">
                        {product.ai_content.technical_analysis.playability.neck_profile}
                      </p>
                    </div>
                    <div>
                      <span className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Comfort Rating</span>
                      <div className="mt-2">
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                          {product.ai_content.technical_analysis.playability.comfort_rating}
                        </span>
                      </div>
                    </div>
                    <div>
                      <span className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Weight Category</span>
                      <p className="text-sm text-gray-700 mt-2">
                        {product.ai_content.technical_analysis.playability.weight_category}
                      </p>
                    </div>

                  </div>
                ) : (
                  <p className="text-sm text-gray-500">No playability data available</p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Technical Specifications */}
        <div>
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <span className="text-2xl">⚙️</span>
            Technical Specifications
          </h3>
          <div className={`grid gap-6 ${getGridClasses(products.length)}`}>
            {products.map((product) => (
              <div key={product.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <h4 className="font-semibold text-gray-900 mb-3 text-lg">{product.name}</h4>
                {product.specifications ? (
                  <div className="space-y-3">
                    {Object.entries(product.specifications).slice(0, 6).map(([key, value]) => (
                      <div key={key}>
                        <span className="text-sm font-semibold text-gray-700 uppercase tracking-wide">
                          {key.replace(/_/g, ' ')}
                        </span>
                        <p className="text-sm text-gray-700 mt-1">
                          {value}
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">No specifications available</p>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Purchase Decision Comparison */}
      <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Purchase Decision Guide</h2>
        
        <div className={`grid gap-6 ${getGridClasses(products.length)}`}>
          {products.map((product) => (
            <div key={product.id} className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-4">{product.name}</h3>
              {product.ai_content ? (
                <div className="space-y-4">
                  {/* Why Buy */}
                  <div>
                    <h4 className="text-sm font-semibold text-green-700 mb-2">Why Buy</h4>
                    <div className="space-y-2">
                      {product.ai_content.purchase_decision.why_buy.slice(0, 2).map((reason, index) => (
                        <div key={index} className="p-2 bg-green-50 border border-green-200 rounded text-xs">
                          <div className="font-medium text-green-800">{reason.title}</div>
                          <div className="text-green-700 mt-1">{reason.description}</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Why Not Buy */}
                  <div>
                    <h4 className="text-sm font-semibold text-red-700 mb-2">Considerations</h4>
                    <div className="space-y-2">
                      {product.ai_content.purchase_decision.why_not_buy.slice(0, 1).map((reason, index) => (
                        <div key={index} className="p-2 bg-red-50 border border-red-200 rounded text-xs">
                          <div className="font-medium text-red-800">{reason.title}</div>
                          <div className="text-red-700 mt-1">{reason.description}</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Best For */}
                  <div>
                    <h4 className="text-sm font-semibold text-blue-700 mb-2">Best For</h4>
                    <div className="space-y-2">
                      {product.ai_content.purchase_decision.best_for.slice(0, 1).map((userType, index) => (
                        <div key={index} className="p-2 bg-blue-50 border border-blue-200 rounded text-xs">
                          <div className="font-medium text-blue-800">{userType.user_type}</div>
                          <div className="text-blue-700 mt-1">{userType.reason}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-gray-500">No purchase guidance available</p>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Expert Ratings Comparison */}
      <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Expert Ratings Comparison</h2>
        
        <div className={`grid gap-6 ${getGridClasses(products.length)}`}>
          {products.map((product) => (
            <div key={product.id} className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-4">{product.name}</h3>
              {product.ai_content ? (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="text-center p-3 bg-gray-50 rounded">
                      <div className="text-lg font-bold text-blue-600">{product.ai_content.professional_assessment.expert_rating.build_quality}/10</div>
                      <div className="text-xs text-gray-600">Build Quality</div>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded">
                      <div className="text-lg font-bold text-green-600">{product.ai_content.professional_assessment.expert_rating.sound_quality}/10</div>
                      <div className="text-xs text-gray-600">Sound Quality</div>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded">
                      <div className="text-lg font-bold text-purple-600">{product.ai_content.professional_assessment.expert_rating.value_for_money}/10</div>
                      <div className="text-xs text-gray-600">Value</div>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded">
                      <div className="text-lg font-bold text-orange-600">{product.ai_content.professional_assessment.expert_rating.versatility}/10</div>
                      <div className="text-xs text-gray-600">Versatility</div>
                    </div>
                  </div>
                  
                  <div>
                    <span className="text-sm font-medium text-gray-500">Standout Features</span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {product.ai_content.professional_assessment.standout_features.slice(0, 2).map((feature, index) => (
                        <span key={index} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                          {feature}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-gray-500">No expert ratings available</p>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Usage Guidance Comparison */}
      <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Usage Guidance Comparison</h2>
        
        <div className={`grid gap-6 ${getGridClasses(products.length)}`}>
          {products.map((product) => (
            <div key={product.id} className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-4">{product.name}</h3>
              {product.ai_content ? (
                <div className="space-y-4">
                  {/* Music Styles */}
                  <div>
                    <span className="text-sm font-medium text-gray-500">Best Genres</span>
                    <div className="space-y-2 mt-2">
                      <div>
                        <span className="text-xs font-medium text-green-600">Excellent:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {product.ai_content.usage_guidance.suitable_music_styles.excellent.slice(0, 2).map((style, index) => (
                            <span key={index} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                              {style}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div>
                        <span className="text-xs font-medium text-blue-600">Good:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {product.ai_content.usage_guidance.suitable_music_styles.good.slice(0, 2).map((style, index) => (
                            <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                              {style}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Recommended Amplifiers */}
                  <div>
                    <span className="text-sm font-medium text-gray-500">Recommended Amps</span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {product.ai_content.usage_guidance.recommended_amplifiers.slice(0, 2).map((amp, index) => (
                        <span key={index} className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">
                          {amp}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Learning Curve */}
                  <div>
                    <span className="text-sm font-medium text-gray-500">Learning Curve</span>
                    <p className="text-sm text-gray-700 mt-1">{product.ai_content.usage_guidance.skill_development.learning_curve}</p>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-gray-500">No usage guidance available</p>
              )}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

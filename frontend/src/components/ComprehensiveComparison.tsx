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

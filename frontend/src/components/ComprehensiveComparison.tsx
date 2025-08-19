'use client';

import React from 'react';
import { Product } from '@/types';

interface ComprehensiveComparisonProps {
  products: Product[];
}

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
      {/* Additional Comparison Insights */}
      <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Additional Comparison Insights</h2>
        
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0">
              <svg className="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-blue-900 mb-2">Expert Analysis Available Above</h3>
              <p className="text-blue-800 text-sm">
                For detailed expert ratings, purchase guidance, and usage recommendations, 
                please refer to the sections above: "Purchase Decision Guide", "Expert Ratings Comparison", 
                and "Usage Guidance Comparison".
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Quick Comparison Summary */}
          <div className="bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-lg p-4">
            <h3 className="font-semibold text-green-900 mb-3 flex items-center gap-2">
              <span className="text-xl">📊</span>
              Quick Summary
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-green-700">Products Compared:</span>
                <span className="font-semibold text-green-900">{products.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-green-700">Categories:</span>
                <span className="font-semibold text-green-900">
                  {new Set(products.map(p => p.category.name)).size}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-green-700">Total Stores:</span>
                <span className="font-semibold text-green-900">
                  {products.reduce((sum, p) => sum + (p.prices?.length || 0), 0)}
                </span>
              </div>
            </div>
          </div>

          {/* Best Value Pick */}
          <div className="bg-gradient-to-br from-purple-50 to-indigo-50 border border-purple-200 rounded-lg p-4">
            <h3 className="font-semibold text-purple-900 mb-3 flex items-center gap-2">
              <span className="text-xl">💰</span>
              Best Value
            </h3>
            {products.length > 1 ? (
              <div className="text-sm">
                <p className="text-purple-700 mb-2">Based on expert ratings:</p>
                {(() => {
                  const bestValue = products.reduce((best, current) => {
                    const bestRating = best.ai_content?.professional_assessment.expert_rating.value_for_money || 0;
                    const currentRating = current.ai_content?.professional_assessment.expert_rating.value_for_money || 0;
                    return currentRating > bestRating ? current : best;
                  });
                  return (
                    <div className="font-semibold text-purple-900">
                      {bestValue.brand.name} {bestValue.name}
                    </div>
                  );
                })()}
              </div>
            ) : (
              <p className="text-sm text-purple-700">Add more products to see value comparison</p>
            )}
          </div>

          {/* Best Sound Quality */}
          <div className="bg-gradient-to-br from-orange-50 to-red-50 border border-orange-200 rounded-lg p-4">
            <h3 className="font-semibold text-orange-900 mb-3 flex items-center gap-2">
              <span className="text-xl">🎵</span>
              Best Sound
            </h3>
            {products.length > 1 ? (
              <div className="text-sm">
                <p className="text-orange-700 mb-2">Based on expert ratings:</p>
                {(() => {
                  const bestSound = products.reduce((best, current) => {
                    const bestRating = best.ai_content?.professional_assessment.expert_rating.sound_quality || 0;
                    const currentRating = current.ai_content?.professional_assessment.expert_rating.sound_quality || 0;
                    return currentRating > bestRating ? current : best;
                  });
                  return (
                    <div className="font-semibold text-orange-900">
                      {bestSound.brand.name} {bestSound.name}
                    </div>
                  );
                })()}
              </div>
            ) : (
              <p className="text-sm text-orange-700">Add more products to see sound comparison</p>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}

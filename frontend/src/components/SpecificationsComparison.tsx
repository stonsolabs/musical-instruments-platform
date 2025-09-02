'use client';

import React, { useState } from 'react';
import type { Product } from '@/types';

// Helper function to generate common specifications across products
const generateCommonSpecs = (products: Product[]): string[] => {
  if (products.length === 0) return [];
  
  try {
    // Get all specification keys from all products
    const allSpecs = new Set<string>();
    products.forEach(product => {
      if (product.specifications && typeof product.specifications === 'object') {
        Object.keys(product.specifications).forEach(key => allSpecs.add(key));
      }
    });
    
    // Filter to only specs that appear in at least one product
    const commonSpecs = Array.from(allSpecs).filter(spec => {
      return products.some(product => 
        product.specifications && 
        typeof product.specifications === 'object' &&
        product.specifications[spec] !== undefined && 
        product.specifications[spec] !== null &&
        product.specifications[spec] !== ''
      );
    });
    
    return commonSpecs.sort();
  } catch (error) {
    console.error('Error generating common specs:', error);
    return [];
  }
};

// Helper function to generate comparison matrix
const generateComparisonMatrix = (products: Product[]): {[spec: string]: {[productId: string]: any}} => {
  try {
    const matrix: {[spec: string]: {[productId: string]: any}} = {};
    const commonSpecs = generateCommonSpecs(products);
    
    commonSpecs.forEach(spec => {
      matrix[spec] = {};
      products.forEach(product => {
        const value = product.specifications && typeof product.specifications === 'object' ? product.specifications[spec] : undefined;
        matrix[spec][String(product.id)] = value || 'N/A';
      });
    });
    
    return matrix;
  } catch (error) {
    console.error('Error generating comparison matrix:', error);
    return {};
  }
};

interface SpecificationsComparisonProps {
  products: Product[];
  isCollapsible?: boolean;
  defaultCollapsed?: boolean;
  className?: string;
}

export default function SpecificationsComparison({ 
  products, 
  isCollapsible = false, 
  defaultCollapsed = false,
  className = ""
}: SpecificationsComparisonProps) {
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);
  
  if (products.length === 0) {
    return null;
  }

  const commonSpecs = generateCommonSpecs(products);
  const comparisonMatrix = generateComparisonMatrix(products);

  const content = (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden ${className}`}>
      <div className="p-6">
        
        {/* Technical Specifications */}
        <div className="mb-8">
          <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <span className="text-2xl">⚙️</span>
            Technical Specifications
          </h4>
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  <th className="text-left py-3 px-4 font-semibold text-gray-900 w-1/3">Specification</th>
                  {products.map((product) => (
                    <th key={product.id} className="text-left py-3 px-4 font-semibold text-gray-900">
                      <div className="flex items-center gap-2">
                        <span className="text-xl">🎸</span>
                        <div>
                          <div className="font-bold text-sm">{product.brand.name}</div>
                          <div className="text-xs font-normal text-gray-600">{product.name}</div>
                        </div>
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {/* Basic Specifications */}
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 font-medium text-gray-900">Brand</td>
                  {products.map((product) => (
                    <td key={product.id} className="py-3 px-4 text-gray-700">{product.brand.name}</td>
                  ))}
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 font-medium text-gray-900">Category</td>
                  {products.map((product) => (
                    <td key={product.id} className="py-3 px-4 text-gray-700">{product.category.name}</td>
                  ))}
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 font-medium text-gray-900">Average Rating</td>
                  {products.map((product) => (
                    <td key={product.id} className="py-3 px-4 text-gray-700">
                      <div className="flex items-center gap-2">
                        <span className="text-yellow-500">★</span>
                        <span>{product.avg_rating > 0 ? product.avg_rating.toFixed(1) : '0.0'}</span>
                        <span className="text-sm text-gray-500">({product.review_count} reviews)</span>
                      </div>
                    </td>
                  ))}
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-3 px-4 font-medium text-gray-900">Available Stores</td>
                  {products.map((product) => (
                    <td key={product.id} className="py-3 px-4 text-gray-700">
                      <span className="font-semibold text-blue-600">{product.prices?.length || 0}</span> stores
                    </td>
                  ))}
                </tr>
                
                {/* Product Specifications */}
                {commonSpecs && commonSpecs.length > 0 && commonSpecs.map((spec) => (
                  <tr key={spec} className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900 capitalize">
                      {spec.replace(/_/g, ' ')}
                    </td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {comparisonMatrix[spec]?.[product.id] || 'N/A'}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Build Quality & Construction */}
        {products.some(p => p.ai_content) && (
          <div className="mb-8">
            <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <span className="text-2xl">🔧</span>
              Build Quality & Construction
            </h4>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b border-gray-200 bg-gray-50">
                    <th className="text-left py-3 px-4 font-semibold text-gray-900 w-1/3">Aspect</th>
                    {products.map((product) => (
                      <th key={product.id} className="text-left py-3 px-4 font-semibold text-gray-900">
                        <div className="flex items-center gap-2">
                          <span className="text-xl">🎸</span>
                          <div>
                            <div className="font-bold text-sm">{product.brand.name}</div>
                            <div className="text-xs font-normal text-gray-600">{product.name}</div>
                          </div>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Construction Type</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.technical_analysis.build_quality.construction_type || 'N/A'}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Hardware Quality</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.technical_analysis.build_quality.hardware_quality ? (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            {product.ai_content?.technical_analysis?.build_quality?.hardware_quality}
                          </span>
                        ) : 'N/A'}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Finish Quality</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.technical_analysis.build_quality.finish_quality || 'N/A'}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Expected Durability</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.technical_analysis.build_quality.expected_durability || 'N/A'}
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Playability & Ergonomics */}
        {products.some(p => p.ai_content) && (
          <div className="mb-8">
            <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <span className="text-2xl">🎯</span>
              Playability & Ergonomics
            </h4>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b border-gray-200 bg-gray-50">
                    <th className="text-left py-3 px-4 font-semibold text-gray-900 w-1/3">Aspect</th>
                    {products.map((product) => (
                      <th key={product.id} className="text-left py-3 px-4 font-semibold text-gray-900">
                        <div className="flex items-center gap-2">
                          <span className="text-xl">🎸</span>
                          <div>
                            <div className="font-bold text-sm">{product.brand.name}</div>
                            <div className="text-xs font-normal text-gray-600">{product.name}</div>
                          </div>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Neck Profile</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.technical_analysis.playability.neck_profile || 'N/A'}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Action Setup</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.technical_analysis.playability.action_setup || 'N/A'}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Comfort Rating</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.technical_analysis.playability.comfort_rating ? (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                            {product.ai_content?.technical_analysis?.playability?.comfort_rating}
                          </span>
                        ) : 'N/A'}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Weight Category</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.technical_analysis.playability.weight_category || 'N/A'}
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Sound Characteristics */}
        {products.some(p => p.ai_content) && (
          <div className="mb-8">
            <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <span className="text-2xl">🎵</span>
              Sound Characteristics
            </h4>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b border-gray-200 bg-gray-50">
                    <th className="text-left py-3 px-4 font-semibold text-gray-900 w-1/3">Aspect</th>
                    {products.map((product) => (
                      <th key={product.id} className="text-left py-3 px-4 font-semibold text-gray-900">
                        <div className="flex items-center gap-2">
                          <span className="text-xl">🎸</span>
                          <div>
                            <div className="font-bold text-sm">{product.brand.name}</div>
                            <div className="text-xs font-normal text-gray-600">{product.name}</div>
                          </div>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Tonal Profile</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        <div className="text-sm leading-relaxed">
                          {product.ai_content?.technical_analysis.sound_characteristics.tonal_profile || 'N/A'}
                        </div>
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Output Level</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.technical_analysis.sound_characteristics.output_level ? (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            {product.ai_content?.technical_analysis?.sound_characteristics?.output_level}
                          </span>
                        ) : 'N/A'}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Best Genres</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.technical_analysis.sound_characteristics.best_genres ? (
                          <div className="flex flex-wrap gap-1">
                            {(product.ai_content?.technical_analysis?.sound_characteristics?.best_genres || []).slice(0, 3).map((genre, index) => (
                              <span key={index} className="px-2 py-1 bg-gradient-to-r from-purple-100 to-blue-100 text-purple-800 text-xs rounded-full font-medium">
                                {genre}
                              </span>
                            ))}
                          </div>
                        ) : 'N/A'}
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Basic Information */}
        {products.some(p => p.ai_content) && (
          <div>
            <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <span className="text-2xl">ℹ️</span>
              Basic Information
            </h4>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b border-gray-200 bg-gray-50">
                    <th className="text-left py-3 px-4 font-semibold text-gray-900 w-1/3">Information</th>
                    {products.map((product) => (
                      <th key={product.id} className="text-left py-3 px-4 font-semibold text-gray-900">
                        <div className="flex items-center gap-2">
                          <span className="text-xl">🎸</span>
                          <div>
                            <div className="font-bold text-sm">{product.brand.name}</div>
                            <div className="text-xs font-normal text-gray-600">{product.name}</div>
                          </div>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Overview</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        <div className="text-sm leading-relaxed line-clamp-3">
                          {product.ai_content?.basic_info.overview || 'N/A'}
                        </div>
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Target Skill Level</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.basic_info.target_skill_level || 'N/A'}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Country of Origin</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.basic_info.country_of_origin || 'N/A'}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Release Year</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.basic_info.release_year || 'N/A'}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">Key Features</td>
                    {products.map((product) => (
                      <td key={product.id} className="py-3 px-4 text-gray-700">
                        {product.ai_content?.basic_info.key_features ? (
                          <ul className="text-sm space-y-1">
                            {(product.ai_content?.basic_info?.key_features || []).slice(0, 3).map((feature, index) => (
                              <li key={index} className="flex items-start gap-1">
                                <span className="text-blue-600 mt-1">•</span>
                                <span>{feature}</span>
                              </li>
                            ))}
                          </ul>
                        ) : 'N/A'}
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  if (isCollapsible) {
    return (
      <div className={className}>
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="w-full bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-left hover:bg-gray-50 transition-colors"
        >
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-semibold text-gray-900">Specifications Comparison</h3>
            <svg
              className={`w-6 h-6 text-gray-500 transition-transform ${isCollapsed ? 'rotate-180' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </button>
        {!isCollapsed && (
          <div className="mt-4">
            {content}
          </div>
        )}
      </div>
    );
  }

  return content;
}

'use client';

import React, { useState } from 'react';
import { Product, ComprehensiveAIContent } from '@/types';

interface ProductOverviewProps {
  product: Product;
}

export default function ProductOverview({ product }: ProductOverviewProps) {
  const [isOpen, setIsOpen] = useState(true);
  const aiContent = product.ai_content;

  if (!aiContent) {
    return null;
  }

  return (
    <section className="bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden mb-8">
      <div className="p-8">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between text-left mb-6 group"
        >
          <h2 className="text-2xl font-bold text-primary-900 group-hover:text-primary-700 transition-colors">
            Overview
          </h2>
          <span className="text-primary-600 text-2xl transition-transform duration-200 group-hover:text-primary-700">
            {isOpen ? '−' : '+'}
          </span>
        </button>
        
        {isOpen && (
          <div className="space-y-4">
            <p className="text-primary-700 leading-relaxed">{aiContent.basic_info.overview}</p>
            
            <div>
              <h3 className="text-lg font-semibold text-primary-900 mb-2">Key Features</h3>
              <ul className="list-disc list-inside space-y-1 text-primary-700">
                {aiContent.basic_info.key_features.map((feature, index) => (
                  <li key={index}>{feature}</li>
                ))}
              </ul>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <span className="text-sm font-medium text-primary-500">Skill Level</span>
                <p className="text-primary-900">{aiContent.basic_info.target_skill_level}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-primary-500">Origin</span>
                <p className="text-primary-900">{aiContent.basic_info.country_of_origin}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-primary-500">Release Year</span>
                <p className="text-primary-900">{aiContent.basic_info.release_year}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

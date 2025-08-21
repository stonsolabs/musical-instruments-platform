'use client';

import React, { useState } from 'react';
import { Product } from '@/types';

interface TechnicalSpecificationsProps {
  product: Product;
}

export default function TechnicalSpecifications({ product }: TechnicalSpecificationsProps) {
  const [isOpen, setIsOpen] = useState(true);
  const specifications = product.specifications;

  if (!specifications || Object.keys(specifications).length === 0) {
    return null;
  }

  // Helper function to format specification values
  const formatSpecValue = (value: any): string => {
    if (typeof value === 'string') {
      return value;
    }
    if (typeof value === 'number') {
      return value.toString();
    }
    if (Array.isArray(value)) {
      return value.join(', ');
    }
    if (typeof value === 'object' && value !== null) {
      return Object.entries(value)
        .map(([key, val]) => `${key}: ${val}`)
        .join(', ');
    }
    return String(value);
  };

  // Helper function to format specification keys for display
  const formatSpecKey = (key: string): string => {
    return key
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (char) => char.toUpperCase())
      .replace(/\b(Id|Url|Sku|Msrp)\b/gi, (match) => match.toUpperCase());
  };

  // Group specifications by category for better organization
  const groupedSpecs = Object.entries(specifications).reduce((acc, [key, value]) => {
    const formattedKey = formatSpecKey(key);
    const formattedValue = formatSpecValue(value);
    
    // Determine category based on key
    let category = 'General';
    if (key.toLowerCase().includes('body') || key.toLowerCase().includes('top') || key.toLowerCase().includes('back') || key.toLowerCase().includes('side')) {
      category = 'Body & Construction';
    } else if (key.toLowerCase().includes('neck') || key.toLowerCase().includes('fingerboard') || key.toLowerCase().includes('fret')) {
      category = 'Neck & Fingerboard';
    } else if (key.toLowerCase().includes('pickup') || key.toLowerCase().includes('electronics') || key.toLowerCase().includes('control')) {
      category = 'Electronics';
    } else if (key.toLowerCase().includes('bridge') || key.toLowerCase().includes('tun') || key.toLowerCase().includes('hardware')) {
      category = 'Hardware';
    } else if (key.toLowerCase().includes('finish') || key.toLowerCase().includes('color') || key.toLowerCase().includes('material')) {
      category = 'Finish & Materials';
    } else if (key.toLowerCase().includes('dimension') || key.toLowerCase().includes('weight') || key.toLowerCase().includes('scale') || key.toLowerCase().includes('length')) {
      category = 'Dimensions & Weight';
    }
    
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push({ key: formattedKey, value: formattedValue });
    return acc;
  }, {} as Record<string, Array<{ key: string; value: string }>>);

  return (
    <section className="bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden mb-8">
      <div className="p-8">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between text-left mb-6 group"
        >
          <h2 className="text-2xl font-bold text-primary-900 group-hover:text-primary-700 transition-colors">
            Technical Specifications
          </h2>
          <span className="text-primary-600 text-2xl transition-transform duration-200 group-hover:text-primary-700">
            {isOpen ? '−' : '+'}
          </span>
        </button>
        
        {isOpen && (
          <div className="space-y-6">
            {Object.entries(groupedSpecs).map(([category, specs]) => (
              <div key={category}>
                <h3 className="text-lg font-semibold text-primary-900 mb-3 border-b border-primary-200 pb-2">
                  {category}
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {specs.map((spec, index) => (
                    <div key={index} className="flex flex-col">
                      <span className="text-sm font-medium text-primary-600 mb-1">
                        {spec.key}
                      </span>
                      <span className="text-primary-900">
                        {spec.value}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

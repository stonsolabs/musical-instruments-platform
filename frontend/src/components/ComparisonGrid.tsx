import React from 'react';
import { ProductComparison } from '../types';
import { getProductImageUrl, formatPrice, getRatingStars } from '../lib/utils';
import { StarIcon } from '@heroicons/react/20/solid';
import { StarIcon as StarOutlineIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';

interface ComparisonGridProps {
  comparison: ProductComparison;
}

export default function ComparisonGrid({ comparison }: ComparisonGridProps) {
  const { products, common_specs, comparison_matrix } = comparison;

  if (products.length === 0) return null;

  // Get all specifications from all products (not just common ones)
  const allSpecs = new Set<string>();
  products.forEach(product => {
    if (product.specifications) {
      Object.keys(product.specifications).forEach(spec => allSpecs.add(spec));
    }
  });
  
  // Also add specs from comparison_matrix
  if (comparison_matrix) {
    Object.keys(comparison_matrix).forEach(spec => allSpecs.add(spec));
  }
  
  const sortedSpecs = Array.from(allSpecs).sort();

  return (
    <>
      {/* Desktop Table View */}
      <div className="hidden lg:block overflow-x-auto">
        <table className="w-full divide-y divide-gray-200 table-fixed">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-1/4">
              Specification
            </th>
            {products.map((product) => (
              <th key={product.id} className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider" style={{width: `${75 / products.length}%`}}>
                <div className="flex flex-col items-center space-y-2">
                  <div className="w-16 h-16 bg-gray-100 rounded-lg overflow-hidden">
                    <img
                      src={getProductImageUrl(product)}
                      alt={product.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.style.display = 'none';
                      }}
                    />
                  </div>
                  <div className="text-center">
                    <Link href={`/products/${product.slug}`} className="hover:text-brand-primary">
                      <div className="font-semibold text-gray-900 text-sm leading-tight">
                        {product.name}
                      </div>
                    </Link>
                    <div className="text-xs text-gray-500">{product.brand.name}</div>
                  </div>
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {sortedSpecs.map((spec) => {
            // Check if this row has any values
            const hasValues = products.some(product => {
              const value = product.specifications?.[spec] || comparison_matrix?.[spec]?.[product.id];
              return value && value !== 'N/A' && value !== '';
            });
            
            if (!hasValues) return null;
            
            return (
              <tr key={spec} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-sm font-medium text-gray-900 capitalize bg-gray-50 break-words">
                  {spec.replace(/_/g, ' ')}
                </td>
                {products.map((product) => {
                  const value = product.specifications?.[spec] || comparison_matrix?.[spec]?.[product.id];
                  
                  const formatValue = (val: any) => {
                    if (!val || val === 'N/A' || val === '') return 'N/A';
                    
                    // Handle arrays (lists)
                    if (Array.isArray(val)) {
                      return (
                        <ul className="text-left space-y-1">
                          {val.map((item, idx) => (
                            <li key={idx} className="break-words">• {String(item)}</li>
                          ))}
                        </ul>
                      );
                    }
                    
                    // Handle objects
                    if (typeof val === 'object' && val !== null) {
                      return JSON.stringify(val);
                    }
                    
                    // Handle long strings (split by common delimiters)
                    const strVal = String(val);
                    if (strVal.length > 50 && (strVal.includes(',') || strVal.includes(';') || strVal.includes('|'))) {
                      const delimiter = strVal.includes(',') ? ',' : strVal.includes(';') ? ';' : '|';
                      const items = strVal.split(delimiter).map(item => item.trim()).filter(Boolean);
                      return (
                        <ul className="text-left space-y-1">
                          {items.map((item, idx) => (
                            <li key={idx} className="break-words">• {item}</li>
                          ))}
                        </ul>
                      );
                    }
                    
                    return <span className="break-words">{strVal}</span>;
                  };
                  
                  const displayValue = formatValue(value);
                  const isNA = !value || value === 'N/A' || value === '';
                  
                  return (
                    <td key={`${product.id}-${spec}`} className="px-4 py-4 text-sm text-gray-900 text-center max-w-xs">
                      <div className={isNA ? 'text-gray-400 italic' : 'font-medium'}>
                        {displayValue}
                      </div>
                    </td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
        </table>
        
        {sortedSpecs.filter(spec => {
          const hasValues = products.some(product => {
            const value = product.specifications?.[spec] || comparison_matrix?.[spec]?.[product.id];
            return value && value !== 'N/A' && value !== '';
          });
          return hasValues;
        }).length === 0 && (
          <div className="text-center py-12">
            <div className="text-4xl mb-4 opacity-20">📊</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Specifications Available</h3>
            <p className="text-sm text-gray-500">
              Specifications for these products are being prepared or are not available in a comparable format.
            </p>
          </div>
        )}
      </div>

      {/* Mobile Card View */}
      <div className="lg:hidden space-y-6">
        {products.map((product, productIndex) => (
          <div key={product.id} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            {/* Product Header */}
            <div className="bg-gray-50 p-4 border-b border-gray-200">
              <div className="flex items-center space-y-2">
                <div className="w-16 h-16 bg-gray-100 rounded-lg overflow-hidden">
                  <img
                    src={getProductImageUrl(product)}
                    alt={product.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.display = 'none';
                    }}
                  />
                </div>
                <div className="ml-4">
                  <Link href={`/products/${product.slug}`} className="hover:text-brand-primary">
                    <h3 className="font-semibold text-gray-900 text-lg leading-tight">
                      {product.name}
                    </h3>
                  </Link>
                  <p className="text-sm text-gray-500">{product.brand.name}</p>
                </div>
              </div>
            </div>
            
            {/* Specifications */}
            <div className="p-4">
              <div className="space-y-3">
                {sortedSpecs.filter(spec => {
                  const value = product.specifications?.[spec] || comparison_matrix?.[spec]?.[product.id];
                  return value && value !== 'N/A' && value !== '';
                }).map((spec) => {
                  const value = product.specifications?.[spec] || comparison_matrix?.[spec]?.[product.id];
                  
                  const formatValue = (val: any) => {
                    if (!val || val === 'N/A' || val === '') return 'N/A';
                    
                    // Handle arrays (lists)
                    if (Array.isArray(val)) {
                      return (
                        <ul className="space-y-1 mt-1">
                          {val.map((item, idx) => (
                            <li key={idx} className="break-words">• {String(item)}</li>
                          ))}
                        </ul>
                      );
                    }
                    
                    // Handle objects
                    if (typeof val === 'object' && val !== null) {
                      return JSON.stringify(val);
                    }
                    
                    // Handle long strings (split by common delimiters)
                    const strVal = String(val);
                    if (strVal.length > 50 && (strVal.includes(',') || strVal.includes(';') || strVal.includes('|'))) {
                      const delimiter = strVal.includes(',') ? ',' : strVal.includes(';') ? ';' : '|';
                      const items = strVal.split(delimiter).map(item => item.trim()).filter(Boolean);
                      return (
                        <ul className="space-y-1 mt-1">
                          {items.map((item, idx) => (
                            <li key={idx} className="break-words">• {item}</li>
                          ))}
                        </ul>
                      );
                    }
                    
                    return <span className="break-words">{strVal}</span>;
                  };
                  
                  const displayValue = formatValue(value);
                  
                  return (
                    <div key={spec} className="border-b border-gray-100 pb-2 last:border-b-0">
                      <div className="flex flex-col space-y-1">
                        <span className="text-sm font-medium text-gray-700 capitalize">
                          {spec.replace(/_/g, ' ')}
                        </span>
                        <div className="text-sm text-gray-900">
                          {displayValue}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

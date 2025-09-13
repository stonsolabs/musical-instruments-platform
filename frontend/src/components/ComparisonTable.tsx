import React, { useMemo } from 'react';
import { ProductComparison } from '../types';
import { getProductImageUrl, getRatingStars } from '../lib/utils';
import { StarIcon } from '@heroicons/react/20/solid';
import { StarIcon as StarOutlineIcon } from '@heroicons/react/24/outline';

interface ComparisonTableProps {
  comparison: ProductComparison;
}

export default function ComparisonTable({ comparison }: ComparisonTableProps) {
  const { products, common_specs, comparison_matrix } = comparison;

  if (products.length === 0) return null;

  // Build full spec set (union across products and matrix), with common first
  const { groupedCommon, groupedOthers } = useMemo(() => {
    const all = new Set<string>();
    Object.keys(comparison_matrix || {}).forEach(k => all.add(k));
    for (const p of products) {
      const specObj = (p as any).content?.specifications || (p as any).specifications || {};
      Object.keys(specObj).forEach(k => all.add(k));
    }
    const commons = new Set<string>(common_specs || []);
    const others = Array.from(all).filter(k => !commons.has(k)).sort();

    const groupBy = (keys: string[]) => {
      const groups: Record<string, string[]> = {};
      for (const spec of keys) {
        const cat = spec.includes('_') ? spec.split('_')[0] : 'general';
        if (!groups[cat]) groups[cat] = [];
        groups[cat].push(spec);
      }
      // Stable order inside groups
      Object.values(groups).forEach(arr => arr.sort());
      return groups;
    };

    return {
      groupedCommon: groupBy(Array.from(commons)),
      groupedOthers: groupBy(others),
    };
  }, [products, common_specs, comparison_matrix]);

  const hasDiff = (spec: string) => {
    const values = products.map((p) => 
      (p as any).specifications?.[spec] ?? 
      comparison_matrix[spec]?.[String(p.id)] ?? 
      (p as any).content?.specifications?.[spec] ?? 
      (p as any)[spec]
    );
    const norm = (v: any) => String(v ?? '').toLowerCase();
    const first = norm(values[0]);
    return values.some((v) => norm(v) !== first);
  };

  return (
    <div className="space-y-6">
      {/* Product Overview Comparison */}
      {/* <div className="card p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">🏆 Product Comparison Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <div key={product.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-start space-x-4">
                <div className="w-16 h-16 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                  <img
                    src={getProductImageUrl(product)}
                    alt={product.name}
                    className="w-full h-full object-cover"
                    loading="lazy"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.display = 'none';
                    }}
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-gray-900 text-sm leading-tight mb-1 truncate">
                    {product.name}
                  </h3>
                  <p className="text-xs text-gray-500 mb-2">{product.brand.name}</p>
                  <div className="text-xs text-gray-600">
                    <div><strong>Category:</strong> {product.category.name}</div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div> */}

      {/* Specifications Comparison Table */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">📊 Detailed Specifications</h2>
        </div>
        <div className="overflow-x-auto -mx-3 px-3 sm:-mx-6 sm:px-6">
          <table className="w-full table-fixed text-sm min-w-[560px] sm:min-w-[600px]">
            <thead>
              <tr className="bg-gray-50">
                <th className="p-3 text-left font-semibold text-gray-900 border-b border-gray-200 sticky left-0 bg-gray-50 z-10">
                  Specification
                </th>
                {products.map((product) => (
                  <th key={product.id} className="p-3 text-center font-semibold text-gray-900 border-b border-gray-200 min-w-[200px]">
                    <div className="text-center">
                      <div className="font-semibold text-gray-900 text-sm leading-tight truncate">
                        {product.name}
                      </div>
                      <div className="text-xs text-gray-500">{product.brand.name}</div>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
        
            <tbody className="divide-y divide-gray-100">
              {/* Community Votes */}
              <tr className="bg-gray-25">
                <td className="p-3 font-semibold text-gray-900 bg-gray-50 sticky left-0 z-10">🌟 Community Votes</td>
                {products.map((product) => {
                  return (
                    <td key={product.id} className="p-3 text-center">
                      {product.vote_stats ? (
                        <div className="space-y-2">
                          <div className="flex items-center justify-center space-x-2">
                            <span className="text-sm">🤘</span>
                            <span className="text-sm font-bold text-green-600">{product.vote_stats.thumbs_up_count}</span>
                          </div>
                          <div className="flex items-center justify-center space-x-2">
                            <span className="text-sm">👎</span>
                            <span className="text-sm font-bold text-red-600">{product.vote_stats.thumbs_down_count}</span>
                          </div>
                        </div>
                      ) : (
                        <div className="text-sm text-gray-500">No votes yet</div>
                      )}
                    </td>
                  );
                })}
              </tr>

              {/* Common Specifications Header */}
              {Object.keys(groupedCommon).length > 0 && (
                <tr className="bg-gray-100">
                  <td className="p-3 font-semibold text-gray-900 sticky left-0 z-10">🔍 Key Specifications</td>
                  {products.map(p => (
                    <td key={`cm-h-${p.id}`} className="p-3"></td>
                  ))}
                </tr>
              )}
          {Object.entries(groupedCommon).map(([cat, specs]) => (
            <>
              <tr key={`hdr-${cat}`} className="bg-gray-50">
                <td className="p-3 font-semibold text-gray-900 capitalize sticky left-0 z-10">{cat.replace(/_/g, ' ')}</td>
                {products.map(p => (
                  <td key={`sp-${cat}-${p.id}`} className="p-3"></td>
                ))}
              </tr>
              {specs.map((spec) => (
                <tr key={spec} className="hover:bg-gray-50">
                  <td className="p-3 font-medium text-gray-900 capitalize sticky left-0 bg-white z-10">
                    {spec.replace(/_/g, ' ')}
                  </td>
                  {products.map((product) => {
                    const rawValue = (product as any).specifications?.[spec] ?? 
                                     comparison_matrix[spec]?.[String(product.id)] ?? 
                                     (product as any).content?.specifications?.[spec] ?? 
                                     'N/A';
                    
                    // Format arrays and complex objects properly
                    const formatValue = (val: any): string => {
                      if (val === null || val === undefined || val === '') return 'N/A';
                      
                      // Handle arrays by creating a readable list
                      if (Array.isArray(val)) {
                        if (val.length === 0) return 'None';
                        if (val.length === 1) return String(val[0]);
                        return val.join(', ');
                      }
                      
                      // Handle objects (but not arrays, which are also objects)
                      if (typeof val === 'object' && val !== null) {
                        // If it's a simple key-value object, format it nicely
                        if (Object.keys(val).length <= 3) {
                          return Object.entries(val)
                            .map(([k, v]) => `${k}: ${v}`)
                            .join(', ');
                        }
                        // For complex objects, fall back to JSON
                        return JSON.stringify(val);
                      }
                      
                      return String(val);
                    };
                    
                    const value = formatValue(rawValue);
                    const diff = hasDiff(spec);
                    return (
                      <td key={`${product.id}-${spec}`} className={`p-3 text-center ${diff ? 'text-gray-900 font-medium' : 'text-gray-600'} border-l border-gray-100`}>
                        <span>{value}</span>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </>
          ))}

              {/* Other Specifications Header */}
              {Object.keys(groupedOthers).length > 0 && (
                <tr className="bg-gray-100">
                  <td className="p-3 font-semibold text-gray-900 sticky left-0 z-10">⚙️ Additional Details</td>
                  {products.map(p => (
                    <td key={`ot-h-${p.id}`} className="p-3"></td>
                  ))}
                </tr>
              )}
          {Object.entries(groupedOthers).map(([cat, specs]) => (
            <>
              <tr key={`oth-hdr-${cat}`} className="bg-gray-50">
                <td className="p-3 font-semibold text-gray-900 capitalize sticky left-0 z-10">{cat.replace(/_/g, ' ')}</td>
                {products.map(p => (
                  <td key={`oth-sp-${cat}-${p.id}`} className="p-3"></td>
                ))}
              </tr>
              {specs.map((spec) => (
                <tr key={`oth-${spec}`} className="hover:bg-gray-50">
                  <td className="p-3 font-medium text-gray-900 capitalize sticky left-0 bg-white z-10">
                    {spec.replace(/_/g, ' ')}
                  </td>
                  {products.map((product) => {
                    const rawValue = (product as any).specifications?.[spec] ?? 
                                     comparison_matrix[spec]?.[String(product.id)] ?? 
                                     (product as any).content?.specifications?.[spec] ?? 
                                     'N/A';
                    
                    // Format arrays and complex objects properly
                    const formatValue = (val: any): string => {
                      if (val === null || val === undefined || val === '') return 'N/A';
                      
                      // Handle arrays by creating a readable list
                      if (Array.isArray(val)) {
                        if (val.length === 0) return 'None';
                        if (val.length === 1) return String(val[0]);
                        return val.join(', ');
                      }
                      
                      // Handle objects (but not arrays, which are also objects)
                      if (typeof val === 'object' && val !== null) {
                        // If it's a simple key-value object, format it nicely
                        if (Object.keys(val).length <= 3) {
                          return Object.entries(val)
                            .map(([k, v]) => `${k}: ${v}`)
                            .join(', ');
                        }
                        // For complex objects, fall back to JSON
                        return JSON.stringify(val);
                      }
                      
                      return String(val);
                    };
                    
                    const value = formatValue(rawValue);
                    const diff = hasDiff(spec);
                    return (
                      <td key={`oth-${product.id}-${spec}`} className={`p-3 text-center ${diff ? 'text-gray-900 font-medium' : 'text-gray-600'} border-l border-gray-100`}>
                        <div className="inline-flex items-center gap-2 justify-center">
                          {diff && <span className="inline-block w-2 h-2 rounded-full bg-blue-500" title="Different from other products" aria-hidden />}
                          <span>{value}</span>
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </>
          ))}

            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

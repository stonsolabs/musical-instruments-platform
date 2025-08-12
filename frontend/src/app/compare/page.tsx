'use client';

import React, { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { apiClient } from '@/lib/api';
import type { ComparisonResponse, Product } from '@/types';
import { formatPrice, formatRating } from '@/lib/utils';

export default function ComparePage() {
  const searchParams = useSearchParams();
  const [data, setData] = useState<ComparisonResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const ids = useMemo(() => {
    const q = searchParams.get('ids');
    if (!q) return [] as number[];
    return q.split(',').map((s) => Number(s)).filter((n) => Number.isFinite(n));
  }, [searchParams]);

  useEffect(() => {
    const run = async () => {
      if (ids.length < 2) {
        setLoading(false);
        return;
      }
      try {
        const res = await apiClient.compareProducts(ids);
        setData(res);
      } catch (e) {
        setError('Failed to load comparison');
      } finally {
        setLoading(false);
      }
    };
    run();
  }, [ids]);

  const bestPrice = (p: Product) => p.best_price ? formatPrice(p.best_price.price, p.best_price.currency) : (p.msrp_price ? formatPrice(p.msrp_price) : '—');

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Compare Products</h1>
        {ids.length < 2 && <div className="text-gray-700">Select at least two products (?ids=1,2)</div>}
        {loading && <div>Loading...</div>}
        {error && <div className="text-red-600">{error}</div>}
        {!loading && !error && data && (
          <div className="space-y-6">
            {/* Header cards side-by-side */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {data.products.map((p) => (
                <div key={p.id} className="bg-white rounded-lg shadow p-4">
                  <div className="aspect-square bg-gray-100 rounded mb-3" />
                  <div className="text-sm text-gray-600">{p.brand.name}</div>
                  <div className="font-semibold text-gray-900 line-clamp-2">{p.name}</div>
                  <div className="mt-2 flex items-center gap-2">
                    {p.avg_rating > 0 && <span className="text-sm text-yellow-700">★ {formatRating(p.avg_rating)}</span>}
                    <span className="text-sm text-gray-500">({p.review_count})</span>
                  </div>
                  <div className="mt-2 text-green-700 font-semibold">{bestPrice(p)}</div>
                  <a href={`/products/${p.slug}-${p.id}`} className="text-blue-600 text-sm hover:text-blue-800 mt-2 inline-block">View details</a>
                </div>
              ))}
            </div>

            {/* Specs comparison matrix */}
            <div className="overflow-x-auto bg-white rounded-lg shadow">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b bg-gray-50">
                    <th className="p-3 text-left w-56">Specification</th>
                    {data.products.map((p) => (
                      <th key={p.id} className="p-3 text-left min-w-[220px]">{p.name}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.common_specs.map((spec) => (
                    <tr key={spec} className="border-b hover:bg-gray-50">
                      <td className="p-3 font-medium capitalize">{spec.replace(/_/g, ' ')}</td>
                      {data.products.map((p) => (
                        <td key={p.id} className="p-3">{String(data.comparison_matrix[spec]?.[String(p.id)] ?? 'N/A')}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* AI summaries if present */}
            {data.products.some((p) => p.ai_content?.summary) && (
              <div className="bg-white rounded-lg shadow p-4">
                <h2 className="font-semibold text-lg mb-3">AI Analysis</h2>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {data.products.map((p) => (
                    p.ai_content?.summary ? (
                      <div key={p.id} className="border rounded p-3">
                        <div className="font-medium mb-1">{p.name}</div>
                        <p className="text-sm text-gray-700">{p.ai_content.summary}</p>
                      </div>
                    ) : null
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}



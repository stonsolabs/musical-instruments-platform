'use client';

import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { apiClient } from '@/lib/api';
import { Product, SearchResponse } from '@/types';

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [pagination, setPagination] = useState<SearchResponse['pagination']>({ page: 1, limit: 20, total: 0, pages: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.searchProducts({ page: 1, limit: 20, sort_by: 'name' });
      setProducts(data.products);
      setPagination(data.pagination);
    } catch (e) {
      setError('Failed to load products.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadProducts(); }, [loadProducts]);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Musical Instruments</h1>
        {loading && <div>Loading...</div>}
        {error && <div className="text-red-600">{error}</div>}
        {!loading && !error && (
          products.length ? (
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {products.map(p => (
                <a key={p.id} href={`/products/${p.slug}-${p.id}`} className="bg-white rounded-lg shadow p-4 hover:shadow-md transition">
                  <div className="aspect-square bg-gray-100 rounded mb-3" />
                  <p className="text-sm text-gray-600">{p.brand.name}</p>
                  <h3 className="font-semibold text-gray-900 line-clamp-2">{p.name}</h3>
                  {p.best_price ? (
                    <div className="mt-2 text-green-700 font-semibold">€{p.best_price.price.toFixed(2)} {p.best_price.currency}</div>
                  ) : (
                    p.msrp_price && <div className="mt-2 text-gray-900 font-semibold">€{p.msrp_price.toFixed(2)}</div>
                  )}
                </a>
              ))}
            </div>
          ) : (
            <div>No products found.</div>
          )
        )}
      </div>
    </div>
  );
}



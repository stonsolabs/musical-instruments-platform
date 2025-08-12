'use client';

import React, { useEffect, useMemo, useState } from 'react';
import { useParams } from 'next/navigation';
import { apiClient } from '@/lib/api';
import type { Product } from '@/types';

export default function ProductDetailPage() {
  const params = useParams();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedImage, setSelectedImage] = useState(0);

  const productId = useMemo(() => {
    const slug = (params?.slug as string) || '';
    const idPart = slug.split('-').pop();
    const idNum = Number(idPart);
    return Number.isFinite(idNum) ? idNum : null;
  }, [params?.slug]);

  useEffect(() => {
    const load = async () => {
      if (!productId) {
        setError('Invalid product ID');
        setLoading(false);
        return;
      }
      try {
        const data = await apiClient.getProduct(productId);
        setProduct(data);
      } catch (e) {
        setError('Product not found');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [productId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto" />
          <p className="mt-4 text-gray-600">Loading product...</p>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Product Not Found</h1>
          <a href="/products" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">Browse All Products</a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="flex items-center space-x-2 text-sm text-gray-600 mb-6">
          <a href="/" className="hover:text-blue-600">Home</a>
          <span>/</span>
          <a href="/products" className="hover:text-blue-600">Products</a>
          <span>/</span>
          <a href={`/products?category=${product.category.slug}`} className="hover:text-blue-600">{product.category.name}</a>
          <span>/</span>
          <span className="text-gray-900">{product.name}</span>
        </nav>

        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="grid lg:grid-cols-2 gap-8 p-8">
            {/* Images */}
            <div>
              <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden mb-3" />
              {product.images?.length > 0 && (
                <div className="flex items-center gap-2 overflow-x-auto">
                  {product.images.map((img, idx) => (
                    <button key={idx} onClick={() => setSelectedImage(idx)} className={`w-16 h-16 rounded border ${idx === selectedImage ? 'border-blue-600' : 'border-gray-200'}`}>
                      {/* Placeholder thumbnails - replace with <Image /> when images are real */}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Info */}
            <div>
              <div className="mb-3">
                <a href={`/products?brand=${product.brand.slug}`} className="text-blue-600 hover:text-blue-800 font-medium">{product.brand.name}</a>
                <h1 className="text-3xl font-bold text-gray-900 mt-1">{product.name}</h1>
              </div>

              {/* AI Summary */}
              {product.ai_content?.summary && (
                <div className="bg-blue-50 p-4 rounded-lg mb-4">
                  <h3 className="font-semibold text-blue-900 mb-2">AI Summary</h3>
                  <p className="text-blue-800">{product.ai_content.summary}</p>
                </div>
              )}

              {/* Prices */}
              {product.prices?.length ? (
                <div className="space-y-3 mb-6">
                  <h3 className="text-lg font-semibold">Where to buy</h3>
                  {product.prices.map((price, i) => (
                    <div key={i} className="flex items-center justify-between p-3 border rounded">
                      <div>
                        <div className="font-medium">{price.store.name}</div>
                        <div className="text-sm text-gray-600">Last checked: {new Date(price.last_checked).toLocaleDateString()}</div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-2xl font-bold text-green-600">€{price.price.toFixed(2)}</div>
                        <a href={price.affiliate_url} target="_blank" rel="noopener noreferrer" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Buy</a>
                      </div>
                    </div>
                  ))}
                </div>
              ) : null}

              {/* Specs */}
              {product.specifications && Object.keys(product.specifications).length > 0 && (
                <div className="mt-4">
                  <h3 className="text-lg font-semibold mb-2">Specifications</h3>
                  <div className="grid md:grid-cols-2 gap-2">
                    {Object.entries(product.specifications).map(([k, v]) => (
                      <div key={k} className="flex justify-between py-2 border-b">
                        <span className="font-medium text-gray-700">{k.replace(/_/g, ' ')}</span>
                        <span className="text-gray-900">{String(v)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}



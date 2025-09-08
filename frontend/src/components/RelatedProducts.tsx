import React, { useEffect, useState } from 'react';
import { Product } from '../types';
import { fetchProducts } from '../lib/api';
import ProductCard from './ProductCard';

interface RelatedProductsProps {
  categorySlug: string;
  brandSlug: string;
  currentProductId: number;
}

export default function RelatedProducts({ categorySlug, brandSlug, currentProductId }: RelatedProductsProps) {
  const [relatedProducts, setRelatedProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRelatedProducts = async () => {
      try {
        // First try to get products from the same category
        const categoryResults = await fetchProducts({
          category: categorySlug,
          per_page: 6,
          sort_by: 'rating',
          sort_order: 'desc'
        });
        
        // Filter out current product
        const filtered = categoryResults.products.filter(p => p.id !== currentProductId);
        
        if (filtered.length >= 3) {
          setRelatedProducts(filtered.slice(0, 3));
        } else {
          // If not enough from same category, get popular products
          const popularResults = await fetchProducts({
            per_page: 6,
            sort_by: 'rating', 
            sort_order: 'desc'
          });
          const popularFiltered = popularResults.products.filter(p => p.id !== currentProductId);
          setRelatedProducts(popularFiltered.slice(0, 3));
        }
      } catch (error) {
        console.error('Error fetching related products:', error);
        setRelatedProducts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchRelatedProducts();
  }, [categorySlug, brandSlug, currentProductId]);

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="animate-pulse bg-gray-200 h-96 rounded-lg"></div>
          ))}
        </div>
      </div>
    );
  }

  if (relatedProducts.length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {relatedProducts.map((product) => (
          <div key={product.id}>
            <ProductCard product={product} />
          </div>
        ))}
      </div>
    </div>
  );
}

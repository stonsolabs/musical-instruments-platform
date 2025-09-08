import React from 'react';
import { Product } from '../types';
import { openAffiliateForStore } from '../lib/affiliate';
import { ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline';

interface ProductPricesProps {
  product: Product;
}

export default function ProductPrices({ product }: ProductPricesProps) {
  const hasStoreLinks = product.content?.store_links && Object.keys(product.content.store_links).length > 0;

  if (!hasStoreLinks) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No store information available for this product.</p>
      </div>
    );
  }

  const storeLinks = product.content?.store_links || {};

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Where to Buy</h2>
      
      {/* Store Links */}
      <div className="card">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Available at These Stores</h3>
        </div>
        
        <div className="p-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(storeLinks).map(([storeName, storeUrl]) => (
              <div key={storeName} className="border border-gray-200 rounded-lg p-4 hover:border-brand-blue transition-colors">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                    <span className="text-lg font-bold text-gray-600">
                      {storeName.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900">{storeName}</div>
                    <div className="text-sm text-gray-500">Online Store</div>
                  </div>
                </div>

                <a
                  href={typeof storeUrl === 'string' ? storeUrl : '#'}
                  onClick={async (e) => {
                    e.preventDefault();
                    await openAffiliateForStore(product as any, storeName, typeof storeUrl === 'string' ? storeUrl : undefined);
                  }}
                  className="btn-primary w-full text-center inline-flex items-center justify-center"
                >
                  View Price at {storeName}
                  <ArrowTopRightOnSquareIcon className="w-4 h-4 ml-2" />
                </a>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Store Information Note */}
      <div className="text-sm text-gray-500 text-center">
        <p>Click on any store to visit their website and check current pricing.</p>
        <p className="mt-1">We update our store links regularly to ensure they're current and working.</p>
      </div>
    </div>
  );
}

'use client';

import React from 'react';
import dynamic from 'next/dynamic';

// Dynamic import WITH server-side rendering (no ssr: false)
const UnifiedSearchAutocomplete = dynamic(() => import('@/components/UnifiedSearchAutocomplete'), {
  loading: () => <div className="w-full px-4 py-3 pl-12 pr-12 text-gray-900 bg-white border border-gray-300 rounded-lg animate-pulse">Loading search...</div>
});

interface CompareSearchInterfaceProps {
  currentProducts?: string;
}

export default function CompareSearchInterface({ currentProducts = '' }: CompareSearchInterfaceProps) {
  const handleInstrument1Select = React.useCallback((product: any) => {
    console.log('Instrument 1 selected:', product);
    if (product?.slug) {
      window.location.href = `/compare?products=${product.slug}`;
    }
  }, []);

  const handleInstrument2Select = React.useCallback((product: any) => {
    console.log('Instrument 2 selected:', product);
    if (product?.slug) {
      const currentProductsArray = currentProducts ? decodeURIComponent(currentProducts).split(',') : [];
      const newProducts = [...currentProductsArray, product.slug];
      window.location.href = `/compare?products=${newProducts.join(',')}`;
    }
  }, [currentProducts]);

  return (
    <div className="max-w-4xl mx-auto mb-8">
      <div className="bg-white rounded-xl shadow-elegant border border-primary-200 p-8">
        <h2 className="text-2xl font-bold text-primary-900 mb-6 text-center">Compare Instruments</h2>
        
        {/* Search Fields */}
        <div className="flex flex-col md:flex-row items-center gap-6 mb-8">
          <div className="flex-1 w-full">
            <label className="block text-sm font-medium text-primary-700 mb-2">Instrument 1</label>
            <UnifiedSearchAutocomplete 
              variant="product-select"
              placeholder="Search for guitars, pianos, drums..."
              className="w-full"
              onProductSelect={handleInstrument1Select}
            />
          </div>
          
          <div className="text-primary-400 font-semibold text-xl">vs</div>
          
          <div className="flex-1 w-full">
            <label className="block text-sm font-medium text-primary-700 mb-2">Instrument 2</label>
            <UnifiedSearchAutocomplete 
              variant="product-select"
              placeholder="Search for guitars, pianos, drums..."
              className="w-full"
              onProductSelect={handleInstrument2Select}
            />
          </div>
        </div>
        
        {/* Add Another Instrument */}
        <div className="border-2 border-dashed border-primary-300 rounded-lg p-6 text-center hover:border-primary-400 transition-colors cursor-pointer">
          <div className="flex items-center justify-center gap-2 text-primary-600">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span className="font-medium">Add another instrument</span>
          </div>
        </div>
        
        {/* Compare Button */}
        <div className="mt-6 text-center">
          <button className="bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors text-lg">
            Compare Instruments
          </button>
        </div>
      </div>
    </div>
  );
}
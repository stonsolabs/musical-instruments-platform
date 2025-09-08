import React, { useState, useMemo, useCallback } from 'react';
import { MagnifyingGlassIcon, PlusIcon } from '@heroicons/react/24/outline';
import { searchProducts } from '../lib/api';
import { getProductImageUrl } from '../lib/utils';

interface CompareSearchProps {
  onProductSelect: (productId: number) => void;
}

export default function CompareSearch({ onProductSelect }: CompareSearchProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);

  // Separate function to perform the actual search
  const performSearch = useCallback(async (query: string) => {
    if (query.trim().length < 2) {
      setSearchResults([]);
      setIsSearching(false);
      return;
    }

    setIsSearching(true);
    try {
      const results = await searchProducts(query, 10);
      const mapped = results.map((p: any) => ({
        id: p.id,
        name: p.name,
        brand: p.brand?.name || '',
        category: p.category?.name || '',
        slug: p.slug,
        images: p.images,
      }));
      setSearchResults(mapped);
    } catch (e) {
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  }, []);

  // Debounced search function
  const debouncedSearch = useMemo(() => {
    let timeoutId: NodeJS.Timeout;
    return (query: string) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => performSearch(query), 300);
    };
  }, [performSearch]);

  // Handle input change
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    setActiveIndex(-1); // Reset active index when typing
    
    if (query.trim().length < 2) {
      setSearchResults([]);
      setIsSearching(false);
      return;
    }
    
    debouncedSearch(query);
  }, [debouncedSearch]);

  const handleProductSelect = (productId: number) => {
    onProductSelect(productId);
    setSearchQuery('');
    setSearchResults([]);
    setActiveIndex(-1);
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!searchResults.length) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActiveIndex((prev) => (prev + 1) % searchResults.length);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveIndex((prev) => (prev - 1 + searchResults.length) % searchResults.length);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (activeIndex >= 0 && activeIndex < searchResults.length) {
        handleProductSelect(searchResults[activeIndex].id);
      }
    } else if (e.key === 'Escape') {
      setSearchResults([]);
      setActiveIndex(-1);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="relative">
        <div className="relative">
          <input
            type="text"
            placeholder="Search for products to compare..."
            value={searchQuery}
            onChange={handleInputChange}
            onKeyDown={onKeyDown}
            className="w-full pl-12 pr-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-blue focus:border-transparent"
          />
          <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-6 w-6 text-gray-400" />
          
          {isSearching && (
            <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-brand-blue"></div>
            </div>
          )}
        </div>

        {/* Search Results Dropdown */}
        {searchResults.length > 0 && (
          <div className="absolute z-20 w-full mt-2 bg-white border border-gray-300 rounded-lg shadow-lg max-h-64 overflow-y-auto">
            {searchResults.map((product, idx) => (
              <button
                key={product.id}
                onClick={() => handleProductSelect(product.id)}
                className={`w-full px-4 py-3 text-left border-b border-gray-100 last:border-b-0 flex items-center justify-between gap-3 ${activeIndex===idx ? 'bg-gray-50' : 'hover:bg-gray-50'}`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gray-100 rounded overflow-hidden flex-shrink-0">
                    <img
                      src={getProductImageUrl(product)}
                      alt={product.name}
                      className="w-full h-full object-cover"
                      onError={(e)=>{(e.target as HTMLImageElement).style.display='none'}}
                    />
                  </div>
                  <div className="flex-1">
                    <div className="font-medium text-gray-900 group-hover:text-brand-blue">
                      {product.name}
                    </div>
                    <div className="text-sm text-gray-500">
                      {product.brand} • {product.category}
                    </div>
                  </div>
                </div>
                <PlusIcon className="w-5 h-5 text-gray-400 group-hover:text-brand-blue" />
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Search Tips */}
      <div className="mt-4 text-center text-sm text-gray-600">
        <p>Search by product name, brand, or category to add products to your comparison</p>
        <p className="mt-1">You can compare up to 4 products at once</p>
      </div>
    </div>
  );
}

import React, { useState, useRef, useEffect } from 'react';
import { MagnifyingGlassIcon, PlusIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { searchProducts } from '../lib/api';
import { Product } from '../types';

interface ComparisonSearchProps {
  className?: string;
}

export default function ComparisonSearch({ className = '' }: ComparisonSearchProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Product[]>([]);
  const [selectedProducts, setSelectedProducts] = useState<Product[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);

  // Check if selected products are from different categories
  const hasDifferentCategories = () => {
    if (selectedProducts.length < 2) return false;
    const categories = new Set(selectedProducts.map(p => p.category.name));
    return categories.size > 1;
  };

  // Handle click outside to close search results
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowResults(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Search products
  const handleSearch = async (query: string) => {
    if (query.trim().length < 2) {
      setSearchResults([]);
      setShowResults(false);
      return;
    }

    setIsSearching(true);
    try {
      const results = await searchProducts(query, 5);
      setSearchResults(results);
      setShowResults(true);
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  // Handle input change with debounce
  useEffect(() => {
    const timer = setTimeout(() => {
      handleSearch(searchQuery);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Add product to comparison
  const addToComparison = (product: Product) => {
    if (selectedProducts.length >= 4) {
      alert('You can compare up to 4 instruments at once.');
      return;
    }
    
    if (!selectedProducts.find(p => p.id === product.id)) {
      setSelectedProducts([...selectedProducts, product]);
    }
    setSearchQuery('');
    setShowResults(false);
  };

  // Remove product from comparison
  const removeFromComparison = (productId: number) => {
    setSelectedProducts(selectedProducts.filter(p => p.id !== productId));
  };

  // Handle compare action
  const handleCompare = () => {
    if (selectedProducts.length === 0) {
      alert('Please add at least 1 instrument.');
      return;
    }
    
    if (selectedProducts.length === 1) {
      // Single product - go to product page
      window.open(`/products/${selectedProducts[0].slug}`, '_blank');
    } else {
      // Multiple products - go to compare page
      const productSlugs = selectedProducts.map(p => p.slug).join(',');
      window.open(`/compare?products=${productSlugs}`, '_blank');
    }
  };

  return (
    <div className={`bg-white rounded-2xl shadow-xl border border-slate-200 p-8 ${className}`}>
      {/* Search Input */}
      <div className="relative mb-6" ref={searchRef}>
        <div className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search instrument 1"
            className="w-full pl-12 pr-4 py-4 text-lg bg-gray-50 border-0 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all"
          />
          <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          {isSearching && (
            <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full"></div>
            </div>
          )}
        </div>
        
        {/* Search Results */}
        {showResults && searchResults.length > 0 && (
          <div className="absolute z-10 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl max-h-60 overflow-y-auto">
            {searchResults.map((product) => (
              <button
                key={product.id}
                onClick={() => addToComparison(product)}
                className="w-full px-4 py-3 text-left hover:bg-slate-50 border-b border-slate-100 last:border-b-0 flex items-center space-x-3 transition-colors"
              >
                <div className="w-12 h-12 bg-slate-100 rounded-lg overflow-hidden flex-shrink-0">
                  {product.images && product.images.length > 0 ? (
                    <img 
                      src={product.images[0]} 
                      alt={product.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full bg-slate-200"></div>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-slate-900 truncate">
                    {product.name}
                  </p>
                  <p className="text-sm text-slate-500">
                    {product.brand.name} • {product.category.name}
                  </p>
                </div>
                <PlusIcon className="h-5 w-5 text-slate-400" />
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Add Another Instrument */}
      {selectedProducts.length > 0 && selectedProducts.length < 4 && (
        <div className="mb-6">
          <button className="w-full border-2 border-dashed border-slate-300 rounded-xl py-8 text-slate-500 hover:border-blue-400 hover:text-blue-600 hover:bg-blue-50 transition-all">
            <PlusIcon className="h-8 w-8 mx-auto mb-2" />
            Add another instrument
          </button>
        </div>
      )}

      {/* Selected Products */}
      {selectedProducts.length > 0 && (
        <div className="mb-6">
          <div className="grid gap-3">
            {selectedProducts.map((product, index) => (
              <div key={product.id} className="flex items-center space-x-3 p-4 bg-slate-50 rounded-xl border border-slate-200">
                <div className="w-12 h-12 bg-slate-100 rounded-lg overflow-hidden flex-shrink-0">
                  {product.images && product.images.length > 0 ? (
                    <img 
                      src={product.images[0]} 
                      alt={product.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full bg-slate-200"></div>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-slate-900 truncate">
                    {product.name}
                  </p>
                  <p className="text-sm text-slate-500">
                    {product.brand.name} • {product.category.name}
                  </p>
                </div>
                <button
                  onClick={() => removeFromComparison(product.id)}
                  className="text-slate-400 hover:text-red-500 transition-colors p-1"
                >
                  <XMarkIcon className="h-5 w-5" />
                </button>
              </div>
            ))}
          </div>
          
          {/* Different Categories Disclaimer */}
          {hasDifferentCategories() && (
            <div className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-xl">
              <div className="flex items-start space-x-2">
                <div className="flex-shrink-0">
                  <span className="text-amber-600">⚠️</span>
                </div>
                <div className="text-sm text-amber-800">
                  <p className="font-medium">Comparing Different Categories</p>
                  <p>You're comparing instruments from different categories. Some specifications may not be directly comparable.</p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Compare Button */}
      <button
        onClick={handleCompare}
        disabled={selectedProducts.length === 0}
        className={`w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all ${
          selectedProducts.length > 0
            ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
            : 'bg-slate-200 text-slate-500 cursor-not-allowed'
        }`}
      >
        {selectedProducts.length === 1 
          ? 'View Instrument' 
          : selectedProducts.length > 1 
            ? `Compare ${selectedProducts.length} Instruments`
            : 'Compare 0 Instruments'
        }
      </button>
    </div>
  );
}

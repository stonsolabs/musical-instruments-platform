import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { XMarkIcon, ScaleIcon } from '@heroicons/react/24/outline';
import { Product } from '../types';

interface ComparisonContextType {
  selectedProducts: Product[];
  addToComparison: (product: Product) => void;
  removeFromComparison: (productId: number) => void;
  clearComparison: () => void;
  isProductSelected: (productId: number) => boolean;
}

const ComparisonContext = createContext<ComparisonContextType | null>(null);

export const useComparison = (): ComparisonContextType => {
  const context = useContext(ComparisonContext);
  if (!context) {
    // Safe no-op fallback when provider is not mounted
    return {
      selectedProducts: [],
      addToComparison: () => {},
      removeFromComparison: () => {},
      clearComparison: () => {},
      isProductSelected: () => false,
    };
  }
  return context;
};

interface ComparisonProviderProps {
  children: React.ReactNode;
}

export function ComparisonProvider({ children }: ComparisonProviderProps) {
  const [selectedProducts, setSelectedProducts] = useState<Product[]>([]);
  const [isHydrated, setIsHydrated] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    setIsHydrated(true);
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('comparison-products');
      if (saved) {
        try {
          setSelectedProducts(JSON.parse(saved));
        } catch (e) {
          console.error('Failed to parse saved comparison products:', e);
        }
      }
    }
  }, []);

  // Save to localStorage when selection changes
  useEffect(() => {
    if (isHydrated && typeof window !== 'undefined') {
      localStorage.setItem('comparison-products', JSON.stringify(selectedProducts));
    }
  }, [selectedProducts, isHydrated]);

  const addToComparison = (product: Product) => {
    setSelectedProducts(prev => {
      // Check if already selected
      if (prev.find(p => p.id === product.id)) {
        return prev;
      }
      
      // Limit to 4 products
      if (prev.length >= 4) {
        alert('You can compare up to 4 instruments at once.');
        return prev;
      }
      
      return [...prev, product];
    });
  };

  const removeFromComparison = (productId: number) => {
    setSelectedProducts(prev => prev.filter(p => p.id !== productId));
  };

  const clearComparison = () => {
    setSelectedProducts([]);
  };

  const isProductSelected = (productId: number) => {
    return selectedProducts.some(p => p.id === productId);
  };

  return (
    <ComparisonContext.Provider value={{
      selectedProducts,
      addToComparison,
      removeFromComparison,
      clearComparison,
      isProductSelected
    }}>
      {children}
      {isHydrated && <FloatingCompareButton />}
    </ComparisonContext.Provider>
  );
}

function FloatingCompareButton() {
  const { selectedProducts, removeFromComparison, clearComparison } = useComparison();
  const router = useRouter();

  // Check if selected products are from different categories
  const hasDifferentCategories = () => {
    if (selectedProducts.length < 2) return false;
    const categories = new Set(selectedProducts.map(p => p?.category?.name).filter(Boolean) as string[]);
    return categories.size > 1;
  };

  const handleCompare = () => {
    if (selectedProducts.length === 0) return;
    
    if (selectedProducts.length === 1) {
      // Single product - go to product page
      router.push(`/products/${selectedProducts[0].slug}`);
    } else {
      // Multiple products - go to compare page
      const productSlugs = selectedProducts.map(p => p.slug).join(',');
      router.push(`/compare?products=${productSlugs}`);
    }
  };

  if (selectedProducts.length === 0) return null;

  return (
    <div className="fixed bottom-4 right-4 z-50 max-w-sm">
      <div className="bg-white rounded-lg shadow-xl border border-gray-200 p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <ScaleIcon className="h-5 w-5 text-brand-primary" />
            <h3 className="font-semibold text-gray-900">
              Compare ({selectedProducts.length}/4)
            </h3>
          </div>
          <button
            onClick={clearComparison}
            className="text-gray-400 hover:text-red-500 transition-colors"
            title="Clear all"
          >
            <XMarkIcon className="h-4 w-4" />
          </button>
        </div>

        {/* Selected Products List */}
        <div className="space-y-2 mb-4 max-h-40 overflow-y-auto">
          {selectedProducts.map((product) => (
            <div key={product.id} className="flex items-center space-x-2 p-2 bg-gray-50 rounded">
              <div className="w-8 h-8 bg-gray-100 rounded overflow-hidden flex-shrink-0">
                {product.images && product.images.length > 0 ? (
                  <img 
                    src={product.images[0]} 
                    alt={product.name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full bg-gray-200"></div>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-gray-900 truncate">
                  {product.name}
                </p>
                <p className="text-xs text-gray-500">
                  {product?.brand?.name || 'Unknown Brand'}
                </p>
              </div>
              <button
                onClick={() => removeFromComparison(product.id)}
                className="text-gray-400 hover:text-red-500 transition-colors flex-shrink-0"
              >
                <XMarkIcon className="h-3 w-3" />
              </button>
            </div>
          ))}
        </div>

        {/* Different Categories Warning */}
        {hasDifferentCategories() && (
          <div className="mb-3 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
            <span className="font-medium">⚠️ Different categories:</span> Some specs may not be comparable
          </div>
        )}

        {/* Action Button */}
        <button
          onClick={handleCompare}
          className="w-full py-2 px-3 bg-brand-primary text-white text-sm font-medium rounded hover:bg-brand-dark transition-colors"
        >
          {selectedProducts.length === 1 
            ? 'View Instrument' 
            : `Compare ${selectedProducts.length} Instruments`
          }
        </button>
      </div>
    </div>
  );
}

interface ProductCompareCheckboxProps {
  product: Product;
  className?: string;
}

export function ProductCompareCheckbox({ product, className = '' }: ProductCompareCheckboxProps) {
  const { addToComparison, removeFromComparison, isProductSelected } = useComparison();
  const isSelected = isProductSelected(product.id);

  const handleToggle = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (isSelected) {
      removeFromComparison(product.id);
    } else {
      addToComparison(product);
    }
  };

  return (
    <button
      onClick={handleToggle}
      className={`flex items-center space-x-1 px-2 py-1 rounded-md text-xs transition-all ${
        isSelected
          ? 'bg-brand-primary text-white shadow-sm'
          : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
      } ${className}`}
      title={isSelected ? 'Remove from comparison' : 'Add to comparison'}
    >
      <ScaleIcon className="w-3 h-3" />
      <span className="font-medium">{isSelected ? 'Added' : 'Compare'}</span>
    </button>
  );
}

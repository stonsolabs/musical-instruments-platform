'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { SearchAutocompleteProduct } from '@/types';
import { trackSearch, trackEvent } from '@/components/Analytics';
import { apiClient } from '@/lib/api';
import { formatPrice, formatRating } from '@/lib/utils';

interface UnifiedSearchAutocompleteProps {
  placeholder?: string;
  className?: string;
  value?: string;
  onChange?: (value: string) => void;
  onSearch?: (query: string) => void;
  onProductSelect?: (product: SearchAutocompleteProduct) => void;
  showSuggestions?: boolean;
  showPrices?: boolean;
  showSearchButton?: boolean;
  variant?: 'default' | 'controlled' | 'product-select';
  autoRedirect?: boolean;
}

export default function UnifiedSearchAutocomplete({
  placeholder = "Search musical instruments...",
  className = "",
  value: controlledValue,
  onChange,
  onSearch,
  onProductSelect,
  showSuggestions = true,
  showPrices = true,
  showSearchButton = true,
  variant = 'default',
  autoRedirect = true
}: UnifiedSearchAutocompleteProps) {
  // State management based on variant
  const [internalValue, setInternalValue] = useState('');
  const [suggestions, setSuggestions] = useState<SearchAutocompleteProduct[]>([]);
  const [loading, setLoading] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  
  const debounceRef = useRef<NodeJS.Timeout>();
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Use controlled or uncontrolled value based on variant
  const currentValue = variant === 'controlled' ? controlledValue || '' : internalValue;

  // Debounced search function
  const debouncedSearch = useCallback(async (searchQuery: string) => {
    if (searchQuery.length < 2) {
      setSuggestions([]);
      setShowDropdown(false);
      return;
    }

    setLoading(true);
    try {
      const response = await apiClient.searchAutocomplete(searchQuery, 8);
      setSuggestions(response.results);
      setShowDropdown(response.results.length > 0);
      
      // Auto-redirect if there's exactly one result and autoRedirect is enabled
      if (autoRedirect && response.results.length === 1) {
        const singleResult = response.results[0];
        
        // Track autocomplete auto-redirect
        trackEvent('search_auto_redirect', {
          search_term: searchQuery,
          selected_item: singleResult.name,
          item_id: singleResult.id,
          item_category: singleResult.category?.name || 'unknown'
        });
        
        // Handle based on variant
        if (variant === 'product-select' && onProductSelect) {
          onProductSelect(singleResult);
        } else {
          // Navigate to product page after a short delay
          setTimeout(() => {
            window.location.href = `/products/${singleResult.slug}-${singleResult.id}`;
          }, 500);
        }
      }
    } catch (error) {
      console.error('Search error:', error);
      setSuggestions([]);
      setShowDropdown(false);
    } finally {
      setLoading(false);
    }
  }, [autoRedirect, variant, onProductSelect]);

  // Handle input change with debouncing
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    
    if (variant === 'controlled') {
      onChange?.(newValue);
    } else {
      setInternalValue(newValue);
    }
    
    setSelectedIndex(-1);

    // Clear previous timeout
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    // Set new timeout for debounced search
    debounceRef.current = setTimeout(() => {
      debouncedSearch(newValue);
    }, 300);
  };

  // Handle keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!showDropdown || suggestions.length === 0) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => 
          prev < suggestions.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && suggestions[selectedIndex]) {
          handleSuggestionClick(suggestions[selectedIndex]);
        } else if (currentValue.trim()) {
          handleSearch();
        }
        break;
      case 'Escape':
        setShowDropdown(false);
        setSelectedIndex(-1);
        inputRef.current?.blur();
        break;
    }
  };

  // Handle suggestion click
  const handleSuggestionClick = (suggestion: SearchAutocompleteProduct) => {
    const newValue = suggestion.name;
    
    if (variant === 'controlled') {
      onChange?.(newValue);
    } else {
      setInternalValue(newValue);
    }
    
    setShowDropdown(false);
    setSelectedIndex(-1);
    
    // Track autocomplete selection
    trackEvent('search_suggestion_click', {
      search_term: currentValue,
      selected_item: suggestion.name,
      item_id: suggestion.id,
      item_category: suggestion.category?.name || 'unknown'
    });
    
    // Handle based on variant
    if (variant === 'product-select' && onProductSelect) {
      onProductSelect(suggestion);
    } else if (variant === 'controlled' && onSearch) {
      onSearch(suggestion.name);
    } else {
      // Navigate to product page
      window.location.href = `/products/${suggestion.slug}-${suggestion.id}`;
    }
  };

  // Handle search button click
  const handleSearch = () => {
    if (currentValue.trim()) {
      setShowDropdown(false);
      
      // Track search
      trackSearch(currentValue.trim(), suggestions.length);
      
      // Call custom onSearch handler if provided
      if (onSearch) {
        onSearch(currentValue.trim());
      } else if (variant !== 'controlled') {
        // Default navigation to products page with search query
        window.location.href = `/products?q=${encodeURIComponent(currentValue.trim())}`;
      }
    }
  };

  // Handle click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current && 
        !dropdownRef.current.contains(event.target as Node) &&
        inputRef.current && 
        !inputRef.current.contains(event.target as Node)
      ) {
        setShowDropdown(false);
        setSelectedIndex(-1);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, []);

  return (
    <div className={`relative ${className}`}>
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={currentValue}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={() => currentValue.length >= 2 && suggestions.length > 0 && setShowDropdown(true)}
          placeholder={placeholder}
          className="w-full px-4 py-3 pl-12 pr-12 text-gray-900 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
        />
        
        {/* Search icon */}
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        {/* Search button */}
        {showSearchButton && (
          <button
            onClick={handleSearch}
            className="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <svg className="h-5 w-5 text-gray-400 hover:text-blue-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        )}

        {/* Loading indicator */}
        {loading && (
          <div className={`absolute inset-y-0 ${showSearchButton ? 'right-8' : 'right-3'} flex items-center`}>
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
          </div>
        )}
      </div>

      {/* Dropdown suggestions */}
      {showSuggestions && showDropdown && (
        <div
          ref={dropdownRef}
          className="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-96 overflow-y-auto"
        >
          {suggestions.length > 0 ? (
            <div className="py-2">
              {suggestions.map((suggestion, index) => (
                <div
                  key={suggestion.id}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className={`px-4 py-3 cursor-pointer transition-colors ${
                    index === selectedIndex
                      ? 'bg-blue-50 border-l-4 border-blue-500'
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3 flex-1 min-w-0">
                      {/* Product Image */}
                      <div className="w-12 h-12 bg-gray-100 rounded-lg flex-shrink-0 overflow-hidden">
                        {suggestion.images && suggestion.images.length > 0 ? (
                          <img 
                            src={suggestion.images[0]} 
                            alt={suggestion.name}
                            className="w-full h-full object-contain"
                          />
                        ) : (
                          <div className="w-full h-full flex items-center justify-center">
                            <span className="text-gray-400 text-lg">🎸</span>
                          </div>
                        )}
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        {/* Product name with highlighting */}
                        <div 
                          className="font-medium text-gray-900 mb-1"
                          dangerouslySetInnerHTML={{ __html: suggestion.search_highlight }}
                        />
                        
                        {/* Brand and category */}
                        <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
                          <span className="font-medium">{suggestion.brand.name}</span>
                          <span>•</span>
                          <span>{suggestion.category.name}</span>
                        </div>

                        {/* Rating */}
                        {suggestion.avg_rating > 0 && (
                          <div className="flex items-center gap-1 text-sm text-gray-600 mb-1">
                            <span className="text-yellow-500">★</span>
                            <span>{formatRating(suggestion.avg_rating)}</span>
                            <span>({suggestion.review_count})</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Price */}
                    {showPrices && (
                      <div className="ml-4 text-right">
                        {suggestion.best_price ? (
                          <div>
                            <div className="font-bold text-green-600">
                              {formatPrice(suggestion.best_price.price, suggestion.best_price.currency)}
                            </div>
                            <div className="text-xs text-gray-500">
                              at {suggestion.best_price.store.name}
                            </div>
                          </div>
                        ) : (
                          <div className="text-sm text-gray-500">No price</div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="px-4 py-3 text-gray-500 text-center">
              No products found
            </div>
          )}
        </div>
      )}
    </div>
  );
}

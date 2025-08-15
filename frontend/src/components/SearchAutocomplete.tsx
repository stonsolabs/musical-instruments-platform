'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import Link from 'next/link';
import { SearchAutocompleteProduct } from '@/types';
import { trackSearch, trackEvent } from '@/components/Analytics';
import { getApiBaseUrl } from '@/lib/api';

// Inline utility functions
const formatPrice = (price: number, currency: string = 'EUR'): string => {
  try {
    return new Intl.NumberFormat('en-GB', { style: 'currency', currency }).format(price);
  } catch {
    return `${currency} ${price.toFixed(2)}`;
  }
};

const formatRating = (rating: number): string => {
  return Number.isFinite(rating) ? rating.toFixed(1) : '0.0';
};

const API_BASE_URL = getApiBaseUrl();

const apiClient = {
  async searchAutocomplete(query: string, limit: number = 8): Promise<{ results: SearchAutocompleteProduct[] }> {
    if (typeof window === 'undefined') {
      return { results: [] };
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/search/autocomplete?q=${encodeURIComponent(query)}&limit=${limit}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Autocomplete API call failed:', error);
      return { results: [] };
    }
  }
};


interface SearchAutocompleteProps {
  placeholder?: string;
  className?: string;
  onSearch?: (query: string) => void;
  showSuggestions?: boolean;
}

export default function SearchAutocomplete({
  placeholder = "Search musical instruments...",
  className = "",
  onSearch,
  showSuggestions = true
}: SearchAutocompleteProps) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<SearchAutocompleteProduct[]>([]);
  const [loading, setLoading] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const debounceRef = useRef<NodeJS.Timeout>();
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

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
    } catch (error) {
      console.error('Search error:', error);
      setSuggestions([]);
      setShowDropdown(false);
    } finally {
      setLoading(false);
    }
  }, []);

  // Handle input change with debouncing
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setSelectedIndex(-1);

    // Clear previous timeout
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    // Set new timeout for debounced search
    debounceRef.current = setTimeout(() => {
      debouncedSearch(value);
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
        } else if (query.trim()) {
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
    setQuery(suggestion.name);
    setShowDropdown(false);
    setSelectedIndex(-1);
    
    // Track autocomplete selection
    trackEvent('search_suggestion_click', {
      search_term: query,
      selected_item: suggestion.name,
      item_id: suggestion.id,
      item_category: suggestion.category?.name || 'unknown'
    });
    
    // Navigate to product page
    window.location.href = `/products/${suggestion.slug}-${suggestion.id}`;
  };

  // Handle search button click
  const handleSearch = () => {
    if (query.trim()) {
      setShowDropdown(false);
      
      // Track search
      trackSearch(query.trim(), suggestions.length);
      
      onSearch?.(query.trim());
      // Navigate to products page with search query
      window.location.href = `/products?q=${encodeURIComponent(query.trim())}`;
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
          value={query}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={() => query.length >= 2 && suggestions.length > 0 && setShowDropdown(true)}
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
        <button
          onClick={handleSearch}
          className="absolute inset-y-0 right-0 pr-3 flex items-center"
        >
          <svg className="h-5 w-5 text-gray-400 hover:text-blue-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>

        {/* Loading indicator */}
        {loading && (
          <div className="absolute inset-y-0 right-8 flex items-center">
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

                    {/* Price */}
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

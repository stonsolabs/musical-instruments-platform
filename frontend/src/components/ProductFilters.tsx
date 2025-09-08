import React, { useState } from 'react';
import { Category, Brand } from '../types';
import { ChevronDownIcon } from '@heroicons/react/24/outline';

interface ProductFiltersProps {
  categories: Category[];
  brands: Brand[];
  filters: {
    category: string;
    brand: string;
    search: string;
    priceMin: string;
    priceMax: string;
  };
  onFiltersChange: (filters: any) => void;
}

export default function ProductFilters({ categories, brands, filters, onFiltersChange }: ProductFiltersProps) {
  const [expandedSections, setExpandedSections] = useState({
    category: true,
    brand: true,
    price: false
  });

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const handleFilterChange = (key: string, value: string) => {
    const newFilters = { ...filters, [key]: value };
    onFiltersChange(newFilters);
  };

  const clearFilters = () => {
    const clearedFilters = {
      category: '',
      brand: '',
      search: '',
      priceMin: '',
      priceMax: ''
    };
    onFiltersChange(clearedFilters);
  };

  const hasActiveFilters = Object.values(filters).some(value => value !== '');

  return (
    <div className="space-y-6">
      {/* Search */}
      <div>
        <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
          Search
        </label>
        <input
          type="text"
          id="search"
          placeholder="Search products..."
          value={filters.search}
          onChange={(e) => handleFilterChange('search', e.target.value)}
          className="input-field"
        />
      </div>

      {/* Category Filter */}
      <div>
        <button
          onClick={() => toggleSection('category')}
          className="flex items-center justify-between w-full text-left text-sm font-medium text-gray-700 mb-2"
        >
          Category
          <ChevronDownIcon
            className={`w-4 h-4 transition-transform ${
              expandedSections.category ? 'rotate-180' : ''
            }`}
          />
        </button>
        
        {expandedSections.category && (
          <div className="space-y-2">
            {categories.map((category) => (
              <label key={category.id} className="flex items-center">
                <input
                  type="radio"
                  name="category"
                  value={category.slug}
                  checked={filters.category === category.slug}
                  onChange={(e) => handleFilterChange('category', e.target.value)}
                  className="h-4 w-4 text-brand-blue focus:ring-brand-blue border-gray-300"
                />
                <span className="ml-2 text-sm text-gray-600">{category.name}</span>
              </label>
            ))}
          </div>
        )}
      </div>

      {/* Brand Filter */}
      <div>
        <button
          onClick={() => toggleSection('brand')}
          className="flex items-center justify-between w-full text-left text-sm font-medium text-gray-700 mb-2"
        >
          Brand
          <ChevronDownIcon
            className={`w-4 h-4 transition-transform ${
              expandedSections.brand ? 'rotate-180' : ''
            }`}
          />
        </button>
        
        {expandedSections.brand && (
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {(brands || []).filter(b => (b.slug !== 'unknown-brand') && (b.name?.toLowerCase() !== 'unknown brand')).map((brand) => (
              <label key={brand.id} className="flex items-center">
                <input
                  type="radio"
                  name="brand"
                  value={brand.slug}
                  checked={filters.brand === brand.slug}
                  onChange={(e) => handleFilterChange('brand', e.target.value)}
                  className="h-4 w-4 text-brand-blue focus:ring-brand-blue border-gray-300"
                />
                <span className="ml-2 text-sm text-gray-600">{brand.name}</span>
              </label>
            ))}
          </div>
        )}
      </div>

      {/* Price Filter - hidden (backend removed price filtering) */}

      {/* Clear Filters */}
      {hasActiveFilters && (
        <button
          onClick={clearFilters}
          className="w-full btn-secondary text-sm"
        >
          Clear All Filters
        </button>
      )}
    </div>
  );
}

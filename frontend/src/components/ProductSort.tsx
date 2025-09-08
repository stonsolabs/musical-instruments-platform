import React from 'react';
import { ChevronDownIcon } from '@heroicons/react/24/outline';

interface ProductSortProps {
  sortBy: string;
  sortOrder: 'asc' | 'desc';
  onSortChange: (sortBy: string, sortOrder: 'asc' | 'desc') => void;
}

export default function ProductSort({ sortBy, sortOrder, onSortChange }: ProductSortProps) {
  const sortOptions = [
    { value: 'name', label: 'Name' },
    { value: 'price', label: 'Price' },
    { value: 'rating', label: 'Rating' },
    { value: 'review_count', label: 'Reviews' },
    { value: 'created_at', label: 'Newest' }
  ];

  const handleSortByChange = (newSortBy: string) => {
    onSortChange(newSortBy, sortOrder);
  };

  const handleSortOrderChange = (newSortOrder: 'asc' | 'desc') => {
    onSortChange(sortBy, newSortOrder);
  };

  return (
    <div className="flex items-center space-x-4">
      <label htmlFor="sortBy" className="text-sm font-medium text-gray-700">
        Sort by:
      </label>
      
      <select
        id="sortBy"
        value={sortBy}
        onChange={(e) => handleSortByChange(e.target.value)}
        className="input-field text-sm py-1 px-2 w-32"
      >
        {sortOptions.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      <button
        onClick={() => handleSortOrderChange(sortOrder === 'asc' ? 'desc' : 'asc')}
        className="flex items-center space-x-1 text-sm text-gray-600 hover:text-gray-900 transition-colors"
        title={sortOrder === 'asc' ? 'Sort ascending' : 'Sort descending'}
      >
        <span>{sortOrder === 'asc' ? 'A to Z' : 'Z to A'}</span>
        <ChevronDownIcon
          className={`w-4 h-4 transition-transform ${
            sortOrder === 'desc' ? 'rotate-180' : ''
          }`}
        />
      </button>
    </div>
  );
}

'use client';

import React, { useState } from 'react';
import Link from 'next/link';

export default function HomePage() {
  const [searchItems, setSearchItems] = useState(['', '']);
  const [showThirdField, setShowThirdField] = useState(false);

  const addSearchField = () => {
    if (searchItems.length < 5) {
      setSearchItems([...searchItems, '']);
      if (searchItems.length === 2) {
        setShowThirdField(true);
      }
    }
  };

  const removeSearchField = (index: number) => {
    if (searchItems.length > 2) {
      const newItems = searchItems.filter((_, i) => i !== index);
      setSearchItems(newItems);
      if (newItems.length === 2) {
        setShowThirdField(false);
      }
    }
  };

  const updateSearchItem = (index: number, value: string) => {
    const newItems = [...searchItems];
    newItems[index] = value;
    setSearchItems(newItems);
  };

  const handleCompare = () => {
    const validItems = searchItems.filter(item => item.trim() !== '');
    if (validItems.length >= 2) {
      const queryString = validItems.join(',');
      window.location.href = `/compare?ids=${queryString}`;
    }
  };

  // Pre-created popular comparisons
  const popularComparisons = [
    { title: 'Fender Stratocaster vs Gibson Les Paul', ids: '1,2', image: '/images/comparison-1.jpg' },
    { title: 'Yamaha vs Roland Keyboards', ids: '3,4', image: '/images/comparison-2.jpg' },
    { title: 'Pearl vs Tama Drums', ids: '5,6', image: '/images/comparison-3.jpg' },
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-900 via-blue-800 to-purple-900 text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left side - Text content */}
            <div className="text-center lg:text-left">
              <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
                Search, compare, save
              </h1>
              <h2 className="text-2xl md:text-3xl font-semibold mb-4">
                Find your next instrument today
              </h2>
              <p className="text-xl text-blue-100 mb-8">
                At MusicEurope you can compare prices on thousands of instruments from Europe's top music stores
              </p>
            </div>

            {/* Right side - Dynamic search interface */}
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
              <h3 className="text-2xl font-bold mb-6 text-center">Compare Instruments</h3>
              
              <div className="space-y-4">
                {searchItems.map((item, index) => (
                  <div key={index} className="relative">
                    <div className="flex items-center gap-3">
                      <input
                        type="text"
                        placeholder={`Search instrument ${index + 1}`}
                        value={item}
                        onChange={(e) => updateSearchItem(index, e.target.value)}
                        className="flex-1 px-4 py-3 rounded-lg border-0 bg-white/90 text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-400 focus:bg-white transition-all"
                      />
                      {searchItems.length > 2 && (
                        <button
                          onClick={() => removeSearchField(index)}
                          className="w-8 h-8 rounded-full bg-red-500 text-white flex items-center justify-center hover:bg-red-600 transition-colors"
                        >
                          ×
                        </button>
                      )}
                    </div>
                    {index < searchItems.length - 1 && (
                      <div className="text-center text-white/80 text-sm font-medium mt-2">vs</div>
                    )}
                  </div>
                ))}
                
                {searchItems.length < 5 && (
                  <button
                    onClick={addSearchField}
                    className="w-full py-3 px-4 border-2 border-dashed border-white/40 rounded-lg text-white/80 hover:border-white/60 hover:text-white transition-colors"
                  >
                    + Add another instrument
                  </button>
                )}
              </div>

              <button
                onClick={handleCompare}
                className="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-6 rounded-lg transition-colors"
              >
                Compare {searchItems.filter(item => item.trim() !== '').length} Instruments
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Popular Comparisons */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Popular Comparisons</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {popularComparisons.map((comparison, index) => (
              <Link
                key={index}
                href={`/compare?ids=${comparison.ids}`}
                className="group bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-all"
              >
                <div className="h-48 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                  <div className="text-white text-4xl font-bold">VS</div>
                </div>
                <div className="p-6">
                  <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                    {comparison.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4">
                    See detailed comparison of these popular instruments
                  </p>
                  <div className="flex items-center text-blue-600 font-medium">
                    Compare Now
                    <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Simple placeholder for products without API calls */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Featured Instruments</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="h-48 bg-gray-200 rounded-lg mb-4 flex items-center justify-center">
                  <span className="text-gray-400 text-2xl">🎸</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Featured Instrument {i}</h3>
                <p className="text-gray-600 text-sm mb-4">High-quality musical instrument perfect for professionals and enthusiasts.</p>
                <div className="flex items-center justify-between">
                  <span className="text-lg font-bold text-green-600">€{299 + i * 50}</span>
                  <span className="text-sm text-gray-500">★ 4.{5 + i % 5}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

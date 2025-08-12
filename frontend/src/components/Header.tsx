"use client";

import React, { useState } from 'react';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm border-b">
      {/* Top navigation */}
      <div className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-10 text-xs">
            <div className="flex items-center space-x-4">
              <a href="/lists" className="hover:text-gray-300">Lists</a>
              <a href="/deals" className="hover:text-gray-300">Deals</a>
              <a href="/forum" className="hover:text-gray-300">Forum</a>
            </div>
            <div className="flex items-center space-x-4">
              <a href="/pro" className="bg-orange-500 px-3 py-1 rounded text-white hover:bg-orange-600">PRO</a>
              <a href="/signatures" className="hover:text-gray-300">Signatures</a>
            </div>
          </div>
        </div>
      </div>

      {/* Main navigation */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <a href="/" className="text-2xl font-bold text-gray-900">
              MusicEurope
            </a>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <div className="relative group">
              <button className="flex items-center text-gray-700 hover:text-gray-900 py-2">
                Electric Guitars
                <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute top-full left-0 w-64 bg-white shadow-lg border rounded-md opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                <div className="p-4">
                  <div className="text-sm font-medium text-gray-900 mb-2">Price Range</div>
                  <div className="space-y-1 text-sm">
                    <a href="/products?price=0-200" className="block hover:text-blue-600">Under €200</a>
                    <a href="/products?price=200-500" className="block hover:text-blue-600">€200-€500</a>
                    <a href="/products?price=500-1000" className="block hover:text-blue-600">€500-€1000</a>
                    <a href="/products?price=1000+" className="block hover:text-blue-600">€1000+</a>
                  </div>
                </div>
              </div>
            </div>

            <div className="relative group">
              <button className="flex items-center text-gray-700 hover:text-gray-900 py-2">
                Acoustic Guitars
                <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute top-full left-0 w-64 bg-white shadow-lg border rounded-md opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                <div className="p-4">
                  <div className="text-sm font-medium text-gray-900 mb-2">Price Range</div>
                  <div className="space-y-1 text-sm">
                    <a href="/products?category=acoustic&price=0-200" className="block hover:text-blue-600">Under €200</a>
                    <a href="/products?category=acoustic&price=200-500" className="block hover:text-blue-600">€200-€500</a>
                    <a href="/products?category=acoustic&price=500-1000" className="block hover:text-blue-600">€500-€1000</a>
                    <a href="/products?category=acoustic&price=1000+" className="block hover:text-blue-600">€1000+</a>
                  </div>
                </div>
              </div>
            </div>

            <a href="/products?category=bass" className="text-gray-700 hover:text-gray-900">Bass Guitars</a>
            <a href="/products?category=drums" className="text-gray-700 hover:text-gray-900">Drums</a>
            <a href="/products?category=keyboards" className="text-gray-700 hover:text-gray-900">Keyboards</a>
            <a href="/compare" className="text-gray-700 hover:text-gray-900">Compare</a>
          </nav>

          {/* Search */}
          <div className="hidden md:flex items-center flex-1 max-w-md mx-8">
            <div className="relative w-full">
              <input
                type="text"
                placeholder="Search instruments..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <svg className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-700 hover:text-gray-900"
            >
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-t">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <a href="/products" className="block px-3 py-2 text-gray-700 hover:text-gray-900">All Products</a>
            <a href="/products?category=electric" className="block px-3 py-2 text-gray-700 hover:text-gray-900">Electric Guitars</a>
            <a href="/products?category=acoustic" className="block px-3 py-2 text-gray-700 hover:text-gray-900">Acoustic Guitars</a>
            <a href="/products?category=bass" className="block px-3 py-2 text-gray-700 hover:text-gray-900">Bass Guitars</a>
            <a href="/compare" className="block px-3 py-2 text-gray-700 hover:text-gray-900">Compare</a>
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;



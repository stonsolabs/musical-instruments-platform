"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import SearchAutocomplete from './SearchAutocomplete';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm border-b sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold text-gray-900 hover:text-blue-600 transition-colors">
              MusicEurope
            </Link>
            <div className="ml-2 text-sm text-gray-600 hidden md:block">The Instrument Database</div>
          </div>

          {/* Search Bar */}
          <div className="hidden md:block flex-1 max-w-2xl mx-8">
            <SearchAutocomplete 
              placeholder="Search guitars, pianos, drums..."
              className="w-full"
            />
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <div className="relative group">
              <button className="flex items-center text-gray-700 hover:text-gray-900 py-2 transition-colors">
                All Categories
                <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute top-full left-0 w-64 bg-white shadow-lg border rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                <div className="p-4">
                  <div className="text-sm font-medium text-gray-900 mb-2">Categories</div>
                  <div className="space-y-1 text-sm">
                    <Link href="/products?category=electric" className="block hover:text-blue-600 transition-colors">Electric Guitars</Link>
                    <Link href="/products?category=acoustic" className="block hover:text-blue-600 transition-colors">Acoustic Guitars</Link>
                    <Link href="/products?category=bass" className="block hover:text-blue-600 transition-colors">Bass Guitars</Link>
                    <Link href="/products?category=drums" className="block hover:text-blue-600 transition-colors">Drums</Link>
                    <Link href="/products?category=keyboards" className="block hover:text-blue-600 transition-colors">Keyboards</Link>
                    <Link href="/products?category=amplifiers" className="block hover:text-blue-600 transition-colors">Amplifiers</Link>
                  </div>
                </div>
              </div>
            </div>

            <Link href="/deals" className="text-gray-700 hover:text-gray-900 transition-colors">Deals</Link>
            <Link href="/blog" className="text-gray-700 hover:text-gray-900 transition-colors">Blog</Link>
            <Link href="/how-to-use" className="text-gray-700 hover:text-gray-900 transition-colors">How to use</Link>
            <Link href="/about" className="text-gray-700 hover:text-gray-900 transition-colors">About us</Link>
          </nav>

          {/* Right side */}
          <div className="flex items-center space-x-4">
            <Link href="/compare" className="hidden md:block text-gray-700 hover:text-gray-900 transition-colors">
              Compare
            </Link>
            <Link href="/pro" className="hidden md:block bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
              PRO
            </Link>
            <Link href="/signin" className="text-gray-700 hover:text-gray-900 transition-colors">
              Sign in
            </Link>

            {/* Mobile menu button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden text-gray-700 hover:text-gray-900 p-2 rounded-md transition-colors"
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
        <div className="md:hidden bg-white border-t animate-slide-up">
          <div className="px-4 pt-4 pb-3 space-y-3">
            {/* Mobile Search */}
            <div className="mb-4">
              <SearchAutocomplete 
                placeholder="Search instruments..."
                className="w-full"
              />
            </div>
            
            <Link href="/products" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">All Products</Link>
            <Link href="/products?category=electric" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Electric Guitars</Link>
            <Link href="/products?category=acoustic" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Acoustic Guitars</Link>
            <Link href="/products?category=bass" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Bass Guitars</Link>
            <Link href="/deals" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Deals</Link>
            <Link href="/compare" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Compare</Link>
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;



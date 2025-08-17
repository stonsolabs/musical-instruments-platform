"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import SearchAutocomplete from './SearchAutocomplete';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center hover:opacity-80 transition-opacity">
              <Image 
                src="/logo.png" 
                alt="GetYourMusicGear Logo" 
                width={180} 
                height={60}
                className="h-12 w-auto"
              />
            </Link>
          </div>

          {/* Search Bar */}
          <div className="hidden md:block flex-1 max-w-xl mx-12">
            <SearchAutocomplete 
              placeholder="Search instruments..."
              className="w-full"
            />
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-10">
            <div className="relative group">
              <button className="flex items-center text-gray-600 hover:text-gray-900 py-2 transition-colors text-sm font-medium">
                Categories
                <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute top-full left-0 w-72 bg-white border border-gray-100 rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 shadow-sm">
                <div className="p-6">
                  <div className="text-sm font-semibold text-gray-900 mb-4">Shop by Category</div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <Link href="/products?category=electric-guitars" className="block hover:text-gray-900 transition-colors text-gray-600">Electric Guitars</Link>
                    <Link href="/products?category=acoustic-guitars" className="block hover:text-gray-900 transition-colors text-gray-600">Acoustic Guitars</Link>
                    <Link href="/products?category=digital-keyboards" className="block hover:text-gray-900 transition-colors text-gray-600">Digital Keyboards</Link>
                    <Link href="/products?category=synthesizers" className="block hover:text-gray-900 transition-colors text-gray-600">Synthesizers</Link>
                    <Link href="/products?category=amplifiers" className="block hover:text-gray-900 transition-colors text-gray-600">Amplifiers</Link>
                    <Link href="/products?category=audio-interfaces" className="block hover:text-gray-900 transition-colors text-gray-600">Audio Interfaces</Link>
                  </div>
                </div>
              </div>
            </div>

            <Link href="/deals" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">Deals</Link>
            <Link href="/blog" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">Blog</Link>
            <Link href="/about" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">About</Link>
          </nav>

          {/* Right side */}
          <div className="flex items-center space-x-4">
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
            <Link href="/products?category=electric-guitars" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Electric Guitars</Link>
            <Link href="/products?category=acoustic-guitars" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Acoustic Guitars</Link>
            <Link href="/products?category=digital-keyboards" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Digital Keyboards</Link>
            <Link href="/products?category=synthesizers" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Synthesizers</Link>
            <Link href="/products?category=amplifiers" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Amplifiers</Link>
            <Link href="/products?category=audio-interfaces" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Audio Interfaces</Link>
            <Link href="/deals" className="block px-3 py-2 text-gray-700 hover:text-gray-900 transition-colors">Deals</Link>
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;



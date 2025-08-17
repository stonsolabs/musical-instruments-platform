"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white border-b border-gray-300 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo - Larger size */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center hover:opacity-80 transition-opacity">
              <Image 
                src="/logo.png" 
                alt="GetYourMusicGear Logo" 
                width={220} 
                height={70}
                className="h-14 w-auto"
              />
            </Link>
          </div>

          {/* Desktop Navigation - Centered and larger text */}
          <nav className="hidden md:flex items-center space-x-10">
            <div className="relative group">
              <button className="flex items-center text-gray-900 hover:text-gray-700 py-2 transition-colors text-base font-medium">
                Instruments
                <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute top-full left-0 w-72 bg-white border border-gray-300 rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 shadow-lg">
                <div className="p-6">
                  <div className="text-base font-semibold text-gray-900 mb-4">Shop by Category</div>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <Link href="/products?category=electric-guitars" className="block hover:text-gray-700 transition-colors text-gray-600 py-1">Electric Guitars</Link>
                    <Link href="/products?category=acoustic-guitars" className="block hover:text-gray-700 transition-colors text-gray-600 py-1">Acoustic Guitars</Link>
                    <Link href="/products?category=digital-keyboards" className="block hover:text-gray-700 transition-colors text-gray-600 py-1">Digital Keyboards</Link>
                    <Link href="/products?category=synthesizers" className="block hover:text-gray-700 transition-colors text-gray-600 py-1">Synthesizers</Link>
                    <Link href="/products?category=amplifiers" className="block hover:text-gray-700 transition-colors text-gray-600 py-1">Amplifiers</Link>
                    <Link href="/products?category=audio-interfaces" className="block hover:text-gray-700 transition-colors text-gray-600 py-1">Audio Interfaces</Link>
                  </div>
                </div>
              </div>
            </div>

            <Link href="/deals" className="text-gray-900 hover:text-gray-700 transition-colors text-base font-medium">Deals</Link>
            <Link href="/blog" className="text-gray-900 hover:text-gray-700 transition-colors text-base font-medium">Blog</Link>
            <Link href="/about" className="text-gray-900 hover:text-gray-700 transition-colors text-base font-medium">About</Link>
          </nav>

          {/* Right side */}
          <div className="flex items-center space-x-4">
            {/* Mobile menu button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden text-gray-900 hover:text-gray-700 p-2 rounded-md transition-colors"
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
        <div className="md:hidden bg-white border-t border-gray-300 animate-slide-up">
          <div className="px-4 pt-4 pb-3 space-y-3">
            <Link href="/products" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">All Products</Link>
            <Link href="/deals" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Deals</Link>
            <Link href="/blog" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Blog</Link>
            <Link href="/about" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">About</Link>
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;



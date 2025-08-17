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
                className="h-24 w-auto"
              />
            </Link>
          </div>

          {/* Desktop Navigation - Centered and larger text */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link href="/products?category=electric-guitars" className="text-gray-900 hover:text-gray-700 transition-colors text-base font-medium">Electric Guitars</Link>
            <Link href="/products?category=acoustic-guitars" className="text-gray-900 hover:text-gray-700 transition-colors text-base font-medium">Acoustic Guitars</Link>
            <Link href="/products?category=digital-keyboards" className="text-gray-900 hover:text-gray-700 transition-colors text-base font-medium">Keyboards</Link>
            <Link href="/products?category=synthesizers" className="text-gray-900 hover:text-gray-700 transition-colors text-base font-medium">Synthesizers</Link>
            <Link href="/products?category=amplifiers" className="text-gray-900 hover:text-gray-700 transition-colors text-base font-medium">Amplifiers</Link>
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
            <Link href="/products?category=electric-guitars" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Electric Guitars</Link>
            <Link href="/products?category=acoustic-guitars" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Acoustic Guitars</Link>
            <Link href="/products?category=digital-keyboards" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Keyboards</Link>
            <Link href="/products?category=synthesizers" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Synthesizers</Link>
            <Link href="/products?category=amplifiers" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Amplifiers</Link>
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



"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white border-b border-gray-300 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center w-[100px]">
            <Link href="/" className="flex items-center hover:opacity-80 transition-opacity w-full h-16">
              <Image 
                src="/logo.svg" 
                alt="GetYourMusicGear Logo" 
                width={100} 
                height={24}
                className="h-5 lg:h-6 w-full object-contain"
                priority
                style={{ maxWidth: '100%', height: 'auto' }}
              />
            </Link>
          </div>

          {/* Desktop Navigation - Fixed spacing */}
          <nav className="hidden lg:flex items-center justify-center flex-1 mx-4">
            <div className="flex items-center space-x-4 flex-wrap justify-center">
              <Link href="/products?category=guitars" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-2 py-2 rounded-md hover:bg-gray-50">Guitars</Link>
              <Link href="/products?category=electric-guitars" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-2 py-2 rounded-md hover:bg-gray-50">Electric</Link>
              <Link href="/products?category=acoustic-guitars" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-2 py-2 rounded-md hover:bg-gray-50">Acoustic</Link>
              <Link href="/products?category=bass-guitars" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-2 py-2 rounded-md hover:bg-gray-50">Bass</Link>
              <Link href="/products?category=drums-percussion" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-2 py-2 rounded-md hover:bg-gray-50">Drums</Link>
              <Link href="/products?category=pianos-keyboards" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-2 py-2 rounded-md hover:bg-gray-50">Keyboards</Link>
              <Link href="/products?category=orchestral" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-2 py-2 rounded-md hover:bg-gray-50">Orchestral</Link>
              <Link href="/products?category=studio-production" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-2 py-2 rounded-md hover:bg-gray-50">Studio</Link>
              <Link href="/products?category=dj-equipment" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-2 py-2 rounded-md hover:bg-gray-50">DJ</Link>
            </div>
          </nav>

          {/* Right side - Mobile menu button */}
          <div className="flex items-center flex-shrink-0">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="lg:hidden text-gray-900 hover:text-blue-600 p-2 rounded-md transition-colors"
              aria-label="Toggle menu"
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
        <div className="lg:hidden bg-white border-t border-gray-300 animate-slide-up">
          <div className="px-4 pt-4 pb-3 space-y-2">
            <Link href="/products?category=guitars" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">All Guitars</Link>
            <Link href="/products?category=electric-guitars" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Electric Guitars</Link>
            <Link href="/products?category=acoustic-guitars" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Acoustic Guitars</Link>
            <Link href="/products?category=bass-guitars" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Bass Guitars</Link>
            <Link href="/products?category=drums-percussion" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Drums & Percussion</Link>
            <Link href="/products?category=pianos-keyboards" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Pianos & Keyboards</Link>
            <Link href="/products?category=orchestral" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Orchestral</Link>
            <Link href="/products?category=studio-production" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Studio & Production</Link>
            <Link href="/products?category=dj-equipment" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">DJ Equipment</Link>
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;



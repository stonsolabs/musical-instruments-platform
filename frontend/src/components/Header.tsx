"use client";

import React, { useState, useRef } from 'react';
import Link from 'next/link';
import Image from 'next/image';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleMouseEnter = (dropdown: string) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setActiveDropdown(dropdown);
  };

  const handleMouseLeave = () => {
    timeoutRef.current = setTimeout(() => {
      setActiveDropdown(null);
    }, 150); // Small delay to allow moving to dropdown
  };

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

          {/* Desktop Navigation - Optimized for better fit */}
          <nav className="hidden lg:flex items-center justify-center flex-1 mx-4">
            <div className="flex items-center space-x-2 xl:space-x-3 flex-nowrap overflow-hidden">
              <div 
                className="relative"
                onMouseEnter={() => handleMouseEnter('guitars')}
                onMouseLeave={handleMouseLeave}
              >
                <button 
                  className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-3 py-2 rounded-md hover:bg-gray-50 flex items-center"
                >
                  Guitars
                  <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {activeDropdown === 'guitars' && (
                  <div 
                    className="absolute left-0 top-full w-48 bg-white border border-gray-200 rounded-md shadow-xl z-[99999] mt-1 py-1"
                    onMouseEnter={() => handleMouseEnter('guitars')}
                    onMouseLeave={handleMouseLeave}
                  >
                    <Link href="/products?category=acoustic-guitars" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors">Acoustic Guitars</Link>
                    <Link href="/products?category=electric-guitars" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors">Electric Guitars</Link>
                  </div>
                )}
              </div>
              <Link href="/products?category=electric-basses" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-3 py-2 rounded-md hover:bg-gray-50">Bass</Link>
              <div 
                className="relative"
                onMouseEnter={() => handleMouseEnter('keys')}
                onMouseLeave={handleMouseLeave}
              >
                <button 
                  className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-3 py-2 rounded-md hover:bg-gray-50 flex items-center"
                >
                  Keys
                  <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {activeDropdown === 'keys' && (
                  <div 
                    className="absolute left-0 top-full w-48 bg-white border border-gray-200 rounded-md shadow-xl z-[99999] mt-1 py-1"
                    onMouseEnter={() => handleMouseEnter('keys')}
                    onMouseLeave={handleMouseLeave}
                  >
                    <Link href="/products?category=digital-pianos" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors">Digital Pianos</Link>
                    <Link href="/products?category=stage-pianos" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors">Stage Pianos</Link>
                    <Link href="/products?category=home-keyboards" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors">Keyboards</Link>
                    <Link href="/products?category=synthesizer-keyboards" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors">Synthesizers</Link>
                    <Link href="/products?category=workstations" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors">Workstations</Link>
                    <Link href="/products?category=midi-master-keyboards" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors">MIDI Controllers</Link>
                  </div>
                )}
              </div>
              <Link href="/products?category=turntables" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-3 py-2 rounded-md hover:bg-gray-50">DJ</Link>
              <Link href="/products?category=studio-equipment" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-3 py-2 rounded-md hover:bg-gray-50">Studio</Link>
              <Link href="/products?category=accessories" className="text-gray-900 hover:text-blue-600 transition-colors text-sm font-medium whitespace-nowrap px-3 py-2 rounded-md hover:bg-gray-50">Accessories</Link>
              <Link href="/top-rated" className="bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 transition-all duration-200 text-sm font-bold whitespace-nowrap px-4 py-2 rounded-lg shadow-md hover:shadow-lg transform hover:scale-105">⭐ Top Rated</Link>
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
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-3 py-1">Guitars</div>
            <Link href="/products?category=acoustic-guitars" className="block px-6 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Acoustic Guitars</Link>
            <Link href="/products?category=electric-guitars" className="block px-6 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Electric Guitars</Link>
            
            <Link href="/products?category=electric-basses" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded font-medium">Bass</Link>
            
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-3 py-1 mt-3">Keys</div>
            <Link href="/products?category=digital-pianos" className="block px-6 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Digital Pianos</Link>
            <Link href="/products?category=stage-pianos" className="block px-6 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Stage Pianos</Link>
            <Link href="/products?category=home-keyboards" className="block px-6 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Keyboards</Link>
            <Link href="/products?category=synthesizer-keyboards" className="block px-6 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Synthesizers</Link>
            <Link href="/products?category=workstations" className="block px-6 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">Workstations</Link>
            <Link href="/products?category=midi-master-keyboards" className="block px-6 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded">MIDI Controllers</Link>
            
            <Link href="/products?category=turntables" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded font-medium">DJ</Link>
            <Link href="/products?category=studio-equipment" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded font-medium">Studio</Link>
            <Link href="/products?category=accessories" className="block px-3 py-2 text-gray-900 hover:text-blue-600 hover:bg-gray-50 transition-colors text-sm rounded font-medium">Accessories</Link>
            <Link href="/top-rated" className="block px-3 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 transition-all duration-200 text-sm rounded-lg font-bold mx-2 mt-2">⭐ Top Rated</Link>
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;



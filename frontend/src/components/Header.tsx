import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/router';
import { MagnifyingGlassIcon, Bars3Icon, XMarkIcon, PlusIcon, ChevronDownIcon } from '@heroicons/react/24/outline';
import { cn } from '../lib/utils';
import InstrumentRequestForm from './InstrumentRequestForm';

const navigation = [
  { 
    name: 'Guitars', 
    icon: '',
    hasDropdown: true,
    items: [
      { name: 'Electric Guitars', href: '/products?category=electric-guitars' },
      { name: 'Acoustic Guitars', href: '/products?category=acoustic-guitars' },
    ]
  },
  { name: 'Bass', href: '/products?category=electric-basses', icon: '' },
  { 
    name: 'Keys', 
    icon: '',
    hasDropdown: true,
    items: [
      // Beginner / Home
      { name: 'Home Keyboards', href: '/products?category=home-keyboards' },
      { name: 'Entertainer Keyboards', href: '/products?category=entertainer-keyboards' },
      
      // Controllers
      { name: 'MIDI Keyboards', href: '/products?category=midi-master-keyboards' },
      
      // Piano family
      { name: 'Digital Pianos', href: '/products?category=digital-pianos' },
      { name: 'Stage Pianos', href: '/products?category=stage-pianos' },
      { name: 'Electric Pianos', href: '/products?category=electric-piano' },
      
      // Organs
      { name: 'Electric Organs', href: '/products?category=electric-organs' },
      
      // Pro / Production
      { name: 'Synthesizers', href: '/products?category=synthesizer-keyboards' },
      { name: 'Workstations', href: '/products?category=workstations' },
    ]
  },
  { name: 'DJ & Studio', href: '/products?category=turntables', icon: '' },
  { name: 'Accessories', href: '/products?category=accessories', icon: '' },
  { name: 'Blog', href: '/blog', icon: '' },
  { name: 'Top Rated', href: '/products?sort_by=rating&sort_order=desc', icon: '' },
];


export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showRequestForm, setShowRequestForm] = useState(false);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const router = useRouter();

  const isActive = (href?: string): boolean => {
    if (!href) return false;
    const path = href.split('?')[0];
    if (path === '/blog') return router.pathname.startsWith('/blog');
    if (path === '/products') {
      try {
        const url = new URL(href, 'http://localhost');
        const cat = url.searchParams.get('category');
        const sortBy = url.searchParams.get('sort_by');
        const sortOrder = url.searchParams.get('sort_order');
        if (cat) return router.pathname === '/products' && router.query.category === cat;
        if (sortBy) {
          const m = router.query.sort_by === sortBy && (!sortOrder || router.query.sort_order === sortOrder);
          return router.pathname === '/products' && m;
        }
        return router.pathname === '/products' && !router.query.category && !router.query.sort_by;
      } catch {
        return router.asPath.split('?')[0] === path;
      }
    }
    return router.asPath.split('?')[0] === path;
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/products?search=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link href="/" className="flex items-center">
              <Image 
                src="/logo.svg" 
                alt="GetYourMusicGear" 
                width={220} 
                height={40} 
                className="h-16 w-auto" 
              />
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navigation.map((item) => (
              <div key={item.name} className="relative">
                {item.hasDropdown ? (
                  <div 
                    className="relative group"
                  >
                    <button
                      className={cn(
                        'flex items-center space-x-1 text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium rounded-md transition-colors group-hover:text-blue-600 group-hover:bg-blue-50'
                      )}
                      onMouseEnter={() => setOpenDropdown(item.name)}
                    >
                      <span>{item.icon}</span>
                      <span>{item.name}</span>
                      <ChevronDownIcon className="w-4 h-4 ml-1 transition-transform group-hover:rotate-180" />
                    </button>
                    
                    <div 
                      className="absolute top-full left-0 mt-1 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200"
                      onMouseLeave={() => setOpenDropdown(null)}
                    >
                      {item.items?.map((subItem) => (
                        <Link
                          key={subItem.name}
                          href={subItem.href}
                          className="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-colors rounded-md mx-2"
                        >
                          {subItem.name}
                        </Link>
                      ))}
                    </div>
                  </div>
                ) : (
                  <Link
                    href={item.href!}
                    className={cn(
                      'flex items-center space-x-1 text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium rounded-md transition-colors',
                      isActive(item.href) && 'text-blue-600 bg-blue-50'
                    )}
                  >
                    <span>{item.icon}</span>
                    <span>{item.name}</span>
                  </Link>
                )}
              </div>
            ))}
          </nav>

          {/* Right side actions */}
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setShowRequestForm(true)}
              className="hidden sm:inline-flex btn-secondary"
            >
              <PlusIcon className="w-4 h-4 mr-2" />
              Request Instrument
            </button>
            
            {/* Mobile menu button */}
            <button
              type="button"
              className="md:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-brand-primary hover:bg-gray-100"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <span className="sr-only">Open main menu</span>
              {mobileMenuOpen ? (
                <XMarkIcon className="block h-6 w-6" />
              ) : (
                <Bars3Icon className="block h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t border-gray-200">
            {/* Mobile Search */}
            <form onSubmit={handleSearch} className="px-3 pb-3">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search instruments..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                />
                <MagnifyingGlassIcon className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
              </div>
            </form>

            {/* Mobile Navigation */}
            {navigation.map((item) => (
              <div key={item.name}>
                {item.hasDropdown ? (
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2 text-gray-700 px-3 py-2 text-base font-medium">
                      <span className="text-lg">{item.icon}</span>
                      <span>{item.name}</span>
                    </div>
                    <div className="pl-8 space-y-1">
                      {item.items?.map((subItem) => (
                        <Link
                          key={subItem.name}
                          href={subItem.href}
                          className="block text-gray-600 hover:text-brand-primary hover:bg-gray-50 px-3 py-2 text-sm rounded-md transition-colors"
                          onClick={() => setMobileMenuOpen(false)}
                        >
                          {subItem.name}
                        </Link>
                      ))}
                    </div>
                  </div>
                ) : (
                  <Link
                    href={item.href!}
                    className={cn(
                      'flex items-center space-x-2 text-gray-700 hover:text-brand-primary hover:bg-gray-50 block px-3 py-2 text-base font-medium rounded-md transition-colors',
                      isActive(item.href) && 'text-brand-primary bg-blue-50'
                    )}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <span className="text-lg">{item.icon}</span>
                    <span>{item.name}</span>
                  </Link>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Instrument Request Form */}
      <InstrumentRequestForm
        isOpen={showRequestForm}
        onClose={() => setShowRequestForm(false)}
      />
    </header>
  );
}

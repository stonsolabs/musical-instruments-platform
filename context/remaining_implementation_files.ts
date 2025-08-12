# Complete Remaining Implementation Files

## Frontend Components (Continued)

### frontend/src/components/Header.tsx
```typescript
import { useState } from 'react';
import Link from 'next/link';
import { Search, Menu, X, ShoppingCart } from 'lucide-react';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/products?q=${encodeURIComponent(searchQuery.trim())}`;
    }
  };

  return (
    <header className="bg-white shadow-sm border-b sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="bg-blue-600 text-white p-2 rounded-lg">
              <ShoppingCart className="w-6 h-6" />
            </div>
            <span className="font-bold text-xl text-gray-900">MusicEurope</span>
          </Link>

          {/* Desktop Search */}
          <div className="hidden md:flex flex-1 max-w-lg mx-8">
            <form onSubmit={handleSearch} className="w-full relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search instruments..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </form>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link href="/products" className="text-gray-700 hover:text-blue-600 font-medium">
              All Instruments
            </Link>
            <Link href="/products?category=electric-guitars" className="text-gray-700 hover:text-blue-600 font-medium">
              Guitars
            </Link>
            <Link href="/products?category=digital-keyboards" className="text-gray-700 hover:text-blue-600 font-medium">
              Keyboards
            </Link>
            <Link href="/products?category=amplifiers" className="text-gray-700 hover:text-blue-600 font-medium">
              Amplifiers
            </Link>
            <Link href="/compare" className="text-gray-700 hover:text-blue-600 font-medium">
              Compare
            </Link>
          </nav>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Search */}
        <div className="md:hidden pb-4">
          <form onSubmit={handleSearch} className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search instruments..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </form>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-t">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <Link
              href="/products"
              className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
            >
              All Instruments
            </Link>
            <Link
              href="/products?category=electric-guitars"
              className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
            >
              Guitars
            </Link>
            <Link
              href="/products?category=digital-keyboards"
              className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
            >
              Keyboards
            </Link>
            <Link
              href="/products?category=amplifiers"
              className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
            >
              Amplifiers
            </Link>
            <Link
              href="/compare"
              className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
            >
              Compare
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
```

### frontend/src/components/Footer.tsx
```typescript
import Link from 'next/link';
import { Mail, MapPin, Phone } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">MusicEurope</h3>
            <p className="text-gray-300 mb-4">
              Europe's leading musical instrument price comparison platform. 
              Find the best deals on guitars, keyboards, drums, and more.
            </p>
            <div className="flex items-center space-x-2 text-gray-300">
              <MapPin className="w-4 h-4" />
              <span>Madrid, Spain</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/products" className="text-gray-300 hover:text-white transition-colors">
                  All Instruments
                </Link>
              </li>
              <li>
                <Link href="/products?category=electric-guitars" className="text-gray-300 hover:text-white transition-colors">
                  Electric Guitars
                </Link>
              </li>
              <li>
                <Link href="/products?category=digital-keyboards" className="text-gray-300 hover:text-white transition-colors">
                  Digital Keyboards
                </Link>
              </li>
              <li>
                <Link href="/compare" className="text-gray-300 hover:text-white transition-colors">
                  Compare Products
                </Link>
              </li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Categories</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/products?category=acoustic-guitars" className="text-gray-300 hover:text-white transition-colors">
                  Acoustic Guitars
                </Link>
              </li>
              <li>
                <Link href="/products?category=synthesizers" className="text-gray-300 hover:text-white transition-colors">
                  Synthesizers
                </Link>
              </li>
              <li>
                <Link href="/products?category=amplifiers" className="text-gray-300 hover:text-white transition-colors">
                  Amplifiers
                </Link>
              </li>
              <li>
                <Link href="/products?category=audio-interfaces" className="text-gray-300 hover:text-white transition-colors">
                  Audio Interfaces
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal & Support */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/privacy" className="text-gray-300 hover:text-white transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-gray-300 hover:text-white transition-colors">
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-gray-300 hover:text-white transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-gray-300 hover:text-white transition-colors">
                  Contact
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-300 text-sm">
              © 2025 MusicEurope. All rights reserved.
            </p>
            <p className="text-gray-400 text-xs mt-2 md:mt-0">
              Affiliate disclosure: We earn commissions from qualifying purchases through our affiliate links.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
```

### frontend/src/app/products/page.tsx
```typescript
'use client';

import { useState, useEffect, useCallback } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { ProductCard } from '@/components/ProductCard';
import { SearchFilters } from '@/components/SearchFilters';
import { Pagination } from '@/components/Pagination';
import { apiClient } from '@/lib/api';
import { Product, SearchResponse } from '@/types';
import { Loader2 } from 'lucide-react';

export default function ProductsPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  const [products, setProducts] = useState<Product[]>([]);
  const [pagination, setPagination] = useState<SearchResponse['pagination']>({
    page: 1,
    limit: 20,
    total: 0,
    pages: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [compareList, setCompareList] = useState<Product[]>([]);

  // Parse current filters from URL
  const currentFilters = {
    q: searchParams.get('q') || '',
    category: searchParams.get('category') || '',
    brand: searchParams.get('brand') || '',
    min_price: searchParams.get('min_price') ? Number(searchParams.get('min_price')) : undefined,
    max_price: searchParams.get('max_price') ? Number(searchParams.get('max_price')) : undefined,
    sort_by: searchParams.get('sort_by') || 'name',
    page: searchParams.get('page') ? Number(searchParams.get('page')) : 1,
  };

  const loadProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.searchProducts(currentFilters);
      setProducts(response.products);
      setPagination(response.pagination);
    } catch (err) {
      setError('Failed to load products. Please try again.');
      console.error('Error loading products:', err);
    } finally {
      setLoading(false);
    }
  }, [currentFilters]);

  useEffect(() => {
    loadProducts();
  }, [loadProducts]);

  const handleFiltersChange = (newFilters: any) => {
    const params = new URLSearchParams();
    
    Object.entries(newFilters).forEach(([key, value]) => {
      if (value !== undefined && value !== '' && value !== null) {
        params.set(key, value.toString());
      }
    });

    router.push(`/products?${params.toString()}`);
  };

  const handlePageChange = (page: number) => {
    handleFiltersChange({ ...currentFilters, page });
  };

  const handleCompareToggle = (product: Product) => {
    const isInCompare = compareList.find(p => p.id === product.id);
    
    if (isInCompare) {
      setCompareList(prev => prev.filter(p => p.id !== product.id));
    } else if (compareList.length < 4) {
      setCompareList(prev => [...prev, product]);
    }
  };

  const handleCompareProducts = () => {
    if (compareList.length >= 2) {
      const ids = compareList.map(p => p.id).join(',');
      router.push(`/compare?ids=${ids}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Filters Sidebar */}
          <div className="lg:w-1/4">
            <SearchFilters
              filters={currentFilters}
              onFiltersChange={handleFiltersChange}
            />
          </div>

          {/* Main Content */}
          <div className="lg:w-3/4">
            {/* Results Header */}
            <div className="flex justify-between items-center mb-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Musical Instruments
                </h1>
                {!loading && (
                  <p className="text-gray-600 mt-1">
                    {pagination.total} products found
                    {currentFilters.q && ` for "${currentFilters.q}"`}
                  </p>
                )}
              </div>

              {/* Compare Button */}
              {compareList.length > 0 && (
                <div className="flex items-center gap-4">
                  <span className="text-sm text-gray-600">
                    {compareList.length} selected
                  </span>
                  <button
                    onClick={handleCompareProducts}
                    disabled={compareList.length < 2}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Compare ({compareList.length})
                  </button>
                </div>
              )}
            </div>

            {/* Loading State */}
            {loading && (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
                <span className="ml-2 text-gray-600">Loading products...</span>
              </div>
            )}

            {/* Error State */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <p className="text-red-800">{error}</p>
                <button
                  onClick={loadProducts}
                  className="mt-2 text-red-600 hover:text-red-800 font-medium"
                >
                  Try again
                </button>
              </div>
            )}

            {/* Products Grid */}
            {!loading && !error && (
              <>
                {products.length > 0 ? (
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {products.map((product) => (
                      <ProductCard
                        key={product.id}
                        product={product}
                        showCompareButton={true}
                        onCompare={handleCompareToggle}
                      />
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      No products found
                    </h3>
                    <p className="text-gray-600 mb-4">
                      Try adjusting your search criteria or filters.
                    </p>
                    <button
                      onClick={() => handleFiltersChange({ sort_by: 'name', page: 1 })}
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      Clear all filters
                    </button>
                  </div>
                )}

                {/* Pagination */}
                {pagination.pages > 1 && (
                  <Pagination
                    currentPage={pagination.page}
                    totalPages={pagination.pages}
                    onPageChange={handlePageChange}
                  />
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
```

### frontend/src/app/products/[slug]/page.tsx
```typescript
'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { Star, ExternalLink, Share2, Heart } from 'lucide-react';
import { apiClient } from '@/lib/api';
import { Product } from '@/types';
import { formatPrice, formatRating } from '@/lib/utils';

export default function ProductDetailPage() {
  const params = useParams();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadProduct = async () => {
      try {
        // Extract product ID from slug (format: name-slug-123)
        const slug = params.slug as string;
        const productId = slug.split('-').pop();
        
        if (!productId || isNaN(Number(productId))) {
          throw new Error('Invalid product ID');
        }

        const productData = await apiClient.getProduct(Number(productId));
        setProduct(productData);
      } catch (err) {
        setError('Product not found');
        console.error('Error loading product:', err);
      } finally {
        setLoading(false);
      }
    };

    loadProduct();
  }, [params.slug]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading product...</p>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Product Not Found</h1>
          <p className="text-gray-600 mb-6">The product you're looking for doesn't exist.</p>
          <Link
            href="/products"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Browse All Products
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="flex items-center space-x-2 text-sm text-gray-600 mb-8">
          <Link href="/" className="hover:text-blue-600">Home</Link>
          <span>/</span>
          <Link href="/products" className="hover:text-blue-600">Products</Link>
          <span>/</span>
          <Link href={`/products?category=${product.category.slug}`} className="hover:text-blue-600">
            {product.category.name}
          </Link>
          <span>/</span>
          <span className="text-gray-900">{product.name}</span>
        </nav>

        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="grid lg:grid-cols-2 gap-8 p-8">
            {/* Product Images */}
            <div>
              <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden mb-4">
                <Image
                  src={product.images[selectedImage] || '/placeholder-product.jpg'}
                  alt={product.name}
                  width={600}
                  height={600}
                  className="w-full h-full object-cover"
                />
              </div>
              
              {/* Image Thumbnails */}
              {product.images.length > 1 && (
                <div className="flex space-x-2 overflow-x-auto">
                  {product.images.map((image, index) => (
                    <button
                      key={index}
                      onClick={() => setSelectedImage(index)}
                      className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 ${
                        selectedImage === index ? 'border-blue-600' : 'border-gray-200'
                      }`}
                    >
                      <Image
                        src={image}
                        alt={`${product.name} ${index + 1}`}
                        width={80}
                        height={80}
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Product Info */}
            <div>
              {/* Brand and Title */}
              <div className="mb-4">
                <Link
                  href={`/products?brand=${product.brand.slug}`}
                  className="text-blue-600 hover:text-blue-800 font-medium"
                >
                  {product.brand.name}
                </Link>
                <h1 className="text-3xl font-bold text-gray-900 mt-1">{product.name}</h1>
              </div>

              {/* Rating */}
              {product.avg_rating > 0 && (
                <div className="flex items-center gap-4 mb-4">
                  <div className="flex items-center">
                    <div className="flex">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <Star
                          key={star}
                          className={`w-5 h-5 ${
                            star <= product.avg_rating
                              ? 'fill-yellow-400 text-yellow-400'
                              : 'text-gray-300'
                          }`}
                        />
                      ))}
                    </div>
                    <span className="ml-2 font-medium">{formatRating(product.avg_rating)}</span>
                  </div>
                  <span className="text-gray-600">({product.review_count} reviews)</span>
                </div>
              )}

              {/* AI Summary */}
              {product.ai_content?.summary && (
                <div className="bg-blue-50 p-4 rounded-lg mb-6">
                  <h3 className="font-semibold text-blue-900 mb-2">AI Summary</h3>
                  <p className="text-blue-800">{product.ai_content.summary}</p>
                </div>
              )}

              {/* Description */}
              {product.description && (
                <div className="mb-6">
                  <h3 className="font-semibold text-gray-900 mb-2">Description</h3>
                  <p className="text-gray-700">{product.description}</p>
                </div>
              )}

              {/* Pros and Cons */}
              {(product.ai_content?.pros?.length || product.ai_content?.cons?.length) && (
                <div className="grid md:grid-cols-2 gap-4 mb-6">
                  {product.ai_content.pros?.length > 0 && (
                    <div className="bg-green-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-green-900 mb-2">Pros</h4>
                      <ul className="text-green-800 text-sm space-y-1">
                        {product.ai_content.pros.map((pro, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-green-600 mr-2">+</span>
                            {pro}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  {product.ai_content.cons?.length > 0 && (
                    <div className="bg-red-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-red-900 mb-2">Cons</h4>
                      <ul className="text-red-800 text-sm space-y-1">
                        {product.ai_content.cons.map((con, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-red-600 mr-2">-</span>
                            {con}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Best For */}
              {product.ai_content?.best_for?.length > 0 && (
                <div className="mb-6">
                  <h3 className="font-semibold text-gray-900 mb-2">Best For</h3>
                  <div className="flex flex-wrap gap-2">
                    {product.ai_content.best_for.map((useCase, index) => (
                      <span
                        key={index}
                        className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                      >
                        {useCase}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Specifications */}
          {Object.keys(product.specifications).length > 0 && (
            <div className="border-t p-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Specifications</h3>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(product.specifications).map(([key, value]) => (
                  <div key={key} className="flex justify-between py-2 border-b border-gray-200">
                    <span className="font-medium text-gray-700">
                      {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
                    </span>
                    <span className="text-gray-900">{value}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Prices */}
          {product.prices && product.prices.length > 0 && (
            <div className="border-t p-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Where to Buy</h3>
              <div className="space-y-4">
                {product.prices.map((price, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div className="flex items-center space-x-4">
                      {price.store.logo_url && (
                        <Image
                          src={price.store.logo_url}
                          alt={price.store.name}
                          width={40}
                          height={40}
                          className="rounded"
                        />
                      )}
                      <div>
                        <h4 className="font-medium text-gray-900">{price.store.name}</h4>
                        <p className="text-sm text-gray-600">
                          Last checked: {new Date(price.last_checked).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <div className="text-2xl font-bold text-green-600">
                          {formatPrice(price.price, price.currency)}
                        </div>
                        {product.msrp_price && price.price < product.msrp_price && (
                          <div className="text-sm text-gray-500 line-through">
                            {formatPrice(product.msrp_price)}
                          </div>
                        )}
                      </div>
                      
                      <a
                        href={price.affiliate_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                      >
                        Buy Now
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </div>
                  </div>
                ))}
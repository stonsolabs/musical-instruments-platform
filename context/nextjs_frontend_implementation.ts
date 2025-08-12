// frontend/src/types/index.ts
export interface Brand {
  id: number;
  name: string;
  slug: string;
  logo_url?: string;
  description?: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  parent_id?: number;
  image_url?: string;
}

export interface ProductPrice {
  store: {
    id: number;
    name: string;
    logo_url?: string;
    website_url: string;
  };
  price: number;
  currency: string;
  affiliate_url: string;
  last_checked: string;
}

export interface Product {
  id: number;
  sku: string;
  name: string;
  slug: string;
  brand: Brand;
  category: Category;
  description?: string;
  specifications: Record<string, any>;
  images: string[];
  msrp_price?: number;
  best_price?: ProductPrice;
  prices?: ProductPrice[];
  avg_rating: number;
  review_count: number;
  ai_content?: {
    summary?: string;
    pros?: string[];
    cons?: string[];
    best_for?: string[];
    genres?: string[];
    skill_level?: string;
  };
}

export interface SearchResponse {
  products: Product[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    pages: number;
  };
  filters_applied: {
    q?: string;
    category?: string;
    brand?: string;
    min_price?: number;
    max_price?: number;
    sort_by: string;
  };
}

export interface ComparisonResponse {
  products: Product[];
  common_specs: string[];
  comparison_matrix: Record<string, Record<string, any>>;
  generated_at: string;
}

// frontend/src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Product endpoints
  async searchProducts(params: {
    q?: string;
    category?: string;
    brand?: string;
    min_price?: number;
    max_price?: number;
    sort_by?: string;
    page?: number;
    limit?: number;
  }): Promise<SearchResponse> {
    const searchParams = new URLSearchParams();
    
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        searchParams.append(key, value.toString());
      }
    });

    return this.request<SearchResponse>(`/api/products?${searchParams}`);
  }

  async getProduct(productId: number): Promise<Product> {
    return this.request<Product>(`/api/products/${productId}`);
  }

  async compareProducts(productIds: number[]): Promise<ComparisonResponse> {
    return this.request<ComparisonResponse>('/api/compare', {
      method: 'POST',
      body: JSON.stringify(productIds),
    });
  }

  // Category and brand endpoints
  async getCategories(parentId?: number): Promise<Category[]> {
    const params = parentId ? `?parent_id=${parentId}` : '';
    return this.request<Category[]>(`/api/categories${params}`);
  }

  async getBrands(category?: string): Promise<Brand[]> {
    const params = category ? `?category=${category}` : '';
    return this.request<Brand[]>(`/api/brands${params}`);
  }

  // Affiliate redirect
  getAffiliateUrl(productId: number, storeId: number): string {
    return `${this.baseURL}/api/redirect/${productId}/${storeId}`;
  }
}

export const apiClient = new ApiClient();

// frontend/src/lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPrice(price: number, currency: string = 'EUR'): string {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: currency,
  }).format(price);
}

export function formatRating(rating: number): string {
  return rating.toFixed(1);
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function generateProductUrl(product: Product): string {
  return `/products/${product.slug}-${product.id}`;
}

export function generateComparisonUrl(productIds: number[]): string {
  return `/compare?ids=${productIds.join(',')}`;
}

// frontend/src/components/ProductCard.tsx
import Image from 'next/image';
import Link from 'next/link';
import { Star, ShoppingCart } from 'lucide-react';
import { Product } from '@/types';
import { formatPrice, formatRating, generateProductUrl } from '@/lib/utils';

interface ProductCardProps {
  product: Product;
  showCompareButton?: boolean;
  onCompare?: (product: Product) => void;
}

export function ProductCard({ 
  product, 
  showCompareButton = false, 
  onCompare 
}: ProductCardProps) {
  const productUrl = generateProductUrl(product);
  const mainImage = product.images[0] || '/placeholder-product.jpg';
  
  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-4">
      {/* Product Image */}
      <Link href={productUrl} className="block mb-3">
        <div className="relative aspect-square overflow-hidden rounded-md bg-gray-100">
          <Image
            src={mainImage}
            alt={product.name}
            fill
            className="object-cover hover:scale-105 transition-transform"
          />
        </div>
      </Link>
      
      {/* Brand */}
      <p className="text-sm text-gray-600 mb-1">{product.brand.name}</p>
      
      {/* Product Name */}
      <Link href={productUrl}>
        <h3 className="font-semibold text-gray-900 mb-2 hover:text-blue-600 transition-colors line-clamp-2">
          {product.name}
        </h3>
      </Link>
      
      {/* AI Summary */}
      {product.ai_content?.summary && (
        <p className="text-sm text-gray-600 mb-3 line-clamp-2">
          {product.ai_content.summary}
        </p>
      )}
      
      {/* Rating */}
      {product.avg_rating > 0 && (
        <div className="flex items-center gap-2 mb-3">
          <div className="flex items-center">
            <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
            <span className="text-sm font-medium ml-1">
              {formatRating(product.avg_rating)}
            </span>
          </div>
          <span className="text-sm text-gray-500">
            ({product.review_count} reviews)
          </span>
        </div>
      )}
      
      {/* Price */}
      <div className="mb-4">
        {product.best_price ? (
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold text-green-600">
                {formatPrice(product.best_price.price, product.best_price.currency)}
              </span>
              {product.msrp_price && product.msrp_price > product.best_price.price && (
                <span className="text-sm text-gray-500 line-through">
                  {formatPrice(product.msrp_price)}
                </span>
              )}
            </div>
            <p className="text-xs text-gray-500">at {product.best_price.store.name}</p>
          </div>
        ) : product.msrp_price ? (
          <span className="text-lg font-bold text-gray-900">
            {formatPrice(product.msrp_price)}
          </span>
        ) : (
          <span className="text-gray-500">Price unavailable</span>
        )}
      </div>
      
      {/* Action Buttons */}
      <div className="flex gap-2">
        {product.best_price && (
          <a
            href={product.best_price.affiliate_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center justify-center gap-2 text-sm font-medium"
          >
            <ShoppingCart className="w-4 h-4" />
            Buy Now
          </a>
        )}
        
        {showCompareButton && onCompare && (
          <button
            onClick={() => onCompare(product)}
            className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors text-sm"
          >
            Compare
          </button>
        )}
      </div>
    </div>
  );
}

// frontend/src/components/SearchFilters.tsx
import { useState, useEffect } from 'react';
import { Search, Filter, X } from 'lucide-react';
import { Category, Brand } from '@/types';
import { apiClient } from '@/lib/api';

interface SearchFiltersProps {
  filters: {
    q?: string;
    category?: string;
    brand?: string;
    min_price?: number;
    max_price?: number;
    sort_by?: string;
  };
  onFiltersChange: (filters: any) => void;
}

export function SearchFilters({ filters, onFiltersChange }: SearchFiltersProps) {
  const [categories, setCategories] = useState<Category[]>([]);
  const [brands, setBrands] = useState<Brand[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // Load categories and brands
    const loadData = async () => {
      try {
        const [categoriesData, brandsData] = await Promise.all([
          apiClient.getCategories(),
          apiClient.getBrands(),
        ]);
        setCategories(categoriesData);
        setBrands(brandsData);
      } catch (error) {
        console.error('Error loading filter data:', error);
      }
    };

    loadData();
  }, []);

  const handleFilterChange = (key: string, value: any) => {
    onFiltersChange({
      ...filters,
      [key]: value,
      page: 1, // Reset to first page when filters change
    });
  };

  const clearFilters = () => {
    onFiltersChange({
      sort_by: 'name',
      page: 1,
    });
  };

  const hasActiveFilters = Object.keys(filters).some(
    key => filters[key] && key !== 'sort_by' && key !== 'page' && key !== 'limit'
  );

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border">
      {/* Mobile Filter Toggle */}
      <div className="md:hidden mb-4">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2 w-full justify-center py-2 px-4 border border-gray-300 rounded-md"
        >
          <Filter className="w-4 h-4" />
          Filters
          {hasActiveFilters && (
            <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded-full">
              {Object.keys(filters).filter(k => filters[k] && k !== 'sort_by').length}
            </span>
          )}
        </button>
      </div>

      {/* Filters Content */}
      <div className={`space-y-4 ${isOpen ? 'block' : 'hidden md:block'}`}>
        {/* Search Query */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Search
          </label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search instruments..."
              value={filters.q || ''}
              onChange={(e) => handleFilterChange('q', e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Category Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Category
          </label>
          <select
            value={filters.category || ''}
            onChange={(e) => handleFilterChange('category', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Categories</option>
            {categories.map((category) => (
              <option key={category.id} value={category.slug}>
                {category.name}
              </option>
            ))}
          </select>
        </div>

        {/* Brand Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Brand
          </label>
          <select
            value={filters.brand || ''}
            onChange={(e) => handleFilterChange('brand', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Brands</option>
            {brands.map((brand) => (
              <option key={brand.id} value={brand.slug}>
                {brand.name}
              </option>
            ))}
          </select>
        </div>

        {/* Price Range */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Price Range (€)
          </label>
          <div className="grid grid-cols-2 gap-2">
            <input
              type="number"
              placeholder="Min"
              value={filters.min_price || ''}
              onChange={(e) => handleFilterChange('min_price', e.target.value ? Number(e.target.value) : undefined)}
              className="p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="number"
              placeholder="Max"
              value={filters.max_price || ''}
              onChange={(e) => handleFilterChange('max_price', e.target.value ? Number(e.target.value) : undefined)}
              className="p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Sort By */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Sort By
          </label>
          <select
            value={filters.sort_by || 'name'}
            onChange={(e) => handleFilterChange('sort_by', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="name">Name A-Z</option>
            <option value="price">Price: Low to High</option>
            <option value="rating">Highest Rated</option>
          </select>
        </div>

        {/* Clear Filters */}
        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="w-full flex items-center justify-center gap-2 py-2 px-4 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            <X className="w-4 h-4" />
            Clear Filters
          </button>
        )}
      </div>
    </div>
  );
}

// frontend/src/components/ComparisonTable.tsx
import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { Star, ExternalLink } from 'lucide-react';
import { ComparisonResponse } from '@/types';
import { formatPrice, formatRating, generateProductUrl } from '@/lib/utils';

interface ComparisonTableProps {
  comparison: ComparisonResponse;
}

export function ComparisonTable({ comparison }: ComparisonTableProps) {
  const [selectedSpecs, setSelectedSpecs] = useState<string[]>(
    comparison.common_specs.slice(0, 8) // Show first 8 specs by default
  );

  const toggleSpec = (spec: string) => {
    setSelectedSpecs(prev =>
      prev.includes(spec)
        ? prev.filter(s => s !== spec)
        : [...prev, spec]
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header with Product Images and Names */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 p-6 bg-gray-50 border-b">
        {comparison.products.map((product) => (
          <div key={product.id} className="text-center">
            <Link href={generateProductUrl(product)}>
              <div className="relative aspect-square mb-3 overflow-hidden rounded-lg bg-white">
                <Image
                  src={product.images[0] || '/placeholder-product.jpg'}
                  alt={product.name}
                  fill
                  className="object-cover hover:scale-105 transition-transform"
                />
              </div>
            </Link>
            
            <h3 className="font-semibold text-sm mb-1">{product.brand.name}</h3>
            <Link
              href={generateProductUrl(product)}
              className="text-blue-600 hover:text-blue-800 font-medium text-sm line-clamp-2"
            >
              {product.name}
            </Link>
            
            {/* Rating */}
            {product.avg_rating > 0 && (
              <div className="flex items-center justify-center gap-1 mt-2">
                <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                <span className="text-sm">{formatRating(product.avg_rating)}</span>
              </div>
            )}
            
            {/* Price */}
            {product.best_price && (
              <div className="mt-2">
                <div className="text-lg font-bold text-green-600">
                  {formatPrice(product.best_price.price, product.best_price.currency)}
                </div>
                <div className="text-xs text-gray-500">at {product.best_price.store.name}</div>
              </div>
            )}
            
            {/* Buy Button */}
            {product.best_price && (
              <a
                href={product.best_price.affiliate_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 mt-3 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm font-medium"
              >
                Buy Now
                <ExternalLink className="w-3 h-3" />
              </a>
            )}
          </div>
        ))}
      </div>

      {/* AI Content Summary */}
      {comparison.products.some(p => p.ai_content?.summary) && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-lg mb-4">AI Analysis</h4>
          <div className="grid gap-4">
            {comparison.products.map((product) => (
              product.ai_content?.summary && (
                <div key={product.id} className="p-4 bg-gray-50 rounded-lg">
                  <h5 className="font-medium mb-2">{product.name}</h5>
                  <p className="text-gray-700 text-sm">{product.ai_content.summary}</p>
                  
                  {/* Pros and Cons */}
                  {(product.ai_content.pros?.length || product.ai_content.cons?.length) && (
                    <div className="mt-3 grid md:grid-cols-2 gap-3">
                      {product.ai_content.pros?.length > 0 && (
                        <div>
                          <h6 className="font-medium text-green-700 mb-1">Pros:</h6>
                          <ul className="text-sm text-gray-600 list-disc list-inside">
                            {product.ai_content.pros.map((pro, idx) => (
                              <li key={idx}>{pro}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {product.ai_content.cons?.length > 0 && (
                        <div>
                          <h6 className="font-medium text-red-700 mb-1">Cons:</h6>
                          <ul className="text-sm text-gray-600 list-disc list-inside">
                            {product.ai_content.cons.map((con, idx) => (
                              <li key={idx}>{con}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )
            ))}
          </div>
        </div>
      )}

      {/* Specifications Filter */}
      {comparison.common_specs.length > 0 && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-lg mb-4">Compare Specifications</h4>
          <div className="flex flex-wrap gap-2">
            {comparison.common_specs.map((spec) => (
              <button
                key={spec}
                onClick={() => toggleSpec(spec)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                  selectedSpecs.includes(spec)
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {spec.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Specifications Comparison Table */}
      {selectedSpecs.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left p-4 bg-gray-50 font-semibold">Specification</th>
                {comparison.products.map((product) => (
                  <th key={product.id} className="text-center p-4 bg-gray-50 font-semibold min-w-[200px]">
                    {product.name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {selectedSpecs.map((spec) => (
                <tr key={spec} className="border-b hover:bg-gray-50">
                  <td className="p-4 font-medium">
                    {spec.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </td>
                  {comparison.products.map((product) => (
                    <td key={product.id} className="p-4 text-center">
                      {comparison.comparison_matrix[spec]?.[product.id.toString()] || 'N/A'}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// frontend/src/components/Pagination.tsx
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export function Pagination({ currentPage, totalPages, onPageChange }: PaginationProps) {
  const getVisiblePages = () => {
    const delta = 2;
    const range = [];
    const rangeWithDots = [];

    for (let i = Math.max(2, currentPage - delta); i <= Math.min(totalPages - 1, currentPage + delta); i++) {
      range.push(i);
    }

    if (currentPage - delta > 2) {
      rangeWithDots.push(1, '...');
    } else {
      rangeWithDots.push(1);
    }

    rangeWithDots.push(...range);

    if (currentPage + delta < totalPages - 1) {
      rangeWithDots.push('...', totalPages);
    } else {
      rangeWithDots.push(totalPages);
    }

    return rangeWithDots;
  };

  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-center gap-2 mt-8">
      {/* Previous Button */}
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="flex items-center gap-1 px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <ChevronLeft className="w-4 h-4" />
        Previous
      </button>

      {/* Page Numbers */}
      <div className="flex gap-1">
        {getVisiblePages().map((page, index) => (
          <button
            key={index}
            onClick={() => typeof page === 'number' && onPageChange(page)}
            disabled={typeof page !== 'number'}
            className={`px-3 py-2 text-sm font-medium rounded-md ${
              page === currentPage
                ? 'bg-blue-600 text-white'
                : typeof page === 'number'
                ? 'text-gray-700 bg-white border border-gray-300 hover:bg-gray-50'
                : 'text-gray-400 cursor-default'
            }`}
          >
            {page}
          </button>
        ))}
      </div>

      {/* Next Button */}
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="flex items-center gap-1 px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Next
        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  );
}

// frontend/src/app/layout.tsx
import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Header } from '@/components/Header'
import { Footer } from '@/components/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Musical Instruments Europe - Compare Prices & Reviews',
  description: 'Find the best deals on musical instruments across Europe. Compare prices, read reviews, and discover your next instrument.',
  keywords: 'musical instruments, guitars, keyboards, drums, Europe, price comparison',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          <Header />
          <main className="flex-1">
            {children}
          </main>
          <Footer />
        </div>
      </body>
    </html>
  )
}

// frontend/src/app/page.tsx
import Link from 'next/link';
import { Search, TrendingUp, Award, Users } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Find Your Perfect Instrument
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100">
              Compare prices across Europe's top music stores and discover the best deals
            </p>
            
            {/* Search Bar */}
            <div className="max-w-2xl mx-auto relative">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search for guitars, keyboards, drums..."
                  className="w-full pl-12 pr-4 py-4 text-lg rounded-lg text-gray-900 border-0 focus:ring-4 focus:ring-blue-300"
                />
                <button className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors">
                  Search
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Choose Our Platform?
            </h2>
            <p className="text-xl text-gray-600">
              We make finding your next musical instrument simple and affordable
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Best Prices</h3>
              <p className="text-gray-600">Compare prices from top European music stores</p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Award className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Expert Reviews</h3>
              <p className="text-gray-600">AI-powered analysis and expert recommendations</p>
            </div>
            
            <div className="text-center">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Community</h3>
              <p className="text-gray-600">Real user reviews and ratings</p>
            </div>
            
            <div className="text-center">
              <div className="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Search className="w-8 h-8 text-orange-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Easy Search</h3>
              <p className="text-gray-600">Find exactly what you're looking for</p>
            </div>
          </div>
        </div>
      </section>

      {/* Popular Categories */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Popular Categories
            </h2>
            <p className="text-xl text-gray-600">
              Explore our most popular instrument categories
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { name: 'Electric Guitars', slug: 'electric-guitars', image: '/category-electric-guitars.jpg' },
              { name: 'Digital Keyboards', slug: 'digital-keyboards', image: '/category-keyboards.jpg' },
              { name: 'Acoustic Guitars', slug: 'acoustic-guitars', image: '/category-acoustic-guitars.jpg' },
              { name: 'Audio Equipment', slug: 'audio-equipment', image: '/category-audio.jpg' },
            ].map((category) => (
              <Link
                key={category.slug}
                href={`/products?category=${category.slug}`}
                className="group relative overflow-hidden rounded-lg bg-gray-200 aspect-square hover:shadow-lg transition-all"
              >
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                <div className="absolute bottom-4 left-4 right-4">
                  <h3 className="text-white font-semibold text-lg group-hover:text-blue-200 transition-colors">
                    {category.name}
                  </h3>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 text-white py-16">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-4">
            Ready to Find Your Next Instrument?
          </h2>
          <p className="text-xl mb-8 text-blue-100">
            Join thousands of musicians who trust us to find the best deals
          </p>
          <Link
            href="/products"
            className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
          >
            Start Shopping
          </Link>
        </div>
      </section>
    </div>
  );
} 
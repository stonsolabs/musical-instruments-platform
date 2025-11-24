import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { fetchProductAffiliateStores } from '../lib/api';
import { AffiliateStore } from '../types';

// Store configuration
interface StoreConfig {
  name: string;
  className: string;
  logo?: string;
}

const STORES_CONFIG: Record<string, StoreConfig> = {
  thomann: {
    name: 'Thomann',
    logo: '/thomann-100.png',
    className: 'bg-store-thomann hover:bg-store-thomann-dark text-white',
  },
  gear4music: {
    name: 'Gear4music', 
    logo: '/gear-100.png',
    className: 'bg-store-gear4music hover:bg-store-gear4music-dark text-white',
  },
  sweetwater: {
    name: 'Sweetwater',
    className: 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white',
  },
  guitarcenter: {
    name: 'Guitar Center',
    className: 'bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 text-white',
  },
  amazon: {
    name: 'Amazon',
    className: 'bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white',
  },
  andertons: {
    name: 'Andertons',
    className: 'bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white',
  },
  official_store: {
    name: 'Official Store',
    className: 'bg-gradient-to-r from-gray-800 to-gray-900 hover:from-gray-900 hover:to-black text-white',
  },
};

export type StoreKey = keyof typeof STORES_CONFIG;
export type ButtonVariant = 'full' | 'compact' | 'minimal' | 'icon-only';

interface Price {
  id: number;
  store: {
    name: string;
  };
  price: number;
  currency: string;
  affiliate_url: string;
  is_available: boolean;
}

interface Product {
  id: number;
  name: string;
  slug: string;
  prices?: Price[];
  content?: {
    store_links?: Record<string, string>;
  };
  thomann_info?: {
    url: string;
  };
}

interface AffiliateStoreWithUrl extends AffiliateStore {
  original_url?: string;
  affiliate_url?: string;
  priority_score?: number;
  has_store_link?: boolean;
  is_exclusive?: boolean;
  is_preferred?: boolean;
}

interface AffiliateButtonsProps {
  product: Product;
  variant?: ButtonVariant;
  maxButtons?: number;
  preferredStores?: StoreKey[];
  showPrices?: boolean;
  className?: string;
  preloadedStores?: AffiliateStoreWithUrl[];
}

export default function AffiliateButtons({
  product,
  variant = 'compact',
  maxButtons = 2,
  preferredStores = ['thomann', 'gear4music'],
  showPrices = false,
  className = '',
  preloadedStores,
}: AffiliateButtonsProps) {
  const [affiliateStores, setAffiliateStores] = useState<AffiliateStoreWithUrl[]>([]);
  const [loading, setLoading] = useState(true);
  const [isHydrated, setIsHydrated] = useState(false);
  const didFetchRef = useRef(false);

  // Simple in-memory cache to avoid duplicate network calls across mounts
  // Note: Resets on reload. Good enough to prevent quick successive calls
  // and React StrictMode double-invocation in dev.
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const cache = (globalThis as any).__AFFILIATE_STORES_CACHE__ || new Map<number, AffiliateStoreWithUrl[]>();
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (globalThis as any).__AFFILIATE_STORES_CACHE__ = cache;
  
  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (preloadedStores && preloadedStores.length > 0) {
      setAffiliateStores(preloadedStores.slice(0, maxButtons));
      setLoading(false);
      return;
    }

    const fetchAffiliateData = async () => {
      if (didFetchRef.current) return;
      didFetchRef.current = true;
      // Use cache if available
      if (cache.has(product.id)) {
        setAffiliateStores((cache.get(product.id) || []).slice(0, maxButtons));
        setLoading(false);
        return;
      }
      try {
        // Prepare store links from product content (API already has them, but we can override)
        const storeLinks: Record<string, { product_url: string }> = {};
        
        if (product.content?.store_links) {
          Object.entries(product.content.store_links).forEach(([key, url]) => {
            if (url) {
              storeLinks[key.toLowerCase()] = { product_url: url };
            }
          });
        }
        
        // Add Thomann link if available
        if (product.thomann_info?.url) {
          storeLinks.thomann = { product_url: product.thomann_info.url };
        }
        
        // Fetch affiliate stores from API - it handles priority, exclusivity, and affiliate URLs
        const response = await fetchProductAffiliateStores(product.id, storeLinks);
        const list = response.affiliate_stores.slice(0, maxButtons);
        setAffiliateStores(list);
        cache.set(product.id, list);
      } catch (error) {
        console.error('Failed to fetch affiliate stores:', error);
        // Fallback to legacy method using existing product data
        const fallback = getLegacyStoreLinks();
        setAffiliateStores(fallback);
        cache.set(product.id, fallback);
      } finally {
        setLoading(false);
      }
    };
    
    fetchAffiliateData();
  }, [product.id, maxButtons, isHydrated, preloadedStores]);
  
  // Legacy fallback method with URL normalization
  const getLegacyStoreLinks = (): AffiliateStoreWithUrl[] => {
    const storeLinks: AffiliateStoreWithUrl[] = [];
    
    // Helper function to normalize Thomann URLs
    const normalizeThomannUrl = (url: string): string => {
      if (!url || !url.includes('thomann')) return url;
      
      try {
        const urlObj = new URL(url);
        // Always use thomann.de domain for affiliate links
        urlObj.hostname = 'www.thomann.de';
        
        // Convert regional paths to /intl/
        const path = urlObj.pathname;
        const regionalPatterns = ['/gb/', '/de/', '/fr/', '/it/', '/es/', '/nl/', '/be/', '/at/', '/ch/', '/us/'];
        
        for (const pattern of regionalPatterns) {
          if (path.startsWith(pattern)) {
            urlObj.pathname = path.replace(pattern, '/intl/');
            break;
          }
        }
        
        // If it's already /intl/ or doesn't have a regional prefix, keep as is
        if (!path.startsWith('/intl/') && !regionalPatterns.some(p => path.startsWith(p))) {
          if (path === '/' || path === '') {
            urlObj.pathname = '/intl/';
          } else if (!path.startsWith('/intl/')) {
            urlObj.pathname = '/intl' + path;
          }
        }
        
        // Add affiliate parameters
        urlObj.searchParams.set('offid', '1');
        urlObj.searchParams.set('affid', '4419'); // This should come from environment or config
        
        return urlObj.toString();
      } catch (error) {
        console.warn('Failed to normalize Thomann URL:', url, error);
        return url;
      }
    };
    
    if (product.content?.store_links) {
      Object.entries(product.content.store_links).forEach(([key, url]) => {
        const storeKey = key.toLowerCase() as StoreKey;
        if (STORES_CONFIG[storeKey] && url) {
          const affiliateUrl = storeKey === 'thomann' ? normalizeThomannUrl(url) : url;
          storeLinks.push({
            id: 0,
            name: STORES_CONFIG[storeKey].name,
            slug: storeKey,
            website_url: url,
            has_affiliate_program: true,
            show_affiliate_buttons: true,
            priority: 1,
            is_active: true,
            original_url: url,
            affiliate_url: affiliateUrl,
          });
        }
      });
    }
    
    // Add Thomann link if available
    if (product.thomann_info?.url) {
      const existingThomann = storeLinks.find(link => link.slug === 'thomann');
      if (!existingThomann) {
        const affiliateUrl = normalizeThomannUrl(product.thomann_info.url);
        storeLinks.push({
          id: 0,
          name: 'Thomann',
          slug: 'thomann',
          website_url: product.thomann_info.url,
          has_affiliate_program: true,
          show_affiliate_buttons: true,
          priority: 1,
          is_active: true,
          original_url: product.thomann_info.url,
          affiliate_url: affiliateUrl,
        });
      }
    }
    
    return storeLinks.slice(0, maxButtons);
  };

  const renderButton = (store: AffiliateStoreWithUrl) => {
    const storeConfig: StoreConfig = STORES_CONFIG[store.slug as StoreKey] || {
      name: store.name,
      className: 'bg-gray-600 hover:bg-gray-700 text-white',
    };
    const url = store.affiliate_url || store.original_url || store.website_url || '#';
    const baseClasses = 'inline-flex items-center justify-center gap-3 font-semibold rounded-xl transition-all duration-200 shadow-sm hover:shadow-md transform hover:-translate-y-0.5 border-2 border-transparent focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-primary';
    const buttonClasses = `${baseClasses} ${storeConfig.className} ${className}`;

    // unified label text

    if (variant === 'minimal') {
      return (
        <a
          key={store.id}
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className={`${buttonClasses} text-xs px-3 py-2 border-2 border-transparent hover:border-white/20`}
        >
          <span className="uppercase tracking-wide text-xs">View at</span>
          {storeConfig.logo && (
            <Image src={storeConfig.logo} alt={store.name} width={28} height={28} className="w-7 h-7 object-contain" />
          )}
        </a>
      );
    }

    if (variant === 'compact') {
      return (
        <a
          key={store.id}
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className={`${buttonClasses} w-full px-4 py-3 hover:border-white/20`}
        >
          <span className="uppercase tracking-wide text-sm">View at</span>
          {storeConfig.logo && (
            <Image src={storeConfig.logo} alt={store.name} width={48} height={48} className="w-12 h-12 object-contain" />
          )}
        </a>
      );
    }

    // Full variant - Professional store button layout
    return (
      <a
        key={store.id}
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className={`${buttonClasses} w-full justify-between px-6 py-4 hover:border-white/20 group`}
      >
        <div className="flex items-center gap-3">
          {storeConfig.logo && (
            <Image src={storeConfig.logo} alt={store.name} width={56} height={56} className="w-14 h-14 object-contain" />
          )}
          <div className="flex flex-col items-start">
            <span className="uppercase tracking-wide text-sm">{storeConfig.name}</span>
            <span className="text-xs opacity-90">Check availability</span>
          </div>
        </div>
        <div className="flex items-center">
          <svg className="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </a>
    );
  };

  if (!isHydrated || loading) {
    return (
      <div className={variant === 'full' ? 'space-y-2' : 'flex gap-2'}>
        {Array.from({ length: Math.min(2, maxButtons) }).map((_, i) => (
          <div key={i} className={variant === 'full' ? 'animate-pulse bg-gray-200 h-10 w-full rounded-lg' : 'animate-pulse bg-gray-200 h-8 w-24 rounded'}></div>
        ))}
      </div>
    );
  }

  if (affiliateStores.length === 0) {
    return (
      <div className="text-sm text-gray-500">
        No store links available
      </div>
    );
  }


  return variant === 'full' ? (
    <div className="space-y-3">
      {affiliateStores.map(renderButton)}
    </div>
  ) : (
    <div className="flex gap-3 flex-wrap">
      {affiliateStores.map(renderButton)}
    </div>
  );
}

// Convenience components for different use cases
export function ProductCardButtons({ product, preloadedStores }: { product: Product; preloadedStores?: AffiliateStoreWithUrl[] }) {
  // Use vertical stacked buttons for a consistent look across the site
  return <AffiliateButtons product={product} variant="full" maxButtons={2} preloadedStores={preloadedStores} />;
}

export function ProductDetailButtons({ product, preloadedStores }: { product: Product; preloadedStores?: AffiliateStoreWithUrl[] }) {
  return <AffiliateButtons product={product} variant="full" maxButtons={4} preloadedStores={preloadedStores} />;
}

export function ComparisonButtons({ product, preloadedStores }: { product: Product; preloadedStores?: AffiliateStoreWithUrl[] }) {
  // Use the same vertical stacked style in comparison view
  return <AffiliateButtons product={product} variant="full" maxButtons={2} preloadedStores={preloadedStores} />;
}

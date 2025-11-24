import React from 'react';
import Image from 'next/image';

// Store configuration (matching main AffiliateButtons)
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

type StoreKey = keyof typeof STORES_CONFIG;
type BlogButtonVariant = 'inline' | 'featured' | 'sidebar' | 'cta';

interface BlogProduct {
  id: string;
  name: string;
  price?: string;
  affiliate_url?: string;
  rating?: number;
  thomann_info?: {
    url: string;
  };
  content?: {
    store_links?: Record<string, string>;
  };
}

interface BlogAffiliateButtonsProps {
  product: BlogProduct;
  variant?: BlogButtonVariant;
  className?: string;
  ctaText?: string;
  showRating?: boolean;
}

export default function BlogAffiliateButtons({
  product,
  variant = 'inline',
  className = '',
  ctaText,
  showRating = false
}: BlogAffiliateButtonsProps) {
  
  // Get affiliate URL with Thomann URL normalization
  const getAffiliateUrl = () => {
    // If we have a direct affiliate URL, use it
    if (product.affiliate_url) {
      return product.affiliate_url;
    }
    
    // If we have Thomann info, normalize the URL
    if (product.thomann_info?.url) {
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
      
      return normalizeThomannUrl(product.thomann_info.url);
    }
    
    // Fallback to example URL
    return `https://example.com/product/${product.id}`;
  };

  // Determine preferred store based on product or default to Thomann
  const getPreferredStore = (): StoreConfig => {
    // In real implementation, this would be smart logic based on product data
    return STORES_CONFIG.thomann;
  };

  const store = getPreferredStore();
  const url = getAffiliateUrl();

  const baseClasses = 'inline-flex items-center justify-center gap-2 font-semibold rounded-lg transition-all duration-200 shadow-sm hover:shadow-md transform hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-primary';

  // Render different variants for blog context
  const renderButton = () => {
    switch (variant) {
      case 'inline':
        // Small inline buttons within blog content
        return (
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer nofollow"
            className={`${baseClasses} ${store.className} text-sm px-4 py-2 ${className}`}
          >
            {store.logo && (
              <Image src={store.logo} alt={store.name} width={20} height={20} className="w-5 h-5 object-contain" />
            )}
            <span>{ctaText || 'Check Price'}</span>
          </a>
        );

      case 'featured':
        // Larger buttons for product spotlights
        return (
          <div className={`space-y-2 ${className}`}>
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer nofollow"
              className={`${baseClasses} ${store.className} px-6 py-3 text-base w-full`}
            >
              {store.logo && (
                <Image src={store.logo} alt={store.name} width={24} height={24} className="w-6 h-6 object-contain" />
              )}
              <span>{ctaText || 'View Product'}</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
            {showRating && product.rating && (
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <div className="flex text-yellow-400">
                  {[...Array(5)].map((_, i) => (
                    <span key={i}>
                      {i < Math.floor(product.rating!) ? '★' : '☆'}
                    </span>
                  ))}
                </div>
                <span>{product.rating}/5 rating</span>
              </div>
            )}
          </div>
        );

      case 'sidebar':
        // Compact sidebar buttons
        return (
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer nofollow"
            className={`${baseClasses} ${store.className} text-xs px-3 py-2 ${className}`}
          >
            {store.logo && (
              <Image src={store.logo} alt={store.name} width={16} height={16} className="w-4 h-4 object-contain" />
            )}
            <span className="uppercase tracking-wide">{ctaText || 'View'}</span>
          </a>
        );

      case 'cta':
        // Call-to-action style buttons
        return (
          <div className={`text-center ${className}`}>
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer nofollow"
              className={`${baseClasses} ${store.className} px-8 py-4 text-lg font-bold`}
            >
              {store.logo && (
                <Image src={store.logo} alt={store.name} width={28} height={28} className="w-7 h-7 object-contain" />
              )}
              <span>{ctaText || 'Get This Product'}</span>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </a>
            <p className="text-xs text-gray-500 mt-2">
              As an affiliate, we earn from qualifying purchases
            </p>
          </div>
        );

      default:
        return null;
    }
  };

  return renderButton();
}

// Additional component for multiple store options (when needed)
interface MultiStoreBlogButtonsProps {
  product: BlogProduct;
  stores?: string[];
  variant?: BlogButtonVariant;
  className?: string;
}

export function MultiStoreBlogButtons({
  product,
  stores = ['thomann', 'gear4music'],
  variant = 'inline',
  className = ''
}: MultiStoreBlogButtonsProps) {
  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {stores.map((storeKey) => {
        const storeConfig = STORES_CONFIG[storeKey as StoreKey];
        if (!storeConfig) return null;

        return (
          <BlogAffiliateButtons
            key={storeKey}
            product={product}
            variant={variant}
            ctaText={variant === 'sidebar' ? 'View' : `View at ${storeConfig.name}`}
          />
        );
      })}
    </div>
  );
}

// Preset button combinations for common blog scenarios
export const BlogButtonPresets = {
  ProductSpotlight: ({ product }: { product: BlogProduct }) => (
    <BlogAffiliateButtons
      product={product}
      variant="featured"
      ctaText="Check Current Price"
      showRating={true}
    />
  ),
  
  InlineRecommendation: ({ product }: { product: BlogProduct }) => (
    <BlogAffiliateButtons
      product={product}
      variant="inline"
      ctaText="View Product"
    />
  ),
  
  CallToAction: ({ product }: { product: BlogProduct }) => (
    <BlogAffiliateButtons
      product={product}
      variant="cta"
      ctaText="Get This Instrument"
    />
  ),
  
  SidebarWidget: ({ product }: { product: BlogProduct }) => (
    <BlogAffiliateButtons
      product={product}
      variant="sidebar"
      ctaText="View"
    />
  )
};
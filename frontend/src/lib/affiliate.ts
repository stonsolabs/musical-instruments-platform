import { fetchProductAffiliateStores } from './api';

type AnyProduct = {
  id: number;
  slug: string;
  content?: { store_links?: Record<string, string> };
  thomann_info?: { url?: string };
};

export function buildStoreLinks(product: AnyProduct): Record<string, { product_url: string }> {
  const storeLinks: Record<string, { product_url: string }> = {};
  const contentLinks = product?.content?.store_links || {};
  Object.entries(contentLinks).forEach(([key, url]) => {
    if (typeof url === 'string' && url) {
      storeLinks[key.toLowerCase()] = { product_url: url };
    }
  });
  const thUrl = product?.thomann_info?.url;
  if (thUrl) storeLinks['thomann'] = { product_url: thUrl };
  return storeLinks;
}

export async function resolveTopAffiliateUrl(product: AnyProduct): Promise<string | null> {
  const storeLinks = buildStoreLinks(product);
  const thUrl = product?.thomann_info?.url;
  
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
  
  try {
    const resp = await fetchProductAffiliateStores(product.id, storeLinks);
    const stores = resp?.affiliate_stores || [];
    const top = stores[0];
    const url = (top?.affiliate_url as string | undefined)
      || (top?.website_url as string | undefined)
      || (top as any)?.original_url
      || thUrl
      || null;
    return url || null;
  } catch {
    // Fallback with URL normalization for Thomann URLs
    return thUrl ? normalizeThomannUrl(thUrl) : null;
  }
}

export async function openTopAffiliate(product: AnyProduct, e?: Event | React.MouseEvent): Promise<void> {
  if (e && 'preventDefault' in e) {
    e.preventDefault();
    // @ts-ignore
    if (e.stopPropagation) e.stopPropagation();
  }
  const url = await resolveTopAffiliateUrl(product);
  if (url) {
    window.open(url, '_blank', 'noopener,noreferrer');
    return;
  }
  // Fallback to product detail
  window.location.href = `/products/${product.slug}`;
}

export async function openAffiliateForStore(
  product: AnyProduct,
  storeNameOrSlug: string,
  originalUrl?: string
): Promise<void> {
  const normalized = (storeNameOrSlug || '').toLowerCase();
  const baseLinks = buildStoreLinks(product);
  if (originalUrl) baseLinks[normalized] = { product_url: originalUrl };

  try {
    const resp = await fetchProductAffiliateStores(product.id, baseLinks);
    const stores = resp?.affiliate_stores || [];
    const match = stores.find((s) => s.slug === normalized) || stores[0];
    const url = (match?.affiliate_url as string | undefined)
      || (match?.website_url as string | undefined)
      || originalUrl;
    if (url) {
      window.open(url, '_blank', 'noopener,noreferrer');
      return;
    }
  } catch {
    // ignore
  }
  if (originalUrl) window.open(originalUrl, '_blank', 'noopener,noreferrer');
}


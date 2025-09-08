import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPrice(price: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
  }).format(price);
}

export function extractImageUrls(images: any): string[] {
  if (!images) return [];
  const urls: string[] = [];
  // If array of strings or objects
  if (Array.isArray(images)) {
    for (const it of images) {
      if (typeof it === 'string') urls.push(it);
      else if (it && typeof it === 'object' && it.url) urls.push(it.url);
    }
    return urls;
  }
  // If object map
  if (typeof images === 'object') {
    for (const key in images) {
      const imageData = images[key];
      if (typeof imageData === 'object' && imageData?.url) {
        urls.push(imageData.url);
      } else if (typeof imageData === 'string') {
        urls.push(imageData);
      }
    }
  }
  return urls;
}

export function getProductImageUrl(product: any, fallback: string = '/placeholder-product.jpg'): string {
  if (!product) return fallback;
  const urls = extractImageUrls(product.images || product.image || product.thumbnails || null);
  return urls.length > 0 ? urls[0] : fallback;
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}

export function generateSlug(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

export function getRatingStars(rating: number): { full: number; half: number; empty: number } {
  const full = Math.floor(rating);
  const decimal = rating - full;
  const half = decimal >= 0.5 ? 1 : 0;
  const empty = 5 - full - half;
  
  return { full, half, empty };
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

export function getCategoryIcon(categoryName: string): string {
  const category = categoryName.toLowerCase();
  
  if (category.includes('guitar')) return '🎸';
  if (category.includes('bass')) return '🎸';
  if (category.includes('piano') || category.includes('keyboard')) return '🎹';
  if (category.includes('drum')) return '🥁';
  if (category.includes('studio') || category.includes('monitor')) return '🎧';
  if (category.includes('accessory')) return '🎵';
  
  return '🎵';
}

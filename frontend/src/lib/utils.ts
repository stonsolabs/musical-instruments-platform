// Centralized utility functions to eliminate duplication across components

/**
 * Format price with proper currency formatting
 */
export const formatPrice = (price: number, currency: string = 'EUR'): string => {
  try {
    return new Intl.NumberFormat('en-GB', { style: 'currency', currency }).format(price);
  } catch {
    return `${currency} ${price.toFixed(2)}`;
  }
};

/**
 * Format rating to one decimal place
 */
export const formatRating = (rating: number): string => {
  return Number.isFinite(rating) ? rating.toFixed(1) : '0.0';
};

/**
 * Format price with store information
 */
export const formatPriceWithStore = (price: number, currency: string, storeName: string): string => {
  return `${formatPrice(price, currency)} at ${storeName}`;
};

import React, { useState } from 'react';
import { Product } from '../types';
import { extractImageUrls } from '../lib/utils';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline';

interface ProductGalleryProps {
  product: Product;
}

export default function ProductGallery({ product }: ProductGalleryProps) {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [isZoomed, setIsZoomed] = useState(false);
  
  const imageUrls = extractImageUrls(product.images);
  const hasImages = imageUrls.length > 0;
  const currentImage = hasImages ? imageUrls[currentImageIndex] : null;

  const nextImage = () => {
    if (hasImages) {
      setCurrentImageIndex((prev) => (prev + 1) % imageUrls.length);
    }
  };

  const previousImage = () => {
    if (hasImages) {
      setCurrentImageIndex((prev) => (prev - 1 + imageUrls.length) % imageUrls.length);
    }
  };

  const goToImage = (index: number) => {
    setCurrentImageIndex(index);
  };

  if (!hasImages) {
    return (
      <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden flex items-center justify-center">
        <div className="text-center text-gray-500">
          <div className="text-6xl mb-4">🎵</div>
          <p className="text-lg font-medium">No Image Available</p>
          <p className="text-sm">{product.name}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Main Image */}
      <div className="relative aspect-square bg-gray-100 rounded-lg overflow-hidden">
        {currentImage && (
          <img
            src={currentImage}
            alt={product.name}
            className={`w-full h-full object-cover cursor-zoom-in transition-transform duration-200 ${
              isZoomed ? 'scale-150' : ''
            }`}
            onClick={() => setIsZoomed(!isZoomed)}
          />
        )}
        
        {/* Navigation Arrows */}
        {imageUrls.length > 1 && (
          <>
            <button
              onClick={previousImage}
              className="absolute left-2 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white text-gray-800 p-2 rounded-full shadow-lg transition-all duration-200 hover:scale-110"
            >
              <ChevronLeftIcon className="w-5 h-5" />
            </button>
            <button
              onClick={nextImage}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white text-gray-800 p-2 rounded-full shadow-lg transition-all duration-200 hover:scale-110"
            >
              <ChevronRightIcon className="w-5 h-5" />
            </button>
          </>
        )}

        {/* Image Counter */}
        {imageUrls.length > 1 && (
          <div className="absolute bottom-2 right-2 bg-black/60 text-white text-xs px-2 py-1 rounded">
            {currentImageIndex + 1} / {imageUrls.length}
          </div>
        )}
      </div>

      {/* Thumbnail Navigation */}
      {imageUrls.length > 1 && (
        <div className="flex space-x-2 overflow-x-auto">
          {imageUrls.map((url, index) => (
            <button
              key={index}
              onClick={() => goToImage(index)}
              className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-all duration-200 ${
                index === currentImageIndex
                  ? 'border-brand-blue ring-2 ring-brand-blue/20'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <img
                src={url}
                alt={`${product.name} - Image ${index + 1}`}
                className="w-full h-full object-cover"
              />
            </button>
          ))}
        </div>
      )}

      {/* Zoom Instructions */}
      {hasImages && (
        <p className="text-xs text-gray-500 text-center">
          Click image to zoom in/out
        </p>
      )}
    </div>
  );
}

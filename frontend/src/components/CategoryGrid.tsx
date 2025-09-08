import React from 'react';
import Link from 'next/link';
import { Category } from '../types';
import { getCategoryIcon } from '../lib/utils';

interface CategoryGridProps {
  categories: Category[];
}

export default function CategoryGrid({ categories }: CategoryGridProps) {
  if (!categories || categories.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No categories available at the moment.</p>
      </div>
    );
  }

  // Define category colors and descriptions
  const categoryConfig: Record<string, { color: string; description: string; icon: string }> = {
    'electric-guitars': {
      color: 'from-red-500 to-pink-500',
      description: 'Electric guitars for rock, blues, jazz, and more',
      icon: '🎸'
    },
    'acoustic-guitars': {
      color: 'from-amber-500 to-orange-500',
      description: 'Acoustic guitars for folk, country, and unplugged performances',
      icon: '🎸'
    },
    'electric-basses': {
      color: 'from-blue-500 to-indigo-500',
      description: 'Electric bass guitars for rhythm and groove',
      icon: '🎸'
    },
    'acoustic-basses': {
      color: 'from-green-500 to-teal-500',
      description: 'Acoustic bass guitars for unplugged sessions',
      icon: '🎸'
    },
    'digital-pianos': {
      color: 'from-purple-500 to-pink-500',
      description: 'Digital pianos and keyboards for home and studio',
      icon: '🎹'
    },
    'acoustic-pianos': {
      color: 'from-yellow-500 to-orange-500',
      description: 'Acoustic pianos for classical and jazz performance',
      icon: '🎹'
    },
    'drums': {
      color: 'from-red-600 to-orange-600',
      description: 'Drum kits and percussion instruments',
      icon: '🥁'
    },
    'studio-monitors': {
      color: 'from-gray-600 to-blue-600',
      description: 'Studio monitors and professional audio equipment',
      icon: '🎧'
    },
    'accessories': {
      color: 'from-gray-500 to-purple-500',
      description: 'Cables, stands, cases, and other accessories',
      icon: '🎵'
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {categories.map((category) => {
        const config = categoryConfig[category.slug] || {
          color: 'from-gray-500 to-gray-600',
          description: 'Musical instruments and equipment',
          icon: '🎵'
        };

        return (
          <Link
            key={category.id}
            href={`/products?category=${category.slug}`}
            className="group block"
          >
            <div className="card hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 overflow-hidden">
              {/* Category Image or Gradient */}
              <div className={`h-48 bg-gradient-to-br ${config.color} relative overflow-hidden`}>
                {category.image_url ? (
                  <img
                    src={category.image_url}
                    alt={category.name}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <span className="text-6xl opacity-80">{config.icon}</span>
                  </div>
                )}
                
                {/* Overlay */}
                <div className="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors duration-300" />
              </div>

              {/* Category Info */}
              <div className="p-6">
                <div className="flex items-center space-x-3 mb-3">
                  <span className="text-2xl">{config.icon}</span>
                  <h3 className="text-xl font-bold text-gray-900 group-hover:text-brand-blue transition-colors">
                    {category.name}
                  </h3>
                </div>
                
                <p className="text-gray-600 mb-4 leading-relaxed">
                  {config.description}
                </p>

                {/* Explore Button */}
                <div className="flex items-center text-brand-blue font-medium group-hover:text-brand-orange transition-colors">
                  <span>Explore {category.name}</span>
                  <svg
                    className="ml-2 w-4 h-4 transform group-hover:translate-x-1 transition-transform duration-200"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </div>
              </div>
            </div>
          </Link>
        );
      })}
    </div>
  );
}

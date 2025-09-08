# GetYourMusicGear Frontend v2

A modern, responsive Next.js frontend for the GetYourMusicGear platform, built with the Pages Router and Server-Side Rendering (SSR).

## Features

- **Server-Side Rendering (SSR)** - Fast initial page loads and SEO optimization
- **Pages Router** - Next.js 14 Pages Router for stable routing
- **TypeScript** - Full type safety and better development experience
- **Tailwind CSS** - Utility-first CSS framework with custom design system
- **Responsive Design** - Mobile-first approach with modern UI components
- **Product Comparison** - Side-by-side comparison of musical instruments
- **Advanced Filtering** - Category, brand, price, and search filters
- **Product Gallery** - Image galleries with zoom and navigation
- **Specifications Display** - Dynamic specification tables based on product category
- **Affiliate Integration** - Store links and pricing information
- **Performance Optimized** - Image optimization, lazy loading, and efficient data fetching

## Tech Stack

- **Framework**: Next.js 14 (Pages Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Heroicons
- **State Management**: React Hooks
- **Data Fetching**: Server-Side Props (SSR)
- **UI Components**: Custom component library
- **Forms**: React Hook Form
- **Animations**: Framer Motion

## Project Structure

```
frontend_v2/
├── pages/                 # Next.js pages (SSR enabled)
│   ├── index.tsx         # Homepage
│   ├── products.tsx      # Products listing
│   ├── products/[slug].tsx # Product detail
│   ├── compare.tsx       # Product comparison
│   └── _app.tsx          # App wrapper
├── src/
│   ├── components/       # Reusable UI components
│   ├── lib/             # Utilities and API functions
│   ├── types/           # TypeScript type definitions
│   └── styles/          # Global styles and Tailwind config
├── public/              # Static assets
└── package.json         # Dependencies and scripts
```

## Key Components

### Core Components
- **Layout** - Main layout with header and footer
- **Header** - Navigation, search, and mobile menu
- **Footer** - Links, company info, and social media
- **ProductCard** - Product display card with ratings and pricing
- **ProductGrid** - Responsive grid layout for products

### Product Components
- **ProductGallery** - Image gallery with zoom and navigation
- **ProductInfo** - Product details, ratings, and description
- **ProductSpecifications** - Dynamic specification tables
- **ProductPrices** - Store pricing and affiliate links
- **ProductReviews** - Customer reviews and ratings

### Comparison Components
- **CompareSearch** - Product search for comparison
- **ComparisonTable** - Side-by-side comparison table
- **ComparisonGrid** - Grid view for product comparison

### Utility Components
- **ProductFilters** - Category, brand, and price filters
- **ProductSort** - Sorting options for product lists
- **Pagination** - Page navigation for large datasets
- **SearchBar** - Global search functionality

## Getting Started

### Prerequisites
- Node.js 18.18.0 or higher
- npm 9.0.0 or higher

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   Create a `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Build and Production

1. **Build for production**:
   ```bash
   npm run build
   ```

2. **Start production server**:
   ```bash
   npm start
   ```

## API Integration

The frontend integrates with the backend API endpoints:

- **Products**: `/api/products` - Product listing and search
- **Product Detail**: `/api/products/{slug}` - Individual product data
- **Comparison**: `/api/compare` - Product comparison data
- **Categories**: `/api/categories` - Product categories
- **Brands**: `/api/brands` - Product brands
- **Trending**: `/api/trending` - Trending products
- **Search**: `/api/search` - Product search functionality

## Design System

### Colors
- **Primary**: Blue palette (`brand-blue`, `brand-blue-light`)
- **Accent**: Orange palette (`brand-orange`, `brand-orange-light`)
- **Neutral**: Gray scale for text and backgrounds

### Typography
- **Headings**: Poppins font family
- **Body**: Inter font family
- **Responsive**: Mobile-first typography scaling

### Components
- **Buttons**: Primary, secondary, and accent variants
- **Cards**: Consistent card design with shadows and borders
- **Forms**: Styled form inputs and controls
- **Badges**: Status and category indicators

## Performance Features

- **SSR**: Server-side rendering for fast initial loads
- **Image Optimization**: Next.js Image component with lazy loading
- **Code Splitting**: Automatic code splitting by routes
- **Bundle Analysis**: Built-in bundle analyzer
- **Caching**: Efficient data fetching and caching strategies

## SEO Features

- **Meta Tags**: Dynamic meta titles and descriptions
- **Open Graph**: Social media sharing optimization
- **Structured Data**: Product schema markup
- **Sitemap**: Automatic sitemap generation
- **Robots.txt**: Search engine crawling configuration

## Responsive Design

- **Mobile First**: Mobile-optimized design approach
- **Breakpoints**: Tailwind CSS responsive breakpoints
- **Touch Friendly**: Mobile-optimized interactions
- **Performance**: Optimized for mobile devices

## Browser Support

- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **Mobile**: iOS Safari, Chrome Mobile
- **Fallbacks**: Graceful degradation for older browsers

## Development Guidelines

### Code Style
- **TypeScript**: Strict type checking enabled
- **ESLint**: Code quality and consistency
- **Prettier**: Code formatting
- **Components**: Functional components with hooks

### File Naming
- **Components**: PascalCase (e.g., `ProductCard.tsx`)
- **Pages**: kebab-case (e.g., `product-detail.tsx`)
- **Utilities**: camelCase (e.g., `formatPrice.ts`)

### Component Structure
```tsx
import React from 'react';
import { ComponentProps } from '@/types';

interface ComponentProps {
  // Props interface
}

export default function Component({ prop1, prop2 }: ComponentProps) {
  // Component logic
  
  return (
    // JSX
  );
}
```

## Testing

### Type Checking
```bash
npm run type-check
```

### Linting
```bash
npm run lint
```

### Build Testing
```bash
npm run build
```

## Deployment

### Vercel (Recommended)
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically on push

### Other Platforms
- **Netlify**: Static site deployment
- **AWS**: S3 + CloudFront
- **Docker**: Containerized deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is proprietary software. All rights reserved.

## Support

For technical support or questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## Changelog

### v2.0.0
- Complete rewrite with Next.js 14
- SSR implementation for all pages
- Modern component architecture
- Improved performance and SEO
- Enhanced user experience
- Mobile-first responsive design

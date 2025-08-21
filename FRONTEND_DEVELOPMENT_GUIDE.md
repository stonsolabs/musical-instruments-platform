# Frontend Development Guide

This document explains where to make changes for different pages and how API calls work in the musical instruments platform frontend.

## Table of Contents
1. [Page Structure Overview](#page-structure-overview)
2. [Where to Update Specific Pages](#where-to-update-specific-pages)
3. [API Call System](#api-call-system)
4. [Component Architecture](#component-architecture)
5. [Common Development Tasks](#common-development-tasks)

## Page Structure Overview

The frontend uses Next.js 13+ with the App Router. Here's the structure:

```
frontend/src/app/
├── layout.tsx                    # Root layout (Header, Footer, Analytics)
├── page.tsx                     # Home page (/)
├── globals.css                  # Global styles
├── about/                       # About page (/about)
├── affiliate-disclosure/        # Affiliate disclosure page
├── blog/                        # Blog pages (/blog, /blog/[slug])
├── compare/                     # Compare page (/compare)
├── contact/                     # Contact page
├── deals/                       # Deals page
├── products/                    # Products pages (/products, /products/[slug])
├── privacy-policy/              # Privacy policy page
├── terms-of-service/            # Terms of service page
└── api/                         # API routes (proxy to backend)
```

## Where to Update Specific Pages

### 🏠 Home Page (`/`)
**File:** `frontend/src/app/page.tsx`

**What to change:**
- Hero section content and styling
- Popular products section
- Top-rated products section
- Blog section
- Newsletter signup
- Ad banners and promotional content

**Key sections:**
- Hero section with search interface (lines 95-150)
- Popular instruments section (lines 180-250)
- Top-rated instruments section (lines 350-420)
- Blog section (lines 450-520)
- Newsletter section (lines 530-550)

### 🔍 Products Page (`/products`)
**File:** `frontend/src/app/products/page.tsx`

**What to change:**
- Page title and description
- Breadcrumb navigation
- Product grid layout
- Filtering and sorting options

**Client Component:** `frontend/src/app/products/ProductsClient.tsx`
- Interactive product grid
- Filter sidebar
- Pagination
- Search functionality

### 📄 Individual Product Page (`/products/[slug]`)
**File:** `frontend/src/app/products/[slug]/page.tsx`

**What to change:**
- Product image gallery
- Product information layout
- Store availability section
- Product actions (Compare, Add to List, etc.)

**Component:** `frontend/src/components/ComprehensiveProductDetails.tsx`
- Detailed product specifications
- Reviews and ratings
- Related products

### 📂 Category Pages (`/products?category=...`)
**File:** `frontend/src/app/products/page.tsx` (with category filter)

**What to change:**
- Category-specific page titles and descriptions
- Category breadcrumb navigation
- Category-specific product filtering
- Category description and metadata

**URL Examples:**
- `/products?category=electric-guitars`
- `/products?category=acoustic-guitars`
- `/products?category=pianos-keyboards`
- `/products?category=drums-percussion`

**Key Features:**
- Dynamic page titles based on category
- SEO-optimized category descriptions
- Category-specific product counts
- Filtered product listings

**Client Component:** `frontend/src/app/products/ProductsClient.tsx`
- Category-specific filtering logic
- Category breadcrumb updates
- Category-based sorting options

**Floating Compare Button:**
- **Component:** `frontend/src/components/FloatingCompareButton.tsx`
- **Location:** Fixed position at bottom-right of screen
- **Functionality:** 
  - Appears when users select products for comparison
  - Shows count of selected products
  - Navigates to compare page with selected products
  - Only visible when at least 1 product is selected
- **Integration:** Used in ProductsClient component for category pages

### ⚖️ Compare Page (`/compare`)
**File:** `frontend/src/app/compare/page.tsx`

**What to change:**
- Compare interface layout
- Product selection interface
- Empty state design

**Client Component:** `frontend/src/app/compare/CompareClient.tsx`
- Comparison table
- Product selection logic
- Dynamic comparison features

### 📝 Blog Pages
**Main Blog:** `frontend/src/app/blog/page.tsx`
**Individual Blog Post:** `frontend/src/app/blog/[slug]/page.tsx`

**What to change:**
- Blog post layout
- Article content structure
- Related posts section

### 📞 Contact Page
**File:** `frontend/src/app/contact/page.tsx`

**What to change:**
- Contact form
- Contact information
- Office locations

### 💰 Deals Page
**File:** `frontend/src/app/deals/page.tsx`

**What to change:**
- Deals grid layout
- Deal filtering
- Promotional content

### ℹ️ About Page
**File:** `frontend/src/app/about/page.tsx`

**What to change:**
- Company information
- Team details
- Mission statement

### 📋 Legal Pages
- **Privacy Policy:** `frontend/src/app/privacy-policy/page.tsx`
- **Terms of Service:** `frontend/src/app/terms-of-service/page.tsx`
- **Affiliate Disclosure:** `frontend/src/app/affiliate-disclosure/page.tsx`

## API Call System

### How API Calls Work

The frontend uses a proxy system to communicate with the backend API:

1. **Frontend → Next.js API Route → Backend**
   - Frontend makes calls to `/api/proxy/*`
   - Next.js API routes forward requests to the backend
   - Backend processes requests and returns data

### API Configuration

**File:** `frontend/src/lib/api.ts`

```typescript
// API base URL configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// API client for making requests
export const apiClient = {
  async get(endpoint: string) { /* ... */ },
  async post(endpoint: string, data?: any) { /* ... */ },
  // ... other methods
};
```

### Proxy Route

**File:** `frontend/src/app/api/proxy/[...path]/route.ts`

This file handles all API requests by:
1. Receiving requests from frontend
2. Adding API key authentication
3. Forwarding to backend
4. Returning responses to frontend

### Common API Endpoints

| Endpoint | Purpose | Used In |
|----------|---------|---------|
| `/api/proxy/products` | Get products list | Home page, Products page |
| `/api/proxy/products/{id}` | Get single product | Product detail page |
| `/api/proxy/search/autocomplete` | Search suggestions | Search components |
| `/api/proxy/categories` | Get categories | Products page filters |
| `/api/proxy/brands` | Get brands | Products page filters |
| `/api/proxy/compare` | Compare products | Compare page |

### Making API Calls

**Example from Home Page:**
```typescript
async function searchProducts(params: any): Promise<{ products: Product[] }> {
  const response = await fetch(`/api/proxy/products?${sp.toString()}`);
  return await response.json();
}
```

**Example from Product Search:**
```typescript
const response = await fetch(`/api/proxy/search/autocomplete?q=${query}&limit=${limit}`);
```

## Component Architecture

### Core Components

**Header:** `frontend/src/components/Header.tsx`
- Navigation menu
- Logo
- Mobile menu

**Footer:** `frontend/src/components/Footer.tsx`
- Site links
- Social media
- Legal links

**ProductSearchAutocomplete:** `frontend/src/components/ProductSearchAutocomplete.tsx`
- Search input with autocomplete
- Product suggestions
- Store availability

**FloatingCompareButton:** `frontend/src/components/FloatingCompareButton.tsx`
- Floating compare button for product selection
- Fixed positioning at bottom-right
- Dynamic visibility based on selection count
- Navigation to compare page

**AffiliateButton:** `frontend/src/components/AffiliateButton.tsx`
- Affiliate link handling
- Store-specific styling

**ComprehensiveProductDetails:** `frontend/src/components/ComprehensiveProductDetails.tsx`
- Detailed product information
- Specifications table
- Reviews section

### Layout Components

**Root Layout:** `frontend/src/app/layout.tsx`
- Global layout structure
- Header and Footer
- Analytics setup
- Global styles

## Common Development Tasks

### Adding a New Page

1. Create a new directory in `frontend/src/app/`
2. Add `page.tsx` file
3. Update navigation in `Header.tsx` if needed
4. Add to sitemap if required

### Modifying Search Functionality

1. **Search Input:** `frontend/src/components/ProductSearchAutocomplete.tsx`
2. **Search Results:** `frontend/src/app/products/page.tsx`
3. **API Endpoint:** `/api/proxy/search/autocomplete`

### Modifying Category Pages

1. **Category Filtering:** `frontend/src/app/products/page.tsx`
2. **Category Navigation:** `frontend/src/components/Header.tsx`
3. **Category Data:** `/api/proxy/categories`
4. **Category-specific Styling:** Update CSS classes for category pages
5. **Floating Compare Button:** `frontend/src/components/FloatingCompareButton.tsx`
   - Modify button styling and positioning
   - Change selection behavior
   - Update compare navigation logic

### Updating Product Display

1. **Product Grid:** `frontend/src/app/products/ProductsClient.tsx`
2. **Product Cards:** Individual product components
3. **Product Details:** `frontend/src/components/ComprehensiveProductDetails.tsx`

### Changing Navigation

**File:** `frontend/src/components/Header.tsx`

Update the navigation links in both desktop and mobile menus.

### Modifying API Calls

1. **Add new endpoint:** Update `frontend/src/lib/api.ts`
2. **Modify existing calls:** Find the component making the call
3. **Update proxy:** Modify `frontend/src/app/api/proxy/[...path]/route.ts` if needed

### Styling Changes

1. **Global styles:** `frontend/src/app/globals.css`
2. **Component styles:** Inline Tailwind classes in component files
3. **Tailwind config:** `frontend/tailwind.config.js`

### Environment Variables

**Development:** `.env.local`
**Production:** Vercel environment variables

Key variables:
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL
- `API_KEY`: Backend API key
- `NEXT_PUBLIC_GTM_ID`: Google Tag Manager ID

## File Locations Summary

| Page/Feature | File Location |
|--------------|---------------|
| Home page | `frontend/src/app/page.tsx` |
| Products listing | `frontend/src/app/products/page.tsx` |
| Category pages | `frontend/src/app/products/page.tsx` (with category filter) |
| Product details | `frontend/src/app/products/[slug]/page.tsx` |
| Compare page | `frontend/src/app/compare/page.tsx` |
| Blog | `frontend/src/app/blog/page.tsx` |
| Search functionality | `frontend/src/components/ProductSearchAutocomplete.tsx` |
| Floating compare button | `frontend/src/components/FloatingCompareButton.tsx` |
| Navigation | `frontend/src/components/Header.tsx` |
| API calls | `frontend/src/lib/api.ts` |
| API proxy | `frontend/src/app/api/proxy/[...path]/route.ts` |
| Global layout | `frontend/src/app/layout.tsx` |
| Global styles | `frontend/src/app/globals.css` |

## Development Workflow

1. **Make changes** to the appropriate file
2. **Test locally** with `npm run dev`
3. **Check API calls** in browser developer tools
4. **Verify styling** across different screen sizes
5. **Test functionality** with real data
6. **Deploy** to Vercel for production testing

## Troubleshooting

### API Call Issues
- Check `frontend/src/app/api/proxy/[...path]/route.ts` logs
- Verify environment variables are set
- Ensure backend is running and accessible

### Styling Issues
- Check Tailwind classes are correct
- Verify responsive breakpoints
- Test in different browsers

### Component Issues
- Check component props and types
- Verify data flow from parent to child
- Check for missing dependencies

This guide should help you navigate the frontend codebase and make changes efficiently!

## 🖼️ Product Image Management System (Future Implementation)

### Current State
Currently, product images are stored as URLs in the product data and displayed using basic `<img>` tags. This approach has limitations:
- No image optimization
- No responsive images
- No fallback handling
- No CDN integration
- Limited image formats support

### Recommended Implementation Strategy

#### 1. Image Storage Architecture

**Option A: Cloud Storage with CDN**
```
Product Images → Cloud Storage (AWS S3/Cloudinary) → CDN → Frontend
```

**Option B: Next.js Image Optimization**
```
Product Images → Next.js Image Component → Automatic Optimization → CDN
```

#### 2. Implementation Plan

**Phase 1: Backend Image Management**
- **File:** `backend/app/services/image_service.py`
- **Features:**
  - Image upload handling
  - Multiple image formats support (WebP, AVIF, JPEG)
  - Image resizing and optimization
  - Thumbnail generation
  - Image metadata storage

**Phase 2: Database Schema Updates**
- **File:** `backend/app/models.py`
```python
class ProductImage(Base):
    __tablename__ = "product_images"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    image_url = Column(String)
    thumbnail_url = Column(String)
    alt_text = Column(String)
    is_primary = Column(Boolean, default=False)
    order_index = Column(Integer, default=0)
    image_format = Column(String)  # webp, jpeg, avif
    file_size = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Phase 3: Frontend Image Components**

**File:** `frontend/src/components/ProductImageGallery.tsx`
```typescript
interface ProductImageGalleryProps {
  images: ProductImage[];
  productName: string;
  onImageSelect?: (index: number) => void;
  selectedIndex?: number;
}

export default function ProductImageGallery({
  images,
  productName,
  onImageSelect,
  selectedIndex = 0
}: ProductImageGalleryProps) {
  return (
    <div className="space-y-4">
      {/* Main Image */}
      <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
        <Image
          src={images[selectedIndex]?.image_url || '/placeholder-product.jpg'}
          alt={`${productName} - Image ${selectedIndex + 1}`}
          width={600}
          height={600}
          className="w-full h-full object-cover"
          priority={selectedIndex === 0}
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          placeholder="blur"
          blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
        />
      </div>
      
      {/* Thumbnail Gallery */}
      {images.length > 1 && (
        <div className="flex gap-2 overflow-x-auto">
          {images.map((image, index) => (
            <button
              key={image.id}
              onClick={() => onImageSelect?.(index)}
              className={`w-16 h-16 rounded border-2 flex-shrink-0 overflow-hidden transition-colors ${
                index === selectedIndex ? 'border-blue-600' : 'border-gray-200'
              }`}
            >
              <Image
                src={image.thumbnail_url || image.image_url}
                alt={`${productName} thumbnail ${index + 1}`}
                width={64}
                height={64}
                className="w-full h-full object-cover"
                sizes="64px"
              />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
```

**File:** `frontend/src/components/OptimizedProductImage.tsx`
```typescript
interface OptimizedProductImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
  priority?: boolean;
  sizes?: string;
}

export default function OptimizedProductImage({
  src,
  alt,
  width = 400,
  height = 400,
  className = "",
  priority = false,
  sizes = "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
}: OptimizedProductImageProps) {
  return (
    <Image
      src={src}
      alt={alt}
      width={width}
      height={height}
      className={className}
      priority={priority}
      sizes={sizes}
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
      onError={(e) => {
        // Fallback to placeholder image
        const target = e.target as HTMLImageElement;
        target.src = '/placeholder-product.jpg';
      }}
    />
  );
}
```

#### 3. Image Optimization Features

**Responsive Images:**
- Generate multiple sizes (thumbnail, small, medium, large)
- Use `srcset` and `sizes` attributes
- WebP and AVIF format support

**Performance Optimizations:**
- Lazy loading for images below the fold
- Progressive image loading
- Blur placeholder while loading
- Image compression and optimization

**Error Handling:**
- Fallback images for broken links
- Retry mechanisms for failed loads
- Graceful degradation

#### 4. Integration Points

**Update Product Detail Page:**
- **File:** `frontend/src/app/products/[slug]/page.tsx`
- Replace current image handling with new components

**Update Product Cards:**
- **File:** `frontend/src/app/products/ProductsClient.tsx`
- Use optimized images in product grid

**Update Search Results:**
- **File:** `frontend/src/components/ProductSearchAutocomplete.tsx`
- Optimize images in search suggestions

#### 5. Environment Configuration

**Add to `.env.local`:**
```bash
# Image optimization
NEXT_PUBLIC_IMAGE_DOMAIN=your-cdn-domain.com
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=your-cloud-name
NEXT_PUBLIC_IMAGE_OPTIMIZATION_ENABLED=true
```

**Update `next.config.js`:**
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['your-cdn-domain.com', 'res.cloudinary.com'],
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
  // ... other config
}
```

#### 6. Migration Strategy

**Step 1: Backend Updates**
1. Create new image service
2. Update database schema
3. Create migration scripts
4. Update API endpoints

**Step 2: Frontend Components**
1. Create new image components
2. Update existing pages gradually
3. Test performance improvements
4. Monitor error rates

**Step 3: Content Migration**
1. Upload existing images to new storage
2. Update database records
3. Verify all images load correctly
4. Remove old image handling

#### 7. Monitoring and Analytics

**Track Image Performance:**
- Load times
- Error rates
- Format adoption (WebP vs JPEG)
- CDN performance

**Tools to Consider:**
- Cloudinary for image management
- AWS S3 + CloudFront for storage/CDN
- Next.js Image component for optimization
- Web Vitals for performance monitoring

This robust image system will significantly improve user experience, page load times, and SEO performance while providing better error handling and optimization.
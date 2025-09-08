import { GetServerSideProps } from 'next';
import Head from 'next/head';
// import Link from 'next/link';
import { TrendingProduct, Category, Product } from '../src/types';
import { fetchTrendingProducts, fetchCategories, fetchProducts } from '../src/lib/api';
import HeroSection from '../src/components/HeroSection';
import TrendingProducts from '../src/components/TrendingProducts';
// import SpecialOffers from '../src/components/SpecialOffers';
import FeaturedComparisons from '../src/components/FeaturedComparisons';

interface HomePageProps {
  trendingProducts: TrendingProduct[];
  categories: Category[];
  featuredComparisons: Array<{
    id: string;
    title: string;
    description: string;
    category: string;
    product1: Product;
    product2: Product;
  }>;
}

export default function HomePage({ trendingProducts, categories, featuredComparisons }: HomePageProps) {
  return (
    <>
      <Head>
        <title>GetYourMusicGear - Find Your Perfect Musical Instrument</title>
        <meta name="description" content="Expert Reviews, Detailed Comparisons, and Trusted Recommendations for Musical Instruments. Compare guitars, basses, pianos, and more from top retailers worldwide." />
        <meta name="keywords" content="musical instruments, guitar comparison, bass guitar, digital piano, music gear reviews" />
        <meta property="og:title" content="GetYourMusicGear - Find Your Perfect Musical Instrument" />
        <meta property="og:description" content="Expert Reviews, Detailed Comparisons, and Trusted Recommendations for Musical Instruments" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://getyourmusicgear.com" />
      </Head>

        <div className="min-h-screen">
        {/* Hero Section */}
        <HeroSection />

        {/* Featured Comparisons */}
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="font-display text-3xl font-bold text-gray-900 mb-4 uppercase tracking-wide">
                Popular Instrument Comparisons
              </h2>
            </div>
            <FeaturedComparisons comparisons={featuredComparisons} />
          </div>
        </section>

        {/* Trending Products */}
        <section className="py-16 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="font-display text-3xl font-bold text-gray-900 mb-4 uppercase tracking-wide">
                Trending Musical Instruments
              </h2>
              {/* <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Discover the most popular and highly-rated instruments that musicians are loving right now
              </p> */}
            </div>
            <TrendingProducts products={trendingProducts} />
          </div>
        </section>

        {/* Special Offers */}
        {/* <section className="py-16 bg-gradient-to-r from-brand-blue to-brand-orange">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <SpecialOffers />
          </div>
        </section> */}

        {/* CTA Section */}
        {/* <section className="py-16 bg-gray-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">
              Ready to Find Your Perfect Instrument?
            </h2>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Start comparing instruments, reading expert reviews, and making informed decisions today
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/products" className="btn-accent text-lg px-8 py-3">
                Browse All Products
              </Link>
              <Link href="/compare" className="btn-secondary text-lg px-8 py-3">
                Compare Instruments
              </Link>
            </div>
          </div>
        </section> */}
      </div>
    </>
  );
}

export const getServerSideProps: GetServerSideProps = async () => {
  try {
    const [trendingProducts, categories] = await Promise.all([
      fetchTrendingProducts(4),
      fetchCategories(),
    ]);

    // Helper function to check if product has images
    const hasImages = (p: any): boolean => {
      return Array.isArray(p?.images) && p.images.length > 0 && p.images.some((img: any) => {
        if (typeof img === 'string') return img.trim().length > 0;
        if (typeof img === 'object' && img !== null) return img.url && img.url.trim().length > 0;
        return false;
      });
    };

    // Helper function to create featured comparison from products with images
    const createComparison = (products: any[], id: string, category: string, description: string) => {
      const productsWithImages = products.filter(hasImages);
      if (productsWithImages.length >= 2) {
        return {
          id,
          title: `${productsWithImages[0].name} vs ${productsWithImages[1].name}`,
          description,
          category,
          product1: productsWithImages[0],
          product2: productsWithImages[1],
        };
      }
      return null;
    };

    // Create featured comparisons from popular products - only with images
    const featuredComparisons = [];
    try {
      // Get guitars for comparison (fetch more to have better selection after filtering)
      const guitarResults = await fetchProducts({ category: 'electric-guitars', per_page: 6, sort_by: 'rating', sort_order: 'desc' });
      const guitarComparison = createComparison(
        guitarResults.products,
        'guitars-1',
        'Electric Guitars',
        'Compare two highly-rated electric guitars perfect for players at any level'
      );
      if (guitarComparison) featuredComparisons.push(guitarComparison);

      // Get pianos for comparison
      const pianoResults = await fetchProducts({ category: 'digital-pianos', per_page: 6, sort_by: 'rating', sort_order: 'desc' });
      const pianoComparison = createComparison(
        pianoResults.products,
        'pianos-1',
        'Digital Pianos',
        'Find the perfect digital piano for your home studio or practice space'
      );
      if (pianoComparison) featuredComparisons.push(pianoComparison);

      // Get acoustic guitars for comparison
      const acousticResults = await fetchProducts({ category: 'acoustic-guitars', per_page: 6, sort_by: 'rating', sort_order: 'desc' });
      const acousticComparison = createComparison(
        acousticResults.products,
        'acoustic-1',
        'Acoustic Guitars',
        'Discover the differences between these premium acoustic guitars'
      );
      if (acousticComparison) featuredComparisons.push(acousticComparison);
    } catch (error) {
      console.error('Error fetching comparison data:', error);
    }

    // Slim down payloads to reduce page data size and avoid undefined serialization
    const slimProduct = (p: any): any => {
      const base: any = {
        id: p.id,
        name: p.name,
        slug: p.slug,
        brand: p?.brand ? { id: p.brand.id, name: p.brand.name, slug: p.brand.slug } : null,
        category: p?.category ? { id: p.category.id, name: p.category.name, slug: p.category.slug } : null,
        review_count: p?.review_count ?? 0,
        is_active: p?.is_active ?? true,
        created_at: p?.created_at ?? null,
        updated_at: p?.updated_at ?? null,
      };
      base.sku = p?.sku ?? null;
      if (Array.isArray(p?.images)) {
        // keep only first image to shrink payload
        base.images = p.images.slice(0, 1);
      }
      if (p?.avg_rating != null) base.avg_rating = p.avg_rating;
      if (p?.vote_stats != null) base.vote_stats = p.vote_stats;
      if (p?.thomann_info?.url) base.thomann_info = { url: p.thomann_info.url };
      return base;
    };

    // Filter and map trending products - only include products with images
    const slimTrending: TrendingProduct[] = (trendingProducts || [])
      .filter((tp: any) => hasImages(tp.product || tp))
      .map((tp: any) => ({
        product: slimProduct(tp.product || tp),
        trending_score: tp.trending_score ?? 0,
        price_change: tp.price_change,
        popularity_increase: tp.popularity_increase,
      }));

    // Filter and map featured comparisons - only include comparisons where both products have images
    const slimComparisons = (featuredComparisons || [])
      .filter(fc => hasImages(fc.product1) && hasImages(fc.product2))
      .map(fc => ({
        ...fc,
        product1: slimProduct(fc.product1),
        product2: slimProduct(fc.product2),
      }));

    // counts logged during development removed for production cleanliness

    return {
      props: {
        trendingProducts: slimTrending,
        categories: (categories || []).filter(cat => cat.is_active).map(c => ({
          id: c.id,
          name: c.name,
          slug: c.slug,
          parent_id: c.parent_id,
          is_active: c.is_active,
        })),
        featuredComparisons: slimComparisons,
      },
    };
  } catch (error) {
    console.error('Error fetching homepage data:', error);
    
    return {
      props: {
        trendingProducts: [],
        categories: [],
        featuredComparisons: [],
      },
    };
  }
};

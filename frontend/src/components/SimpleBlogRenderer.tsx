import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import BlogAffiliateButtons from './BlogAffiliateButtons';
import BlogProductSpotlight from './BlogProductSpotlight';

interface SimpleBlogRendererProps {
  content: any;
  className?: string;
  hydrate?: Record<string, Partial<Product>>; // map by product_id as string
  fallbackProducts?: Partial<Product>[]; // from post.products when spotlight JSON is wrong
}

interface Product {
  id: string;
  name: string;
  price: string;
  reason?: string;
  rating?: number;
  pros?: string[];
  cons?: string[];
  affiliate_url: string;
  store_url?: string;
  cta_text?: string;
  slug?: string;
  image_url?: string;
}

interface Section {
  type: string;
  title?: string;
  content?: string;
  products?: Product[];
  product?: Product;
}

const SimpleBlogRenderer: React.FC<SimpleBlogRendererProps> = ({ content, className = '', hydrate = {}, fallbackProducts = [] }) => {
  if (!content?.sections) {
    // Fallback to legacy content if no sections
    return (
      <div className={`prose prose-lg max-w-none ${className}`}>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content?.content || ''}
        </ReactMarkdown>
      </div>
    );
  }

  const renderSection = (section: Section, index: number) => {
    switch (section.type) {
      case 'intro':
        return (
          <div key={index} className="mb-8">
            <div className="prose prose-lg max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {section.content || ''}
              </ReactMarkdown>
            </div>
          </div>
        );

      case 'quick_picks':
        return (
          <div key={index} className="mb-12">
            {section.title && (
              <h2 className="text-2xl font-bold mb-6 text-gray-900">{section.title}</h2>
            )}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {section.products?.map((product, i) => (
                <div key={i} className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                  <h3 className="font-semibold text-lg mb-2">{product.name}</h3>
                  <p className="text-2xl font-bold text-gray-900 mb-3">{product.price}</p>
                  {product.reason && (
                    <p className="text-gray-600 mb-4">{product.reason}</p>
                  )}
                  <div className="flex flex-col gap-2">
                    <BlogAffiliateButtons
                      product={{ id: String(product.id), name: product.name, affiliate_url: product.affiliate_url, rating: product.rating }}
                      variant="inline"
                      ctaText="Check Price"
                    />
                    {(product.slug || product.store_url) && (
                      <a 
                        href={product.slug ? `/products/${product.slug}` : product.store_url}
                        className="inline-block text-gray-800 border border-gray-300 px-6 py-2 rounded-md hover:bg-gray-50 transition-colors font-semibold text-center"
                        style={{fontFamily: 'Montserrat, sans-serif'}}
                        target={product.slug ? undefined : "_blank"}
                        rel={product.slug ? undefined : "noopener noreferrer"}
                      >
                        {product.cta_text || 'See Details'}
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        );

      case 'content':
        return (
          <div key={index} className="mb-8">
            <div className="prose prose-lg max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {section.content || ''}
              </ReactMarkdown>
            </div>
          </div>
        );

      case 'product_spotlight': {
        let products: Product[] = Array.isArray(section.products) && section.products.length > 0
          ? (section.products as Product[])
          : (section.product ? [section.product as Product] : []);

        // Build slug map for hydration by slug/name if id missing
        const hydrateBySlug: Record<string, Partial<Product>> = {};
        Object.values(hydrate).forEach((h: any) => {
          if (h?.slug) hydrateBySlug[String(h.slug)] = h as any;
        });

        // Hydrate products from map when IDs match (or by slug/name)
        products = products.map((p) => {
          const key = String((p as any).id || '');
          let h = key ? hydrate[key] : undefined;
          if (!h && (p as any).slug) {
            h = hydrateBySlug[String((p as any).slug)];
          }
          if (!h && (p as any).name) {
            // fuzzy name match
            const pn = String((p as any).name).toLowerCase();
            h = (Object.values(hydrate).find((x: any) => String(x?.name || '').toLowerCase().includes(pn)) as any) || undefined;
          }
          if (!h) return p;
          return {
            ...p,
            name: h.name || p.name,
            slug: (h as any).slug || p.slug,
            affiliate_url: (h as any).affiliate_url || p.affiliate_url,
            store_url: (h as any).store_url || p.store_url,
            id: (h as any).id || p.id,
          };
        });

        // Fallback: if after hydration none have slug and we have fallbackProducts, use them instead
        const noneHydrated = !products.some(p => (p as any).slug);
        if (noneHydrated && Array.isArray(fallbackProducts) && fallbackProducts.length > 0) {
          products = fallbackProducts.slice(0, Math.max(products.length, 1)).map((fp) => ({
            id: fp.id as any,
            name: fp.name || 'Product',
            slug: (fp as any).slug,
            affiliate_url: (fp as any).slug ? `/products/${(fp as any).slug}` : undefined,
            store_url: (fp as any).slug ? `/products/${(fp as any).slug}` : undefined,
            price: '',
          })) as Product[];
        }

        if (products.length === 0) return null;

        return (
          <BlogProductSpotlight key={index} products={products} />
        );
      }

      case 'affiliate_banner':
        return (
          <div key={index} className="mb-8 bg-gray-50 border border-gray-200 rounded-lg p-6 text-center">
            <h3 className="font-bold text-lg mb-2">🎸 Ready to Buy?</h3>
            <p className="text-gray-700 mb-4">Check out our top recommendations and get the best deals!</p>
            <a 
              href="#quick_picks" 
              className="inline-block bg-brand-primary text-white px-6 py-2 rounded-md hover:opacity-90 transition-colors"
            >
              View Our Picks
            </a>
          </div>
        );

      case 'conclusion':
        return (
          <div key={index} className="mb-8 border-t border-gray-200 pt-8">
            <div className="prose prose-lg max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {section.content || ''}
              </ReactMarkdown>
            </div>
          </div>
        );

      default:
        return (
          <div key={index} className="mb-8">
            <div className="prose prose-lg max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {section.content || ''}
              </ReactMarkdown>
            </div>
          </div>
        );
    }
  };

  return (
    <div className={`${className}`}>
      {content.sections.map((section: Section, index: number) => 
        renderSection(section, index)
      )}
    </div>
  );
};

export default SimpleBlogRenderer;

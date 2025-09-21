import React from 'react';
import AffiliateButtons from './AffiliateButtons';

interface Product {
  id: string | number;
  name: string;
  price?: string;
  rating?: number;
  pros?: string[];
  cons?: string[];
  affiliate_url: string;
  store_url?: string;
  cta_text?: string;
  slug?: string;
  image_url?: string;
}

interface BlogProductSpotlightProps {
  products: Product[];
  title?: string;
  alternateLayout?: boolean; // alternate image left/right per product
}

export default function BlogProductSpotlight({ products, title, alternateLayout = true }: BlogProductSpotlightProps) {
  if (!products || products.length === 0) return null;

  return (
    <section className="mb-12 bg-white border border-gray-200 rounded-lg p-8 shadow-sm">
      {title && (
        <h3 className="text-2xl font-bold text-gray-900 mb-6" style={{fontFamily: 'Montserrat, sans-serif'}}>{title}</h3>
      )}

      <div className="space-y-10">
        {products.map((product, idx) => {
          const reverse = alternateLayout && idx % 2 === 1;
          return (
            <div key={idx} className={`flex flex-col ${reverse ? 'lg:flex-row-reverse' : 'lg:flex-row'} gap-8`}>
              {/* Image */}
              <div className="lg:w-64 w-full">
                <div className="aspect-square bg-gray-100 rounded overflow-hidden">
                  {product.image_url ? (
                    <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full bg-gray-100" />
                  )}
                </div>
              </div>

              {/* Details */}
              <div className="flex-1">
                <h4 className="text-xl font-bold text-gray-900 mb-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
                  {product.name}
                </h4>
                {product.price && (
                  <div className="text-2xl font-extrabold text-gray-900 mb-3" style={{fontFamily: 'Montserrat, sans-serif'}}>
                    {product.price}
                  </div>
                )}

                {typeof product.rating === 'number' && (
                  <div className="flex items-center mb-3">
                    <div className="flex text-yellow-400 mr-2">
                      {[...Array(5)].map((_, i) => (
                        <span key={i}>{i < Math.floor(product.rating || 0) ? '★' : '☆'}</span>
                      ))}
                    </div>
                    <span className="text-gray-600">{product.rating}/5</span>
                  </div>
                )}

                {(product.pros || product.cons) && (
                  <div className="grid sm:grid-cols-2 gap-4 mb-4">
                    {product.pros && product.pros.length > 0 && (
                      <div>
                        <h5 className="font-semibold text-green-700 mb-2">Pros</h5>
                        <ul className="space-y-1">
                          {product.pros.map((p, i) => (
                            <li key={i} className="text-sm text-gray-700">✓ {p}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {product.cons && product.cons.length > 0 && (
                      <div>
                        <h5 className="font-semibold text-gray-700 mb-2">Cons</h5>
                        <ul className="space-y-1">
                          {product.cons.map((c, i) => (
                            <li key={i} className="text-sm text-gray-700">✗ {c}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}

                <div className="flex flex-col gap-3 mt-2">
                  <AffiliateButtons 
                    product={{ id: Number(product.id), name: product.name, slug: product.slug || '' }} 
                    variant="full" 
                    maxButtons={2}
                  />
                  {(product.slug || product.store_url) && (
                    <a
                      href={product.slug ? `/products/${product.slug}` : product.store_url}
                      className="text-sm text-gray-700 underline hover:text-gray-900"
                      style={{fontFamily: 'Montserrat, sans-serif'}}
                      target={product.slug ? undefined : "_blank"}
                      rel={product.slug ? undefined : "noopener noreferrer"}
                    >
                      View details
                    </a>
                  )}
                </div>

                <p className="text-xs text-gray-500 mt-2">
                  As an affiliate, we earn from qualifying purchases
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

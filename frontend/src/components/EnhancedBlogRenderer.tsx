import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import Link from 'next/link';

interface EnhancedBlogRendererProps {
  content: any;
  className?: string;
}

interface Product {
  id: string;
  name: string;
  slug?: string;
  price: string;
  category?: string;
  brand?: string;
  rating?: number;
  review_count?: number;
  pros?: string[];
  cons?: string[];
  description?: string;
  affiliate_url: string;
  store_url?: string;
  cta_text?: string;
  image_url?: string;
}

interface Section {
  type: string;
  title?: string;
  content?: string;
  products?: Product[];
  product?: Product;
}

const StarRating: React.FC<{ rating: number; reviewCount?: number }> = ({ rating, reviewCount }) => (
  <div className="flex items-center gap-2 mb-3">
    <div className="flex">
      {[...Array(5)].map((_, i) => (
        <svg
          key={i}
          className={`w-4 h-4 ${i < Math.floor(rating) ? 'text-yellow-400' : 'text-gray-300'}`}
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      ))}
    </div>
    <span className="text-sm text-gray-600 font-medium" style={{fontFamily: 'Montserrat, sans-serif'}}>
      {rating.toFixed(1)} {reviewCount && `(${reviewCount} reviews)`}
    </span>
  </div>
);

const ProductSpotlight: React.FC<{ product: Product }> = ({ product }) => (
  <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm mb-8">
    <div className="flex flex-col lg:flex-row gap-6">
      {/* Product Image */}
      <div className="lg:w-48 flex-shrink-0">
        {product.image_url ? (
          <img 
            src={product.image_url} 
            alt={product.name}
            className="w-full h-48 lg:h-40 object-cover rounded-lg"
          />
        ) : (
          <div className="w-full h-48 lg:h-40 bg-gray-100 rounded-lg flex items-center justify-center">
            <svg className="w-16 h-16 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
            </svg>
          </div>
        )}
      </div>
      
      {/* Product Details */}
      <div className="flex-1">
        <div className="mb-4">
          <h3 className="text-xl font-bold text-gray-900 mb-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
            {product.name}
          </h3>
          {product.category && (
            <span className="inline-block bg-gray-100 text-gray-700 text-xs font-medium px-2 py-1 rounded-full mb-2">
              {product.category}
            </span>
          )}
        </div>

        {product.rating && (
          <StarRating rating={product.rating} reviewCount={product.review_count} />
        )}

        <div className="mb-4">
          <div className="text-2xl font-extrabold text-gray-900 mb-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
            {product.price}
          </div>
          {product.description && (
            <p className="text-gray-600 text-sm leading-relaxed">
              {product.description.length > 150 
                ? `${product.description.substring(0, 150)}...`
                : product.description
              }
            </p>
          )}
        </div>

        {/* Pros and Cons */}
        {(product.pros || product.cons) && (
          <div className="grid md:grid-cols-2 gap-4 mb-6">
            {product.pros && (
              <div>
                <h4 className="font-semibold text-green-700 mb-2 text-sm" style={{fontFamily: 'Montserrat, sans-serif'}}>
                  Pros
                </h4>
                <ul className="space-y-1">
                  {product.pros.map((pro, i) => (
                    <li key={i} className="text-sm text-gray-600 flex items-start">
                      <svg className="w-4 h-4 text-green-500 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      {pro}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {product.cons && (
              <div>
                <h4 className="font-semibold text-gray-700 mb-2 text-sm" style={{fontFamily: 'Montserrat, sans-serif'}}>
                  Cons
                </h4>
                <ul className="space-y-1">
                  {product.cons.map((con, i) => (
                    <li key={i} className="text-sm text-gray-600 flex items-start">
                      <svg className="w-4 h-4 text-gray-400 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                      </svg>
                      {con}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="lg:w-48 flex flex-col justify-center gap-3">
        <a 
          href={product.affiliate_url}
          className="bg-brand-primary text-white px-6 py-3 rounded-md hover:opacity-90 transition-colors text-center font-bold block text-sm"
          style={{fontFamily: 'Montserrat, sans-serif'}}
          target="_blank"
          rel="noopener noreferrer"
        >
          Check Price
        </a>
        
        {product.store_url && (
          <Link
            href={product.store_url}
            className="text-gray-700 border border-gray-300 px-6 py-3 rounded-md hover:bg-gray-50 transition-colors text-center font-semibold block text-sm"
            style={{fontFamily: 'Montserrat, sans-serif'}}
          >
            {product.cta_text || 'See Details'}
          </Link>
        )}
        
        <p className="text-xs text-gray-500 text-center mt-2">
          As an affiliate, we earn from qualifying purchases
        </p>
      </div>
    </div>
  </div>
);

const ProductGrid: React.FC<{ products: Product[]; title?: string }> = ({ products, title }) => (
  <div className="mb-12">
    {title && (
      <h2 className="text-2xl font-bold mb-6 text-gray-900" style={{fontFamily: 'Montserrat, sans-serif'}}>
        {title}
      </h2>
    )}
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      {products.map((product, i) => (
        <div key={i} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <div className="mb-3">
            <h3 className="font-semibold text-base mb-2 line-clamp-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
              {product.name}
            </h3>
            {product.category && (
              <span className="inline-block bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded-full">
                {product.category}
              </span>
            )}
          </div>
          
          {product.rating && (
            <StarRating rating={product.rating} reviewCount={product.review_count} />
          )}
          
          <div className="text-xl font-extrabold text-gray-900 mb-4" style={{fontFamily: 'Montserrat, sans-serif'}}>
            {product.price}
          </div>
          
          <div className="flex flex-col gap-2">
            <a 
              href={product.affiliate_url}
              className="bg-brand-primary text-white px-4 py-2 rounded-md hover:opacity-90 transition-colors text-center font-bold text-sm"
              style={{fontFamily: 'Montserrat, sans-serif'}}
              target="_blank"
              rel="noopener noreferrer"
            >
              Check Price
            </a>
            {product.store_url && (
              <Link
                href={product.store_url}
                className="text-gray-700 border border-gray-300 px-4 py-2 rounded-md hover:bg-gray-50 transition-colors text-center font-semibold text-sm"
                style={{fontFamily: 'Montserrat, sans-serif'}}
              >
                Details
              </Link>
            )}
          </div>
        </div>
      ))}
    </div>
  </div>
);

const BlogNavigation: React.FC<{ title: string; category?: string }> = ({ title, category }) => (
  <div className="mb-8">
    {/* Breadcrumbs */}
    <nav className="mb-4" aria-label="Breadcrumb">
      <ol className="flex items-center space-x-2 text-sm">
        <li>
          <Link href="/" className="text-gray-500 hover:text-gray-700" style={{fontFamily: 'Montserrat, sans-serif'}}>
            Home
          </Link>
        </li>
        <li className="text-gray-400">/</li>
        <li>
          <Link href="/blog" className="text-gray-500 hover:text-gray-700" style={{fontFamily: 'Montserrat, sans-serif'}}>
            Blog
          </Link>
        </li>
        {category && (
          <>
            <li className="text-gray-400">/</li>
            <li>
              <Link href={`/blog/category/${category}`} className="text-gray-500 hover:text-gray-700" style={{fontFamily: 'Montserrat, sans-serif'}}>
                {category.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </Link>
            </li>
          </>
        )}
        <li className="text-gray-400">/</li>
        <li className="text-gray-900 font-medium" style={{fontFamily: 'Montserrat, sans-serif'}}>
          {title.length > 50 ? `${title.substring(0, 50)}...` : title}
        </li>
      </ol>
    </nav>
    
    {/* Blog Navigation Menu */}
    <div className="flex flex-wrap gap-4 pb-4 border-b border-gray-200">
      <Link href="/blog" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors" style={{fontFamily: 'Montserrat, sans-serif'}}>
        Latest
      </Link>
      <Link href="/blog/category/buying-guide" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors" style={{fontFamily: 'Montserrat, sans-serif'}}>
        Buying Guides
      </Link>
      <Link href="/blog/category/review" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors" style={{fontFamily: 'Montserrat, sans-serif'}}>
        Reviews
      </Link>
      <Link href="/blog/category/comparison" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors" style={{fontFamily: 'Montserrat, sans-serif'}}>
        Comparisons
      </Link>
      <Link href="/blog/category/artist-spotlight" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors" style={{fontFamily: 'Montserrat, sans-serif'}}>
        Artists
      </Link>
      <Link href="/blog/category/gear-tips" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors" style={{fontFamily: 'Montserrat, sans-serif'}}>
        Tips & Guides
      </Link>
    </div>
  </div>
);

const EnhancedBlogRenderer: React.FC<EnhancedBlogRendererProps> = ({ content, className = '' }) => {
  if (!content?.sections) {
    // Fallback to legacy content if no sections
    return (
      <div className={`prose prose-lg max-w-none ${className}`} style={{fontFamily: 'Arial, Helvetica, sans-serif'}}>
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
            <div className="prose prose-lg max-w-none" style={{fontFamily: 'Arial, Helvetica, sans-serif'}}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {section.content || ''}
              </ReactMarkdown>
            </div>
          </div>
        );

      case 'quick_picks':
        return (
          <ProductGrid 
            key={index}
            products={section.products || []}
            title={section.title || "Our Top Picks"}
          />
        );

      case 'content':
        return (
          <div key={index} className="mb-8">
            <div className="prose prose-lg max-w-none" style={{fontFamily: 'Arial, Helvetica, sans-serif'}}>
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]}
                components={{
                  h1: ({node, ...props}) => <h1 className="text-3xl font-bold mb-6 text-gray-900" style={{fontFamily: 'Montserrat, sans-serif'}} {...props} />,
                  h2: ({node, ...props}) => <h2 className="text-2xl font-bold mb-4 text-gray-900" style={{fontFamily: 'Montserrat, sans-serif'}} {...props} />,
                  h3: ({node, ...props}) => <h3 className="text-xl font-bold mb-3 text-gray-900" style={{fontFamily: 'Montserrat, sans-serif'}} {...props} />,
                  h4: ({node, ...props}) => <h4 className="text-lg font-bold mb-2 text-gray-900" style={{fontFamily: 'Montserrat, sans-serif'}} {...props} />,
                  a: ({node, ...props}) => <a className="text-gray-900 underline hover:opacity-80" {...props} />,
                }}
              >
                {section.content || ''}
              </ReactMarkdown>
            </div>
          </div>
        );

      case 'product_spotlight':
        const product = section.product;
        if (!product) return null;
        
        return <ProductSpotlight key={index} product={product} />;

      case 'affiliate_banner':
        return (
          <div key={index} className="mb-8 bg-gray-50 border border-gray-200 rounded-lg p-6 text-center">
            <h3 className="font-bold text-lg mb-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
              🎸 Ready to Buy?
            </h3>
            <p className="text-gray-700 mb-4">Check out our top recommendations and get the best deals!</p>
            <a 
              href="#quick_picks" 
              className="inline-block bg-brand-primary text-white px-6 py-2 rounded-md transition-colors font-bold hover:opacity-90"
              style={{fontFamily: 'Montserrat, sans-serif'}}
            >
              View Our Picks
            </a>
          </div>
        );

      case 'conclusion':
        return (
          <div key={index} className="mb-8 border-t border-gray-200 pt-8">
            <div className="prose prose-lg max-w-none" style={{fontFamily: 'Arial, Helvetica, sans-serif'}}>
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]}
                components={{
                  h2: ({node, ...props}) => <h2 className="text-2xl font-bold mb-4 text-gray-900" style={{fontFamily: 'Montserrat, sans-serif'}} {...props} />,
                  h3: ({node, ...props}) => <h3 className="text-xl font-bold mb-3 text-gray-900" style={{fontFamily: 'Montserrat, sans-serif'}} {...props} />,
                }}
              >
                {section.content || ''}
              </ReactMarkdown>
            </div>
          </div>
        );

      default:
        return (
          <div key={index} className="mb-8">
            <div className="prose prose-lg max-w-none" style={{fontFamily: 'Arial, Helvetica, sans-serif'}}>
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
      {/* Blog Navigation */}
      <BlogNavigation 
        title={content.title || "Blog Post"}
        category={content.category}
      />
      
      {/* Blog Content */}
      <div style={{fontFamily: 'Arial, Helvetica, sans-serif'}}>
        {content.sections.map((section: Section, index: number) => 
          renderSection(section, index)
        )}
      </div>
      
      {/* Author Section */}
      {content.author_name && (
        <div className="mt-12 pt-8 border-t border-gray-200">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-gray-300 rounded-full flex items-center justify-center mr-4">
              <svg className="w-6 h-6 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <p className="font-semibold text-gray-900" style={{fontFamily: 'Montserrat, sans-serif'}}>
                {content.author_name}
              </p>
              <p className="text-sm text-gray-600">Music Gear Expert</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EnhancedBlogRenderer;

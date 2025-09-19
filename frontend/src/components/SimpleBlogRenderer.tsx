import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface SimpleBlogRendererProps {
  content: any;
  className?: string;
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
}

interface Section {
  type: string;
  title?: string;
  content?: string;
  products?: Product[];
  product?: Product;
}

const SimpleBlogRenderer: React.FC<SimpleBlogRendererProps> = ({ content, className = '' }) => {
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
                  <p className="text-2xl font-bold text-red-600 mb-3">{product.price}</p>
                  {product.reason && (
                    <p className="text-gray-600 mb-4">{product.reason}</p>
                  )}
                  <a 
                    href={product.affiliate_url}
                    className="inline-block bg-red-600 text-white px-6 py-2 rounded-md hover:bg-red-700 transition-colors"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Check Price
                  </a>
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

      case 'product_spotlight':
        const product = section.product;
        if (!product) return null;
        
        return (
          <div key={index} className="mb-12 bg-gray-50 rounded-lg p-8">
            <div className="flex flex-col lg:flex-row gap-8">
              <div className="flex-1">
                <h3 className="text-2xl font-bold mb-2">{product.name}</h3>
                <p className="text-3xl font-bold text-red-600 mb-4">{product.price}</p>
                
                {product.rating && (
                  <div className="flex items-center mb-4">
                    <div className="flex text-yellow-400 mr-2">
                      {[...Array(5)].map((_, i) => (
                        <span key={i}>
                          {i < Math.floor(product.rating!) ? '★' : '☆'}
                        </span>
                      ))}
                    </div>
                    <span className="text-gray-600">{product.rating}/5</span>
                  </div>
                )}

                {(product.pros || product.cons) && (
                  <div className="grid md:grid-cols-2 gap-4 mb-6">
                    {product.pros && (
                      <div>
                        <h4 className="font-semibold text-green-700 mb-2">Pros</h4>
                        <ul className="space-y-1">
                          {product.pros.map((pro, i) => (
                            <li key={i} className="text-sm text-gray-600">✓ {pro}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {product.cons && (
                      <div>
                        <h4 className="font-semibold text-red-700 mb-2">Cons</h4>
                        <ul className="space-y-1">
                          {product.cons.map((con, i) => (
                            <li key={i} className="text-sm text-gray-600">✗ {con}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
              
              <div className="lg:w-64 flex flex-col justify-center">
                <a 
                  href={product.affiliate_url}
                  className="bg-red-600 text-white px-8 py-3 rounded-md hover:bg-red-700 transition-colors text-center font-semibold mb-4"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Check Price
                </a>
                <p className="text-xs text-gray-500 text-center">
                  As an affiliate, we earn from qualifying purchases
                </p>
              </div>
            </div>
          </div>
        );

      case 'affiliate_banner':
        return (
          <div key={index} className="mb-8 bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <h3 className="font-bold text-lg mb-2">🎸 Ready to Buy?</h3>
            <p className="text-gray-700 mb-4">Check out our top recommendations and get the best deals!</p>
            <a 
              href="#quick_picks" 
              className="inline-block bg-red-600 text-white px-6 py-2 rounded-md hover:bg-red-700 transition-colors"
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
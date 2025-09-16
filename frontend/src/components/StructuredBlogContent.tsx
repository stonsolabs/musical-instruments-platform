import React from 'react';

interface BlogSection {
  type: string;
  title?: string;
  content: string;
  products_mentioned?: number[];
  products?: Array<{
    product_id: number;
    context: string;
    position: number;
  }>;
  faqs?: Array<{
    question: string;
    answer: string;
  }>;
}

interface StructuredBlogContent {
  title: string;
  excerpt?: string;
  seo_title?: string;
  seo_description?: string;
  featured_image_alt?: string;
  reading_time?: number;
  sections: BlogSection[];
  tags?: string[];
  meta?: {
    content_type?: string;
    expertise_level?: string;
    target_audience?: string[];
    key_benefits?: string[];
  };
}

interface StructuredBlogRendererProps {
  content: StructuredBlogContent;
  products?: any[]; // Product data fetched separately
}

const SectionRenderer: React.FC<{ section: BlogSection; products?: any[] }> = ({ 
  section, 
  products = [] 
}) => {
  const getSectionClassName = (type: string) => {
    const baseClasses = "mb-8";
    const typeClasses = {
      introduction: "prose prose-lg",
      comparison_table: "overflow-x-auto",
      product_showcase: "space-y-6",
      buying_guide: "prose",
      faqs: "space-y-4",
      conclusion: "prose"
    };
    return `${baseClasses} ${typeClasses[type as keyof typeof typeClasses] || 'prose'}`;
  };

  const renderSectionContent = () => {
    switch (section.type) {
      case 'product_showcase':
        return (
          <div className="space-y-6">
            {section.title && (
              <h2 className="text-2xl font-bold text-gray-900 mb-6">{section.title}</h2>
            )}
            <div dangerouslySetInnerHTML={{ __html: section.content }} />
            
            {section.products && (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {section.products
                  .sort((a, b) => a.position - b.position)
                  .map((productRef) => {
                    const product = products.find(p => p.id === productRef.product_id);
                    if (!product) return null;
                    
                    return (
                      <div key={productRef.product_id} className="bg-white rounded-lg shadow-md overflow-hidden">
                        {product.featured_image && (
                          <img 
                            src={product.featured_image} 
                            alt={product.name}
                            className="w-full h-48 object-cover"
                          />
                        )}
                        <div className="p-6">
                          <h3 className="font-semibold text-lg mb-2">{product.name}</h3>
                          {product.brand && (
                            <p className="text-gray-600 text-sm mb-2">{product.brand}</p>
                          )}
                          {productRef.context && (
                            <p className="text-sm text-gray-700 mb-4">{productRef.context}</p>
                          )}
                          <a 
                            href={`/products/${product.slug}`}
                            className="inline-flex items-center text-brand-primary hover:text-brand-orange font-medium transition-colors"
                          >
                            View Details
                            <svg className="ml-2 w-4 h-4 transform hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                          </a>
                        </div>
                      </div>
                    );
                  })}
              </div>
            )}
          </div>
        );

      case 'faqs':
        return (
          <div>
            {section.title && (
              <h2 className="text-2xl font-bold text-gray-900 mb-6">{section.title}</h2>
            )}
            <div dangerouslySetInnerHTML={{ __html: section.content }} />
            
            {section.faqs && (
              <div className="space-y-4 mt-6">
                {section.faqs.map((faq, index) => (
                  <details key={index} className="bg-gray-50 rounded-lg p-4">
                    <summary className="font-semibold text-gray-900 cursor-pointer">
                      {faq.question}
                    </summary>
                    <div className="mt-3 text-gray-700" dangerouslySetInnerHTML={{ __html: faq.answer }} />
                  </details>
                ))}
              </div>
            )}
          </div>
        );

      case 'comparison_table':
        return (
          <div>
            {section.title && (
              <h2 className="text-2xl font-bold text-gray-900 mb-6">{section.title}</h2>
            )}
            <div className="overflow-x-auto">
              <div dangerouslySetInnerHTML={{ __html: section.content }} />
            </div>
          </div>
        );

      default:
        return (
          <div>
            {section.title && (
              <h2 className="text-2xl font-bold text-gray-900 mb-6">{section.title}</h2>
            )}
            <div dangerouslySetInnerHTML={{ __html: section.content }} />
          </div>
        );
    }
  };

  return (
    <section className={getSectionClassName(section.type)}>
      {renderSectionContent()}
    </section>
  );
};

const StructuredBlogRenderer: React.FC<StructuredBlogRendererProps> = ({ 
  content, 
  products = [] 
}) => {
  return (
    <article className="max-w-4xl mx-auto">
      {/* Article Header */}
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">{content.title}</h1>
        {content.excerpt && (
          <p className="text-xl text-gray-600 leading-relaxed mb-6">{content.excerpt}</p>
        )}
        
        {/* Meta information */}
        <div className="flex items-center gap-4 text-sm text-gray-500 mb-6">
          {content.reading_time && (
            <span>{content.reading_time} min read</span>
          )}
          {content.meta?.expertise_level && (
            <span className="bg-gray-100 px-2 py-1 rounded">
              {content.meta.expertise_level}
            </span>
          )}
        </div>

        {/* Tags */}
        {content.tags && content.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-6">
            {content.tags.map((tag, index) => (
              <span 
                key={index}
                className="bg-brand-primary/10 text-brand-primary px-3 py-1 rounded-full text-sm"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}
      </header>

      {/* Article Sections */}
      <main>
        {content.sections.map((section, index) => (
          <SectionRenderer 
            key={index} 
            section={section} 
            products={products}
          />
        ))}
      </main>

      {/* Article Footer */}
      <footer className="mt-12 pt-8 border-t border-gray-200">
        {content.meta?.key_benefits && (
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="font-semibold text-gray-900 mb-3">Key Takeaways</h3>
            <ul className="space-y-2">
              {content.meta.key_benefits.map((benefit, index) => (
                <li key={index} className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">{benefit.replace(/_/g, ' ')}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </footer>
    </article>
  );
};

export default StructuredBlogRenderer;
export type { StructuredBlogContent, BlogSection };
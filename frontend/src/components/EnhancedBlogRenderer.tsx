import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import InlineProductShowcase from './InlineProductShowcase';
import ProsCons from './ProsCons';
import BlogComparisonTable from './BlogComparisonTable';
import SpecsList from './SpecsList';
import { BlogPost } from '../types/blog';

interface EnhancedBlogRendererProps {
  post: BlogPost;
  showInlineProducts?: boolean;
}

interface BlogSection {
  type: string;
  title?: string;
  content?: string;
  products?: Array<{
    product_id: number;
    context: string;
    position: number;
    cta_text?: string;
    affiliate_placement?: string;
  }>;
  products_mentioned?: number[];
  pros?: string[];
  cons?: string[];
  headers?: string[];
  rows?: string[][];
  specs?: Array<{ label: string; value: string }>;
  faqs?: Array<{ question: string; answer: string }>;
  affiliate_placement?: string;
}

export default function EnhancedBlogRenderer({ 
  post, 
  showInlineProducts = true 
}: EnhancedBlogRendererProps) {
  
  const structuredContent = (post as any).structured_content;
  
  if (!structuredContent?.sections || !Array.isArray(structuredContent.sections)) {
    // Fallback to regular markdown rendering
    return (
      <div className="prose prose-lg lg:prose-xl max-w-none">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {post.content}
        </ReactMarkdown>
      </div>
    );
  }

  const renderSection = (section: BlogSection, index: number) => {
    const sectionType = section.type || '';
    
    return (
      <section key={index} className="prose prose-lg lg:prose-xl max-w-none">
        {section.title && (
          <h2 id={`sec-${index}`} className="mt-0 scroll-mt-24">
            {section.title}
          </h2>
        )}
        
        {/* Render section content based on type */}
        {renderSectionContent(section, index)}
      </section>
    );
  };

  const renderSectionContent = (section: BlogSection, index: number) => {
    const sectionType = section.type || '';
    
    // Handle inline product showcases
    if (sectionType.includes('product_showcase_inline') && section.products && showInlineProducts) {
      return (
        <div className="space-y-6">
          {/* Section content */}
          {section.content && (
            <div className="prose prose-lg max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {section.content}
              </ReactMarkdown>
            </div>
          )}
          
          {/* Inline product showcases */}
          {section.products.map((product, productIndex) => (
            <InlineProductShowcase
              key={`${index}-${productIndex}`}
              productId={product.product_id}
              context={product.context}
              position={product.position}
              ctaText={product.cta_text || "Check Latest Price"}
              layout="horizontal"
              showFullDetails={true}
            />
          ))}
        </div>
      );
    }
    
    // Handle pros/cons sections
    if (sectionType.includes('pros_cons') && (section.pros || section.cons)) {
      return (
        <div className="space-y-4">
          {section.content && (
            <div className="prose prose-lg max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {section.content}
              </ReactMarkdown>
            </div>
          )}
          <ProsCons pros={section.pros || []} cons={section.cons || []} />
        </div>
      );
    }
    
    // Handle comparison tables
    if (sectionType.includes('comparison_table') && section.headers && section.rows) {
      return (
        <div className="space-y-4">
          {section.content && (
            <div className="prose prose-lg max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {section.content}
              </ReactMarkdown>
            </div>
          )}
          <BlogComparisonTable headers={section.headers} rows={section.rows} />
          
          {/* Add affiliate placement below table if specified */}
          {section.affiliate_placement === 'below_table' && section.products_mentioned && showInlineProducts && (
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="text-lg font-semibold text-blue-900 mb-3">Ready to Buy?</h4>
              <p className="text-blue-800 mb-4">
                Check out the products mentioned in this comparison and find the best deals.
              </p>
              <div className="flex flex-wrap gap-2">
                {section.products_mentioned.map((productId, idx) => (
                  <InlineProductShowcase
                    key={`table-${idx}`}
                    productId={productId}
                    context="Featured in comparison above"
                    position={idx + 1}
                    ctaText="View Details"
                    layout="compact"
                    showFullDetails={false}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      );
    }
    
    // Handle specs sections
    if (sectionType.includes('specs') && section.specs && section.specs.length > 0) {
      return (
        <div className="space-y-4">
          {section.content && (
            <div className="prose prose-lg max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {section.content}
              </ReactMarkdown>
            </div>
          )}
          <SpecsList specs={section.specs} />
        </div>
      );
    }
    
    // Handle FAQ sections
    if (sectionType.includes('faqs') && section.faqs && section.faqs.length > 0) {
      return (
        <div className="space-y-4">
          {section.content && (
            <div className="prose prose-lg max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {section.content}
              </ReactMarkdown>
            </div>
          )}
          <div className="space-y-3">
            {section.faqs.map((faq, faqIndex) => (
              <details key={faqIndex} className="group border rounded-md p-4 bg-white">
                <summary className="cursor-pointer font-medium text-gray-800 group-open:text-brand-primary">
                  {faq.question}
                </summary>
                <div className="mt-2 text-gray-700">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {faq.answer}
                  </ReactMarkdown>
                </div>
              </details>
            ))}
          </div>
        </div>
      );
    }
    
    // Handle regular content sections
    if (section.content) {
      return (
        <div className="space-y-4">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {section.content}
          </ReactMarkdown>
          
          {/* Add inline product mentions if specified */}
          {section.products_mentioned && section.products_mentioned.length > 0 && showInlineProducts && (
            <div className="mt-6 p-4 bg-gray-50 border border-gray-200 rounded-lg">
              <h4 className="text-lg font-semibold text-gray-900 mb-3">Mentioned Products</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {section.products_mentioned.map((productId, idx) => (
                  <InlineProductShowcase
                    key={`mentioned-${idx}`}
                    productId={productId}
                    context="Mentioned in this section"
                    position={idx + 1}
                    ctaText="Learn More"
                    layout="compact"
                    showFullDetails={false}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      );
    }
    
    return null;
  };

  return (
    <div className="space-y-10">
      {structuredContent.sections.map((section: BlogSection, index: number) => 
        renderSection(section, index)
      )}
    </div>
  );
}

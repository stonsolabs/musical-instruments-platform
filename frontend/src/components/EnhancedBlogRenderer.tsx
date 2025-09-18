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

// Function to render structured content directly
function renderStructuredContent(structuredContent: any, showInlineProducts: boolean) {
  const sections = [];
  
  // Render introduction
  if (structuredContent.introduction) {
    sections.push(
      <section key="introduction" className="mb-8">
        <h2 id="introduction" className="text-2xl font-bold mb-4">Introduction</h2>
        <div className="prose prose-lg max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {structuredContent.introduction}
          </ReactMarkdown>
        </div>
      </section>
    );
  }
  
  // Render buying criteria
  if (structuredContent.buying_criteria) {
    sections.push(
      <section key="buying_criteria" className="mb-8">
        <h2 id="buying_criteria" className="text-2xl font-bold mb-4">What to Look For</h2>
        <div className="prose prose-lg max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {structuredContent.buying_criteria}
          </ReactMarkdown>
        </div>
      </section>
    );
  }
  
  // Render detailed reviews
  if (structuredContent.detailed_reviews) {
    sections.push(
      <section key="detailed_reviews" className="mb-8">
        <h2 id="detailed_reviews" className="text-2xl font-bold mb-4">Detailed Reviews</h2>
        <div className="prose prose-lg max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {structuredContent.detailed_reviews}
          </ReactMarkdown>
        </div>
      </section>
    );
  }
  
  // Render comparison table
  if (structuredContent.comparison_table) {
    sections.push(
      <section key="comparison_table" className="mb-8">
        <h2 id="comparison_table" className="text-2xl font-bold mb-4">Comparison Table</h2>
        <div className="prose prose-lg max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {structuredContent.comparison_table}
          </ReactMarkdown>
        </div>
      </section>
    );
  }
  
  // Render budget breakdown
  if (structuredContent.budget_breakdown) {
    sections.push(
      <section key="budget_breakdown" className="mb-8">
        <h2 id="budget_breakdown" className="text-2xl font-bold mb-4">Budget Breakdown</h2>
        <div className="prose prose-lg max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {structuredContent.budget_breakdown}
          </ReactMarkdown>
        </div>
      </section>
    );
  }
  
  // Render setup guide
  if (structuredContent.setup_guide) {
    sections.push(
      <section key="setup_guide" className="mb-8">
        <h2 id="setup_guide" className="text-2xl font-bold mb-4">Setup Guide</h2>
        <div className="prose prose-lg max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {structuredContent.setup_guide}
          </ReactMarkdown>
        </div>
      </section>
    );
  }
  
  // Render common mistakes
  if (structuredContent.common_mistakes) {
    sections.push(
      <section key="common_mistakes" className="mb-8">
        <h2 id="common_mistakes" className="text-2xl font-bold mb-4">Common Mistakes to Avoid</h2>
        <div className="prose prose-lg max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {structuredContent.common_mistakes}
          </ReactMarkdown>
        </div>
      </section>
    );
  }
  
  // Render quick picks
  if (structuredContent.quick_picks) {
    sections.push(
      <section key="quick_picks" className="mb-8">
        <h2 id="quick_picks" className="text-2xl font-bold mb-4">Quick Picks</h2>
        <div className="prose prose-lg max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {structuredContent.quick_picks}
          </ReactMarkdown>
        </div>
      </section>
    );
  }
  
  // Render expert verdict
  if (structuredContent.expert_verdict) {
    sections.push(
      <section key="expert_verdict" className="mb-8">
        <h2 id="expert_verdict" className="text-2xl font-bold mb-4">Expert Verdict</h2>
        <div className="prose prose-lg max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {structuredContent.expert_verdict}
          </ReactMarkdown>
        </div>
      </section>
    );
  }
  
  // Render conclusion
  if (structuredContent.conclusion) {
    sections.push(
      <section key="conclusion" className="mb-8">
        <h2 id="conclusion" className="text-2xl font-bold mb-4">Conclusion</h2>
        <div className="prose prose-lg max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {structuredContent.conclusion}
          </ReactMarkdown>
        </div>
      </section>
    );
  }
  
  // Render FAQs
  if (structuredContent.faqs && Array.isArray(structuredContent.faqs)) {
    sections.push(
      <section key="faqs" className="mb-8">
        <h2 id="faqs" className="text-2xl font-bold mb-4">Frequently Asked Questions</h2>
        <div className="space-y-3">
          {structuredContent.faqs.map((faq: any, index: number) => (
            <details key={index} className="group border rounded-md p-4 bg-white">
              <summary className="cursor-pointer font-medium text-gray-800 group-open:text-brand-primary">
                {faq.q || faq.question}
              </summary>
              <div className="mt-2 text-gray-700">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {faq.a || faq.answer}
                </ReactMarkdown>
              </div>
            </details>
          ))}
        </div>
      </section>
    );
  }
  
  return <div className="space-y-8">{sections}</div>;
}

export default function EnhancedBlogRenderer({ 
  post, 
  showInlineProducts = true 
}: EnhancedBlogRendererProps) {
  
  const structuredContent = (post as any).structured_content;
  
  // If we have structured content but no sections array, render the structured content directly
  if (structuredContent && !structuredContent.sections) {
    return (
      <div className="prose prose-lg lg:prose-xl max-w-none">
        {renderStructuredContent(structuredContent, showInlineProducts)}
      </div>
    );
  }
  
  if (!structuredContent?.sections || !Array.isArray(structuredContent.sections)) {
    // Fallback to regular markdown rendering
    return (
      <div className="prose prose-lg lg:prose-xl max-w-none">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {post.content || 'No content available'}
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

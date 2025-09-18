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
    const intro = structuredContent.introduction;
    sections.push(
      <section key="introduction" className="mb-8">
        <h2 id="introduction" className="text-2xl font-bold mb-4">Introduction</h2>
        <div className="prose prose-lg max-w-none">
          {intro.hook && (
            <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
              <p className="text-lg font-medium text-blue-800">{intro.hook}</p>
            </div>
          )}
          {intro.problem_statement && (
            <div className="mb-4">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {intro.problem_statement}
              </ReactMarkdown>
            </div>
          )}
          {intro.solution_preview && (
            <div className="bg-green-50 border-l-4 border-green-400 p-4">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {intro.solution_preview}
              </ReactMarkdown>
            </div>
          )}
        </div>
      </section>
    );
  }
  
  // Render quick picks
  if (structuredContent.quick_picks) {
    const quickPicks = structuredContent.quick_picks;
    sections.push(
      <section key="quick_picks" className="mb-8">
        <h2 id="quick_picks" className="text-2xl font-bold mb-4">{quickPicks.title || 'Quick Picks'}</h2>
        {quickPicks.products && Array.isArray(quickPicks.products) && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {quickPicks.products.map((product: any, index: number) => (
              <div key={index} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{product.name}</h3>
                  <div className="text-2xl font-bold text-green-600 mb-2">{product.price}</div>
                  {product.rating && (
                    <div className="flex items-center mb-2">
                      <span className="text-yellow-400">★</span>
                      <span className="ml-1 text-sm text-gray-600">{product.rating}/10</span>
                    </div>
                  )}
                </div>
                <div className="mb-4">
                  <p className="text-sm text-gray-600 mb-2"><strong>Best for:</strong> {product.best_for}</p>
                  {product.why_we_love_it && (
                    <p className="text-sm text-gray-700">{product.why_we_love_it}</p>
                  )}
                </div>
                {showInlineProducts && product.product_id && (
                  <div className="mt-4">
                    <InlineProductShowcase
                      productId={parseInt(product.product_id)}
                      context={product.affiliate_cta || "Featured in this guide"}
                      position={index + 1}
                      ctaText="Check Latest Price"
                      layout="compact"
                      showFullDetails={false}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    );
  }
  
  // Render buying criteria
  if (structuredContent.buying_criteria) {
    const criteria = structuredContent.buying_criteria;
    sections.push(
      <section key="buying_criteria" className="mb-8">
        <h2 id="buying_criteria" className="text-2xl font-bold mb-4">{criteria.title || 'What to Look For'}</h2>
        {criteria.criteria && Array.isArray(criteria.criteria) && (
          <div className="space-y-6">
            {criteria.criteria.map((criterion: any, index: number) => (
              <div key={index} className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{criterion.criterion}</h3>
                <p className="text-gray-700 mb-3">{criterion.description}</p>
                {criterion.why_matters && (
                  <div className="bg-blue-50 border-l-4 border-blue-400 p-3 mb-3">
                    <p className="text-sm text-blue-800"><strong>Why it matters:</strong> {criterion.why_matters}</p>
                  </div>
                )}
                {criterion.red_flags && (
                  <div className="bg-red-50 border-l-4 border-red-400 p-3">
                    <p className="text-sm text-red-800"><strong>Red flags:</strong> {criterion.red_flags}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    );
  }
  
  // Render detailed reviews
  if (structuredContent.detailed_reviews) {
    const reviews = structuredContent.detailed_reviews;
    sections.push(
      <section key="detailed_reviews" className="mb-8">
        <h2 id="detailed_reviews" className="text-2xl font-bold mb-4">Detailed Reviews</h2>
        {Array.isArray(reviews) && (
          <div className="space-y-8">
            {reviews.map((review: any, index: number) => (
              <div key={index} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-semibold text-gray-900">{review.name}</h3>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-green-600">{review.price}</div>
                    {review.rating && (
                      <div className="flex items-center justify-end mt-1">
                        <span className="text-yellow-400">★</span>
                        <span className="ml-1 text-sm text-gray-600">{review.rating}/10</span>
                      </div>
                    )}
                  </div>
                </div>
                
                {review.overview && (
                  <p className="text-gray-700 mb-4">{review.overview}</p>
                )}
                
                {review.key_features && Array.isArray(review.key_features) && (
                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-900 mb-2">Key Features:</h4>
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                      {review.key_features.map((feature: string, idx: number) => (
                        <li key={idx}>{feature}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {review.ideal_for && (
                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-900 mb-2">Ideal For:</h4>
                    <p className="text-gray-700">{review.ideal_for}</p>
                  </div>
                )}
                
                {review.performance_analysis && (
                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-900 mb-2">Performance Analysis:</h4>
                    <p className="text-gray-700">{review.performance_analysis}</p>
                  </div>
                )}
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  {review.pros && Array.isArray(review.pros) && review.pros.length > 0 && (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <h4 className="font-semibold text-green-800 mb-2">Pros:</h4>
                      <ul className="list-disc list-inside text-green-700 space-y-1">
                        {review.pros.map((pro: string, idx: number) => (
                          <li key={idx}>{pro}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  {review.cons && Array.isArray(review.cons) && review.cons.length > 0 && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                      <h4 className="font-semibold text-red-800 mb-2">Cons:</h4>
                      <ul className="list-disc list-inside text-red-700 space-y-1">
                        {review.cons.map((con: string, idx: number) => (
                          <li key={idx}>{con}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
                
                {review.current_deals && (
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
                    <h4 className="font-semibold text-yellow-800 mb-2">Current Deals:</h4>
                    <p className="text-yellow-700">{review.current_deals}</p>
                  </div>
                )}
                
                {showInlineProducts && review.product_id && (
                  <div className="mt-4">
                    <InlineProductShowcase
                      productId={parseInt(review.product_id)}
                      context={review.affiliate_cta || "Featured in this review"}
                      position={index + 1}
                      ctaText="Check Latest Price"
                      layout="horizontal"
                      showFullDetails={true}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    );
  }
  
  // Render comparison table
  if (structuredContent.comparison_table) {
    const table = structuredContent.comparison_table;
    sections.push(
      <section key="comparison_table" className="mb-8">
        <h2 id="comparison_table" className="text-2xl font-bold mb-4">{table.title || 'Comparison Table'}</h2>
        {table.headers && table.rows && (
          <div className="overflow-x-auto">
            <BlogComparisonTable headers={table.headers} rows={table.rows} />
          </div>
        )}
      </section>
    );
  }
  
  // Render budget breakdown
  if (structuredContent.budget_breakdown) {
    const breakdown = structuredContent.budget_breakdown;
    sections.push(
      <section key="budget_breakdown" className="mb-8">
        <h2 id="budget_breakdown" className="text-2xl font-bold mb-4">{breakdown.title || 'Budget Breakdown'}</h2>
        {breakdown.tiers && Array.isArray(breakdown.tiers) && (
          <div className="space-y-6">
            {breakdown.tiers.map((tier: any, index: number) => (
              <div key={index} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">{tier.tier}</h3>
                  <div className="text-right">
                    <div className="text-lg font-semibold text-gray-900">{tier.recommendation}</div>
                  </div>
                </div>
                <p className="text-gray-700 mb-4">{tier.reasoning}</p>
                {showInlineProducts && tier.product_id && (
                  <div className="mt-4">
                    <InlineProductShowcase
                      productId={parseInt(tier.product_id)}
                      context="Recommended for this budget tier"
                      position={index + 1}
                      ctaText="Check Latest Price"
                      layout="compact"
                      showFullDetails={false}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    );
  }
  
  // Render setup guide
  if (structuredContent.setup_guide) {
    const guide = structuredContent.setup_guide;
    sections.push(
      <section key="setup_guide" className="mb-8">
        <h2 id="setup_guide" className="text-2xl font-bold mb-4">{guide.title || 'Setup Guide'}</h2>
        {guide.steps && Array.isArray(guide.steps) && (
          <div className="space-y-6">
            {guide.steps.map((step: any, index: number) => (
              <div key={index} className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <div className="flex items-start">
                  <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold mr-4">
                    {step.step || index + 1}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-blue-900 mb-2">{step.title}</h3>
                    <p className="text-blue-800 mb-3">{step.description}</p>
                    {step.tips && (
                      <div className="bg-blue-100 border-l-4 border-blue-400 p-3">
                        <p className="text-sm text-blue-800"><strong>Pro tip:</strong> {step.tips}</p>
                      </div>
                    )}
                    {step.required_products && Array.isArray(step.required_products) && step.required_products.length > 0 && showInlineProducts && (
                      <div className="mt-4">
                        <h4 className="font-semibold text-blue-900 mb-2">Required Products:</h4>
                        <div className="flex flex-wrap gap-2">
                          {step.required_products.map((productId: string, idx: number) => (
                            <InlineProductShowcase
                              key={idx}
                              productId={parseInt(productId)}
                              context="Required for this step"
                              position={idx + 1}
                              ctaText="View Product"
                              layout="compact"
                              showFullDetails={false}
                            />
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    );
  }
  
  // Render common mistakes
  if (structuredContent.common_mistakes) {
    const mistakes = structuredContent.common_mistakes;
    sections.push(
      <section key="common_mistakes" className="mb-8">
        <h2 id="common_mistakes" className="text-2xl font-bold mb-4">{mistakes.title || 'Common Mistakes to Avoid'}</h2>
        {mistakes.mistakes && Array.isArray(mistakes.mistakes) && (
          <div className="space-y-6">
            {mistakes.mistakes.map((mistake: any, index: number) => (
              <div key={index} className="bg-red-50 border border-red-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-red-900 mb-2">{mistake.mistake}</h3>
                {mistake.why_happens && (
                  <div className="mb-3">
                    <h4 className="font-semibold text-red-800 mb-1">Why this happens:</h4>
                    <p className="text-red-700">{mistake.why_happens}</p>
                  </div>
                )}
                {mistake.how_to_avoid && (
                  <div className="mb-3">
                    <h4 className="font-semibold text-red-800 mb-1">How to avoid:</h4>
                    <p className="text-red-700">{mistake.how_to_avoid}</p>
                  </div>
                )}
                {mistake.better_alternative && (
                  <div className="bg-green-50 border-l-4 border-green-400 p-3">
                    <h4 className="font-semibold text-green-800 mb-1">Better alternative:</h4>
                    <p className="text-green-700">{mistake.better_alternative}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    );
  }
  
  // Render expert verdict
  if (structuredContent.expert_verdict) {
    const verdict = structuredContent.expert_verdict;
    sections.push(
      <section key="expert_verdict" className="mb-8">
        <h2 id="expert_verdict" className="text-2xl font-bold mb-4">{verdict.title || 'Expert Verdict'}</h2>
        <div className="bg-gradient-to-r from-blue-50 to-green-50 border border-blue-200 rounded-lg p-6">
          {verdict.winner && (
            <div className="text-center mb-4">
              <div className="inline-block bg-green-600 text-white px-4 py-2 rounded-full text-lg font-semibold">
                🏆 Winner: {verdict.winner}
              </div>
            </div>
          )}
          {verdict.reasoning && (
            <div className="mb-4">
              <h3 className="font-semibold text-gray-900 mb-2">Our Reasoning:</h3>
              <p className="text-gray-700">{verdict.reasoning}</p>
            </div>
          )}
          {verdict.product_id && showInlineProducts && (
            <div className="mt-4">
              <InlineProductShowcase
                productId={parseInt(verdict.product_id)}
                context={verdict.final_cta || "Our top recommendation"}
                position={1}
                ctaText="Get This Product"
                layout="horizontal"
                showFullDetails={true}
              />
            </div>
          )}
        </div>
      </section>
    );
  }
  
  // Render conclusion
  if (structuredContent.conclusion) {
    const conclusion = structuredContent.conclusion;
    sections.push(
      <section key="conclusion" className="mb-8">
        <h2 id="conclusion" className="text-2xl font-bold mb-4">Conclusion</h2>
        <div className="prose prose-lg max-w-none">
          {conclusion.summary && (
            <div className="mb-4">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {conclusion.summary}
              </ReactMarkdown>
            </div>
          )}
          {conclusion.next_steps && (
            <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
              <h3 className="font-semibold text-blue-900 mb-2">Next Steps:</h3>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {conclusion.next_steps}
              </ReactMarkdown>
            </div>
          )}
          {conclusion.final_recommendation && (
            <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
              <h3 className="font-semibold text-green-900 mb-2">Final Recommendation:</h3>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {conclusion.final_recommendation}
              </ReactMarkdown>
            </div>
          )}
          {conclusion.affiliate_cta && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-center">
              <p className="text-lg font-semibold text-yellow-800">{conclusion.affiliate_cta}</p>
            </div>
          )}
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
import React from 'react';
import { Product } from '../types';

interface ComprehensiveProductContentProps {
  product: Product;
}

interface ContentSection {
  title: string;
  icon: string;
  priority: number;
  render: () => React.ReactNode | null;
}

export default function ComprehensiveProductContent({ product }: ComprehensiveProductContentProps) {
  const content = product.content;
  const aiContent = product.ai_content;
  
  if (!content && !aiContent) return null;

  // Comprehensive content sections with proper hierarchy
  const sections: ContentSection[] = [
    // 1. OVERVIEW SECTION
    {
      title: 'Product Overview',
      icon: '📋',
      priority: 1,
      render: () => {
        const overview = content?.basic_info || aiContent?.basic_info;
        
        if (!overview) return null;
        
        return (
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 leading-relaxed">{overview}</p>
          </div>
        );
      }
    },

    {
      title: 'Usage Guidance',
      icon: '🎯',
      priority: 2,
      render: () => {
        const guidance = content?.usage_guidance || aiContent?.usage_guidance;
        
        if (!guidance) return null;
        
        return (
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 leading-relaxed">{guidance}</p>
          </div>
        );
      }
    },

    {
      title: 'Best For & Considerations',
      icon: '🎯',
      priority: 3,
      render: () => {
        const helpers = (content as any)?.comparison_helpers || (aiContent as any)?.comparison_helpers;
        if (!helpers) return null;
        
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {helpers.best_for && Array.isArray(helpers.best_for) && (
              <div className="bg-green-50 rounded-lg p-4">
                <h4 className="font-semibold text-green-900 mb-3">✅ Best For</h4>
                <ul className="space-y-2">
                  {helpers.best_for.map((item: string, index: number) => (
                    <li key={index} className="flex items-start space-x-2">
                      <span className="text-green-500 mt-0.5">✓</span>
                      <span className="text-green-800 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {helpers.not_ideal_for && Array.isArray(helpers.not_ideal_for) && (
              <div className="bg-red-50 rounded-lg p-4">
                <h4 className="font-semibold text-red-900 mb-3">❌ Not Ideal For</h4>
                <ul className="space-y-2">
                  {helpers.not_ideal_for.map((item: string, index: number) => (
                    <li key={index} className="flex items-start space-x-2">
                      <span className="text-red-500 mt-0.5">✗</span>
                      <span className="text-red-800 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        );
      }
    },

    // 2. SPECIFICATIONS SECTION  
    {
      title: 'Technical Analysis',
      icon: '🔬',
      priority: 10,
      render: () => {
        const analysis = content?.technical_analysis || aiContent?.technical_analysis;
        
        if (!analysis) return null;
        
        return (
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 leading-relaxed">{analysis}</p>
          </div>
        );
      }
    },

    {
      title: 'Professional Assessment',
      icon: '👨‍🔬',
      priority: 11,
      render: () => {
        const assessment = content?.professional_assessment || aiContent?.professional_assessment;
        
        if (!assessment) return null;
        
        return (
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 leading-relaxed">{assessment}</p>
          </div>
        );
      }
    },

    // 3. ADDITIONAL INFORMATION SECTION
    {
      title: 'Customer Reviews Summary',
      icon: '⭐',
      priority: 20,
      render: () => {
        const reviews = content?.customer_reviews || aiContent?.customer_reviews;
        
        if (!reviews) return null;
        
        return (
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 leading-relaxed">{reviews}</p>
          </div>
        );
      }
    },

    {
      title: 'Care & Maintenance',
      icon: '🔧',
      priority: 21,
      render: () => {
        const maintenance = content?.maintenance_care || aiContent?.maintenance_care;
        
        if (!maintenance) return null;
        
        return (
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 leading-relaxed">{maintenance}</p>
          </div>
        );
      }
    },

    {
      title: 'Purchase Decision Guide',
      icon: '🛒',
      priority: 22,
      render: () => {
        const decision = content?.purchase_decision || aiContent?.purchase_decision;
        
        if (!decision) return null;
        
        return (
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 leading-relaxed">{decision}</p>
          </div>
        );
      }
    },

    {
      title: 'Questions & Answers',
      icon: '❓',
      priority: 23,
      render: () => {
        // Check for Q&A at top level first (correct structure), then fallback to nested locations
        const qaData = (product as any).qa || content?.qa || content?.content_metadata?.qa || aiContent?.qa;
        if (!qaData || !Array.isArray(qaData) || qaData.length === 0) return null;
        
        return (
          <div className="space-y-4">
            {qaData.map((item: any, index: number) => (
              <div key={index} className="border-b border-gray-100 pb-4 last:border-b-0">
                <div className="font-semibold text-gray-900 mb-2">
                  Q: {item.question}
                </div>
                <div className="text-gray-700 text-sm leading-relaxed">
                  A: {item.answer}
                </div>
              </div>
            ))}
          </div>
        );
      }
    },

    {
      title: 'Setup Tips',
      icon: '🔧',
      priority: 24,
      render: () => {
        const setupTips = (product as any).setup_tips || content?.setup_tips || (aiContent as any)?.setup_tips;
        if (!setupTips || !Array.isArray(setupTips) || setupTips.length === 0) return null;
        
        return (
          <div className="space-y-3">
            {setupTips.map((tip: string, index: number) => (
              <div key={index} className="flex items-start space-x-3">
                <span className="text-blue-500 mt-1">💡</span>
                <span className="text-gray-700 text-sm">{tip}</span>
              </div>
            ))}
          </div>
        );
      }
    },

    {
      title: 'Warranty Information',
      icon: '🛡️',
      priority: 25,
      render: () => {
        const warranty = (product as any).warranty_info || content?.warranty_info || aiContent?.warranty_info;
        if (!warranty) return null;
        
        return (
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 leading-relaxed">{warranty}</p>
          </div>
        );
      }
    },


  ];

  // Filter sections that have content
  const availableSections = sections
    .filter(section => section.render() !== null)
    .sort((a, b) => a.priority - b.priority);

  if (availableSections.length === 0) return null;

  // Group by priority ranges
  const overviewSections = availableSections.filter(s => s.priority < 10);
  const specificationSections = availableSections.filter(s => s.priority >= 10 && s.priority < 20);  
  const additionalSections = availableSections.filter(s => s.priority >= 20);

  return (
    <div className="space-y-6">
      {/* 1. OVERVIEW SECTIONS */}
      {overviewSections.length > 0 && (
        <div className="space-y-4">
          <div className="card p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">📋 Overview & Guidance</h2>
            {overviewSections.map((section) => (
              <div key={section.title} className="mb-6 last:mb-0">
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                  <span className="mr-2">{section.icon}</span>
                  {section.title}
                </h3>
                {section.render()}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 2. SPECIFICATIONS SECTIONS */}
      {specificationSections.length > 0 && (
        <div className="space-y-4">
          <div className="card p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">🔬 Technical & Professional Analysis</h2>
            {specificationSections.map((section) => (
              <div key={section.title} className="mb-6 last:mb-0">
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                  <span className="mr-2">{section.icon}</span>
                  {section.title}
                </h3>
                {section.render()}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 3. ADDITIONAL INFORMATION SECTIONS */}
      {additionalSections.length > 0 && (
        <div className="space-y-4">
          {additionalSections.map((section) => (
            <details key={section.title} className="card" open>
              <summary className="px-6 py-4 border-b border-gray-200 cursor-pointer list-none hover:bg-gray-50">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                  <span className="mr-2">{section.icon}</span>
                  {section.title}
                </h3>
              </summary>
              <div className="px-6 py-4">
                {section.render()}
              </div>
            </details>
          ))}
        </div>
      )}
    </div>
  );
}
import React from 'react';

type Content = Record<string, any> | undefined | null;

interface ProductContentSectionsProps {
  content: Content;
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <details className="card" open>
      <summary className="px-6 py-4 border-b border-gray-200 cursor-pointer list-none">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      </summary>
      <div className="px-6 py-4 text-gray-700 leading-relaxed">
        {children}
      </div>
    </details>
  );
}

export default function ProductContentSections({ content }: ProductContentSectionsProps) {
  if (!content || typeof content !== 'object') return null;

  const md = content.content_metadata || {};
  const sources: string[] = md.sources || content.sources || [];
  const qaList: Array<{ question: string; answer: string }>
    = Array.isArray(md.qa) ? md.qa : [];

  // Narrative group (kept together)
  const narrative: Array<{ key: string; title: string; value?: string }>= [
    { key: 'basic_info', title: 'Overview', value: content.basic_info },
    { key: 'usage_guidance', title: 'Usage Guidance', value: content.usage_guidance },
    { key: 'customer_reviews', title: 'Customer Feedback', value: content.customer_reviews },
    { key: 'maintenance_care', title: 'Care & Maintenance', value: content.maintenance_care },
    { key: 'purchase_decision', title: 'Why Choose This', value: content.purchase_decision },
    { key: 'technical_analysis', title: 'Technical Analysis', value: content.technical_analysis },
    { key: 'professional_assessment', title: 'Professional Assessment', value: content.professional_assessment },
  ].filter(n => !!n.value);

  const ratings = (content as any).professional_ratings as undefined | {
    playability?: number; sound?: number; build?: number; value?: number; overall_score?: number; notes?: string;
  };
  const audience = (content as any).audience_fit as undefined | {
    beginners?: boolean; intermediate?: boolean; professionals?: boolean; learning_curve?: string; suitable_genres?: string[]; studio_live_role?: string;
  };
  const helpers = (content as any).comparison_helpers as undefined | {
    standout_strengths?: string[]; key_tradeoffs?: string[]; best_for?: string[]; not_ideal_for?: string[];
  };
  const catSpecific = (content as any).category_specific as undefined | { metrics?: Record<string, number> };
  const accessories = (content as any).accessory_recommendations as undefined | Array<{ name: string; why: string }>;
  const setupTips = (content as any).setup_tips as undefined | string[];
  const quickBadges = (content as any).quick_badges as undefined | Record<string, boolean>;

  return (
    <div className="space-y-6">
      {/* 1. OVERVIEW & GUIDANCE SECTION */}
      {narrative.length > 0 && (
        <details className="card" open>
          <summary className="px-6 py-4 border-b border-gray-200 cursor-pointer list-none">
            <h3 className="text-lg font-semibold text-gray-900">📝 Overview & Guidance</h3>
          </summary>
          <div className="px-6 py-4 space-y-4 text-gray-700 leading-relaxed">
            {narrative.map(n => (
              <div key={n.key}>
                <h4 className="font-semibold text-gray-900 mb-2">{n.title}</h4>
                <p className="text-sm leading-relaxed">{n.value}</p>
              </div>
            ))}
          </div>
        </details>
      )}

      {/* 2. SPECIFICATIONS & RATINGS SECTION */}
      {ratings && (
        <details className="card" open>
          <summary className="px-6 py-4 border-b border-gray-200 cursor-pointer list-none">
            <h3 className="text-lg font-semibold text-gray-900">📊 Professional Ratings</h3>
          </summary>
          <div className="px-6 py-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {['playability','sound','build','value','overall_score'].map((k) => (
                (ratings as any)[k] !== undefined && (
                  <div key={k} className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600 capitalize">{k.replace(/_/g,' ')}</span>
                      <span className="font-medium text-gray-900">{(ratings as any)[k]}</span>
                    </div>
                    <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-2 bg-brand-primary" style={{ width: `${Math.max(0, Math.min(100, Number((ratings as any)[k])))}%` }}></div>
                    </div>
                  </div>
                )
              ))}
            </div>
            {ratings.notes && (
              <p className="text-sm text-gray-600 mt-3">{ratings.notes}</p>
            )}
          </div>
        </details>
      )}

      {/* Audience Fit & Quick Badges */}
      {(audience || quickBadges) && (
        <details className="card" open>
          <summary className="px-6 py-4 border-b border-gray-200 cursor-pointer list-none">
            <h3 className="text-lg font-semibold text-gray-900">🎯 Audience & Badges</h3>
          </summary>
          <div className="px-6 py-4 grid grid-cols-1 md:grid-cols-2 gap-6">
            {audience && (
              <div className="space-y-2">
                <div className="text-sm text-gray-600">
                  <strong>Beginners:</strong> {audience.beginners ? 'Yes' : 'No'} • <strong>Intermediate:</strong> {audience.intermediate ? 'Yes' : 'No'} • <strong>Pros:</strong> {audience.professionals ? 'Yes' : 'No'}
                </div>
                {audience.learning_curve && (
                  <div className="text-sm text-gray-600"><strong>Learning curve:</strong> {audience.learning_curve}</div>
                )}
                {Array.isArray(audience.suitable_genres) && audience.suitable_genres.length > 0 && (
                  <div className="text-sm text-gray-600"><strong>Genres:</strong> {audience.suitable_genres.join(', ')}</div>
                )}
                {audience.studio_live_role && (
                  <div className="text-sm text-gray-600"><strong>Role:</strong> {audience.studio_live_role}</div>
                )}
              </div>
            )}
            {quickBadges && (
              <div className="flex flex-wrap gap-2">
                {Object.entries(quickBadges).filter(([,v]) => !!v).map(([k]) => (
                  <span key={k} className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200 capitalize">
                    {k.replace(/_/g,' ')}
                  </span>
                ))}
              </div>
            )}
          </div>
        </details>
      )}

      {/* Comparison Helpers */}
      {helpers && (
        <details className="card" open>
          <summary className="px-6 py-4 border-b border-gray-200 cursor-pointer list-none">
            <h3 className="text-lg font-semibold text-gray-900">⚖️ Strengths & Tradeoffs</h3>
          </summary>
          <div className="px-6 py-4 grid grid-cols-1 md:grid-cols-2 gap-6">
            {helpers.standout_strengths && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Standout Strengths</h4>
                <ul className="list-disc pl-5 space-y-1 text-gray-700 text-sm">
                  {helpers.standout_strengths.map((s, i) => <li key={`ss-${i}`}>{s}</li>)}
                </ul>
              </div>
            )}
            {helpers.key_tradeoffs && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Key Tradeoffs</h4>
                <ul className="list-disc pl-5 space-y-1 text-gray-700 text-sm">
                  {helpers.key_tradeoffs.map((s, i) => <li key={`kt-${i}`}>{s}</li>)}
                </ul>
              </div>
            )}
            {helpers.best_for && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Best For</h4>
                <ul className="list-disc pl-5 space-y-1 text-gray-700 text-sm">
                  {helpers.best_for.map((s, i) => <li key={`bf-${i}`}>{s}</li>)}
                </ul>
              </div>
            )}
            {helpers.not_ideal_for && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Not Ideal For</h4>
                <ul className="list-disc pl-5 space-y-1 text-gray-700 text-sm">
                  {helpers.not_ideal_for.map((s, i) => <li key={`ni-${i}`}>{s}</li>)}
                </ul>
              </div>
            )}
          </div>
        </details>
      )}

      {/* Category Metrics */}
      {catSpecific?.metrics && Object.keys(catSpecific.metrics).length > 0 && (
        <details className="card" open>
          <summary className="px-6 py-4 border-b border-gray-200 cursor-pointer list-none">
            <h3 className="text-lg font-semibold text-gray-900">📈 Category Metrics</h3>
          </summary>
          <div className="px-6 py-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(catSpecific.metrics).map(([k, v]) => (
              <div key={k} className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 capitalize">{k.replace(/_/g,' ')}</span>
                  <span className="font-medium text-gray-900">{v}</span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-2 bg-purple-500" style={{ width: `${Math.max(0, Math.min(100, Number(v)))}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </details>
      )}

      {/* 3. ADDITIONAL INFORMATION SECTION */}
      {/* Accessories & Setup Tips */}
      {(Array.isArray(accessories) && accessories.length > 0) || (Array.isArray(setupTips) && setupTips.length > 0) ? (
        <details className="card" open>
          <summary className="px-6 py-4 border-b border-gray-200 cursor-pointer list-none">
            <h3 className="text-lg font-semibold text-gray-900">🔧 Accessories & Setup Tips</h3>
          </summary>
          <div className="px-6 py-4 grid grid-cols-1 md:grid-cols-2 gap-6">
            {Array.isArray(accessories) && accessories.length > 0 && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Recommended Accessories</h4>
                <ul className="list-disc pl-5 space-y-1 text-gray-700 text-sm">
                  {accessories.map((a, i) => (
                    <li key={`acc-${i}`}><span className="font-medium">{a.name}:</span> {a.why}</li>
                  ))}
                </ul>
              </div>
            )}
            {Array.isArray(setupTips) && setupTips.length > 0 && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Setup Tips</h4>
                <ul className="list-disc pl-5 space-y-1 text-gray-700 text-sm">
                  {setupTips.map((t, i) => (<li key={`tip-${i}`}>{t}</li>))}
                </ul>
              </div>
            )}
          </div>
        </details>
      ) : null}

      {/* Q&A */}
      {qaList.length > 0 && (
        <details className="card" open>
          <summary className="px-6 py-4 border-b border-gray-200 cursor-pointer list-none">
            <h3 className="text-lg font-semibold text-gray-900">❓ Questions & Answers</h3>
          </summary>
          <div className="px-6 py-4 space-y-4">
            {qaList.map((qa, idx) => (
              <div key={idx} className="border-b border-gray-100 pb-3 last:border-b-0">
                <div className="font-semibold text-gray-900">Q: {qa.question}</div>
                <div className="text-gray-700">A: {qa.answer}</div>
              </div>
            ))}
          </div>
        </details>
      )}

      {/* Warranty & Sources */}
      {(content.warranty_info || (Array.isArray(sources) && sources.length > 0)) && (
        <details className="card" open>
          <summary className="px-6 py-4 border-b border-gray-200 cursor-pointer list-none">
            <h3 className="text-lg font-semibold text-gray-900">📜 Warranty & Sources</h3>
          </summary>
          <div className="px-6 py-4 space-y-3 text-sm">
            {content.warranty_info && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Warranty Information</h4>
                <p className="text-gray-700">{content.warranty_info}</p>
              </div>
            )}
            {Array.isArray(sources) && sources.length > 0 && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Sources</h4>
                <ul className="list-disc pl-5 space-y-1 text-gray-700">
                  {sources.map((s, i) => (<li key={`src-${i}`}>{String(s)}</li>))}
                </ul>
              </div>
            )}
          </div>
        </details>
      )}

    </div>
  );
}

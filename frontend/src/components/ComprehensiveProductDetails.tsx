'use client';

import React from 'react';
import { Product, ComprehensiveAIContent } from '@/types';

interface ComprehensiveProductDetailsProps {
  product: Product;
}

export default function ComprehensiveProductDetails({ product }: ComprehensiveProductDetailsProps) {
  const aiContent = product.ai_content;

  if (!aiContent) {
    return (
      <div className="bg-white rounded-lg shadow-elegant border border-primary-200 p-6">
        <p className="text-primary-500 text-center">Detailed information not available for this product.</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Basic Information */}
      <section className="bg-white rounded-lg shadow-elegant border border-primary-200 p-6">
        <h2 className="text-2xl font-bold text-primary-900 mb-4">Overview</h2>
        <div className="space-y-4">
          <p className="text-primary-700 leading-relaxed">{aiContent.basic_info.overview}</p>
          
          <div>
            <h3 className="text-lg font-semibold text-primary-900 mb-2">Key Features</h3>
            <ul className="list-disc list-inside space-y-1 text-primary-700">
              {aiContent.basic_info.key_features.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <span className="text-sm font-medium text-primary-500">Skill Level</span>
              <p className="text-primary-900">{aiContent.basic_info.target_skill_level}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-500">Origin</span>
              <p className="text-primary-900">{aiContent.basic_info.country_of_origin}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-500">Release Year</span>
              <p className="text-primary-900">{aiContent.basic_info.release_year}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Technical Analysis */}
      <section className="bg-white rounded-lg shadow-elegant border border-primary-200 p-6">
        <h2 className="text-2xl font-bold text-primary-900 mb-4">Technical Analysis</h2>
        
        {/* Sound Characteristics */}
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-primary-900 mb-3">Sound Characteristics</h3>
          <div className="space-y-3">
            <div>
              <span className="text-sm font-medium text-primary-500">Tonal Profile</span>
              <p className="text-primary-700">{aiContent.technical_analysis.sound_characteristics.tonal_profile}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-500">Output Level</span>
              <p className="text-primary-700">{aiContent.technical_analysis.sound_characteristics.output_level}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-500">Best Genres</span>
              <div className="flex flex-wrap gap-2 mt-1">
                {aiContent.technical_analysis.sound_characteristics.best_genres.map((genre, index) => (
                  <span key={index} className="px-2 py-1 bg-primary-100 text-primary-800 text-sm rounded-full">
                    {genre}
                  </span>
                ))}
              </div>
            </div>
            {aiContent.technical_analysis.sound_characteristics.pickup_positions && (
              <div>
                <span className="text-sm font-medium text-primary-500">Pickup Positions</span>
                <div className="space-y-2 mt-2">
                  {Object.entries(aiContent.technical_analysis.sound_characteristics.pickup_positions).map(([position, description]) => (
                    <div key={position} className="pl-4 border-l-2 border-primary-200">
                      <span className="text-sm font-medium text-primary-600 capitalize">{position.replace(/_/g, ' ')}:</span>
                      <p className="text-primary-700 text-sm">{description}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Build Quality */}
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-primary-900 mb-3">Build Quality</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <span className="text-sm font-medium text-primary-500">Construction Type</span>
              <p className="text-primary-700">{aiContent.technical_analysis.build_quality.construction_type}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-500">Hardware Quality</span>
              <p className="text-primary-700">{aiContent.technical_analysis.build_quality.hardware_quality}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-500">Finish Quality</span>
              <p className="text-primary-700">{aiContent.technical_analysis.build_quality.finish_quality}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-500">Expected Durability</span>
              <p className="text-primary-700">{aiContent.technical_analysis.build_quality.expected_durability}</p>
            </div>
          </div>
        </div>

        {/* Playability */}
        <div>
          <h3 className="text-xl font-semibold text-primary-900 mb-3">Playability</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <span className="text-sm font-medium text-primary-500">Neck Profile</span>
              <p className="text-primary-700">{aiContent.technical_analysis.playability.neck_profile}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-500">Action Setup</span>
              <p className="text-primary-700">{aiContent.technical_analysis.playability.action_setup}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-500">Comfort Rating</span>
              <p className="text-primary-700">{aiContent.technical_analysis.playability.comfort_rating}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-500">Weight Category</span>
              <p className="text-primary-700">{aiContent.technical_analysis.playability.weight_category}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Purchase Decision */}
      <section className="bg-white rounded-lg shadow-elegant border border-primary-200 p-6">
        <h2 className="text-2xl font-bold text-primary-900 mb-4">Purchase Decision Guide</h2>
        
        {/* Why Buy */}
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-success-700 mb-3">Why Buy This Product</h3>
          <div className="space-y-3">
            {aiContent.purchase_decision.why_buy.map((reason, index) => (
              <div key={index} className="p-4 bg-success-50 border border-success-200 rounded-lg">
                <h4 className="font-semibold text-success-800 mb-1">{reason.title}</h4>
                <p className="text-success-700">{reason.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Why Not Buy */}
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-error-700 mb-3">Considerations</h3>
          <div className="space-y-3">
            {aiContent.purchase_decision.why_not_buy.map((reason, index) => (
              <div key={index} className="p-4 bg-error-50 border border-error-200 rounded-lg">
                <h4 className="font-semibold text-error-800 mb-1">{reason.title}</h4>
                <p className="text-error-700">{reason.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Best For */}
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-primary-700 mb-3">Best For</h3>
          <div className="space-y-3">
            {aiContent.purchase_decision.best_for.map((userType, index) => (
              <div key={index} className="p-4 bg-primary-50 border border-primary-200 rounded-lg">
                <h4 className="font-semibold text-primary-800 mb-1">{userType.user_type}</h4>
                <p className="text-primary-700">{userType.reason}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Not Ideal For */}
        <div>
          <h3 className="text-xl font-semibold text-warning-700 mb-3">Not Ideal For</h3>
          <div className="space-y-3">
            {aiContent.purchase_decision.not_ideal_for.map((userType, index) => (
              <div key={index} className="p-4 bg-warning-50 border border-warning-200 rounded-lg">
                <h4 className="font-semibold text-warning-800 mb-1">{userType.user_type}</h4>
                <p className="text-warning-700">{userType.reason}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Usage Guidance */}
      <section className="bg-white rounded-lg shadow-elegant border border-primary-200 p-6">
        <h2 className="text-2xl font-bold text-primary-900 mb-4">Usage Guidance</h2>
        
        {/* Recommended Amplifiers */}
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-primary-900 mb-3">Recommended Amplifiers</h3>
          <div className="flex flex-wrap gap-2">
            {aiContent.usage_guidance.recommended_amplifiers.map((amp, index) => (
              <span key={index} className="px-3 py-1 bg-accent-100 text-accent-800 text-sm rounded-full">
                {amp}
              </span>
            ))}
          </div>
        </div>

        {/* Suitable Music Styles */}
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-primary-900 mb-3">Suitable Music Styles</h3>
          <div className="space-y-3">
            <div>
              <span className="text-sm font-medium text-success-600">Excellent for:</span>
              <div className="flex flex-wrap gap-2 mt-1">
                {aiContent.usage_guidance.suitable_music_styles.excellent.map((style, index) => (
                  <span key={index} className="px-2 py-1 bg-success-100 text-success-800 text-sm rounded-full">
                    {style}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-600">Good for:</span>
              <div className="flex flex-wrap gap-2 mt-1">
                {aiContent.usage_guidance.suitable_music_styles.good.map((style, index) => (
                  <span key={index} className="px-2 py-1 bg-primary-100 text-primary-800 text-sm rounded-full">
                    {style}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-warning-600">Limited for:</span>
              <div className="flex flex-wrap gap-2 mt-1">
                {aiContent.usage_guidance.suitable_music_styles.limited.map((style, index) => (
                  <span key={index} className="px-2 py-1 bg-warning-100 text-warning-800 text-sm rounded-full">
                    {style}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Skill Development */}
        <div>
          <h3 className="text-xl font-semibold text-primary-900 mb-3">Skill Development</h3>
          <div className="space-y-3">
            <div>
              <span className="text-sm font-medium text-primary-500">Learning Curve</span>
              <p className="text-primary-700">{aiContent.usage_guidance.skill_development.learning_curve}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-primary-500">Growth Potential</span>
              <p className="text-primary-700">{aiContent.usage_guidance.skill_development.growth_potential}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Maintenance & Care */}
      <section className="bg-white rounded-lg shadow-elegant border border-primary-200 p-6">
        <h2 className="text-2xl font-bold text-primary-900 mb-4">Maintenance & Care</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-xl font-semibold text-primary-900 mb-3">Care Instructions</h3>
            <div className="space-y-3">
              <div>
                <span className="text-sm font-medium text-primary-500">Daily</span>
                <p className="text-primary-700 text-sm">{aiContent.maintenance_care.care_instructions.daily}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-primary-500">Weekly</span>
                <p className="text-primary-700 text-sm">{aiContent.maintenance_care.care_instructions.weekly}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-primary-500">Monthly</span>
                <p className="text-primary-700 text-sm">{aiContent.maintenance_care.care_instructions.monthly}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-primary-500">Annual</span>
                <p className="text-primary-700 text-sm">{aiContent.maintenance_care.care_instructions.annual}</p>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-primary-900 mb-3">Upgrade Potential</h3>
            <div className="space-y-3">
              <div>
                <span className="text-sm font-medium text-primary-500">Easy Upgrades</span>
                <ul className="list-disc list-inside text-sm text-primary-700 mt-1">
                  {aiContent.maintenance_care.upgrade_potential.easy_upgrades.map((upgrade, index) => (
                    <li key={index}>{upgrade}</li>
                  ))}
                </ul>
              </div>
              <div>
                <span className="text-sm font-medium text-primary-500">Recommended Budget</span>
                <p className="text-primary-700">{aiContent.maintenance_care.upgrade_potential.recommended_budget}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6">
          <h3 className="text-xl font-semibold text-primary-900 mb-3">Common Issues</h3>
          <div className="flex flex-wrap gap-2">
            {aiContent.maintenance_care.common_issues.map((issue, index) => (
              <span key={index} className="px-3 py-1 bg-warning-100 text-warning-800 text-sm rounded-full">
                {issue}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Professional Assessment */}
      <section className="bg-white rounded-lg shadow-elegant border border-primary-200 p-6">
        <h2 className="text-2xl font-bold text-primary-900 mb-4">Professional Assessment</h2>
        
        {/* Expert Ratings */}
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-primary-900 mb-3">Expert Ratings</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-primary-50 rounded-lg">
              <div className="text-2xl font-bold text-success-600">{aiContent.professional_assessment.expert_rating.build_quality}/10</div>
              <div className="text-sm text-primary-600">Build Quality</div>
            </div>
            <div className="text-center p-4 bg-primary-50 rounded-lg">
              <div className="text-2xl font-bold text-accent-600">{aiContent.professional_assessment.expert_rating.sound_quality}/10</div>
              <div className="text-sm text-primary-600">Sound Quality</div>
            </div>
            <div className="text-center p-4 bg-primary-50 rounded-lg">
              <div className="text-2xl font-bold text-warning-600">{aiContent.professional_assessment.expert_rating.value_for_money}/10</div>
              <div className="text-sm text-primary-600">Value for Money</div>
            </div>
            <div className="text-center p-4 bg-primary-50 rounded-lg">
              <div className="text-2xl font-bold text-primary-600">{aiContent.professional_assessment.expert_rating.versatility}/10</div>
              <div className="text-sm text-primary-600">Versatility</div>
            </div>
          </div>
        </div>

        {/* Standout Features */}
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-success-700 mb-3">Standout Features</h3>
          <div className="flex flex-wrap gap-2">
            {aiContent.professional_assessment.standout_features.map((feature, index) => (
              <span key={index} className="px-3 py-1 bg-success-100 text-success-800 text-sm rounded-full">
                {feature}
              </span>
            ))}
          </div>
        </div>

        {/* Notable Limitations */}
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-warning-700 mb-3">Notable Limitations</h3>
          <div className="flex flex-wrap gap-2">
            {aiContent.professional_assessment.notable_limitations.map((limitation, index) => (
              <span key={index} className="px-3 py-1 bg-warning-100 text-warning-800 text-sm rounded-full">
                {limitation}
              </span>
            ))}
          </div>
        </div>

        {/* Competitive Position */}
        <div>
          <h3 className="text-xl font-semibold text-primary-900 mb-3">Competitive Position</h3>
          <p className="text-primary-700 leading-relaxed">{aiContent.professional_assessment.competitive_position}</p>
        </div>
      </section>
    </div>
  );
}

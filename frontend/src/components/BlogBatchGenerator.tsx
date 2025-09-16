import React, { useState, useEffect } from 'react';
import { BlogGenerationTemplate, BlogCategory } from '../types/blog';

interface BatchGenerationRequest {
  template_id: number;
  category_ids: number[];
  product_combinations: number[][];
  target_word_count: number;
  batch_size: number;
  auto_schedule: boolean;
  publishing_schedule?: {
    start_date: string;
    frequency: 'daily' | 'weekly' | 'bi-weekly';
    time_of_day: string;
  };
}

interface BlogBatchGeneratorProps {
  onClose: () => void;
}

const PROXY_BASE = '/api/proxy/v1';

export default function BlogBatchGenerator({ onClose }: BlogBatchGeneratorProps) {
  const [templates, setTemplates] = useState<BlogGenerationTemplate[]>([]);
  const [categories, setCategories] = useState<BlogCategory[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  
  const [batchConfig, setBatchConfig] = useState<BatchGenerationRequest>({
    template_id: 0,
    category_ids: [],
    product_combinations: [],
    target_word_count: 2500,
    batch_size: 10,
    auto_schedule: false,
  });

  // Pre-defined high-converting product combinations
  const HIGH_VALUE_COMBINATIONS = {
    'Electric Guitars': [
      [376, 619, 253], // Fender Player II, Gibson LP, Harley Benton
      [602, 655, 267], // Premium electrics
      [264, 305, 297], // Budget to mid-range
    ],
    'Digital Pianos': [
      [370, 361, 365], // Yamaha CLP-835, Casio PX series
      [589, 697, 722], // Budget digital pianos
      [581, 596, 630], // Premium models
    ],
    'Acoustic Guitars': [
      [186, 197, 232], // Taylor vs Martin comparison
      [155, 190, 199], // Beginner acoustics
      [220, 222, 230], // Mid-range acoustics
    ],
    'Bass Guitars': [
      [381, 309, 502], // Fender P vs J bass
      [482, 484, 551], // Beginner basses
      [314, 335, 343], // 5-string basses
    ],
    'Synthesizers': [
      [507, 508, 514], // Beginner synths
      [506, 521, 964], // Professional synths
      [477, 519, 762], // Budget synths
    ],
  };

  const BLOG_TEMPLATES = [
    {
      id: 1,
      name: 'Ultimate Buying Guide 2025',
      description: 'Comprehensive buying guides with 5-7 products, 2500+ words',
      conversion_rate: 8.5,
      word_count: 2500,
    },
    {
      id: 2,
      name: 'Head-to-Head Comparison',
      description: 'Direct product comparisons, 2000 words',
      conversion_rate: 12.3,
      word_count: 2000,
    },
    {
      id: 3,
      name: 'Best Budget Options',
      description: 'Budget-focused roundups under $500',
      conversion_rate: 6.8,
      word_count: 1800,
    },
    {
      id: 4,
      name: 'Professional Review',
      description: 'In-depth single product reviews',
      conversion_rate: 9.2,
      word_count: 2200,
    },
    {
      id: 5,
      name: 'Seasonal Deal Roundup',
      description: 'Time-sensitive deal collections',
      conversion_rate: 15.6,
      word_count: 2000,
    },
  ];

  useEffect(() => {
    loadTemplatesAndCategories();
  }, []);

  const loadTemplatesAndCategories = async () => {
    try {
      const [templatesRes, categoriesRes] = await Promise.all([
        fetch(`${PROXY_BASE}/blog/templates`),
        fetch(`${PROXY_BASE}/blog/categories`),
      ]);

      if (templatesRes.ok) {
        const templatesData = await templatesRes.json();
        setTemplates(templatesData);
      }

      if (categoriesRes.ok) {
        const categoriesData = await categoriesRes.json();
        setCategories(categoriesData);
      }
    } catch (error) {
      console.error('Failed to load templates and categories:', error);
    }
  };

  const generateBatchPosts = async () => {
    if (!batchConfig.template_id || batchConfig.category_ids.length === 0) {
      alert('Please select a template and at least one category');
      return;
    }

    setIsGenerating(true);
    
    try {
      const batchRequests = buildBatchRequests();
      
      const response = await fetch(`${PROXY_BASE}/admin/blog/batch/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          requests: batchRequests,
          batch_size: batchConfig.batch_size,
          auto_schedule: batchConfig.auto_schedule,
          publishing_schedule: batchConfig.publishing_schedule,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Batch generation started! ${result.batch_count} batches created with ${result.total_posts} posts.`);
        onClose();
      } else {
        throw new Error('Batch generation failed');
      }
    } catch (error) {
      console.error('Batch generation error:', error);
      alert('Failed to start batch generation. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const buildBatchRequests = () => {
    const requests: any[] = [];
    
    for (const categoryId of batchConfig.category_ids) {
      const category = categories.find(c => c.id === categoryId);
      if (!category) continue;

      const combinations = HIGH_VALUE_COMBINATIONS[category.name as keyof typeof HIGH_VALUE_COMBINATIONS] || [[]];
      
      combinations.forEach((productIds, index) => {
        if (requests.length >= batchConfig.batch_size) return;
        
        requests.push({
          custom_id: `${category.slug}-${batchConfig.template_id}-${index}`,
          template_id: batchConfig.template_id,
          category_id: categoryId,
          product_ids: productIds,
          target_word_count: batchConfig.target_word_count,
          generation_params: {
            model: 'gpt-4o',
            temperature: 0.7,
          },
        });
      });
    }

    return requests;
  };

  const addProductCombination = () => {
    setBatchConfig(prev => ({
      ...prev,
      product_combinations: [...prev.product_combinations, []],
    }));
  };

  const updateProductCombination = (index: number, productIds: number[]) => {
    setBatchConfig(prev => ({
      ...prev,
      product_combinations: prev.product_combinations.map((combo, i) => 
        i === index ? productIds : combo
      ),
    }));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900">🚀 Batch Blog Generator</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p className="text-gray-600 mt-2">Generate multiple high-quality blog posts automatically</p>
        </div>

        <div className="p-6">
          {/* Step Indicator */}
          <div className="flex items-center justify-center mb-8">
            {[1, 2, 3].map((step) => (
              <div key={step} className="flex items-center">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                  currentStep >= step 
                    ? 'bg-brand-primary text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}>
                  {step}
                </div>
                {step < 3 && (
                  <div className={`w-20 h-1 mx-4 ${
                    currentStep > step ? 'bg-brand-primary' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            ))}
          </div>

          {/* Step 1: Template Selection */}
          {currentStep === 1 && (
            <div className="space-y-6">
              <h3 className="text-xl font-bold text-gray-900">Choose Template Type</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {BLOG_TEMPLATES.map((template) => (
                  <div
                    key={template.id}
                    onClick={() => setBatchConfig(prev => ({ ...prev, template_id: template.id }))}
                    className={`p-6 rounded-xl border-2 cursor-pointer transition-all duration-300 ${
                      batchConfig.template_id === template.id
                        ? 'border-brand-primary bg-brand-primary/5'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-semibold text-gray-900">{template.name}</h4>
                      <span className="text-green-600 font-bold text-sm">
                        {template.conversion_rate}% CVR
                      </span>
                    </div>
                    <p className="text-gray-600 text-sm mb-2">{template.description}</p>
                    <div className="text-xs text-gray-500">
                      Target: {template.word_count} words
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="flex justify-end">
                <button
                  onClick={() => setCurrentStep(2)}
                  disabled={!batchConfig.template_id}
                  className="px-6 py-3 bg-brand-primary text-white font-semibold rounded-xl disabled:opacity-50 disabled:cursor-not-allowed hover:bg-brand-dark transition-colors"
                >
                  Next: Categories
                </button>
              </div>
            </div>
          )}

          {/* Step 2: Category & Product Selection */}
          {currentStep === 2 && (
            <div className="space-y-6">
              <h3 className="text-xl font-bold text-gray-900">Select Categories & Products</h3>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Target Categories (Select multiple for variety)
                </label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {categories.map((category) => (
                    <label
                      key={category.id}
                      className="flex items-center p-3 rounded-lg border border-gray-200 hover:bg-gray-50 cursor-pointer"
                    >
                      <input
                        type="checkbox"
                        checked={batchConfig.category_ids.includes(category.id)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setBatchConfig(prev => ({
                              ...prev,
                              category_ids: [...prev.category_ids, category.id],
                            }));
                          } else {
                            setBatchConfig(prev => ({
                              ...prev,
                              category_ids: prev.category_ids.filter(id => id !== category.id),
                            }));
                          }
                        }}
                        className="mr-3"
                      />
                      <div>
                        <span className="text-lg mr-2">{category.icon}</span>
                        <span className="font-medium">{category.name}</span>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">🎯 Smart Product Selection</h4>
                <p className="text-blue-800 text-sm">
                  We'll automatically use our highest-converting product combinations for each category. 
                  These combinations are optimized based on affiliate performance data.
                </p>
              </div>

              <div className="flex justify-between">
                <button
                  onClick={() => setCurrentStep(1)}
                  className="px-6 py-3 bg-gray-200 text-gray-700 font-semibold rounded-xl hover:bg-gray-300 transition-colors"
                >
                  Back
                </button>
                <button
                  onClick={() => setCurrentStep(3)}
                  disabled={batchConfig.category_ids.length === 0}
                  className="px-6 py-3 bg-brand-primary text-white font-semibold rounded-xl disabled:opacity-50 disabled:cursor-not-allowed hover:bg-brand-dark transition-colors"
                >
                  Next: Settings
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Batch Settings */}
          {currentStep === 3 && (
            <div className="space-y-6">
              <h3 className="text-xl font-bold text-gray-900">Batch Configuration</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Target Word Count
                  </label>
                  <select
                    value={batchConfig.target_word_count}
                    onChange={(e) => setBatchConfig(prev => ({ 
                      ...prev, 
                      target_word_count: Number(e.target.value) 
                    }))}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                  >
                    <option value={1500}>1,500 words (Quick Articles)</option>
                    <option value={2000}>2,000 words (Standard)</option>
                    <option value={2500}>2,500 words (Comprehensive)</option>
                    <option value={3000}>3,000 words (Ultimate Guides)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Batch Size
                  </label>
                  <select
                    value={batchConfig.batch_size}
                    onChange={(e) => setBatchConfig(prev => ({ 
                      ...prev, 
                      batch_size: Number(e.target.value) 
                    }))}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                  >
                    <option value={5}>5 posts (Small batch)</option>
                    <option value={10}>10 posts (Recommended)</option>
                    <option value={20}>20 posts (Large batch)</option>
                    <option value={50}>50 posts (Mega batch)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={batchConfig.auto_schedule}
                    onChange={(e) => setBatchConfig(prev => ({ 
                      ...prev, 
                      auto_schedule: e.target.checked 
                    }))}
                    className="mr-3"
                  />
                  <span className="font-medium">Auto-schedule publishing</span>
                </label>
                <p className="text-gray-600 text-sm mt-1">
                  Automatically publish posts over time for consistent content flow
                </p>
              </div>

              {batchConfig.auto_schedule && (
                <div className="bg-gray-50 p-4 rounded-lg space-y-4">
                  <h4 className="font-semibold">Publishing Schedule</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Start Date
                      </label>
                      <input
                        type="date"
                        value={batchConfig.publishing_schedule?.start_date || ''}
                        onChange={(e) => setBatchConfig(prev => ({
                          ...prev,
                          publishing_schedule: {
                            ...prev.publishing_schedule,
                            start_date: e.target.value,
                            frequency: 'weekly',
                            time_of_day: '09:00',
                          },
                        }))}
                        className="w-full p-2 border border-gray-300 rounded"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Frequency
                      </label>
                      <select
                        value={batchConfig.publishing_schedule?.frequency || 'weekly'}
                        onChange={(e) => setBatchConfig(prev => ({
                          ...prev,
                          publishing_schedule: {
                            ...prev.publishing_schedule!,
                            frequency: e.target.value as 'daily' | 'weekly' | 'bi-weekly',
                          },
                        }))}
                        className="w-full p-2 border border-gray-300 rounded"
                      >
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="bi-weekly">Bi-weekly</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Time
                      </label>
                      <input
                        type="time"
                        value={batchConfig.publishing_schedule?.time_of_day || '09:00'}
                        onChange={(e) => setBatchConfig(prev => ({
                          ...prev,
                          publishing_schedule: {
                            ...prev.publishing_schedule!,
                            time_of_day: e.target.value,
                          },
                        }))}
                        className="w-full p-2 border border-gray-300 rounded"
                      />
                    </div>
                  </div>
                </div>
              )}

              <div className="flex justify-between">
                <button
                  onClick={() => setCurrentStep(2)}
                  className="px-6 py-3 bg-gray-200 text-gray-700 font-semibold rounded-xl hover:bg-gray-300 transition-colors"
                >
                  Back
                </button>
                <button
                  onClick={generateBatchPosts}
                  disabled={isGenerating}
                  className="px-8 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white font-bold rounded-xl hover:from-green-600 hover:to-green-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isGenerating ? (
                    <div className="flex items-center">
                      <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full mr-2" />
                      Generating...
                    </div>
                  ) : (
                    `🚀 Generate ${batchConfig.batch_size} Posts`
                  )}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
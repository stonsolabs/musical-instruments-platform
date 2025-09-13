import React, { useState, useEffect } from 'react';
import { Product } from '../types';
import { searchProducts } from '../lib/api';
import { 
  SparklesIcon, 
  CogIcon, 
  ClockIcon, 
  DocumentTextIcon,
  XMarkIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

interface BlogGenerationTemplate {
  id: number;
  name: string;
  description?: string;
  template_type: string;
  min_products: number;
  max_products: number;
  suggested_tags: string[];
  content_structure: any;
}

interface BlogAIGeneratorProps {
  isOpen: boolean;
  onClose: () => void;
  onGenerated?: (result: any) => void;
}

interface GenerationResult {
  success: boolean;
  blog_post_id?: number;
  generated_title?: string;
  generated_content?: string;
  error_message?: string;
  tokens_used?: number;
  generation_time_ms?: number;
}

const PROXY_BASE = '/api/proxy/v1';
const ADMIN_API_BASE = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net'}/api/v1`;

export default function BlogAIGenerator({ isOpen, onClose, onGenerated }: BlogAIGeneratorProps) {
  const [templates, setTemplates] = useState<BlogGenerationTemplate[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<BlogGenerationTemplate | null>(null);
  const [selectedProducts, setSelectedProducts] = useState<Product[]>([]);
  const [productSearch, setProductSearch] = useState('');
  const [searchResults, setSearchResults] = useState<Product[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationResult, setGenerationResult] = useState<GenerationResult | null>(null);
  
  const [formData, setFormData] = useState({
    title: '',
    category_id: 0,
    custom_prompt_additions: '',
    target_word_count: 800,
    include_seo_optimization: true,
    auto_publish: false,
    generation_params: {
      temperature: 0.7,
      model: 'gpt-4o'
    }
  });

  useEffect(() => {
    if (isOpen) {
      fetchTemplates();
    }
  }, [isOpen]);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (productSearch.trim().length >= 2) {
        handleProductSearch(productSearch);
      } else {
        setSearchResults([]);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [productSearch]);

  const fetchTemplates = async () => {
    try {
      const adminToken = typeof window !== 'undefined' ? sessionStorage.getItem('adminToken') : null;
      const response = await fetch(`${ADMIN_API_BASE}/admin/blog/templates`, { credentials: 'include', headers: { ...(adminToken ? { 'X-Admin-Token': adminToken } : {}) } });
      if (response.ok) {
        const data = await response.json();
        setTemplates(data);
      }
    } catch (error) {
      console.error('Failed to fetch templates:', error);
    }
  };

  const handleProductSearch = async (query: string) => {
    try {
      const results = await searchProducts(query, 10);
      setSearchResults(results);
    } catch (error) {
      console.error('Product search failed:', error);
      setSearchResults([]);
    }
  };

  const addProduct = (product: Product) => {
    if (!selectedProducts.find(p => p.id === product.id)) {
      setSelectedProducts([...selectedProducts, product]);
    }
    setProductSearch('');
    setSearchResults([]);
  };

  const removeProduct = (productId: number) => {
    setSelectedProducts(selectedProducts.filter(p => p.id !== productId));
  };

  const handleGenerate = async () => {
    if (!selectedTemplate) {
      alert('Please select a template');
      return;
    }

    setIsGenerating(true);
    setGenerationResult(null);

    try {
      const requestData = {
        template_id: selectedTemplate.id,
        title: formData.title || undefined,
        category_id: formData.category_id || undefined,
        product_ids: selectedProducts.map(p => p.id),
        custom_prompt_additions: formData.custom_prompt_additions || undefined,
        target_word_count: formData.target_word_count,
        include_seo_optimization: formData.include_seo_optimization,
        auto_publish: formData.auto_publish,
        generation_params: formData.generation_params
      };

      const adminToken = typeof window !== 'undefined' ? sessionStorage.getItem('adminToken') : null;
      const response = await fetch(`${ADMIN_API_BASE}/admin/blog/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(adminToken ? { 'X-Admin-Token': adminToken } : {})
        },
        credentials: 'include',
        body: JSON.stringify(requestData),
      });

      const result = await response.json();
      setGenerationResult(result);

      if (result.success) {
        onGenerated?.(result);
        setTimeout(() => {
          onClose();
          // Reset form
          setSelectedTemplate(null);
          setSelectedProducts([]);
          setFormData({
            title: '',
            category_id: 0,
            custom_prompt_additions: '',
            target_word_count: 800,
            include_seo_optimization: true,
            auto_publish: false,
            generation_params: {
              temperature: 0.7,
              model: 'gpt-4o'
            }
          });
        }, 3000);
      }
    } catch (error) {
      console.error('Generation failed:', error);
      setGenerationResult({
        success: false,
        error_message: 'Network error occurred'
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    if (name.startsWith('generation_params.')) {
      const paramName = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        generation_params: {
          ...prev.generation_params,
          [paramName]: type === 'number' ? parseFloat(value) : value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : 
                type === 'number' ? parseInt(value) : value
      }));
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50">
      <div className="flex min-h-screen items-center justify-center px-4">
        <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <SparklesIcon className="w-8 h-8 text-brand-primary" />
              <div>
                <h2 className="text-2xl font-bold text-gray-900">AI Blog Generator</h2>
                <p className="text-sm text-gray-500">Generate engaging blog posts with AI assistance</p>
              </div>
            </div>
            <button
              type="button"
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>

          {/* Generation Result */}
          {generationResult && (
            <div className={`mx-6 mt-6 p-4 rounded-lg ${
              generationResult.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
            }`}>
              <div className="flex items-center space-x-2">
                {generationResult.success ? (
                  <CheckCircleIcon className="w-5 h-5 text-green-600" />
                ) : (
                  <ExclamationTriangleIcon className="w-5 h-5 text-red-600" />
                )}
                <p className={`font-medium ${generationResult.success ? 'text-green-800' : 'text-red-800'}`}>
                  {generationResult.success ? 'Blog post generated successfully!' : 'Generation failed'}
                </p>
              </div>
              {generationResult.success && generationResult.generated_title && (
                <p className="mt-2 text-sm text-green-700">
                  <strong>Title:</strong> {generationResult.generated_title}
                </p>
              )}
              {generationResult.error_message && (
                <p className="mt-2 text-sm text-red-700">{generationResult.error_message}</p>
              )}
              {generationResult.tokens_used && (
                <p className="mt-2 text-xs text-gray-500">
                  Tokens used: {generationResult.tokens_used} | 
                  Time: {generationResult.generation_time_ms}ms
                </p>
              )}
            </div>
          )}

          {/* Form */}
          <div className="p-6 space-y-6">
            {/* Template Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Generation Template *
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {templates.map((template) => (
                  <div
                    key={template.id}
                    className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                      selectedTemplate?.id === template.id
                        ? 'border-brand-primary bg-brand-accent'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => setSelectedTemplate(template)}
                  >
                    <h4 className="font-medium text-gray-900">{template.name}</h4>
                    {template.description && (
                      <p className="text-sm text-gray-600 mt-1">{template.description}</p>
                    )}
                    <div className="flex items-center justify-between mt-2">
                      <span className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded-full">
                        {template.template_type.replace('_', ' ')}
                      </span>
                      <span className="text-xs text-gray-500">
                        {template.min_products}-{template.max_products} products
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {selectedTemplate && (
              <>
                {/* Basic Settings */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Custom Title (Optional)
                    </label>
                    <input
                      type="text"
                      name="title"
                      value={formData.title}
                      onChange={handleChange}
                      placeholder="Leave empty to generate automatically"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Target Word Count
                    </label>
                    <input
                      type="number"
                      name="target_word_count"
                      value={formData.target_word_count}
                      onChange={handleChange}
                      min="300"
                      max="3000"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                    />
                  </div>
                </div>

                {/* Product Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Featured Products ({selectedProducts.length}/{selectedTemplate.max_products})
                  </label>
                  
                  {/* Selected Products */}
                  {selectedProducts.length > 0 && (
                    <div className="mb-4 space-y-2">
                      {selectedProducts.map((product) => (
                        <div key={product.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                          <div>
                            <span className="font-medium">{product.name}</span>
                            <span className="text-gray-500 ml-2">by {product.brand.name}</span>
                          </div>
                          <button
                            type="button"
                            onClick={() => removeProduct(product.id)}
                            className="text-red-500 hover:text-red-700"
                          >
                            <XMarkIcon className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Product Search */}
                  {selectedProducts.length < selectedTemplate.max_products && (
                    <div className="relative">
                      <input
                        type="text"
                        value={productSearch}
                        onChange={(e) => setProductSearch(e.target.value)}
                        placeholder="Search products to feature..."
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                      />
                      
                      {/* Search Results */}
                      {searchResults.length > 0 && (
                        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                          {searchResults.map((product) => (
                            <button
                              key={product.id}
                              type="button"
                              onClick={() => addProduct(product)}
                              className="w-full px-4 py-3 text-left hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
                            >
                              <div className="font-medium">{product.name}</div>
                              <div className="text-sm text-gray-500">{product.brand.name} • {product.category.name}</div>
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {selectedProducts.length < selectedTemplate.min_products && (
                    <p className="text-sm text-amber-600 mt-2">
                      ⚠️ This template requires at least {selectedTemplate.min_products} products
                    </p>
                  )}
                </div>

                {/* Custom Prompt Additions */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Additional Instructions (Optional)
                  </label>
                  <textarea
                    name="custom_prompt_additions"
                    rows={3}
                    value={formData.custom_prompt_additions}
                    onChange={handleChange}
                    placeholder="Add any specific requirements or focus areas..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                  />
                </div>

                {/* Advanced Settings */}
                <div className="border-t border-gray-200 pt-6">
                  <div className="flex items-center space-x-2 mb-4">
                    <CogIcon className="w-5 h-5 text-gray-500" />
                    <h3 className="text-lg font-medium text-gray-900">Advanced Settings</h3>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        AI Model
                      </label>
                      <select
                        name="generation_params.model"
                        value={formData.generation_params.model}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                      >
                        <option value="gpt-4o">GPT-4o (Recommended)</option>
                        <option value="gpt-4-turbo">GPT-4 Turbo</option>
                        <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Creativity (Temperature)
                      </label>
                      <input
                        type="number"
                        name="generation_params.temperature"
                        value={formData.generation_params.temperature}
                        onChange={handleChange}
                        min="0"
                        max="1"
                        step="0.1"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                      />
                      <p className="text-xs text-gray-500 mt-1">0 = Conservative, 1 = Creative</p>
                    </div>

                    <div className="space-y-3">
                      <label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          name="include_seo_optimization"
                          checked={formData.include_seo_optimization}
                          onChange={handleChange}
                          className="rounded border-gray-300 text-brand-primary focus:ring-brand-primary"
                        />
                        <span className="text-sm font-medium text-gray-700">SEO Optimization</span>
                      </label>

                      <label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          name="auto_publish"
                          checked={formData.auto_publish}
                          onChange={handleChange}
                          className="rounded border-gray-300 text-brand-primary focus:ring-brand-primary"
                        />
                        <span className="text-sm font-medium text-gray-700">Auto Publish</span>
                      </label>
                    </div>
                  </div>
                </div>

                {/* Suggested Tags */}
                {selectedTemplate.suggested_tags?.length > 0 && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Suggested Tags
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {selectedTemplate.suggested_tags.map((tag, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-brand-accent text-brand-primary"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}

            {/* Actions */}
            <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
              <button
                type="button"
                onClick={onClose}
                disabled={isGenerating}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleGenerate}
                disabled={
                  !selectedTemplate || 
                  selectedProducts.length < selectedTemplate.min_products || 
                  isGenerating
                }
                className="px-6 py-2 bg-brand-primary text-white rounded-md hover:bg-brand-dark transition-colors disabled:opacity-50 flex items-center space-x-2"
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Generating...</span>
                  </>
                ) : (
                  <>
                    <SparklesIcon className="w-4 h-4" />
                    <span>Generate Blog Post</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

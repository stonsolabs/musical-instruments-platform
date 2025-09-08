import React, { useState, useEffect } from 'react';
import { BlogCategory } from '../types/blog';
import { Product } from '../types';
import { searchProducts } from '../lib/api';
import { PlusIcon, XMarkIcon, EyeIcon } from '@heroicons/react/24/outline';

interface BlogPostEditorProps {
  isOpen: boolean;
  onClose: () => void;
  onSave?: (post: any) => void;
}

const PROXY_BASE = '/api/proxy/v1';

export default function BlogPostEditor({ isOpen, onClose, onSave }: BlogPostEditorProps) {
  const [categories, setCategories] = useState<BlogCategory[]>([]);
  const [selectedProducts, setSelectedProducts] = useState<Product[]>([]);
  const [productSearch, setProductSearch] = useState('');
  const [searchResults, setSearchResults] = useState<Product[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [previewMode, setPreviewMode] = useState(false);
  
  const [formData, setFormData] = useState({
    title: '',
    slug: '',
    excerpt: '',
    content: '',
    featured_image: '',
    category_id: 0,
    author_name: 'GetYourMusicGear Team',
    status: 'draft',
    seo_title: '',
    seo_description: '',
    featured: false,
    tag_names: [] as string[],
  });

  const [tagInput, setTagInput] = useState('');

  useEffect(() => {
    if (isOpen) {
      fetchCategories();
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

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${PROXY_BASE}/blog/categories`);
      if (response.ok) {
        const data = await response.json();
        setCategories(data);
      }
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  };

  const handleProductSearch = async (query: string) => {
    setIsSearching(true);
    try {
      const results = await searchProducts(query, 10);
      setSearchResults(results);
    } catch (error) {
      console.error('Product search failed:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
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

  const addTag = () => {
    if (tagInput.trim() && !formData.tag_names.includes(tagInput.trim())) {
      setFormData(prev => ({
        ...prev,
        tag_names: [...prev.tag_names, tagInput.trim()]
      }));
      setTagInput('');
    }
  };

  const removeTag = (tagToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      tag_names: prev.tag_names.filter(tag => tag !== tagToRemove)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const postData = {
        ...formData,
        product_ids: selectedProducts.map(p => p.id),
        seo_title: formData.seo_title || formData.title,
        seo_description: formData.seo_description || formData.excerpt
      };

      const response = await fetch(`${PROXY_BASE}/blog/posts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData),
      });

      if (response.ok) {
        const result = await response.json();
        alert('Blog post created successfully!');
        onSave?.(result);
        onClose();
        // Reset form
        setFormData({
          title: '',
          slug: '',
          excerpt: '',
          content: '',
          featured_image: '',
          category_id: 0,
          author_name: 'GetYourMusicGear Team',
          status: 'draft',
          seo_title: '',
          seo_description: '',
          featured: false,
          tag_names: [],
        });
        setSelectedProducts([]);
      } else {
        const error = await response.json();
        alert(`Failed to create post: ${error.detail}`);
      }
    } catch (error) {
      console.error('Failed to create blog post:', error);
      alert('Failed to create blog post');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }));
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50">
      <div className="flex min-h-screen items-center justify-center px-4">
        <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <div className="flex items-center space-x-4">
              <h2 className="text-2xl font-bold text-gray-900">Create Blog Post</h2>
              <button
                type="button"
                onClick={() => setPreviewMode(!previewMode)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                  previewMode
                    ? 'bg-brand-primary text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <EyeIcon className="w-4 h-4" />
                <span>{previewMode ? 'Edit' : 'Preview'}</span>
              </button>
            </div>
            <button
              type="button"
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-6 space-y-6">
            {!previewMode ? (
              <>
                {/* Basic Info */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Title *</label>
                    <input
                      type="text"
                      name="title"
                      required
                      value={formData.title}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Slug</label>
                    <input
                      type="text"
                      name="slug"
                      value={formData.slug}
                      onChange={handleChange}
                      placeholder="Auto-generated from title"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                    />
                  </div>
                </div>

                {/* Category and Status */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Category *</label>
                    <select
                      name="category_id"
                      required
                      value={formData.category_id}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                    >
                      <option value={0}>Select Category</option>
                      {categories.map((category) => (
                        <option key={category.id} value={category.id}>
                          {category.icon} {category.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
                    <select
                      name="status"
                      value={formData.status}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                    >
                      <option value="draft">Draft</option>
                      <option value="published">Published</option>
                    </select>
                  </div>

                  <div>
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        name="featured"
                        checked={formData.featured}
                        onChange={handleChange}
                        className="rounded border-gray-300 text-brand-primary focus:ring-brand-primary"
                      />
                      <span className="text-sm font-medium text-gray-700">Featured Post</span>
                    </label>
                  </div>
                </div>

                {/* Featured Image */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Featured Image URL</label>
                  <input
                    type="url"
                    name="featured_image"
                    value={formData.featured_image}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                  />
                </div>

                {/* Excerpt */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Excerpt</label>
                  <textarea
                    name="excerpt"
                    rows={3}
                    value={formData.excerpt}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                  />
                </div>

                {/* Content */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Content *</label>
                  <textarea
                    name="content"
                    required
                    rows={12}
                    value={formData.content}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary font-mono"
                    placeholder="Write your blog post content here... You can use markdown formatting."
                  />
                </div>

                {/* Tags */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Tags</label>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {formData.tag_names.map((tag, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-gray-100 text-gray-800"
                      >
                        #{tag}
                        <button
                          type="button"
                          onClick={() => removeTag(tag)}
                          className="ml-2 text-gray-500 hover:text-red-500"
                        >
                          <XMarkIcon className="w-4 h-4" />
                        </button>
                      </span>
                    ))}
                  </div>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={tagInput}
                      onChange={(e) => setTagInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
                      placeholder="Add a tag"
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                    />
                    <button
                      type="button"
                      onClick={addTag}
                      className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
                    >
                      Add
                    </button>
                  </div>
                </div>

                {/* Product Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Featured Products</label>
                  
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
                </div>

                {/* SEO */}
                <div className="border-t border-gray-200 pt-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">SEO Settings</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">SEO Title</label>
                      <input
                        type="text"
                        name="seo_title"
                        value={formData.seo_title}
                        onChange={handleChange}
                        placeholder="Defaults to post title"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">SEO Description</label>
                      <textarea
                        name="seo_description"
                        rows={2}
                        value={formData.seo_description}
                        onChange={handleChange}
                        placeholder="Defaults to excerpt"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand-primary focus:border-brand-primary"
                      />
                    </div>
                  </div>
                </div>
              </>
            ) : (
              /* Preview Mode */
              <div className="prose prose-lg max-w-none">
                <h1>{formData.title}</h1>
                {formData.excerpt && (
                  <p className="text-xl text-gray-700 italic">{formData.excerpt}</p>
                )}
                <div dangerouslySetInnerHTML={{ __html: formData.content.replace(/\n/g, '<br />') }} />
              </div>
            )}

            {/* Actions */}
            <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
              <button
                type="button"
                onClick={onClose}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-6 py-2 bg-brand-primary text-white rounded-md hover:bg-brand-dark transition-colors"
              >
                {formData.status === 'published' ? 'Publish Post' : 'Save Draft'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

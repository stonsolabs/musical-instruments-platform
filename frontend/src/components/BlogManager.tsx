import React, { useState, useEffect } from 'react';
import BlogPostEditor from './BlogPostEditor';
import BlogAIGenerator from './BlogAIGenerator';
import BlogPostCard from './BlogPostCard';
import { 
  BlogPostSummary, 
  BlogGenerationHistory, 
  AIBlogPost 
} from '../types/blog';
import {
  PlusIcon,
  SparklesIcon,
  ClockIcon,
  DocumentTextIcon,
  ChartBarIcon,
  EyeIcon
} from '@heroicons/react/24/outline';

const PROXY_BASE = '/api/proxy/v1';
const ADMIN_API_BASE = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net'}/api/v1`;

export default function BlogManager() {
  // Assumindo que o usuário já está autenticado quando chega aqui via /admin
  const [blogPosts, setBlogPosts] = useState<BlogPostSummary[]>([]);
  const [generationHistory, setGenerationHistory] = useState<BlogGenerationHistory[]>([]);
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [isAIGeneratorOpen, setIsAIGeneratorOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'posts' | 'ai-history'>('posts');
  const [stats, setStats] = useState({
    totalPosts: 0,
    publishedPosts: 0,
    aiGeneratedPosts: 0,
    totalViews: 0
  });

  useEffect(() => {
    fetchBlogPosts();
    fetchGenerationHistory();
    fetchStats();
  }, []);

  const fetchBlogPosts = async () => {
    try {
      const response = await fetch(`${PROXY_BASE}/blog/posts?limit=50`);
      if (response.ok) {
        const data = await response.json();
        setBlogPosts(data);
      }
    } catch (error) {
      console.error('Failed to fetch blog posts:', error);
    }
  };

  const fetchGenerationHistory = async () => {
    try {
      // Call admin endpoint directly on API domain with credentials so Azure auth cookie is sent
      const response = await fetch(`${ADMIN_API_BASE}/admin/blog/generation-history?limit=20`, {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setGenerationHistory(data);
      }
    } catch (error) {
      console.error('Failed to fetch generation history:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      // This would need to be implemented in the API
      const response = await fetch(`${PROXY_BASE}/blog/posts?limit=1000`);
      if (response.ok) {
        const data = await response.json();
        const totalViews = data.reduce((sum: number, post: BlogPostSummary) => sum + post.view_count, 0);
        
        setStats({
          totalPosts: data.length,
          publishedPosts: data.filter((p: BlogPostSummary) => p.published_at).length,
          aiGeneratedPosts: 0, // Would need API support
          totalViews
        });
      }
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const handlePostCreated = (newPost: any) => {
    fetchBlogPosts();
    fetchStats();
  };

  const handleAIGenerated = (result: any) => {
    fetchBlogPosts();
    fetchGenerationHistory();
    fetchStats();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100';
      case 'generating': return 'text-blue-600 bg-blue-100';
      case 'failed': return 'text-red-600 bg-red-100';
      case 'pending': return 'text-yellow-600 bg-yellow-100';
      case 'cancelled': return 'text-gray-600 bg-gray-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  // BlogManager agora é usado apenas dentro do /admin protegido

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-64"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-64 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Blog Management</h1>
          <p className="text-gray-600 mt-2">Create and manage blog posts with AI assistance</p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-end space-x-3 mb-8">
        <button
            onClick={() => setIsAIGeneratorOpen(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-indigo-600 text-white rounded-lg hover:from-purple-600 hover:to-indigo-700 transition-all shadow-lg"
          >
            <SparklesIcon className="w-5 h-5" />
            <span>AI Generator</span>
          </button>
          <button
            onClick={() => setIsEditorOpen(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-brand-primary text-white rounded-lg hover:bg-brand-dark transition-colors"
          >
            <PlusIcon className="w-5 h-5" />
            <span>New Post</span>
          </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Total Posts</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalPosts}</p>
            </div>
            <DocumentTextIcon className="w-8 h-8 text-brand-primary" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Published</p>
              <p className="text-2xl font-bold text-gray-900">{stats.publishedPosts}</p>
            </div>
            <ChartBarIcon className="w-8 h-8 text-green-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">AI Generated</p>
              <p className="text-2xl font-bold text-gray-900">{stats.aiGeneratedPosts}</p>
            </div>
            <SparklesIcon className="w-8 h-8 text-purple-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Total Views</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalViews.toLocaleString()}</p>
            </div>
            <EyeIcon className="w-8 h-8 text-blue-600" />
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab('posts')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'posts'
                ? 'border-brand-primary text-brand-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Blog Posts ({blogPosts.length})
          </button>
          <button
            onClick={() => setActiveTab('ai-history')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'ai-history'
                ? 'border-brand-primary text-brand-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            AI Generation History ({generationHistory.length})
          </button>
        </nav>
      </div>

      {/* Content */}
      {activeTab === 'posts' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {blogPosts.length > 0 ? (
            blogPosts.map((post) => (
              <BlogPostCard 
                key={post.id} 
                post={post}
                showMeta={true}
                showCategory={true}
                showExcerpt={true}
              />
            ))
          ) : (
            <div className="col-span-full text-center py-12">
              <DocumentTextIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No blog posts yet</h3>
              <p className="text-gray-500 mb-6">Get started by creating your first blog post</p>
              <div className="space-x-3">
                <button
                  onClick={() => setIsAIGeneratorOpen(true)}
                  className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-indigo-600 text-white rounded-lg hover:from-purple-600 hover:to-indigo-700 transition-all"
                >
                  <SparklesIcon className="w-5 h-5" />
                  <span>Generate with AI</span>
                </button>
                <button
                  onClick={() => setIsEditorOpen(true)}
                  className="inline-flex items-center space-x-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <PlusIcon className="w-5 h-5" />
                  <span>Create Manually</span>
                </button>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          {generationHistory.length > 0 ? (
            generationHistory.map((history) => (
              <div key={history.id} className="bg-white p-6 rounded-lg shadow-md">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(history.generation_status)}`}>
                      {history.generation_status}
                    </span>
                    <span className="text-sm text-gray-500">
                      {new Date(history.created_at).toLocaleDateString()} at{' '}
                      {new Date(history.created_at).toLocaleTimeString()}
                    </span>
                  </div>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    {history.model_used && (
                      <span>Model: {history.model_used}</span>
                    )}
                    {history.tokens_used && (
                      <span>Tokens: {history.tokens_used}</span>
                    )}
                    {history.generation_time_ms && (
                      <span>Time: {history.generation_time_ms}ms</span>
                    )}
                  </div>
                </div>
                
                {history.blog_post_id && (
                  <div className="mb-3">
                    <a
                      href={`/blog/ai-posts/${history.blog_post_id}`}
                      className="text-brand-primary hover:text-brand-dark font-medium"
                    >
                      View Generated Post →
                    </a>
                  </div>
                )}
                
                {history.error_message && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                    <p className="text-sm text-red-700">
                      <strong>Error:</strong> {history.error_message}
                    </p>
                  </div>
                )}
                
                {history.prompt_used && (
                  <details className="mt-3">
                    <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
                      View Prompt Used
                    </summary>
                    <div className="mt-2 p-3 bg-gray-50 rounded-md">
                      <pre className="text-xs text-gray-600 whitespace-pre-wrap">
                        {history.prompt_used.length > 500 
                          ? history.prompt_used.substring(0, 500) + '...'
                          : history.prompt_used
                        }
                      </pre>
                    </div>
                  </details>
                )}
              </div>
            ))
          ) : (
            <div className="text-center py-12">
              <ClockIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No AI generation history</h3>
              <p className="text-gray-500 mb-6">Generate your first blog post with AI to see history here</p>
              <button
                onClick={() => setIsAIGeneratorOpen(true)}
                className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-indigo-600 text-white rounded-lg hover:from-purple-600 hover:to-indigo-700 transition-all"
              >
                <SparklesIcon className="w-5 h-5" />
                <span>Generate First Post</span>
              </button>
            </div>
          )}
        </div>
      )}

      {/* Modals */}
      <BlogPostEditor
        isOpen={isEditorOpen}
        onClose={() => setIsEditorOpen(false)}
        onSave={handlePostCreated}
      />

      <BlogAIGenerator
        isOpen={isAIGeneratorOpen}
        onClose={() => setIsAIGeneratorOpen(false)}
        onGenerated={handleAIGenerated}
      />
    </div>
  );
}

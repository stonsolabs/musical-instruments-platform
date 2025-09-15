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
  const [blogPosts, setBlogPosts] = useState<any[]>([]);
  const [selected, setSelected] = useState<Set<number>>(new Set());
  const [backfillDays, setBackfillDays] = useState<number>(14);
  const [generationHistory, setGenerationHistory] = useState<BlogGenerationHistory[]>([]);
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [isAIGeneratorOpen, setIsAIGeneratorOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'posts' | 'ai-history'>('posts');
  const [statusFilter, setStatusFilter] = useState<'all'|'draft'|'published'>('all');
  const [aiFilter, setAiFilter] = useState<'all'|'ai'|'manual'>('all');
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
  }, [statusFilter, aiFilter]);

  const fetchBlogPosts = async () => {
    try {
      const adminToken = typeof window !== 'undefined' ? sessionStorage.getItem('adminToken') : null;
      const qs = new URLSearchParams({ limit: '50' });
      if (statusFilter !== 'all') qs.set('status', statusFilter);
      if (aiFilter !== 'all') qs.set('ai_generated', aiFilter === 'ai' ? 'true' : 'false');
      const response = await fetch(`${ADMIN_API_BASE}/admin/blog/posts?${qs.toString()}`, {
        credentials: 'include',
        headers: { ...(adminToken ? { 'X-Admin-Token': adminToken } : {}) }
      });
      if (response.ok) {
        const data = await response.json();
        const mapped: any[] = (data.posts || []).map((p: any) => ({
          id: p.id,
          title: p.title,
          slug: p.slug,
          excerpt: p.excerpt,
          featured_image: p.featured_image,
          category: p.category_slug ? {
            id: 0,
            name: p.category_name,
            slug: p.category_slug,
            color: p.category_color,
            sort_order: 0,
            is_active: true,
          } as any : undefined,
          author_name: p.author_name,
          status: p.status,
          reading_time: p.reading_time,
          view_count: p.view_count || 0,
          featured: p.featured || false,
          published_at: p.published_at,
          tags: [],
        }));
        setBlogPosts(mapped);
      }
    } catch (error) {
      console.error('Failed to fetch blog posts:', error);
    }
  };

  const fetchGenerationHistory = async () => {
    try {
      // Call admin endpoint directly on API domain; include SSO token if available
      const adminToken = typeof window !== 'undefined' ? sessionStorage.getItem('adminToken') : null;
      const response = await fetch(`${ADMIN_API_BASE}/admin/blog/generation-history?limit=20`, {
        credentials: 'include',
        headers: { ...(adminToken ? { 'X-Admin-Token': adminToken } : {}) }
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
      const adminToken = typeof window !== 'undefined' ? sessionStorage.getItem('adminToken') : null;
      const response = await fetch(`${ADMIN_API_BASE}/admin/stats`, {
        credentials: 'include',
        headers: { ...(adminToken ? { 'X-Admin-Token': adminToken } : {}) }
      });
      if (response.ok) {
        const data = await response.json();
        setStats({
          totalPosts: data.blog?.total_posts || 0,
          publishedPosts: data.blog?.published_posts || 0,
          aiGeneratedPosts: data.blog?.ai_generated_posts || 0,
          totalViews: data.blog?.total_views || 0,
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

  const toggleSelect = (id: number) => {
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  const clearSelection = () => setSelected(new Set());

  const bulkPublish = async (strategy: 'now' | 'backfill') => {
    if (selected.size === 0) return;
    try {
      const adminToken = typeof window !== 'undefined' ? sessionStorage.getItem('adminToken') : null;
      const resp = await fetch(`${ADMIN_API_BASE}/admin/blog/posts/publish-batch`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          ...(adminToken ? { 'X-Admin-Token': adminToken } : {})
        },
        body: JSON.stringify({
          ids: Array.from(selected),
          strategy,
          backfill_days: strategy === 'backfill' ? backfillDays : undefined
        })
      });
      if (!resp.ok) throw new Error('Bulk publish failed');
      clearSelection();
      fetchBlogPosts();
      fetchStats();
    } catch (e) {
      console.error(e);
      alert('Failed to bulk publish');
    }
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

      {/* Filters + Actions */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
        {/* Filters */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">Status:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as any)}
              className="px-2 py-1 border rounded text-sm"
            >
              <option value="all">All</option>
              <option value="draft">Drafts</option>
              <option value="published">Published</option>
            </select>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">Origin:</span>
            <select
              value={aiFilter}
              onChange={(e) => setAiFilter(e.target.value as any)}
              className="px-2 py-1 border rounded text-sm"
            >
              <option value="all">All</option>
              <option value="ai">AI</option>
              <option value="manual">Manual</option>
            </select>
          </div>
        </div>
        {/* Bulk bar */}
        {selected.size > 0 ? (
          <div className="flex items-center space-x-3">
            <span className="text-sm text-gray-700">Selected: {selected.size}</span>
            <button
              onClick={() => bulkPublish('now')}
              className="px-3 py-2 text-sm bg-green-600 text-white rounded hover:bg-green-700"
            >
              Publish Now
            </button>
            <div className="flex items-center space-x-2">
              <input
                type="number"
                min={1}
                max={90}
                value={backfillDays}
                onChange={(e) => setBackfillDays(parseInt(e.target.value || '14', 10))}
                className="w-16 px-2 py-1 border rounded"
                title="Distribute dates across past N days"
              />
              <button
                onClick={() => bulkPublish('backfill')}
                className="px-3 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Publish Spread
              </button>
              <button onClick={clearSelection} className="px-3 py-2 text-sm border rounded text-gray-700 hover:bg-gray-50">Clear</button>
            </div>
          </div>
        ) : <div />}

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
            blogPosts.map((post) => {
              const isSelected = selected.has(post.id);
              const isPublished = post.status === 'published';
              const hrefOverride = isPublished ? `/blog/${post.slug}` : `/admin/blog/preview/${post.id}`;
              return (
                <div key={post.id} className="relative">
                  <div className="absolute top-3 left-3 z-10 bg-white/90 rounded-md p-1 shadow">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => toggleSelect(post.id)}
                      className="h-4 w-4"
                      title="Select for bulk publish"
                    />
                  </div>
                  <div className={`absolute top-3 right-3 z-10 px-2 py-1 rounded text-xs font-medium ${isPublished ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    {isPublished ? 'Published' : 'Draft'}
                  </div>
                  <BlogPostCard
                    post={post}
                    showMeta={true}
                    showCategory={true}
                    showExcerpt={true}
                    hrefOverride={hrefOverride}
                  />
                  {/* Explicit action bar below each card */}
                  <div className="mt-2 flex items-center justify-between text-sm">
                    {!isPublished ? (
                      <a
                        href={`/admin/blog/preview/${post.id}`}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        Preview (draft)
                      </a>
                    ) : (
                      <a
                        href={`/blog/${post.slug}`}
                        className="text-green-600 hover:text-green-800"
                      >
                        View public page
                      </a>
                    )}
                  </div>
                </div>
              );
            })
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

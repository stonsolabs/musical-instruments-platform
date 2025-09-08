import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';

interface UserInfo {
  email: string;
  name: string;
  roles?: string[];
}

export default function DocsPage() {
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    checkAuthentication();
  }, []);

  const checkAuthentication = async () => {
    try {
      const response = await fetch('/api/proxy/v1/admin/user-info');
      
      if (response.status === 401) {
        // Not authenticated - redirect to Azure AD login
        window.location.href = '/.auth/login/aad?post_login_redirect_url=' + encodeURIComponent('/docs');
        return;
      }
      
      if (response.status === 403) {
        // Authenticated but not admin
        setError('Access denied. Admin privileges required to view documentation.');
        setLoading(false);
        return;
      }

      if (response.ok) {
        const data = await response.json();
        setUserInfo(data.user);
        setLoading(false);
      } else {
        throw new Error('Failed to verify authentication');
      }
    } catch (err) {
      console.error('Authentication check failed:', err);
      setError('Failed to verify authentication');
      setLoading(false);
    }
  };

  const handleLogout = () => {
    window.location.href = '/.auth/logout?post_logout_redirect_url=/';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Verifying authentication...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto">
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <p>{error}</p>
          </div>
          <button
            onClick={() => router.push('/')}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors"
          >
            Return to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>API Documentation - GetYourMusicGear Admin</title>
        <meta name="description" content="API Documentation for GetYourMusicGear platform" />
        <meta name="robots" content="noindex, nofollow" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center space-x-4">
                <h1 className="text-2xl font-bold text-gray-900">API Documentation</h1>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Admin Access
                </span>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">
                  Welcome, {userInfo?.name || userInfo?.email}
                </span>
                <button
                  onClick={() => router.push('/admin')}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  Admin Dashboard
                </button>
                <button
                  onClick={handleLogout}
                  className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded text-sm transition-colors"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Content */}
        <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Interactive API Documentation</h2>
              <p className="mt-1 text-sm text-gray-600">
                Explore and test the GetYourMusicGear API endpoints
              </p>
            </div>
            
            <div className="p-6">
              {/* Swagger UI Container */}
              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <iframe
                  src="/api/proxy/v1/docs/"
                  className="w-full h-[800px] border-0"
                  title="API Documentation"
                  sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
                />
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* API Overview */}
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">API Overview</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Base URL: <code className="bg-gray-100 px-1 rounded">{process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1</code></li>
                <li>• Authentication: API Key in header</li>
                <li>• Response format: JSON</li>
                <li>• Rate limiting: 1000 requests/hour</li>
              </ul>
            </div>

            {/* Blog API */}
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Blog API</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• <code className="bg-gray-100 px-1 rounded">GET /blog/posts</code> - List posts</li>
                <li>• <code className="bg-gray-100 px-1 rounded">POST /blog/posts</code> - Create post</li>
                <li>• <code className="bg-gray-100 px-1 rounded">GET /blog/categories</code> - List categories</li>
                <li>• <code className="bg-gray-100 px-1 rounded">POST /admin/blog/generate</code> - AI generate</li>
              </ul>
            </div>

            {/* Batch API */}
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Batch API</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• <code className="bg-gray-100 px-1 rounded">POST /admin/blog/batch/create</code> - Create batch</li>
                <li>• <code className="bg-gray-100 px-1 rounded">POST /admin/blog/batch/&#123;id&#125;/upload</code> - Upload</li>
                <li>• <code className="bg-gray-100 px-1 rounded">GET /admin/blog/batches</code> - List batches</li>
                <li>• <code className="bg-gray-100 px-1 rounded">POST /admin/blog/batch/process</code> - Process results</li>
              </ul>
            </div>

            {/* Product API */}
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Product API</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• <code className="bg-gray-100 px-1 rounded">GET /products</code> - List products</li>
                <li>• <code className="bg-gray-100 px-1 rounded">GET /products/&#123;id&#125;</code> - Get product</li>
                <li>• <code className="bg-gray-100 px-1 rounded">GET /search/autocomplete</code> - Search</li>
                <li>• <code className="bg-gray-100 px-1 rounded">POST /compare</code> - Compare products</li>
              </ul>
            </div>

            {/* Admin API */}
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Admin API</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• <code className="bg-gray-100 px-1 rounded">GET /admin/stats</code> - Dashboard stats</li>
                <li>• <code className="bg-gray-100 px-1 rounded">GET /admin/system/health</code> - System health</li>
                <li>• <code className="bg-gray-100 px-1 rounded">GET /admin/user-info</code> - User info</li>
                <li>• <code className="bg-gray-100 px-1 rounded">GET /admin/blog/generation-history</code> - AI history</li>
              </ul>
            </div>

            {/* Utilities */}
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Utilities</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• <code className="bg-gray-100 px-1 rounded">GET /categories</code> - List categories</li>
                <li>• <code className="bg-gray-100 px-1 rounded">GET /brands</code> - List brands</li>
                <li>• <code className="bg-gray-100 px-1 rounded">GET /trending/instruments</code> - Trending</li>
                <li>• <code className="bg-gray-100 px-1 rounded">POST /voting/products/&#123;id&#125;/vote</code> - Vote</li>
              </ul>
            </div>
          </div>

          {/* Footer Note */}
          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">Admin Access Required</h3>
                <p className="mt-1 text-sm text-blue-700">
                  This documentation is only accessible to authenticated admin users via Azure App Service Authentication.
                  All API endpoints require proper authentication and authorization.
                </p>
              </div>
            </div>
          </div>
        </main>
      </div>
    </>
  );
}
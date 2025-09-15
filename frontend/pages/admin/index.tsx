import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import BlogManager from '../../src/components/BlogManager';
import { ShieldCheckIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface UserInfo {
  email: string;
  name?: string;
  provider: string;
  is_admin: boolean;
}

interface AuthError {
  error: string;
  message: string;
  login_url?: string;
  contact?: string;
}

export default function AdminPage() {
  const router = useRouter();
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<AuthError | null>(null);

  useEffect(() => {
    checkAdminAuth();
  }, []);

  const checkAdminAuth = async () => {
    try {
      console.log('[ADMIN] Checking authentication with Azure backend...');
      // Check authentication directly against the API domain so Azure Easy Auth cookies are sent
      const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';
      const adminToken = typeof window !== 'undefined' ? sessionStorage.getItem('adminToken') : null;
      const response = await fetch(`${apiBase}/api/v1/admin/user-info`, {
        method: 'GET',
        // Include credentials so browser sends Azure App Service auth cookies to the API domain
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          ...(adminToken ? { 'X-Admin-Token': adminToken } : {})
        }
      });

      console.log(`[ADMIN] Auth response status: ${response.status}`);

      if (response.status === 401) {
        // User is not authenticated, redirect to Azure AD login
        // First try SSO bridge to obtain a short-lived admin token without relying on third-party cookies
        const bridgeUrl = `${apiBase}/api/v1/admin/sso/bridge?origin=${encodeURIComponent(window.location.origin)}`;
        const w = 520, h = 600;
        const y = window.top!.outerHeight / 2 + window.top!.screenY - ( h / 2);
        const x = window.top!.outerWidth / 2 + window.top!.screenX - ( w / 2);
        const popup = window.open(bridgeUrl, 'gy-admin-sso', `width=${w},height=${h},left=${x},top=${y}`);

        if (popup) {
          await new Promise<void>((resolve) => {
            const handler = (ev: MessageEvent) => {
              if (ev.origin !== window.location.origin) return;
              if (ev.data && ev.data.type === 'GYMG_SSO_TOKEN' && ev.data.token) {
                sessionStorage.setItem('adminToken', ev.data.token);
                window.removeEventListener('message', handler);
                resolve();
              }
            };
            window.addEventListener('message', handler);
          });
          // Retry with token
          const retry = await fetch(`${apiBase}/api/v1/admin/user-info`, {
            method: 'GET',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json', 'X-Admin-Token': sessionStorage.getItem('adminToken') || '' }
          });
          if (retry.ok) {
            const data = await retry.json();
            setUserInfo(data.user);
            setIsLoading(false);
            return;
          }
        }

        // Fallback to direct Azure AD login
        const azureBackend = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';
        const loginUrl = `${azureBackend}/.auth/login/aad?post_login_redirect_url=${encodeURIComponent(window.location.href)}`;
        console.log('[ADMIN] Redirecting to login:', loginUrl);
        window.location.href = loginUrl;
        return;
      }

      if (response.status === 403) {
        // User is authenticated but not an admin
        setError({
          error: 'access_denied',
          message: 'Access denied. Only administrators can access this area.',
          contact: 'Contact the system administrator if you believe you should have access.'
        });
        return;
      }

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      console.log('[ADMIN] User info received:', data);
      
      if (data.user && data.user.is_admin) {
        setUserInfo(data.user);
        console.log('[ADMIN] Admin access granted');
      } else {
        setError({
          error: 'access_denied',
          message: 'Access denied. Only administrators can access this area.',
          contact: 'Contact the system administrator if you believe you should have access.'
        });
      }
    } catch (err) {
      console.error('Auth check failed:', err);
      setError({
        error: 'network_error',
        message: 'Unable to connect to the server. Please check your connection.'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    try {
      // Clear any client-side tokens/flags first to avoid stale auth on reload
      sessionStorage.removeItem('adminToken');
      sessionStorage.removeItem('adminKey');
      // Also clear common localStorage fallbacks if ever used
      try { localStorage.removeItem('adminToken'); } catch {}
      try { localStorage.removeItem('adminKey'); } catch {}
    } catch {}
    const azureBackend = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';
    const redirect = `${window.location.origin}/admin?logged_out=1&ts=${Date.now()}`;
    window.location.href = `${azureBackend}/.auth/logout?post_logout_redirect_url=${encodeURIComponent(redirect)}`;
  };

  if (isLoading) {
    return (
      <>
        <Head>
          <title>Admin Panel - GetYourMusicGear</title>
          <meta name="robots" content="noindex, nofollow" />
        </Head>
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-primary mx-auto"></div>
            <p className="mt-4 text-gray-600">Verificando autenticação...</p>
          </div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Head>
          <title>Acesso Negado - GetYourMusicGear</title>
          <meta name="robots" content="noindex, nofollow" />
        </Head>
        <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4 sm:px-6 lg:px-8">
          <div className="max-w-md w-full space-y-8 text-center">
            <div>
              <div className="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-red-100">
                <ExclamationTriangleIcon className="h-10 w-10 text-red-600" />
              </div>
              <h2 className="mt-6 text-3xl font-bold text-gray-900">
                {error.error === 'authentication_required' ? 'Login Necessário' : 'Acesso Negado'}
              </h2>
              <div className="mt-4 space-y-2">
                <p className="text-gray-600">{error.message}</p>
                {error.contact && (
                  <p className="text-sm text-gray-500">{error.contact}</p>
                )}
              </div>
            </div>

            <div className="space-y-4">
              {(error.error === 'authentication_required' || error.error === 'network_error') ? (
                <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                  <p className="text-sm text-blue-700">
                    {error.error === 'authentication_required' ? 
                      'Authentication required to access admin panel.' : 
                      'Please try logging in again.'}
                  </p>
                  <a
                    href={error.login_url || `${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net'}/.auth/login/aad?post_login_redirect_url=${encodeURIComponent(window.location.href)}`}
                    className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors"
                  >
                    <ShieldCheckIcon className="w-4 h-4 mr-2" />
                    Login with Azure AD
                  </a>
                </div>
              ) : (
                <div className="bg-gray-50 border border-gray-200 rounded-md p-4">
                  <p className="text-sm text-gray-600">
                    Esta área é restrita aos administradores do sistema.
                  </p>
                </div>
              )}

              <button
                onClick={() => router.push('/')}
                className="text-brand-primary hover:text-brand-dark font-medium transition-colors"
              >
                ← Voltar ao site principal
              </button>
            </div>
          </div>
        </div>
      </>
    );
  }

  if (userInfo?.is_admin) {
    return (
      <>
        <Head>
          <title>Admin Panel - GetYourMusicGear</title>
          <meta name="robots" content="noindex, nofollow" />
          <meta name="description" content="Admin panel for GetYourMusicGear blog management" />
        </Head>
        
        {/* Admin Header */}
        <div className="bg-brand-primary text-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-3">
                <ShieldCheckIcon className="h-6 w-6" />
                <div>
                  <h1 className="font-semibold">Admin Panel</h1>
                  <p className="text-sm text-brand-accent">GetYourMusicGear</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <a
                  href="/docs"
                  className="text-sm text-brand-accent hover:text-white transition-colors px-3 py-1 rounded border border-brand-accent hover:border-white"
                >
                  📚 API Docs
                </a>
                <div className="text-right">
                  <p className="text-sm font-medium">
                    {userInfo.name || userInfo.email}
                  </p>
                  <p className="text-xs text-brand-accent">
                    {userInfo.provider === 'azure' ? 'Azure AD' : 'Local'}
                  </p>
                </div>
                <button
                  onClick={handleLogout}
                  className="text-sm text-brand-accent hover:text-white transition-colors px-3 py-1 rounded border border-brand-accent hover:border-white"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Blog Manager */}
        <div className="min-h-screen bg-gray-50">
          <BlogManager />
        </div>
      </>
    );
  }

  return null;
}

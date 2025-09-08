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
      const response = await fetch('/api/proxy/v1/admin/user-info');
      
      if (response.ok) {
        const data = await response.json();
        setUserInfo(data.user);
        setError(null);
      } else if (response.status === 401) {
        // Não autenticado - redirecionar para Azure AD login
        const errorData = await response.json();
        setError(errorData.detail);
        
        // Redirecionar para login do Azure AD após um delay
        setTimeout(() => {
          window.location.href = '/.auth/login/aad?post_login_redirect_url=/admin';
        }, 3000);
      } else if (response.status === 403) {
        // Autenticado mas não é admin
        const errorData = await response.json();
        setError(errorData.detail);
      } else {
        setError({
          error: 'unknown_error',
          message: 'An unexpected error occurred. Please try again.'
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
    window.location.href = '/.auth/logout?post_logout_redirect_url=/';
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
              {error.error === 'authentication_required' ? (
                <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                  <p className="text-sm text-blue-700">
                    Você será redirecionado para o login em alguns segundos...
                  </p>
                  <a
                    href={error.login_url || '/.auth/login/aad?post_login_redirect_url=/admin'}
                    className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors"
                  >
                    <ShieldCheckIcon className="w-4 h-4 mr-2" />
                    Login com Azure AD
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
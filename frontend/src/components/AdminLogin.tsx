import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { 
  ShieldCheckIcon, 
  KeyIcon, 
  ExclamationCircleIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/react/24/outline';

interface AdminLoginProps {
  onSuccess?: () => void;
}

export default function AdminLogin({ onSuccess }: AdminLoginProps) {
  const { login, isLoading, error } = useAuth();
  const [adminKey, setAdminKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [loginAttempted, setLoginAttempted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginAttempted(true);

    if (!adminKey.trim()) {
      return;
    }

    const success = await login(adminKey.trim());
    if (success) {
      onSuccess?.();
    }
  };

  const handleKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAdminKey(e.target.value);
    setLoginAttempted(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-brand-primary/10 to-brand-dark/10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-brand-primary/10">
            <ShieldCheckIcon className="h-10 w-10 text-brand-primary" />
          </div>
          <h2 className="mt-6 text-3xl font-bold text-gray-900">
            Admin Access Required
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Enter your admin key to access the blog management system
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="admin-key" className="sr-only">
              Admin Key
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <KeyIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="admin-key"
                name="admin-key"
                type={showKey ? 'text' : 'password'}
                required
                value={adminKey}
                onChange={handleKeyChange}
                className="appearance-none rounded-md relative block w-full pl-10 pr-12 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-brand-primary focus:border-brand-primary focus:z-10 sm:text-sm"
                placeholder="Enter admin key"
                disabled={isLoading}
              />
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <button
                  type="button"
                  onClick={() => setShowKey(!showKey)}
                  className="text-gray-400 hover:text-gray-600 focus:outline-none"
                  disabled={isLoading}
                >
                  {showKey ? (
                    <EyeSlashIcon className="h-5 w-5" />
                  ) : (
                    <EyeIcon className="h-5 w-5" />
                  )}
                </button>
              </div>
            </div>
          </div>

          {(error || (loginAttempted && !adminKey.trim())) && (
            <div className="flex items-center space-x-2 text-red-600 text-sm">
              <ExclamationCircleIcon className="h-5 w-5" />
              <span>
                {error || 'Admin key is required'}
              </span>
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={isLoading || !adminKey.trim()}
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-brand-primary hover:bg-brand-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? (
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Authenticating...</span>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <ShieldCheckIcon className="h-5 w-5" />
                  <span>Access Admin Panel</span>
                </div>
              )}
            </button>
          </div>

          <div className="text-xs text-gray-500 text-center space-y-2">
            <p>
              This area is restricted to administrators only.
            </p>
            <p>
              If you are the site owner and don't have your admin key, 
              check your environment variables or contact support.
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}
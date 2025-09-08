import { useState, useEffect } from 'react';

interface AuthState {
  isAdmin: boolean;
  isLoading: boolean;
  error: string | null;
}

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    isAdmin: false,
    isLoading: true,
    error: null
  });

  const [adminKey, setAdminKey] = useState<string>('');

  useEffect(() => {
    // Check if admin key is stored in sessionStorage
    const storedAdminKey = sessionStorage.getItem('adminKey');
    if (storedAdminKey) {
      setAdminKey(storedAdminKey);
      validateAdminKey(storedAdminKey);
    } else {
      setAuthState({ isAdmin: false, isLoading: false, error: null });
    }
  }, []);

  const validateAdminKey = async (key: string) => {
    try {
      // Test admin access by calling a protected endpoint
      const response = await fetch('/api/proxy/v1/blog/generation-history?limit=1', {
        headers: {
          'X-Admin-Key': key
        }
      });

      if (response.ok) {
        setAuthState({ isAdmin: true, isLoading: false, error: null });
      } else if (response.status === 401 || response.status === 403) {
        setAuthState({ isAdmin: false, isLoading: false, error: 'Invalid admin credentials' });
        sessionStorage.removeItem('adminKey');
        setAdminKey('');
      } else {
        setAuthState({ isAdmin: false, isLoading: false, error: 'Authentication check failed' });
      }
    } catch (error) {
      setAuthState({ isAdmin: false, isLoading: false, error: 'Network error' });
    }
  };

  const login = async (key: string): Promise<boolean> => {
    setAuthState({ ...authState, isLoading: true, error: null });

    try {
      // Test admin access
      const response = await fetch('/api/proxy/v1/blog/generation-history?limit=1', {
        headers: {
          'X-Admin-Key': key
        }
      });

      if (response.ok) {
        sessionStorage.setItem('adminKey', key);
        setAdminKey(key);
        setAuthState({ isAdmin: true, isLoading: false, error: null });
        return true;
      } else {
        setAuthState({ isAdmin: false, isLoading: false, error: 'Invalid admin key' });
        return false;
      }
    } catch (error) {
      setAuthState({ isAdmin: false, isLoading: false, error: 'Network error' });
      return false;
    }
  };

  const logout = () => {
    sessionStorage.removeItem('adminKey');
    setAdminKey('');
    setAuthState({ isAdmin: false, isLoading: false, error: null });
  };

  const getAuthHeaders = () => {
    return adminKey ? { 'X-Admin-Key': adminKey } : {};
  };

  return {
    isAdmin: authState.isAdmin,
    isLoading: authState.isLoading,
    error: authState.error,
    login,
    logout,
    getAuthHeaders
  };
}
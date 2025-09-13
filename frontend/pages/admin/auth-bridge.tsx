import React, { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function AuthBridge() {
  const router = useRouter();

  useEffect(() => {
    // This page runs in the Azure App Service context where authentication works
    const checkAuth = async () => {
      try {
        const response = await fetch('/api/v1/admin/user-info');
        if (response.ok) {
          const data = await response.json();
          // Send user data back to parent window (Vercel frontend)
          window.parent.postMessage({
            type: 'AUTH_SUCCESS',
            user: data.user
          }, window.location.origin);
        } else {
          window.parent.postMessage({
            type: 'AUTH_FAILED',
            status: response.status
          }, window.location.origin);
        }
      } catch (error) {
        window.parent.postMessage({
          type: 'AUTH_ERROR',
          error: error.message
        }, window.location.origin);
      }
    };

    checkAuth();
  }, []);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Checking authentication...</p>
      </div>
    </div>
  );
}
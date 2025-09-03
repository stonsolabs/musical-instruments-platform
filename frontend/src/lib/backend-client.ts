// Shared backend client that can be used by both proxy and server-side code
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';
const API_KEY = process.env.API_KEY || '';

export async function callBackendApi(endpoint: string, options: RequestInit = {}) {
  // Ensure no double slashes by properly joining the URL parts
  const baseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
  const apiPrefix = '/api/v1';
  const targetUrl = `${baseUrl}${apiPrefix}${endpoint}`;
  
  console.log('🔗 Direct backend call:', {
    endpoint,
    targetUrl,
    hasApiKey: !!API_KEY,
    environment: process.env.NODE_ENV
  });
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'User-Agent': 'MusicalInstrumentsPlatform/1.0',
    ...options.headers as Record<string, string>,
  };
  
  // Add API key for authentication
  if (API_KEY) {
    headers['X-API-Key'] = API_KEY;
  }
  
  const response = await fetch(targetUrl, {
    ...options,
    headers,
    // Add timeout
    signal: AbortSignal.timeout(10000), // 10 second timeout
  });

  console.log('📡 Backend response:', {
    status: response.status,
    statusText: response.statusText,
    ok: response.ok,
    url: targetUrl
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error('❌ Backend error response:', errorText);
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}
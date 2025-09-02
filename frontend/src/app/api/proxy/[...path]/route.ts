import { NextRequest, NextResponse } from 'next/server';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';
const API_KEY = process.env.API_KEY || '';

export async function GET(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  const path = params.path.join('/');
  const url = new URL(request.url);
  const searchParams = url.searchParams.toString();
  
  // Enhanced debug logging
  console.log('🔍 Proxy GET request:', {
    path,
    searchParams,
    apiBaseUrl: API_BASE_URL,
    hasApiKey: !!API_KEY,
    apiKeyLength: API_KEY ? API_KEY.length : 0,
    fullUrl: `${API_BASE_URL}${API_BASE_URL.includes('localhost') ? '' : '/api/v1'}/${path}?${searchParams}`,
    userAgent: request.headers.get('user-agent'),
    origin: request.headers.get('origin')
  });
  
  // Validate API_BASE_URL - allow localhost for development
  if (!API_BASE_URL) {
    console.error('❌ Invalid API_BASE_URL:', API_BASE_URL);
    return NextResponse.json(
      { 
        error: 'API_BASE_URL not configured properly',
        currentValue: API_BASE_URL,
        expected: 'https://getyourmusicgear-api.azurewebsites.net',
        instructions: 'Set NEXT_PUBLIC_API_BASE_URL environment variable in Vercel dashboard'
      },
      { status: 500 }
    );
  }
  
  // Skip API key validation for local development
  if (!API_KEY && !API_BASE_URL.includes('localhost')) {
    console.error('❌ API_KEY not configured for production');
    return NextResponse.json(
      { 
        error: 'API_KEY environment variable is required for production',
        instructions: 'Set API_KEY environment variable in your hosting platform'
      },
      { status: 500 }
    );
  }
  
  try {
    // Ensure no double slashes by properly joining the URL parts
    const baseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
    // Use /api/v1 prefix for production, direct path for local development
    const apiPrefix = API_BASE_URL.includes('localhost') ? '' : '/api/v1';
    const targetUrl = `${baseUrl}${apiPrefix}/${path}?${searchParams}`;
    console.log('🚀 Making request to:', targetUrl);
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'User-Agent': 'MusicalInstrumentsPlatform/1.0',
    };
    
    // Only add API key for production
    if (!API_BASE_URL.includes('localhost')) {
      headers['X-API-Key'] = API_KEY;
    }
    
    const response = await fetch(targetUrl, {
      headers,
      // Add timeout
      signal: AbortSignal.timeout(10000), // 10 second timeout
    });

    console.log('📡 Backend response:', {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
      headers: Object.fromEntries(response.headers.entries())
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ Backend error response:', errorText);
      return NextResponse.json(
        { 
          error: 'Backend request failed',
          details: errorText,
          status: response.status,
          url: targetUrl
        },
        { status: response.status }
      );
    }

    const data = await response.json();
    console.log('✅ Successfully received data from backend');
    return NextResponse.json(data);
  } catch (error) {
    console.error('💥 Proxy error:', error);
    
    // Handle specific error types
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        return NextResponse.json(
          { 
            error: 'Request timeout',
            details: 'Backend request took too long to respond',
            apiBaseUrl: API_BASE_URL
          },
          { status: 504 }
        );
      }
      
      if (error.message.includes('fetch')) {
        return NextResponse.json(
          { 
            error: 'Network error',
            details: error.message,
            apiBaseUrl: API_BASE_URL,
            hint: 'Check if backend is accessible'
          },
          { status: 502 }
        );
      }
    }
    
    return NextResponse.json(
      { 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error',
        apiBaseUrl: API_BASE_URL,
        hasApiKey: !!API_KEY
      },
      { status: 500 }
    );
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  const path = params.path.join('/');
  const body = await request.json();
  
  try {
    // Ensure no double slashes by properly joining the URL parts
    const baseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
    const apiPrefix = API_BASE_URL.includes('localhost') ? '' : '/api/v1';
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    // Only add API key for production
    if (!API_BASE_URL.includes('localhost')) {
      headers['X-API-Key'] = API_KEY;
    }
    
    const response = await fetch(`${baseUrl}${apiPrefix}/${path}`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Backend request failed' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  const path = params.path.join('/');
  const body = await request.json();
  
  try {
    // Ensure no double slashes by properly joining the URL parts
    const baseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
    const apiPrefix = API_BASE_URL.includes('localhost') ? '' : '/api/v1';
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    // Only add API key for production
    if (!API_BASE_URL.includes('localhost')) {
      headers['X-API-Key'] = API_KEY;
    }
    
    const response = await fetch(`${baseUrl}${apiPrefix}/${path}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Backend request failed' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  const path = params.path.join('/');
  
  try {
    // Ensure no double slashes by properly joining the URL parts
    const baseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
    const response = await fetch(`${baseUrl}/api/v1/${path}`, {
      method: 'DELETE',
      headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Backend request failed' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

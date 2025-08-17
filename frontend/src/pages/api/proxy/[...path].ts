import { NextApiRequest, NextApiResponse } from 'next';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const API_KEY = process.env.API_KEY || '';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { method, query, body } = req;
  const path = Array.isArray(query.path) ? query.path.join('/') : query.path || '';
  
  // Enhanced debug logging
  console.log('🔍 Proxy request:', {
    method,
    path,
    query: req.query,
    apiBaseUrl: API_BASE_URL,
    hasApiKey: !!API_KEY,
    apiKeyLength: API_KEY ? API_KEY.length : 0,
    userAgent: req.headers['user-agent'],
    origin: req.headers['origin']
  });
  
  // Validate API_BASE_URL
  if (!API_BASE_URL || API_BASE_URL === 'http://localhost:8000') {
    console.error('❌ Invalid API_BASE_URL:', API_BASE_URL);
    return res.status(500).json({
      error: 'API_BASE_URL not configured properly',
      currentValue: API_BASE_URL,
      expected: 'https://your-backend-app.onrender.com'
    });
  }
  
  // Validate API_KEY
  if (!API_KEY) {
    console.error('❌ API_KEY not configured');
    return res.status(500).json({
      error: 'API_KEY not configured',
      hint: 'Set API_KEY environment variable in Vercel'
    });
  }

  // Handle different HTTP methods
  if (method === 'GET') {
    return handleGet(req, res, path);
  } else if (method === 'POST') {
    return handlePost(req, res, path);
  } else if (method === 'PUT') {
    return handlePut(req, res, path);
  } else if (method === 'DELETE') {
    return handleDelete(req, res, path);
  } else {
    return res.status(405).json({ error: 'Method not allowed' });
  }
}

async function handleGet(req: NextApiRequest, res: NextApiResponse, path: string) {
  const searchParams = new URLSearchParams();
  
  // Add query parameters
  Object.entries(req.query).forEach(([key, value]) => {
    if (key !== 'path' && value !== undefined) {
      if (Array.isArray(value)) {
        value.forEach(v => searchParams.append(key, v));
      } else {
        searchParams.append(key, value);
      }
    }
  });

  try {
    // Ensure no double slashes by properly joining the URL parts
    const baseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
    const targetUrl = `${baseUrl}/api/v1/${path}?${searchParams.toString()}`;
    console.log('🚀 Making GET request to:', targetUrl);
    
    const response = await fetch(targetUrl, {
      headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json',
        'User-Agent': 'MusicalInstrumentsPlatform/1.0',
      },
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
      return res.status(response.status).json({
        error: 'Backend request failed',
        details: errorText,
        status: response.status,
        url: targetUrl
      });
    }

    const data = await response.json();
    console.log('✅ Successfully received data from backend');
    return res.status(200).json(data);
  } catch (error) {
    console.error('💥 Proxy error:', error);
    
    // Handle specific error types
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        return res.status(504).json({
          error: 'Request timeout',
          details: 'Backend request took too long to respond',
          apiBaseUrl: API_BASE_URL
        });
      }
      
      if (error.message.includes('fetch')) {
        return res.status(502).json({
          error: 'Network error',
          details: error.message,
          apiBaseUrl: API_BASE_URL,
          hint: 'Check if backend is accessible'
        });
      }
    }
    
    return res.status(500).json({
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error',
      apiBaseUrl: API_BASE_URL,
      hasApiKey: !!API_KEY
    });
  }
}

async function handlePost(req: NextApiRequest, res: NextApiResponse, path: string) {
  try {
    const baseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
    const response = await fetch(`${baseUrl}/api/v1/${path}`, {
      method: 'POST',
      headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(req.body),
    });

    if (!response.ok) {
      return res.status(response.status).json({
        error: 'Backend request failed'
      });
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    return res.status(500).json({
      error: 'Internal server error'
    });
  }
}

async function handlePut(req: NextApiRequest, res: NextApiResponse, path: string) {
  try {
    const baseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
    const response = await fetch(`${baseUrl}/api/v1/${path}`, {
      method: 'PUT',
      headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(req.body),
    });

    if (!response.ok) {
      return res.status(response.status).json({
        error: 'Backend request failed'
      });
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    return res.status(500).json({
      error: 'Internal server error'
    });
  }
}

async function handleDelete(req: NextApiRequest, res: NextApiResponse, path: string) {
  try {
    const baseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
    const response = await fetch(`${baseUrl}/api/v1/${path}`, {
      method: 'DELETE',
      headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      return res.status(response.status).json({
        error: 'Backend request failed'
      });
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    return res.status(500).json({
      error: 'Internal server error'
    });
  }
}

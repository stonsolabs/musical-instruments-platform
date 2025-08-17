import { NextApiRequest, NextApiResponse } from 'next';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const API_KEY = process.env.API_KEY || '';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Test the backend connection
    const response = await fetch(`${API_BASE_URL}/health`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const healthData = await response.json();

    // Test a protected endpoint
    const productsResponse = await fetch(`${API_BASE_URL}/api/v1/products?limit=1`, {
      headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json',
      },
    });

    const productsData = productsResponse.ok ? await productsResponse.json() : { error: productsResponse.statusText };

    return res.status(200).json({
      timestamp: new Date().toISOString(),
      environment: {
        API_BASE_URL,
        hasApiKey: !!API_KEY,
        nodeEnv: process.env.NODE_ENV,
      },
      backend: {
        health: healthData,
        products: productsData,
        productsStatus: productsResponse.status,
      },
      proxy: {
        expectedUrl: `${API_BASE_URL}/api/v1/products`,
        proxyUrl: `/api/proxy/products`,
      }
    });
  } catch (error) {
    return res.status(500).json({
      error: error instanceof Error ? error.message : 'Unknown error',
      environment: {
        API_BASE_URL,
        hasApiKey: !!API_KEY,
        nodeEnv: process.env.NODE_ENV,
      }
    });
  }
}

import { NextResponse } from 'next/server';

export async function GET() {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  const apiKey = process.env.API_KEY;
  
  return NextResponse.json({
    environment: process.env.NODE_ENV,
    apiBaseUrl: apiBaseUrl || 'NOT_SET',
    hasApiKey: !!apiKey,
    apiKeyLength: apiKey ? apiKey.length : 0,
    timestamp: new Date().toISOString(),
    message: 'Debug endpoint - check Vercel logs for proxy errors'
  });
}

import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    environment: {
      nodeEnv: process.env.NODE_ENV,
      hasApiBaseUrl: !!process.env.NEXT_PUBLIC_API_BASE_URL,
      hasApiKey: !!process.env.API_KEY,
      apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || 'NOT_SET',
    },
    message: 'Frontend is running correctly'
  });
}

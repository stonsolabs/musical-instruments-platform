import { NextResponse } from 'next/server';
import { getApiBaseUrl } from '../../../lib/api';

export async function GET() {
  try {
    // Check if we can connect to the backend API
    const apiUrl = getApiBaseUrl();
    
    let backendStatus = 'unknown';
    
    if (apiUrl) {
      try {
        const response = await fetch(`${apiUrl}/health`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          // Short timeout for health checks
          signal: AbortSignal.timeout(5000)
        });
        
        backendStatus = response.ok ? 'healthy' : 'unhealthy';
      } catch (error) {
        backendStatus = 'unreachable';
      }
    }
    
    return NextResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'Musical Instruments Platform Frontend',
      backend: {
        url: apiUrl,
        status: backendStatus
      },
      environment: process.env.NODE_ENV,
      version: process.env.npm_package_version || '1.0.0'
    });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: 'Health check failed'
      },
      { status: 500 }
    );
  }
}

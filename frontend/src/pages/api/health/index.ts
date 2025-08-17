import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  return res.status(200).json({
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

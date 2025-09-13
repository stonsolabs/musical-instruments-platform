import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { redirect_url = '/' } = req.query;
  const azureBackend = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';
  
  // Construct the Azure AD login URL with proper redirect
  const callbackUrl = `${req.headers.origin || 'https://www.getyourmusicgear.com'}/api/auth/callback?redirect_url=${encodeURIComponent(String(redirect_url))}`;
  const azureLoginUrl = `${azureBackend}/.auth/login/aad?post_login_redirect_url=${encodeURIComponent(callbackUrl)}`;
  
  console.log(`[AUTH] Redirecting to Azure AD: ${azureLoginUrl}`);
  
  // Redirect to Azure App Service for authentication
  res.redirect(302, azureLoginUrl);
}
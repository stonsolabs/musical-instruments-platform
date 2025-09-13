import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { redirect_url = '/admin' } = req.query;
  
  console.log(`[AUTH] Callback received, redirecting to: ${redirect_url}`);
  
  // After Azure AD authentication, redirect back to the original destination
  res.redirect(302, String(redirect_url));
}
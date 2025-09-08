import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const base = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
    const { path = [] } = req.query as { path: string[] };
    const qs = req.url?.includes('?') ? req.url.substring(req.url.indexOf('?')) : '';
    const target = `${base}/api/${path.join('/')}${qs}`;

    const headers: Record<string, string> = {
      'Content-Type': req.headers['content-type'] || 'application/json',
      'X-API-Key': process.env.API_KEY || '',
    };
    // Forward user ip if needed
    if (req.headers['x-forwarded-for']) headers['x-forwarded-for'] = String(req.headers['x-forwarded-for']);

    const init: RequestInit = {
      method: req.method,
      headers,
    };
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      init.body = req.body && typeof req.body === 'string' ? req.body : JSON.stringify(req.body || {});
    }

    const r = await fetch(target, init);
    const contentType = r.headers.get('content-type') || '';
    res.status(r.status);
    if (contentType.includes('application/json')) {
      const data = await r.json();
      res.json(data);
    } else {
      const text = await r.text();
      res.send(text);
    }
  } catch (e: any) {
    res.status(500).json({ error: 'Proxy error', detail: e?.message || String(e) });
  }
}


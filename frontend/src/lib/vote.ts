// Centralized voting API helpers (client and SSR-safe)

function abs(path: string): string {
  if (typeof window !== 'undefined') return path;
  const origin = process.env.NEXT_PUBLIC_APP_ORIGIN
    || (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : 'http://localhost:3000');
  return origin.replace(/\/$/, '') + path;
}

const PROXY_BASE = '/api/proxy/v1';

const jsonHeaders: HeadersInit = { 'Content-Type': 'application/json' };

export async function submitVote(productId: number, voteType: 'up' | 'down') {
  const res = await fetch(abs(`${PROXY_BASE}/voting/products/${productId}/vote`), {
    method: 'POST',
    headers: jsonHeaders,
    body: JSON.stringify({ vote_type: voteType }),
  });
  if (!res.ok) {
    const txt = await res.text().catch(() => '');
    throw new Error(`Vote failed: ${res.status} ${res.statusText} ${txt}`);
  }
  return res.json();
}

export async function getVoteStats(productId: number) {
  const res = await fetch(abs(`${PROXY_BASE}/voting/products/${productId}/stats`), {
    headers: jsonHeaders,
  });
  if (!res.ok) {
    const txt = await res.text().catch(() => '');
    throw new Error(`Stats fetch failed: ${res.status} ${res.statusText} ${txt}`);
  }
  return res.json();
}


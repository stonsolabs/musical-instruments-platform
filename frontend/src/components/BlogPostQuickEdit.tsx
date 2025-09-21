import React, { useEffect, useState } from 'react';

interface QuickEditProps {
  isOpen: boolean;
  postId: number;
  onClose: () => void;
  onSaved?: () => void;
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';

export default function BlogPostQuickEdit({ isOpen, postId, onClose, onSaved }: QuickEditProps) {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [title, setTitle] = useState('');
  const [excerpt, setExcerpt] = useState('');
  const [seoTitle, setSeoTitle] = useState('');
  const [seoDesc, setSeoDesc] = useState('');
  const [contentJson, setContentJson] = useState<any>({ sections: [] });

  useEffect(() => {
    if (!isOpen) return;
    const fetchPost = async () => {
      setLoading(true);
      setError(null);
      try {
        const resp = await fetch(`${API_BASE}/api/v1/blog/posts/by-id/${postId}`);
        if (!resp.ok) throw new Error(`Fetch failed: ${resp.status}`);
        const data = await resp.json();
        setTitle(data.title || '');
        setExcerpt(data.excerpt || '');
        setSeoTitle(data.seo_title || data.title || '');
        setSeoDesc(data.seo_description || data.excerpt || '');
        setContentJson((data as any).content_json || { sections: [] });
      } catch (e: any) {
        setError(e?.message || 'Failed to load post');
      } finally {
        setLoading(false);
      }
    };
    fetchPost();
  }, [isOpen, postId]);

  const addSpotlight = (variant: 'full' | 'compact') => {
    const ids = prompt('Enter product IDs (comma-separated):');
    if (!ids) return;
    const arr = ids.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n));
    if (arr.length === 0) return;
    const section: any = {
      type: variant === 'compact' ? 'product_spotlight_compact' : 'product_spotlight',
      products: arr.map(id => ({ id })),
      variant: variant,
    };
    setContentJson((prev: any) => ({
      ...prev,
      sections: Array.isArray(prev.sections) ? [...prev.sections, section] : [section],
    }));
  };

  const moveSection = (index: number, dir: -1 | 1) => {
    setContentJson((prev: any) => {
      const secs = Array.isArray(prev.sections) ? [...prev.sections] : [];
      const ni = index + dir;
      if (ni < 0 || ni >= secs.length) return prev;
      const tmp = secs[index];
      secs[index] = secs[ni];
      secs[ni] = tmp;
      return { ...prev, sections: secs };
    });
  };

  const removeSection = (index: number) => {
    setContentJson((prev: any) => {
      const secs = Array.isArray(prev.sections) ? [...prev.sections] : [];
      secs.splice(index, 1);
      return { ...prev, sections: secs };
    });
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    try {
      const adminToken = typeof window !== 'undefined' ? sessionStorage.getItem('adminToken') : null;
      const resp = await fetch(`${API_BASE}/api/v1/admin/blog/posts/${postId}`, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          ...(adminToken ? { 'X-Admin-Token': adminToken } : {}),
        },
        body: JSON.stringify({
          title,
          excerpt,
          seo_title: seoTitle,
          seo_description: seoDesc,
          content_json: contentJson,
        }),
      });
      if (!resp.ok) throw new Error(`Update failed: ${resp.status}`);
      onSaved?.();
      onClose();
    } catch (e: any) {
      setError(e?.message || 'Save failed');
    } finally {
      setSaving(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/40">
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-xl w-full max-w-5xl max-h-[90vh] overflow-y-auto">
          <div className="flex items-center justify-between p-4 border-b">
            <h3 className="text-xl font-bold">Quick Edit Post #{postId}</h3>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-700">✕</button>
          </div>
          <div className="p-4 space-y-4">
            {loading ? (
              <div className="text-gray-600">Loading…</div>
            ) : error ? (
              <div className="text-red-600">{error}</div>
            ) : (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Title</label>
                    <input className="w-full border rounded px-3 py-2" value={title} onChange={e => setTitle(e.target.value)} />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Excerpt</label>
                    <input className="w-full border rounded px-3 py-2" value={excerpt} onChange={e => setExcerpt(e.target.value)} />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">SEO Title</label>
                    <input className="w-full border rounded px-3 py-2" value={seoTitle} onChange={e => setSeoTitle(e.target.value)} />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">SEO Description</label>
                    <input className="w-full border rounded px-3 py-2" value={seoDesc} onChange={e => setSeoDesc(e.target.value)} />
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button onClick={() => addSpotlight('full')} className="px-3 py-2 bg-gray-100 rounded hover:bg-gray-200 text-sm">+ Add Spotlight (Full)</button>
                  <button onClick={() => addSpotlight('compact')} className="px-3 py-2 bg-gray-100 rounded hover:bg-gray-200 text-sm">+ Add Spotlight (Compact)</button>
                </div>

                {/* Sections quick view */}
                <div className="space-y-2">
                  <h4 className="font-semibold">Sections</h4>
                  {Array.isArray(contentJson.sections) && contentJson.sections.length > 0 ? (
                    contentJson.sections.map((s: any, i: number) => (
                      <div key={i} className="flex items-center justify-between border rounded p-2 text-sm">
                        <div>
                          <span className="font-medium">{s.type}</span>
                          {s.title ? <span className="text-gray-500 ml-2">{s.title}</span> : null}
                          {s.variant ? <span className="text-gray-400 ml-2">({s.variant})</span> : null}
                        </div>
                        <div className="flex items-center gap-2">
                          <button onClick={() => moveSection(i, -1)} className="px-2 py-1 border rounded">↑</button>
                          <button onClick={() => moveSection(i, 1)} className="px-2 py-1 border rounded">↓</button>
                          <button onClick={() => removeSection(i)} className="px-2 py-1 border rounded text-red-600">Remove</button>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-gray-500 text-sm">No sections</div>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">content_json (raw)</label>
                  <textarea className="w-full border rounded px-3 py-2 font-mono text-xs" rows={12} value={JSON.stringify(contentJson, null, 2)} onChange={e => {
                    try { setContentJson(JSON.parse(e.target.value)); setError(null); }
                    catch { setError('Invalid JSON'); }
                  }} />
                </div>

                <div className="flex items-center justify-end gap-2">
                  <button onClick={onClose} className="px-4 py-2 border rounded">Cancel</button>
                  <button onClick={handleSave} disabled={saving || !!error} className="px-4 py-2 bg-brand-primary text-white rounded disabled:opacity-50">{saving ? 'Saving…' : 'Save'}</button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}


import React, { useEffect, useMemo, useState } from 'react';

const ADMIN_API_BASE = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net'}/api/v1`;

export default function BlogTemplatesManager() {
  const [templates, setTemplates] = useState<any[]>([]);
  const [selected, setSelected] = useState<any | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const adminHeaders = useMemo(() => {
    const adminToken = typeof window !== 'undefined' ? sessionStorage.getItem('adminToken') : null;
    return { 'Content-Type': 'application/json', ...(adminToken ? { 'X-Admin-Token': adminToken } : {}) } as HeadersInit;
  }, []);

  const loadTemplates = async () => {
    try {
      const res = await fetch(`${ADMIN_API_BASE}/admin/blog/templates`, { credentials: 'include', headers: adminHeaders });
      const data = await res.json();
      setTemplates(Array.isArray(data) ? data : []);
    } catch (e) {
      setMessage('Failed to load templates');
    }
  };

  useEffect(() => { loadTemplates(); }, []);

  const editTemplate = (tpl: any) => {
    setSelected({ ...tpl, content_structure_text: JSON.stringify(tpl.content_structure || {}, null, 2), suggested_tags_text: (tpl.suggested_tags || []).join(', '), required_product_types_text: (tpl.required_product_types || []).join(', ') });
  };

  const saveTemplate = async () => {
    if (!selected) return;
    try {
      const payload: any = {
        name: selected.name,
        description: selected.description,
        category_id: selected.category_id,
        template_type: selected.template_type,
        base_prompt: selected.base_prompt,
        system_prompt: selected.system_prompt,
        product_context_prompt: selected.product_context_prompt,
        min_products: Number(selected.min_products) || 0,
        max_products: Number(selected.max_products) || 10,
        is_active: !!selected.is_active,
      };
      try { payload.content_structure = JSON.parse(selected.content_structure_text || '{}'); } catch { payload.content_structure = {}; }
      payload.suggested_tags = String(selected.suggested_tags_text || '').split(',').map(s=>s.trim()).filter(Boolean);
      payload.required_product_types = String(selected.required_product_types_text || '').split(',').map(s=>s.trim()).filter(Boolean);

      const res = await fetch(`${ADMIN_API_BASE}/admin/blog/templates/${selected.id}`, {
        method: 'PUT', credentials: 'include', headers: adminHeaders, body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error('Save failed');
      setMessage('Template saved');
      setSelected(null);
      loadTemplates();
    } catch (e) {
      setMessage('Failed to save template');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">AI Templates</h2>
        <button onClick={loadTemplates} className="text-sm text-gray-600 hover:text-gray-800">Refresh</button>
      </div>
      {message && <div className="text-sm text-gray-700">{message}</div>}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {templates.map(t => (
          <div key={t.id} className="bg-white p-5 rounded-lg shadow border">
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-semibold">{t.name}</h3>
              <span className="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-700">{t.template_type}</span>
            </div>
            <p className="text-sm text-gray-600 line-clamp-2 mb-3">{t.description}</p>
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>Min/Max: {t.min_products}/{t.max_products}</span>
              <span>{t.is_active ? 'Active' : 'Inactive'}</span>
            </div>
            <div className="mt-3">
              <button onClick={() => editTemplate(t)} className="text-sm text-brand-primary hover:text-brand-dark">Edit</button>
            </div>
          </div>
        ))}
      </div>

      {selected && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-3xl rounded-lg shadow-lg overflow-auto max-h-[90vh]">
            <div className="p-4 border-b flex items-center justify-between">
              <h3 className="font-semibold">Edit Template</h3>
              <button onClick={()=>setSelected(null)} className="text-gray-500">✕</button>
            </div>
            <div className="p-4 space-y-3">
              <div>
                <label className="block text-sm text-gray-600 mb-1">Name</label>
                <input className="w-full border rounded px-3 py-2" value={selected.name} onChange={e=>setSelected({...selected, name: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Description</label>
                <input className="w-full border rounded px-3 py-2" value={selected.description||''} onChange={e=>setSelected({...selected, description: e.target.value})} />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Template Type</label>
                  <input className="w-full border rounded px-3 py-2" value={selected.template_type} onChange={e=>setSelected({...selected, template_type: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Category ID</label>
                  <input type="number" className="w-full border rounded px-3 py-2" value={selected.category_id||''} onChange={e=>setSelected({...selected, category_id: Number(e.target.value)||null})} />
                </div>
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">System Prompt</label>
                <textarea rows={4} className="w-full border rounded px-3 py-2" value={selected.system_prompt||''} onChange={e=>setSelected({...selected, system_prompt: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Base Prompt</label>
                <textarea rows={6} className="w-full border rounded px-3 py-2" value={selected.base_prompt||''} onChange={e=>setSelected({...selected, base_prompt: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Product Context Prompt</label>
                <textarea rows={3} className="w-full border rounded px-3 py-2" value={selected.product_context_prompt||''} onChange={e=>setSelected({...selected, product_context_prompt: e.target.value})} />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Min Products</label>
                  <input type="number" className="w-full border rounded px-3 py-2" value={selected.min_products||0} onChange={e=>setSelected({...selected, min_products: Number(e.target.value)||0})} />
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Max Products</label>
                  <input type="number" className="w-full border rounded px-3 py-2" value={selected.max_products||10} onChange={e=>setSelected({...selected, max_products: Number(e.target.value)||10})} />
                </div>
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Suggested Tags (comma separated)</label>
                <input className="w-full border rounded px-3 py-2" value={selected.suggested_tags_text||''} onChange={e=>setSelected({...selected, suggested_tags_text: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Required Product Types (comma separated)</label>
                <input className="w-full border rounded px-3 py-2" value={selected.required_product_types_text||''} onChange={e=>setSelected({...selected, required_product_types_text: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Content Structure (JSON)</label>
                <textarea rows={10} className="w-full font-mono text-xs border rounded px-3 py-2" value={selected.content_structure_text||''} onChange={e=>setSelected({...selected, content_structure_text: e.target.value})} />
              </div>
              <div className="flex items-center gap-2">
                <input id="is_active_tpl" type="checkbox" checked={!!selected.is_active} onChange={e=>setSelected({...selected, is_active: e.target.checked})} />
                <label htmlFor="is_active_tpl" className="text-sm text-gray-700">Active</label>
              </div>
              <div className="flex justify-end gap-2 pt-3">
                <button onClick={()=>setSelected(null)} className="px-4 py-2 border rounded">Cancel</button>
                <button onClick={saveTemplate} className="px-4 py-2 bg-brand-primary text-white rounded">Save</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}


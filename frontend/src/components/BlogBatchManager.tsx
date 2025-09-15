import React, { useEffect, useMemo, useState } from 'react';

const ADMIN_API_BASE = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net'}/api/v1`;

interface Template {
  id: number;
  name: string;
  template_type: string;
  min_products: number;
  max_products: number;
}

interface BatchJob {
  id: number;
  batch_id: string;
  batch_name: string;
  request_count: number;
  status: string;
  azure_batch_id?: string;
  created_at: string;
  azure_created_at?: string;
  completed_at?: string;
  total_requests?: number;
  completed_requests?: number;
  failed_requests?: number;
  created_by_email?: string;
}

export default function BlogBatchManager() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(false);
  const [batchName, setBatchName] = useState('batch-' + new Date().toISOString().slice(0,10));
  const [templateId, setTemplateId] = useState<number | ''>('' as any);
  const [totalRequests, setTotalRequests] = useState(50);
  const [productsPerPost, setProductsPerPost] = useState(3);
  const [productIdsInput, setProductIdsInput] = useState('');
  const [targetWordCount, setTargetWordCount] = useState(2000);
  const [autoPublish, setAutoPublish] = useState(false);
  const [batches, setBatches] = useState<BatchJob[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  const adminHeaders = useMemo(() => {
    const adminToken = typeof window !== 'undefined' ? sessionStorage.getItem('adminToken') : null;
    return { 'Content-Type': 'application/json', ...(adminToken ? { 'X-Admin-Token': adminToken } : {}) } as HeadersInit;
  }, []);

  useEffect(() => {
    loadTemplates();
    loadBatches();
  }, []);

  const loadTemplates = async () => {
    try {
      const res = await fetch(`${ADMIN_API_BASE}/admin/blog/templates`, { credentials: 'include', headers: adminHeaders });
      if (res.ok) {
        const data = await res.json();
        setTemplates(data);
      }
    } catch (e) {
      console.error('Failed to load templates', e);
    }
  };

  const loadBatches = async () => {
    try {
      const res = await fetch(`${ADMIN_API_BASE}/admin/blog/batches?limit=20`, { credentials: 'include', headers: adminHeaders });
      if (res.ok) {
        const data = await res.json();
        setBatches(data.batches || data || []);
      }
    } catch (e) {
      console.error('Failed to load batches', e);
    }
  };

  const parseProductIds = (): number[] => {
    return productIdsInput
      .split(/[\s,]+/)
      .map(s => s.trim())
      .filter(Boolean)
      .map(n => parseInt(n, 10))
      .filter(n => Number.isFinite(n));
  };

  const buildGenerationRequests = (): any[] => {
    const ids = parseProductIds();
    const reqs: any[] = [];
    for (let i = 0; i < totalRequests; i++) {
      let selected: number[] = [];
      if (ids.length > 0) {
        // sample without caring about uniqueness across posts
        selected = Array.from({ length: Math.min(productsPerPost, ids.length) }, () => ids[Math.floor(Math.random() * ids.length)]);
      }
      reqs.push({
        template_id: templateId,
        product_ids: selected,
        target_word_count: targetWordCount,
        include_seo_optimization: true,
        auto_publish: autoPublish,
        generation_params: {},
        provider: 'openai',
      });
    }
    return reqs;
  };

  const createBatch = async () => {
    if (!templateId) {
      setMessage('Select a template');
      return;
    }
    setLoading(true);
    setMessage(null);
    try {
      const generation_requests = buildGenerationRequests();
      const res = await fetch(`${ADMIN_API_BASE}/admin/blog/batch/create?batch_name=${encodeURIComponent(batchName)}`, {
        method: 'POST',
        credentials: 'include',
        headers: adminHeaders,
        body: JSON.stringify(generation_requests),
      });
      const data = await res.json();
      if (!res.ok || data.success === false) throw new Error(data.detail || data.error || 'Failed to create batch');
      setMessage(`Batch created: ${data.batch_id || data.batch_name}`);
      loadBatches();
    } catch (e: any) {
      console.error(e);
      setMessage(`Error: ${e.message || String(e)}`);
    } finally {
      setLoading(false);
    }
  };

  const uploadBatch = async (batch_id: string) => {
    setMessage(null);
    const res = await fetch(`${ADMIN_API_BASE}/admin/blog/batch/${encodeURIComponent(batch_id)}/upload`, { method: 'POST', credentials: 'include', headers: adminHeaders });
    const data = await res.json();
    if (!res.ok || data.success === false) { setMessage(`Upload failed: ${data.detail || data.error || res.status}`); return; }
    setMessage('Uploaded to Azure. Input file id: ' + (data.input_file_id || data.file_id || 'n/a'));
  };

  const startBatch = async (file_id: string, name: string) => {
    setMessage(null);
    const res = await fetch(`${ADMIN_API_BASE}/admin/blog/batch/${encodeURIComponent(file_id)}/start?batch_name=${encodeURIComponent(name)}`, { method: 'POST', credentials: 'include', headers: adminHeaders });
    const data = await res.json();
    if (!res.ok || data.success === false) { setMessage(`Start failed: ${data.detail || data.error || res.status}`); return; }
    setMessage('Batch started. Azure batch id: ' + data.batch_id);
  };

  const checkStatus = async (azure_batch_id: string) => {
    setMessage(null);
    const res = await fetch(`${ADMIN_API_BASE}/admin/blog/batch/${encodeURIComponent(azure_batch_id)}/status`, { credentials: 'include', headers: adminHeaders });
    const data = await res.json();
    if (!res.ok) { setMessage(`Status failed: ${res.status}`); return; }
    setMessage('Status: ' + JSON.stringify(data));
  };

  const downloadResults = async (azure_batch_id: string) => {
    setMessage('Provide output_file_id from Azure response in prompt');
    const output_file_id = window.prompt('Enter output_file_id from Azure batch status/result:');
    if (!output_file_id) return;
    const res = await fetch(`${ADMIN_API_BASE}/admin/blog/batch/${encodeURIComponent(azure_batch_id)}/download`, {
      method: 'POST', credentials: 'include', headers: adminHeaders, body: JSON.stringify({ output_file_id })
    });
    const data = await res.json();
    if (!res.ok || data.success === false) { setMessage(`Download failed: ${data.detail || data.error || res.status}`); return; }
    setMessage('Downloaded results. Local path: ' + (data.results_file_path || 'n/a'));
  };

  const processResults = async () => {
    const results_file_path = window.prompt('Enter results_file_path (local path on server):');
    const metadata_file_path = window.prompt('Enter metadata_file_path (local path on server):');
    if (!results_file_path || !metadata_file_path) return;
    const res = await fetch(`${ADMIN_API_BASE}/admin/blog/batch/process`, {
      method: 'POST', credentials: 'include', headers: adminHeaders,
      body: JSON.stringify({ results_file_path, metadata_file_path, auto_publish: false })
    });
    const data = await res.json();
    if (!res.ok || data.success === false) { setMessage(`Process failed: ${data.detail || data.error || res.status}`); return; }
    setMessage(`Processed. Created posts: ${data.total_processed || 'n/a'}`);
  };

  const selectedTemplate = templates.find(t => t.id === templateId);

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Create Azure/OpenAI Batch</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-600 mb-1">Batch name</label>
            <input value={batchName} onChange={(e) => setBatchName(e.target.value)} className="w-full px-3 py-2 border rounded" />
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">Template</label>
            <select value={templateId} onChange={(e) => setTemplateId(Number(e.target.value))} className="w-full px-3 py-2 border rounded">
              <option value="" disabled>Select template</option>
              {templates.map(t => (
                <option key={t.id} value={t.id}>{t.name} ({t.template_type})</option>
              ))}
            </select>
            {selectedTemplate && (
              <p className="text-xs text-gray-500 mt-1">Min/Max products per post: {selectedTemplate.min_products}/{selectedTemplate.max_products}</p>
            )}
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">Total requests</label>
            <input type="number" min={1} max={1000} value={totalRequests} onChange={(e) => setTotalRequests(parseInt(e.target.value || '1', 10))} className="w-full px-3 py-2 border rounded"/>
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">Products per post (optional)</label>
            <input type="number" min={1} max={10} value={productsPerPost} onChange={(e) => setProductsPerPost(parseInt(e.target.value || '1', 10))} className="w-full px-3 py-2 border rounded"/>
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm text-gray-600 mb-1">Product IDs (comma/space separated; optional)</label>
            <textarea value={productIdsInput} onChange={(e) => setProductIdsInput(e.target.value)} rows={3} className="w-full px-3 py-2 border rounded" placeholder="e.g. 573, 865, 589" />
            <p className="text-xs text-gray-500 mt-1">If left empty, the backend selects relevant products per template.</p>
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">Target word count</label>
            <input type="number" min={800} max={4000} value={targetWordCount} onChange={(e) => setTargetWordCount(parseInt(e.target.value || '1800', 10))} className="w-full px-3 py-2 border rounded"/>
          </div>
          <div className="flex items-center gap-2">
            <input id="autopub" type="checkbox" checked={autoPublish} onChange={(e) => setAutoPublish(e.target.checked)} />
            <label htmlFor="autopub" className="text-sm text-gray-600">Auto publish results</label>
          </div>
        </div>
        <div className="mt-4 flex gap-3">
          <button onClick={createBatch} disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">{loading ? 'Creating...' : 'Create Batch'}</button>
          <button onClick={processResults} className="px-4 py-2 border rounded">Process Downloaded Results</button>
        </div>
        {message && <div className="mt-3 text-sm text-gray-700">{message}</div>}
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-xl font-semibold">Recent Batches</h2>
          <button onClick={loadBatches} className="text-sm text-gray-600 hover:text-gray-800">Refresh</button>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left text-gray-600">
                <th className="px-3 py-2">Name</th>
                <th className="px-3 py-2">Batch ID</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Azure Batch</th>
                <th className="px-3 py-2">Requests</th>
                <th className="px-3 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {batches.map(b => (
                <tr key={b.batch_id} className="border-t">
                  <td className="px-3 py-2">{b.batch_name || b.batch_id}</td>
                  <td className="px-3 py-2 font-mono text-xs">{b.batch_id}</td>
                  <td className="px-3 py-2">
                    <span className={`px-2 py-1 rounded text-xs ${b.status === 'completed' ? 'bg-green-100 text-green-700' : b.status === 'failed' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'}`}>{b.status}</span>
                  </td>
                  <td className="px-3 py-2 font-mono text-xs">{b.azure_batch_id || '-'}</td>
                  <td className="px-3 py-2">{b.request_count}</td>
                  <td className="px-3 py-2 flex gap-2">
                    <button onClick={() => uploadBatch(b.batch_id)} className="text-blue-600 hover:text-blue-800">Upload</button>
                    <button onClick={() => startBatch(prompt('Input file_id from upload result') || '', b.batch_name)} className="text-indigo-600 hover:text-indigo-800">Start</button>
                    {b.azure_batch_id && <button onClick={() => checkStatus(b.azure_batch_id!)} className="text-gray-700 hover:text-black">Status</button>}
                    {b.azure_batch_id && <button onClick={() => downloadResults(b.azure_batch_id!)} className="text-green-700 hover:text-green-900">Download</button>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

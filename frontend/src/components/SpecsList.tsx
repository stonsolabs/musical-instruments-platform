import React from 'react';

interface SpecItem { label: string; value: string; }

export default function SpecsList({ specs = [] as SpecItem[] }) {
  if (!specs.length) return null;
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {specs.map((s, i) => (
        <div key={i} className="flex justify-between gap-3 bg-white border border-gray-200 rounded-lg px-3 py-2 shadow-sm">
          <span className="text-gray-600">{s.label}</span>
          <span className="text-gray-900 font-medium text-right">{s.value}</span>
        </div>
      ))}
    </div>
  );
}

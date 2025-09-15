import React from 'react';

export default function ProsCons({ pros = [], cons = [] as string[] }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="p-5 rounded-lg bg-green-50 border border-green-200">
        <h4 className="font-semibold text-green-800 mb-3">Pros</h4>
        <ul className="list-disc list-inside text-green-900 space-y-1">
          {pros.map((p, i) => (
            <li key={i}>{p}</li>
          ))}
        </ul>
      </div>
      <div className="p-5 rounded-lg bg-red-50 border border-red-200">
        <h4 className="font-semibold text-red-800 mb-3">Cons</h4>
        <ul className="list-disc list-inside text-red-900 space-y-1">
          {cons.map((c, i) => (
            <li key={i}>{c}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}


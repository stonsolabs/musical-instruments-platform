import React from 'react';

interface ProsConsProps {
  pros?: string[];
  cons?: string[];
}

export default function ProsCons({ pros = [], cons = [] }: ProsConsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="p-5 rounded-lg border border-gray-200 bg-white">
        <h4 className="font-semibold text-gray-900 mb-3">Pros</h4>
        <ul className="list-disc list-inside text-gray-800 space-y-1">
          {pros.map((p, i) => (
            <li key={i}>{p}</li>
          ))}
        </ul>
      </div>
      <div className="p-5 rounded-lg border border-gray-200 bg-white">
        <h4 className="font-semibold text-gray-900 mb-3">Cons</h4>
        <ul className="list-disc list-inside text-gray-800 space-y-1">
          {cons.map((c, i) => (
            <li key={i}>{c}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

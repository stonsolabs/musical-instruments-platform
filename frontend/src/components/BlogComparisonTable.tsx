import React from 'react';

interface Props {
  headers?: string[];
  rows?: string[][];
}

export default function BlogComparisonTable({ headers = [], rows = [] }: Props) {
  if (!headers.length || !rows.length) return null;
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 shadow-sm bg-white">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-50">
          <tr>
            {headers.map((h, i) => (
              <th key={i} className="px-4 py-3 text-left font-semibold text-gray-700">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, idx) => (
            <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
              {r.map((cell, j) => (
                <td key={j} className="px-4 py-3 align-top text-gray-800">{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}


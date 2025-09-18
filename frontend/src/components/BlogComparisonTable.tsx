import React from 'react';

interface Props {
  headers?: string[];
  rows?: string[][];
}

export default function BlogComparisonTable({ headers = [], rows = [] }: Props) {
  if (!headers.length || !rows.length) return null;
  
  return (
    <div className="w-full overflow-x-auto rounded-lg border border-gray-200 shadow-sm bg-white my-6">
      <div className="min-w-full">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              {headers.map((h, i) => (
                <th 
                  key={i} 
                  className={`px-3 sm:px-4 py-3 text-left font-semibold text-gray-700 whitespace-nowrap ${
                    i === 0 ? 'sticky left-0 bg-gray-50 z-10' : ''
                  }`}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, idx) => (
              <tr key={idx} className={`${idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'} hover:bg-gray-100 transition-colors`}>
                {r.map((cell, j) => (
                  <td 
                    key={j} 
                    className={`px-3 sm:px-4 py-3 align-top text-gray-800 break-words ${
                      j === 0 ? 'sticky left-0 bg-inherit z-10 font-medium' : ''
                    }`}
                  >
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}


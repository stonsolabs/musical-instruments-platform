import React from 'react';

interface ProductSpecificationsProps {
  specifications: Record<string, string | number | boolean>;
}

export default function ProductSpecifications({ specifications }: ProductSpecificationsProps) {
  if (!specifications || Object.keys(specifications).length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No specifications available for this product.</p>
      </div>
    );
  }

  const formatValue = (value: string | number | boolean): string => {
    if (typeof value === 'boolean') {
      return value ? 'Yes' : 'No';
    }
    if (typeof value === 'number') {
      return value.toString();
    }
    return value;
  };

  const formatKey = (key: string): string => {
    return key
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (l) => l.toUpperCase())
      .replace(/\b(kg|mm|cm|in|lb|oz|db|hz|khz|mhz|ghz|w|kw|v|mv|a|ma|ohm|kohm|mohm|f|uf|nf|pf|h|mh|uh|deg|°|rpm|bpm|ms|s|min|hr|year|yr)\b/gi, (match) => match.toUpperCase());
  };

  const groupedSpecs = Object.entries(specifications).reduce((acc, [key, value]) => {
    const category = key.includes('_') ? key.split('_')[0] : 'general';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push([key, value]);
    return acc;
  }, {} as Record<string, [string, string | number | boolean][]>);

  return (
    <div className="card">
      <div className="overflow-x-auto">
        <table className="w-full table-fixed text-sm">
          <thead>
            <tr className="bg-gray-50">
              <th className="p-3 text-left font-semibold text-gray-900 border-b border-gray-200 w-1/3">
                Specification
              </th>
              <th className="p-3 text-left font-semibold text-gray-900 border-b border-gray-200">
                Value
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {Object.entries(groupedSpecs).map(([category, specs]) => (
              <React.Fragment key={category}>
                {/* Category Header */}
                <tr className="bg-gray-50">
                  <td className="p-3 font-semibold text-gray-900 capitalize" colSpan={2}>
                    <span className="flex items-center">
                      <span className="mr-2">⚙️</span>
                      {category.replace(/_/g, ' ')}
                    </span>
                  </td>
                </tr>
                {/* Category Specifications */}
                {specs.map(([key, value]) => (
                  <tr key={key} className="hover:bg-gray-50">
                    <td className="p-3 font-medium text-gray-900 capitalize">
                      {formatKey(key)}
                    </td>
                    <td className="p-3 text-gray-700">
                      {formatValue(value)}
                    </td>
                  </tr>
                ))}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

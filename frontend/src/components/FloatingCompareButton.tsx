'use client';

import React from 'react';
import { useRouter } from 'next/navigation';

interface FloatingCompareButtonProps {
  selectedCount: number;
  onCompare: () => void;
  isVisible: boolean;
}

export default function FloatingCompareButton({ selectedCount, onCompare, isVisible }: FloatingCompareButtonProps) {
  console.log('🔍 FloatingCompareButton - selectedCount:', selectedCount, 'isVisible:', isVisible);
  if (!isVisible || selectedCount === 0) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <button
        onClick={() => {
          console.log('🔍 FloatingCompareButton clicked - selectedCount:', selectedCount);
          onCompare();
        }}
        className="bg-gray-800 text-white px-6 py-3 rounded-full shadow-lg hover:bg-gray-700 transition-all duration-200 transform hover:scale-105 flex items-center gap-2"
      >
        <span className="text-lg">🔍</span>
        <span className="font-semibold">
          Compare ({selectedCount})
        </span>
      </button>
    </div>
  );
}

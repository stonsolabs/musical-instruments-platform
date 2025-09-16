import React, { useMemo, useState } from 'react';
import { useRouter } from 'next/router';
import { MagnifyingGlassIcon, PlusIcon } from '@heroicons/react/24/outline';
import { searchProducts } from '../lib/api';
import { getProductImageUrl } from '../lib/utils';

export default function HeroSection() {
  const [searchQueries, setSearchQueries] = useState<string[]>(['']);
  const [selectedSlugs, setSelectedSlugs] = useState<(string | null)[]>([null]);
  const [suggestions, setSuggestions] = useState<Record<number, any[]>>({});
  const [searching, setSearching] = useState<Record<number, boolean>>({});
  const [focusedIndex, setFocusedIndex] = useState<number>(0);
  const [activeIndex, setActiveIndex] = useState<number>(-1);
  const router = useRouter();

  const addSearchField = () => {
    setSearchQueries([...searchQueries, '']);
    setSelectedSlugs([...selectedSlugs, null]);
  };

  const updateSearchQuery = (index: number, value: string) => {
    const newQueries = [...searchQueries];
    newQueries[index] = value;
    setSearchQueries(newQueries);
    // Clear previously selected slug when user edits text
    const newSlugs = [...selectedSlugs];
    newSlugs[index] = null;
    setSelectedSlugs(newSlugs);
  };

  // Debounce helper
  function debounce<T extends (...args: any[]) => any>(fn: T, wait = 300) {
    let t: any;
    return (...args: Parameters<T>) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), wait);
    };
  }

  const runSearch = async (index: number, query: string) => {
    if (!query || query.trim().length < 2) {
      setSuggestions(prev => ({ ...prev, [index]: [] }));
      setSearching(prev => ({ ...prev, [index]: false }));
      return;
    }
    setSearching(prev => ({ ...prev, [index]: true }));
    try {
      const results = await searchProducts(query, 8);
      const mapped = results.map((p: any) => ({
        id: p.id,
        name: p.name,
        brand: p.brand?.name || '',
        category: p.category?.name || '',
        slug: p.slug,
        images: p.images,
      }));
      setSuggestions(prev => ({ ...prev, [index]: mapped }));
    } catch (e) {
      setSuggestions(prev => ({ ...prev, [index]: [] }));
    } finally {
      setSearching(prev => ({ ...prev, [index]: false }));
    }
  };

  const debouncedRunSearch = useMemo(() => debounce(runSearch, 300), []);

  const handleCompare = (e: React.FormEvent) => {
    e.preventDefault();
    const slugs = selectedSlugs.filter(Boolean) as string[];
    const validQueries = searchQueries.filter(q => q.trim());
    if (slugs.length > 0) {
      if (slugs.length === 1) {
        router.push(`/products/${slugs[0]}`);
      } else {
        router.push(`/compare?products=${slugs.join(',')}`);
      }
      return;
    }
    if (validQueries.length > 0) {
      const searchParams = validQueries.map(q => `search=${encodeURIComponent(q.trim())}`).join('&');
      router.push(`/compare?${searchParams}`);
    }
  };

  return (
    <section className="relative bg-white py-16 lg:py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Main Heading */}
          <h1 className="font-display text-4xl md:text-5xl font-bold text-brand-primary mb-12 leading-tight uppercase tracking-wide">
            Compare Instruments
          </h1>

          {/* Comparison Interface */}
          <div className="max-w-4xl mx-auto mb-12">
            <form onSubmit={handleCompare} className="space-y-4">
              {/* Search Fields */}
              <div className="space-y-4">
                {searchQueries.map((query, index) => (
                  <div key={index} className="relative">
                    <input
                      type="text"
                      placeholder={`Search instrument ${index + 1}`}
                      value={query}
                      onChange={(e) => {
                        updateSearchQuery(index, e.target.value);
                        debouncedRunSearch(index, e.target.value);
                      }}
                      onFocus={() => { setFocusedIndex(index); setActiveIndex(-1); }}
                      onKeyDown={(e) => {
                        const list = suggestions[index] || [];
                        if (!list.length) return;
                        if (e.key === 'ArrowDown') {
                          e.preventDefault();
                          setFocusedIndex(index);
                          setActiveIndex((prev) => (prev + 1) % list.length);
                        } else if (e.key === 'ArrowUp') {
                          e.preventDefault();
                          setFocusedIndex(index);
                          setActiveIndex((prev) => (prev - 1 + list.length) % list.length);
                        } else if (e.key === 'Enter') {
                          if (activeIndex >= 0 && activeIndex < list.length) {
                            const p = list[activeIndex];
                            const q = [...searchQueries];
                            q[index] = p.name;
                            setSearchQueries(q);
                            const s = [...selectedSlugs];
                            s[index] = p.slug;
                            setSelectedSlugs(s);
                            setSuggestions(prev => ({ ...prev, [index]: [] }));
                            setActiveIndex(-1);
                          }
                        } else if (e.key === 'Escape') {
                          setSuggestions(prev => ({ ...prev, [index]: [] }));
                          setActiveIndex(-1);
                        }
                      }}
                      className="w-full pl-16 pr-6 py-4 text-lg border border-gray-200 rounded-2xl bg-white shadow-elegant focus:ring-2 focus:ring-brand-primary focus:border-brand-primary focus:outline-none transition-all duration-200"
                    />
                    <MagnifyingGlassIcon className="absolute left-6 top-1/2 transform -translate-y-1/2 h-6 w-6 text-gray-400" />

                    {/* Suggestions */}
                    {suggestions[index] && suggestions[index].length > 0 && (
                      <div className="absolute z-20 w-full mt-2 bg-white border border-gray-200 rounded-xl shadow-lg max-h-64 overflow-y-auto">
                        {suggestions[index].map((p, idx) => (
                          <button
                            key={p.id}
                            type="button"
                            onClick={() => {
                              // set text and selected slug
                              const q = [...searchQueries];
                              q[index] = p.name;
                              setSearchQueries(q);
                              const s = [...selectedSlugs];
                              s[index] = p.slug;
                              setSelectedSlugs(s);
                              setSuggestions(prev => ({ ...prev, [index]: [] }));
                            }}
                            className={`w-full px-4 py-3 text-left border-b border-gray-100 last:border-b-0 flex items-center justify-between gap-3 ${focusedIndex===index && activeIndex===idx ? 'bg-gray-50' : 'hover:bg-gray-50'}`}
                          >
                            <div className="flex items-center gap-3">
                              <div className="w-10 h-10 bg-gray-100 rounded overflow-hidden flex-shrink-0">
                                <img
                                  src={getProductImageUrl(p)}
                                  alt={p.name}
                                  className="w-full h-full object-cover"
                                  onError={(e)=>{(e.target as HTMLImageElement).style.display='none'}}
                                />
                              </div>
                              <div>
                                <div className="font-medium text-gray-900">{p.name}</div>
                                <div className="text-sm text-gray-500">{p.brand} • {p.category}</div>
                              </div>
                            </div>
                            {searching[index] ? (
                              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-300" />
                            ) : null}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Add Another Instrument Button */}
              <button
                type="button"
                onClick={addSearchField}
                className="w-full py-4 border-2 border-dashed border-gray-300 text-gray-600 hover:text-brand-primary hover:border-brand-primary rounded-2xl font-medium transition-colors duration-200 flex items-center justify-center gap-2"
              >
                <PlusIcon className="h-5 w-5" />
                Add another instrument
              </button>

              {/* Compare Button */}
              <button
                type="submit"
                className="btn-primary w-full py-4 text-lg"
              >
                {searchQueries.filter(q => q.trim()).length === 1 
                  ? 'View Instrument' 
                  : `Compare ${searchQueries.filter(q => q.trim()).length || 0} Instruments`
                }
              </button>
            </form>
          </div>

          {/* Trust Indicators */}
          <div className="mt-16 flex flex-col sm:flex-row items-center justify-center gap-8 text-gray-600">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
              <span className="text-sm font-medium">Expert Reviews</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
              <span className="text-sm font-medium">Trusted Partners</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
              <span className="text-sm font-medium">Unbiased Comparisons</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

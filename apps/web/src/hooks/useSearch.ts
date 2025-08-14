import { useEffect, useState } from 'react';
import { searchApi, getFacets, SearchResponse, FacetsResponse } from '../api/search';

export function useSearch(token: string, params: Record<string, any>) {
  const [result, setResult] = useState<SearchResponse | null>(null);
  const [facets, setFacets] = useState<FacetsResponse | null>(null);

  useEffect(() => {
    if (!token) return;
    searchApi(token, params)
      .then((r) => setResult(r))
      .catch(() => setResult(null));
    getFacets(token, params)
      .then((f) => setFacets(f))
      .catch(() => setFacets(null));
  }, [token, JSON.stringify(params)]);

  return { result, facets };
}

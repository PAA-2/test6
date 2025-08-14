const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface SearchItem {
  entity: 'project' | 'file';
  id: string;
  score: number;
  title: string;
  snippet: string;
  status?: string | null;
  mime?: string | null;
  owner_id: string;
  created_at: string;
}

export interface SearchResponse {
  items: SearchItem[];
  page: number;
  page_size: number;
  total: number;
}

export async function searchApi(token: string, params: Record<string, any>): Promise<SearchResponse> {
  const res = await fetch(`${API_URL}/search?${new URLSearchParams(params).toString()}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('search failed');
  return res.json();
}

export interface FacetsResponse {
  projects_by_status: Record<string, number>;
  files_by_mime: { mime: string; count: number }[];
}

export async function getFacets(token: string, params: Record<string, any>): Promise<FacetsResponse> {
  const res = await fetch(`${API_URL}/search/facets?${new URLSearchParams(params).toString()}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('facets failed');
  return res.json();
}

export interface SuggestionItem {
  entity: 'project' | 'file';
  title: string;
}

export async function getSuggestions(token: string, params: { q: string; type: string; limit: number }): Promise<SuggestionItem[]> {
  const res = await fetch(`${API_URL}/search/suggestions?${new URLSearchParams(params as any).toString()}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('suggest failed');
  return res.json();
}

export interface SavedSearch {
  id: string;
  name: string;
  params: Record<string, any>;
  created_at: string;
}

export interface SavedSearchList {
  items: SavedSearch[];
  page: number;
  page_size: number;
  total: number;
}

export async function createSavedSearchApi(token: string, data: { name: string; params: any }): Promise<SavedSearch> {
  const res = await fetch(`${API_URL}/search/saved`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('save failed');
  return res.json();
}

export async function listSavedSearchesApi(token: string): Promise<SavedSearchList> {
  const res = await fetch(`${API_URL}/search/saved`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('list failed');
  return res.json();
}

export async function deleteSavedSearchApi(token: string, id: string): Promise<void> {
  const res = await fetch(`${API_URL}/search/saved/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('delete failed');
}

import { useState } from 'react';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import FacetPanel from '../components/FacetPanel';
import SavedSearchesPanel from '../components/SavedSearchesPanel';
import { useSearch } from '../hooks/useSearch';
import { useSavedSearches } from '../hooks/useSavedSearches';
import { createSavedSearchApi, deleteSavedSearchApi } from '../api/search';

export default function Search() {
  const token = localStorage.getItem('token') || '';
  const [params, setParams] = useState<Record<string, any>>({ type: 'all' });
  const { result, facets } = useSearch(token, params);
  const { data: saved, reload } = useSavedSearches(token);

  const runSearch = (q: string) => setParams({ ...params, q });

  const saveCurrent = async () => {
    if (!token) return;
    await createSavedSearchApi(token, { name: 'saved', params });
    await reload();
  };

  const runSaved = (p: Record<string, any>) => setParams({ ...params, ...p });

  const deleteSaved = async (id: string) => {
    if (!token) return;
    await deleteSavedSearchApi(token, id);
    await reload();
  };

  return (
    <div>
      <SearchBar onSearch={runSearch} />
      <button onClick={saveCurrent}>Save</button>
      <FacetPanel facets={facets} />
      <SearchResults items={result?.items} />
      {saved && (
        <SavedSearchesPanel
          searches={saved.items}
          onRun={runSaved}
          onDelete={deleteSaved}
        />
      )}
    </div>
  );
}

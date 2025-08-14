import { useEffect, useState } from 'react';
import { listSavedSearchesApi, SavedSearchList } from '../api/search';

export function useSavedSearches(token: string) {
  const [data, setData] = useState<SavedSearchList | null>(null);

  const reload = () => {
    if (!token) return Promise.resolve();
    return listSavedSearchesApi(token)
      .then((d) => setData(d))
      .catch(() => setData(null));
  };

  useEffect(() => {
    reload();
  }, [token]);

  return { data, reload };
}

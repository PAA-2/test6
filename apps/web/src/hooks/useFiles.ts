import { useEffect, useState } from 'react';
import { listFiles, FileMeta } from '../api/files';

export function useFiles(token: string, reload: number) {
  const [data, setData] = useState<FileMeta[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    listFiles(token)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [token, reload]);

  return { data, loading, error };
}

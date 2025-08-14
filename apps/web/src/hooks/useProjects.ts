import { useEffect, useState } from 'react';
import { listProjects, Project } from '../api/projects';

export function useProjects(token: string) {
  const [data, setData] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    listProjects(token)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { data, loading, error };
}

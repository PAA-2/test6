import { useEffect, useState } from 'react';
import { getJobStatus, Job } from '../api/jobs';

export function useJobStatus(token: string, id: string) {
  const [job, setJob] = useState<Job | null>(null);
  useEffect(() => {
    let active = true;
    async function poll() {
      try {
        const data = await getJobStatus(token, id);
        if (active) {
          setJob(data);
          if (data.status === 'finished' || data.status === 'failed') return;
        }
      } catch {
        /* ignore */
      }
      if (active) setTimeout(poll, 2000);
    }
    poll();
    return () => {
      active = false;
    };
  }, [token, id]);
  return job;
}

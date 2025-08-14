const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Job {
  id: string;
  type: string;
  status: string;
  started_at?: string;
  finished_at?: string;
  error_text?: string | null;
}

export interface JobListResponse {
  items: Job[];
  page: number;
  page_size: number;
  total: number;
}

export async function rebuildAnalytics(
  token: string,
  scope: 'global' | 'user' = 'global',
): Promise<{ task_id: string }> {
  const res = await fetch(`${API_URL}/tasks/analytics/rebuild?scope=${scope}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('enqueue failed');
  return res.json();
}

export async function enqueueThumbnail(
  token: string,
  fileId: string,
): Promise<{ task_id: string }> {
  const res = await fetch(`${API_URL}/tasks/files/${fileId}/thumbnail`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('enqueue failed');
  return res.json();
}

export async function getJobStatus(
  token: string,
  id: string,
): Promise<Job> {
  const res = await fetch(`${API_URL}/tasks/${id}/status`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('status failed');
  return res.json();
}

export async function listJobs(
  token: string,
  params: { type?: string; status?: string; page?: number; page_size?: number },
): Promise<JobListResponse> {
  const q = new URLSearchParams();
  if (params.type) q.set('type', params.type);
  if (params.status) q.set('status', params.status);
  if (params.page) q.set('page', String(params.page));
  if (params.page_size) q.set('page_size', String(params.page_size));
  const res = await fetch(`${API_URL}/tasks?${q.toString()}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('list failed');
  return res.json();
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface FileMimeStat {
  mime: string;
  count: number;
}

export interface SummaryResponse {
  projects_total: number;
  projects_by_status: Record<string, number>;
  files_total: number;
  files_bytes_total: number;
  files_top_mime: FileMimeStat[];
  notifications_unread: number;
}

export interface ProjectPerDay {
  date: string;
  count: number;
}

export interface TopUser {
  user_id: number;
  email: string;
  projects_count: number;
}

export async function getSummary(token: string): Promise<SummaryResponse> {
  const res = await fetch(`${API_URL}/analytics/summary`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('summary failed');
  return res.json();
}

export async function getProjectsPerDay(
  token: string,
  days = 30,
): Promise<ProjectPerDay[]> {
  const res = await fetch(`${API_URL}/analytics/projects-per-day?days=${days}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('ppd failed');
  return res.json();
}

export async function getTopUsers(
  token: string,
  limit = 5,
): Promise<TopUser[]> {
  const res = await fetch(`${API_URL}/analytics/top-users?limit=${limit}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('top users failed');
  return res.json();
}

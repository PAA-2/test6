const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Project {
  id: string;
  name: string;
  description?: string;
  status: 'draft' | 'active' | 'archived';
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export async function listProjects(token: string): Promise<Project[]> {
  const res = await fetch(`${API_URL}/projects`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to load projects');
  return res.json();
}

export async function createProject(
  token: string,
  data: { name: string; description?: string; status: 'draft' | 'active' | 'archived' }
): Promise<Project> {
  const res = await fetch(`${API_URL}/projects`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Create failed');
  return res.json();
}

export async function updateProject(
  token: string,
  id: string,
  data: Partial<{ name: string; description?: string; status: 'draft' | 'active' | 'archived' }>
): Promise<Project> {
  const res = await fetch(`${API_URL}/projects/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Update failed');
  return res.json();
}

export async function deleteProject(token: string, id: string): Promise<void> {
  const res = await fetch(`${API_URL}/projects/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Delete failed');
}

export async function getProject(token: string, id: string): Promise<Project> {
  const res = await fetch(`${API_URL}/projects/${id}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Load failed');
  return res.json();
}

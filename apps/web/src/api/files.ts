const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface FileMeta {
  id: string;
  owner_id: number;
  original_name: string;
  mime_type: string;
  size_bytes: number;
  created_at: string;
}

export async function listFiles(token: string): Promise<FileMeta[]> {
  const res = await fetch(`${API_URL}/files`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to load files');
  return res.json();
}

export async function uploadFile(token: string, file: File): Promise<FileMeta> {
  const form = new FormData();
  form.append('file', file);
  const res = await fetch(`${API_URL}/files/upload`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}

export async function deleteFileApi(token: string, id: string): Promise<void> {
  const res = await fetch(`${API_URL}/files/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Delete failed');
}

export async function downloadFile(token: string, id: string): Promise<Blob> {
  const res = await fetch(`${API_URL}/files/${id}/download`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Download failed');
  return res.blob();
}

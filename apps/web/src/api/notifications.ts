export interface Notification {
  id: string;
  type: string;
  message: string;
  data?: Record<string, unknown>;
  read: boolean;
  created_at: string;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_URL = API_URL.replace(/^http/, 'ws');

export async function listNotifications(token: string): Promise<Notification[]> {
  const res = await fetch(`${API_URL}/notifications`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed to load');
  return res.json();
}

export async function markNotificationRead(token: string, id: string) {
  const res = await fetch(`${API_URL}/notifications/${id}/read`, {
    method: 'PATCH',
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Failed');
  return res.json();
}

export async function markAllRead(token: string) {
  await fetch(`${API_URL}/notifications/read-all`, {
    method: 'PATCH',
    headers: { Authorization: `Bearer ${token}` },
  });
}

export function connectNotifications(
  token: string,
  onMessage: (n: Notification) => void,
) {
  const ws = new WebSocket(`${WS_URL}/notifications/ws?token=${token}`);
  ws.onmessage = (e) => {
    const data = JSON.parse(e.data);
    onMessage(data);
  };
  return ws;
}

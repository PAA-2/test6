import { useEffect, useState } from 'react';
import {
  listNotifications,
  connectNotifications,
  Notification,
} from '../api/notifications';

export function useNotifications(token: string) {
  const [data, setData] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    listNotifications(token)
      .then((n) => setData(n))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
    const ws = connectNotifications(token, (n) =>
      setData((prev) => [n, ...prev]),
    );
    return () => ws.close();
  }, [token]);

  const unread = data.filter((n) => !n.read).length;

  return { data, unread, loading, error, setData };
}

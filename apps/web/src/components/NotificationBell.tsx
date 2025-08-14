import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useNotifications } from '../hooks/useNotifications';

interface Props {
  token: string;
}

export default function NotificationBell({ token }: Props) {
  const { data, unread } = useNotifications(token);
  const [open, setOpen] = useState(false);
  return (
    <div>
      <button onClick={() => setOpen((o) => !o)} aria-label="notifications">
        🔔 {unread}
      </button>
      {open && (
        <div>
          <ul>
            {data.slice(0, 5).map((n) => (
              <li key={n.id}>{n.message}</li>
            ))}
            <li>
              <Link to="/notifications">All notifications</Link>
            </li>
          </ul>
        </div>
      )}
    </div>
  );
}

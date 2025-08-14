import { markAllRead } from '../api/notifications';
import { useNotifications } from '../hooks/useNotifications';

interface Props {
  token: string;
}

export default function MyNotifications({ token }: Props) {
  const { data, setData } = useNotifications(token);
  return (
    <div>
      <h1>My Notifications</h1>
      <button
        onClick={async () => {
          await markAllRead(token);
          setData(data.map((n) => ({ ...n, read: true })));
        }}
      >
        Mark all as read
      </button>
      <ul>
        {data.map((n) => (
          <li key={n.id}>{n.message}</li>
        ))}
      </ul>
    </div>
  );
}

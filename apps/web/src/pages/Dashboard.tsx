import { useEffect, useState } from 'react';
import { getMe } from '../api';

interface User {
  email: string;
  full_name?: string;
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      getMe(token).then(setUser).catch(() => setError('Failed to load'));
    }
  }, []);

  if (error) return <p>{error}</p>;
  if (!user) return <p>Loading...</p>;
  return (
    <div>
      <h1>Dashboard</h1>
      <p>{user.email}</p>
    </div>
  );
}

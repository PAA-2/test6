import { useEffect, useState } from 'react';
import { getMe } from '../api';
import {
  getSummary,
  getProjectsPerDay,
  getTopUsers,
  SummaryResponse,
  ProjectPerDay,
  TopUser,
} from '../api/analytics';
import StatsCard from '../components/StatsCard';
import LineChart from '../components/LineChart';
import BarChart from '../components/BarChart';

export default function Dashboard() {
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [perDay, setPerDay] = useState<ProjectPerDay[]>([]);
  const [topUsers, setTopUsers] = useState<TopUser[]>([]);
  const [role, setRole] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token') || '';
    if (!token) {
      setError('No token');
      return;
    }
    getMe(token)
      .then((u) => {
        setRole(u.role || '');
        if (u.role) localStorage.setItem('role', u.role);
      })
      .catch(() => setError('Failed to load user'));
    getSummary(token)
      .then(setSummary)
      .catch(() => setError('Failed to load summary'));
    getProjectsPerDay(token)
      .then(setPerDay)
      .catch(() => {});
    if (localStorage.getItem('role') === 'admin') {
      getTopUsers(token)
        .then(setTopUsers)
        .catch(() => {});
    }
  }, []);

  if (error) return <p>{error}</p>;
  if (!summary) return <p>Loading...</p>;

  return (
    <div>
      <h1>Dashboard</h1>
      <div>
        <StatsCard title="Projects" value={summary.projects_total} />
        <StatsCard title="Files" value={summary.files_total} />
        <StatsCard title="Unread Notifications" value={summary.notifications_unread} />
      </div>
      <div>
        <h2>Projects per day</h2>
        <LineChart data={perDay} />
      </div>
      <div>
        <h2>Top MIME types</h2>
        <BarChart
          data={summary.files_top_mime.map((m) => ({ label: m.mime, value: m.count }))}
        />
      </div>
      {role === 'admin' && (
        <div>
          <h2>Top users</h2>
          <ul>
            {topUsers.map((u) => (
              <li key={u.user_id}>
                {u.email}: {u.projects_count}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

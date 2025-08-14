import { useEffect, useState } from 'react';
import { listJobs, rebuildAnalytics, Job } from '../api/jobs';
import JobStatusBadge from '../components/JobStatusBadge';

export default function Jobs() {
  const token = localStorage.getItem('token') || '';
  const [jobs, setJobs] = useState<Job[]>([]);
  const [typeFilter, setType] = useState('');
  const [statusFilter, setStatus] = useState('');
  const [error, setError] = useState('');

  const load = () => {
    listJobs(token, { type: typeFilter || undefined, status: statusFilter || undefined })
      .then((r) => setJobs(r.items))
      .catch(() => setError('failed'));
  };

  useEffect(() => {
    if (token) load();
  }, []);

  const handleRebuild = async () => {
    await rebuildAnalytics(token);
    load();
  };

  if (!token) return <p>No token</p>;

  return (
    <div>
      <h1>Jobs</h1>
      <div>
        <input
          placeholder="type"
          value={typeFilter}
          onChange={(e) => setType(e.target.value)}
        />
        <input
          placeholder="status"
          value={statusFilter}
          onChange={(e) => setStatus(e.target.value)}
        />
        <button onClick={load}>Filter</button>
        <button onClick={handleRebuild}>Rebuild analytics</button>
      </div>
      {error && <p>{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((j) => (
            <tr key={j.id}>
              <td>{j.type}</td>
              <td>
                <JobStatusBadge status={j.status} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

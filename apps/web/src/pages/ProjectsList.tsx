import { useProjects } from '../hooks/useProjects';
import { ProjectTable } from '../components/ProjectTable';
import { useNavigate } from 'react-router-dom';

interface Props {
  token: string;
  role: string;
}

export default function ProjectsList({ token, role }: Props) {
  const { data, loading, error } = useProjects(token);
  const navigate = useNavigate();
  const canCreate = role === 'admin' || role === 'editor';

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error</p>;

  return (
    <div>
      <h2>Projects</h2>
      {canCreate && <button onClick={() => navigate('/projects/new')}>New Project</button>}
      <ProjectTable projects={data} />
    </div>
  );
}

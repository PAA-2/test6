import { Project } from '../api/projects';

interface Props {
  projects: Project[];
}

export function ProjectTable({ projects }: Props) {
  if (projects.length === 0) return <p>No projects</p>;
  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {projects.map((p) => (
          <tr key={p.id}>
            <td>{p.name}</td>
            <td>{p.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

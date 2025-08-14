import { useEffect, useState } from 'react';
import { getProject, Project } from '../api/projects';
import { useParams } from 'react-router-dom';

interface Props {
  token: string;
}

export default function ProjectDetails({ token }: Props) {
  const { id } = useParams();
  const [project, setProject] = useState<Project | null>(null);

  useEffect(() => {
    if (id) {
      getProject(token, id).then(setProject);
    }
  }, [id, token]);

  if (!project) return <p>Loading...</p>;
  return (
    <div>
      <h2>{project.name}</h2>
      <p>{project.description}</p>
      <p>Status: {project.status}</p>
    </div>
  );
}

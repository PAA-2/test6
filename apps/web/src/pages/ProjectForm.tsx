import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { createProject, updateProject, getProject } from '../api/projects';
import { useNavigate, useParams } from 'react-router-dom';
import { useEffect } from 'react';

const schema = z.object({
  name: z.string().min(2).max(80),
  description: z.string().max(5000).optional(),
  status: z.enum(['draft', 'active', 'archived']),
});

type FormData = z.infer<typeof schema>;

interface Props {
  token: string;
  editing?: boolean;
}

export default function ProjectForm({ token, editing }: Props) {
  const params = useParams();
  const navigate = useNavigate();
  const { register, handleSubmit, setValue, formState: { errors } } = useForm<FormData>({ resolver: zodResolver(schema) });

  useEffect(() => {
    if (editing && params.id) {
      getProject(token, params.id).then((p) => {
        setValue('name', p.name);
        setValue('description', p.description || '');
        setValue('status', p.status);
      });
    }
  }, [editing, params.id, token, setValue]);

  const onSubmit = async (data: FormData) => {
    if (editing && params.id) {
      await updateProject(token, params.id, data);
    } else {
      await createProject(token, data);
    }
    navigate('/projects');
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="name">Name</label>
        <input id="name" {...register('name')} />
        {errors.name && <span>{errors.name.message}</span>}
      </div>
      <div>
        <label htmlFor="description">Description</label>
        <textarea id="description" {...register('description')} />
        {errors.description && <span>{errors.description.message}</span>}
      </div>
      <div>
        <label htmlFor="status">Status</label>
        <select id="status" {...register('status')}>
          <option value="draft">Draft</option>
          <option value="active">Active</option>
          <option value="archived">Archived</option>
        </select>
        {errors.status && <span>{errors.status.message}</span>}
      </div>
      <button type="submit">Save</button>
    </form>
  );
}

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { register as apiRegister } from '../api';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
  full_name: z.string().optional(),
});

type FormData = z.infer<typeof schema>;

export default function Register() {
  const [error, setError] = useState('');
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: FormData) => {
    setError('');
    try {
      await apiRegister(data);
    } catch {
      setError('Register failed');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input placeholder="Email" {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      <input placeholder="Password" type="password" {...register('password')} />
      {errors.password && <span>{errors.password.message}</span>}
      <input placeholder="Full name" {...register('full_name')} />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Loading...' : 'Register'}
      </button>
      {error && <p>{error}</p>}
    </form>
  );
}

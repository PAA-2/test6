export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function login(data: { username: string; password: string }): Promise<AuthResponse> {
  const form = new URLSearchParams();
  form.append('username', data.username);
  form.append('password', data.password);
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    body: form,
  });
  if (!res.ok) throw new Error('Login failed');
  return res.json();
}

export async function register(data: {
  email: string;
  password: string;
  full_name?: string;
}): Promise<AuthResponse> {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Register failed');
  return res.json();
}

export async function getMe(token: string) {
  const res = await fetch(`${API_URL}/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Unauthorized');
  return res.json();
}

export async function updateMe(
  token: string,
  data: { full_name?: string; email_notifications?: boolean },
) {
  const res = await fetch(`${API_URL}/me`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Update failed');
  return res.json();
}

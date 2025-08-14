import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import ProjectDetails from '../ProjectDetails';

vi.mock('react-router-dom', () => ({
  useParams: () => ({ id: '1' }),
}));

vi.mock('../../api/projects', () => ({
  getProject: () => Promise.resolve({
    id: '1',
    name: 'P',
    description: 'D',
    status: 'draft',
    owner_id: 1,
    created_at: '',
    updated_at: '',
  }),
}));

describe('ProjectDetails', () => {
  it('renders project', async () => {
    render(<ProjectDetails token="t" />);
    expect(await screen.findByText('P')).toBeInTheDocument();
  });
});

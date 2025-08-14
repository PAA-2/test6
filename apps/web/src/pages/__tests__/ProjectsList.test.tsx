import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import { MemoryRouter } from 'react-router-dom';
import ProjectsList from '../ProjectsList';

vi.mock('../../hooks/useProjects', () => ({
  useProjects: () => ({ data: [], loading: false, error: null }),
}));

describe('ProjectsList', () => {
  it('renders list', () => {
    render(
      <MemoryRouter>
        <ProjectsList token="t" role="admin" />
      </MemoryRouter>
    );
    expect(screen.getByText(/Projects/)).toBeInTheDocument();
  });
});

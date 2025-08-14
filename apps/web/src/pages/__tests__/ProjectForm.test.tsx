import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom/vitest';
import ProjectForm from '../ProjectForm';

describe('ProjectForm', () => {
  it('renders inputs', () => {
    render(
      <MemoryRouter>
        <ProjectForm token="t" />
      </MemoryRouter>
    );
    expect(screen.getByLabelText(/Name/)).toBeInTheDocument();
  });
});

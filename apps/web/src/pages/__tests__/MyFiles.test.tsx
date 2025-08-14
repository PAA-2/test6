import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import MyFiles from '../MyFiles';

vi.mock('../../hooks/useFiles', () => ({
  useFiles: () => ({ data: [], loading: false, error: null }),
}));

vi.mock('../../components/UploadForm', () => ({
  default: () => <div>UploadForm</div>,
}));

describe('MyFiles', () => {
  it('renders header', () => {
    render(<MyFiles token="t" />);
    expect(screen.getByText(/My Files/)).toBeInTheDocument();
  });
});

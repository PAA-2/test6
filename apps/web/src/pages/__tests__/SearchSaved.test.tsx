import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import Search from '../Search';

vi.mock('../../api', () => ({
  getMe: vi.fn().mockResolvedValue({ email: 'a', role: 'admin' }),
}));

vi.mock('../../api/search', () => ({
  searchApi: vi
    .fn()
    .mockResolvedValue({ items: [], page: 1, page_size: 10, total: 0 }),
  getFacets: vi
    .fn()
    .mockResolvedValue({ projects_by_status: {}, files_by_mime: [] }),
  listSavedSearchesApi: vi
    .fn()
    .mockResolvedValue({ items: [], page: 1, page_size: 10, total: 0 }),
  createSavedSearchApi: vi.fn(),
  deleteSavedSearchApi: vi.fn(),
}));

import { createSavedSearchApi } from '../../api/search';

describe('Save search', () => {
  beforeEach(() => {
    localStorage.setItem('token', 't');
  });

  it('calls API on save', async () => {
    render(<Search />);
    const btn = await screen.findByText('Save');
    fireEvent.click(btn);
    expect(createSavedSearchApi).toHaveBeenCalled();
  });
});

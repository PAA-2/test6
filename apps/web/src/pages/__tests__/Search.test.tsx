import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import Search from '../Search';

vi.mock('../../api', () => ({
  getMe: vi.fn().mockResolvedValue({ email: 'a', role: 'admin' }),
}));

vi.mock('../../api/search', () => ({
  searchApi: vi.fn().mockResolvedValue({
    items: [
      {
        id: '1',
        entity: 'project',
        score: 1,
        title: 'Test',
        snippet: '<mark>Test</mark>',
        owner_id: '1',
        created_at: '2023-01-01',
        status: 'draft',
        mime: null,
      },
    ],
    page: 1,
    page_size: 10,
    total: 1,
  }),
  getFacets: vi
    .fn()
    .mockResolvedValue({ projects_by_status: { draft: 1 }, files_by_mime: [] }),
  listSavedSearchesApi: vi
    .fn()
    .mockResolvedValue({ items: [], page: 1, page_size: 10, total: 0 }),
  createSavedSearchApi: vi.fn(),
  deleteSavedSearchApi: vi.fn(),
}));

describe('Search page', () => {
  beforeEach(() => {
    localStorage.setItem('token', 't');
  });

  it('renders results with highlight', async () => {
    render(<Search />);
    const nodes = await screen.findAllByText('Test');
    expect(nodes.length).toBeGreaterThan(0);
    const mark = await screen.findByText('Test', { selector: 'mark' });
    expect(mark).toBeInTheDocument();
  });
});

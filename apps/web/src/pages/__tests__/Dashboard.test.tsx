import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import Dashboard from '../Dashboard';

vi.mock('../../api', () => ({
  getMe: vi.fn().mockResolvedValue({ email: 'a', role: 'editor' }),
}));

vi.mock('../../api/analytics', () => ({
  getSummary: vi.fn().mockResolvedValue({
    projects_total: 2,
    projects_by_status: { draft: 1, active: 1, archived: 0 },
    files_total: 3,
    files_bytes_total: 123,
    files_top_mime: [{ mime: 'pdf', count: 2 }],
    notifications_unread: 1,
  }),
  getProjectsPerDay: vi.fn().mockResolvedValue([]),
  getTopUsers: vi.fn().mockResolvedValue([
    { user_id: 1, email: 'x@example.com', projects_count: 2 },
  ]),
}));

describe('Dashboard', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('renders KPIs', async () => {
    localStorage.setItem('token', 't');
    render(<Dashboard />);
    expect(await screen.findByText('Projects')).toBeInTheDocument();
    localStorage.clear();
    expect(screen.getByText('2')).toBeInTheDocument();
  });

  it('hides top users for non-admin', async () => {
    localStorage.setItem('token', 't');
    render(<Dashboard />);
    await waitFor(() => {
      expect(screen.queryByText('Top users')).not.toBeInTheDocument();
    });
  });
});

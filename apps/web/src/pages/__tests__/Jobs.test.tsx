import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom/vitest';
import Jobs from '../Jobs';

vi.mock('../../api/jobs', () => ({
  listJobs: vi.fn().mockResolvedValue({
    items: [{ id: '1', type: 'analytics.rebuild', status: 'finished' }],
    page: 1,
    page_size: 10,
    total: 1,
  }),
  rebuildAnalytics: vi.fn().mockResolvedValue({ task_id: '1' }),
}));

describe('Jobs', () => {
  beforeEach(() => {
    localStorage.setItem('token', 't');
  });

  it('renders list and rebuild button', async () => {
    render(<Jobs />);
    expect(await screen.findByText('analytics.rebuild')).toBeInTheDocument();
    await userEvent.click(screen.getByText('Rebuild analytics'));
    const api = await import('../../api/jobs');
    expect(api.rebuildAnalytics).toHaveBeenCalled();
  });
});

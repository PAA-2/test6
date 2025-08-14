import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import '@testing-library/jest-dom/vitest';
import MyNotifications from '../MyNotifications';

vi.mock('../../hooks/useNotifications', () => ({
  useNotifications: () => ({ data: [], setData: vi.fn() }),
}));

describe('MyNotifications', () => {
  it('renders title', () => {
    render(<MyNotifications token="t" />);
    expect(screen.getByText(/My Notifications/)).toBeInTheDocument();
  });
});

import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import '@testing-library/jest-dom/vitest';
import NotificationBell from '../NotificationBell';

vi.mock('../../hooks/useNotifications', () => ({
  useNotifications: () => ({ data: [{ id: '1', message: 'Hi', read: false }], unread: 1 }),
}));

describe('NotificationBell', () => {
  it('shows unread count', () => {
    render(<NotificationBell token="t" />);
    expect(screen.getByLabelText('notifications')).toHaveTextContent('1');
  });
});

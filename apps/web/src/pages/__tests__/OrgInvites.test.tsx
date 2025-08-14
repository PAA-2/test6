import { render, screen, fireEvent } from '@testing-library/react';
import OrgInvites from '../OrgInvites';
import * as api from '../../api/orgs';
import { describe, it, vi } from 'vitest';

vi.mock('../../api/orgs');

const listOrgs = vi.mocked(api.listOrgs);
const createInvite = vi.mocked(api.createInvite);

listOrgs.mockResolvedValue([{ id: '1', name: 'A' }]);
createInvite.mockResolvedValue({ token: 'abc', email: 'x', role: 'member' });

describe('OrgInvites', () => {
  it('create invite', async () => {
    render(<OrgInvites />);
    const input = await screen.findByLabelText('email');
    fireEvent.change(input, { target: { value: 'a@b.com' } });
    fireEvent.click(screen.getByText('Invite'));
    await screen.findByText('abc');
  });
});

import { render, screen } from '@testing-library/react';
import OrgMembers from '../OrgMembers';
import * as api from '../../api/orgs';
import { describe, it, vi } from 'vitest';

vi.mock('../../api/orgs');

const listOrgs = vi.mocked(api.listOrgs);
const listMembers = vi.mocked(api.listMembers);

listOrgs.mockResolvedValue([{ id: '1', name: 'A' }]);
listMembers.mockResolvedValue([{ user_id: 1, role: 'owner' }]);

describe('OrgMembers', () => {
  it('render members', async () => {
    render(<OrgMembers />);
    await screen.findByText('1: owner');
  });
});

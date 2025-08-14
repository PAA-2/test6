import { render, screen, fireEvent } from '@testing-library/react';
import OrgSwitcher from '../OrgSwitcher';
import * as api from '../../api/orgs';
import { describe, it, expect, vi } from 'vitest';

vi.mock('../../api/orgs');

describe('OrgSwitcher', () => {
  it('switch organization', async () => {
    const listOrgs = vi.mocked(api.listOrgs);
    const setCurrentOrg = vi.mocked(api.setCurrentOrg);
    listOrgs.mockResolvedValue([
      { id: '1', name: 'A' },
      { id: '2', name: 'B' },
    ]);
    setCurrentOrg.mockResolvedValue();
    render(<OrgSwitcher />);
    const select = await screen.findByLabelText('organization');
    fireEvent.change(select, { target: { value: '2' } });
    expect(setCurrentOrg).toHaveBeenCalledWith('2');
  });
});

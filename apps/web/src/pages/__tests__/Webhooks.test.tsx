import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import { vi, test, expect } from 'vitest';
import Webhooks from '../../pages/Webhooks';
import * as dev from '../../api/devPortal';
import * as orgs from '../../api/orgs';

test('renders webhooks list', async () => {
  vi.spyOn(orgs, 'listOrgs').mockResolvedValue([]);
  vi.spyOn(dev, 'listWebhooks').mockResolvedValue([]);
  render(<Webhooks />);
  expect(await screen.findByText('Webhooks')).toBeInTheDocument();
});

import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import { vi, test, expect } from 'vitest';
import WebhookDeliveries from '../../pages/WebhookDeliveries';
import * as dev from '../../api/devPortal';
import * as orgs from '../../api/orgs';

test('renders deliveries', async () => {
  vi.spyOn(orgs, 'listOrgs').mockResolvedValue([]);
  vi.spyOn(dev, 'listDeliveries').mockResolvedValue([]);
  render(<WebhookDeliveries endpointId="1" />);
  expect(await screen.findByText('Deliveries')).toBeInTheDocument();
});

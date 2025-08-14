import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import { vi, test, expect } from 'vitest';
import ApiKeys from '../../pages/ApiKeys';
import * as dev from '../../api/devPortal';
import * as orgs from '../../api/orgs';

test('renders api keys list', async () => {
  vi.spyOn(orgs, 'listOrgs').mockResolvedValue([]);
  vi.spyOn(dev, 'listApiKeys').mockResolvedValue([]);
  render(<ApiKeys />);
  expect(await screen.findByText('API Keys')).toBeInTheDocument();
});

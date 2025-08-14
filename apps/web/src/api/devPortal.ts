import api from '../api';

export interface ApiKey {
  id: string;
  name: string;
  prefix: string;
  scopes: string[];
  active: boolean;
}

export async function createApiKey(orgId: string, name: string, scopes: string[]): Promise<{ id: string; key: string }> {
  const res = await api.post(`/orgs/${orgId}/api-keys`, { name, scopes });
  return res.data as { id: string; key: string };
}

export async function listApiKeys(orgId: string): Promise<ApiKey[]> {
  const res = await api.get(`/orgs/${orgId}/api-keys`);
  return res.data as ApiKey[];
}

export interface WebhookEndpoint {
  id: string;
  url: string;
  events: string[];
  active: boolean;
}

export async function createWebhook(orgId: string, url: string, events: string[]): Promise<{ id: string; secret: string }> {
  const res = await api.post(`/orgs/${orgId}/webhooks`, { url, events });
  return res.data as { id: string; secret: string };
}

export async function listWebhooks(orgId: string): Promise<WebhookEndpoint[]> {
  const res = await api.get(`/orgs/${orgId}/webhooks`);
  return res.data as WebhookEndpoint[];
}

export interface Delivery {
  id: string;
  event: string;
  status: string;
  response_code: number;
  attempts: number;
}

export async function listDeliveries(orgId: string, endpointId: string): Promise<Delivery[]> {
  const res = await api.get(`/orgs/${orgId}/webhooks/${endpointId}/deliveries`);
  return res.data as Delivery[];
}

export async function sendTest(orgId: string, endpointId: string): Promise<void> {
  await api.post(`/orgs/${orgId}/webhooks/${endpointId}/test`);
}

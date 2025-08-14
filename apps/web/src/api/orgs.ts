import api from '../api';

export interface Organization {
  id: string;
  name: string;
}

export interface OrgInvite {
  token: string;
  email: string;
  role: string;
}

export async function listOrgs(): Promise<Organization[]> {
  const res = await api.get<Organization[]>('/orgs');
  return res.data;
}

export async function setCurrentOrg(org_id: string): Promise<void> {
  await api.post('/me/org', { org_id });
}

export async function createInvite(org_id: string, email: string, role: string) {
  const res = await api.post<OrgInvite>(`/orgs/${org_id}/invites`, { email, role });
  return res.data;
}

export async function listMembers(org_id: string) {
  const res = await api.get<{ user_id: number; role: string }[]>(`/orgs/${org_id}/members`);
  return res.data;
}

export async function getInvite(token: string) {
  const res = await api.get<OrgInvite>(`/invites/${token}`);
  return res.data;
}

export async function acceptInvite(token: string) {
  await api.post(`/invites/${token}/accept`);
}

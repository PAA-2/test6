import { test, expect } from "@playwright/test";

test("public api with key", async ({ request }) => {
  const email = `p_${Date.now()}@example.com`;
  await request.post("/auth/register", { data: { email, password: "pw123456", full_name: "P" } });
  const login = await request.post("/auth/login", { form: { username: email, password: "pw123456" } });
  const token = (await login.json()).access_token;
  const headers = { Authorization: `Bearer ${token}` };
  const orgs = await request.get("/orgs", { headers });
  const orgId = (await orgs.json())[0].id;
  const keyResp = await request.post(`/orgs/${orgId}/api-keys`, { headers, data: { name: "k", scopes: ["projects:read"] } });
  const apiKey = (await keyResp.json()).key
  const res = await request.get("/api/v1/projects", { headers: { Authorization: `Bearer ${apiKey}` } });
  expect(res.ok()).toBeTruthy();
});

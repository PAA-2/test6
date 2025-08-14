import { test, expect } from "@playwright/test";

test("search projects", async ({ request }) => {
  const email = `s_${Date.now()}@example.com`;
  await request.post("/auth/register", { data: { email, password: "pw123456", full_name: "S" } });
  const login = await request.post("/auth/login", { form: { username: email, password: "pw123456" } });
  const token = (await login.json()).access_token;
  const headers = { Authorization: `Bearer ${token}` };
  const res = await request.get("/search", { headers, params: { q: "" } });
  expect(res.ok()).toBeTruthy();
});

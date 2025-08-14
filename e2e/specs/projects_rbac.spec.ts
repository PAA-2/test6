import { test, expect } from "@playwright/test";

test("projects CRUD", async ({ request }) => {
  const email = `edit_${Date.now()}@example.com`;
  await request.post("/auth/register", {
    data: { email, password: "pw123456", full_name: "E" },
  });
  const login = await request.post("/auth/login", {
    form: { username: email, password: "pw123456" },
  });
  const token = (await login.json()).access_token;
  const headers = { Authorization: `Bearer ${token}` };
  const created = await request.post("/projects", { headers, data: { name: "p1", description: "", status: "draft" } });
  expect(created.ok()).toBeTruthy();
});

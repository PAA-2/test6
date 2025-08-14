import { test, expect } from "@playwright/test";

test("register and login", async ({ request }) => {
  const email = `user_${Date.now()}@example.com`;
  const reg = await request.post("/auth/register", {
    data: { email, password: "pw123456", full_name: "Test" },
  });
  expect(reg.ok()).toBeTruthy();
  const login = await request.post("/auth/login", {
    form: { username: email, password: "pw123456" },
  });
  expect(login.ok()).toBeTruthy();
});

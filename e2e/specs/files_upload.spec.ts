import { test, expect } from "@playwright/test";

test("upload file", async ({ request }) => {
  const email = `file_${Date.now()}@example.com`;
  await request.post("/auth/register", { data: { email, password: "pw123456", full_name: "F" } });
  const login = await request.post("/auth/login", { form: { username: email, password: "pw123456" } });
  const token = (await login.json()).access_token;
  const headers = { Authorization: `Bearer ${token}` };
  const res = await request.post("/files/upload", {
    headers,
    multipart: {
      file: {
        name: "test.txt",
        mimeType: "text/plain",
        buffer: Buffer.from("hello"),
      },
    },
  });
  expect(res.ok()).toBeTruthy();
});

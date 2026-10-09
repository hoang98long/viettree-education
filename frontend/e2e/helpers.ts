import { expect, type Page } from "@playwright/test";

export async function login(page: Page, username: string, password: string) {
  await page.goto("/login");
  await page.getByLabel("Tên đăng nhập", { exact: true }).fill(username);
  await page.getByLabel("Mật khẩu", { exact: true }).fill(password);
  const submit = () =>
    Promise.all([
      page.waitForResponse(
        (response) =>
          response.url().endsWith("/api/v1/auth/login") &&
          response.request().method() === "POST",
      ),
      page.getByRole("button", { name: "Vào học thôi" }).click(),
    ]);
  let [response] = await submit();
  // Respect the shared proxy IP login limit, including when both browser projects run.
  if (response.status() === 429) {
    const seconds = Number(response.headers()["retry-after"] ?? 60);
    await page.waitForTimeout(Math.min(60, Math.max(1, seconds)) * 1000);
    [response] = await submit();
  }
  expect(response.status()).toBe(200);
  await expect(page).toHaveURL(/\/(student|admin)\/dashboard$/);
}

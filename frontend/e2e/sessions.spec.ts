import { test, expect } from "@playwright/test";
import { login } from "./helpers";

test("học sinh: ghi nhớ, logo trang chủ, reload, mở tab mới và đăng xuất đồng bộ", async ({
  page,
  context,
}) => {
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(
    !password,
    "Cần backend nối database test riêng và E2E_STUDENT_PASSWORD",
  );
  const response = await login(
    page,
    process.env.E2E_STUDENT_USERNAME || "longnh",
    password!,
    true,
  );
  expect(response.status()).toBe(200);
  expect(response.request().postDataJSON().remember_me).toBe(true);
  await expect(page).toHaveURL(/\/student\/dashboard$/);
  const cookie = (await context.cookies()).find(
    (item) => item.name === "viettree_session",
  )!;
  expect(cookie.httpOnly).toBe(true);
  expect(cookie.expires).toBeGreaterThan(Date.now() / 1000 + 6 * 86400);

  await page.goto("/student/history");
  await page.getByRole("link", { name: "VietTree · Về trang chủ" }).click();
  await expect(page).toHaveURL(/\/student\/dashboard$/);
  await page.goto("/");
  await expect(page.getByRole("link", { name: /^Đăng nhập/ })).toHaveCount(0);
  await page
    .getByRole("link", { name: /Vào góc học tập/ })
    .first()
    .click();
  await expect(page).toHaveURL(/\/student\/dashboard$/);
  await page.goto("/login");
  await expect(page).toHaveURL(/\/student\/dashboard$/);
  await page.reload();
  await expect(
    page.getByRole("heading", { name: "Vườn kiến thức của em" }),
  ).toBeVisible();

  const otherTab = await context.newPage();
  await otherTab.goto("/login");
  await expect(otherTab).toHaveURL(/\/student\/dashboard$/);
  await page
    .getByRole("button", { name: "Đăng xuất", exact: true })
    .last()
    .click();
  await expect(page).toHaveURL(/\/login$/);
  await expect(otherTab).toHaveURL(/\/login$/);
  await expect(otherTab.getByLabel("Mật khẩu", { exact: true })).toBeVisible();
  const oldSession = await context.request.get("/api/v1/auth/me", {
    headers: { Cookie: `viettree_session=${cookie.value}` },
  });
  expect(oldSession.status()).toBe(401);
  await otherTab.close();
});

test("admin: logo và trang đăng nhập giữ phiên, cookie bị xóa thì yêu cầu đăng nhập", async ({
  page,
  context,
}) => {
  const password = process.env.E2E_ADMIN_PASSWORD;
  test.skip(!password, "Cần E2E_ADMIN_PASSWORD và database test riêng");
  await login(page, "admin", password!);
  const cookie = (await context.cookies()).find(
    (item) => item.name === "viettree_session",
  )!;
  expect(cookie.expires).toBeLessThan(Date.now() / 1000 + 9 * 3600);
  await page.goto("/admin/questions");
  await page.getByRole("link", { name: "VietTree · Về trang chủ" }).click();
  await expect(page).toHaveURL(/\/admin\/dashboard$/);
  await page.goto("/");
  await page
    .getByRole("link", { name: /Về trang quản trị/ })
    .first()
    .click();
  await expect(page).toHaveURL(/\/admin\/dashboard$/);
  await page.goto("/login");
  await expect(page).toHaveURL(/\/admin\/dashboard$/);
  await context.clearCookies();
  await page.reload();
  await expect(page).toHaveURL(/\/login$/);
  await expect(page.getByLabel("Tên đăng nhập", { exact: true })).toBeVisible();
});

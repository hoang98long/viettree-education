import { expect, test } from "@playwright/test";
import { login } from "./helpers";

test("Admin kiểm tra hệ thống và làm mới kết quả trên desktop/mobile", async ({
  page,
}) => {
  test.skip(
    !process.env.E2E_ADMIN_PASSWORD,
    "Cần mật khẩu admin của database test",
  );
  await login(page, "admin", process.env.E2E_ADMIN_PASSWORD!);
  await page.goto("/admin/system");
  await expect(
    page.getByRole("heading", { name: "Kiểm tra hệ thống" }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Các kiểm tra dữ liệu đều đạt" }),
  ).toBeVisible();
  await expect(
    page.getByRole("cell", { name: "Migration đúng phiên bản" }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Bảo trì phiên đăng nhập" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Kiểm tra lại", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Các kiểm tra dữ liệu đều đạt" }),
  ).toBeVisible();
  const report = await page.request.get("/api/v1/admin/system-status");
  expect(report.status()).toBe(200);
  expect(report.headers()["cache-control"]).toBe("no-store");
  expect(report.headers()["x-request-id"]).toMatch(/^[a-f0-9]{32}$/);
  expect(
    (await report.json()).checks.every((check: { ok: boolean }) => check.ok),
  ).toBe(true);
});

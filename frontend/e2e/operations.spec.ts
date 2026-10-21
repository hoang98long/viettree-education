import { expect, test } from "@playwright/test";
import { login } from "./helpers";
import { readFile } from "node:fs/promises";

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
    page
      .getByRole("list", { name: "Các kiểm tra dữ liệu" })
      .getByRole("listitem")
      .filter({ hasText: "Migration đúng phiên bản" }),
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
  const release = page.getByRole("region", {
    name: "Kiểm tra trước khi mở web",
  });
  await release
    .getByRole("button", { name: "Kiểm tra trước khi mở web", exact: true })
    .click();
  const releaseResponse = await page.request.get(
    "/api/v1/admin/release-status",
  );
  expect(releaseResponse.status()).toBe(200);
  expect(releaseResponse.headers()["cache-control"]).toBe("no-store");
  const releaseReport = await releaseResponse.json();
  if ((await report.json()).environment === "production") {
    expect(releaseReport.status).toBe("ok");
  }
  await expect(
    release.getByRole("heading", {
      name:
        releaseReport.status === "ok"
          ? "Các kiểm tra trước mở web đều đạt"
          : "Còn hạng mục trước khi mở web",
      exact: true,
    }),
  ).toBeVisible();
  expect(releaseReport.curriculum).toHaveLength(15);
  expect(releaseReport.curriculum.every((row: { ok: boolean }) => row.ok)).toBe(
    true,
  );
  expect(releaseReport.academy.baseline_published).toBe(200);
  const [download] = await Promise.all([
    page.waitForEvent("download"),
    release
      .getByRole("button", { name: "Tải biên bản kiểm tra (CSV)", exact: true })
      .click(),
  ]);
  const csv = await readFile((await download.path())!, "utf8");
  expect(csv).toContain("Bài AI yêu cầu");
  expect(csv).toContain("Câu tối thiểu");
  expect(csv).not.toContain("password_hash");
  await page.screenshot({
    path: `../.tools/release-preflight-${test.info().project.name}.png`,
    fullPage: true,
  });
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
});

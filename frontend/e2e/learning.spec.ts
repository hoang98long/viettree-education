import { test, expect } from "@playwright/test";
import { login } from "./helpers";

test("cỡ chữ lưu theo tài khoản; kế hoạch và tiến độ đọc tồn tại sau reload", async ({
  page,
}, testInfo) => {
  const password = process.env.E2E_STUDENT_PASSWORD;
  const username = process.env.E2E_STUDENT_USERNAME;
  test.skip(
    !password || !username,
    "Cần học sinh test riêng và backend nối database test",
  );
  await login(page, username!, password!);
  await page.getByRole("link", { name: "Hồ sơ của em", exact: true }).click();
  await page
    .getByRole("button", { name: "Chữ vừa đủ lớn", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Chữ vừa đủ lớn", exact: true }),
  ).toHaveAttribute("aria-pressed", "true");
  await page.getByRole("button", { name: "Chữ lớn hơn", exact: true }).click();
  await expect(page.getByRole("status")).toHaveText("Đã lưu cỡ chữ cho em.");
  await page.reload();
  await expect(
    page.getByRole("button", { name: "Chữ lớn hơn", exact: true }),
  ).toHaveAttribute("aria-pressed", "true");
  await page
    .getByRole("button", { name: "Đăng xuất", exact: true })
    .first()
    .click();
  await expect(page).toHaveURL(/\/login$/);
  await login(page, username!, password!);
  await expect(page.locator(".student")).toHaveAttribute(
    "data-text-size",
    "large",
  );
  await page.getByRole("link", { name: "Kế hoạch học", exact: true }).click();
  await page.getByLabel("Môn em muốn học").selectOption("ENGLISH");
  await page
    .getByRole("button", { name: "Chuẩn bị kế hoạch", exact: true })
    .click();
  const plan = page.locator(".learning-plan").filter({
    has: page.getByRole("heading", { name: "7 ngày cùng Tiếng Anh" }),
  });
  await expect(plan).toHaveCount(1);
  await expect(plan.locator(".plan-steps li")).toHaveCount(5);
  const before = Number(await plan.locator("progress").getAttribute("value"));
  await page.screenshot({
    path: `test-results/plan-large-${testInfo.project.name}.png`,
    fullPage: true,
  });
  await plan
    .locator('li[data-completed="false"]')
    .first()
    .getByRole("link")
    .click();
  await expect(page.getByRole("heading", { name: "Em ghi nhớ" })).toBeVisible();
  await page
    .getByRole("button", { name: "Em đã đọc xong", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Đã đánh dấu đọc xong", exact: true }),
  ).toBeDisabled();
  await page.reload();
  await expect(
    page.getByRole("button", { name: "Đã đánh dấu đọc xong", exact: true }),
  ).toBeDisabled();
  await page.screenshot({
    path: `test-results/lesson-large-${testInfo.project.name}.png`,
    fullPage: true,
  });
  await page
    .getByRole("link", { name: "Xem kế hoạch học", exact: true })
    .click();
  await expect(plan.locator("progress")).toHaveAttribute(
    "value",
    String(before + 1),
  );
  await page.getByLabel("Môn em muốn học").selectOption("ENGLISH");
  await page
    .getByRole("button", { name: "Chuẩn bị kế hoạch", exact: true })
    .click();
  await expect(plan).toHaveCount(1);
  await page.reload();
  await expect(plan.locator("progress")).toHaveAttribute(
    "value",
    String(before + 1),
  );
  for (const width of [320, 768, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
  }
});

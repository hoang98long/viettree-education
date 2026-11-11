import AxeBuilder from "@axe-core/playwright";
import { expect, test, type Page } from "@playwright/test";
import { login } from "./helpers";

async function checkPage(page: Page, path: string) {
  const response = await page.goto(path);
  expect(response?.status(), path).toBe(200);
  await expect(page.getByRole("heading", { level: 1 }).first()).toBeVisible();
  await expect(page.getByRole("status", { name: "Đang tải" })).toHaveCount(0);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
    path,
  ).toBe(true);
  const result = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
    .analyze();
  expect(
    result.violations.map((item) => ({
      id: item.id,
      impact: item.impact,
      targets: item.nodes.map((node) => node.target),
    })),
    path,
  ).toEqual([]);
}

test("kiểm toán: học sinh đọc và điều hướng ở 320px/768px", async ({
  page,
}, info) => {
  const username =
    process.env[
      `E2E_EDITORIAL_GRADE4_FREE_${info.project.name.toUpperCase()}_USERNAME`
    ];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần fixture audit riêng");
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.name));
  await page.goto("/login");
  const anonymous = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa"])
    .analyze();
  expect(anonymous.violations.map((item) => item.id)).toEqual([]);
  await login(page, username!, password!);
  for (const width of [320, 768]) {
    await page.setViewportSize({ width, height: 900 });
    for (const path of [
      "/student/dashboard",
      "/student/lessons",
      "/student/profile",
      "/ai-academy",
    ])
      await checkPage(page, path);
  }
  expect(errors).toEqual([]);
});

test("kiểm toán: quản trị, dialog giữ focus và Escape trả focus", async ({
  page,
}) => {
  const password = process.env.E2E_ADMIN_PASSWORD;
  test.skip(!password, "Cần admin giả trên DB test");
  await login(page, "admin", password!);
  for (const path of [
    "/admin/dashboard",
    "/admin/accounts",
    "/admin/questions",
    "/admin/content-access",
  ])
    await checkPage(page, path);
  await page.goto("/admin/questions");
  const opener = page.getByRole("button", { name: "Xem", exact: true }).first();
  await opener.click();
  const dialog = page.getByRole("dialog", {
    name: "Nội dung câu hỏi",
    exact: true,
  });
  await expect(dialog).toBeVisible();
  const close = dialog.getByRole("button", {
    name: "Đóng chi tiết",
    exact: true,
  });
  await expect(close).toBeFocused();
  for (const key of ["Tab", "Shift+Tab", "Tab"]) {
    await page.keyboard.press(key);
    expect(
      await dialog.evaluate((element) =>
        element.contains(document.activeElement),
      ),
    ).toBe(true);
  }
  await page.keyboard.press("Escape");
  await expect(dialog).toHaveCount(0);
  await expect(opener).toBeFocused();
});

test("kiểm toán: Escape không đóng xác nhận khi đang nộp bài", async ({
  page,
}, info) => {
  const username =
    process.env[`E2E_AUDIT_SUBMIT_${info.project.name.toUpperCase()}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần fixture audit riêng");
  await login(page, username!, password!);
  const csrf = (await page.context().cookies()).find(
    (item) => item.name === "viettree_csrf",
  )!.value;
  const headers = { "X-CSRF-Token": csrf };
  const assessments = await (
    await page.request.get("/api/v1/assessments?grade=4&subject_code=MATH")
  ).json();
  const assessment = assessments.find(
    (item: { code: string }) => item.code === "VT4-MATH-numbers-practice",
  );
  const assignment = await (
    await page.request.post(
      `/api/v1/students/me/assessments/${assessment.id}/assign-self`,
      { headers },
    )
  ).json();
  const started = await page.request.post("/api/v1/attempts", {
    headers,
    data: { assignment_id: assignment.id },
  });
  expect(started.status()).toBe(200);
  const attempt = await started.json();
  await page.goto(`/student/attempts/${attempt.id}`);
  await page.getByRole("radio").first().check();
  await expect(page.locator(".save-message")).toContainText("Đã lưu");
  await page
    .getByRole("button", { name: "Xem lại trước khi nộp", exact: true })
    .click();
  await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
  const dialog = page.getByRole("dialog");
  let release!: () => void;
  const held = new Promise<void>((resolve) => {
    release = resolve;
  });
  await page.route(`**/api/v1/attempts/${attempt.id}/submit`, async (route) => {
    await held;
    await route.continue();
  });
  try {
    await dialog
      .getByRole("button", { name: "Xác nhận nộp", exact: true })
      .click();
    await expect(
      dialog.getByRole("button", { name: "Đang nộp…", exact: true }),
    ).toBeDisabled();
    await page.keyboard.press("Escape");
    await expect(dialog).toBeVisible();
    await expect(
      dialog.getByRole("button", { name: "Quay lại kiểm tra", exact: true }),
    ).toBeDisabled();
  } finally {
    release();
  }
  await expect(page).toHaveURL(new RegExp(`/student/results/${attempt.id}$`));
});

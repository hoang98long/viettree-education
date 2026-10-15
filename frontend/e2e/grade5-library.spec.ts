import { test, expect } from "@playwright/test";
import { expectedSeedQuestions, login } from "./helpers";
import { localTLS } from "./environment";

test("Lớp 5: thư viện, hình học, tiến độ, bài thập phân và cấp/thu hồi VIP", async ({
  page,
  browser,
}, info) => {
  const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  const username = process.env[`E2E_GRADE5_${suffix}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD,
    adminPassword = process.env.E2E_ADMIN_PASSWORD;
  test.skip(
    !username || !password || !adminPassword,
    "Cần fixture lớp 5 trên DB test riêng",
  );
  await login(page, username!, password!);
  const me = await (await page.request.get("/api/v1/auth/me")).json();
  await page
    .getByRole("link", { name: "Thư viện bài học", exact: true })
    .click();
  const library = await (
    await page.request.get("/api/v1/students/me/lesson-library")
  ).json();
  expect(library.summary.total).toBeGreaterThanOrEqual(68);
  await expect(
    page.getByText(`${library.summary.total} bài phù hợp`, { exact: true }),
  ).toBeVisible();
  await expect(page.locator(".library-card")).toHaveCount(12);
  await page.screenshot({
    path: `test-results/grade5-library-all-${suffix}.png`,
    fullPage: true,
  });
  await page.getByRole("button", { name: "Trang sau", exact: true }).click();
  await expect(
    page.getByText(`Trang 2/${Math.ceil(library.summary.total / 12)}`, {
      exact: true,
    }),
  ).toBeVisible();
  await page.getByLabel("Tên bài hoặc chủ đề").fill("dien tich tam giac");
  await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
  await expect(page.getByText("1 bài phù hợp", { exact: true })).toBeVisible();
  await expect(page.getByText("Trang 1/1", { exact: true })).toBeVisible();
  await page.getByRole("link", { name: "Mở bài học", exact: true }).click();
  await expect(page).toHaveURL(/\/student\/lessons\/[0-9a-f-]+$/);
  const lessonPath = new URL(page.url()).pathname;
  await expect(
    page.getByRole("img", { name: /tam giác đáy 6 cm/ }),
  ).toBeVisible();
  await page.screenshot({
    path: `test-results/grade5-triangle-${suffix}.png`,
    fullPage: true,
  });
  await expect(page.locator(".geometry-measures")).toContainText(
    "Chiều cao:4 cm",
  );
  await page
    .locator(".geometry-figure")
    .screenshot({ path: `test-results/grade5-figure-${suffix}.png` });
  await page.getByRole("button", { name: "Mở gợi ý 1", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Đã mở hết gợi ý", exact: true }),
  ).toBeDisabled();
  await page
    .getByRole("button", { name: "Em đã đọc xong", exact: true })
    .click();
  await page
    .getByRole("link", { name: "Thư viện bài học", exact: true })
    .click();
  await page.getByText("Chọn thêm bộ lọc", { exact: true }).click();
  await page.getByLabel("Tiến độ đọc").selectOption("completed");
  await expect(page.getByText("1 bài phù hợp", { exact: true })).toBeVisible();
  await expect(page.locator(".library-card-meta")).toContainText("Đã đọc xong");
  await page.getByRole("button", { name: "Xóa bộ lọc", exact: true }).click();
  await page.getByLabel("Gói bài học").selectOption("vip");
  await expect(
    page.getByText(`${library.summary.vip} bài phù hợp`, { exact: true }),
  ).toBeVisible();
  await page.screenshot({
    path: `test-results/grade5-library-${suffix}.png`,
    fullPage: true,
  });
  await page
    .getByRole("link", { name: "Xem giới thiệu", exact: true })
    .first()
    .click();
  await expect(page).toHaveURL(/\/student\/lessons\/[0-9a-f-]+$/);
  const vipPath = new URL(page.url()).pathname;
  await expect(
    page.getByRole("link", { name: "Xem gói học cùng phụ huynh" }),
  ).toBeVisible();
  expect(
    (
      await page.request.get(`/api/v1/lessons/${vipPath.split("/").at(-1)}`)
    ).status(),
  ).toBe(403);
  const adminContext = await browser.newContext({
    baseURL: process.env.E2E_BASE_URL,
    ignoreHTTPSErrors: localTLS,
  });
  try {
    const admin = await adminContext.newPage();
    await login(admin, "admin", adminPassword!);
    await admin.goto("/admin/curriculum");
    await admin
      .getByRole("combobox", { name: "Lớp học liệu", exact: true })
      .selectOption("5");
    await expect(
      admin.getByRole("heading", {
        name: "Theo dõi học liệu lớp 5",
        exact: true,
      }),
    ).toBeVisible();
    const mapping = await (
      await admin.request.get("/api/v1/admin/curriculum-map?grade=5")
    ).json();
    expect(mapping.rows).toHaveLength(22);
    expect(
      mapping.rows.reduce(
        (n: number, r: { questions: number }) => n + r.questions,
        0,
      ),
    ).toBe(expectedSeedQuestions(mapping));
    const downloadEvent = admin.waitForEvent("download");
    await admin
      .getByRole("button", { name: "Xuất học liệu CSV", exact: true })
      .click();
    expect((await downloadEvent).suggestedFilename()).toBe(
      "viettree-hoc-lieu-lop-5.csv",
    );
    const token = (await adminContext.cookies()).find(
      (c) => c.name === "viettree_csrf",
    )!.value;
    const change = async (operation: "grant" | "revoke") => {
      const response = await admin.request.post(
        `/api/v1/admin/students/${me.id}/membership/${operation}`,
        {
          headers: {
            "X-CSRF-Token": token,
            "Idempotency-Key": crypto.randomUUID(),
          },
          data: {
            ...(operation === "grant" ? { duration_days: 30 } : {}),
            reason: "Kiểm thử học liệu lớp 5",
          },
        },
      );
      expect(response.status()).toBe(200);
    };
    await change("grant");
    await page.goto(lessonPath);
    for (let i = 1; i <= 3; i++)
      await page
        .getByRole("button", { name: `Mở gợi ý ${i}`, exact: true })
        .click();
    await page.goto("/student/lessons");
    await page.getByLabel("Tên bài hoặc chủ đề").fill("Tư duy: so sánh nhóm");
    await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
    await expect(
      page.getByText("1 bài phù hợp", { exact: true }),
    ).toBeVisible();
    await page.getByRole("link", { name: "Mở bài học", exact: true }).click();
    await expect(
      page.getByRole("img", { name: /Cùng một tổng/ }),
    ).toBeVisible();
    await expect(page.locator(".pie-legend")).toContainText("Đọc sách: 50%");
    await page.screenshot({
      path: `test-results/grade5-pie-${suffix}.png`,
      fullPage: true,
    });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    await change("revoke");
    await page.reload();
    await expect(
      page.getByRole("link", { name: "Xem gói học cùng phụ huynh" }),
    ).toBeVisible();
    await page.goto("/student/lessons");
    await page.getByText("Chọn thêm bộ lọc", { exact: true }).click();
    await page.getByLabel("Gói bài học").selectOption("vip");
    await expect(
      page.getByRole("link", { name: "Xem giới thiệu", exact: true }),
    ).toHaveCount(12);
    const assessments = await (
      await page.request.get("/api/v1/assessments?grade=5&subject_code=MATH")
    ).json();
    const assessment = assessments.find(
      (a: { code: string }) => a.code === "VT5-MATH-decimals-practice",
    );
    await page.goto(`/student/assessments/${assessment.id}`);
    await page
      .getByRole("button", { name: "Bắt đầu / Tiếp tục", exact: true })
      .click();
    await expect(page).toHaveURL(/\/student\/attempts\//);
    await page.getByRole("radio", { name: /0,1/ }).check();
    await page.getByRole("button", { name: "Câu tiếp", exact: true }).click();
    await page.getByRole("textbox").fill("0,2");
    await page.getByRole("button", { name: "Lưu bài", exact: true }).click();
    await page.reload();
    await page
      .getByRole("button", { name: "Câu 2, đã trả lời", exact: true })
      .click();
    await expect(page.getByRole("textbox")).toHaveValue("0,2");
    await page
      .getByRole("button", { name: "Xem lại trước khi nộp", exact: true })
      .click();
    await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
    await page
      .getByRole("button", { name: "Xác nhận nộp", exact: true })
      .click();
    await expect(page).toHaveURL(/\/student\/results\//);
    await expect(
      page.getByRole("heading", { name: "Em đã hoàn thành bài luyện tập" }),
    ).toBeVisible();
    await admin.goto("/admin/lessons/new");
    await admin.getByLabel("Chọn minh họa").selectOption("pie");
    await expect(admin.getByText(/Tổng hiện tại: 100%/)).toBeVisible();
    await admin.getByLabel("Giá trị phần 1 (%)").fill("40");
    await expect(admin.getByText(/Tổng hiện tại: 90%/)).toBeVisible();
    await admin.getByLabel("Chọn minh họa").selectOption("trapezoid");
    await admin.getByLabel("Đáy thứ nhất (cm)").fill("7.5");
    await expect(admin.getByLabel("Đáy thứ nhất (cm)")).toHaveValue("7.5");
  } finally {
    await adminContext.close();
  }
});

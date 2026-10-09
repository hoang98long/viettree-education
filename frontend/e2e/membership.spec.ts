import { test, expect } from "@playwright/test";
import { login } from "./helpers";

test("Free → admin cấp/gia hạn VIP → học nâng cao → thu hồi, giữ kết quả", async ({
  page,
  browser,
}, testInfo) => {
  const username =
    testInfo.project.name === "mobile"
      ? process.env.E2E_VIP_MOBILE_STUDENT_USERNAME
      : process.env.E2E_VIP_STUDENT_USERNAME;
  const password = process.env.E2E_STUDENT_PASSWORD;
  const adminPassword = process.env.E2E_ADMIN_PASSWORD;
  test.skip(
    !username || !password || !adminPassword,
    "Cần tài khoản và backend database test riêng",
  );
  await login(page, username!, password!);
  const me = await (await page.request.get("/api/v1/auth/me")).json();
  const lessons = await (
    await page.request.get("/api/v1/topics?grade=4&subject_code=MATH")
  ).json();
  let vipLesson: { id: string; title: string } | undefined;
  for (const topic of lessons) {
    const items = await (
      await page.request.get(`/api/v1/lessons?topic_id=${topic.id}`)
    ).json();
    vipLesson = items.find(
      (item: { minimum_plan_code: string }) => item.minimum_plan_code === "vip",
    );
    if (vipLesson) break;
  }
  expect(vipLesson).toBeTruthy();
  await page.goto(`/student/lessons/${vipLesson!.id}`);
  await expect(
    page.getByRole("heading", { name: "Cùng khám phá thêm với VIP" }),
  ).toBeVisible();
  await expect(page.getByRole("heading", { name: "Em ghi nhớ" })).toHaveCount(
    0,
  );
  await expect(
    page.getByRole("heading", { name: "Em sẽ khám phá" }),
  ).toBeVisible();
  const adminContext = await browser.newContext({
    baseURL: testInfo.project.use.baseURL,
  });
  const admin = await adminContext.newPage();
  try {
    await login(admin, "admin", adminPassword!);
    await admin.goto(`/admin/students/${me.id}/membership`);
    await admin.getByLabel("Thao tác").selectOption("grant");
    await admin
      .getByLabel("Lý do", { exact: true })
      .fill("Cấp VIP để kiểm tra trình duyệt");
    await admin.getByRole("checkbox").check();
    await admin
      .getByRole("button", { name: "Xác nhận cập nhật gói", exact: true })
      .click();
    await expect(
      admin.getByRole("heading", { name: "VIP đang hoạt động" }),
    ).toBeVisible();
    await admin.getByLabel("Thao tác").selectOption("extend");
    await admin
      .getByLabel("Lý do", { exact: true })
      .fill("Gia hạn VIP để kiểm tra trình duyệt");
    await admin.getByRole("checkbox").check();
    await admin
      .getByRole("button", { name: "Xác nhận cập nhật gói", exact: true })
      .click();
    await expect(admin.locator('p[role="status"]')).toContainText(
      "Đã cập nhật gói học",
    );
    await page.reload();
    await expect(
      page.getByRole("heading", { name: "Em ghi nhớ" }),
    ).toBeVisible();
    await page
      .getByRole("link", { name: /^Thử thách:/ })
      .first()
      .click();
    await page.getByRole("button", { name: "Bắt đầu / Tiếp tục" }).click();
    await expect(page).toHaveURL(/\/student\/attempts\//);
    await page.getByRole("radio").first().check();
    await page.getByRole("button", { name: "Lưu bài", exact: true }).click();
    await expect(page.getByRole("status")).toContainText("Đã lưu");
    await page.getByRole("button", { name: "Xem lại trước khi nộp" }).click();
    await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
    await page
      .getByRole("button", { name: "Xác nhận nộp", exact: true })
      .click();
    await expect(page).toHaveURL(/\/student\/results\//);
    const resultUrl = page.url();
    await page.goto("/student/learning-plan");
    await page.getByLabel("Môn em muốn học").selectOption("VIETNAMESE");
    await page.getByLabel("Kiểu kế hoạch").selectOption("adaptive");
    await page
      .getByRole("button", { name: "Chuẩn bị kế hoạch", exact: true })
      .click();
    await expect(
      page.locator(".learning-plan").getByText(/Kế hoạch VIP/),
    ).toBeVisible();
    await page.screenshot({
      path: `test-results/vip-plan-${testInfo.project.name}.png`,
      fullPage: true,
    });
    await admin.getByLabel("Thao tác").selectOption("revoke");
    await admin
      .getByLabel("Lý do", { exact: true })
      .fill("Kết thúc kiểm tra, thu hồi VIP");
    await admin.getByRole("checkbox").check();
    await admin
      .getByRole("button", { name: "Xác nhận cập nhật gói", exact: true })
      .click();
    await expect(
      admin.getByRole("heading", { name: "Đang dùng gói miễn phí" }),
    ).toBeVisible();
    await page.reload();
    await expect(page.getByText("Tạm dừng", { exact: true })).toBeVisible();
    await page.goto(resultUrl);
    await expect(
      page.getByRole("heading", { name: "Em đã hoàn thành bài luyện tập" }),
    ).toBeVisible();
    await page.goto(`/student/lessons/${vipLesson!.id}`);
    await expect(
      page.getByRole("heading", { name: "Cùng khám phá thêm với VIP" }),
    ).toBeVisible();
    await page.screenshot({
      path: `test-results/vip-locked-${testInfo.project.name}.png`,
      fullPage: true,
    });
    for (const width of [320, 768, 1280]) {
      await page.setViewportSize({ width, height: 900 });
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
      ).toBe(true);
    }
    await admin.goto("/admin/content-access");
    await admin.getByLabel("Lọc gói").selectOption("vip");
    await expect(
      admin.getByRole("button", { name: "Cấu hình quyền" }),
    ).toHaveCount(24);
  } finally {
    await adminContext.close();
  }
});

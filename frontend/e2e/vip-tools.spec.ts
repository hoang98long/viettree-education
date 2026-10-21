import { expect, test } from "@playwright/test";
import { login } from "./helpers";
import { localTLS } from "./environment";

test("VIP: thư viện mới → ôn lỗi không đổi điểm → báo cáo/in → thu hồi giữ kết quả", async ({
  page,
  browser,
}, info) => {
  const username =
    info.project.name === "mobile"
      ? process.env.E2E_VIP_TOOLS_MOBILE_USERNAME
      : process.env.E2E_VIP_TOOLS_USERNAME;
  const password = process.env.E2E_STUDENT_PASSWORD;
  const adminPassword = process.env.E2E_ADMIN_PASSWORD;
  test.skip(
    !username || !password || !adminPassword,
    "Cần tài khoản mới trong database test riêng",
  );
  await login(page, username!, password!);
  const me = await (await page.request.get("/api/v1/auth/me")).json();
  await page.goto("/student/vip");
  await expect(
    page.getByRole("heading", { name: "Cùng khám phá thêm với VIP" }),
  ).toBeVisible();
  expect(
    (await page.request.get("/api/v1/students/me/vip/library")).status(),
  ).toBe(403);
  const adminContext = await browser.newContext({
    ignoreHTTPSErrors: localTLS,
    baseURL: info.project.use.baseURL,
  });
  const admin = await adminContext.newPage();
  try {
    await login(admin, "admin", adminPassword!);
    expect(
      (await admin.request.get("/api/v1/students/me/vip/library")).status(),
    ).toBe(403);
    const csrf = (await adminContext.cookies()).find(
      (cookie) => cookie.name === "viettree_csrf",
    )!.value;
    const headers = {
      "X-CSRF-Token": csrf,
      "Idempotency-Key": crypto.randomUUID(),
    };
    const granted = await admin.request.post(
      `/api/v1/admin/students/${me.id}/membership/grant`,
      {
        headers,
        data: { duration_days: 30, reason: "Kiểm thử công cụ VIP lớp 4" },
      },
    );
    expect(granted.status()).toBe(200);
    await page.reload();
    await expect(
      page.getByRole("heading", { name: "Sổ tay ôn lỗi" }),
    ).toBeVisible();
    await page
      .getByRole("combobox", { name: "Môn học", exact: true })
      .selectOption("MATH");
    const lesson = page.locator("article").filter({
      has: page.getByRole("heading", {
        name: "Phân số trong một buổi làm bánh",
      }),
    });
    await lesson.getByRole("link", { name: "Mở bài học" }).click();
    await expect(
      page.getByRole("heading", { name: "Em ghi nhớ" }),
    ).toBeVisible();
    await page
      .getByRole("link", { name: /Thử thách: Phân số trong một buổi làm bánh/ })
      .click();
    await page.getByRole("button", { name: "Bắt đầu / Tiếp tục" }).click();
    await page.getByRole("button", { name: "Xem lại trước khi nộp" }).click();
    await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
    await page
      .getByRole("button", { name: "Xác nhận nộp", exact: true })
      .click();
    await expect(page).toHaveURL(/\/student\/results\//);
    const resultUrl = page.url();
    const attemptId = resultUrl.split("/").at(-1)!;
    const before = await (
      await page.request.get(`/api/v1/attempts/${attemptId}/result`)
    ).json();
    await page.goto("/student/vip/mistakes");
    await expect(page.locator(".vip-mistake")).toHaveCount(8);
    const card = page.locator(".vip-mistake:has(input[type=radio])").first();
    await card.getByRole("radio").first().check();
    await card.getByRole("button", { name: "Kiểm tra câu tự ôn" }).click();
    await expect(card.getByRole("status")).toContainText("Em đã trả lời đúng!");
    const after = await (
      await page.request.get(`/api/v1/attempts/${attemptId}/result`)
    ).json();
    expect(after.total_score).toBe(before.total_score);
    await page.goto("/student/vip/report");
    await expect(
      page.getByRole("heading", { name: "Nhịp luyện tập từng ngày" }),
    ).toBeVisible();
    await expect(page.locator(".vip-daily [role=listitem]")).toHaveCount(7);
    await page
      .getByRole("combobox", { name: "Khoảng thời gian", exact: true })
      .selectOption("30");
    await expect(page.locator(".vip-daily [role=listitem]")).toHaveCount(30);
    await page.evaluate(() => {
      window.print = () => {
        document.body.dataset.printChecked = "yes";
      };
    });
    await page.getByRole("button", { name: "In / lưu PDF" }).click();
    await expect(page.locator("body")).toHaveAttribute(
      "data-print-checked",
      "yes",
    );
    await page.emulateMedia({ media: "print" });
    await expect(page.locator(".sidebar")).toBeHidden();
    await expect(page.locator(".vip-report-print")).toBeVisible();
    await page.emulateMedia({ media: "screen" });
    await page.screenshot({
      path: `test-results/vip-report-${info.project.name}.png`,
      fullPage: true,
    });
    const revoked = await admin.request.post(
      `/api/v1/admin/students/${me.id}/membership/revoke`,
      {
        headers: { ...headers, "Idempotency-Key": crypto.randomUUID() },
        data: { reason: "Kiểm thử thu hồi quyền công cụ VIP" },
      },
    );
    expect(revoked.status()).toBe(200);
    await page.reload();
    await expect(
      page.getByRole("heading", { name: "Cùng khám phá thêm với VIP" }),
    ).toBeVisible();
    expect(
      (
        await page.request.get("/api/v1/students/me/vip/report?days=30")
      ).status(),
    ).toBe(403);
    await page.goto(resultUrl);
    await expect(
      page.getByRole("heading", { name: "Em đã hoàn thành bài luyện tập" }),
    ).toBeVisible();
  } finally {
    await adminContext.close();
  }
});

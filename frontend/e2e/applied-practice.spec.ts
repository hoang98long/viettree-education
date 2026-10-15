import { test, expect } from "@playwright/test";
import { login } from "./helpers";

test("Lớp 1 Free: bài mới, gợi ý, làm bài và lọc phần cần ôn", async ({
  page,
}, info) => {
  const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  const username = process.env[`E2E_REVIEW_GRADE1_FREE_${suffix}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(
    !username || !password,
    "Cần database test và bộ tình huống bổ sung",
  );
  await login(page, username!, password!);
  await page.goto("/student/practice");
  await expect(
    page.getByRole("heading", { name: "Thư viện luyện tập của em" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Bài ngắn", exact: true }).click();
  await page.getByText("Chọn thêm bộ lọc", { exact: true }).click();
  await page.getByLabel("Độ dài bài").selectOption("4");
  await page.getByLabel("Tên bài hoặc chủ đề").fill("gio qua cua em");
  await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
  await expect(
    page.getByText("1 bài luyện phù hợp", { exact: true }),
  ).toBeVisible();
  await page.getByRole("link", { name: "Xem bài học và gợi ý" }).click();
  await expect(page.getByRole("img", { name: /Sáu chấm tròn/ })).toBeVisible();
  await page.getByRole("button", { name: "Mở gợi ý 1", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Đã mở hết gợi ý", exact: true }),
  ).toBeDisabled();
  await page.goto("/student/practice");
  await page.getByLabel("Tên bài hoặc chủ đề").fill("gio qua cua em");
  await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
  await page
    .locator(".library-card")
    .getByRole("link", { name: /Mở bài luyện tập|Luyện lại/ })
    .click();
  await page.getByRole("button", { name: "Bắt đầu / Tiếp tục" }).click();
  // Leave all four unanswered: review status must come from this real submission.
  await page.getByRole("button", { name: "Xem lại trước khi nộp" }).click();
  await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
  await page.getByRole("button", { name: "Xác nhận nộp", exact: true }).click();
  await expect(page).toHaveURL(/\/student\/results\//);
  await page.goto("/student/practice");
  await page.getByRole("button", { name: "Ôn thêm", exact: true }).click();
  await page.getByLabel("Tên bài hoặc chủ đề").fill("gio qua cua em");
  await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
  await expect(page.locator(".library-card")).toHaveCount(1);
  await expect(page.locator(".library-card")).toContainText("Gần nhất: 0%");
  await page.screenshot({
    path: `test-results/applied-free-review-${suffix}.png`,
    fullPage: true,
  });
  for (const width of [320, 390, 768, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
  }
});

test("Lớp 5 VIP: đọc biểu đồ, mở đủ gợi ý và lọc thử thách ngắn", async ({
  page,
}, info) => {
  const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  const username = process.env[`E2E_REVIEW_GRADE5_VIP_${suffix}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần học sinh VIP test riêng");
  await login(page, username!, password!);
  await page.goto("/student/practice");
  await page.getByText("Chọn thêm bộ lọc", { exact: true }).click();
  await page.getByLabel("Gói bài luyện").selectOption("vip");
  await page.getByLabel("Loại bài luyện").selectOption("quiz");
  await page.getByLabel("Độ dài bài").selectOption("6");
  await page.getByLabel("Tên bài hoặc chủ đề").fill("gian sach giam gia");
  await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
  await expect(
    page.getByText("1 bài luyện phù hợp", { exact: true }),
  ).toBeVisible();
  await page.getByRole("link", { name: "Xem bài học và gợi ý" }).click();
  await expect(
    page.getByRole("img", { name: /Giảm 20% giá gốc/ }),
  ).toBeVisible();
  for (const hint of [1, 2, 3])
    await page
      .getByRole("button", { name: `Mở gợi ý ${hint}`, exact: true })
      .click();
  await expect(
    page.getByRole("button", { name: "Đã mở hết gợi ý", exact: true }),
  ).toBeDisabled();
  await page.screenshot({
    path: `test-results/applied-vip-hints-${suffix}.png`,
    fullPage: true,
  });
});

test("Admin: kiểm kê học liệu tình huống đủ cả năm khối", async ({ page }) => {
  const password = process.env.E2E_ADMIN_PASSWORD;
  test.skip(!password, "Cần admin trên database test riêng");
  await login(page, "admin", password!);
  await page.goto("/admin/curriculum");
  for (const grade of [1, 2, 3, 4, 5]) {
    await page.getByLabel("Lớp học liệu").selectOption(String(grade));
    await expect(page.getByLabel("Học liệu tình huống bổ sung")).toContainText(
      "6/6 bài · 30/30 câu hỏi · 6/6 đề",
    );
    await expect(page.getByLabel("Học liệu tình huống bổ sung")).toContainText(
      `Lớp ${grade}`,
    );
  }
});

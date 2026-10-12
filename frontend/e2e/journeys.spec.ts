import { test, expect } from "@playwright/test";
import { login } from "./helpers";

test("học sinh: bài học → làm bài → lưu/reload → nộp → kết quả → lịch sử", async ({
  page,
}, testInfo) => {
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(
    !password,
    "Cần E2E_STUDENT_PASSWORD, backend dùng database test riêng",
  );
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: /Mỗi điều em học/ }),
  ).toBeVisible();
  await login(page, process.env.E2E_STUDENT_USERNAME || "longnh", password!);
  await expect(
    page.getByRole("heading", { name: "Vườn kiến thức của em" }),
  ).toBeVisible();
  await page.screenshot({
    path: `test-results/dashboard-${testInfo.project.name}.png`,
    fullPage: true,
  });
  await page.getByRole("link", { name: /Toán.*chủ đề/ }).click();
  await page.getByRole("link", { name: /Hàng, lớp và cách đọc số/ }).click();
  await expect(page.getByRole("heading", { name: "Em ghi nhớ" })).toBeVisible();
  await page.getByRole("link", { name: /Luyện tập: Số tự nhiên/ }).click();
  await page.getByRole("button", { name: "Bắt đầu / Tiếp tục" }).click();
  await expect(page).toHaveURL(/\/student\/attempts\//);
  await page.getByRole("radio", { name: /70 000/ }).check();
  await page.getByRole("button", { name: "Lưu bài", exact: true }).click();
  await expect(page.getByRole("status")).toContainText("Đã lưu");
  await page.reload();
  await expect(page.getByRole("radio", { name: /70 000/ })).toBeChecked();
  await page.getByRole("button", { name: "Xem lại trước khi nộp" }).click();
  await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
  await page.getByRole("button", { name: "Xác nhận nộp", exact: true }).click();
  await expect(page).toHaveURL(/\/student\/results\//);
  await expect(
    page.getByRole("heading", { name: "Em đã hoàn thành bài luyện tập" }),
  ).toBeVisible();
  await page.reload();
  await page.locator("details summary").first().click();
  await expect(page.getByText("Em trả lời:").first()).toBeVisible();
  await page
    .getByRole("link", { name: "Lịch sử luyện tập", exact: true })
    .click();
  await expect(
    page.getByRole("link", { name: /Luyện tập: Số tự nhiên/ }).first(),
  ).toBeVisible();
  await page.getByRole("link", { name: "Cây năng lực", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Cây năng lực của em" }),
  ).toBeVisible();
  await page.goto("/student/grades");
  await page.getByRole("button", { name: /Lớp 5/ }).click();
  await expect(
    page.getByText("Chương trình lớp 5 đang xây dựng"),
  ).toBeVisible();
  await page.goto("/admin/dashboard");
  await expect(page.getByRole("heading", { name: /403/ })).toBeVisible();
});

test("admin: thống kê, danh sách, đáp án chỉ quản trị và trình soạn câu hỏi", async ({
  page,
}, testInfo) => {
  const password = process.env.E2E_ADMIN_PASSWORD;
  test.skip(!password, "Cần E2E_ADMIN_PASSWORD");
  await login(page, "admin", password!);
  await expect(
    page.getByText("Câu hỏi đã xuất bản", { exact: true }),
  ).toBeVisible();
  await page.goto("/admin/students");
  await page.getByLabel("Tìm theo tên").fill("Long");
  await expect(
    page.getByRole("cell", { name: "longnh", exact: true }),
  ).toBeVisible();
  await page.goto("/admin/questions");
  await page.getByRole("button", { name: "Xem", exact: true }).first().click();
  await expect(
    page.getByRole("heading", { name: /Đáp án · Chỉ quản trị viên/ }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Đóng chi tiết" }).click();
  await page.goto("/admin/questions/new");
  await expect(page.getByLabel("Mã câu hỏi")).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Lưu nháp câu hỏi" }),
  ).toBeEnabled();
  await expect(
    page.getByRole("button", { name: "Xem trước câu hỏi" }),
  ).toBeEnabled();
  await page.screenshot({
    path: `test-results/authoring-${testInfo.project.name}.png`,
    fullPage: true,
  });
  for (const path of ["curriculum", "assessments", "analytics", "settings"]) {
    await page.goto(`/admin/${path}`);
    await expect(page.locator("main h1")).toBeVisible();
    await expect(page.getByText("Chưa tải được dữ liệu")).toHaveCount(0);
  }
  await page
    .getByRole("button", { name: "Đăng xuất", exact: true })
    .first()
    .click();
  await expect(page).toHaveURL(/\/login$/);
});

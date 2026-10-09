import { test, expect, type Page } from "@playwright/test";
import { login } from "./helpers";

async function publish(page: Page) {
  await page
    .getByLabel("Lý do duyệt / xuất bản / lưu trữ")
    .fill("Kiểm tra nội dung và đáp án trước khi xuất bản");
  await page
    .getByRole("button", { name: "Duyệt nội dung", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Xuất bản", exact: true }),
  ).toBeEnabled();
  await page.getByRole("button", { name: "Xuất bản", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Xuất bản", exact: true }),
  ).toHaveCount(0);
}

test("admin tạo câu, ghép đề và giao bài; học sinh tìm, làm và xem kết quả", async ({
  page,
}, testInfo) => {
  const adminPassword = process.env.E2E_ADMIN_PASSWORD;
  const studentPassword = process.env.E2E_STUDENT_PASSWORD;
  const student = process.env.E2E_AUTHORING_STUDENT_USERNAME;
  test.skip(
    !adminPassword || !studentPassword || !student,
    "Cần tài khoản trong database test riêng",
  );
  const code = `E2E-${testInfo.project.name}-${Date.now()}`;
  const title = `Bài luyện mới ${code}`;
  await login(page, "admin", adminPassword!);
  await page.goto("/admin/questions/new");
  await page.getByLabel("Mã câu hỏi", { exact: true }).fill(code);
  await page
    .getByRole("combobox", { name: "Môn học", exact: true })
    .selectOption({ label: "Toán" });
  await page
    .getByLabel("Nội dung câu hỏi", { exact: true })
    .fill("Tính tổng 125 và 375, em được số nào?");
  await page.getByLabel("Các lựa chọn", { exact: false }).fill("500\n400\n600");
  await page.getByRole("radio", { name: "A. 500", exact: true }).check();
  await page
    .getByLabel("Lời giải", { exact: true })
    .fill("125 + 375 = 500. Em cộng theo từng hàng.");
  await page.getByRole("button", { name: "Xem trước câu hỏi" }).click();
  await expect(
    page.locator(".author-preview").getByRole("radio", { name: /500/ }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Lưu nháp câu hỏi" }).click();
  await expect(page).toHaveURL(/\/admin\/questions\/[^/]+\/edit$/);
  await publish(page);
  await expect(
    page.getByRole("textbox", { name: "Nội dung câu hỏi", exact: true }),
  ).toBeDisabled();
  await page.goto("/admin/assessments/new");
  await page.getByLabel("Mã bài tập", { exact: true }).fill(`${code}-EX`);
  await page
    .getByRole("combobox", { name: "Môn học", exact: true })
    .selectOption({ label: "Toán" });
  await page.getByLabel("Tên bài tập", { exact: true }).fill(title);
  await page.getByLabel("Tìm câu để thêm").fill(code);
  await expect(page.locator(".question-picker .list-row")).toHaveCount(1);
  await page.getByRole("button", { name: "Thêm câu", exact: true }).click();
  await page.getByLabel("Điểm câu 1", { exact: true }).fill("2");
  await page
    .getByRole("button", { name: "Lưu nháp bài tập", exact: true })
    .click();
  await expect(page).toHaveURL(/\/admin\/assessments\/[^/]+\/edit$/);
  await publish(page);
  await page.getByLabel("Tìm học sinh để giao").fill(student!);
  await expect(
    page.getByRole("checkbox", { name: new RegExp(student!) }),
  ).toBeVisible();
  await page.getByRole("checkbox", { name: new RegExp(student!) }).check();
  await page
    .getByRole("button", { name: "Xác nhận giao bài", exact: true })
    .click();
  await expect(page.getByRole("status")).toContainText("1 học sinh");
  await page.screenshot({
    path: `test-results/exercise-authoring-${testInfo.project.name}.png`,
    fullPage: true,
  });
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await page
    .getByRole("button", { name: "Đăng xuất", exact: true })
    .first()
    .click();
  await login(page, student!, studentPassword!);
  await page.goto("/student/practice");
  await page.getByLabel("Gói bài luyện").selectOption("free");
  await page.getByLabel("Tìm bài luyện tập").fill(code);
  await expect(
    page.getByRole("link", { name: new RegExp(title) }),
  ).toBeVisible();
  await page.goto("/student/dashboard");
  const assignedLink = page
    .locator('a[href*="assignment_id="]')
    .filter({ hasText: title });
  await expect(assignedLink).toBeVisible();
  const assignmentId = new URL(
    (await assignedLink.getAttribute("href")) ?? "",
    page.url(),
  ).searchParams.get("assignment_id");
  await assignedLink.click();
  await page.getByRole("button", { name: "Bắt đầu / Tiếp tục" }).click();
  await expect(page).toHaveURL(/\/student\/attempts\//);
  const attemptId = page.url().split("/").at(-1);
  const attempt = await (
    await page.request.get(`/api/v1/attempts/${attemptId}`)
  ).json();
  expect(attempt.assignment_id).toBe(assignmentId);
  await page.getByRole("radio", { name: /500/ }).check();
  await page.getByRole("button", { name: "Xem lại trước khi nộp" }).click();
  await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
  await page.getByRole("button", { name: "Xác nhận nộp", exact: true }).click();
  await expect(page).toHaveURL(/\/student\/results\//);
  await expect(
    page.getByRole("heading", { name: "Em đã hoàn thành bài luyện tập" }),
  ).toBeVisible();
  await expect(page.locator(".score-circle")).toContainText("2");
  const tasks = await (
    await page.request.get("/api/v1/students/me/assignments")
  ).json();
  expect(
    tasks.find((item: { id: string }) => item.id === assignmentId).status,
  ).toBe("completed");
});

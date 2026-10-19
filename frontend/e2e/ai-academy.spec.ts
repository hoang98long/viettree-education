import { expect, test, type Page } from "@playwright/test";
import { login } from "./helpers";

async function staffLogin(page: Page, username: string, password: string) {
  await page.goto("/login");
  await page.getByLabel("Tên đăng nhập", { exact: true }).fill(username);
  await page.getByLabel("Mật khẩu", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Vào học thôi" }).click();
  await expect(page).toHaveURL(/\/(teacher|guardian)\/dashboard$/);
}

test("AI Academy: học/chấm/resume, lab, an toàn, sản phẩm và huy hiệu", async ({
  page,
}, info) => {
  const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  const username = process.env["E2E_ACADEMY_" + suffix + "_USERNAME"];
  test.skip(
    !username || !process.env.E2E_STUDENT_PASSWORD,
    "Cần fixture AI trong database test riêng",
  );
  await login(page, username!, process.env.E2E_STUDENT_PASSWORD!);
  await page.getByRole("link", { name: "AI Academy", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Khám phá AI, sáng tạo an toàn" }),
  ).toBeVisible();
  const catalog = await (
    await page.request.get("/api/v1/ai-academy/catalog?grade=4")
  ).json();
  expect(catalog).toHaveLength(40);
  const lesson = catalog.find((l: { code: string }) => l.code === "AI4-01");
  await page.goto("/ai-academy/lessons/" + lesson.id);
  await expect(
    page.getByRole("heading", {
      name: "AI là gì và AI không phải là gì?",
      exact: true,
    }),
  ).toBeVisible();
  await page.screenshot({
    path: `test-results/ai-lesson-${suffix}.png`,
    fullPage: true,
  });
  for (let i = 0; i < 3; i++)
    await page.getByRole("button", { name: "Tiếp theo", exact: true }).click();
  const answers = ["Có dùng AI", "Thiết bị thông thường", "Có dùng AI"];
  const board = page.getByRole("region", { name: "Hoạt động tương tác" });
  for (let i = 0; i < 3; i++) {
    await board.getByRole("button", { name: answers[i], exact: true }).click();
    if (i < 2)
      await board
        .getByRole("button", { name: "Thẻ tiếp", exact: true })
        .click();
  }
  await page.getByRole("button", { name: "Kiểm tra lựa chọn" }).click();
  await expect(page.getByRole("status")).toContainText("100%");
  await page.reload();
  await expect(
    page.getByRole("button", { name: "Tiếp theo", exact: true }),
  ).toBeEnabled();
  await page.getByRole("button", { name: "Tiếp theo", exact: true }).click();
  const quizAnswers = [
    "Nó làm theo lệnh bật/tắt đã định",
    "Ước đoán nhãn từ dữ liệu",
    "Câu được hệ thống tạo hoặc lập trình",
  ];
  for (let i = 0; i < quizAnswers.length; i++) {
    await page
      .getByRole("radio", { name: quizAnswers[i], exact: true })
      .check();
    if (i < quizAnswers.length - 1)
      await board
        .getByRole("button", { name: "Thẻ tiếp", exact: true })
        .click();
  }
  await page.getByRole("button", { name: "Kiểm tra lựa chọn" }).click();
  await expect(page.getByRole("status")).toContainText("100%");
  for (let i = 0; i < 2; i++)
    await page.getByRole("button", { name: "Tiếp theo", exact: true }).click();
  await page
    .getByRole("button", { name: "Hoàn thành bài", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Em đã khám phá xong bài này!" }),
  ).toBeVisible();
  await page.goto("/ai-academy/portfolio");
  await expect(
    page.getByText("Bước khám phá đầu tiên", { exact: true }),
  ).toBeVisible();
  await page.goto("/ai-academy/lab");
  await page.getByRole("button", { name: "2. Thử với mẫu mới" }).click();
  await expect(
    page.getByRole("heading", { name: "3. Kiểm tra và cải tiến" }),
  ).toBeVisible();
  await page.goto("/ai-academy/ai-tutor");
  await page.getByRole("button", { name: "Nhận hướng dẫn" }).click();
  await expect(page.getByRole("status")).toContainText("mô phỏng");
  await page
    .getByLabel("Em đã thử gì?", { exact: false })
    .fill("private-test@example.com");
  await page.getByRole("button", { name: "Nhận hướng dẫn" }).click();
  await expect(page.getByRole("status")).toContainText("Cần điều chỉnh");
  await page.goto("/ai-academy/creative-studio");
  await page
    .getByLabel("Tên sản phẩm", { exact: true })
    .fill("Truyện khu vườn kiểm thử");
  await page
    .getByRole("button", { name: "Ghép truyện 4 khung từ mẫu" })
    .click();
  await page
    .getByLabel("Em tự đánh giá:", { exact: false })
    .fill("Em đã kiểm tra dữ liệu mẫu và sửa một ý để truyện rõ hơn.");
  await page
    .getByRole("combobox", { name: "Gửi tới lớp", exact: true })
    .selectOption(process.env["E2E_ACADEMY_" + suffix + "_CLASS_ID"]!);
  await expect(page.getByRole("status")).toContainText("Đã lưu nháp riêng");
  await page
    .getByRole("button", { name: "Nộp cho giáo viên", exact: true })
    .click();
  await expect(page.getByRole("status")).toContainText("Đã gửi riêng");
  await page.reload();
  await expect(page.getByLabel("Tên sản phẩm", { exact: true })).toHaveValue(
    "Truyện khu vườn kiểm thử",
  );
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
});

test("AI Academy: admin biên soạn bản sao, xem trước, thư viện và an toàn", async ({
  page,
}) => {
  test.skip(!process.env.E2E_ADMIN_PASSWORD, "Cần mật khẩu admin test");
  await login(
    page,
    process.env.E2E_ADMIN_USERNAME || "admin",
    process.env.E2E_ADMIN_PASSWORD!,
  );
  await page.goto("/admin/ai-academy");
  await expect(
    page.getByRole("heading", { name: "Quản trị AI Academy", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Xem trước học sinh", exact: true })
    .click();
  await expect(
    page.getByText("Xem trước chỉ đọc; không ghi điểm/tiến độ học sinh.", {
      exact: true,
    }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Quay lại biên soạn", exact: true })
    .click();
  const before = await (
    await page.request.get("/api/v1/ai-academy/admin/lessons?grade=4")
  ).json();
  const occupied = new Set(
    before
      .filter((r: { unit_id: string }) => r.unit_id === before[0].unit_id)
      .map((r: { position: number }) => r.position),
  );
  let copyPosition = 100;
  while (occupied.has(copyPosition)) copyPosition++;
  await page
    .getByLabel("Thứ tự bản sao", { exact: true })
    .fill(String(copyPosition));
  await page.getByRole("button", { name: "Nhân bản bài", exact: true }).click();
  await expect
    .poll(
      async () =>
        (
          await (
            await page.request.get("/api/v1/ai-academy/admin/lessons?grade=4")
          ).json()
        ).length,
    )
    .toBe(before.length + 1);
  await page
    .getByRole("button", { name: "Thư viện hình", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Tải ảnh học thuật", exact: true }),
  ).toBeVisible();
  await expect(page.locator(".academy-card img").first()).toBeVisible();
  await page
    .getByRole("button", { name: "An toàn / dữ liệu", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Cảnh báo an toàn", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Mẫu hướng dẫn", exact: true })
    .click();
  await expect(
    page.getByRole("heading", {
      name: "Mẫu hướng dẫn có phiên bản",
      exact: true,
    }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
});

test("AI Academy: giáo viên đúng lớp, chấm rubric và phụ huynh đúng trẻ", async ({
  page,
}, info) => {
  const teacher = process.env.E2E_ACADEMY_TEACHER_USERNAME,
    guardian = process.env.E2E_ACADEMY_GUARDIAN_USERNAME,
    password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(
    !teacher || !guardian || !password,
    "Cần fixture teacher/guardian test",
  );
  const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  await staffLogin(page, teacher!, password!);
  await page.goto("/teacher/ai-academy");
  await page
    .getByRole("combobox", { name: "Lớp được phân công", exact: true })
    .selectOption(process.env["E2E_ACADEMY_" + suffix + "_CLASS_ID"]!);
  await page
    .getByRole("button", { name: "Giao bài cho lớp", exact: true })
    .click();
  await expect(page.getByRole("status")).toContainText("Đã giao tới 1");
  await expect(
    page.getByRole("heading", {
      name: "Truyện khu vườn kiểm thử",
      exact: true,
    }),
  ).toBeVisible();
  await page
    .getByRole("textbox", { name: "Góp ý cụ thể", exact: true })
    .fill(
      "Em có lời giải thích rõ và dùng dữ liệu mẫu an toàn; hãy thêm một cách kiểm tra kết quả.",
    );
  await page
    .getByRole("button", { name: "Lưu đánh giá riêng", exact: true })
    .click();
  await expect(
    page.getByRole("textbox", { name: "Góp ý cụ thể", exact: true }),
  ).toHaveValue(/dữ liệu mẫu an toàn/);
  await page
    .getByRole("button", { name: "Đăng xuất", exact: true })
    .first()
    .click();
  await staffLogin(page, guardian!, password!);
  await page.goto("/guardian/ai-academy");
  await expect(
    page.getByRole("heading", { name: "AI Academy · Phụ huynh" }),
  ).toBeVisible();
  const buttons = page.getByRole("button", {
    name: "Cho phép trợ giảng theo chính sách trên",
    exact: true,
  });
  await buttons.first().click();
  await expect(
    page.getByRole("status").filter({ hasText: "Đã cập nhật lựa chọn" }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
});

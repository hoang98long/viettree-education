import { test, expect } from "@playwright/test";
import { login } from "./helpers";

test("admin tạo/duyệt bài minh họa; học sinh đọc, mở gợi ý; nháp giữ bài cũ", async ({
  page,
  browser,
}, info) => {
  const adminPassword = process.env.E2E_ADMIN_PASSWORD;
  const password = process.env.E2E_STUDENT_PASSWORD;
  const username =
    info.project.name === "mobile"
      ? process.env.E2E_LESSON_MOBILE_USERNAME
      : process.env.E2E_LESSON_USERNAME;
  test.skip(
    !adminPassword || !password || !username,
    "Cần tài khoản trong database test riêng",
  );
  await login(page, "admin", adminPassword!);
  await page.goto("/admin/lessons/new");
  const readingReview = page.getByRole("complementary", {
    name: "Rà soát học liệu",
  });
  await expect(readingReview).toContainText("Phần chưa có nội dung");
  const code = `E2E-LESSON-${info.project.name}-${Date.now()}`;
  const title = `Bánh chia đều ${code}`;
  await page.getByLabel("Mã bài học", { exact: true }).fill(code);
  await page.getByLabel("Tên bài học", { exact: true }).fill(title);
  await page
    .getByRole("combobox", { name: "Môn học", exact: true })
    .selectOption({ label: "Toán" });
  await page
    .getByRole("combobox", { name: "Chủ đề", exact: true })
    .selectOption({ label: "Khám phá phân số" });
  await page
    .getByLabel("Mục tiêu (mỗi dòng một ý, tối đa 5)")
    .fill("Nhận biết ba phần tám\nGiải thích bằng hình vẽ");
  for (let i = 1; i <= 4; i++)
    await page
      .getByLabel(`Nội dung phần ${i}`, { exact: true })
      .fill(
        `Phần ${i}: Một bánh chia thành tám phần bằng nhau. Chọn ba phần là 3/8 chiếc bánh.`,
      );
  await page
    .getByLabel("Gợi ý từng bước (mỗi dòng một ý, tối đa 5)")
    .fill(
      "Xác định một chiếc bánh làm đơn vị.\nĐếm tám phần bằng nhau rồi chọn ba phần.",
    );
  await page
    .getByLabel("Câu hỏi tự suy ngẫm (mỗi dòng một ý, tối đa 3)")
    .fill("Vì sao cần chia các phần bằng nhau?");
  await page
    .getByRole("combobox", { name: "Chọn minh họa" })
    .selectOption("fraction");
  const caption = "Minh họa ba trong tám phần bánh bằng nhau.";
  await page
    .getByLabel("Chú thích hình (nêu rõ ý nghĩa và số liệu)")
    .fill(caption);
  await expect(readingReview).toContainText("Đã chọn hình minh họa");
  await expect(readingReview).toContainText("1 mức Free / 1 mức VIP");
  await expect(readingReview).not.toContainText("Phần chưa có nội dung");
  await page
    .getByRole("button", { name: "Xem trước bài học", exact: true })
    .click();
  await expect(page.getByRole("img", { name: caption })).toBeVisible();
  await page
    .getByRole("button", { name: "Lưu nháp bài học", exact: true })
    .click();
  await expect(page).toHaveURL(/\/admin\/lessons\/[^/]+\/edit$/);
  const id = page.url().split("/").at(-2)!;
  const studentContext = await browser.newContext({
    baseURL: info.project.use.baseURL,
    viewport: info.project.use.viewport,
    isMobile: info.project.use.isMobile,
    deviceScaleFactor: info.project.use.deviceScaleFactor,
    hasTouch: info.project.use.hasTouch,
  });
  const student = await studentContext.newPage();
  try {
    await login(student, username!, password!);
    expect((await student.request.get(`/api/v1/lessons/${id}`)).status()).toBe(
      404,
    );
    expect(
      (await student.request.get(`/api/v1/admin/lessons/${id}`)).status(),
    ).toBe(403);
    await page
      .getByLabel("Lý do duyệt / xuất bản / tạo lại nháp")
      .fill("Kiểm tra ví dụ, minh họa và các gợi ý");
    await expect(
      page.getByRole("button", { name: "Xuất bản bài học", exact: true }),
    ).toBeDisabled();
    await page
      .getByRole("button", { name: "Duyệt bài học", exact: true })
      .click();
    await expect(page.getByRole("status")).toContainText("Đã duyệt bản nháp");
    await page
      .getByRole("button", { name: "Xuất bản bài học", exact: true })
      .click();
    await expect(page.getByRole("status")).toContainText("Đã xuất bản bài học");
    await student.goto(`/student/lessons/${id}`);
    await expect(
      student.getByRole("heading", { name: title, exact: true }),
    ).toBeVisible();
    await expect(student.getByRole("img", { name: caption })).toBeVisible();
    await expect(
      student.getByText("Xác định một chiếc bánh làm đơn vị.", { exact: true }),
    ).toHaveCount(0);
    await student
      .getByRole("button", { name: "Mở gợi ý 1", exact: true })
      .click();
    await expect(
      student.getByText("Xác định một chiếc bánh làm đơn vị.", { exact: true }),
    ).toBeVisible();
    await student
      .getByLabel("Vì sao cần chia các phần bằng nhau?")
      .fill("Để mỗi phần là một phần tám.");
    await student
      .getByRole("button", { name: "Mở gợi ý 2", exact: true })
      .click();
    await expect(
      student.getByLabel("Vì sao cần chia các phần bằng nhau?"),
    ).toHaveValue("Để mỗi phần là một phần tám.");
    await expect(
      student.getByRole("button", { name: "Đã mở hết gợi ý", exact: true }),
    ).toBeDisabled();
    await student
      .getByRole("button", { name: "Em đã đọc xong", exact: true })
      .click();
    await expect(
      student.getByRole("button", { name: "Đã đánh dấu đọc xong" }),
    ).toBeDisabled();
    await student.screenshot({
      path: `test-results/illustrated-lesson-${info.project.name}.png`,
      fullPage: true,
    });
    for (const width of [320, 768, 1280]) {
      await student.setViewportSize({ width, height: 900 });
      expect(
        await student.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
      ).toBe(true);
    }
    await page
      .getByLabel("Tên bài học", { exact: true })
      .fill(`Nháp chưa xuất bản ${code}`);
    await page
      .getByRole("button", { name: "Lưu nháp bài học", exact: true })
      .click();
    await expect(page.getByRole("status")).toContainText("Đã lưu nháp");
    await student.reload();
    await expect(
      student.getByRole("heading", { name: title, exact: true }),
    ).toBeVisible();
    await expect(
      student.getByRole("button", { name: "Đã đánh dấu đọc xong" }),
    ).toBeDisabled();
    await expect(
      student.getByLabel("Vì sao cần chia các phần bằng nhau?"),
    ).toHaveValue("");
    const next = student.locator(".lesson-next .list-row").first();
    await next.click();
    await expect(
      student.getByRole("button", { name: "Em đã đọc xong", exact: true }),
    ).toBeEnabled();
    await page.goto("/admin/lessons");
    await page
      .getByRole("combobox", { name: "Trạng thái bài học", exact: true })
      .selectOption("pending");
    await page.getByLabel("Tìm bài học", { exact: true }).fill(code);
    await expect(page.locator(".studio-card")).toHaveCount(1);
    for (const width of [320, 768, 1280]) {
      await page.setViewportSize({ width, height: 900 });
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
      ).toBe(true);
    }
  } finally {
    await studentContext.close();
  }
});

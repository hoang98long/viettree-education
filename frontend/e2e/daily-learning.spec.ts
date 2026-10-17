import { expect, test, type Page, type TestInfo } from "@playwright/test";
import { login } from "./helpers";

const cases = [
  {
    grade: 1,
    title: "Bảy giờ sáng rồi!",
    answers: ["12", "7", "6 giờ", "Buổi sáng"],
  },
  {
    grade: 2,
    title: "Nửa giờ trên đồng hồ",
    answers: ["7 giờ 30 phút", "30 phút", "7 giờ 30 phút", "6"],
  },
  {
    grade: 3,
    title: "Đọc sách trong bao lâu?",
    answers: ["25 phút", "9 giờ 35 phút", "8 giờ 5 phút", "60 phút"],
  },
  {
    grade: 4,
    title: "Xếp lịch học và nghỉ",
    answers: ["40 phút", "14 giờ 15 phút", "14 giờ 20 phút", "5 phút"],
  },
  {
    grade: 5,
    title: "Chuyến đi trong bài toán",
    answers: ["6 km", "18 km", "7 giờ 45 phút", "30 phút"],
  },
];
const suffixFor = (info: TestInfo) =>
  info.project.name === "mobile" ? "MOBILE" : "DESKTOP";

async function student(page: Page, info: TestInfo, grade: number) {
  const username =
    process.env[`E2E_VERIFICATION_GRADE${grade}_${suffixFor(info)}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần fixture riêng trên database test");
  await login(page, username!, password!);
}
const regex = (value: string) =>
  new RegExp("^[A-Z]\\s+" + value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "$");

for (const row of cases) {
  test(`Lớp ${row.grade}: bài mới, học tiếp đúng lượt và chấm đủ bốn câu`, async ({
    page,
  }, info) => {
    await student(page, info, row.grade);
    await page.goto("/student/lessons");
    await page.getByLabel("Tên bài hoặc chủ đề").fill(row.title);
    await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
    await page.getByRole("link", { name: /^(Mở bài học|Đọc tiếp)$/ }).click();
    await expect(page).toHaveURL(/\/student\/lessons\/[a-f0-9-]+$/);
    const lessonPath = new URL(page.url()).pathname;
    await expect(
      page.getByRole("heading", { name: row.title, exact: true }),
    ).toBeVisible();
    await page.getByRole("button", { name: "Mở gợi ý 1", exact: true }).click();
    await page
      .getByRole("link", { name: "VietTree · Về trang chủ", exact: true })
      .click();
    await expect(page).toHaveURL(/\/student\/dashboard$/);
    const resumed = page.getByRole("region", { name: "Việc học đang dở" });
    await expect(
      resumed.getByRole("link", {
        name: new RegExp(row.title.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")),
      }),
    ).toHaveAttribute("href", lessonPath);
    await expect(
      page
        .locator(".welcome-card")
        .getByRole("link", { name: "Học tiếp", exact: true }),
    ).toHaveAttribute("href", lessonPath);
    await resumed.getByRole("link").first().click();
    await page
      .getByRole("link", {
        name: new RegExp(
          row.title.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "$",
        ),
      })
      .last()
      .click();
    await page.getByRole("button", { name: "Bắt đầu / Tiếp tục" }).click();
    await expect(page).toHaveURL(/\/student\/attempts\/[a-f0-9-]+$/);
    const attemptPath = new URL(page.url()).pathname;
    const saved = page.waitForResponse(
      (response) =>
        response.url().includes("/answers/") &&
        response.request().method() === "PUT" &&
        response.status() === 200,
    );
    await page.getByRole("radio", { name: regex(row.answers[0]) }).check();
    await saved;
    await page
      .getByRole("link", { name: "VietTree · Về trang chủ", exact: true })
      .click();
    await expect(page).toHaveURL(/\/student\/dashboard$/);
    await expect(
      page
        .locator(".welcome-card")
        .getByRole("link", { name: "Học tiếp", exact: true }),
    ).toHaveAttribute("href", attemptPath);
    await page.screenshot({
      path: `../.tools/daily-resume-grade${row.grade}-${suffixFor(info)}.png`,
      fullPage: true,
    });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    await page
      .locator(".welcome-card")
      .getByRole("link", { name: "Học tiếp", exact: true })
      .click();
    await expect(page).toHaveURL(attemptPath);
    await expect(
      page.getByRole("radio", { name: regex(row.answers[0]) }),
    ).toBeChecked();
    for (let i = 1; i < row.answers.length; i++) {
      await page.getByRole("button", { name: "Câu tiếp", exact: true }).click();
      await page.getByRole("radio", { name: regex(row.answers[i]) }).check();
    }
    await page.getByRole("button", { name: "Xem lại", exact: true }).click();
    await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
    await page
      .getByRole("button", { name: "Xác nhận nộp", exact: true })
      .click();
    await expect(page).toHaveURL(/\/student\/results\//);
    const result = await (
      await page.request.get(
        `/api/v1/attempts/${attemptPath.split("/").pop()}/result`,
      )
    ).json();
    expect(result.correct_count).toBe(4);
  });
}

test("AI lớp 1: tìm thẻ chưa đúng, sửa rồi kiểm tra lại", async ({
  page,
}, info) => {
  await student(page, info, 1);
  const catalog = await (
    await page.request.get("/api/v1/ai-academy/catalog?grade=1")
  ).json();
  const lesson = catalog.find(
    (item: { code: string }) => item.code === "AI1-37",
  );
  await page.goto(`/ai-academy/lessons/${lesson.id}`);
  for (let i = 0; i < 3; i++)
    await page.getByRole("button", { name: "Tiếp theo", exact: true }).click();
  const board = page.getByRole("region", { name: "Hoạt động tương tác" });
  await board
    .getByRole("button", { name: "Khớp với que tính", exact: true })
    .click();
  await board.getByRole("button", { name: "Thẻ tiếp", exact: true }).click();
  await board
    .getByRole("button", { name: "Khớp với que tính", exact: true })
    .click();
  await board
    .getByRole("button", { name: "Kiểm tra lựa chọn", exact: true })
    .click();
  await expect(board.getByRole("status")).toContainText("50%");
  await board
    .getByRole("button", { name: "Thẻ 1 · Xem lại", exact: true })
    .click();
  await expect(
    board.getByRole("heading", { name: "2 + 3 = 6", exact: true }),
  ).toBeVisible();
  await expect(board.getByRole("note")).toContainText("5 que");
  await expect(board.getByRole("note")).toHaveCSS("display", "block");
  await expect(board.getByRole("status")).toHaveCSS("display", "block");
  await page.screenshot({
    path: `../.tools/daily-ai-review-${suffixFor(info)}.png`,
    fullPage: true,
  });
  await board.getByRole("button", { name: "Đếm lại", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Tiếp theo", exact: true }),
  ).toBeDisabled();
  await board
    .getByRole("button", { name: "Kiểm tra lựa chọn", exact: true })
    .click();
  await expect(board.getByRole("status")).toContainText("100%");
  await expect(
    page.getByRole("button", { name: "Tiếp theo", exact: true }),
  ).toBeEnabled();
});

test("Học tiếp gộp bài đọc, lượt luyện và bước AI gần nhất", async ({
  page,
}, info) => {
  await student(page, info, 3);
  const practices = await (
    await page.request.get(
      "/api/v1/students/me/practice-library?search=Meet%20my%20family",
    )
  ).json();
  expect(practices.items).toHaveLength(1);
  const visit = page.waitForResponse(
    (response) =>
      response
        .url()
        .includes(`/lessons/${practices.items[0].lesson_id}/visit`) &&
      response.status() === 200,
  );
  await page.goto(`/student/lessons/${practices.items[0].lesson_id}`);
  await visit;
  await page.goto(`/student/assessments/${practices.items[0].id}`);
  await page.getByRole("button", { name: "Bắt đầu / Tiếp tục" }).click();
  await expect(page).toHaveURL(/\/student\/attempts\//);
  const attemptPath = new URL(page.url()).pathname;
  const catalog = await (
    await page.request.get("/api/v1/ai-academy/catalog?grade=3")
  ).json();
  const lesson = catalog.find(
    (item: { code: string }) => item.code === "AI3-37",
  );
  await page.goto(`/ai-academy/lessons/${lesson.id}`);
  await page.getByRole("button", { name: "Tiếp theo", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Em khám phá", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("link", { name: "VietTree · Về trang chủ", exact: true })
    .click();
  await expect(page).toHaveURL(/\/student\/dashboard$/);
  const resumed = page.getByRole("region", { name: "Việc học đang dở" });
  await expect(resumed.getByRole("link")).toHaveCount(3);
  await expect(resumed.getByText("Bước 2/7", { exact: true })).toBeVisible();
  await expect(
    resumed.getByRole("link", { name: /Bài đang làm/ }),
  ).toHaveAttribute("href", attemptPath);
  await expect(
    page
      .locator(".welcome-card")
      .getByRole("link", { name: "Học tiếp", exact: true }),
  ).toHaveAttribute("href", `/ai-academy/lessons/${lesson.id}`);
  await page.screenshot({
    path: `../.tools/daily-three-kinds-${suffixFor(info)}.png`,
    fullPage: true,
  });
  await page
    .locator(".welcome-card")
    .getByRole("link", { name: "Học tiếp", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Em khám phá", exact: true }),
  ).toBeVisible();
});

test("VIP lớp 5: hội thoại có tranh đúng đồ ăn và nước uống", async ({
  page,
}, info) => {
  await student(page, info, 5);
  const library = await (
    await page.request.get(
      "/api/v1/students/me/lesson-library?search=A%20polite%20meal",
    )
  ).json();
  expect(library.items).toHaveLength(1);
  await page.goto(`/student/lessons/${library.items[0].id}`);
  await expect(page.locator('img[src*="rice.svg"]').first()).toBeVisible();
  await expect(page.locator('img[src*="water.svg"]').first()).toBeVisible();
  for (const level of [1, 2, 3])
    await page
      .getByRole("button", { name: `Mở gợi ý ${level}`, exact: true })
      .click();
  await expect(
    page.getByRole("button", { name: "Đã mở hết gợi ý", exact: true }),
  ).toBeDisabled();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await page.screenshot({
    path: `../.tools/daily-rice-lesson-${suffixFor(info)}.png`,
    fullPage: true,
  });
});

test("Admin kiểm kê bộ Mỗi ngày một khám phá của cả năm khối", async ({
  page,
}) => {
  test.skip(!process.env.E2E_ADMIN_PASSWORD, "Cần admin test riêng");
  await login(page, "admin", process.env.E2E_ADMIN_PASSWORD!);
  await page.goto("/admin/curriculum");
  for (const grade of [1, 2, 3, 4, 5]) {
    await page.getByLabel("Lớp học liệu").selectOption(String(grade));
    await expect(
      page.getByLabel("Học liệu bổ sung daily-2026-03"),
    ).toContainText("3/3 bài · 12/12 câu hỏi · 3/3 đề");
  }
});

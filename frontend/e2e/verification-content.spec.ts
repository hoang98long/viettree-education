import { expect, test } from "@playwright/test";
import { login } from "./helpers";

const cases = [
  {
    grade: 1,
    number: 37,
    activity: ["Đếm lại", "Khớp với que tính"],
    quiz: ["5 que", "Không", "Que tính"],
    reading: "Bút của Hà",
  },
  {
    grade: 2,
    number: 37,
    activity: ["Đúng thẻ gốc", "Cần sửa"],
    quiz: ["Cạnh sách", "Đọc lại thẻ gốc", "Nhờ người lớn chỉ bằng vật mẫu"],
    reading: "Chiếc cốc dùng lại",
  },
  {
    grade: 3,
    number: 38,
    activity: [
      "Thêm mẫu đa dạng",
      "Kiểm tra đặc điểm",
      "Chưa thêm dạng mới",
      "Thêm mẫu đa dạng",
    ],
    quiz: ["Có thể dựa nhầm vào màu", "Táo xanh", "Có, bằng thẻ để riêng"],
    reading: "Giỏ sách lớp em",
  },
  {
    grade: 4,
    number: 38,
    activity: [
      "Bổ sung mẫu",
      "Bổ sung mẫu",
      "Kiểm tra chưa đủ",
      "Kiểm tra theo nhóm",
    ],
    quiz: ["Bút đỏ", "Không bảo đảm", "Thử từng nhóm bằng thẻ mới"],
    reading: "Tấm bảng nhắc tưới cây",
  },
  {
    grade: 5,
    number: 38,
    activity: [
      "Kết quả nhóm xanh",
      "Kết quả nhóm đỏ",
      "Thiếu thông tin nhóm",
      "Bổ sung kiểm tra",
    ],
    quiz: ["80%", "Đúng 0 trong 2 thẻ", "Chưa, mới thử hai thẻ đỏ"],
    reading: "Đọc bảng tin cho đúng",
  },
];

for (const row of cases) {
  test(`Lớp ${row.grade}: học AI mới, gợi ý, tiếp tục phiên và bài đọc mới`, async ({
    page,
  }, info) => {
    const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
    const username =
      process.env[`E2E_VERIFICATION_GRADE${row.grade}_${suffix}_USERNAME`];
    const password = process.env.E2E_STUDENT_PASSWORD;
    test.skip(!username || !password, "Cần fixture riêng trong database test");
    await login(page, username!, password!);
    const catalog = await (
      await page.request.get(`/api/v1/ai-academy/catalog?grade=${row.grade}`)
    ).json();
    expect(catalog).toHaveLength(38);
    const lesson = catalog.find(
      (l: { code: string }) => l.code === `AI${row.grade}-${row.number}`,
    );
    await page.goto(`/ai-academy/lessons/${lesson.id}`);
    await expect(
      page.getByRole("heading", { name: lesson.title, exact: true }),
    ).toBeVisible();
    for (let i = 0; i < 3; i++)
      await page
        .getByRole("button", { name: "Tiếp theo", exact: true })
        .click();
    const board = page.getByRole("region", { name: "Hoạt động tương tác" });
    const limit = row.grade >= 3 ? 3 : 1;
    for (let i = 1; i <= limit; i++) {
      await page
        .getByRole("button", {
          name: i === 1 ? "Em cần gợi ý" : "Gợi ý thêm · VIP",
          exact: true,
        })
        .click();
      await expect(
        page.getByText(`Gợi ý ${i}/${limit}`, { exact: true }),
      ).toBeVisible();
    }
    await expect(
      page.getByRole("button", { name: "Đã mở hết gợi ý", exact: true }),
    ).toBeDisabled();
    if (row.grade >= 3) {
      await board.getByText("Đổi số thẻ thực hành", { exact: true }).click();
      await board.getByLabel("Mức thực hành").selectOption("3");
    }
    const keys: string[] = [];
    if (row.grade === 1) {
      await page.route(
        "**/api/v1/ai-academy/lessons/*/attempts",
        async (route) => {
          keys.push(route.request().postDataJSON().idempotency_key);
          if (keys.length === 1) {
            await route.fetch(); // Server has committed; the response is lost.
            await route.abort("failed");
          } else await route.continue();
        },
      );
    }
    for (let i = 0; i < row.activity.length; i++) {
      await board
        .getByRole("button", { name: row.activity[i], exact: true })
        .click();
      if (i < row.activity.length - 1)
        await board
          .getByRole("button", { name: "Thẻ tiếp", exact: true })
          .click();
    }
    await board
      .getByRole("button", { name: "Kiểm tra lựa chọn", exact: true })
      .click();
    if (row.grade === 1) {
      await expect(board.getByRole("alert")).toBeVisible();
      await board
        .getByRole("button", { name: "Kiểm tra lựa chọn", exact: true })
        .click();
      await expect(board.getByRole("status")).toContainText("100%");
      expect(keys).toHaveLength(2);
      expect(keys[0]).toBe(keys[1]);
      await page.unroute("**/api/v1/ai-academy/lessons/*/attempts");
    } else await expect(board.getByRole("status")).toContainText("100%");
    await page.screenshot({
      path: `../.tools/verification-grade${row.grade}-${suffix}.png`,
      fullPage: true,
    });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    await page.reload();
    await expect(
      page.getByRole("button", { name: "Tiếp theo", exact: true }),
    ).toBeEnabled();
    await page.getByRole("button", { name: "Tiếp theo", exact: true }).click();
    for (let i = 0; i < row.quiz.length; i++) {
      await board
        .getByRole("radio", { name: row.quiz[i], exact: true })
        .check();
      if (i < row.quiz.length - 1)
        await board
          .getByRole("button", { name: "Thẻ tiếp", exact: true })
          .click();
    }
    await board
      .getByRole("button", { name: "Kiểm tra lựa chọn", exact: true })
      .click();
    await expect(board.getByRole("status")).toContainText("100%");
    for (let i = 0; i < 2; i++)
      await page
        .getByRole("button", { name: "Tiếp theo", exact: true })
        .click();
    await page
      .getByRole("button", { name: "Hoàn thành bài", exact: true })
      .click();
    await expect(
      page.getByRole("heading", { name: "Em đã khám phá xong bài này!" }),
    ).toBeVisible();
    await page.goto("/student/lessons");
    await page.getByLabel("Tên bài hoặc chủ đề").fill(row.reading);
    await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
    await page.getByRole("link", { name: /^(Mở bài học|Đọc tiếp)$/ }).click();
    await expect(
      page.getByRole("heading", { name: row.reading, exact: true }),
    ).toBeVisible();
    await page.getByRole("button", { name: "Mở gợi ý 1", exact: true }).click();
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
  });
}

test("Admin thấy đủ học liệu ôn tập cho năm khối", async ({ page }) => {
  test.skip(!process.env.E2E_ADMIN_PASSWORD, "Cần admin test riêng");
  await login(page, "admin", process.env.E2E_ADMIN_PASSWORD!);
  await page.goto("/admin/curriculum");
  for (const grade of [1, 2, 3, 4, 5]) {
    await page.getByLabel("Lớp học liệu").selectOption(String(grade));
    await expect(
      page.getByLabel("Học liệu bổ sung review-2026-02"),
    ).toContainText("3/3 bài · 12/12 câu hỏi · 3/3 đề");
  }
});

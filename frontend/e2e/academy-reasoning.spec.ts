import { expect, test } from "@playwright/test";
import { login } from "./helpers";

const vipCases = [
  {
    grade: 1,
    activity: ["Gọi tên sách", "Hỏi lại"],
    quiz: ["Không thấy", "Mở phần che", "Có"],
  },
  {
    grade: 2,
    activity: ["Hỏi sách môn nào", "Chọn sách Toán", "Chọn sách Tiếng Việt"],
    quiz: ["Sách môn nào?", "Sách Toán", "Để hiểu đúng yêu cầu"],
  },
  {
    grade: 3,
    activity: ["Đủ để theo bảng", "Cần thêm thông tin", "Ngoài bộ quy tắc"],
    quiz: [
      "Bổ sung dòng bị mất",
      "Bảng này chưa xét cam",
      "Người thiết kế bảng",
    ],
  },
  {
    grade: 4,
    activity: [
      "Khớp thẻ gốc",
      "Khác thẻ gốc",
      "Vẫn phải đối chiếu",
      "Cần tìm nguồn",
    ],
    quiz: ["16 giờ", "Không", "Nhờ người lớn kiểm tra giờ hiện hành"],
  },
  {
    grade: 5,
    activity: [
      "Bổ sung bối cảnh",
      "Bổ sung bối cảnh",
      "Chưa dùng ngay",
      "Kiểm tra trước khi dùng",
    ],
    quiz: [
      "Chưa, cần người phụ trách kiểm tra",
      "Loại cây và độ ẩm đất",
      "Người phụ trách được phân công",
    ],
  },
];
for (const row of vipCases) {
  test(`VIP: lớp ${row.grade} hoàn thành bài giải thích nâng cao`, async ({
    page,
  }, info) => {
    const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
    const username =
      process.env[
        `E2E_${row.grade < 3 ? "REASONING_VIP" : "REASONING"}_GRADE${row.grade}_${suffix}_USERNAME`
      ];
    test.skip(
      !username || !process.env.E2E_STUDENT_PASSWORD,
      "Cần fixture VIP test riêng",
    );
    await login(page, username!, process.env.E2E_STUDENT_PASSWORD!);
    const catalog = await (
      await page.request.get(`/api/v1/ai-academy/catalog?grade=${row.grade}`)
    ).json();
    const lesson = catalog.find(
      (entry: { code: string }) => entry.code === `AI${row.grade}-40`,
    );
    await page.goto(`/ai-academy/lessons/${lesson.id}`);
    for (let index = 0; index < 3; index++)
      await page
        .getByRole("button", { name: "Tiếp theo", exact: true })
        .click();
    const board = page.getByRole("region", { name: "Hoạt động tương tác" });
    for (let index = 1; index <= 3; index++) {
      await page
        .getByRole("button", {
          name: index === 1 ? "Em cần gợi ý" : "Gợi ý thêm · VIP",
          exact: true,
        })
        .click();
      await expect(
        page.getByText(`Gợi ý ${index}/3`, { exact: true }),
      ).toBeVisible();
    }
    if (row.grade >= 3) {
      await board.getByText("Đổi số thẻ thực hành", { exact: true }).click();
      await board.getByLabel("Mức thực hành").selectOption("3");
    }
    for (let index = 0; index < row.activity.length; index++) {
      await board
        .getByRole("button", { name: row.activity[index], exact: true })
        .click();
      if (index < row.activity.length - 1)
        await board
          .getByRole("button", { name: "Thẻ tiếp", exact: true })
          .click();
    }
    await board
      .getByRole("button", { name: "Kiểm tra lựa chọn", exact: true })
      .click();
    await expect(board.getByRole("status")).toContainText("100%");
    if (row.grade === 1)
      await page.screenshot({
        path: `../.tools/academy-concealed-card-${suffix}.png`,
        fullPage: true,
      });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    await page.getByRole("button", { name: "Tiếp theo", exact: true }).click();
    for (let index = 0; index < row.quiz.length; index++) {
      await board
        .getByRole("radio", { name: row.quiz[index], exact: true })
        .check();
      if (index < row.quiz.length - 1)
        await board
          .getByRole("button", { name: "Thẻ tiếp", exact: true })
          .click();
    }
    await board
      .getByRole("button", { name: "Kiểm tra lựa chọn", exact: true })
      .click();
    await expect(board.getByRole("status")).toContainText("100%");
    for (let index = 0; index < 2; index++)
      await page
        .getByRole("button", { name: "Tiếp theo", exact: true })
        .click();
    await page
      .getByRole("button", { name: "Hoàn thành bài", exact: true })
      .click();
    await expect(
      page.getByRole("heading", { name: "Em đã khám phá xong bài này!" }),
    ).toBeVisible();
  });
}

const cases = [
  {
    grade: 1,
    activity: ["Có trang để đọc", "Dùng để viết"],
    quiz: ["Sách", "Có trang để đọc", "Nhờ người lớn đọc cùng"],
  },
  {
    grade: 2,
    activity: ["Đúng cả hai", "Khác màu", "Khác đồ vật"],
    quiz: ["Bút đỏ", "Màu sắc", "Hai: vật và màu"],
  },
  {
    grade: 3,
    activity: ["Nhánh đọc", "Nhánh viết, có mực", "Nhánh viết, không mực"],
    quiz: ["Bút mực", "Viết, không có mực", "Không"],
  },
  {
    grade: 4,
    activity: [
      "Căn cứ phù hợp",
      "Chưa đủ căn cứ",
      "Chưa đủ căn cứ",
      "Không đúng chủ đề",
    ],
    quiz: ["Nội dung trồng cây", "Không", "Có, đối chiếu nội dung sách"],
  },
  {
    grade: 5,
    activity: [
      "Đáp ứng hai tiêu chí",
      "Khác chủ đề",
      "Vượt độ dài",
      "Vẫn cần xét tiêu chí",
    ],
    quiz: ["Sách A", "80 trang vượt giới hạn 20 trang", "Xét lại các tiêu chí"],
  },
];
for (const row of cases) {
  test(`AI lớp ${row.grade}: đúng lớp, tìm không dấu, học tiếp và chấm bài mới`, async ({
    page,
  }, info) => {
    const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
    const username =
      process.env[`E2E_REASONING_GRADE${row.grade}_${suffix}_USERNAME`];
    test.skip(
      !username || !process.env.E2E_STUDENT_PASSWORD,
      "Cần fixture database test riêng",
    );
    const errors: string[] = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await login(page, username!, process.env.E2E_STUDENT_PASSWORD!);
    const requests: string[] = [];
    page.on("request", (request) => {
      if (request.url().includes("/ai-academy/catalog?"))
        requests.push(request.url());
    });
    await page.goto("/ai-academy");
    await expect(
      page.getByRole("heading", {
        name: `Lớp ${row.grade} · 40 bài · 11 chủ đề`,
        exact: true,
      }),
    ).toBeVisible();
    expect(requests).toEqual([]);
    if (row.grade === 1) {
      await page.getByLabel("Chọn lớp để khám phá").selectOption("2");
      await expect(
        page.getByRole("heading", {
          name: "Lớp 2 · 40 bài · 11 chủ đề",
          exact: true,
        }),
      ).toBeVisible();
      await page
        .getByRole("button", { name: "Em có thể học", exact: true })
        .click();
      await expect(
        page.getByRole("region", { name: "Tìm bài AI" }).getByRole("status"),
      ).toHaveText("0 bài phù hợp");
      await expect(
        page.getByRole("region", { name: "Bài AI tiếp theo" }),
      ).toHaveCount(0);
      await page.getByLabel("Chọn lớp để khám phá").selectOption("1");
    }
    await page
      .getByLabel("Tìm tên bài hoặc chủ đề")
      .fill("giai thich lua chon");
    await expect(
      page.getByRole("region", { name: "Tìm bài AI" }).getByRole("status"),
    ).toHaveText("2 bài phù hợp");
    const catalog = await (
      await page.request.get(`/api/v1/ai-academy/catalog?grade=${row.grade}`)
    ).json();
    const lesson = catalog.find(
      (entry: { code: string }) => entry.code === `AI${row.grade}-39`,
    );
    await page
      .getByRole("button", { name: "Em có thể học", exact: true })
      .click();
    await expect(
      page.getByRole("region", { name: "Tìm bài AI" }).getByRole("status"),
    ).toHaveText(`${row.grade < 3 ? 1 : 2} bài phù hợp`);
    await page.goto(`/ai-academy/lessons/${lesson.id}`);
    for (let i = 0; i < 3; i++)
      await page
        .getByRole("button", { name: "Tiếp theo", exact: true })
        .click();
    await page.goto("/ai-academy");
    const resume = page.getByRole("region", { name: "Bài AI tiếp theo" });
    await expect(
      resume.getByRole("heading", { name: lesson.title, exact: true }),
    ).toBeVisible();
    await expect(
      resume.getByRole("link", { name: "Học tiếp bài này" }),
    ).toHaveAttribute("href", `/ai-academy/lessons/${lesson.id}`);
    await page.getByRole("button", { name: "Đang học", exact: true }).click();
    await expect(
      page.getByRole("region", { name: "Tìm bài AI" }).getByRole("status"),
    ).toHaveText("1 bài phù hợp");
    await page.getByLabel("Tìm tên bài hoặc chủ đề").fill("khongcotukhoanay");
    await expect(
      page.getByText(
        "Chưa có bài phù hợp. Em thử từ khác hoặc xem tất cả bài nhé.",
      ),
    ).toBeVisible();
    await page
      .getByRole("button", { name: "Xem tất cả bài", exact: true })
      .click();
    await page.goto("/ai-academy/games");
    await expect(
      page.getByRole("heading", {
        name: `Trò chơi học tập · Lớp ${row.grade}`,
        exact: true,
      }),
    ).toBeVisible();
    await page
      .getByRole("button", { name: "Em có thể học", exact: true })
      .click();
    const links = page.locator("a.academy-card");
    for (const href of await links.evaluateAll((elements) =>
      elements.map((element) => element.getAttribute("href")),
    )) {
      expect(
        catalog.some(
          (entry: { id: string; locked: boolean }) =>
            !entry.locked && href === `/ai-academy/lessons/${entry.id}`,
        ),
      ).toBe(true);
    }
    await page
      .locator(`a.academy-card[href="/ai-academy/lessons/${lesson.id}"]`)
      .click();
    const board = page.getByRole("region", { name: "Hoạt động tương tác" });
    await expect(board).toBeVisible();
    const limit = row.grade < 3 ? 1 : 3;
    for (let index = 1; index <= limit; index++) {
      await page
        .getByRole("button", {
          name: index === 1 ? "Em cần gợi ý" : "Gợi ý thêm · VIP",
          exact: true,
        })
        .click();
      await expect(
        page.getByText(`Gợi ý ${index}/${limit}`, { exact: true }),
      ).toBeVisible();
    }
    if (row.grade >= 3) {
      await board.getByText("Đổi số thẻ thực hành", { exact: true }).click();
      await board.getByLabel("Mức thực hành").selectOption("3");
    }
    for (let index = 0; index < row.activity.length; index++) {
      await board
        .getByRole("button", { name: row.activity[index], exact: true })
        .click();
      if (index < row.activity.length - 1)
        await board
          .getByRole("button", { name: "Thẻ tiếp", exact: true })
          .click();
    }
    await board
      .getByRole("button", { name: "Kiểm tra lựa chọn", exact: true })
      .click();
    await expect(board.getByRole("status")).toContainText("100%");
    await page.screenshot({
      path: `../.tools/academy-reasoning-${row.grade}-${suffix}.png`,
      fullPage: true,
    });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    await page.getByRole("button", { name: "Tiếp theo", exact: true }).click();
    for (let index = 0; index < row.quiz.length; index++) {
      await board
        .getByRole("radio", { name: row.quiz[index], exact: true })
        .check();
      if (index < row.quiz.length - 1)
        await board
          .getByRole("button", { name: "Thẻ tiếp", exact: true })
          .click();
    }
    await board
      .getByRole("button", { name: "Kiểm tra lựa chọn", exact: true })
      .click();
    await expect(board.getByRole("status")).toContainText("100%");
    for (let index = 0; index < 2; index++)
      await page
        .getByRole("button", { name: "Tiếp theo", exact: true })
        .click();
    await page
      .getByRole("button", { name: "Hoàn thành bài", exact: true })
      .click();
    await expect(
      page.getByRole("heading", { name: "Em đã khám phá xong bài này!" }),
    ).toBeVisible();
    expect(errors).toEqual([]);
  });
}

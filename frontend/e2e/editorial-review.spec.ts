import { expect, test } from "@playwright/test";
import { login } from "./helpers";

test.use({ actionTimeout: 15_000 });
type ReviewCase = {
  grade: number;
  plan: string;
  aiCode: string;
  aiTitle: string;
  activity: string[];
  quiz: string[];
  ordinaryTitle: string;
};
const cases: ReviewCase[] = [
  {
    grade: 1,
    plan: "FREE",
    aiCode: "AI1-02",
    aiTitle: "Xếp thẻ cùng nhóm",
    activity: ["Con vật", "Trái cây"],
    quiz: ["Con vật", "Trái cây", "Kiểm tra lại, nhờ cô giúp"],
    ordinaryTitle: "Nhìn khối hộp và khối lập phương",
  },
  {
    grade: 1,
    plan: "VIP",
    aiCode: "AI1-26",
    aiTitle: "Cat or dog?",
    activity: ["Đúng", "Thử lại"],
    quiz: ["Đúng", "Thử lại", "Kiểm tra lại, nhờ cô giúp"],
    ordinaryTitle: "Tư duy: tìm số còn thiếu",
  },
  {
    grade: 2,
    plan: "FREE",
    aiCode: "AI2-01",
    aiTitle: "Sắp xếp bộ sưu tập",
    activity: ["Con vật", "Trái cây", "Con vật"],
    quiz: ["Con vật", "Con vật", "Kiểm tra lại, nhờ cô giúp"],
    ordinaryTitle: "Ôn đọc số và chục, đơn vị",
  },
  {
    grade: 2,
    plan: "VIP",
    aiCode: "AI2-26",
    aiTitle: "Fruit picture cards",
    activity: ["Đúng", "Đúng", "Thử lại"],
    quiz: ["Đúng", "Thử lại", "Kiểm tra lại, nhờ cô giúp"],
    ordinaryTitle: "Tư duy: nhiều hơn một số vật",
  },
  {
    grade: 3,
    plan: "FREE",
    aiCode: "AI3-02",
    aiTitle: "Nhãn của bộ dữ liệu",
    activity: ["Con vật", "Trái cây", "Con vật"],
    quiz: ["Con vật", "Con vật", "Kiểm tra lại, nhờ cô giúp"],
    ordinaryTitle: "Đọc và viết số có bốn chữ số",
  },
  {
    grade: 3,
    plan: "VIP",
    aiCode: "AI3-28",
    aiTitle: "Check a short sentence",
    activity: ["Có căn cứ", "Cần kiểm tra"],
    quiz: ["Có căn cứ", "Cần kiểm tra", "Kiểm tra lại, nhờ cô giúp"],
    ordinaryTitle: "Bài toán hai bước và dữ kiện thừa",
  },
  {
    grade: 4,
    plan: "FREE",
    aiCode: "AI4-04",
    aiTitle: "Dữ liệu là gì?",
    activity: ["Hình ảnh", "Âm thanh", "Số", "Từ ngữ"],
    quiz: ["Nhóm của mẫu", "Chưa đủ thông tin", "Thẻ đồ vật tự vẽ"],
    ordinaryTitle: "Đổi đơn vị trong đời sống",
  },
  {
    grade: 4,
    plan: "VIP",
    aiCode: "AI4-12",
    aiTitle: "Phân số trực quan với bánh và hình khối",
    activity: ["3/8", "1/4", "Tổng số phần bằng nhau", "Số phần được chọn"],
    quiz: ["3/8", "Không, phải kiểm tra phần bằng nhau", "Không nhất thiết"],
    ordinaryTitle: "Giải nhiều bước và kiểm tra kết quả",
  },
  {
    grade: 5,
    plan: "FREE",
    aiCode: "AI5-01",
    aiTitle: "Nhãn quyết định điều máy học",
    activity: ["Nhãn phù hợp", "Cần sửa nhãn", "Nhãn phù hợp"],
    quiz: ["Nhãn phù hợp", "Nhãn phù hợp", "Kiểm tra lại, nhờ cô giúp"],
    ordinaryTitle: "Ôn số tự nhiên và tính hợp lí",
  },
  {
    grade: 5,
    plan: "VIP",
    aiCode: "AI5-28",
    aiTitle: "Verify a short description",
    activity: ["Có căn cứ", "Cần kiểm tra", "Có căn cứ"],
    quiz: ["Có căn cứ", "Có căn cứ", "Kiểm tra lại, nhờ cô giúp"],
    ordinaryTitle: "Tư duy: tỉ lệ bản đồ và đổi đơn vị",
  },
];

for (const row of cases) {
  test(`Biên tập lớp ${row.grade} ${row.plan}: bài cũ, hình AI và quyền học`, async ({
    page,
  }, info) => {
    const device = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
    const username =
      process.env[
        `E2E_EDITORIAL_GRADE${row.grade}_${row.plan}_${device}_USERNAME`
      ];
    const password = process.env.E2E_STUDENT_PASSWORD;
    test.skip(!username || !password, "Cần fixture riêng trên database test");
    await login(page, username!, password!);
    await page.goto("/student/lessons");
    await page.getByLabel("Tên bài hoặc chủ đề").fill(row.ordinaryTitle);
    await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
    const card = page.locator("article.library-card").filter({
      has: page.getByRole("heading", {
        name: row.ordinaryTitle,
        exact: true,
      }),
    });
    await expect(card).toHaveCount(1);
    await card.getByRole("link", { name: /^(Mở bài học|Đọc tiếp)$/ }).click();
    await expect(
      page.getByRole("heading", { name: row.ordinaryTitle, exact: true }),
    ).toBeVisible();
    await expect(page.locator(".lesson-figure")).toBeVisible();
    await page.getByRole("button", { name: "Mở gợi ý 1", exact: true }).click();
    if (row.grade === 4 && row.plan === "FREE") {
      await expect(page.locator(".lesson-figure")).toContainText(
        "9 giờ 30 phút",
      );
      await expect(page.locator(".lesson-hints li")).not.toContainText(
        "chu vi",
      );
    }
    const catalog = await (
      await page.request.get(`/api/v1/ai-academy/catalog?grade=${row.grade}`)
    ).json();
    expect(catalog).toHaveLength(40);
    const lesson = catalog.find(
      (item: { code: string }) => item.code === row.aiCode,
    );
    await page.goto(`/ai-academy/lessons/${lesson.id}`);
    await expect(
      page.getByRole("heading", { name: row.aiTitle, exact: true }),
    ).toBeVisible();
    for (let i = 0; i < 3; i++)
      await page
        .getByRole("button", { name: "Tiếp theo", exact: true })
        .click();
    const board = page.getByRole("region", { name: "Hoạt động tương tác" });
    await page
      .getByRole("button", { name: "Em cần gợi ý", exact: true })
      .click();
    const hintCount = row.plan === "VIP" ? 3 : 1;
    await expect(
      page.getByText(`Gợi ý 1/${hintCount}`, { exact: true }),
    ).toBeVisible();
    if (row.plan === "VIP") {
      for (let i = 2; i <= 3; i++) {
        await page
          .getByRole("button", { name: "Gợi ý thêm · VIP", exact: true })
          .click();
        await expect(
          page.getByText(`Gợi ý ${i}/3`, { exact: true }),
        ).toBeVisible();
      }
    }
    if (row.grade >= 3) {
      await board.getByText("Đổi số thẻ thực hành", { exact: true }).click();
      await board.getByLabel("Mức thực hành").selectOption("3");
    }
    for (let i = 0; i < row.activity.length; i++) {
      await board
        .getByRole("button", { name: row.activity[i], exact: true })
        .click();
      for (const img of await board.locator("img").all())
        await expect
          .poll(() =>
            img.evaluate(
              (element: HTMLImageElement) =>
                element.complete && element.naturalWidth > 0,
            ),
          )
          .toBe(true);
      if (i < row.activity.length - 1)
        await board
          .getByRole("button", { name: "Thẻ tiếp", exact: true })
          .click();
    }
    await board
      .getByRole("button", { name: "Kiểm tra lựa chọn", exact: true })
      .click();
    await expect(board.getByRole("status")).toContainText("100%");
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    await page.screenshot({
      path: `../.tools/editorial-grade${row.grade}-${row.plan}-${device}.png`,
      fullPage: true,
    });
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
    const csrf = (await page.context().cookies()).find(
      (cookie) => cookie.name === "viettree_csrf",
    )!.value;
    for (const entry of catalog) {
      const response = await page.request.post(
        `/api/v1/ai-academy/lessons/${entry.id}/start`,
        {
          headers: {
            "X-CSRF-Token": csrf,
            Origin: process.env.E2E_BASE_URL || "http://localhost:3000",
          },
        },
      );
      expect(response.status(), entry.code).toBe(entry.locked ? 403 : 200);
      if (response.status() === 200) {
        const data = await response.json();
        for (const step of data.content.steps) {
          for (const q of step.questions) {
            expect(q).not.toHaveProperty("answer");
            expect(q).not.toHaveProperty("explanation");
          }
          if (step.activity)
            for (const item of step.activity.items)
              expect(item).not.toHaveProperty("answer");
        }
      }
    }
  });
}

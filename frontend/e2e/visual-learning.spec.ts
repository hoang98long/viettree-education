import { expect, test } from "@playwright/test";
import { login } from "./helpers";

test("minh họa VIP: màu đỏ đúng với nhãn ở lớp 1–3", async ({ page }, info) => {
  const username =
    process.env[`E2E_ACADEMY_${info.project.name.toUpperCase()}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần fixture VIP test riêng");
  await login(page, username!, password!);
  for (const [grade, code] of [
    [1, "AI1-08"],
    [2, "AI2-04"],
    [3, "AI3-08"],
  ] as const) {
    const catalog = await (
      await page.request.get(`/api/v1/ai-academy/catalog?grade=${grade}`)
    ).json();
    const lesson = catalog.find((row: { code: string }) => row.code === code);
    const [started] = await Promise.all([
      page.waitForResponse(
        (response) =>
          response.url().endsWith(`/lessons/${lesson.id}/start`) &&
          response.request().method() === "POST",
      ),
      page.goto(`/ai-academy/lessons/${lesson.id}`),
    ]);
    expect(started.status()).toBe(200);
    const data = await started.json();
    const card = data.content.steps[3].activity.items.find(
      (item: { text: string }) => item.text === "Cặp đỏ",
    );
    expect(card.asset).toContain("color-v3");
    const illustration = await page.request.get(
      `/api/v1/ai-academy/media/${card.asset}`,
    );
    expect(illustration.status()).toBe(200);
    expect(await illustration.text()).toContain('fill="#e87969"');
    for (let i = 0; i < 3; i++)
      await page
        .getByRole("button", { name: "Tiếp theo", exact: true })
        .click();
    const board = page.getByRole("region", { name: "Hoạt động tương tác" });
    await board.getByRole("button", { name: "Trái cây", exact: true }).click();
    await board.getByRole("button", { name: "Thẻ tiếp", exact: true }).click();
    await expect(
      board.getByRole("heading", { name: "Cặp đỏ", exact: true }),
    ).toBeVisible();
    await board.locator(".academy-focus-card").screenshot({
      path: `test-results/visual-red-grade${grade}-${info.project.name}.png`,
    });
  }
});

const activities: Record<number, string[]> = {
  1: ["Con người", "Máy"],
  2: ["Con vật", "Trái cây", "Con vật"],
  3: ["Rõ ràng", "Chưa rõ"],
  4: ["Có dùng AI", "Thiết bị thông thường", "Có dùng AI"],
  5: ["Nhãn phù hợp", "Cần sửa nhãn", "Nhãn phù hợp"],
};
const checkpoints: Record<number, string[]> = {
  1: ["Con người", "Máy", "Kiểm tra lại, nhờ cô giúp"],
  2: ["Con vật", "Con vật", "Kiểm tra lại, nhờ cô giúp"],
  3: ["Rõ ràng", "Chưa rõ", "Kiểm tra lại, nhờ cô giúp"],
  4: [
    "Nó làm theo lệnh bật/tắt đã định",
    "Ước đoán nhãn từ dữ liệu",
    "Câu được hệ thống tạo hoặc lập trình",
  ],
  5: ["Nhãn phù hợp", "Nhãn phù hợp", "Kiểm tra lại, nhờ cô giúp"],
};

test("năm khối: 36 bài, học bằng tranh/chạm, gợi ý không gõ, hoàn thành và ôn lại", async ({
  page,
}, info) => {
  test.setTimeout(240_000);
  const password = process.env.E2E_STUDENT_PASSWORD;
  const device = info.project.name.toUpperCase();
  test.skip(
    !password || !process.env[`E2E_VISUAL_GRADE1_${device}_USERNAME`],
    "Cần fixture riêng cho năm khối",
  );
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  for (const grade of [1, 2, 3, 4, 5]) {
    const username = process.env[`E2E_VISUAL_GRADE${grade}_${device}_USERNAME`];
    await login(page, username!, password!);
    await page.goto("/ai-academy");
    await expect(
      page.getByRole("heading", {
        name: `Lớp ${grade} · 36 bài · 9 chủ đề`,
        exact: true,
      }),
    ).toBeVisible();
    const catalog = await (
      await page.request.get(`/api/v1/ai-academy/catalog?grade=${grade}`)
    ).json();
    expect(catalog).toHaveLength(36);
    expect(
      catalog.filter((row: { locked: boolean }) => row.locked),
    ).toHaveLength(33);
    const lesson = catalog.find(
      (row: { code: string }) => row.code === `AI${grade}-01`,
    );
    await page.goto(`/ai-academy/lessons/${lesson.id}`);
    await expect(page.locator(".academy-scenes img").first()).toBeVisible();
    await expect
      .poll(() =>
        page
          .locator(".academy-scenes img")
          .first()
          .evaluate((image) => (image as HTMLImageElement).naturalWidth),
      )
      .toBeGreaterThan(0);
    expect(await page.locator(".academy-step textarea").count()).toBe(0);
    await page
      .getByRole("button", { name: "Em cần gợi ý", exact: true })
      .click();
    await expect(
      page.locator(".academy-help").getByRole("status"),
    ).toBeVisible();
    for (let i = 0; i < 3; i++)
      await page
        .getByRole("button", { name: "Tiếp theo", exact: true })
        .click();
    const board = page.getByRole("region", { name: "Hoạt động tương tác" });
    for (let i = 0; i < activities[grade].length; i++) {
      await expect(board.locator(".academy-focus-card")).toHaveCount(1);
      await expect(board.getByRole("img")).toBeVisible();
      const choice = board.getByRole("button", {
        name: activities[grade][i],
        exact: true,
      });
      expect((await choice.boundingBox())!.height).toBeGreaterThanOrEqual(48);
      await choice.click();
      if (i < activities[grade].length - 1)
        await board
          .getByRole("button", { name: "Thẻ tiếp", exact: true })
          .click();
    }
    await page.locator(".academy-step").screenshot({
      path: `test-results/visual-ai-grade${grade}-${info.project.name}.png`,
    });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    await board
      .getByRole("button", { name: "Kiểm tra lựa chọn", exact: true })
      .click();
    await expect(board.getByRole("status")).toContainText("100%");
    await page.reload();
    await expect(
      page.getByRole("button", { name: "Tiếp theo", exact: true }),
    ).toBeEnabled();
    await page.getByRole("button", { name: "Tiếp theo", exact: true }).click();
    for (let i = 0; i < checkpoints[grade].length; i++) {
      await expect(board.locator("fieldset")).toHaveCount(1);
      await board
        .getByRole("radio", { name: checkpoints[grade][i], exact: true })
        .check();
      if (i < checkpoints[grade].length - 1)
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
      page.getByRole("heading", {
        name: "Em đã khám phá xong bài này!",
        exact: true,
      }),
    ).toBeVisible();
    await page.reload();
    await expect(
      page.getByRole("heading", {
        name: "Em đã khám phá xong bài này!",
        exact: true,
      }),
    ).toBeVisible();
    await page.goto("/student/dashboard");
    await page
      .getByRole("button", { name: "Đăng xuất", exact: true })
      .first()
      .click();
    await expect(page).toHaveURL(/\/login$/);
  }
  expect(errors).toEqual([]);
});

test("bài học Toán: mở từng phần và minh họa các hàng của số", async ({
  page,
}, info) => {
  const password = process.env.E2E_STUDENT_PASSWORD;
  const username =
    process.env[
      `E2E_VISUAL_GRADE4_${info.project.name.toUpperCase()}_USERNAME`
    ];
  test.skip(!password || !username, "Cần học sinh lớp 4 test riêng");
  await login(page, username!, password!);
  await page.getByRole("link", { name: /Toán.*chủ đề/ }).click();
  await page.getByRole("link", { name: /Hàng, lớp và cách đọc số/ }).click();
  await expect(page.locator(".lesson-block[open]")).toHaveCount(1);
  await page.getByText("Thử với ví dụ", { exact: true }).click();
  await expect(page.getByLabel("Tách các hàng của số")).toBeVisible();
  await expect(
    page.getByLabel("Tách các hàng của số").locator("dd"),
  ).toHaveText(["3", "2", "5", "4", "1", "8"]);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await page.locator(".lesson-block.example").screenshot({
    path: `test-results/visual-core-place-value-${info.project.name}.png`,
  });
});

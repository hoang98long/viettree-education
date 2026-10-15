import { test, expect } from "@playwright/test";
import { login } from "./helpers";
import { baseURL, localTLS } from "./environment";

test("Bài đã lưu: bỏ thẻ cuối trang tự quay về trang còn dữ liệu", async ({
  page,
}, info) => {
  const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  const username = process.env[`E2E_EXPLORER_GRADE1_${suffix}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần fixture riêng trên database test");
  await login(page, username!, password!);
  const first = await (
    await page.request.get(
      "/api/v1/students/me/lesson-library?plan=free&page=1",
    )
  ).json();
  const second = await (
    await page.request.get(
      "/api/v1/students/me/lesson-library?plan=free&page=2",
    )
  ).json();
  const ids = [
    ...first.items.map((item: { id: string }) => item.id),
    second.items[0].id,
  ];
  const csrf = (await page.context().cookies()).find(
    (cookie) => cookie.name === "viettree_csrf",
  )!.value;
  const headers = { "X-CSRF-Token": csrf, Origin: baseURL };
  try {
    for (const id of ids)
      expect(
        (
          await page.request.put(`/api/v1/students/me/lessons/${id}/bookmark`, {
            headers,
            data: { saved: true },
          })
        ).status(),
      ).toBe(200);
    await page.goto("/student/saved-lessons");
    await expect(
      page.getByText("13 bài phù hợp", { exact: true }),
    ).toBeVisible();
    await page.setViewportSize({ width: 320, height: 900 });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    await page.getByRole("button", { name: "Trang sau", exact: true }).click();
    await expect(page.getByText("Trang 2/2", { exact: true })).toBeVisible();
    await expect(page.locator(".library-card")).toHaveCount(1);
    await page
      .locator(".library-card")
      .getByRole("button", { name: "Bỏ lưu bài học", exact: true })
      .click();
    await expect(page.getByText("Trang 1/1", { exact: true })).toBeVisible();
    await expect(page.locator(".library-card")).toHaveCount(12);
  } finally {
    for (const id of ids)
      await page.request.put(`/api/v1/students/me/lessons/${id}/bookmark`, {
        headers,
        data: { saved: false },
      });
  }
});

test("Free lớp 1: lỗi mạng, lưu bài và đồng bộ giữa hai phiên đăng nhập", async ({
  page,
  browser,
}, info) => {
  const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  const username = process.env[`E2E_EXPLORER_GRADE1_${suffix}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(
    !username || !password,
    "Cần fixture riêng và bộ explorers trên database test",
  );
  await login(page, username!, password!);
  await page.goto("/student/lessons");
  await page.getByLabel("Tên bài hoặc chủ đề").fill("thuoc ke ti hon");
  await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
  await expect(page.getByText("1 bài phù hợp", { exact: true })).toBeVisible();
  await page.getByRole("link", { name: /^(Mở bài học|Đọc tiếp)$/ }).click();
  await expect(page).toHaveURL(/\/student\/lessons\/[0-9a-f-]+$/);
  await expect(
    page.getByRole("heading", { name: "Thước kẻ tí hon", exact: true }),
  ).toBeVisible();
  const lessonPath = new URL(page.url()).pathname;
  const route = "**/api/v1/students/me/lessons/*/bookmark";
  await page.route(route, (request) => request.abort());
  await page.getByRole("button", { name: "Lưu bài học", exact: true }).click();
  await expect(
    page.locator(".lesson-bookmark").getByRole("alert"),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Lưu bài học", exact: true }),
  ).toHaveAttribute("aria-pressed", "false");
  await page.unroute(route);
  await page.getByRole("button", { name: "Lưu bài học", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Bỏ lưu bài học", exact: true }),
  ).toHaveAttribute("aria-pressed", "true");
  await page.reload();
  await expect(
    page.getByRole("button", { name: "Bỏ lưu bài học", exact: true }),
  ).toBeVisible();
  const second = await browser.newContext({
    baseURL,
    ignoreHTTPSErrors: localTLS,
    viewport: { width: 390, height: 844 },
  });
  try {
    const other = await second.newPage();
    await login(other, username!, password!);
    await other.goto("/student/saved-lessons");
    await expect(
      other.getByRole("heading", { name: "Bài học đã lưu", exact: true }),
    ).toBeVisible();
    await expect(other.locator(".library-card")).toHaveCount(1);
    await expect(other.locator(".library-card")).toContainText(
      "Thước kẻ tí hon",
    );
    for (const width of [320, 390, 768, 1280]) {
      await other.setViewportSize({ width, height: 900 });
      expect(
        await other.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
      ).toBe(true);
    }
    await other.setViewportSize({ width: 390, height: 844 });
    await other.screenshot({
      path: `../.tools/explorer-bookmarks-${suffix}.png`,
      fullPage: true,
    });
    await other
      .getByRole("button", { name: "Bỏ lưu bài học", exact: true })
      .click();
    await expect(other.locator(".library-card")).toHaveCount(0);
    await page.goto(lessonPath);
    await expect(
      page.getByRole("button", { name: "Lưu bài học", exact: true }),
    ).toHaveAttribute("aria-pressed", "false");
    for (const width of [320, 390, 768, 1280]) {
      await other.setViewportSize({ width, height: 900 });
      expect(
        await other.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
      ).toBe(true);
    }
  } finally {
    await second.close();
  }
});

test("VIP lớp 3: khung giấy, gợi ý và bốn đáp án được chấm đúng", async ({
  page,
}, info) => {
  const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  const username = process.env[`E2E_EXPLORER_GRADE3_${suffix}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần học sinh VIP test riêng");
  await login(page, username!, password!);
  await page.goto("/student/lessons");
  await page.getByLabel("Tên bài hoặc chủ đề").fill("khung giay co khe ho");
  await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
  await page.getByRole("link", { name: /^(Mở bài học|Đọc tiếp)$/ }).click();
  for (const hint of [1, 2, 3])
    await page
      .getByRole("button", { name: `Mở gợi ý ${hint}`, exact: true })
      .click();
  await page
    .getByRole("link", { name: "Thử thách: Khung giấy có khe hở", exact: true })
    .click();
  await page.getByRole("button", { name: "Bắt đầu / Tiếp tục" }).click();
  await page.getByRole("radio", { name: /40 cm$/ }).check();
  await page.getByRole("button", { name: "Câu tiếp", exact: true }).click();
  await page.getByLabel("Câu trả lời của em", { exact: true }).fill("38");
  await page.getByRole("button", { name: "Câu tiếp", exact: true }).click();
  await page.getByRole("radio", { name: /96 cm²$/ }).check();
  await page.getByRole("button", { name: "Câu tiếp", exact: true }).click();
  await page.getByRole("radio", { name: /35 cm$/ }).check();
  await page.getByRole("button", { name: "Xem lại", exact: true }).click();
  await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
  await page.getByRole("button", { name: "Xác nhận nộp", exact: true }).click();
  await expect(page).toHaveURL(/\/student\/results\//);
  const identifier = new URL(page.url()).pathname.split("/").pop();
  const result = await page.request.get(
    `/api/v1/attempts/${identifier}/result`,
  );
  expect(result.status()).toBe(200);
  expect((await result.json()).correct_count).toBe(4);
  await page.screenshot({
    path: `../.tools/explorer-grade3-result-${suffix}.png`,
    fullPage: true,
  });
});

test("VIP lớp 5: hộp chữ nhật minh họa đúng số đo và gợi ý", async ({
  page,
}, info) => {
  const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  const username = process.env[`E2E_EXPLORER_GRADE5_${suffix}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần học sinh VIP test riêng");
  await login(page, username!, password!);
  await page.goto("/student/lessons");
  await page
    .getByLabel("Tên bài hoặc chủ đề")
    .fill("hop qua va khoi lap phuong");
  await page.getByRole("button", { name: "Tìm bài", exact: true }).click();
  await page.getByRole("link", { name: /^(Mở bài học|Đọc tiếp)$/ }).click();
  await expect(
    page.getByRole("img", { name: /Hộp chữ nhật dài 5 cm/ }),
  ).toBeVisible();
  for (const hint of [1, 2, 3])
    await page
      .getByRole("button", { name: `Mở gợi ý ${hint}`, exact: true })
      .click();
  await expect(
    page.getByRole("button", { name: "Đã mở hết gợi ý", exact: true }),
  ).toBeDisabled();
  await page.screenshot({
    path: `../.tools/explorer-grade5-lesson-${suffix}.png`,
    fullPage: true,
  });
});

test("Admin: theo dõi hai bộ học liệu riêng cho năm khối", async ({ page }) => {
  const password = process.env.E2E_ADMIN_PASSWORD;
  test.skip(!password, "Cần admin test riêng");
  await login(page, "admin", password!);
  await page.goto("/admin/curriculum");
  for (const grade of [1, 2, 3, 4, 5]) {
    await page.getByLabel("Lớp học liệu").selectOption(String(grade));
    await expect(page.getByLabel("Học liệu khám phá bổ sung")).toContainText(
      "3/3 bài · 12/12 câu hỏi · 3/3 đề",
    );
    await expect(page.getByLabel("Học liệu tình huống bổ sung")).toContainText(
      "6/6 bài · 30/30 câu hỏi · 6/6 đề",
    );
  }
});

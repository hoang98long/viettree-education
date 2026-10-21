import { devices, expect, test, type Page } from "@playwright/test";
import { login } from "./helpers";
import { localTLS } from "./environment";

async function choose(page: Page, label: string) {
  const [response] = await Promise.all([
    page.waitForResponse(
      (r) =>
        r.url().endsWith("/students/me/accessibility") &&
        r.request().method() === "PUT",
    ),
    page.getByRole("button", { name: label, exact: true }).click(),
  ]);
  expect(response.status()).toBe(200);
  await expect(page.getByRole("status")).toHaveText("Đã lưu cỡ chữ cho em.");
  return response.json();
}

async function noOverflow(page: Page) {
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
}

test("cỡ chữ gọn: lưu, lỗi mạng, bài học, AI, màn hình nhỏ và đổi tài khoản", async ({
  page,
}, info) => {
  const username =
    process.env[`E2E_READING_${info.project.name.toUpperCase()}_USERNAME`];
  const other = process.env.E2E_READING_OTHER_USERNAME;
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(
    !username || !other || !password,
    "Cần tài khoản đọc riêng trên DB test",
  );
  await login(page, username!, password!);
  await page.getByRole("link", { name: "Cỡ chữ", exact: true }).click();
  await expect(
    page.getByRole("group", { name: "Cỡ chữ" }).getByRole("button"),
  ).toHaveCount(3);
  const device = info.project.name === "mobile" ? "phone" : "desktop";
  await expect(page.locator(".student")).toHaveAttribute(
    "data-device-type",
    device,
  );
  const saved = await choose(page, "Chữ gọn hơn");
  expect(saved.text_size).toBe("comfortable");
  expect(saved.text_size_by_device[device]).toBe("compact");
  await expect(page.locator(".student")).toHaveCSS("font-size", "16px");
  await expect(page.locator(".reading-preview")).toHaveCSS("font-size", "18px");
  for (const button of await page.locator(".text-size-choices button").all()) {
    expect((await button.boundingBox())!.height).toBeGreaterThanOrEqual(48);
  }
  await page.locator(".reading-settings").screenshot({
    path: `test-results/reading-compact-${info.project.name}.png`,
  });
  await page.reload();
  await expect(
    page.getByRole("button", { name: "Chữ gọn hơn", exact: true }),
  ).toHaveAttribute("aria-pressed", "true");
  await page.route("**/api/v1/students/me/accessibility", (route) =>
    route.fulfill({
      status: 503,
      contentType: "application/json",
      body: JSON.stringify({ detail: "Thử lại khi có mạng." }),
    }),
  );
  await page.getByRole("button", { name: "Chữ lớn hơn", exact: true }).click();
  await expect(page.locator(".reading-settings").getByRole("alert")).toHaveText(
    "Thử lại khi có mạng.",
  );
  await expect(page.locator(".student")).toHaveAttribute(
    "data-text-size",
    "compact",
  );
  await page.unroute("**/api/v1/students/me/accessibility");
  for (const width of [320, 390, 768, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    await noOverflow(page);
    await expect(page.locator(".student")).toHaveAttribute(
      "data-device-type",
      device,
    );
  }
  await page.setViewportSize({
    width: info.project.name === "mobile" ? 390 : 1280,
    height: 844,
  });
  await page
    .getByRole("link", { name: "Thư viện bài học", exact: true })
    .click();
  await expect(page.locator(".library-card").first()).toBeVisible();
  await noOverflow(page);
  await page
    .getByRole("link", { name: "Mở bài học", exact: true })
    .first()
    .click();
  await expect(page.locator(".lesson-block p").first()).toHaveCSS(
    "font-size",
    "18px",
  );
  await noOverflow(page);
  await page.screenshot({
    path: `test-results/reading-lesson-${info.project.name}.png`,
    fullPage: true,
  });
  const assessments = await (
    await page.request.get("/api/v1/assessments?grade=4&subject_code=MATH")
  ).json();
  const free = assessments.find((item: { locked: boolean }) => !item.locked);
  expect(free).toBeTruthy();
  await page.goto(`/student/assessments/${free.id}`);
  await page
    .getByRole("button", { name: "Bắt đầu / Tiếp tục", exact: true })
    .click();
  await expect(page.locator(".question-prompt")).toHaveCSS("font-size", "20px");
  await expect(page.locator(".option").first()).toHaveCSS("font-size", "16px");
  await noOverflow(page);
  await page.screenshot({
    path: `test-results/reading-quiz-${info.project.name}.png`,
    fullPage: true,
  });
  const attemptPath = new URL(page.url()).pathname;
  for (const [label, questionSize] of [
    ["Chữ vừa đủ lớn", "22px"],
    ["Chữ lớn hơn", "26px"],
    ["Chữ gọn hơn", "20px"],
  ]) {
    await page.goto("/student/profile");
    await choose(page, label);
    await page.goto(attemptPath);
    await expect(page.locator(".question-prompt")).toHaveCSS(
      "font-size",
      questionSize,
    );
    await noOverflow(page);
  }
  await page.goto("/ai-academy");
  await expect(page.locator(".academy-page")).toHaveAttribute(
    "data-text-size",
    "compact",
  );
  await expect(page.locator(".academy-page")).toHaveCSS("font-size", "18px");
  await noOverflow(page);
  await page.getByRole("link", { name: "Cỡ chữ", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Chữ gọn hơn", exact: true }),
  ).toHaveAttribute("aria-pressed", "true");
  await page
    .getByRole("button", { name: "Đăng xuất", exact: true })
    .first()
    .click();
  await expect(page).toHaveURL(/\/login$/);
  await login(page, username!, password!);
  await expect(page.locator(".student")).toHaveAttribute(
    "data-text-size",
    "compact",
  );
  await page
    .getByRole("button", { name: "Đăng xuất", exact: true })
    .first()
    .click();
  await expect(page).toHaveURL(/\/login$/);
  await login(page, other!, password!);
  await expect(page.locator(".student")).toHaveAttribute(
    "data-text-size",
    "comfortable",
  );
});

test("cùng tài khoản lưu ba cỡ riêng và đồng bộ tab", async ({
  page,
  browser,
}, info) => {
  test.skip(
    info.project.name !== "desktop",
    "Ba loại thiết bị được thử trong cùng một lượt",
  );
  const username = process.env.E2E_READING_DESKTOP_USERNAME;
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần tài khoản đọc riêng trên DB test");
  await login(page, username!, password!);
  await page.goto("/student/profile");
  await choose(page, "Chữ lớn hơn");
  const phoneContext = await browser.newContext({
    ignoreHTTPSErrors: localTLS,
    ...devices["iPhone 13"],
    baseURL: process.env.E2E_BASE_URL,
  });
  const tabletContext = await browser.newContext({
    ignoreHTTPSErrors: localTLS,
    ...devices["iPad (gen 7)"],
    baseURL: process.env.E2E_BASE_URL,
  });
  try {
    const phone = await phoneContext.newPage();
    const tablet = await tabletContext.newPage();
    await login(phone, username!, password!);
    await phone.goto("/student/profile");
    await expect(phone.locator(".student")).toHaveAttribute(
      "data-device-type",
      "phone",
    );
    await expect(phone.locator(".student")).toHaveAttribute(
      "data-text-size",
      "comfortable",
    );
    await choose(phone, "Chữ gọn hơn");
    await login(tablet, username!, password!);
    await tablet.goto("/student/profile");
    await expect(tablet.locator(".student")).toHaveAttribute(
      "data-device-type",
      "tablet",
    );
    await choose(tablet, "Chữ vừa đủ lớn");
    expect(
      (await (await tablet.request.get("/api/v1/auth/me")).json())
        .text_size_by_device,
    ).toEqual({
      phone: "compact",
      tablet: "comfortable",
      desktop: "large",
    });
    await page.reload();
    await phone.reload();
    await tablet.reload();
    await expect(page.locator(".student")).toHaveAttribute(
      "data-text-size",
      "large",
    );
    await expect(phone.locator(".student")).toHaveAttribute(
      "data-text-size",
      "compact",
    );
    await expect(tablet.locator(".student")).toHaveAttribute(
      "data-text-size",
      "comfortable",
    );
    await phone.setViewportSize({ width: 844, height: 390 });
    await expect(phone.locator(".student")).toHaveAttribute(
      "data-device-type",
      "phone",
    );
    await expect(phone.locator(".student")).toHaveAttribute(
      "data-text-size",
      "compact",
    );
    const secondTab = await page.context().newPage();
    await secondTab.goto("/student/profile");
    await expect(secondTab.locator(".student")).toHaveAttribute(
      "data-text-size",
      "large",
    );
    await choose(page, "Chữ gọn hơn");
    await expect(secondTab.locator(".student")).toHaveAttribute(
      "data-text-size",
      "compact",
    );
    await secondTab.close();
    await tablet.getByRole("link", { name: "Cỡ chữ", exact: true }).click();
    await noOverflow(tablet);
  } finally {
    await phoneContext.close();
    await tabletContext.close();
  }
});

import { expect, test } from "@playwright/test";
import { login } from "./helpers";

test("lớp 1: tranh trong thẻ từ và đáp án vẫn chọn và lưu được", async ({
  page,
}, info) => {
  const username =
    process.env[
      `E2E_VISUAL_GRADE1_${info.project.name.toUpperCase()}_USERNAME`
    ];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần học sinh test riêng");
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await login(page, username!, password!);
  const topics = await (
    await page.request.get("/api/v1/topics?grade=1&subject_code=ENGLISH")
  ).json();
  const topic = topics.find(
    (row: { code: string }) => row.code === "VT1-ENGLISH-school",
  );
  const lessons = await (
    await page.request.get(`/api/v1/lessons?topic_id=${topic.id}`)
  ).json();
  const lesson = lessons.find(
    (row: { title: string }) => row.title === "Book, pen, bag và ruler",
  );
  await page.goto(`/student/lessons/${lesson.id}`);
  const cards = page.locator(".early-word-cards");
  await expect(cards.locator(".word-picture")).toHaveCount(4);
  await expect(
    cards.locator('img[src="/learning/schoolbag.svg"]'),
  ).toBeVisible();
  const details = await (
    await page.request.get(`/api/v1/lessons/${lesson.id}`)
  ).json();
  await page.goto(`/student/assessments/${details.practice[0].id}`);
  await page
    .getByRole("button", { name: "Bắt đầu / Tiếp tục", exact: true })
    .click();
  await expect(page).toHaveURL(/\/student\/attempts\//);
  const options = page.locator(".options");
  await expect(options.locator(".word-picture").first()).toBeVisible();
  for (const image of await options.locator("img").all()) {
    expect(
      await image.evaluate(
        (node: HTMLImageElement) => node.complete && node.naturalWidth > 0,
      ),
    ).toBe(true);
  }
  const selected = options.getByRole("radio").first();
  const selectedName = await selected.locator("..").innerText();
  await selected.check();
  await page.getByRole("button", { name: "Lưu bài", exact: true }).click();
  await expect(page.getByRole("status")).toContainText("Đã lưu");
  await page.reload();
  await expect(options.getByRole("radio").first()).toBeChecked();
  await expect(options.getByRole("radio").first().locator("..")).toHaveText(
    selectedName,
    { useInnerText: true },
  );
  const initialViewport = page.viewportSize();
  for (const width of [320, 390, 768, 1280]) {
    await page.setViewportSize({ width, height: 850 });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    expect(
      (await selected.locator("..").boundingBox())!.height,
    ).toBeGreaterThanOrEqual(48);
  }
  if (initialViewport) await page.setViewportSize(initialViewport);
  await page.locator(".quiz").screenshot({
    path: `test-results/picture-choice-${info.project.name}.png`,
  });
  const catalog = await (
    await page.request.get("/api/v1/ai-academy/catalog?grade=1")
  ).json();
  const aiLesson = catalog.find(
    (row: { code: string }) => row.code === "AI1-02",
  );
  await page.goto(`/ai-academy/lessons/${aiLesson.id}`);
  const journey = page.getByRole("list", { name: "Hành trình bài AI" });
  await expect(journey.getByRole("listitem")).toHaveCount(7);
  await expect(journey.locator('[aria-current="step"]')).toContainText(
    "đang học",
  );
  await expect(
    journey.locator('[aria-current="step"] .journey-label'),
  ).toHaveText("1");
  await page.getByRole("button", { name: "Tiếp theo", exact: true }).click();
  await expect(
    journey.locator('[aria-current="step"] .journey-label'),
  ).toHaveText("2");
  await expect(journey.getByRole("listitem").first()).toContainText("đã xong");
  await page.getByRole("button", { name: "Em cần gợi ý", exact: true }).click();
  await expect(page.locator(".academy-help").getByRole("status")).toBeVisible();
  await page.getByRole("button", { name: "Quay lại", exact: true }).click();
  await expect(page.locator(".academy-help").getByRole("status")).toHaveCount(
    0,
  );
  await page
    .locator(".academy-main")
    .screenshot({ path: `test-results/ai-journey-${info.project.name}.png` });
  expect(errors).toEqual([]);
});

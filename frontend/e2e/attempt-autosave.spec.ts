import { expect, test } from "@playwright/test";
import { login } from "./helpers";

test("tự lưu: reload, lỗi mạng, phản hồi chậm và chuyển trang vẫn giữ đáp án mới", async ({
  page,
}, info) => {
  const password = process.env.E2E_STUDENT_PASSWORD;
  const username =
    process.env[
      `E2E_VISUAL_GRADE4_${info.project.name.toUpperCase()}_USERNAME`
    ];
  test.skip(!password || !username, "Cần fixture test riêng");
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await login(page, username!, password!);
  const csrf = (await page.context().cookies()).find(
    (cookie) => cookie.name === "viettree_csrf",
  )!.value;
  const assessments = await (
    await page.request.get("/api/v1/assessments?grade=4&subject_code=MATH")
  ).json();
  const assessment = assessments.find(
    (item: { code: string }) => item.code === "VT4-MATH-numbers-practice",
  );
  const assignment = await (
    await page.request.post(
      `/api/v1/students/me/assessments/${assessment.id}/assign-self`,
      { headers: { "X-CSRF-Token": csrf } },
    )
  ).json();
  const started = await page.request.post("/api/v1/attempts", {
    headers: { "X-CSRF-Token": csrf },
    data: { assignment_id: assignment.id },
  });
  expect(started.status()).toBe(200);
  const attempt = await started.json();
  await page.goto(`/student/attempts/${attempt.id}`);
  const data = await (
    await page.request.get(`/api/v1/attempts/${attempt.id}`)
  ).json();
  expect(data.server_time).toBeTruthy();
  const radios = page.getByRole("radio");
  await radios.nth(0).check();
  await expect(page.locator(".save-message")).toContainText("Đã lưu");
  await page.reload();
  await expect(radios.nth(0)).toBeChecked();

  const answers = "**/api/v1/attempts/*/answers/*";
  await page.route(answers, (route) => route.abort("internetdisconnected"));
  await radios.nth(1).check();
  await expect(page.locator(".quiz").getByRole("alert")).toContainText(
    "Chưa kết nối",
  );
  await expect(radios.nth(1)).toBeChecked();
  await expect(page.locator(".save-message")).toHaveText("Chưa lưu được");
  await page.unroute(answers);
  await page.evaluate(() => window.dispatchEvent(new Event("online")));
  await expect(page.locator(".save-message")).toContainText("Đã lưu");
  await page.reload();
  await expect(radios.nth(1)).toBeChecked();

  let release!: () => void;
  let received!: () => void;
  const held = new Promise<void>((resolve) => {
    release = resolve;
  });
  const incoming = new Promise<void>((resolve) => {
    received = resolve;
  });
  let first = true;
  await page.route(answers, async (route) => {
    if (!first) {
      await route.continue();
      return;
    }
    first = false;
    const response = await route.fetch();
    received();
    await held;
    await route.fulfill({ response });
  });
  await radios.nth(0).check();
  await incoming;
  await radios.nth(1).check();
  // Clicking a Next.js link must wait for the pending latest answer.
  await page.getByRole("link", { name: "Góc học tập", exact: true }).click();
  expect(page.url()).toContain(`/student/attempts/${attempt.id}`);
  release();
  await expect(page).toHaveURL(/\/student\/dashboard$/);
  await page.unroute(answers);
  const saved = await (
    await page.request.get(`/api/v1/attempts/${attempt.id}`)
  ).json();
  expect(saved.items[0].answer).toEqual({
    option_id: data.items[0].content.options[1].id,
  });
  await page.goto(`/student/attempts/${attempt.id}`);
  await expect(radios.nth(1)).toBeChecked();
  for (const width of [320, 390, 1280]) {
    await page.setViewportSize({ width, height: 850 });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
  }
  if (info.project.use.viewport)
    await page.setViewportSize(info.project.use.viewport);
  await page
    .locator(".quiz")
    .screenshot({ path: `test-results/autosave-${info.project.name}.png` });
  expect(errors).toEqual([]);
});

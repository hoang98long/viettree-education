import { expect, test } from "@playwright/test";
import { login } from "./helpers";

test("HTTPS: cookie bảo mật, API riêng tư và chống yêu cầu khác nguồn", async ({
  page,
}, info) => {
  const base = process.env.E2E_BASE_URL || "";
  const username =
    process.env[
      `E2E_VISUAL_GRADE3_${info.project.name.toUpperCase()}_USERNAME`
    ];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(
    !base.startsWith("https:") || !username || !password,
    "Cần HTTPS và fixture test riêng",
  );
  const picture = await page.request.get("/learning/cat.svg");
  expect(picture.status()).toBe(200);
  expect(picture.headers()["cache-control"]).toContain("public, max-age=3600");
  for (const resource of ["/ready", "/docs", "/openapi.json"])
    expect((await page.request.get(resource)).status()).toBe(404);
  await login(page, username!, password!);
  const cookies = await page.context().cookies();
  const session = cookies.find((cookie) => cookie.name === "viettree_session")!;
  expect(session.secure).toBe(true);
  expect(session.httpOnly).toBe(true);
  expect(session.sameSite).toBe("Lax");
  const csrf = cookies.find((cookie) => cookie.name === "viettree_csrf")!.value;
  expect(
    (
      await page.request.post("/api/v1/auth/logout", {
        headers: { Origin: "https://evil.invalid", "X-CSRF-Token": csrf },
      })
    ).status(),
  ).toBe(403);
  expect((await page.request.get("/api/v1/auth/me")).status()).toBe(200);
  expect((await page.request.post("/api/v1/auth/logout")).status()).toBe(403);
  expect(
    (
      await page.request.post("/api/v1/auth/logout", {
        headers: { "X-CSRF-Token": csrf, Origin: base },
      })
    ).status(),
  ).toBe(200);
  const anonymous = await page.request.get("/api/v1/auth/me");
  expect(anonymous.status()).toBe(401);
  expect(anonymous.headers()["cache-control"]).toContain("no-store");
});

test("mạng có thêm độ trễ: chuyển câu, tải lại và nộp vẫn giữ đáp án", async ({
  page,
}, info) => {
  const username =
    process.env[`E2E_READING_${info.project.name.toUpperCase()}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần fixture test riêng");
  await page.route("**/api/v1/**", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 250));
    await route.continue();
  });
  await login(page, username!, password!);
  const csrf = (await page.context().cookies()).find(
    (cookie) => cookie.name === "viettree_csrf",
  )!.value;
  const headers = { "X-CSRF-Token": csrf };
  const catalog = await (
    await page.request.get("/api/v1/assessments?grade=4&subject_code=MATH")
  ).json();
  const assessment = catalog.find(
    (item: { code: string }) => item.code === "VT4-MATH-operations-practice",
  );
  expect(assessment).toBeTruthy();
  const assignment = await (
    await page.request.post(
      `/api/v1/students/me/assessments/${assessment.id}/assign-self`,
      { headers },
    )
  ).json();
  const started = await page.request.post("/api/v1/attempts", {
    headers,
    data: { assignment_id: assignment.id },
  });
  expect(started.status()).toBe(200);
  const attempt = await started.json();
  await page.goto(`/student/attempts/${attempt.id}`);
  await page.getByRole("radio").first().check();
  await page.getByRole("button", { name: "Câu tiếp", exact: true }).click();
  await expect(page.locator(".quiz-header")).toContainText("Câu 2");
  await page.reload();
  await expect(page.getByRole("radio").first()).toBeChecked();
  await expect(page.locator(".quiz-header")).toContainText("1 câu đã trả lời");
  await page.getByRole("button", { name: "Xem lại trước khi nộp" }).click();
  await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
  await page.getByRole("button", { name: "Xác nhận nộp", exact: true }).click();
  await expect(page).toHaveURL(`/student/results/${attempt.id}`);
  const result = await (
    await page.request.get(`/api/v1/attempts/${attempt.id}/result`)
  ).json();
  expect(result.answered_count).toBe(1);
});

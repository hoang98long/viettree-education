import { localTLS } from "./environment";
import { test, expect } from "@playwright/test";
import { expectedSeedQuestions, login } from "./helpers";

test("lớp 3: ba môn, quản trị học liệu và gợi ý Free/VIP cấp rồi thu hồi", async ({
  page,
  browser,
}, info) => {
  const username =
    info.project.name === "mobile"
      ? process.env.E2E_GRADE3_MOBILE_USERNAME
      : process.env.E2E_GRADE3_USERNAME;
  const password = process.env.E2E_STUDENT_PASSWORD,
    adminPassword = process.env.E2E_ADMIN_PASSWORD;
  test.skip(
    !username || !password || !adminPassword,
    "Cần học sinh lớp 3 mới trong database test riêng",
  );
  await login(page, username!, password!);
  const me = await (await page.request.get("/api/v1/auth/me")).json();
  await page.goto("/student/grades");
  await expect(page.getByRole("button", { name: /Lớp 3/ })).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  for (const name of ["Toán", "Tiếng Việt", "Tiếng Anh"]) {
    await expect(
      page.getByRole("link", { name: new RegExp(`${name}.*chủ đề`) }),
    ).toBeVisible();
  }
  await page.getByRole("link", { name: /Toán.*chủ đề/ }).click();
  const topics = await (
    await page.request.get("/api/v1/topics?grade=3&subject_code=MATH")
  ).json();
  const topic = topics.find(
    (t: { code: string }) => t.code === "VT3-MATH-numbers",
  );
  const lessons = await (
    await page.request.get(`/api/v1/lessons?topic_id=${topic.id}`)
  ).json();
  const free = lessons.find(
    (l: { code: string }) => l.code === "VT3-MATH-numbers-lesson-1",
  );
  const path = `/student/lessons/${free.id}`;
  const apiPath = `/api/v1/lessons/${free.id}`;
  const freePayload = await (await page.request.get(apiPath)).json();
  expect(freePayload.content.hints).toHaveLength(1);
  expect(freePayload.hint_access.vip_locked).toBe(2);
  await page.goto(path);
  await expect(
    page.getByRole("heading", { name: "Đọc và viết số có bốn chữ số" }),
  ).toBeVisible();
  await expect(
    page.getByRole("link", { name: "Tìm hiểu gợi ý VIP" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Mở gợi ý 1" }).click();
  await expect(
    page.getByRole("button", { name: "Đã mở hết gợi ý" }),
  ).toBeDisabled();
  await expect(
    page.getByText(freePayload.content.hints[0], { exact: true }),
  ).toBeVisible();
  const adminContext = await browser.newContext({
    ignoreHTTPSErrors: localTLS,
    baseURL: info.project.use.baseURL,
  });
  const admin = await adminContext.newPage();
  try {
    await login(admin, "admin", adminPassword!);
    await admin.goto("/admin/curriculum");
    await admin.getByLabel("Lớp").selectOption("3");
    await expect(
      admin.getByRole("heading", { name: "Theo dõi học liệu lớp 3" }),
    ).toBeVisible();
    const map = await (
      await admin.request.get("/api/v1/admin/curriculum-map?grade=3")
    ).json();
    expect(map.rows).toHaveLength(21);
    expect(
      map.rows.reduce(
        (n: number, r: { questions: number }) => n + r.questions,
        0,
      ),
    ).toBe(expectedSeedQuestions(map));
    await admin.goto(`/admin/lessons/${free.id}/edit`);
    await expect(admin.getByLabel("Số gợi ý miễn phí")).toHaveValue("1");
    const csrf = (await adminContext.cookies()).find(
      (c) => c.name === "viettree_csrf",
    )!.value;
    const change = async (operation: "grant" | "revoke") => {
      const response = await admin.request.post(
        `/api/v1/admin/students/${me.id}/membership/${operation}`,
        {
          headers: {
            "X-CSRF-Token": csrf,
            "Idempotency-Key": crypto.randomUUID(),
          },
          data: {
            ...(operation === "grant" ? { duration_days: 30 } : {}),
            reason: "Kiểm thử phân bổ gợi ý lớp 3",
          },
        },
      );
      expect(response.status()).toBe(200);
    };
    await change("grant");
    await page.reload();
    const vipPayload = await (await page.request.get(apiPath)).json();
    expect(vipPayload.content.hints).toHaveLength(3);
    await expect(
      page.getByRole("link", { name: "Tìm hiểu gợi ý VIP" }),
    ).toHaveCount(0);
    for (let n = 0; n < 3; n++) {
      await page.getByRole("button", { name: `Mở gợi ý ${n + 1}` }).click();
      await expect(
        page.getByText(vipPayload.content.hints[n], { exact: true }),
      ).toBeVisible();
    }
    for (const width of [320, 768, 1280]) {
      await page.setViewportSize({ width, height: 800 });
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      ).toBe(true);
    }
    await page.screenshot({
      path: `test-results/grade3-${info.project.name}.png`,
      fullPage: true,
    });
    await change("revoke");
    await page.reload();
    const revoked = await (await page.request.get(apiPath)).json();
    expect(revoked.content.hints).toHaveLength(1);
    await expect(
      page.getByRole("link", { name: "Tìm hiểu gợi ý VIP" }),
    ).toBeVisible();
    for (const hint of vipPayload.content.hints.slice(1)) {
      expect(JSON.stringify(revoked)).not.toContain(hint);
      await expect(page.getByText(hint, { exact: true })).toHaveCount(0);
    }
  } finally {
    await adminContext.close();
  }
});

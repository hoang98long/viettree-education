import { test, expect } from "@playwright/test";
import { login } from "./helpers";

for (const grade of [1, 2]) {
  test(`Lớp ${grade}: ba môn, bài ngắn/minh họa, lưu bài và quyền gợi ý`, async ({
    page,
    browser,
  }, info) => {
    const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
    const username = process.env[`E2E_GRADE${grade}_${suffix}_USERNAME`];
    const password = process.env.E2E_STUDENT_PASSWORD,
      adminPassword = process.env.E2E_ADMIN_PASSWORD;
    test.skip(
      !username || !password || !adminPassword,
      "Cần fixture lớp 1–2 trên DB test riêng",
    );
    await login(page, username!, password!);
    const me = await (await page.request.get("/api/v1/auth/me")).json();
    await page.goto("/student/grades");
    await expect(
      page.getByRole("button", { name: new RegExp(`Lớp ${grade}`) }),
    ).toHaveAttribute("aria-pressed", "true");
    for (const subject of ["Toán", "Tiếng Việt", "Tiếng Anh"])
      await expect(
        page.getByRole("link", { name: new RegExp(`${subject}.*chủ đề`) }),
      ).toBeVisible();
    const topics = await (
      await page.request.get(`/api/v1/topics?grade=${grade}&subject_code=MATH`)
    ).json();
    const topic = topics.find(
      (t: { code: string }) => t.code === `VT${grade}-MATH-numbers`,
    );
    const lessons = await (
      await page.request.get(`/api/v1/lessons?topic_id=${topic.id}`)
    ).json();
    const lesson = lessons.find(
      (l: { code: string }) => l.code === `VT${grade}-MATH-numbers-lesson-1`,
    );
    const path = `/student/lessons/${lesson.id}`,
      apiPath = `/api/v1/lessons/${lesson.id}`;
    await page.goto(path);
    await expect(
      page.getByRole("heading", { name: lesson.title, exact: true }),
    ).toBeVisible();
    const payload = await (await page.request.get(apiPath)).json();
    expect(payload.estimated_minutes).toBe(grade === 1 ? 6 : 8);
    expect(payload.content.hints).toHaveLength(1);
    if (grade === 1)
      await expect(
        page.getByRole("img", { name: /Có 3 chấm tròn/ }),
      ).toBeVisible();
    await page.getByRole("button", { name: "Mở gợi ý 1", exact: true }).click();
    await expect(
      page.getByRole("button", { name: "Đã mở hết gợi ý", exact: true }),
    ).toBeDisabled();
    await page
      .getByRole("button", { name: "Em đã đọc xong", exact: true })
      .click();
    await expect(
      page.getByRole("button", { name: "Đã đánh dấu đọc xong", exact: true }),
    ).toBeDisabled();
    await page.reload();
    await expect(
      page.getByRole("button", { name: "Đã đánh dấu đọc xong", exact: true }),
    ).toBeDisabled();
    await page.screenshot({
      path: `test-results/grade-${grade}-${suffix}.png`,
      fullPage: true,
    });
    const assessments = await (
      await page.request.get(
        `/api/v1/assessments?grade=${grade}&subject_code=MATH`,
      )
    ).json();
    const free = assessments.find(
      (a: { minimum_plan_code: string }) => a.minimum_plan_code === "free",
    );
    await page.goto(`/student/assessments/${free.id}`);
    await page
      .getByRole("button", { name: "Bắt đầu / Tiếp tục", exact: true })
      .click();
    await expect(page).toHaveURL(/\/student\/attempts\//);
    await page.getByRole("radio").first().check();
    await page.getByRole("button", { name: "Lưu bài", exact: true }).click();
    await expect(
      page.getByText("Đã lưu câu trả lời. Em có thể quay lại bài này.", {
        exact: true,
      }),
    ).toBeVisible();
    await page.reload();
    await expect(page.getByRole("radio").first()).toBeChecked();
    await page
      .getByRole("button", { name: "Xem lại trước khi nộp", exact: true })
      .click();
    await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
    await page
      .getByRole("button", { name: "Xác nhận nộp", exact: true })
      .click();
    await expect(page).toHaveURL(/\/student\/results\//);
    const adminContext = await browser.newContext({
      baseURL: process.env.E2E_BASE_URL,
    });
    const admin = await adminContext.newPage();
    try {
      await login(admin, "admin", adminPassword!);
      await admin.goto("/admin/curriculum");
      await admin
        .getByRole("combobox", { name: "Lớp học liệu", exact: true })
        .selectOption(String(grade));
      await expect(
        admin.getByRole("heading", {
          name: `Theo dõi học liệu lớp ${grade}`,
          exact: true,
        }),
      ).toBeVisible();
      await expect(
        admin.getByRole("heading", { name: /^Theo dõi học liệu lớp/ }),
      ).toHaveCount(1);
      const map = await (
        await admin.request.get(`/api/v1/admin/curriculum-map?grade=${grade}`)
      ).json();
      expect(map.rows).toHaveLength(21);
      expect(
        map.rows.reduce(
          (n: number, r: { questions: number }) => n + r.questions,
          0,
        ),
      ).toBe(384);
      const token = (await adminContext.cookies()).find(
        (c) => c.name === "viettree_csrf",
      )!.value;
      const change = async (operation: "grant" | "revoke") => {
        const response = await admin.request.post(
          `/api/v1/admin/students/${me.id}/membership/${operation}`,
          {
            headers: {
              "X-CSRF-Token": token,
              "Idempotency-Key": crypto.randomUUID(),
            },
            data: {
              ...(operation === "grant" ? { duration_days: 30 } : {}),
              reason: `Kiểm thử gợi ý lớp ${grade}`,
            },
          },
        );
        expect(response.status()).toBe(200);
      };
      await change("grant");
      await page.goto(path);
      const full = await (await page.request.get(apiPath)).json();
      expect(full.content.hints).toHaveLength(3);
      for (let i = 1; i <= 3; i++) {
        await page
          .getByRole("button", { name: `Mở gợi ý ${i}`, exact: true })
          .click();
        await expect(
          page.getByText(full.content.hints[i - 1], { exact: true }),
        ).toBeVisible();
      }
      await change("revoke");
      await page.reload();
      expect(
        (await (await page.request.get(apiPath)).json()).content.hints,
      ).toHaveLength(1);
      for (const hint of full.content.hints.slice(1))
        await expect(page.getByText(hint, { exact: true })).toHaveCount(0);
      const englishTopics = await (
        await page.request.get(
          `/api/v1/topics?grade=${grade}&subject_code=ENGLISH`,
        )
      ).json();
      const school = englishTopics.find(
        (t: { code: string }) => t.code === `VT${grade}-ENGLISH-school`,
      );
      const english = await (
        await page.request.get(`/api/v1/lessons?topic_id=${school.id}`)
      ).json();
      const englishLesson = english.find(
        (l: { minimum_plan_code: string }) => l.minimum_plan_code === "free",
      );
      await page.goto(`/student/lessons/${englishLesson.id}`);
      await expect(
        page.getByRole("img", { name: /Thẻ từ minh họa/ }),
      ).toBeVisible();
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      ).toBe(true);
    } finally {
      await adminContext.close();
    }
  });
}

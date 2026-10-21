import { expect, test } from "@playwright/test";
import { login } from "./helpers";

for (const grade of [1, 5]) {
  for (const plan of ["FREE", "VIP"]) {
    test(`lớp ${grade} ${plan}: đọc đủ ngữ liệu, câu hỏi ngắn và lưu trên điện thoại`, async ({
      page,
    }, info) => {
      const username =
        process.env[
          `E2E_REVIEW_GRADE${grade}_${plan}_${info.project.name.toUpperCase()}_USERNAME`
        ];
      const password = process.env.E2E_STUDENT_PASSWORD;
      test.skip(!username || !password, "Cần fixture riêng trên database test");
      await login(page, username!, password!);
      const csrf = (await page.context().cookies()).find(
        (c) => c.name === "viettree_csrf",
      )!.value;
      const code =
        grade === 1
          ? plan === "FREE"
            ? "reading"
            : "g1-rain"
          : plan === "FREE"
            ? "reading"
            : "g5-evidence-inference";
      const catalog = await (
        await page.request.get(
          `/api/v1/assessments?grade=${grade}&subject_code=VIETNAMESE`,
        )
      ).json();
      const assessment = catalog.find(
        (a: { code: string }) =>
          a.code === `VT${grade}-VIETNAMESE-${code}-practice`,
      );
      expect(assessment).toBeTruthy();
      const assigned = await page.request.post(
        `/api/v1/students/me/assessments/${assessment.id}/assign-self`,
        {
          headers: { "X-CSRF-Token": csrf },
        },
      );
      expect(assigned.status()).toBe(200);
      const started = await page.request.post("/api/v1/attempts", {
        headers: { "X-CSRF-Token": csrf },
        data: { assignment_id: (await assigned.json()).id },
      });
      expect(started.status()).toBe(200);
      const attemptId = (await started.json()).id;
      const response = await page.request.get(`/api/v1/attempts/${attemptId}`);
      const data = await response.json();
      expect(data.grade).toBe(grade);
      expect(await response.text()).not.toMatch(
        /correct_option_id|accepted_answers|"grading"/,
      );
      const authored = data.items[0].content.prompt as string;
      const boundary = authored.lastIndexOf("\n\n");
      expect(boundary).toBeGreaterThan(0);
      const passage = authored
        .slice(0, boundary)
        .replace(/^Ngữ liệu của bài:\s*\n/u, "");
      await page.goto(`/student/attempts/${attemptId}`);
      await expect(page.locator(".question-prompt")).toHaveText(
        authored.slice(boundary + 2),
      );
      const reading = page.locator(".question-reading");
      await expect(reading).toBeVisible();
      const full = reading.getByRole("button", {
        name: "Xem cả phần",
        exact: true,
      });
      if (await full.count()) await full.click();
      await expect(reading.locator(".reading-paragraph")).toHaveText(passage);
      await expect(reading.locator("img")).toHaveCount(0);
      const radios = page.getByRole("radio");
      const selected = (await radios.first().isChecked())
        ? radios.nth(1)
        : radios.first();
      await selected.check();
      await expect(page.locator(".save-message")).toContainText("Đã lưu");
      for (const width of [320, 390, 1280]) {
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
      await page.reload();
      await expect(page.locator(".question-prompt")).toHaveText(
        authored.slice(boundary + 2),
        { timeout: 15000 },
      );
      await expect(selected).toBeChecked();
      await expect(reading).toBeVisible();
      if (info.project.use.viewport)
        await page.setViewportSize(info.project.use.viewport);
      await page.locator(".quiz").screenshot({
        path: `test-results/question-reading-g${grade}-${plan}-${info.project.name}.png`,
      });
      await page.getByRole("button", { name: "Xem lại trước khi nộp" }).click();
      await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
      await page
        .getByRole("button", { name: "Xác nhận nộp", exact: true })
        .click();
      await expect(page).toHaveURL(`/student/results/${attemptId}`);
      const result = await (
        await page.request.get(`/api/v1/attempts/${attemptId}/result`)
      ).json();
      expect(result.grade).toBe(grade);
      expect(result.answered_count).toBe(1);
      const firstReview = page.locator(".result-item").first();
      if (
        !(await firstReview.evaluate(
          (node) => (node as HTMLDetailsElement).open,
        ))
      )
        await firstReview.locator(":scope > summary").click();
      await expect(firstReview.getByRole("heading", { level: 3 })).toHaveText(
        authored.slice(boundary + 2),
      );
      await expect(
        firstReview.getByText("Đáp án đúng:", { exact: true }),
      ).toBeVisible();
      await expect(firstReview.locator(".question-reading")).toBeVisible();
      await expect(firstReview.locator(".explanation")).toContainText(
        "Cùng hiểu cách làm",
      );
      for (const width of [320, 390, 1280]) {
        await page.setViewportSize({ width, height: 850 });
        expect(
          await page.evaluate(
            () => document.documentElement.scrollWidth <= window.innerWidth,
          ),
        ).toBe(true);
      }
    });
  }
}

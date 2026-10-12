import { test, expect, type Page, type BrowserContext } from "@playwright/test";
import { login } from "./helpers";

async function csrf(context: BrowserContext) {
  return (
    (await context.cookies()).find((c) => c.name === "viettree_csrf")?.value ||
    ""
  );
}
async function staffLogin(page: Page, username: string, password: string) {
  await page.goto("/login");
  await page.getByLabel("Tên đăng nhập", { exact: true }).fill(username);
  await page.getByLabel("Mật khẩu", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Vào học thôi", exact: true }).click();
  await expect(page).toHaveURL(/\/teacher\/dashboard$/);
}

test("AI Free/VIP và bảng giá: cấp rồi thu hồi chặn bài đã mở", async ({
  page,
  browser,
}, info) => {
  const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  const username = process.env[`E2E_CLASS_${suffix}_FREE_USERNAME`],
    password = process.env.E2E_STUDENT_PASSWORD,
    adminPassword = process.env.E2E_ADMIN_PASSWORD;
  test.skip(!username || !password || !adminPassword, "Cần fixture test riêng");
  await login(page, username!, password!);
  const me = await (await page.request.get("/api/v1/auth/me")).json();
  const catalog = await (
    await page.request.get("/api/v1/ai-academy/catalog?grade=4")
  ).json();
  expect(catalog.filter((r: { locked: boolean }) => !r.locked)).toHaveLength(3);
  const lesson = catalog.find((r: { code: string }) => r.code === "AI4-02");
  await page.goto(`/ai-academy/lessons/${lesson.id}`);
  await expect(
    page.getByRole("heading", {
      name: "Cùng khám phá thêm với VIP",
      exact: true,
    }),
  ).toBeVisible();
  await page.goto("/student/membership");
  await expect(
    page.getByRole("heading", {
      name: "Tham khảo gói VIP cùng phụ huynh",
      exact: true,
    }),
  ).toBeVisible();
  const prices = await (
    await page.request.get("/api/v1/membership/prices")
  ).json();
  await expect(
    page.getByRole("heading", {
      name: new RegExp(
        prices.offers[0].effective_price_vnd
          .toLocaleString("vi-VN")
          .replace(/\./g, "\\."),
      ),
    }),
  ).toBeVisible();
  const admin = await browser.newContext({
    baseURL: process.env.E2E_BASE_URL,
    viewport: page.viewportSize()!,
  });
  const adminPage = await admin.newPage();
  await login(adminPage, "admin", adminPassword!);
  const token = await csrf(admin);
  const path = `/api/v1/admin/students/${me.id}/membership`;
  const grant = await admin.request.post(path + "/grant", {
    data: { duration_days: 30, reason: "E2E kiểm tra mở quyền đào tạo VIP" },
    headers: { "X-CSRF-Token": token, "Idempotency-Key": crypto.randomUUID() },
  });
  expect(grant.status()).toBe(200);
  await page.goto(`/ai-academy/lessons/${lesson.id}`);
  await expect(
    page.getByRole("heading", { name: lesson.title, exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Lưu và tiếp tục", exact: true })
    .click();
  const revoked = await admin.request.post(path + "/revoke", {
    data: { reason: "E2E thu hồi khi học sinh đang trong bài" },
    headers: { "X-CSRF-Token": token, "Idempotency-Key": crypto.randomUUID() },
  });
  expect(revoked.status()).toBe(200);
  await page
    .getByRole("button", { name: "Lưu và tiếp tục", exact: true })
    .click();
  await expect(
    page.getByRole("heading", {
      name: "Cùng khám phá thêm với VIP",
      exact: true,
    }),
  ).toBeVisible();
  await page.goto("/ai-academy/creative-studio");
  await expect(
    page.getByRole("heading", {
      name: "Cùng khám phá thêm với VIP",
      exact: true,
    }),
  ).toBeVisible();
  await page.goto("/student/classroom");
  await expect(
    page.getByRole("heading", {
      name: "Kết quả tháng này theo từng loại",
      exact: true,
    }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  await admin.close();
});

test("Lớp học: tạo, ghi danh, giao cả lớp/cá nhân và tuyên dương top 3", async ({
  page,
  browser,
}, info) => {
  const suffix = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  const usernames = ["FREE", "SECOND", "THIRD"].map(
    (s) => process.env[`E2E_CLASS_${suffix}_${s}_USERNAME`],
  );
  const password = process.env.E2E_STUDENT_PASSWORD,
    adminPassword = process.env.E2E_ADMIN_PASSWORD,
    teacher = process.env.E2E_ACADEMY_TEACHER_USERNAME;
  test.skip(
    usernames.some((u) => !u) || !password || !adminPassword || !teacher,
    "Cần fixture lớp test riêng",
  );
  await login(page, "admin", adminPassword!);
  await page.goto("/admin/classes");
  const create = page
    .locator("details")
    .filter({ has: page.getByText("Tạo lớp quản lý mới", { exact: true }) });
  await create.locator("summary").click();
  const name = `Lớp thành tích ${suffix} ${Date.now()}`;
  await create.getByLabel("Tên lớp quản lý", { exact: true }).fill(name);
  await create
    .getByRole("searchbox", { name: "Tìm Giáo viên của lớp", exact: true })
    .fill(teacher!);
  const teacherRow = await (
    await page.request.get(
      `/api/v1/admin/accounts?role=teacher&search=${teacher}`,
    )
  ).json();
  await create
    .getByRole("combobox", { name: "Giáo viên của lớp", exact: true })
    .selectOption(teacherRow.items[0].id);
  await create
    .getByRole("button", { name: "Tạo lớp quản lý", exact: true })
    .click();
  await expect
    .poll(async () =>
      (await (await page.request.get("/api/v1/classroom/classes")).json()).some(
        (c: { name: string }) => c.name === name,
      ),
    )
    .toBe(true);
  const classroom = (
    await (await page.request.get("/api/v1/classroom/classes")).json()
  ).find((c: { name: string }) => c.name === name);
  await page
    .getByRole("combobox", { name: "Chọn lớp quản lý", exact: true })
    .selectOption(classroom.id);
  const roster = page.locator("section").filter({
    has: page.getByRole("heading", {
      name: `Học sinh trong lớp · ${name}`,
      exact: true,
    }),
  });
  await expect(roster).toBeVisible();
  await expect(
    page.getByRole("heading", { name: /^Học sinh trong lớp ·/ }),
  ).toHaveCount(1);
  const students = [];
  for (const username of usernames) {
    const data = await (
      await page.request.get(
        `/api/v1/admin/accounts?role=student&grade=4&search=${username}`,
      )
    ).json();
    students.push(data.items[0]);
    await roster
      .getByRole("searchbox", { name: "Tìm Học sinh để ghi danh", exact: true })
      .fill(username!);
    await roster
      .getByRole("combobox", { name: "Học sinh để ghi danh", exact: true })
      .selectOption(data.items[0].id);
    await roster
      .getByRole("button", { name: "Ghi danh vào lớp", exact: true })
      .click();
    await expect
      .poll(
        async () =>
          (
            await (
              await page.request.get(
                `/api/v1/classroom/students?class_id=${classroom.id}&grade=4`,
              )
            ).json()
          ).total,
      )
      .toBe(students.length);
  }
  await page
    .getByRole("combobox", { name: "Loại bài giao", exact: true })
    .selectOption("ai_lesson");
  const catalog = await (
    await page.request.get("/api/v1/ai-academy/catalog?grade=4")
  ).json();
  const lesson = catalog.find((l: { code: string }) => l.code === "AI4-01");
  await page
    .getByRole("combobox", { name: "Chọn nội dung giao", exact: true })
    .selectOption(lesson.id);
  await page
    .getByRole("button", { name: "Giao bài đã chọn", exact: true })
    .click();
  await expect(
    page.getByRole("status").filter({ hasText: "Đã giao cho 3 học sinh" }),
  ).toBeVisible();
  await page
    .getByRole("combobox", { name: "Đối tượng giao bài", exact: true })
    .selectOption("individual");
  await page
    .getByRole("searchbox", {
      name: "Tìm Học sinh nhận bài riêng",
      exact: true,
    })
    .fill(usernames[0]!);
  await page
    .getByRole("combobox", { name: "Học sinh nhận bài riêng", exact: true })
    .selectOption(students[0].id);
  await page
    .getByRole("button", { name: "Giao bài đã chọn", exact: true })
    .click();
  await expect(
    page.getByRole("status").filter({ hasText: "Đã giao cho 1 học sinh" }),
  ).toBeVisible();
  for (let i = 0; i < usernames.length; i++) {
    const context = await browser.newContext({
      baseURL: process.env.E2E_BASE_URL,
    });
    expect(
      (
        await context.request.post("/api/v1/auth/login", {
          data: { username: usernames[i], password },
        })
      ).status(),
    ).toBe(200);
    const headers = { "X-CSRF-Token": await csrf(context) };
    const root = `/api/v1/ai-academy/lessons/${lesson.id}`;
    const started = await context.request.post(root + "/start", { headers });
    expect(started.status()).toBe(200);
    const body = (await started.json()).content;
    for (const step_id of ["story", "discover", "observe"])
      expect(
        (
          await context.request.post(root + "/steps", {
            headers,
            data: { step_id },
          })
        ).status(),
      ).toBe(200);
    expect(
      (
        await context.request.post(root + "/attempts", {
          headers,
          data: {
            step_id: "practice",
            level: 2,
            idempotency_key: crypto.randomUUID(),
            answers: {
              "item-1": "Có dùng AI",
              "item-2": "Thiết bị thông thường",
              "item-3": "Có dùng AI",
            },
          },
        })
      ).status(),
    ).toBe(200);
    expect(
      (
        await context.request.post(root + "/steps", {
          headers,
          data: { step_id: "practice" },
        })
      ).status(),
    ).toBe(200);
    const correct = [
      "Nó làm theo lệnh bật/tắt đã định",
      "Ước đoán nhãn từ dữ liệu",
      "Câu được hệ thống tạo hoặc lập trình",
    ];
    const answers: Record<string, string> = {};
    body.steps[4].questions.forEach(
      (q: { id: string; options: string[] }, n: number) => {
        const index = q.options.indexOf(correct[n]);
        answers[q.id] = String(n >= 3 - i ? 1 - index : index);
      },
    );
    const graded = await context.request.post(root + "/attempts", {
      headers,
      data: {
        step_id: "checkpoint",
        level: 2,
        idempotency_key: crypto.randomUUID(),
        answers,
      },
    });
    expect(graded.status()).toBe(200);
    await context.close();
  }
  await page
    .getByRole("button", { name: "Đăng xuất", exact: true })
    .first()
    .click();
  await staffLogin(page, teacher!, password!);
  await page.goto("/teacher/classes");
  await page
    .getByRole("combobox", { name: "Chọn lớp quản lý", exact: true })
    .selectOption(classroom.id);
  await page
    .getByRole("combobox", { name: "Loại kết quả", exact: true })
    .selectOption("AI");
  await expect(page.getByRole("heading", { name: /^Top [123] ·/ })).toHaveCount(
    3,
  );
  await page
    .getByRole("button", { name: "Tuyên dương top 3 của kỳ", exact: true })
    .click();
  await expect(
    page.getByRole("status").filter({ hasText: "Đã ghi nhận top đầu" }),
  ).toBeVisible();
  await page.screenshot({
    path: `test-results/class-top-three-${suffix}.png`,
    fullPage: true,
  });
  await page
    .getByRole("button", { name: "Đăng xuất", exact: true })
    .first()
    .click();
  await login(page, usernames[0]!, password!);
  await page.goto("/student/classroom");
  await page
    .getByRole("combobox", { name: "Loại kết quả", exact: true })
    .selectOption("AI");
  await expect(
    page.getByRole("heading", { name: /^Top 1 · Em/ }),
  ).toBeVisible();
  await expect(page.getByText(usernames[1]!, { exact: true })).toHaveCount(0);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
});

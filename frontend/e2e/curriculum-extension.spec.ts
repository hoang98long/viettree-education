import { test, expect } from "@playwright/test";
import { login } from "./helpers";

test("lớp 4: bài mới, biểu đồ/góc, Góc tư duy Free/VIP và bảng học liệu admin", async ({
  page,
  browser,
}, info) => {
  const username =
    info.project.name === "mobile"
      ? process.env.E2E_CURRICULUM_MOBILE_USERNAME
      : process.env.E2E_CURRICULUM_USERNAME;
  const password = process.env.E2E_STUDENT_PASSWORD,
    adminPassword = process.env.E2E_ADMIN_PASSWORD;
  test.skip(
    !username || !password || !adminPassword,
    "Cần tài khoản mới trong database test riêng",
  );
  await login(page, username!, password!);
  const me = await (await page.request.get("/api/v1/auth/me")).json();
  await page.goto("/student/thinking");
  await expect(
    page.getByRole("heading", { name: "Góc tư duy và đố mẹo" }),
  ).toBeVisible();
  const free = page.locator("article").filter({
    has: page.getByRole("heading", {
      name: "Đố mẹo: đếm khoảng, không chỉ đếm điểm",
    }),
  });
  const vip = page.locator("article").filter({
    has: page.getByRole("heading", {
      name: "Nâng cao: loại trừ và kiểm tra đủ điều kiện",
    }),
  });
  await expect(vip.getByRole("link", { name: "Xem gói học" })).toBeVisible();
  const catalog = await (
    await page.request.get("/api/v1/students/me/thinking")
  ).json();
  const locked = catalog.items.find(
    (item: { title: string }) =>
      item.title === "Nâng cao: loại trừ và kiểm tra đủ điều kiện",
  );
  expect(
    (await page.request.get(`/api/v1/lessons/${locked.id}`)).status(),
  ).toBe(403);
  await free.getByRole("link", { name: "Khám phá bài" }).click();
  await expect(
    page.getByRole("heading", {
      name: "Đố mẹo: đếm khoảng, không chỉ đếm điểm",
    }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Mở gợi ý 1" }).click();
  await expect(
    page.getByText("Vẽ ít nhất ba mốc liên tiếp.", { exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Em đã đọc xong", exact: true })
    .click();
  await page.goto("/student/thinking");
  await expect(
    page.locator("article").filter({ hasText: "Đố mẹo: đếm khoảng" }),
  ).toContainText("Đã đọc xong");
  for (const [topicCode, caption] of [
    ["geometry", "Góc 120°: lớn hơn góc vuông 90° và nhỏ hơn góc bẹt 180°."],
    [
      "statistics",
      "Số cây ba tổ trồng: 12, 16, 20 cây. Mỗi vạch của trục đứng ứng với 4 cây.",
    ],
  ]) {
    const topics = await (
      await page.request.get("/api/v1/topics?grade=4&subject_code=MATH")
    ).json();
    const topic = topics.find(
      (t: { code: string }) => t.code === `VT4-MATH-${topicCode}`,
    );
    const lessons = await (
      await page.request.get(`/api/v1/lessons?topic_id=${topic.id}`)
    ).json();
    await page.goto(`/student/lessons/${lessons[0].id}`);
    await expect(page.getByRole("img", { name: caption })).toBeVisible();
    for (const width of [320, 768, 1280]) {
      await page.setViewportSize({ width, height: 800 });
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      ).toBe(true);
    }
  }
  const adminContext = await browser.newContext({
    baseURL: info.project.use.baseURL,
  });
  const admin = await adminContext.newPage();
  try {
    await login(admin, "admin", adminPassword!);
    await admin.goto("/admin/curriculum");
    await expect(
      admin.getByRole("heading", { name: "Theo dõi học liệu lớp 4" }),
    ).toBeVisible();
    await admin.getByLabel("Chỉ mạch chưa có bài miễn phí khả dụng").check();
    await expect(
      admin.getByRole("row").filter({ hasText: "Nghe và phát âm" }),
    ).toContainText("Chưa có chủ đề hoạt động");
    const csrf = (await adminContext.cookies()).find(
      (c) => c.name === "viettree_csrf",
    )!.value;
    const response = await admin.request.post(
      `/api/v1/admin/students/${me.id}/membership/grant`,
      {
        headers: {
          "X-CSRF-Token": csrf,
          "Idempotency-Key": crypto.randomUUID(),
        },
        data: { duration_days: 30, reason: "Kiểm thử bài tư duy nâng cao" },
      },
    );
    expect(response.status()).toBe(200);
    await page.goto("/student/thinking");
    await page
      .getByRole("combobox", { name: "Môn học", exact: true })
      .selectOption("MATH");
    const vipCard = page
      .locator("article")
      .filter({ hasText: "Nâng cao: loại trừ" });
    await vipCard.getByRole("link", { name: "Khám phá bài" }).click();
    await expect(
      page.getByRole("heading", { name: "Em ghi nhớ" }),
    ).toBeVisible();
    // Verify the new category and both illustrations survive the editor round trip.
    await admin.goto(`/admin/lessons/${locked.id}/edit`);
    await expect(admin.getByLabel("Nhóm bài học")).toHaveValue("thinking");
    await admin
      .getByRole("combobox", { name: "Chọn minh họa" })
      .selectOption("bars");
    await admin
      .getByLabel("Chú thích hình (nêu rõ ý nghĩa và số liệu)")
      .fill("Biểu đồ xem trước của ba nhóm");
    await admin.getByLabel("Giá trị cột 1").fill("8");
    await admin
      .getByRole("button", { name: "Xem trước bài học", exact: true })
      .click();
    await expect(
      admin.getByRole("img", { name: "Biểu đồ xem trước của ba nhóm" }),
    ).toBeVisible();
    await admin
      .getByRole("button", { name: "Lưu nháp bài học", exact: true })
      .click();
    await expect(
      admin.getByText(
        "Đã lưu nháp. Chỉ bản đã xuất bản hiển thị cho học sinh.",
        { exact: true },
      ),
    ).toBeVisible();
    await admin.reload();
    await expect(admin.getByLabel("Giá trị cột 1")).toHaveValue("8");
    // The unpublished diagram remains absent from the student's published lesson.
    await page.reload();
    await expect(
      page.getByRole("img", { name: "Biểu đồ xem trước của ba nhóm" }),
    ).toHaveCount(0);
    await page.screenshot({
      path: `test-results/thinking-${info.project.name}.png`,
      fullPage: true,
    });
  } finally {
    await adminContext.close();
  }
});

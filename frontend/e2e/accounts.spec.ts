import { test, expect } from "@playwright/test";
import { login } from "./helpers";

const temporary = "Mat khau tam ban dau 2026";
const chosen = "Cum tu rieng cua hoc sinh 2026";
const resetPassword = "Mat khau ho tro lan hai 2026";
const finalPassword = "Cum tu cuoi cung cua em 2026";

test("quản trị tài khoản: tạo, sửa, khóa/mở, đặt lại; người dùng đổi mật khẩu và phiên", async ({
  page,
  browser,
}, info) => {
  const adminPassword = process.env.E2E_ADMIN_PASSWORD;
  test.skip(!adminPassword, "Cần admin trong DB test riêng");
  const username = `ui-account-${crypto.randomUUID()}`;
  await login(page, "admin", adminPassword!);
  await page.goto("/admin/accounts");
  await page.getByRole("link", { name: "Tạo tài khoản", exact: true }).click();
  const createForm = page.locator("form").filter({
    has: page.getByRole("heading", { name: "Thông tin tài khoản mới" }),
  });
  await createForm.getByLabel("Tên đăng nhập", { exact: true }).fill(username);
  await createForm
    .getByLabel("Tên hiển thị", { exact: true })
    .fill("Học sinh quản trị tài khoản");
  await createForm.getByLabel("Mật khẩu tạm", { exact: true }).fill(temporary);
  await createForm
    .getByLabel("Lý do tạo tài khoản")
    .fill("Tạo tài khoản kiểm thử giao diện");
  await createForm
    .getByLabel("Mật khẩu của quản trị viên")
    .fill(adminPassword!);
  await createForm
    .getByRole("button", { name: "Tạo tài khoản", exact: true })
    .click();
  await expect(page).toHaveURL(/\/admin\/accounts\/[^/]+\/edit$/);
  const accountId = page.url().split("/").at(-2)!;
  await expect(
    page.getByRole("heading", { name: "Nhật ký tài khoản" }),
  ).toBeVisible();
  const studentContext = await browser.newContext({
    ...info.project.use,
    baseURL: info.project.use.baseURL,
  });
  const student = await studentContext.newPage();
  try {
    async function temporaryLogin(password: string) {
      await student.goto("/login");
      await student.getByLabel("Tên đăng nhập", { exact: true }).fill(username);
      await student.getByLabel("Mật khẩu", { exact: true }).fill(password);
      await student.getByRole("button", { name: "Vào học thôi" }).click();
      await expect(student).toHaveURL(/\/account\/security$/);
      await expect(
        student.getByText("Bạn đang dùng mật khẩu tạm.", { exact: false }),
      ).toBeVisible();
    }
    async function changeOwnPassword(old: string, next: string) {
      const form = student.locator("form").filter({
        has: student.getByRole("heading", {
          name: "Đổi mật khẩu",
          exact: true,
        }),
      });
      await form.getByLabel("Mật khẩu hiện tại", { exact: true }).fill(old);
      await form.getByLabel("Mật khẩu mới", { exact: true }).fill(next);
      await form
        .getByLabel("Nhập lại mật khẩu mới", { exact: true })
        .fill(next);
      await form
        .getByRole("button", { name: "Đổi mật khẩu", exact: true })
        .click();
      await expect(
        student.getByText("Đã đổi mật khẩu.", { exact: false }),
      ).toBeVisible();
    }
    await temporaryLogin(temporary);
    expect(
      (await student.request.get("/api/v1/students/me/profile")).status(),
    ).toBe(403);
    const oldToken = (await studentContext.cookies()).find(
      (c) => c.name === "viettree_session",
    )!.value;
    await changeOwnPassword(temporary, chosen);
    expect(
      (await studentContext.cookies()).find(
        (c) => c.name === "viettree_session",
      )!.value,
    ).not.toBe(oldToken);
    await student.getByRole("link", { name: "Tiếp tục sử dụng" }).click();
    await expect(student).toHaveURL(/\/student\/dashboard$/);
    await page.reload(); // Password change also increments the edit revision.
    const editForm = page.locator("form").filter({
      has: page.getByRole("heading", { name: "Thông tin và quyền truy cập" }),
    });
    async function saveProfile(active: boolean, name = "Học sinh đã cập nhật") {
      await editForm.getByLabel("Tên hiển thị", { exact: true }).fill(name);
      await editForm
        .getByLabel("Tài khoản hoạt động", { exact: true })
        .setChecked(active);
      await editForm
        .getByLabel("Lý do cập nhật", { exact: true })
        .fill("Cập nhật trạng thái tài khoản kiểm thử");
      await editForm
        .getByLabel("Mật khẩu của quản trị viên")
        .fill(adminPassword!);
      await editForm
        .getByRole("button", { name: "Lưu tài khoản", exact: true })
        .click();
      await expect(
        page.getByText("Đã lưu tài khoản.", { exact: true }),
      ).toBeVisible();
      await expect(
        editForm.getByLabel("Mật khẩu của quản trị viên"),
      ).toHaveValue("");
    }
    await editForm
      .getByLabel("Cỡ chữ mặc định của học sinh")
      .selectOption("compact");
    await saveProfile(true);
    await expect(
      editForm.getByLabel("Cỡ chữ mặc định của học sinh"),
    ).toHaveValue("compact");
    await saveProfile(false);
    expect((await student.request.get("/api/v1/auth/me")).status()).toBe(401);
    await saveProfile(true);
    await login(student, username, chosen);
    expect(
      (await (await student.request.get("/api/v1/auth/me")).json())
        .display_name,
    ).toBe("Học sinh đã cập nhật");
    const resetForm = page.locator("form").filter({
      has: page.getByRole("heading", {
        name: "Đặt lại mật khẩu",
        exact: true,
      }),
    });
    await resetForm
      .getByLabel("Mật khẩu tạm mới", { exact: true })
      .fill(resetPassword);
    await resetForm
      .getByLabel("Nhập lại mật khẩu tạm mới", { exact: true })
      .fill(resetPassword);
    await resetForm
      .getByLabel("Lý do đặt lại mật khẩu")
      .fill("Hỗ trợ học sinh quên mật khẩu");
    await resetForm
      .getByLabel("Mật khẩu của quản trị viên")
      .fill(adminPassword!);
    await resetForm
      .getByRole("button", { name: "Đặt lại mật khẩu và thu hồi phiên" })
      .click();
    await expect(
      page.getByText("Đã đặt lại mật khẩu và thu hồi các phiên.", {
        exact: true,
      }),
    ).toBeVisible();
    expect((await student.request.get("/api/v1/auth/me")).status()).toBe(401);
    await student.reload();
    await expect(student).toHaveURL(/\/login$/);
    await temporaryLogin(resetPassword);
    await changeOwnPassword(resetPassword, finalPassword);
    await student
      .getByLabel("Xác nhận mật khẩu để đăng xuất phiên khác")
      .fill(finalPassword);
    await student
      .getByRole("button", { name: "Đăng xuất các phiên khác", exact: true })
      .click();
    await expect(
      student.getByText("Phiên hiện tại được giữ.", { exact: false }),
    ).toBeVisible();
    await page.goto("/admin/accounts");
    await page.getByLabel("Tìm tài khoản").fill(username);
    await expect(
      page.getByRole("row").filter({ hasText: username }),
    ).toContainText("Học sinh đã cập nhật");
    await page.goto(`/admin/accounts/${accountId}/edit`);
    await expect(
      page.getByRole("heading", { name: "Đặt lại mật khẩu", exact: true }),
    ).toHaveCount(2); // action form and history entry
    for (const width of [320, 768, 1280]) {
      await page.setViewportSize({ width, height: 800 });
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      ).toBe(true);
    }
    if (info.project.name === "mobile")
      await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({
      path: `test-results/accounts-${info.project.name}.png`,
      fullPage: true,
    });
  } finally {
    await studentContext.close();
  }
});

import { expect, test, type Page } from "@playwright/test";
import { login } from "./helpers";

test.use({ actionTimeout: 15_000 });

test("Gợi ý VIP: nút dễ đọc ở màn hình hẹp", async ({ page }, info) => {
  const device = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
  const username = process.env[`E2E_DISCOVERY_GRADE1_FREE_${device}_USERNAME`];
  const password = process.env.E2E_STUDENT_PASSWORD;
  test.skip(!username || !password, "Cần tài khoản riêng trên database test");
  await login(page, username!, password!);
  const catalog = await (
    await page.request.get(
      "/api/v1/students/me/lesson-library?release_code=discovery-2026-04&plan=free&subject_code=VIETNAMESE",
    )
  ).json();
  await page.goto(`/student/lessons/${catalog.items[0].id}`);
  for (const width of device === "MOBILE" ? [320, 390] : [1280]) {
    await page.setViewportSize({ width, height: 844 });
    const link = page.getByRole("link", {
      name: "Tìm hiểu gợi ý VIP",
      exact: true,
    });
    await expect(link).toBeVisible();
    const box = await link.boundingBox();
    expect(box!.width).toBeGreaterThan(150);
    expect(box!.height).toBeLessThan(100);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    await page
      .locator(".lesson-hints")
      .screenshot({ path: `../.tools/discovery-hints-${width}.png` });
  }
});

type DiscoveryCase = {
  grade: number;
  plan: string;
  units: { subject: string; title: string; answers: string[] }[];
};

// Frozen editorial answer labels. Arithmetic is also checked independently in Python.
const cases: DiscoveryCase[] = [
  {
    grade: 1,
    plan: "FREE",
    units: [
      {
        subject: "MATH",
        title: "Đếm hạt để gieo",
        answers: ["5 hạt", "4 hạt", "Nhóm A", "1 hạt"],
      },
      {
        subject: "VIETNAMESE",
        title: "Chiếc lá bên cửa",
        answers: ["Chiếc lá", "Giỏ", "Bé Na", "Sạch"],
      },
      {
        subject: "ENGLISH",
        title: "Mèo và chó: cat, dog",
        answers: ["cat", "dog", "Mèo", "This is a cat."],
      },
    ],
  },
  {
    grade: 1,
    plan: "VIP",
    units: [
      {
        subject: "MATH",
        title: "Ô trống của bạn Ong",
        answers: ["3 hạt", "5", "3 que", "5 + □ = 7"],
      },
      {
        subject: "VIETNAMESE",
        title: "Chờ bạn cùng đi",
        answers: ["Ra cổng", "Buộc dây giày", "Để cùng An đi học", "Nam và An"],
      },
      {
        subject: "ENGLISH",
        title: "Hỏi lại: có phải mèo không?",
        answers: ["Mèo", "Yes.", "No.", "Không"],
      },
    ],
  },
  {
    grade: 2,
    plan: "FREE",
    units: [
      {
        subject: "MATH",
        title: "Đo hai dải giấy",
        answers: ["40 cm", "16 cm", "7 cm", "Dải 40 cm"],
      },
      {
        subject: "VIETNAMESE",
        title: "Bình nước của Mai",
        answers: ["Bình nước", "Đậy nắp", "Lan", "Cô giáo"],
      },
      {
        subject: "ENGLISH",
        title: "Thước và tẩy của em",
        answers: ["ruler", "eraser", "Thước và tẩy", "Tôi có"],
      },
    ],
  },
  {
    grade: 2,
    plan: "VIP",
    units: [
      {
        subject: "MATH",
        title: "Tìm số trên cánh cửa",
        answers: ["45", "35", "47", "62"],
      },
      {
        subject: "VIETNAMESE",
        title: "Góc đọc có chỗ trống",
        answers: [
          "Cạnh cửa sổ",
          "Nhường chỗ cho Linh",
          "Cảm ơn",
          "Để không làm phiền cả lớp",
        ],
      },
      {
        subject: "ENGLISH",
        title: "Hai chiếc bút xanh",
        answers: ["Hai", "Xanh dương", "two pens", "two pens thành one pen"],
      },
    ],
  },
  {
    grade: 3,
    plan: "FREE",
    units: [
      {
        subject: "MATH",
        title: "Các hàng cây nhỏ",
        answers: ["24 cây", "6 cây", "30 cây", "18 cây"],
      },
      {
        subject: "VIETNAMESE",
        title: "Tấm nhãn ở vườn trường",
        answers: [
          "Ngày gieo và tên rau",
          "Minh",
          "Chụp nhãn cũ và hỏi Thu",
          "Đầu luống",
        ],
      },
      {
        subject: "ENGLISH",
        title: "My pets can move",
        answers: ["Run", "Fly", "Khả năng", "My bird can fly."],
      },
    ],
  },
  {
    grade: 3,
    plan: "VIP",
    units: [
      {
        subject: "MATH",
        title: "Bảng số còn thiếu",
        answers: ["24", "20", "20 hạt", "8"],
      },
      {
        subject: "VIETNAMESE",
        title: "Lời mời trong giờ ra chơi",
        answers: [
          "Hà chưa biết luật",
          "Thử chậm",
          "Nhặt bóng và bắt đầu lại",
          "Giờ ra chơi sau",
        ],
      },
      {
        subject: "ENGLISH",
        title: "Where is the rabbit?",
        answers: [
          "In the box",
          "Under the desk",
          "under",
          "Không, thỏ ở trong hộp",
        ],
      },
    ],
  },
  {
    grade: 4,
    plan: "FREE",
    units: [
      {
        subject: "MATH",
        title: "Đọc bảng mượn sách",
        answers: ["36 quyển", "12 quyển", "8 quyển", "Tổ 3"],
      },
      {
        subject: "VIETNAMESE",
        title: "Đọc thông báo đổi lịch",
        answers: [
          "Chiều thứ Sáu",
          "Phòng đọc cần sửa đèn",
          "Hai quyển",
          "Có, được cùng đọc tại chỗ",
        ],
      },
      {
        subject: "ENGLISH",
        title: "The weather card",
        answers: ["Rainy", "Read books", "At home", "Chưa cho biết"],
      },
    ],
  },
  {
    grade: 4,
    plan: "VIP",
    units: [
      {
        subject: "MATH",
        title: "Hai đội giữ sân xanh",
        answers: ["27 lá", "19 lá", "27 và 19", "12 bút"],
      },
      {
        subject: "VIETNAMESE",
        title: "Hai ý kiến cho góc xanh",
        answers: [
          "Giữa lối đi",
          "Chừa lối đi",
          "Đo khoảng trống và hỏi cô",
          "Có ý kiến ban đầu và lý do thay đổi",
        ],
      },
      {
        subject: "ENGLISH",
        title: "Two days, two activities",
        answers: [
          "Play football",
          "Tuesday",
          "I read books on Tuesday.",
          "Vào thứ Hai",
        ],
      },
    ],
  },
  {
    grade: 5,
    plan: "FREE",
    units: [
      {
        subject: "MATH",
        title: "Giảm giá trong bài toán",
        answers: ["30 000 đồng", "90 000 đồng", "75%", "72 000 đồng"],
      },
      {
        subject: "VIETNAMESE",
        title: "Đọc bản tin có ngày tháng",
        answers: [
          "Số sách mới nhận",
          "40 quyển",
          "Lịch mượn riêng của lớp",
          "Ngày bản tin và ý nghĩa số sách mới",
        ],
      },
      {
        subject: "ENGLISH",
        title: "Water after a walk",
        answers: ["Thirsty", "Some water", "In the shade", "Muốn"],
      },
    ],
  },
  {
    grade: 5,
    plan: "VIP",
    units: [
      {
        subject: "MATH",
        title: "Xếp hộp theo từng lớp",
        answers: ["24 cm³", "12 khối", "36 cm³", "2 cm"],
      },
      {
        subject: "VIETNAMESE",
        title: "Một đề xuất có căn cứ",
        answers: [
          "24 phiếu",
          "Phần lớn phiếu của lớp chọn bảng nhắc",
          "Khảo sát mới lấy phiếu của lớp 5B",
          "Thử một tuần và nhận thêm ý kiến",
        ],
      },
      {
        subject: "ENGLISH",
        title: "Read the trip plan",
        answers: ["8:00", "9:00", "We arrive before lunch.", "One hour"],
      },
    ],
  },
];
const release = "discovery-2026-04";
const answerName = (value: string) =>
  new RegExp("^[A-Z]\\s+" + value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "$");

async function selectPack(
  page: Page,
  library: "lesson" | "practice",
  plan: string,
) {
  await page.goto(
    library === "lesson" ? "/student/lessons" : "/student/practice",
  );
  await page.getByText("Chọn thêm bộ lọc", { exact: true }).click();
  await page.getByLabel("Bộ bài học").selectOption(release);
  await expect(page.locator("article.library-card")).toHaveCount(6);
  await page
    .getByLabel(library === "lesson" ? "Gói bài học" : "Gói bài luyện")
    .selectOption(plan.toLowerCase());
  await expect(page.locator("article.library-card")).toHaveCount(3);
}

for (const row of cases) {
  test(`Khám phá lớp ${row.grade} ${row.plan}: ba môn, gợi ý, tranh và chấm bài`, async ({
    page,
  }, info) => {
    const device = info.project.name === "mobile" ? "MOBILE" : "DESKTOP";
    const username =
      process.env[
        `E2E_DISCOVERY_GRADE${row.grade}_${row.plan}_${device}_USERNAME`
      ];
    const password = process.env.E2E_STUDENT_PASSWORD;
    test.skip(!username || !password, "Cần tài khoản riêng trên database test");
    await login(page, username!, password!);
    const metadata = await (
      await page.request.get(
        `/api/v1/students/me/lesson-library?release_code=${release}`,
      )
    ).json();
    expect(metadata.grade).toBe(row.grade);
    expect(metadata.summary.total).toBe(6);
    expect(
      metadata.items.filter((item: { locked: boolean }) => item.locked),
    ).toHaveLength(row.plan === "FREE" ? 3 : 0);
    if (row.plan === "FREE") {
      const locked = metadata.items.find(
        (item: { locked: boolean }) => item.locked,
      );
      expect(
        (await page.request.get(`/api/v1/lessons/${locked.id}`)).status(),
      ).toBe(403);
    }
    for (const unit of row.units) {
      await selectPack(page, "lesson", row.plan);
      await page.getByLabel("Môn học").selectOption(unit.subject);
      const card = page.locator("article.library-card");
      await expect(card).toHaveCount(1);
      await expect(
        card.getByRole("heading", { name: unit.title, exact: true }),
      ).toBeVisible();
      await card.getByRole("link", { name: /^(Mở bài học|Đọc tiếp)$/ }).click();
      await expect(
        page.getByRole("heading", { name: unit.title, exact: true }),
      ).toBeVisible();
      await expect(page.locator(".lesson-figure")).toBeVisible();
      for (const img of await page.locator(".lesson-figure img").all()) {
        await expect
          .poll(() =>
            img.evaluate(
              (element: HTMLImageElement) =>
                element.complete && element.naturalWidth > 0,
            ),
          )
          .toBe(true);
      }
      const hints = row.plan === "VIP" ? 3 : 1;
      for (let i = 1; i <= hints; i++)
        await page
          .getByRole("button", { name: `Mở gợi ý ${i}`, exact: true })
          .click();
      await expect(page.locator(".lesson-hints [role=status]")).toHaveText(
        `Đã mở ${hints}/${hints} gợi ý.`,
      );
      await expect(
        page.getByRole("button", { name: "Đã mở hết gợi ý", exact: true }),
      ).toBeDisabled();
      const complete = page.getByRole("button", {
        name: "Em đã đọc xong",
        exact: true,
      });
      if (await complete.count()) await complete.click();
      await expect(
        page.getByRole("button", { name: "Đã đánh dấu đọc xong", exact: true }),
      ).toBeDisabled();
      if (unit.subject === "VIETNAMESE") {
        await page.screenshot({
          path: `../.tools/discovery-grade${row.grade}-${row.plan}-${device}.png`,
          fullPage: true,
        });
      }
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
      ).toBe(true);
      const prefix = row.plan === "VIP" ? "Thử thách" : "Luyện tập";
      await page
        .getByRole("link", { name: `${prefix}: ${unit.title}`, exact: true })
        .click();
      await page
        .getByRole("button", { name: "Bắt đầu / Tiếp tục", exact: true })
        .click();
      await expect(page).toHaveURL(/\/student\/attempts\/[a-f0-9-]+$/);
      const attemptId = new URL(page.url()).pathname.split("/").pop();
      for (let i = 0; i < unit.answers.length; i++) {
        await expect(page.locator(".quiz-header")).toContainText(
          `Câu ${i + 1} / 4`,
        );
        await page
          .getByRole("radio", { name: answerName(unit.answers[i]) })
          .check();
        await page
          .getByRole("button", {
            name: i < 3 ? "Câu tiếp" : "Xem lại",
            exact: true,
          })
          .click();
      }
      await page.getByRole("button", { name: "Nộp bài", exact: true }).click();
      await page
        .getByRole("button", { name: "Xác nhận nộp", exact: true })
        .click();
      await expect(page).toHaveURL(/\/student\/results\//);
      const result = await (
        await page.request.get(`/api/v1/attempts/${attemptId}/result`)
      ).json();
      expect(result.correct_count).toBe(4);
      expect(result.items).toHaveLength(4);
    }
    await selectPack(page, "practice", row.plan);
    await page.getByLabel("Kết quả gần nhất").selectOption("mastered");
    await expect(page.locator("article.library-card")).toHaveCount(3);
    await expect(page.getByText("100%", { exact: true })).toHaveCount(3);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    await page.getByRole("button", { name: "Xóa bộ lọc", exact: true }).click();
    await expect(page.getByLabel("Bộ bài học")).toHaveValue("");
    await expect(page.locator("article.library-card")).toHaveCount(12);
  });
}

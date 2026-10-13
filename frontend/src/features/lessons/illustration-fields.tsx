"use client";
import type { LessonContent, LessonIllustration } from "@/lib/types";

export const illustrations: Record<LessonIllustration["kind"], string> = {
  fraction: "Thanh phân số",
  garden: "Luống rau và diện tích",
  reading: "Hành trình đọc hiểu",
  clock: "Đồng hồ",
  bars: "Biểu đồ cột",
  angles: "Góc và số đo",
  counters: "Chấm tròn để đếm (lớp 1–2)",
  cards: "Thẻ chữ và từ ngắn (lớp 1–2)",
  triangle: "Tam giác: đáy và chiều cao",
  trapezoid: "Hình thang: hai đáy và chiều cao",
  circle: "Hình tròn: bán kính và đường kính",
  box: "Hình hộp chữ nhật: ba kích thước",
  pie: "Biểu đồ quạt tròn (tổng 100%)",
};

const numberFields: Partial<
  Record<LessonIllustration["kind"], [string, string, number, number, string][]>
> = {
  fraction: [
    ["numerator", "Số phần tô màu", 0, 12, "1"],
    ["denominator", "Tổng số phần", 1, 12, "1"],
  ],
  garden: [
    ["rows", "Số hàng ô vuông", 1, 6, "1"],
    ["columns", "Số cột ô vuông", 1, 8, "1"],
  ],
  clock: [
    ["hour", "Giờ (0–23)", 0, 23, "1"],
    ["minute", "Phút", 0, 59, "1"],
  ],
  angles: [["angle", "Số đo góc (độ)", 1, 180, "1"]],
  counters: [["count", "Số chấm tròn (0–20)", 0, 20, "1"]],
  bars: [["tick", "Số đơn vị mỗi vạch", 1, 20, "1"]],
  triangle: [
    ["base", "Đáy (cm)", 0.001, 1000, "any"],
    ["height", "Chiều cao vuông góc (cm)", 0.001, 1000, "any"],
  ],
  trapezoid: [
    ["base", "Đáy thứ nhất (cm)", 0.001, 1000, "any"],
    ["upper_base", "Đáy thứ hai (cm)", 0.001, 1000, "any"],
    ["height", "Chiều cao vuông góc (cm)", 0.001, 1000, "any"],
  ],
  circle: [["radius", "Bán kính (cm)", 0.001, 1000, "any"]],
  box: [
    ["length", "Chiều dài (cm)", 0.001, 1000, "any"],
    ["width", "Chiều rộng (cm)", 0.001, 1000, "any"],
    ["height", "Chiều cao (cm)", 0.001, 1000, "any"],
  ],
};

export function IllustrationFields({
  value,
  content,
  busy,
}: {
  value: LessonContent;
  content: (patch: Partial<LessonContent>) => void;
  busy: boolean;
}) {
  return (
    <fieldset disabled={busy}>
      <legend>Minh họa cho bài học</legend>
      <label htmlFor="lesson-illustration">
        Chọn minh họa
        <select
          id="lesson-illustration"
          value={value.illustration?.kind || ""}
          onChange={(e) =>
            content({
              illustration: e.target.value
                ? {
                    kind: e.target.value as LessonIllustration["kind"],
                    caption: "",
                    numerator: 3,
                    denominator: 8,
                    rows: 3,
                    columns: 4,
                    hour: 8,
                    minute: 0,
                    count: 5,
                    angle: 60,
                    tick: 4,
                    base: 6,
                    upper_base: 4,
                    height: 4,
                    radius: 2,
                    length: 6,
                    width: 4,
                    labels:
                      e.target.value === "cards"
                        ? ["a", "ă", "â"]
                        : ["Tổ 1", "Tổ 2", "Tổ 3"],
                    values:
                      e.target.value === "pie" ? [50, 30, 20] : [12, 16, 20],
                  }
                : null,
            })
          }
        >
          <option value="">Không dùng minh họa</option>
          {Object.entries(illustrations).map(([kind, label]) => (
            <option key={kind} value={kind}>
              {label}
            </option>
          ))}
        </select>
      </label>
      {value.illustration && (
        <>
          <label htmlFor="lesson-caption">
            Chú thích hình (nêu rõ ý nghĩa và số liệu)
            <textarea
              id="lesson-caption"
              required
              minLength={5}
              maxLength={400}
              value={value.illustration.caption}
              onChange={(e) =>
                content({
                  illustration: {
                    ...value.illustration!,
                    caption: e.target.value,
                  },
                })
              }
            />
          </label>
          <div className="two-columns">
            {(numberFields[value.illustration.kind] || []).map(
              ([key, label, min, max, step]) => (
                <label key={key} htmlFor={`figure-${key}`}>
                  {label}
                  <input
                    id={`figure-${key}`}
                    type="number"
                    required
                    min={Number(min)}
                    max={Number(max)}
                    step={step}
                    value={Number(
                      value.illustration![key as keyof LessonIllustration] ?? 0,
                    )}
                    onChange={(e) =>
                      content({
                        illustration: {
                          ...value.illustration!,
                          [key]: Number(e.target.value),
                        },
                      })
                    }
                  />
                </label>
              ),
            )}
          </div>
          {value.illustration.kind === "cards" && (
            <label>
              Thẻ chữ/từ (1–6 thẻ, phân cách bằng dấu phẩy)
              <input
                value={(value.illustration.labels || []).join(", ")}
                onChange={(e) =>
                  content({
                    illustration: {
                      ...value.illustration!,
                      labels: e.target.value.split(",").map((v) => v.trim()),
                    },
                  })
                }
              />
            </label>
          )}
          {["bars", "pie"].includes(value.illustration.kind) && (
            <fieldset>
              <legend>Số liệu biểu đồ (1–6 nhóm)</legend>
              {value.illustration.kind === "pie" && (
                <p className="notice">
                  Tổng hiện tại:{" "}
                  {(value.illustration.values || []).reduce(
                    (sum, n) => sum + n,
                    0,
                  )}
                  %. Cần đúng 100% để lưu bài.
                </p>
              )}
              {(value.illustration.values || [12, 16, 20]).map((number, i) => (
                <div className="two-columns" key={i}>
                  <label htmlFor={`bar-label-${i}`}>
                    Nhãn {value.illustration!.kind === "pie" ? "phần" : "cột"}{" "}
                    {i + 1}
                    <input
                      id={`bar-label-${i}`}
                      required
                      maxLength={18}
                      value={
                        (value.illustration!.labels || [
                          "Tổ 1",
                          "Tổ 2",
                          "Tổ 3",
                        ])[i]
                      }
                      onChange={(e) => {
                        const labels = [
                          ...(value.illustration!.labels || [
                            "Tổ 1",
                            "Tổ 2",
                            "Tổ 3",
                          ]),
                        ];
                        labels[i] = e.target.value;
                        content({
                          illustration: {
                            ...value.illustration!,
                            labels,
                          },
                        });
                      }}
                    />
                  </label>
                  <label htmlFor={`bar-value-${i}`}>
                    Giá trị{" "}
                    {value.illustration!.kind === "pie" ? "phần" : "cột"}{" "}
                    {i + 1}
                    {value.illustration!.kind === "pie" ? " (%)" : ""}
                    <input
                      id={`bar-value-${i}`}
                      type="number"
                      min={0}
                      max={100}
                      required
                      value={number}
                      onChange={(e) => {
                        const values = [
                          ...(value.illustration!.values || [12, 16, 20]),
                        ];
                        values[i] = Number(e.target.value);
                        content({
                          illustration: {
                            ...value.illustration!,
                            values,
                          },
                        });
                      }}
                    />
                  </label>
                </div>
              ))}
              <div className="actions">
                <button
                  type="button"
                  className="button secondary"
                  disabled={
                    (value.illustration.values || [12, 16, 20]).length >= 6
                  }
                  onClick={() =>
                    content({
                      illustration: {
                        ...value.illustration!,
                        labels: [
                          ...(value.illustration!.labels || [
                            "Tổ 1",
                            "Tổ 2",
                            "Tổ 3",
                          ]),
                          "Nhóm mới",
                        ],
                        values: [
                          ...(value.illustration!.values || [12, 16, 20]),
                          0,
                        ],
                      },
                    })
                  }
                >
                  Thêm nhóm
                </button>
                <button
                  type="button"
                  className="button secondary"
                  disabled={
                    (value.illustration.values || [12, 16, 20]).length <= 1
                  }
                  onClick={() =>
                    content({
                      illustration: {
                        ...value.illustration!,
                        labels: (
                          value.illustration!.labels || ["Tổ 1", "Tổ 2", "Tổ 3"]
                        ).slice(0, -1),
                        values: (
                          value.illustration!.values || [12, 16, 20]
                        ).slice(0, -1),
                      },
                    })
                  }
                >
                  Bỏ nhóm cuối
                </button>
              </div>
            </fieldset>
          )}
        </>
      )}
    </fieldset>
  );
}

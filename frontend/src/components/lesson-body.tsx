"use client";

import { useId, useState } from "react";
import Link from "next/link";
import { BookOpen, Lightbulb, MessageCircle } from "lucide-react";
import type { LessonContent, LessonIllustration } from "@/lib/types";

export function LessonFigure({ value }: { value: LessonIllustration }) {
  const label = useId();
  if (value.kind === "cards")
    return (
      <figure className="lesson-figure">
        <div className="early-word-cards" role="img" aria-label={value.caption}>
          {(value.labels || []).slice(0, 6).map((word, i) => (
            <span key={i}>{word}</span>
          ))}
        </div>
        <figcaption>{value.caption}</figcaption>
      </figure>
    );
  const n = Math.max(0, Math.min(value.numerator ?? 3, value.denominator ?? 8));
  const d = Math.max(1, Math.min(value.denominator ?? 8, 12));
  const rows = Math.max(1, Math.min(value.rows ?? 3, 6));
  const cols = Math.max(1, Math.min(value.columns ?? 4, 8));
  const hour = (value.hour ?? 8) % 12;
  const minute = value.minute ?? 0;
  const hand = (angle: number, length: number) => ({
    x: 300 + Math.sin(angle) * length,
    y: 126 - Math.cos(angle) * length,
  });
  const short = hand(((hour + minute / 60) * Math.PI) / 6, 55);
  const long = hand((minute * Math.PI) / 30, 80);
  const angle = Math.max(1, Math.min(value.angle ?? 60, 180));
  const ax = 200 + 160 * Math.cos((angle * Math.PI) / 180);
  const ay = 210 - 160 * Math.sin((angle * Math.PI) / 180);
  const bars = (value.values || [12, 16, 20])
    .slice(0, 6)
    .map((n) => Math.max(0, Math.min(n, 100)));
  const tick = Math.max(1, Math.min(value.tick ?? 4, 20));
  const maximum = Math.max(tick, Math.ceil(Math.max(...bars, 0) / tick) * tick);
  // Keep at most six labelled ticks, even for a manually entered fine scale.
  const stride = Math.ceil(maximum / tick / 5);
  return (
    <figure className="lesson-figure">
      <svg viewBox="0 0 600 260" role="img" aria-labelledby={label}>
        <title id={label}>{value.caption}</title>
        <rect width="600" height="260" rx="24" fill="#edf6ef" />
        <circle cx="550" cy="34" r="16" fill="#f5ce71" />
        {value.kind === "counters" && (
          <>
            {Array.from(
              { length: Math.max(0, Math.min(value.count ?? 5, 20)) },
              (_, i) => (
                <circle
                  key={i}
                  cx={75 + (i % 10) * 50}
                  cy={85 + Math.floor(i / 10) * 65}
                  r="18"
                  fill={i < 10 ? "#23805b" : "#d69b35"}
                />
              ),
            )}
            <text
              x="300"
              y="227"
              textAnchor="middle"
              fontSize="27"
              fill="#203d34"
            >
              {value.count ?? 5} chấm tròn
            </text>
          </>
        )}
        <path
          d="M35 224Q55 194 75 224T115 224"
          fill="none"
          stroke="#86bca0"
          strokeWidth="5"
        />
        {value.kind === "angles" && (
          <>
            <path
              d={`M${ax} ${ay}L200 210L400 210`}
              fill="none"
              stroke="#23805b"
              strokeWidth="6"
            />
            <path
              d={`M260 210A60 60 0 0 0 ${200 + 60 * Math.cos((angle * Math.PI) / 180)} ${210 - 60 * Math.sin((angle * Math.PI) / 180)}`}
              fill="none"
              stroke="#c68132"
              strokeWidth="4"
            />
            <circle cx="200" cy="210" r="5" fill="#203d34" />
            <text x="420" y="125" fontSize="30" fill="#203d34">
              {angle}°
            </text>
            <text x="420" y="160" fontSize="23" fill="#203d34">
              {angle < 90
                ? "Góc nhọn"
                : angle === 90
                  ? "Góc vuông"
                  : angle < 180
                    ? "Góc tù"
                    : "Góc bẹt"}
            </text>
          </>
        )}
        {value.kind === "bars" && (
          <>
            {Array.from(
              { length: Math.floor(maximum / (tick * stride)) + 1 },
              (_, i) => {
                const number = i * tick * stride,
                  y = 215 - (number / maximum) * 165;
                return (
                  <g key={number}>
                    <path d={`M65 ${y}H560`} stroke="#c2daca" />
                    <text
                      x="55"
                      y={y + 7}
                      textAnchor="end"
                      fontSize="20"
                      fill="#203d34"
                    >
                      {number}
                    </text>
                  </g>
                );
              },
            )}
            {bars.map((number, i) => {
              const label = (value.labels || ["Tổ 1", "Tổ 2", "Tổ 3"])[i] || "";
              const limit = bars.length > 4 ? 7 : 12;
              const spacing = 490 / bars.length,
                x = 70 + spacing * i + spacing * 0.2,
                width = spacing * 0.6;
              return (
                <g key={i}>
                  <title>
                    {label}: {number}
                  </title>
                  <rect
                    x={x}
                    y={215 - (number / maximum) * 165}
                    width={width}
                    height={(number / maximum) * 165}
                    rx="4"
                    fill="#2d9167"
                  />
                  <text
                    x={x + width / 2}
                    y={205 - (number / maximum) * 165}
                    textAnchor="middle"
                    fontSize="22"
                    fill="#203d34"
                  >
                    {number}
                  </text>
                  <text
                    x={x + width / 2}
                    y="245"
                    textAnchor="middle"
                    fontSize="19"
                    fill="#203d34"
                  >
                    {label.length > limit
                      ? `${label.slice(0, limit - 1)}…`
                      : label}
                  </text>
                </g>
              );
            })}
          </>
        )}
        {value.kind === "fraction" && (
          <>
            <text
              x="300"
              y="58"
              textAnchor="middle"
              fontSize="25"
              fill="#203d34"
            >
              Các phần có kích thước bằng nhau
            </text>
            {Array.from({ length: d }, (_, i) => (
              <rect
                key={i}
                x={40 + (i * 520) / d}
                y="85"
                width={520 / d}
                height="90"
                fill={i < n ? "#2d9167" : "#fff"}
                stroke="#203d34"
                strokeWidth="2"
              />
            ))}
            <text
              x="300"
              y="222"
              textAnchor="middle"
              fontSize="26"
              fill="#203d34"
            >
              {n} phần tô màu / {d} phần = {n}/{d}
            </text>
          </>
        )}
        {value.kind === "garden" && (
          <>
            <text
              x="300"
              y="36"
              textAnchor="middle"
              fontSize="23"
              fill="#203d34"
            >
              Luống rau: mỗi ô là 1 m²
            </text>
            {Array.from({ length: rows * cols }, (_, i) => {
              const w = 360 / cols,
                h = 150 / rows,
                x = 120 + (i % cols) * w,
                y = 54 + Math.floor(i / cols) * h;
              return (
                <g key={i}>
                  <rect
                    x={x}
                    y={y}
                    width={w}
                    height={h}
                    fill={i % 2 ? "#cde8cc" : "#deefd8"}
                    stroke="#4d7956"
                    strokeWidth="2"
                  />
                  <path
                    d={`M${x + w / 2} ${y + h * 0.76}v-${h * 0.35}`}
                    stroke="#347454"
                    strokeWidth="2"
                  />
                  <ellipse
                    cx={x + w * 0.43}
                    cy={y + h * 0.48}
                    rx={Math.min(w * 0.13, 12)}
                    ry={Math.min(h * 0.13, 8)}
                    fill="#4c9c62"
                  />
                  <ellipse
                    cx={x + w * 0.57}
                    cy={y + h * 0.35}
                    rx={Math.min(w * 0.13, 12)}
                    ry={Math.min(h * 0.13, 8)}
                    fill="#6fb475"
                  />
                </g>
              );
            })}
            <text
              x="300"
              y="237"
              textAnchor="middle"
              fontSize="23"
              fill="#203d34"
            >
              {rows} × {cols} = {rows * cols} m² · Chu vi: {2 * (rows + cols)} m
            </text>
          </>
        )}
        {value.kind === "reading" && (
          <>
            <path
              d="M90 158Q158 62 228 150T390 140T516 108"
              fill="none"
              stroke="#96bd9f"
              strokeWidth="5"
              strokeDasharray="10 9"
            />
            {["Đọc", "Tìm", "Giải thích", "Kiểm tra"].map((word, i) => (
              <g key={word}>
                <circle
                  cx={80 + i * 145}
                  cy={110 + (i % 2) * 38}
                  r="35"
                  fill={i % 2 ? "#f6cc72" : "#3284ae"}
                />
                <text
                  x={80 + i * 145}
                  y={119 + (i % 2) * 38}
                  textAnchor="middle"
                  fontSize="27"
                  fill={i % 2 ? "#203d34" : "#fff"}
                >
                  {i + 1}
                </text>
                <text
                  x={80 + i * 145}
                  y="219"
                  textAnchor="middle"
                  fontSize="22"
                  fill="#203d34"
                >
                  {word}
                </text>
              </g>
            ))}
            <path
              d="M273 28q13-12 27 0q14-12 27 0v35q-14-10-27 0q-14-10-27 0Z"
              fill="#fff"
              stroke="#23805b"
              strokeWidth="3"
            />
            <path d="M300 28v35" stroke="#23805b" strokeWidth="2" />
          </>
        )}
        {value.kind === "clock" && (
          <>
            <circle
              cx="300"
              cy="126"
              r="96"
              fill="white"
              stroke="#3284ae"
              strokeWidth="7"
            />
            {Array.from({ length: 12 }, (_, i) => {
              const angle = ((i + 1) * Math.PI) / 6;
              return (
                <text
                  key={i}
                  x={300 + Math.sin(angle) * 78}
                  y={133 - Math.cos(angle) * 78}
                  textAnchor="middle"
                  fontSize="20"
                  fill="#203d34"
                >
                  {i + 1}
                </text>
              );
            })}
            <path
              d={`M300 126L${short.x} ${short.y}`}
              stroke="#23805b"
              strokeWidth="8"
              strokeLinecap="round"
            />
            <path
              d={`M300 126L${long.x} ${long.y}`}
              stroke="#c68132"
              strokeWidth="5"
              strokeLinecap="round"
            />
            <circle cx="300" cy="126" r="7" fill="#203d34" />
            <text
              x="300"
              y="249"
              textAnchor="middle"
              fontSize="24"
              fill="#203d34"
            >
              {String(value.hour ?? 8).padStart(2, "0")}:
              {String(minute).padStart(2, "0")}
            </text>
          </>
        )}
      </svg>
      <figcaption>{value.caption}</figcaption>
    </figure>
  );
}

export function LessonBody({
  content,
  hintAccess,
}: {
  content: LessonContent;
  hintAccess?: { available: number; total: number; vip_locked: number };
}) {
  const [revealed, setRevealed] = useState(0);
  const prefix = useId();
  const hints = content.hints || [];
  return (
    <div className="lesson-reading">
      {!!content.goals?.length && (
        <section className="panel lesson-goals">
          <h2>
            <BookOpen aria-hidden size={24} /> Sau bài này, em có thể
          </h2>
          <ul>
            {content.goals.map((goal, i) => (
              <li key={i}>{goal}</li>
            ))}
          </ul>
        </section>
      )}
      <nav className="lesson-outline panel" aria-label="Các phần trong bài">
        <strong>Chọn phần em muốn đọc</strong>
        <div>
          {content.blocks.map((block, i) => (
            <a href={`#${prefix}-block-${i}`} key={i}>
              {i + 1}. {block.title}
            </a>
          ))}
        </div>
      </nav>
      {content.illustration && <LessonFigure value={content.illustration} />}
      <div className="lesson-blocks">
        {content.blocks.map((block, i) => (
          <section
            id={`${prefix}-block-${i}`}
            className={`lesson-block ${block.type}`}
            key={i}
          >
            <h2>{block.title}</h2>
            <p>{block.text}</p>
          </section>
        ))}
      </div>
      {!!hints.length && (
        <section className="panel lesson-hints">
          <h2>
            <Lightbulb aria-hidden size={24} /> Gợi ý từng bước
          </h2>
          <p>
            Thử nghĩ trước, rồi mở thêm gợi ý khi em cần. Gợi ý này giúp học
            bài, không trả lời thay bài kiểm tra.
          </p>
          <ol>
            {hints.slice(0, revealed).map((hint, i) => (
              <li key={i}>{hint}</li>
            ))}
          </ol>
          <button
            className="button secondary"
            disabled={revealed >= hints.length}
            onClick={() => setRevealed((n) => Math.min(n + 1, hints.length))}
          >
            {revealed >= hints.length
              ? "Đã mở hết gợi ý"
              : `Mở gợi ý ${revealed + 1}`}
          </button>
          <p role="status" aria-live="polite">
            Đã mở {revealed}/{hints.length} gợi ý.
          </p>
          {!!hintAccess?.vip_locked && (
            <div className="notice">
              <p>
                Em có {hints.length} gợi ý định hướng miễn phí. VIP có thêm{" "}
                {hintAccess.vip_locked} gợi ý về cách làm và kiểm tra, mở từng
                bước khi cần.
              </p>
              <Link className="button secondary" href="/student/membership">
                Tìm hiểu gợi ý VIP
              </Link>
            </div>
          )}
        </section>
      )}
      {!!content.reflection?.length && (
        <section className="panel lesson-reflection">
          <h2>
            <MessageCircle aria-hidden size={24} /> Em thử giải thích nhé
          </h2>
          <p>
            Em có thể nói với người thân hoặc ghi ý của mình. Phần này không
            chấm điểm; ghi chú chỉ ở trang hiện tại và không lưu khi rời trang.
          </p>
          {content.reflection.map((question, i) => (
            <label key={i} htmlFor={`${prefix}-reflection-${i}`}>
              {question}
              <textarea
                id={`${prefix}-reflection-${i}`}
                rows={3}
                maxLength={1200}
                placeholder="Ý của em…"
              />
            </label>
          ))}
        </section>
      )}
    </div>
  );
}

"use client";

import { useId } from "react";
import type { LessonIllustration } from "@/lib/types";

const colors = [
  "#23805b",
  "#3284ae",
  "#c68132",
  "#8460a3",
  "#a44867",
  "#657e35",
];

export function GeometryFigure({ value }: { value: LessonIllustration }) {
  const label = useId();
  const base = value.base ?? 6,
    top = value.upper_base ?? 4,
    height = value.height ?? 4;
  const scale = Math.min(
    280 / Math.max(base, value.kind === "trapezoid" ? top : base),
    160 / height,
  );
  const w = base * scale,
    h = height * scale,
    upper = top * scale;
  const trapezoidWidth = Math.max(w, upper);
  const trapezoidLeft = 100 + (trapezoidWidth - w) / 2;
  const trapezoidTopLeft = 100 + (trapezoidWidth - upper) / 2;
  const trapezoidCenter = 100 + trapezoidWidth / 2;
  const length = value.length ?? 6,
    width = value.width ?? 4;
  const boxScale = Math.min(210 / length, 120 / (height + width * 0.5));
  const bx = length * boxScale,
    by = height * boxScale,
    dx = width * boxScale * 0.8,
    dy = width * boxScale * 0.5;
  const values = value.values || [50, 30, 20];
  const labels = value.labels || ["Nhóm 1", "Nhóm 2", "Nhóm 3"];
  const measurements: Partial<
    Record<LessonIllustration["kind"], [string, number][]>
  > = {
    triangle: [
      ["Đáy", base],
      ["Chiều cao", height],
    ],
    trapezoid: [
      ["Đáy thứ nhất", base],
      ["Đáy thứ hai", top],
      ["Chiều cao", height],
    ],
    circle: [
      ["Bán kính", value.radius ?? 2],
      ["Đường kính", 2 * (value.radius ?? 2)],
    ],
    box: [
      ["Chiều dài", length],
      ["Chiều rộng", width],
      ["Chiều cao", height],
    ],
  };
  const starts = values.map((_, i) =>
    values.slice(0, i).reduce((a, b) => a + b, 0),
  );
  const point = (percent: number) => ({
    x: 250 + 95 * Math.cos((((percent / 100) * 360 - 90) * Math.PI) / 180),
    y: 140 + 95 * Math.sin((((percent / 100) * 360 - 90) * Math.PI) / 180),
  });
  return (
    <figure className="lesson-figure geometry-figure">
      <svg viewBox="0 0 600 280" role="img" aria-labelledby={label}>
        <title id={label}>{value.caption}</title>
        <rect width="600" height="280" rx="24" fill="#edf6ef" />
        {value.kind === "triangle" && (
          <g>
            <path
              d={`M100 230H${100 + w}L100 ${230 - h}Z`}
              fill="#cce6d8"
              stroke="#23805b"
              strokeWidth="3"
            />
            <path
              d="M100 214H116V230"
              fill="none"
              stroke="#c68132"
              strokeWidth="3"
            />
            <text x={100 + w / 2} y="260" textAnchor="middle" fontSize="24">
              Đáy {base} cm
            </text>
            <text x="420" y="120" fontSize="24">
              Cao {height} cm
            </text>
            <text x="420" y="155" fontSize="20">
              Vuông góc đáy
            </text>
          </g>
        )}
        {value.kind === "trapezoid" && (
          <g>
            <path
              d={`M${trapezoidLeft} 230H${trapezoidLeft + w}L${trapezoidTopLeft + upper} ${230 - h}H${trapezoidTopLeft}Z`}
              fill="#cce6d8"
              stroke="#23805b"
              strokeWidth="3"
            />
            <path
              d={`M${trapezoidCenter} ${230 - h}V230`}
              stroke="#c68132"
              strokeWidth="3"
              strokeDasharray="7 5"
            />
            <text
              x={trapezoidCenter}
              y={230 - h - 12}
              textAnchor="middle"
              fontSize="24"
            >
              {top} cm
            </text>
            <text x={trapezoidCenter} y="260" textAnchor="middle" fontSize="24">
              {base} cm
            </text>
            <text x="420" y="145" fontSize="24">
              Cao {height} cm
            </text>
          </g>
        )}
        {value.kind === "circle" && (
          <g>
            <circle
              cx="250"
              cy="140"
              r="90"
              fill="#cce6d8"
              stroke="#23805b"
              strokeWidth="3"
            />
            <path d="M250 140H340" stroke="#c68132" strokeWidth="4" />
            <circle cx="250" cy="140" r="5" fill="#203d34" />
            <text x="405" y="120" fontSize="24">
              r = {value.radius ?? 2} cm
            </text>
            <text x="405" y="160" fontSize="24">
              d = {2 * (value.radius ?? 2)} cm
            </text>
          </g>
        )}
        {value.kind === "box" && (
          <g>
            <path
              d={`M140 220h${bx}v${-by}H140Z`}
              fill="#cce6d8"
              stroke="#23805b"
              strokeWidth="3"
            />
            <path
              d={`M140 ${220 - by}l${dx} ${-dy}h${bx}l${-dx} ${dy}Z`}
              fill="#abcfbd"
              stroke="#23805b"
              strokeWidth="3"
            />
            <path
              d={`M${140 + bx} 220l${dx} ${-dy}v${-by}l${-dx} ${dy}Z`}
              fill="#8fb9a5"
              stroke="#23805b"
              strokeWidth="3"
            />
            <text x={140 + bx / 2} y="255" textAnchor="middle" fontSize="24">
              Dài {length} cm
            </text>
            <text x="425" y="110" fontSize="24">
              Rộng {width} cm
            </text>
            <text x="425" y="150" fontSize="24">
              Cao {height} cm
            </text>
          </g>
        )}
        {value.kind === "pie" &&
          values.map((v, i) => {
            if (v === 0) return null;
            const start = point(starts[i]),
              end = point(starts[i] + v);
            const middle =
              ((starts[i] + v / 2) / 100) * 2 * Math.PI - Math.PI / 2;
            return (
              <g key={i}>
                {v === 100 ? (
                  <circle cx="250" cy="140" r="95" fill={colors[i]} />
                ) : (
                  <path
                    d={`M250 140L${start.x} ${start.y}A95 95 0 ${v > 50 ? 1 : 0} 1 ${end.x} ${end.y}Z`}
                    fill={colors[i]}
                    stroke="white"
                    strokeWidth="2"
                  >
                    <title>
                      {labels[i]}: {v}%
                    </title>
                  </path>
                )}
                {v >= 10 && (
                  <text
                    x={250 + 60 * Math.cos(middle)}
                    y={140 + 60 * Math.sin(middle) + 7}
                    textAnchor="middle"
                    fontSize="23"
                    fill="white"
                    fontWeight="700"
                  >
                    {v}%
                  </text>
                )}
              </g>
            );
          })}
      </svg>
      {!!measurements[value.kind] && (
        <dl className="geometry-measures" aria-label="Số đo của hình">
          {measurements[value.kind]!.map(([name, number]) => (
            <div key={name}>
              <dt>{name}:</dt>
              <dd>{String(number).replace(".", ",")} cm</dd>
            </div>
          ))}
        </dl>
      )}
      {value.kind === "pie" && (
        <ul className="pie-legend">
          {values.map((v, i) => (
            <li key={i}>
              <span aria-hidden style={{ background: colors[i] }} />
              {labels[i]}: <strong>{v}%</strong>
            </li>
          ))}
        </ul>
      )}
      <figcaption>{value.caption}</figcaption>
    </figure>
  );
}

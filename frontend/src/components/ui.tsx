"use client";
import Link from "next/link";
import {
  BookOpen,
  Calculator,
  Globe,
  Sprout,
  ArrowRight,
  AlertCircle,
} from "lucide-react";
import type { Subject } from "@/lib/types";

export function Brand() {
  return (
    <Link href="/" className="brand">
      <span className="brand-icon">
        <Sprout size={25} />
      </span>
      <span>
        VietTree<small>EDUCATION</small>
      </span>
    </Link>
  );
}
export function Loading() {
  return (
    <div className="skeleton" role="status" aria-label="Đang tải">
      <span />
      <span />
      <span />
    </div>
  );
}
export function ErrorState({
  message,
  retry,
}: {
  message: string;
  retry?: () => void;
}) {
  return (
    <div className="notice error" role="alert">
      <AlertCircle />
      <div>
        <strong>Chưa tải được dữ liệu</strong>
        <p>{message}</p>
        {retry && (
          <button onClick={retry} className="button secondary">
            Thử lại
          </button>
        )}
      </div>
    </div>
  );
}
export function Empty({ children }: { children: React.ReactNode }) {
  return (
    <div className="empty">
      <Sprout />
      <p>{children}</p>
    </div>
  );
}
export function PageTitle({
  eyebrow,
  title,
  description,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
}) {
  return (
    <header className="page-title">
      {eyebrow && <span className="eyebrow">{eyebrow}</span>}
      <h1>{title}</h1>
      {description && <p>{description}</p>}
    </header>
  );
}
export function SubjectCards({ subjects }: { subjects: Subject[] }) {
  return (
    <div className="subject-grid">
      {subjects.map((subject) => {
        const Icon =
          subject.code === "MATH"
            ? Calculator
            : subject.code === "ENGLISH"
              ? Globe
              : BookOpen;
        const available = subject.status === "available";
        return (
          <Link
            className={`subject-card ${subject.code.toLowerCase()}`}
            href={`/student/subjects/${subject.code}?grade=${subject.grade}`}
            key={subject.id}
          >
            <span className="subject-icon">
              <Icon size={28} />
            </span>
            <h3>{subject.name_vi}</h3>
            <p>
              {available
                ? `${subject.topic_count} chủ đề để khám phá`
                : "Đang xây dựng"}
            </p>
            <span className="card-link">
              {available ? "Bắt đầu khám phá" : "Xem chương trình"}
              <ArrowRight size={17} />
            </span>
          </Link>
        );
      })}
    </div>
  );
}
export function TreeArt() {
  return (
    <svg
      viewBox="0 0 440 390"
      role="img"
      aria-label="Cây tri thức đang lớn lên"
      className="tree-art"
    >
      <circle cx="225" cy="180" r="153" fill="#dcefe5" />
      <ellipse cx="225" cy="350" rx="150" ry="16" fill="#c9e2d5" />
      <path d="M211 343V143h24v200" fill="#b47944" />
      <path
        d="m222 236-62-64m65 32 61-59"
        stroke="#b47944"
        strokeWidth="18"
        strokeLinecap="round"
      />
      <circle cx="154" cy="150" r="58" fill="#61b987" />
      <circle cx="217" cy="106" r="68" fill="#25966b" />
      <circle cx="291" cy="146" r="61" fill="#45ac7d" />
      <circle cx="197" cy="176" r="65" fill="#36a775" />
      <circle cx="258" cy="188" r="58" fill="#73c59a" />
      <rect
        x="74"
        y="269"
        width="60"
        height="65"
        rx="12"
        fill="#f4ad5b"
        transform="rotate(-12 74 269)"
      />
      <path
        d="M88 289h29m-29 10h24m-24 10h19"
        stroke="white"
        strokeWidth="5"
        strokeLinecap="round"
      />
      <rect
        x="304"
        y="251"
        width="63"
        height="60"
        rx="12"
        fill="#5fadd7"
        transform="rotate(12 304 251)"
      />
      <path
        d="M320 276h26m-13-13v26"
        stroke="white"
        strokeWidth="5"
        strokeLinecap="round"
      />
      <circle cx="324" cy="61" r="8" fill="#f4ad5b" />
      <circle cx="90" cy="211" r="6" fill="#5fadd7" />
      <path d="m350 196 4 9 9 4-9 4-4 9-4-9-9-4 9-4z" fill="#edb24e" />
      <path d="M173 343q15-28 35 0m41 0q14-31 29 0" fill="#45ac7d" />
    </svg>
  );
}

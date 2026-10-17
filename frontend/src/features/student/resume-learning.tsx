import Link from "next/link";
import { ArrowRight, BookOpen, PencilLine, Sparkles } from "lucide-react";
import type { ResumeItem } from "@/lib/types";
import styles from "./resume-learning.module.css";

export function resumePath(item: Pick<ResumeItem, "kind" | "id">) {
  if (item.kind === "ai") return `/ai-academy/lessons/${item.id}`;
  return `/student/${item.kind === "lesson" ? "lessons" : "attempts"}/${item.id}`;
}

const names = {
  lesson: "Bài đang đọc",
  practice: "Bài đang làm",
  ai: "Bài AI đang học",
};
const icons = { lesson: BookOpen, practice: PencilLine, ai: Sparkles };

export function ResumeLearning({ items }: { items: ResumeItem[] }) {
  if (!items.length) return null;
  return (
    <section className={`panel ${styles.resume}`} aria-label="Việc học đang dở">
      <h2>Bài em đang học</h2>
      <div className={styles.cards}>
        {items.map((item) => {
          const Icon = icons[item.kind];
          return (
            <Link
              className={styles.card}
              key={`${item.kind}-${item.id}`}
              href={resumePath(item)}
            >
              <Icon size={24} aria-hidden="true" />
              <div>
                <small>
                  {names[item.kind]} · Lớp {item.grade}
                </small>
                <h3>{item.title}</h3>
                <p>
                  {item.kind === "ai" && item.step_count
                    ? `Bước ${Math.min((item.next_step ?? 0) + 1, item.step_count)}/${item.step_count}`
                    : item.subject_name}
                </p>
              </div>
              <ArrowRight size={20} aria-hidden="true" />
            </Link>
          );
        })}
      </div>
    </section>
  );
}

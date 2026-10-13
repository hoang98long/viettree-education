import {
  BookOpen,
  Check,
  Eye,
  Flag,
  Lightbulb,
  ListChecks,
  MousePointer2,
  Sparkles,
} from "lucide-react";
import type { Step } from "./types";

const stepIcons = {
  story: Eye,
  illustrated_explanation: BookOpen,
  flip_card: Lightbulb,
  activity: MousePointer2,
  quiz: ListChecks,
  reflection: Sparkles,
  summary: Flag,
  project_task: Flag,
};

export function StepJourney({
  steps,
  current,
  nextStep,
  completed,
}: {
  steps: Step[];
  current: number;
  nextStep: number;
  completed: boolean;
}) {
  return (
    <ol className="academy-step-journey" aria-label="Hành trình bài AI">
      {steps.map((step, index) => {
        const done = completed || index < nextStep;
        const Icon = done
          ? Check
          : stepIcons[step.kind as keyof typeof stepIcons] || BookOpen;
        return (
          <li
            key={step.id}
            aria-current={index === current ? "step" : undefined}
            className={done ? "done" : ""}
          >
            <span className="journey-symbol" title={step.title}>
              <Icon aria-hidden size={22} />
            </span>
            <span className="journey-label">{index + 1}</span>
            <span className="sr-only">
              {step.title} ·{" "}
              {done ? "đã xong" : index === current ? "đang học" : "chưa học"}
            </span>
          </li>
        );
      })}
    </ol>
  );
}

"use client";
import { useParams } from "next/navigation";
import { Journey, GameCenter } from "@/features/academy/home";
import { LessonPlayer } from "@/features/academy/player";
import { ClassificationLab, PromptBuilder } from "@/features/academy/lab";
import { ProjectWorkspace, Portfolio } from "@/features/academy/creative";
import { LessonTutor } from "@/features/academy/tutor";
import NotFound from "@/app/not-found";
import { AcademyFeatureGate } from "@/features/academy/shared";
export default function Page() {
  const { path } = useParams<{ path: string[] }>();
  if (path.length === 2 && path[0] === "lessons")
    return <LessonPlayer key={path[1]} id={path[1]} />;
  if (path.length === 2 && path[0] === "grades" && /^[1-5]$/.test(path[1]))
    return <Journey grade={Number(path[1])} />;
  if (path.length === 1)
    switch (path[0]) {
      case "lab":
        return (
          <AcademyFeatureGate feature="academy.lab">
            <ClassificationLab />
            <PromptBuilder />
          </AcademyFeatureGate>
        );
      case "games":
        return <GameCenter />;
      case "creative-studio":
        return (
          <AcademyFeatureGate feature="academy.studio">
            <ProjectWorkspace studio />
          </AcademyFeatureGate>
        );
      case "projects":
        return (
          <AcademyFeatureGate feature="academy.studio">
            <ProjectWorkspace />
          </AcademyFeatureGate>
        );
      case "portfolio":
        return <Portfolio />;
      case "ai-tutor":
        return <LessonTutor />;
    }
  return <NotFound />;
}

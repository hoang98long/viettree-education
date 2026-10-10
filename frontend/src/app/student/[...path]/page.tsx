"use client";
import { useParams } from "next/navigation";
import {
  AssessmentPage,
  AttemptPage,
  Grades,
  HistoryPage,
  LessonPage,
  ProfilePage,
  ProgressPage,
  ResultPage,
  StudentDashboard,
  SubjectPage,
} from "@/features/student";
import NotFound from "@/app/not-found";
import { LearningPlanPage } from "@/features/learning-plan";
import { MembershipPage } from "@/features/membership";
import { PracticeLibrary } from "@/features/practice-library";
import { VipLibraryPage, VipMistakesPage, VipReportPage } from "@/features/vip";
import { ThinkingPage } from "@/features/curriculum-extension";
export default function Page() {
  const { path } = useParams<{ path: string[] }>();
  if (path.length === 1)
    switch (path[0]) {
      case "dashboard":
        return <StudentDashboard />;
      case "grades":
        return <Grades />;
      case "history":
        return <HistoryPage />;
      case "progress":
        return <ProgressPage />;
      case "profile":
        return <ProfilePage />;
      case "learning-plan":
        return <LearningPlanPage />;
      case "membership":
        return <MembershipPage />;
      case "practice":
        return <PracticeLibrary />;
      case "vip":
        return <VipLibraryPage />;
      case "thinking":
        return <ThinkingPage />;
    }
  if (path.length === 2)
    switch (path[0]) {
      case "vip":
        if (path[1] === "mistakes") return <VipMistakesPage />;
        if (path[1] === "report") return <VipReportPage />;
        return <NotFound />;
      case "subjects":
        return <SubjectPage key={path[1]} code={path[1]} />;
      case "lessons":
        return <LessonPage key={path[1]} id={path[1]} />;
      case "assessments":
        return <AssessmentPage key={path[1]} id={path[1]} />;
      case "attempts":
        return <AttemptPage key={path[1]} id={path[1]} />;
      case "results":
        return <ResultPage key={path[1]} id={path[1]} />;
    }
  return <NotFound />;
}

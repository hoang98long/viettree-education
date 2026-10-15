"use client";
import { useParams } from "next/navigation";
import { AssessmentPage } from "@/features/student/assessment";
import { AttemptPage } from "@/features/student/attempt";
import { Grades, SubjectPage } from "@/features/student/catalog";
import { HistoryPage } from "@/features/student/history";
import { LessonPage } from "@/features/student/lesson";
import { LessonLibraryPage } from "@/features/student/lesson-library";
import { ProfilePage } from "@/features/student/profile";
import { ProgressPage } from "@/features/student/progress";
import { ResultPage } from "@/features/student/result";
import { StudentDashboard } from "@/features/student/dashboard";
import NotFound from "@/app/not-found";
import { LearningPlanPage } from "@/features/student/learning-plan";
import { MembershipPage } from "@/features/membership/pages";
import { PracticeLibrary } from "@/features/student/practice-library";
import {
  VipLibraryPage,
  VipMistakesPage,
  VipReportPage,
} from "@/features/vip/workspace";
import { ThinkingPage } from "@/features/curriculum/thinking";
import { StudentClassroom } from "@/features/classrooms/student";
export default function Page() {
  const { path } = useParams<{ path: string[] }>();
  if (path.length === 1)
    switch (path[0]) {
      case "classroom":
        return <StudentClassroom />;
      case "dashboard":
        return <StudentDashboard />;
      case "grades":
        return <Grades />;
      case "lessons":
        return <LessonLibraryPage />;
      case "saved-lessons":
        return <LessonLibraryPage savedOnly />;
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

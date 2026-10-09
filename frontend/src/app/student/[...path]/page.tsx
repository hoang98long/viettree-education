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
    }
  if (path.length === 2)
    switch (path[0]) {
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

"use client";
import { useParams } from "next/navigation";
import {
  AdminDashboard,
  AssessmentsPage,
  CurriculumPage,
  QuestionsPage,
  SettingsPage,
  StudentsPage,
} from "@/features/admin";
import NotFound from "@/app/not-found";
import { AdminMembershipPage } from "@/features/membership";
import { ContentAccessPage } from "@/features/content-access";
import { QuestionEditorPage, AssessmentEditorPage } from "@/features/authoring";
import { LessonEditorPage, LessonsAdminPage } from "@/features/lesson-studio";
export default function Page() {
  const { path } = useParams<{ path: string[] }>();
  if (path.join("/") === "questions/new") return <QuestionEditorPage />;
  if (path.join("/") === "assessments/new") return <AssessmentEditorPage />;
  if (path.join("/") === "lessons/new") return <LessonEditorPage />;
  if (path.length === 3 && path[2] === "edit") {
    if (path[0] === "lessons")
      return <LessonEditorPage key={path[1]} id={path[1]} />;
    if (path[0] === "questions")
      return <QuestionEditorPage key={path[1]} id={path[1]} />;
    if (path[0] === "assessments")
      return <AssessmentEditorPage key={path[1]} id={path[1]} />;
  }
  if (path.length === 3 && path[0] === "students" && path[2] === "membership")
    return <AdminMembershipPage key={path[1]} id={path[1]} />;
  if (path.length === 1)
    switch (path[0]) {
      case "dashboard":
        return <AdminDashboard />;
      case "analytics":
        return <AdminDashboard analytics />;
      case "students":
        return <StudentsPage />;
      case "content-access":
        return <ContentAccessPage />;
      case "questions":
        return <QuestionsPage />;
      case "curriculum":
        return <CurriculumPage />;
      case "lessons":
        return <LessonsAdminPage />;
      case "assessments":
        return <AssessmentsPage />;
      case "settings":
        return <SettingsPage />;
    }
  return <NotFound />;
}

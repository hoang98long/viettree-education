"use client";
import { useParams } from "next/navigation";
import {
  AdminDashboard,
  AssessmentsPage,
  AuthoringScaffold,
  CurriculumPage,
  QuestionsPage,
  SettingsPage,
  StudentsPage,
} from "@/features/admin";
import NotFound from "@/app/not-found";
export default function Page() {
  const { path } = useParams<{ path: string[] }>();
  if (path.join("/") === "questions/new") return <AuthoringScaffold />;
  if (path.length === 1)
    switch (path[0]) {
      case "dashboard":
        return <AdminDashboard />;
      case "analytics":
        return <AdminDashboard analytics />;
      case "students":
        return <StudentsPage />;
      case "questions":
        return <QuestionsPage />;
      case "curriculum":
        return <CurriculumPage />;
      case "assessments":
        return <AssessmentsPage />;
      case "settings":
        return <SettingsPage />;
    }
  return <NotFound />;
}

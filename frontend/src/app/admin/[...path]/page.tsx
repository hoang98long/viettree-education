"use client";
import { useParams } from "next/navigation";
import { AdminDashboard } from "@/features/admin/dashboard";
import { AssessmentsPage } from "@/features/admin/assessments";
import { CurriculumPage } from "@/features/admin/curriculum";
import { QuestionsPage } from "@/features/admin/questions";
import { SettingsPage } from "@/features/admin/settings";
import { StudentsPage } from "@/features/admin/students";
import NotFound from "@/app/not-found";
import { AdminMembershipPage } from "@/features/membership/pages";
import { ContentAccessPage } from "@/features/membership/content-access";
import { QuestionEditorPage } from "@/features/authoring/question-editor";
import { AssessmentEditorPage } from "@/features/authoring/assessment-editor";
import { LessonEditorPage } from "@/features/lessons/editor";
import { LessonsAdminPage } from "@/features/lessons/catalog";
import { AccountsPage } from "@/features/accounts/catalog";
import { AccountEditorPage } from "@/features/accounts/editor";
import { SystemStatusPage } from "@/features/admin/system-status";
import { AcademyAdmin } from "@/features/academy/admin";
import { ClassroomsPage } from "@/features/classrooms/catalog";
import { VipPricing } from "@/features/membership/pricing";
export default function Page() {
  const { path } = useParams<{ path: string[] }>();
  if (path.join("/") === "questions/new") return <QuestionEditorPage />;
  if (path.join("/") === "assessments/new") return <AssessmentEditorPage />;
  if (path.join("/") === "lessons/new") return <LessonEditorPage />;
  if (path.join("/") === "accounts/new") return <AccountEditorPage />;
  if (path.length === 3 && path[2] === "edit") {
    if (path[0] === "accounts")
      return <AccountEditorPage key={path[1]} id={path[1]} />;
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
      case "classes":
        return <ClassroomsPage />;
      case "vip-pricing":
        return <VipPricing admin />;
      case "dashboard":
        return <AdminDashboard />;
      case "analytics":
        return <AdminDashboard analytics />;
      case "students":
        return <StudentsPage />;
      case "accounts":
        return <AccountsPage />;
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
      case "system":
        return <SystemStatusPage />;
      case "ai-academy":
        return <AcademyAdmin />;
    }
  return <NotFound />;
}

import { AcademyLayout } from "@/features/academy/shared";
import "@/features/academy/academy.css";
export default function Layout({ children }: { children: React.ReactNode }) {
  return <AcademyLayout>{children}</AcademyLayout>;
}

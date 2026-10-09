import { Shell } from "@/components/shell";
export default function Layout({ children }: { children: React.ReactNode }) {
  return <Shell role="student">{children}</Shell>;
}

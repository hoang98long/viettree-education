"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { createContext, useContext } from "react";
import {
  BookOpen,
  ChartNoAxesCombined,
  Clock,
  GraduationCap,
  Home,
  LogOut,
  Settings,
  Users,
  ListChecks,
  Plus,
  UserRound,
} from "lucide-react";
import { api } from "@/lib/api";
import type { User } from "@/lib/types";
import { useResource } from "@/hooks/use-resource";
import { Brand, ErrorState, Loading } from "./ui";

const UserContext = createContext<User | null>(null);
export function useUser() {
  return useContext(UserContext)!;
}
const studentMenu = [
  ["dashboard", "Góc học tập", Home],
  ["grades", "Khám phá lớp học", GraduationCap],
  ["history", "Lịch sử luyện tập", Clock],
  ["progress", "Cây năng lực", ChartNoAxesCombined],
  ["profile", "Hồ sơ của em", UserRound],
] as const;
const adminMenu = [
  ["dashboard", "Tổng quan", Home],
  ["students", "Học sinh", Users],
  ["curriculum", "Chương trình", BookOpen],
  ["questions", "Ngân hàng câu hỏi", ListChecks],
  ["questions/new", "Tạo bài tập", Plus],
  ["assessments", "Bài luyện tập", GraduationCap],
  ["analytics", "Thống kê", ChartNoAxesCombined],
  ["settings", "Cài đặt", Settings],
] as const;
export function Shell({
  role,
  children,
}: {
  role: "student" | "admin" | "teacher" | "guardian";
  children: React.ReactNode;
}) {
  const { data: user, error, loading, retry } = useResource<User>("/auth/me");
  const path = usePathname();
  const router = useRouter();
  async function logout() {
    try {
      await api("/auth/logout", { method: "POST" });
      router.push("/login");
    } catch (e) {
      window.alert((e as Error).message);
    }
  }
  if (loading)
    return (
      <main className="standalone">
        <Loading />
      </main>
    );
  if (error || !user)
    return (
      <main className="standalone">
        <ErrorState message={error} retry={retry} />
      </main>
    );
  if (!user.roles.includes(role))
    return (
      <main className="standalone">
        <h1>403 · Chưa có quyền truy cập</h1>
        <p>Trang này dành cho vai trò {role}.</p>
        <Link
          className="button"
          href={
            user.roles.includes("admin")
              ? "/admin/dashboard"
              : "/student/dashboard"
          }
        >
          Về trang của bạn
        </Link>
      </main>
    );
  const menu =
    role === "admin" ? adminMenu : role === "student" ? studentMenu : [];
  return (
    <UserContext.Provider value={user}>
      <div className={`app-shell ${role}`}>
        <aside className="sidebar">
          <Brand />
          <span className="sidebar-label">
            {role === "admin" ? "KHÔNG GIAN QUẢN TRỊ" : "MỖI NGÀY MỘT KHÁM PHÁ"}
          </span>
          <nav aria-label="Điều hướng chính">
            {menu.map(([href, label, Icon]) => (
              <Link
                key={href}
                href={`/${role}/${href}`}
                className={path === `/${role}/${href}` ? "active" : ""}
              >
                <Icon size={20} />
                {label}
              </Link>
            ))}
            {role === "teacher" && (
              <Link href="/teacher/questions/new">
                <Plus />
                Tạo bài tập
              </Link>
            )}
          </nav>
          <div className="sidebar-footer">
            <span className="avatar">{user.display_name.charAt(0)}</span>
            <div>
              <strong>{user.display_name}</strong>
              <small>{user.username}</small>
            </div>
            <button aria-label="Đăng xuất" onClick={logout}>
              <LogOut size={19} />
            </button>
          </div>
        </aside>
        <div className="main-column">
          <header className="topbar">
            <span>
              VietTree Education{" "}
              <span className="muted">
                /{" "}
                {role === "admin"
                  ? "Quản trị"
                  : role === "student"
                    ? "Học sinh"
                    : role === "teacher"
                      ? "Giáo viên"
                      : "Phụ huynh"}
              </span>
            </span>
            <span className="pill">Học điều hay, lớn mỗi ngày 🌱</span>
            <button
              className="button secondary small"
              onClick={logout}
              aria-label="Đăng xuất"
            >
              <LogOut size={17} />
              <span>Đăng xuất</span>
            </button>
          </header>
          <main id="main" className="content">
            {children}
          </main>
          <footer className="app-footer">
            VietTree Education · Không gian học tập an toàn và riêng tư
          </footer>
        </div>
      </div>
    </UserContext.Provider>
  );
}

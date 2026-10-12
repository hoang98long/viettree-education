"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { createContext, useContext, useEffect, useState } from "react";
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
  Crown,
  LockKeyhole,
  Lightbulb,
  ShieldCheck,
  Trophy,
} from "lucide-react";
import { api } from "@/lib/api";
import type { TextSize, User } from "@/lib/types";
import { homeFor, useSession } from "@/lib/session";
import { Brand, ErrorState, Loading } from "./ui";

const UserContext = createContext<User | null>(null);
export function useUser() {
  return useContext(UserContext)!;
}
const AccessibilityContext = createContext<{
  textSize: TextSize;
  saveTextSize: (size: TextSize) => Promise<void>;
} | null>(null);
export function useAccessibility() {
  return useContext(AccessibilityContext)!;
}
const studentMenu = [
  ["dashboard", "Góc học tập", Home],
  ["learning-plan", "Kế hoạch học", ListChecks],
  ["grades", "Khám phá lớp học", GraduationCap],
  ["practice", "Thư viện luyện tập", BookOpen],
  ["thinking", "Góc tư duy", Lightbulb],
  ["history", "Lịch sử luyện tập", Clock],
  ["progress", "Cây năng lực", ChartNoAxesCombined],
  ["profile", "Hồ sơ của em", UserRound],
  ["membership", "Gói học của em", Crown],
  ["classroom", "Lớp và thành tích", Trophy],
  ["vip", "Góc học VIP", Crown],
] as const;
const adminMenu = [
  ["dashboard", "Tổng quan", Home],
  ["accounts", "Quản trị tài khoản", UserRound],
  ["students", "Học sinh", Users],
  ["classes", "Lớp và giao bài", GraduationCap],
  ["vip-pricing", "Giá VIP và ưu đãi", Crown],
  ["content-access", "Quyền nội dung", LockKeyhole],
  ["curriculum", "Chương trình", BookOpen],
  ["lessons", "Quản lý bài học", BookOpen],
  ["questions", "Ngân hàng câu hỏi", ListChecks],
  ["questions/new", "Tạo câu hỏi", Plus],
  ["assessments/new", "Tạo bài tập", Plus],
  ["assessments", "Bài luyện tập", GraduationCap],
  ["analytics", "Thống kê", ChartNoAxesCombined],
  ["settings", "Cài đặt", Settings],
  ["system", "Kiểm tra hệ thống", ShieldCheck],
  ["ai-academy", "AI Academy", Lightbulb],
] as const;
export function Shell({
  role,
  children,
}: {
  role: "student" | "admin" | "teacher" | "guardian";
  children: React.ReactNode;
}) {
  const { user, error, loading, refresh, clear } = useSession();
  const path = usePathname();
  const router = useRouter();
  const [chosenSize, setChosenSize] = useState<TextSize | null>(null);
  useEffect(() => {
    if (!loading && !user && !error) router.replace("/login");
    if (user?.must_change_password) router.replace("/account/security");
  }, [loading, user, error, router]);
  const textSize = chosenSize ?? user?.text_size ?? "comfortable";
  async function saveTextSize(size: TextSize) {
    await api("/students/me/accessibility", {
      method: "PUT",
      body: JSON.stringify({ text_size: size }),
    });
    setChosenSize(size);
  }
  async function logout() {
    try {
      await api("/auth/logout", { method: "POST" });
      clear();
      router.replace("/login");
      router.refresh();
    } catch (e) {
      window.alert((e as Error).message);
    }
  }
  if (loading || user?.must_change_password)
    return (
      <main className="standalone">
        <Loading />
      </main>
    );
  if (error || !user)
    return (
      <main className="standalone">
        {error ? (
          <ErrorState message={error} retry={() => void refresh(true)} />
        ) : (
          <Loading />
        )}
      </main>
    );
  if (!user.roles.includes(role))
    return (
      <main className="standalone">
        <h1>403 · Chưa có quyền truy cập</h1>
        <p>Trang này dành cho vai trò {role}.</p>
        <Link className="button" href={homeFor(user)}>
          Về trang của bạn
        </Link>
      </main>
    );
  const menu =
    role === "admin" ? adminMenu : role === "student" ? studentMenu : [];
  return (
    <UserContext.Provider value={user}>
      <AccessibilityContext.Provider value={{ textSize, saveTextSize }}>
        <div className={`app-shell ${role}`} data-text-size={textSize}>
          <aside className="sidebar">
            <Brand href={`/${role}/dashboard`} />
            <span className="sidebar-label">
              {role === "admin"
                ? "KHÔNG GIAN QUẢN TRỊ"
                : "MỖI NGÀY MỘT KHÁM PHÁ"}
            </span>
            <nav aria-label="Điều hướng chính">
              {role === "student" && (
                <Link href="/ai-academy">
                  <Lightbulb />
                  AI Academy
                </Link>
              )}
              {role === "teacher" && (
                <Link href="/teacher/ai-academy">
                  <Lightbulb />
                  AI Academy
                </Link>
              )}
              {role === "guardian" && (
                <Link href="/guardian/ai-academy">
                  <Lightbulb />
                  AI Academy
                </Link>
              )}
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
                <Link href="/teacher/classes">
                  <GraduationCap /> Lớp và thành tích
                </Link>
              )}
              {role === "teacher" && (
                <Link href="/teacher/questions/new">
                  <Plus />
                  Tạo bài tập
                </Link>
              )}
            </nav>
            <Link className="button secondary small" href="/account/security">
              Bảo mật tài khoản
            </Link>
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
      </AccessibilityContext.Provider>
    </UserContext.Provider>
  );
}

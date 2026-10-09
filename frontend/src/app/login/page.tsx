"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, ShieldCheck } from "lucide-react";
import { Brand, TreeArt } from "@/components/ui";
import { api } from "@/lib/api";
import type { User } from "@/lib/types";
export default function Login() {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const router = useRouter();
  return (
    <main id="main" className="login-page">
      <div className="login-story">
        <Brand />
        <div>
          <span className="eyebrow">CHÀO MỪNG EM TRỞ LẠI</span>
          <h1>
            Góc học tập nhỏ.
            <br />
            Khám phá thật to.
          </h1>
          <TreeArt />
        </div>
        <p>
          <ShieldCheck size={18} /> Dữ liệu học tập của em luôn được giữ riêng
          tư.
        </p>
      </div>
      <section className="login-form">
        <span className="eyebrow">VIETTREE EDUCATION</span>
        <h2>Đăng nhập</h2>
        <p>Hành trình hôm nay đang chờ em!</p>
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            const fields = new FormData(e.currentTarget);
            setBusy(true);
            setError("");
            try {
              const user = await api<User>("/auth/login", {
                method: "POST",
                body: JSON.stringify({
                  username: fields.get("username"),
                  password: fields.get("password"),
                }),
              });
              const role = ["admin", "student", "teacher", "guardian"].find(
                (r) => user.roles.includes(r),
              );
              router.replace(role ? `/${role}/dashboard` : "/403");
            } catch (err) {
              setError((err as Error).message);
            } finally {
              setBusy(false);
            }
          }}
        >
          <label htmlFor="username">Tên đăng nhập</label>
          <input
            id="username"
            name="username"
            autoComplete="username"
            required
            minLength={3}
            maxLength={80}
            placeholder="Tên đăng nhập của em"
          />
          <label htmlFor="password">Mật khẩu</label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            maxLength={256}
            placeholder="Nhập mật khẩu"
          />
          {error && (
            <div role="alert" className="notice error">
              {error}
            </div>
          )}
          <button className="button" disabled={busy}>
            {busy ? "Đang đăng nhập…" : "Vào học thôi"}
            <ArrowRight size={18} />
          </button>
        </form>
        <p className="muted">
          Nếu quên mật khẩu, em hãy nhờ giáo viên hoặc quản trị viên hỗ trợ.
        </p>
      </section>
    </main>
  );
}

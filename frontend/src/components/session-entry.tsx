"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { homeFor, useSession } from "@/lib/session";
import { Brand } from "./ui";

export function SessionBrand() {
  const { user } = useSession();
  return <Brand href={user ? homeFor(user) : "/"} />;
}

export function SessionEntry({
  children,
  className = "button",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  const { user, loading, error, refresh } = useSession();
  if (loading)
    return (
      <span className={className} role="status">
        Đang kiểm tra phiên…
      </span>
    );
  if (error)
    return (
      <button className={className} onClick={() => void refresh(true)}>
        Thử lại kết nối
      </button>
    );
  return (
    <Link className={className} href={user ? homeFor(user) : "/login"}>
      {user
        ? user.roles.includes("admin")
          ? "Về trang quản trị"
          : "Vào góc học tập"
        : children}
      <ArrowRight size={18} />
    </Link>
  );
}

"use client";
import Link from "next/link";
import type { User } from "@/lib/types";
import { PageTitle } from "@/components/ui";
import { Data } from "@/features/admin/shared";

export function SettingsPage() {
  return (
    <>
      <PageTitle title="Cài đặt và vận hành" />
      <Link className="button secondary" href="/admin/system">
        Kiểm tra hệ thống
      </Link>
      <section className="panel">
        <h2>Thông tin phiên bản MVP</h2>
        <p>
          Giao diện tiếng Việt · Chương trình lớp 1–5 · Nội dung lớp 1–5: Toán,
          Tiếng Việt, Tiếng Anh.
        </p>
        <p>
          Cá nhân hóa rule_v1: dựa trên câu trả lời đã chấm và lịch ôn tập, có
          độ tin cậy theo lượng dữ liệu.
        </p>
        <p>
          Tài khoản demo chỉ dành cho local development. Cấu hình kết nối và mật
          khẩu được quản lý ngoài giao diện bằng biến môi trường.
        </p>
        <p>
          Hướng dẫn seed, backup, migration và chạy kiểm thử nằm trong README
          của dự án.
        </p>
      </section>
      <section className="panel section-title">
        <h2>Tài khoản hệ thống</h2>
        <Link className="button" href="/admin/accounts">
          Mở quản trị tài khoản
        </Link>
        <Link className="button secondary" href="/account/security">
          Bảo mật tài khoản của tôi
        </Link>
        <Data<User[]> path="/admin/users">
          {(users) =>
            users.map((user) => (
              <div className="list-row" key={user.id}>
                <strong>{user.display_name}</strong>
                <span>{user.username}</span>
              </div>
            ))
          }
        </Data>
      </section>
    </>
  );
}

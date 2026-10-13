"use client";
import type { User } from "@/lib/types";
import { PageTitle } from "@/components/ui";
import { TextSizeControl } from "@/components/text-size-control";
import { MembershipSummary } from "@/features/membership/pages";
import { Resource } from "@/features/student/shared";

export function ProfilePage() {
  return (
    <Resource<
      User & {
        current_grade: number;
        learning_preferences: Record<string, unknown>;
      }
    > path="/students/me/profile">
      {(data) => (
        <>
          <PageTitle title="Hồ sơ của em" />
          <section className="panel profile-card">
            <span className="avatar large">{data.display_name.charAt(0)}</span>
            <h2>{data.display_name}</h2>
            <dl>
              <dt>Tên đăng nhập</dt>
              <dd>{data.username}</dd>
              <dt>Lớp đang học</dt>
              <dd>Lớp {data.current_grade}</dd>
            </dl>
            <p className="muted">
              Để sửa thông tin, em hãy nhờ quản trị viên hỗ trợ. Không cần cung
              cấp ngày sinh, địa chỉ hay số điện thoại.
            </p>
          </section>
          <TextSizeControl />
          <MembershipSummary />
        </>
      )}
    </Resource>
  );
}

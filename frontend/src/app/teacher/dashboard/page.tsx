import Link from "next/link";
import { PageTitle } from "@/components/ui";
export default function Page() {
  return (
    <>
      <PageTitle
        title="Không gian giáo viên"
        description="Phân quyền đã được chuẩn bị. Chức năng quản lý lớp và giao bài đang được phát triển."
      />
      <Link className="button secondary" href="/teacher/questions/new">
        Xem khung tạo bài tập
      </Link>
    </>
  );
}

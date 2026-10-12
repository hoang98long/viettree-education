import Link from "next/link";
import { PageTitle } from "@/components/ui";
export default function Page() {
  return (
    <>
      <PageTitle
        title="Không gian giáo viên"
        description="Theo dõi lớp được phân công, giao bài AI Academy và nhận xét sản phẩm học sinh."
      />
      <Link className="button" href="/teacher/ai-academy">
        Lớp học AI Academy
      </Link>
      <Link className="button secondary" href="/teacher/questions/new">
        Xem khung tạo bài tập
      </Link>
    </>
  );
}

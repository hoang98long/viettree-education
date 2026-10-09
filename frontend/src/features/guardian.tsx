"use client";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import { membershipTime } from "@/features/membership";
import type { Membership } from "@/lib/types";

type Child = { id: string; display_name: string; current_grade: number };
function ChildMembership({ child }: { child: Child }) {
  const resource = useResource<Membership>(
    `/guardian/students/${child.id}/membership`,
  );
  return (
    <section className="panel">
      <h2>
        {child.display_name} · Lớp {child.current_grade}
      </h2>
      {resource.loading ? (
        <Loading />
      ) : resource.error ? (
        <ErrorState message={resource.error} retry={resource.retry} />
      ) : (
        <>
          <p>
            Gói học:{" "}
            <strong>
              {resource.data?.plan_code === "vip" ? "VIP" : "Miễn phí"}
            </strong>
          </p>
          {resource.data?.ends_at && (
            <p>
              {resource.data.status === "active"
                ? "Có hiệu lực đến"
                : "Kỳ VIP trước kết thúc"}
              : {membershipTime(resource.data.ends_at)} (giờ Việt Nam)
            </p>
          )}
          <p>
            Để cấp hoặc gia hạn VIP, phụ huynh vui lòng liên hệ đơn vị quản lý
            và cung cấp tên tài khoản của học sinh.
          </p>
        </>
      )}
    </section>
  );
}
export function GuardianDashboard() {
  const resource = useResource<Child[]>("/guardian/students");
  return (
    <>
      <PageTitle
        title="Không gian phụ huynh"
        description="Theo dõi gói học của các con đã được xác minh liên kết với tài khoản của phụ huynh."
      />
      {resource.loading ? (
        <Loading />
      ) : resource.error ? (
        <ErrorState message={resource.error} retry={resource.retry} />
      ) : resource.data?.length ? (
        <div className="two-columns">
          {resource.data.map((child) => (
            <ChildMembership key={child.id} child={child} />
          ))}
        </div>
      ) : (
        <Empty>
          Tài khoản chưa có liên kết học sinh được xác minh. Phụ huynh vui lòng
          liên hệ đơn vị quản lý để được hỗ trợ.
        </Empty>
      )}
    </>
  );
}

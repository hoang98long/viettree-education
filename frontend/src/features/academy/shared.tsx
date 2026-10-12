"use client";
import Image from "next/image";
import Link from "next/link";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession, homeFor } from "@/lib/session";
import { ErrorState, Loading, Brand } from "@/components/ui";
import { useMembership, LockedContent } from "../membership";

export function AcademyFeatureGate({
  feature,
  children,
}: {
  feature: string;
  children: React.ReactNode;
}) {
  const membership = useMembership();
  if (membership.loading) return <Loading />;
  if (membership.error)
    return <ErrorState message={membership.error} retry={membership.retry} />;
  if (!membership.data?.features.includes(feature))
    return (
      <>
        <LockedContent message="Phòng thực hành và xưởng sáng tạo dành cho VIP. Em vẫn học được các bài nhập môn miễn phí." />
        <Link className="button secondary" href="/ai-academy">
          Về bài AI miễn phí
        </Link>
      </>
    );
  return <>{children}</>;
}

export function AcademyImage({
  code,
  alt,
  small = false,
}: {
  code: string;
  alt: string;
  small?: boolean;
}) {
  return (
    <Image
      unoptimized={!code.startsWith("upload-")}
      loader={({ src, width }) =>
        `${src}?variant=${width <= 256 ? "thumbnail" : width <= 768 ? "responsive" : "original"}`
      }
      sizes={
        small
          ? "(max-width: 480px) 45vw, 230px"
          : "(max-width: 800px) 90vw, 600px"
      }
      loading="lazy"
      src={`/api/v1/ai-academy/media/${encodeURIComponent(code)}`}
      alt={alt}
      width={small ? 300 : 600}
      height={small ? 300 : 360}
      className={small ? "academy-icon" : "academy-image"}
      draggable={false}
    />
  );
}
export function AcademyLayout({ children }: { children: React.ReactNode }) {
  const { user, loading, error, refresh } = useSession();
  const router = useRouter();
  useEffect(() => {
    if (!loading && !user && !error) router.replace("/login");
    if (user?.must_change_password) router.replace("/account/security");
  }, [user, loading, error, router]);
  if (loading || !user || user.must_change_password)
    return (
      <main className="standalone">
        {error ? (
          <ErrorState message={error} retry={() => void refresh(true)} />
        ) : (
          <Loading />
        )}
      </main>
    );
  if (!user.roles.includes("student"))
    return (
      <main className="standalone">
        <h1>AI Academy dành cho học sinh</h1>
        <Link
          className="button"
          href={
            user.roles.includes("admin")
              ? "/admin/ai-academy"
              : user.roles.includes("teacher")
                ? "/teacher/ai-academy"
                : "/guardian/ai-academy"
          }
        >
          Mở không gian của bạn
        </Link>
      </main>
    );
  return (
    <div
      className="academy-page"
      data-text-size={user.text_size || "comfortable"}
    >
      <header className="academy-header">
        <Brand href={homeFor(user)} />
        <Link href="/ai-academy" className="button secondary">
          AI Academy
        </Link>
        <Link href={homeFor(user)}>Góc học tập</Link>
      </header>
      <nav aria-label="Điều hướng AI Academy" className="academy-tabs">
        {[
          ["", "Hành trình"],
          ["games", "Trò chơi"],
          ["lab", "Phòng thí nghiệm"],
          ["creative-studio", "Xưởng sáng tạo"],
          ["ai-tutor", "Trợ giảng"],
          ["projects", "Dự án"],
          ["portfolio", "Sản phẩm của em"],
        ].map(([path, title]) => (
          <Link key={path} href={"/ai-academy" + (path ? "/" + path : "")}>
            {title}
          </Link>
        ))}
      </nav>
      <main id="main" className="academy-main">
        {children}
      </main>
      <footer className="academy-footer">
        Mầm AI là nhân vật minh họa. Học, thử và kiểm tra · Dữ liệu mẫu · Không
        xếp hạng công khai.
      </footer>
    </div>
  );
}

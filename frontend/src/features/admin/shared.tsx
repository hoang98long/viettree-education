"use client";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Loading } from "@/components/ui";

export function Data<T>({
  path,
  children,
}: {
  path: string;
  children: (data: T) => React.ReactNode;
}) {
  const { data, error, loading, retry } = useResource<T>(path);
  if (loading) return <Loading />;
  if (error || !data) return <ErrorState message={error} retry={retry} />;
  return <>{children(data)}</>;
}

export function Pagination({
  page,
  total,
  onChange,
}: {
  page: number;
  total: number;
  onChange: (page: number) => void;
}) {
  return (
    <div className="pagination">
      <span>
        {total} bản ghi · Trang {page}/{Math.max(1, Math.ceil(total / 20))}
      </span>
      <button
        className="button secondary"
        aria-label="Trang trước"
        disabled={page === 1}
        onClick={() => onChange(page - 1)}
      >
        <ArrowLeft size={17} />
      </button>
      <button
        className="button secondary"
        aria-label="Trang sau"
        disabled={page * 20 >= total}
        onClick={() => onChange(page + 1)}
      >
        <ArrowRight size={17} />
      </button>
    </div>
  );
}

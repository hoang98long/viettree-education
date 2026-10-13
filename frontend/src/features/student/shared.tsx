"use client";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Loading } from "@/components/ui";

export function Resource<T>({
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

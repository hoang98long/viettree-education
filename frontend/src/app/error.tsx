"use client";
import { ErrorState } from "@/components/ui";
export default function ErrorPage({ reset }: { reset: () => void }) {
  return (
    <main className="standalone">
      <ErrorState
        message="Trang tạm thời gặp lỗi. Em hãy thử lại nhé."
        retry={reset}
      />
    </main>
  );
}

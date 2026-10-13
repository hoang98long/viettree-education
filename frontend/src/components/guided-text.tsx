"use client";

import { useState } from "react";
import { readingPages } from "@/lib/guided-reading";
import { BlockPictures } from "./block-pictures";

export function GuidedText({
  text,
  grade,
  illustrated = false,
}: {
  text: string;
  grade?: number;
  illustrated?: boolean;
}) {
  return (
    <PagedText
      key={`${grade}:${text}`}
      text={text}
      grade={grade}
      illustrated={illustrated}
    />
  );
}

function PagedText({
  text,
  grade,
  illustrated,
}: {
  text: string;
  grade?: number;
  illustrated: boolean;
}) {
  const [page, setPage] = useState(0);
  const [full, setFull] = useState(false);
  const pages = readingPages(text, grade && grade <= 2 ? 35 : 55);
  const currentText = full ? text : pages[Math.min(page, pages.length - 1)];
  return (
    <div className="guided-text">
      {illustrated && <BlockPictures text={currentText} />}
      <p className="reading-paragraph">{currentText}</p>
      {pages.length > 1 && (
        <div className="reading-page-actions">
          {!full && (
            <>
              <button
                className="button secondary"
                disabled={page === 0}
                onClick={() => setPage(page - 1)}
              >
                Đoạn trước
              </button>
              <span aria-live="polite">
                Đoạn {page + 1}/{pages.length}
              </span>
              <button
                className="button"
                disabled={page === pages.length - 1}
                onClick={() => setPage(page + 1)}
              >
                Đọc tiếp
              </button>
            </>
          )}
          <button
            className="button secondary"
            aria-pressed={full}
            onClick={() => setFull(!full)}
          >
            {full ? "Đọc từng đoạn" : "Xem cả phần"}
          </button>
        </div>
      )}
    </div>
  );
}

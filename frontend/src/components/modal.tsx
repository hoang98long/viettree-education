"use client";
import { useEffect, useRef } from "react";
import styles from "./modal.module.css";

function tabStops(dialog: HTMLDialogElement) {
  return Array.from(
    dialog.querySelectorAll<HTMLElement>(
      "a[href], button, input:not([type='hidden']), select, textarea, summary, [tabindex], [contenteditable='true']",
    ),
  )
    .filter((element) => {
      if (
        element.tabIndex < 0 ||
        element.matches(":disabled") ||
        element.closest("[hidden], [inert], [aria-hidden='true']")
      )
        return false;
      for (
        let node: HTMLElement | null = element;
        node && node !== dialog;
        node = node.parentElement
      ) {
        const style = window.getComputedStyle(node);
        if (
          style.display === "none" ||
          ["hidden", "collapse"].includes(style.visibility)
        )
          return false;
        if (
          node instanceof HTMLDetailsElement &&
          !node.open &&
          !node.querySelector(":scope > summary")?.contains(element)
        )
          return false;
      }
      return true;
    })
    .sort(
      (left, right) =>
        (left.tabIndex || Number.MAX_SAFE_INTEGER) -
        (right.tabIndex || Number.MAX_SAFE_INTEGER),
    );
}

/** Native dialog makes the page inert; explicit Tab boundaries retain focus. */
export function Modal({
  children,
  labelledBy,
  onClose,
  closeDisabled = false,
  wide = false,
}: {
  children: React.ReactNode;
  labelledBy: string;
  onClose: () => void;
  closeDisabled?: boolean;
  wide?: boolean;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const dialog = ref.current!;
    const previous = document.activeElement;
    dialog.showModal();
    return () => {
      dialog.close();
      if (previous instanceof HTMLElement && previous.isConnected)
        previous.focus();
    };
  }, []);
  return (
    <dialog
      ref={ref}
      className={`modal ${wide ? "wide" : ""} ${styles.dialog}`}
      aria-modal="true"
      aria-labelledby={labelledBy}
      tabIndex={-1}
      onKeyDown={(event) => {
        if (
          event.key !== "Tab" ||
          event.altKey ||
          event.ctrlKey ||
          event.metaKey
        )
          return;
        const dialog = event.currentTarget;
        const stops = tabStops(dialog);
        const first = stops[0];
        const last = stops.at(-1);
        const active = document.activeElement;
        if (!first || !last) {
          event.preventDefault();
          dialog.focus();
        } else if (
          !stops.includes(active as HTMLElement) ||
          (event.shiftKey ? active === first : active === last)
        ) {
          event.preventDefault();
          (event.shiftKey ? last : first).focus();
        }
      }}
      onCancel={(event) => {
        // React owns visibility. Keep an in-flight save/submit open.
        event.preventDefault();
        if (!closeDisabled) onClose();
      }}
    >
      {children}
    </dialog>
  );
}

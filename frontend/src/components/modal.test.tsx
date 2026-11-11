import { fireEvent, render, screen } from "@testing-library/react";
import {
  afterAll,
  beforeAll,
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";
import { Modal } from "./modal";

// jsdom does not implement native dialog opening. Tab boundaries below are
// tested explicitly; native inert/backdrop still need a real browser.
const showModal = vi.fn(function (this: HTMLDialogElement) {
  this.open = true;
});
const close = vi.fn(function (this: HTMLDialogElement) {
  this.open = false;
});
const originals = Object.fromEntries(
  ["showModal", "close"].map((key) => [
    key,
    Object.getOwnPropertyDescriptor(HTMLDialogElement.prototype, key),
  ]),
);
beforeAll(() => {
  Object.defineProperties(HTMLDialogElement.prototype, {
    showModal: { configurable: true, value: showModal },
    close: { configurable: true, value: close },
  });
});
beforeEach(() => {
  showModal.mockClear();
  close.mockClear();
});
afterAll(() => {
  for (const [key, descriptor] of Object.entries(originals)) {
    if (descriptor)
      Object.defineProperty(HTMLDialogElement.prototype, key, descriptor);
    else Reflect.deleteProperty(HTMLDialogElement.prototype, key);
  }
});

function content(onClose: () => void, busy = false) {
  return (
    <Modal labelledBy="title" onClose={onClose} closeDisabled={busy}>
      <h2 id="title">Kiểm tra bài</h2>
      <button>Quay lại</button>
    </Modal>
  );
}

describe("Hộp thoại dùng chung", () => {
  it("mở modal native có tên kể cả khi nội dung chưa tải xong", () => {
    render(content(vi.fn()));
    expect(showModal).toHaveBeenCalledOnce();
    expect(
      screen.getByRole("dialog", { name: "Kiểm tra bài" }),
    ).toHaveAttribute("aria-modal", "true");
  });

  it("Escape chuyển qua callback đóng, không đóng native ngoài state React", () => {
    const onClose = vi.fn();
    render(content(onClose));
    const cancel = new Event("cancel", { bubbles: false, cancelable: true });
    fireEvent(screen.getByRole("dialog"), cancel);
    expect(cancel.defaultPrevented).toBe(true);
    expect(onClose).toHaveBeenCalledOnce();
  });

  it("không Escape trong khi lưu/nộp; mở lại quyền đóng sau khi request kết thúc", () => {
    const onClose = vi.fn();
    const view = render(content(onClose, true));
    const cancel = new Event("cancel", { cancelable: true });
    fireEvent(screen.getByRole("dialog"), cancel);
    expect(cancel.defaultPrevented).toBe(true);
    expect(onClose).not.toHaveBeenCalled();
    view.rerender(content(onClose, false));
    fireEvent(
      screen.getByRole("dialog"),
      new Event("cancel", { cancelable: true }),
    );
    expect(onClose).toHaveBeenCalledOnce();
    expect(showModal).toHaveBeenCalledOnce();
  });

  it("khôi phục focus tới nút mở khi component được đóng", () => {
    const opener = document.createElement("button");
    document.body.append(opener);
    opener.focus();
    const view = render(content(vi.fn()));
    screen.getByRole("button", { name: "Quay lại" }).focus();
    view.unmount();
    expect(close).toHaveBeenCalledOnce();
    expect(opener).toHaveFocus();
    opener.remove();
  });

  it("giữ Tab và Shift+Tab trong dialog chỉ có một nút", () => {
    render(content(vi.fn()));
    const button = screen.getByRole("button", { name: "Quay lại" });
    button.focus();
    for (const shiftKey of [false, true]) {
      const tab = new KeyboardEvent("keydown", {
        key: "Tab",
        shiftKey,
        bubbles: true,
        cancelable: true,
      });
      fireEvent(button, tab);
      expect(tab.defaultPrevented).toBe(true);
      expect(button).toHaveFocus();
    }
  });

  it("quay vòng hai đầu, bỏ qua controls disabled, hidden và tabindex âm", () => {
    render(
      <Modal labelledBy="title" onClose={vi.fn()}>
        <h2 id="title">Hai lựa chọn</h2>
        <button disabled>Đang bận</button>
        <div style={{ display: "none" }}>
          <button>Ẩn theo CSS</button>
        </div>
        <button hidden>Ẩn theo thuộc tính</button>
        <button tabIndex={-1}>Không tham gia Tab</button>
        <button>Đầu</button>
        <button>Cuối</button>
      </Modal>,
    );
    const first = screen.getByRole("button", { name: "Đầu" });
    const last = screen.getByRole("button", { name: "Cuối" });
    last.focus();
    fireEvent.keyDown(last, { key: "Tab" });
    expect(first).toHaveFocus();
    fireEvent.keyDown(first, { key: "Tab", shiftKey: true });
    expect(last).toHaveFocus();
    const forward = new KeyboardEvent("keydown", {
      key: "Tab",
      bubbles: true,
      cancelable: true,
    });
    first.focus();
    fireEvent(first, forward);
    expect(forward.defaultPrevented).toBe(false);
  });

  it("dùng chính dialog làm nơi giữ focus khi không có control khả dụng", () => {
    render(
      <Modal labelledBy="title" onClose={vi.fn()} closeDisabled>
        <h2 id="title">Đang lưu</h2>
        <button disabled>Đang lưu…</button>
      </Modal>,
    );
    const dialog = screen.getByRole("dialog");
    dialog.focus();
    fireEvent.keyDown(dialog, { key: "Tab" });
    expect(dialog).toHaveFocus();
    fireEvent.keyDown(dialog, { key: "Tab", shiftKey: true });
    expect(dialog).toHaveFocus();
  });
});

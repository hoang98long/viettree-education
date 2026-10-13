export const roles = [
  ["student", "Học sinh"],
  ["guardian", "Phụ huynh"],
  ["teacher", "Giáo viên"],
  ["admin", "Quản trị viên"],
];

export const actionNames: Record<string, string> = {
  account_created: "Tạo tài khoản",
  account_updated: "Cập nhật tài khoản",
  account_password_reset: "Đặt lại mật khẩu",
  account_password_changed: "Tự đổi mật khẩu",
  account_sessions_revoked: "Thu hồi toàn bộ phiên",
  account_other_sessions_revoked: "Đăng xuất các phiên khác",
};

export const passwordHelp =
  "Dùng ít nhất 15 ký tự, có thể là cụm vài từ dễ nhớ. Không dùng tên đăng nhập hay mật khẩu phổ biến. Mật khẩu phân biệt hoa/thường.";

export function getUserInitials(username: string): string {
  return username
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("");
}

export function getRoleLabel(role: string): string {
  switch (role) {
    case "ADMIN":
      return "Quản trị viên";
    case "USER":
      return "Nhân viên";
    case "VIEWER":
      return "Chỉ xem";
    default:
      return role;
  }
}
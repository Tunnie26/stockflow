export function formatQuantity(value: string) {
  return Number(value).toLocaleString("vi-VN", {
    maximumFractionDigits: 4,
  });
}

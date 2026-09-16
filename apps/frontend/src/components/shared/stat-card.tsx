import type { LucideIcon } from "lucide-react";

export interface StatCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon: LucideIcon;
  iconClassName?: string;
}

export function StatCard({
  title,
  value,
  description,
  icon: Icon,
  iconClassName,
}: StatCardProps) {
  return (
    <div className="group relative overflow-hidden rounded-[14px] border border-[#202C43] bg-[#0D1422] p-5 transition-all duration-200 hover:-translate-y-0.5 hover:border-[#2C3A55]">
      <div className="absolute inset-x-0 top-0 h-px bg-linear-to-r from-transparent via-[#385FC4]/40 to-transparent opacity-0 transition-opacity duration-200 group-hover:opacity-100" />

      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-sm font-medium text-[#B8C2D9]">
            {title}
          </p>

          <p className="mt-2 text-[32px] font-semibold leading-none tracking-tight text-[#F4F7FF]">
            {value}
          </p>

          {description && (
            <p className="mt-2 text-xs text-[#8490A8]">
              {description}
            </p>
          )}
        </div>

        <div
          className={`flex size-11 shrink-0 items-center justify-center rounded-xl ${iconClassName ?? "bg-[#18253A] text-[#F4F7FF]"}`}
        >
          <Icon className="size-5" strokeWidth={1.8} />
        </div>
      </div>
    </div>
  );
}
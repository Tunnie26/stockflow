import type { LucideIcon } from "lucide-react";

import { cn } from "@/lib/utils";

interface DataPanelProps {
  title: string;
  description?: string;
  icon?: LucideIcon;
  action?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  contentClassName?: string;
}

export function DataPanel({
  title,
  description,
  icon: Icon,
  action,
  children,
  className,
  contentClassName,
}: DataPanelProps) {
  return (
    <section
      className={cn(
        "rounded-2xl border border-[#202C43] bg-[#0D1422]",
        className,
      )}
    >
      <div className="flex items-center justify-between gap-4 border-b border-[#172136] px-5 py-4">
        <div className="flex min-w-0 items-center gap-3">
          {Icon && (
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[rgba(79,124,255,0.12)] text-[#4F7CFF]">
              <Icon className="h-4 w-4" />
            </div>
          )}

          <div className="min-w-0">
            <h2 className="truncate text-sm font-semibold text-[#F4F7FF]">
              {title}
            </h2>

            {description && (
              <p className="mt-0.5 truncate text-xs text-[#8490A8]">
                {description}
              </p>
            )}
          </div>
        </div>

        {action && <div className="shrink-0">{action}</div>}
      </div>

      <div className={cn("p-5", contentClassName)}>{children}</div>
    </section>
  );
}

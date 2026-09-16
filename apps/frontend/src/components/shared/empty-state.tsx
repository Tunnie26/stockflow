import type { LucideIcon } from "lucide-react";
import { Inbox } from "lucide-react";

import { cn } from "@/lib/utils";

interface EmptyStateProps {
  title: string;
  description?: string;
  icon?: LucideIcon;
  action?: React.ReactNode;
  className?: string;
}

export function EmptyState({
  title,
  description,
  icon: Icon = Inbox,
  action,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex min-h-40 flex-col items-center justify-center rounded-xl border border-dashed border-[#202C43] bg-[#090E1A] px-6 py-8 text-center",
        className,
      )}
    >
      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[rgba(79,124,255,0.08)] text-[#8490A8]">
        <Icon className="h-5 w-5" />
      </div>

      <h3 className="mt-3 text-sm font-medium text-[#F4F7FF]">{title}</h3>

      {description && (
        <p className="mt-1 max-w-sm text-xs leading-5 text-[#8490A8]">
          {description}
        </p>
      )}

      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}

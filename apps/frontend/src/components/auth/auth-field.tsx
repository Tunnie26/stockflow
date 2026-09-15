"use client";

import type { InputHTMLAttributes, ReactNode } from "react";

interface AuthFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  icon?: ReactNode;
  error?: string;
}

export function AuthField({
  label,
  icon,
  error,
  id,
  className = "",
  ...props
}: AuthFieldProps) {
  return (
    <div className="space-y-2">
      <label
        htmlFor={id}
        className="block text-sm font-medium text-[#B8C2D9]"
      >
        {label}
      </label>

      <div
        className={[
          "group relative flex h-12 items-center rounded-xl",
          "border border-[#202C43]",
          "bg-[#0D1422]/80",
          "transition-all duration-200",
          "focus-within:border-[#4F7CFF]",
          "focus-within:ring-4 focus-within:ring-[#4F7CFF]/10",
          "hover:border-[#2C3A55]",
          error ? "border-[#F0526B]" : "",
        ].join(" ")}
      >
        {icon && (
          <div className="pointer-events-none ml-4 shrink-0 text-[#8490A8] transition-colors group-focus-within:text-[#6F8FFF]">
            {icon}
          </div>
        )}

        <input
          id={id}
          aria-invalid={Boolean(error)}
          aria-describedby={error ? `${id}-error` : undefined}
          className={[
            "h-full w-full bg-transparent px-4 text-sm text-[#F4F7FF]",
            "outline-none placeholder:text-[#606C84]",
            icon ? "pl-3" : "",
            className,
          ].join(" ")}
          {...props}
        />
      </div>

      {error && (
        <p
          id={`${id}-error`}
          className="text-xs text-[#F0526B]"
        >
          {error}
        </p>
      )}
    </div>
  );
}
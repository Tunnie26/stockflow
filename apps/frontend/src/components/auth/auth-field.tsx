"use client";

import type { InputHTMLAttributes } from "react";

type AuthFieldProps = InputHTMLAttributes<HTMLInputElement> & {
  id: string;
  label: string;
  error?: string;
};

export function AuthField({
  id,
  label,
  error,
  className,
  ...props
}: AuthFieldProps) {
  return (
    <div className="space-y-2">
      <label htmlFor={id} className="block text-sm font-medium text-[#B8C2D9]">
        {label}
      </label>

      <input
        id={id}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? `${id}-error` : undefined}
        className={[
          "h-11 w-full rounded-lg border bg-[#0D1422] px-3.5 text-sm text-[#F4F7FF]",
          "outline-none transition",
          "placeholder:text-[#606C84]",
          "focus:border-[#5B82FF] focus:ring-2 focus:ring-[#5B82FF]/20",
          error ? "border-[#F0526B]" : "border-[#202C43]",
          className,
        ]
          .filter(Boolean)
          .join(" ")}
        {...props}
      />

      {error && (
        <p id={`${id}-error`} className="text-sm text-[#F0526B]" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}

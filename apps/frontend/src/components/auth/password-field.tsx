"use client";

import {
  Eye,
  EyeOff,
  LockKeyhole,
} from "lucide-react";
import { useState } from "react";

interface PasswordFieldProps {
  value: string;
  onChange: (value: string) => void;
  error?: string;
  disabled?: boolean;
}

export function PasswordField({
  value,
  onChange,
  error,
  disabled = false,
}: PasswordFieldProps) {
  const [visible, setVisible] = useState(false);

  return (
    <div className="space-y-2">
      <label
        htmlFor="password"
        className="block text-sm font-medium text-[#B8C2D9]"
      >
        Password
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
          disabled ? "cursor-not-allowed opacity-60" : "",
        ].join(" ")}
      >
        <LockKeyhole className="ml-4 size-4 shrink-0 text-[#8490A8] transition-colors group-focus-within:text-[#6F8FFF]" />

        <input
          id="password"
          type={visible ? "text" : "password"}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          disabled={disabled}
          autoComplete="current-password"
          aria-invalid={Boolean(error)}
          aria-describedby={error ? "password-error" : undefined}
          placeholder="Enter your password"
          className="h-full w-full min-w-0 bg-transparent px-3 text-sm text-[#F4F7FF] outline-none placeholder:text-[#606C84]"
        />

        <button
          type="button"
          disabled={disabled}
          onClick={() => setVisible((current) => !current)}
          aria-label={visible ? "Hide password" : "Show password"}
          className="mr-2 flex size-8 shrink-0 items-center justify-center rounded-lg text-[#8490A8] transition-colors hover:bg-[#18253A] hover:text-[#B8C2D9] disabled:pointer-events-none"
        >
          {visible ? (
            <EyeOff className="size-4" />
          ) : (
            <Eye className="size-4" />
          )}
        </button>
      </div>

      {error && (
        <p
          id="password-error"
          className="text-xs text-[#F0526B]"
        >
          {error}
        </p>
      )}
    </div>
  );
}
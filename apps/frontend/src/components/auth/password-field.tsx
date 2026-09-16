"use client";

import { forwardRef, useState, type InputHTMLAttributes } from "react";
import { Eye, EyeOff } from "lucide-react";

type PasswordFieldProps = InputHTMLAttributes<HTMLInputElement> & {
  id: string;
  label: string;
  error?: string;
};

export const PasswordField = forwardRef<HTMLInputElement, PasswordFieldProps>(
  function PasswordField({ id, label, error, className, ...props }, ref) {
    const [showPassword, setShowPassword] = useState(false);

    return (
      <div className="space-y-2">
        <label
          htmlFor={id}
          className="block text-sm font-medium text-[#B8C2D9]"
        >
          {label}
        </label>

        <div className="relative">
          <input
            ref={ref}
            id={id}
            type={showPassword ? "text" : "password"}
            aria-invalid={Boolean(error)}
            aria-describedby={error ? `${id}-error` : undefined}
            className={[
              "h-11 w-full rounded-lg border bg-[#0D1422] px-3.5 pr-11 text-sm text-[#F4F7FF]",
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

          <button
            type="button"
            aria-label={showPassword ? "Hide password" : "Show password"}
            onClick={() => setShowPassword((current) => !current)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-[#8490A8] transition-colors hover:text-[#B8C2D9]"
          >
            {showPassword ? (
              <EyeOff className="h-4 w-4 cursor-pointer" />
            ) : (
              <Eye className="h-4 w-4 cursor-pointer" />
            )}
          </button>
        </div>

        {error && (
          <p id={`${id}-error`} className="text-sm text-[#F0526B]" role="alert">
            {error}
          </p>
        )}
      </div>
    );
  },
);

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { ApiError } from "@/lib/api/errors";
import { useAuth } from "@/features/auth/auth-context";
import { loginSchema, type LoginFormData } from "@/features/auth/auth-schema";

import { AuthField } from "./auth-field";
import { PasswordField } from "./password-field";

export function LoginForm() {
  const router = useRouter();
  const { login } = useAuth();

  const [apiError, setApiError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: "",
      password: "",
    },
    mode: "onSubmit",
  });

  const onSubmit = async (data: LoginFormData) => {
    setApiError(null);

    try {
      await login(data);

      router.replace("/dashboard");
    } catch (error) {
      if (error instanceof ApiError) {
        setApiError(error.message);
        return;
      }

      setApiError("Unable to sign in. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5" noValidate>
      <AuthField
        id="username"
        label="Username"
        type="text"
        autoComplete="username"
        placeholder="Enter your username"
        error={errors.username?.message}
        {...register("username")}
      />

      <PasswordField
        id="password"
        label="Password"
        autoComplete="current-password"
        placeholder="Enter your password"
        error={errors.password?.message}
        {...register("password")}
      />

      {apiError && (
        <div
          role="alert"
          aria-live="polite"
          className="rounded-lg border border-[#F0526B]/30 bg-[#F0526B]/10 px-4 py-3 text-sm text-[#F0526B]"
        >
          {apiError}
        </div>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className="flex h-11 w-full items-center justify-center gap-2 cursor-pointer rounded-lg bg-gradient-to-r from-[#4F7CFF] to-[#7C5CFF] font-medium text-white transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isSubmitting ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
            <span>Signing in...</span>
          </>
        ) : (
          "Sign In"
        )}
      </button>
    </form>
  );
}

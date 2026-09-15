"use client";

import { Loader2, UserRound } from "lucide-react";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

import { ApiError } from "@/lib/api/errors";
import { useAuth } from "@/features/auth/auth-context";

import { AuthField } from "./auth-field";
import { PasswordField } from "./password-field";

interface FormErrors {
  username?: string;
  password?: string;
}

export function LoginForm() {
  const router = useRouter();
  const { login, isLoading } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [errors, setErrors] = useState<FormErrors>({});
  const [apiError, setApiError] = useState("");

  function validate(): boolean {
    const nextErrors: FormErrors = {};

    if (!username.trim()) {
      nextErrors.username = "Username is required.";
    }

    if (!password) {
      nextErrors.password = "Password is required.";
    }

    setErrors(nextErrors);

    return Object.keys(nextErrors).length === 0;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setApiError("");

    if (!validate()) {
      return;
    }

    try {
      await login({
        username: username.trim(),
        password,
      });

      router.replace("/dashboard");
    } catch (error) {
      if (error instanceof ApiError) {
        setApiError(error.message);
      } else {
        setApiError("Unable to sign in. Please try again.");
      }
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      noValidate
      className="mt-8 space-y-5"
    >
      {apiError && (
        <div
          role="alert"
          className="rounded-xl border border-[#F0526B]/30 bg-[#F0526B]/10 px-4 py-3 text-sm text-[#F0526B]"
        >
          {apiError}
        </div>
      )}

      <AuthField
        id="username"
        name="username"
        type="text"
        label="Username"
        placeholder="Enter your username"
        value={username}
        onChange={(event) => {
          setUsername(event.target.value);

          if (errors.username) {
            setErrors((current) => ({
              ...current,
              username: undefined,
            }));
          }
        }}
        autoComplete="username"
        disabled={isLoading}
        icon={<UserRound className="size-4" />}
        error={errors.username}
      />

      <PasswordField
        value={password}
        onChange={(value) => {
          setPassword(value);

          if (errors.password) {
            setErrors((current) => ({
              ...current,
              password: undefined,
            }));
          }
        }}
        error={errors.password}
        disabled={isLoading}
      />

      <button
        type="submit"
        disabled={isLoading}
        className={[
          "relative flex h-12 w-full items-center justify-center",
          "rounded-xl px-6",
          "bg-gradient-to-r from-[#4F7CFF] to-[#7C5CFF]",
          "text-sm font-semibold text-white",
          "shadow-[0_0_24px_rgba(79,124,255,0.28)]",
          "transition-all duration-200",
          "hover:brightness-110",
          "hover:shadow-[0_0_30px_rgba(79,124,255,0.38)]",
          "active:scale-[0.99]",
          "disabled:cursor-not-allowed disabled:opacity-60",
        ].join(" ")}
      >
        {isLoading ? (
          <>
            <Loader2 className="mr-2 size-4 animate-spin" />
            Signing in...
          </>
        ) : (
          "Sign In"
        )}
      </button>
    </form>
  );
}
"use client";

import { useEffect, type ReactNode } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/features/auth/auth-context";

const PUBLIC_ROUTES = ["/login"];

export function AuthGate({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();
  const isPublicRoute = PUBLIC_ROUTES.includes(pathname);

  useEffect(() => {
    if (isLoading) {
      return;
    }

    if (!isAuthenticated && !isPublicRoute) {
      router.replace("/login");
      return;
    }

    if (isAuthenticated && isPublicRoute) {
      router.replace("/dashboard");
    }
  }, [isAuthenticated, isLoading, isPublicRoute, pathname, router]);

  if (isLoading && !isPublicRoute) {
    return null;
  }

  if (!isAuthenticated && !isPublicRoute) {
    return null;
  }

  if (isAuthenticated && isPublicRoute) {
    return null;
  }

  return children;
}

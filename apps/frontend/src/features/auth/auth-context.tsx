"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  getAccessToken,
  removeAccessToken,
  setAccessToken,
} from "@/lib/auth/token-storage";

import { getCurrentUser, login as loginRequest } from "./auth-service";

import type { AuthState, LoginRequest, User } from "./types";

interface AuthContextValue extends AuthState {
  login: (credentials: LoginRequest) => Promise<void>;

  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedToken = getAccessToken();

    if (!storedToken) {
      queueMicrotask(() => {
        setIsLoading(false);
      });

      return;
    }

    async function restoreSession() {
      try {
        const currentUser = await getCurrentUser();

        setToken(storedToken);
        setUser(currentUser);

        if (process.env.NODE_ENV === "development") {
          console.log("[StockFlow Auth] Session restored", {
            token: storedToken,
            user: currentUser,
          });
        }
      } catch {
        removeAccessToken();

        setToken(null);
        setUser(null);

        if (process.env.NODE_ENV === "development") {
          console.warn("[StockFlow Auth] Stored token is invalid or expired");
        }
      } finally {
        setIsLoading(false);
      }
    }

    void restoreSession();
  }, []);

  const login = useCallback(async (credentials: LoginRequest) => {
    setIsLoading(true);

    try {
      const response = await loginRequest(credentials);
      const accessToken = response.access_token;

      if (!accessToken) {
        throw new Error("Login succeeded but no access token was returned.");
      }

      if (process.env.NODE_ENV === "development") {
        console.log("[StockFlow Auth] Login response:", response);
        console.log("[StockFlow Auth] Access token:", accessToken);
      }

      setAccessToken(accessToken);

      const currentUser = await getCurrentUser();

      setToken(accessToken);
      setUser(currentUser);

      if (process.env.NODE_ENV === "development") {
        console.log("[StockFlow Auth] Authenticated user:", currentUser);
      }
    } catch (error) {
      removeAccessToken();

      setToken(null);
      setUser(null);

      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    removeAccessToken();

    setToken(null);
    setUser(null);

    if (process.env.NODE_ENV === "development") {
      console.log("[StockFlow Auth] Logged out");
    }
  }, []);

  const value = useMemo(
    () => ({
      token,
      user,
      isLoading,
      isAuthenticated: Boolean(token && user),
      login,
      logout,
    }),
    [token, user, isLoading, login, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider.");
  }

  return context;
}

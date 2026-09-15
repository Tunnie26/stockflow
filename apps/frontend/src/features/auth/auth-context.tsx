"use client";

import {
  createContext,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  getCurrentUser,
  login as loginRequest,
} from "./auth-service";
import type { AuthState, LoginRequest, User } from "./types";

interface AuthContextValue extends AuthState {
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({
  children,
}: AuthProviderProps) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const login = async (
    credentials: LoginRequest,
  ): Promise<void> => {
    setIsLoading(true);

    try {
      const response = await loginRequest(credentials);
      const currentUser = await getCurrentUser(
        response.access_token,
      );

      setToken(response.access_token);
      setUser(currentUser);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = (): void => {
    setToken(null);
    setUser(null);
  };

  const value = useMemo<AuthContextValue>(
    () => ({
      token,
      user,
      isLoading,
      isAuthenticated: token !== null && user !== null,
      login,
      logout,
    }),
    [token, user, isLoading],
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used within an AuthProvider.",
    );
  }

  return context;
}
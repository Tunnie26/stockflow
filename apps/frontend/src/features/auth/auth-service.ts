import { apiClient } from "@/lib/api/client";
import { LoginRequest, LoginResponse, User } from "./types";

export async function login(credentials: LoginRequest): Promise<LoginResponse> {
  return apiClient.post<LoginResponse>("/api/v1/auth/login", credentials);
}

export async function getCurrentUser(token: string): Promise<User> {
  return apiClient.get<User>("/api/v1/auth/me", {
    token,
  });
}

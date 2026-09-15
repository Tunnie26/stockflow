import { apiClient } from "@/lib/api/client";
import type { LoginRequest, LoginResponse, User } from "./types";

export async function login(credentials: LoginRequest): Promise<LoginResponse> {
  return apiClient.post<LoginResponse>(process.env.NEXT_PUBLIC_AUTH_LOGIN!, credentials, {
    skipAuth: true,
  });
}

export async function getCurrentUser(): Promise<User> {
  return apiClient.get<User>(process.env.NEXT_PUBLIC_AUTH_ME!);
}

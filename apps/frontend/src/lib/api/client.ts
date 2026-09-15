import { getAccessToken } from "@/lib/auth/token-storage";
import { ApiError } from "./errors";
import type { ErrorResponse } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL;
console.log(process.env.NEXT_PUBLIC_API_URL)

if (!API_URL) {
  throw new Error("Missing required environment variable: NEXT_PUBLIC_API_URL");
}

export interface ApiRequestOptions extends RequestInit {
  skipAuth?: boolean;
}

async function request<T>(
  endpoint: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  const { skipAuth = false, ...fetchOptions } = options;

  const headers = new Headers(fetchOptions.headers);
  headers.set("Content-Type", "application/json");

  if (!skipAuth) {
    const token = getAccessToken();

    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  });

  const contentType = response.headers.get("content-type");
  const isJson = contentType?.includes("application/json");

  const body = isJson ? await response.json() : null;

  if (!response.ok) {
    const errorBody = body as ErrorResponse | null;

    throw new ApiError(
      errorBody?.error?.code ?? "API_ERROR",
      errorBody?.error?.message ?? "An unexpected error occurred.",
      response.status,
    );
  }

  if (body === null) {
    return undefined as T;
  }

  return body.data as T;
}

export const apiClient = {
  get<T>(endpoint: string, options?: ApiRequestOptions) {
    return request<T>(endpoint, {
      ...options,
      method: "GET",
    });
  },

  post<T>(
    endpoint: string,
    body?: unknown,
    options?: ApiRequestOptions,
  ) {
    return request<T>(endpoint, {
      ...options,
      method: "POST",
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  },

  patch<T>(
    endpoint: string,
    body?: unknown,
    options?: ApiRequestOptions,
  ) {
    return request<T>(endpoint, {
      ...options,
      method: "PATCH",
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  },

  delete<T>(endpoint: string, options?: ApiRequestOptions) {
    return request<T>(endpoint, {
      ...options,
      method: "DELETE",
    });
  },
};
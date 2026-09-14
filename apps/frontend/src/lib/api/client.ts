import { ApiError, isErrorResponse } from "./errors";
import type { SuccessResponse } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) {
  throw new Error("NEXT_PUBLIC_API_URL is not configured.");
}

interface RequestOptions extends Omit<RequestInit, "body"> {
  token?: string;
  body?: unknown;
}

async function request<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const { token, body, headers, ...requestInit } = options;

  const requestHeaders = new Headers(headers);

  requestHeaders.set("Accept", "application/json");

  if (body !== undefined) {
    requestHeaders.set("Content-Type", "application/json");
  }

  if (token) {
    requestHeaders.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...requestInit,
    headers: requestHeaders,
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  const contentType = response.headers.get("content-type");
  const isJson = contentType?.includes("application/json");

  const payload: unknown = isJson ? await response.json() : null;

  if (!response.ok) {
    if (isErrorResponse(payload)) {
      throw new ApiError(
        payload.error.code,
        payload.error.message,
        response.status,
      );
    }

    throw new ApiError(
      "UNKNOWN_ERROR",
      `Request failed with status ${response.status}.`,
      response.status,
    );
  }

  if (
    typeof payload !== "object" ||
    payload === null ||
    !("data" in payload)
  ) {
    throw new ApiError(
      "INVALID_RESPONSE",
      "The API returned an invalid response.",
      response.status,
    );
  }

  return (payload as SuccessResponse<T>).data;
}

export const apiClient = {
  get<T>(path: string, options?: Omit<RequestOptions, "body">) {
    return request<T>(path, {
      ...options,
      method: "GET",
    });
  },

  post<T>(
    path: string,
    body?: unknown,
    options?: Omit<RequestOptions, "body">,
  ) {
    return request<T>(path, {
      ...options,
      method: "POST",
      body,
    });
  },

  patch<T>(
    path: string,
    body?: unknown,
    options?: Omit<RequestOptions, "body">,
  ) {
    return request<T>(path, {
      ...options,
      method: "PATCH",
      body,
    });
  },

  delete<T>(path: string, options?: Omit<RequestOptions, "body">) {
    return request<T>(path, {
      ...options,
      method: "DELETE",
    });
  },
};
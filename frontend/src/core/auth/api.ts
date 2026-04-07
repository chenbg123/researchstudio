import { getBackendBaseURL } from "@/core/config";

import { type AuthSession } from "./types";

export async function loginWithPassword(
  username: string,
  password: string,
): Promise<AuthSession> {
  const response = await fetch(
    `${getBackendBaseURL()}/api/admin/auth/login`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
      credentials: "include",
    },
  );
  if (!response.ok) throw new Error("Login failed");
  return response.json() as Promise<AuthSession>;
}

export async function fetchSession(): Promise<AuthSession | null> {
  const response = await fetch(
    `${getBackendBaseURL()}/api/admin/auth/session`,
    {
      credentials: "include",
    },
  );
  if (!response.ok) return null;
  return response.json() as Promise<AuthSession>;
}

export async function logout(): Promise<void> {
  await fetch(`${getBackendBaseURL()}/api/admin/auth/logout`, {
    method: "POST",
    credentials: "include",
  });
}

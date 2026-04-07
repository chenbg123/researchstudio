import { getBackendBaseURL } from "../config";

import type { AdminUser, VisibilityRule } from "./types";

export async function listUsers(): Promise<{ users: AdminUser[] }> {
  const response = await fetch(`${getBackendBaseURL()}/api/admin/users`, {
    credentials: "include",
  });
  if (!response.ok) throw new Error("Failed to list users");
  return response.json() as Promise<{ users: AdminUser[] }>;
}

export async function createUser(data: {
  username: string;
  password: string;
  display_name: string;
  role?: string;
}): Promise<AdminUser> {
  const response = await fetch(`${getBackendBaseURL()}/api/admin/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
    credentials: "include",
  });
  if (!response.ok) {
    const error = await response
      .json()
      .catch(() => ({ detail: "Failed to create user" }));
    throw new Error(error.detail ?? "Failed to create user");
  }
  return response.json() as Promise<AdminUser>;
}

export async function disableUser(userId: string): Promise<AdminUser> {
  const response = await fetch(
    `${getBackendBaseURL()}/api/admin/users/${encodeURIComponent(userId)}/disable`,
    {
      method: "POST",
      credentials: "include",
    },
  );
  if (!response.ok) throw new Error("Failed to disable user");
  return response.json() as Promise<AdminUser>;
}

export async function resetPassword(
  userId: string,
  password: string,
): Promise<AdminUser> {
  const response = await fetch(
    `${getBackendBaseURL()}/api/admin/users/${encodeURIComponent(userId)}/reset-password`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
      credentials: "include",
    },
  );
  if (!response.ok) throw new Error("Failed to reset password");
  return response.json() as Promise<AdminUser>;
}

export async function listVisibilityRules(): Promise<{
  rules: VisibilityRule[];
}> {
  const response = await fetch(
    `${getBackendBaseURL()}/api/admin/visibility`,
    {
      credentials: "include",
    },
  );
  if (!response.ok) throw new Error("Failed to list visibility rules");
  return response.json() as Promise<{ rules: VisibilityRule[] }>;
}

export async function updateVisibility(
  category: string,
  key: string,
  enabled: boolean,
): Promise<VisibilityRule> {
  const response = await fetch(
    `${getBackendBaseURL()}/api/admin/visibility/${encodeURIComponent(category)}/${encodeURIComponent(key)}`,
    {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ enabled }),
      credentials: "include",
    },
  );
  if (!response.ok) throw new Error("Failed to update visibility");
  return response.json() as Promise<VisibilityRule>;
}

export async function listAllConversations(): Promise<{
  threads: Array<{
    thread_id: string;
    status: string;
    created_at: string;
    updated_at: string;
    metadata: Record<string, unknown>;
    values: Record<string, unknown>;
  }>;
}> {
  const response = await fetch(
    `${getBackendBaseURL()}/api/threads/search`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ limit: 200 }),
      credentials: "include",
    },
  );
  if (!response.ok) throw new Error("Failed to list conversations");
  const threads = await response.json();
  return { threads };
}

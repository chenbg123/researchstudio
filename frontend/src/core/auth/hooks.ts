"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { fetchSession, loginWithPassword, logout } from "./api";
import { type AuthSession } from "./types";

export function useSession() {
  return useQuery({
    queryKey: ["auth", "session"],
    queryFn: fetchSession,
  });
}

export function useLogin() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ username, password }: { username: string; password: string }) =>
      loginWithPassword(username, password),
    onSuccess: (session: AuthSession) => {
      queryClient.setQueryData(["auth", "session"], session);
    },
  });
}

export function useLogout() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: logout,
    onSuccess: () => {
      queryClient.setQueryData(["auth", "session"], null);
    },
  });
}

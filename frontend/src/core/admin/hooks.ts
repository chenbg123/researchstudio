import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  createUser,
  disableUser,
  listAllConversations,
  listUsers,
  listVisibilityRules,
  resetPassword,
  updateVisibility,
} from "./api";

export function useAdminUsers() {
  return useQuery({
    queryKey: ["admin", "users"],
    queryFn: listUsers,
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createUser,
    onSuccess() {
      void queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
    },
  });
}

export function useDisableUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ userId }: { userId: string }) => disableUser(userId),
    onSuccess() {
      void queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
    },
  });
}

export function useResetPassword() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      userId,
      password,
    }: {
      userId: string;
      password: string;
    }) => resetPassword(userId, password),
    onSuccess() {
      void queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
    },
  });
}

export function useAdminConversations() {
  return useQuery({
    queryKey: ["admin", "conversations"],
    queryFn: listAllConversations,
  });
}

export function useVisibilityRules() {
  return useQuery({
    queryKey: ["admin", "visibility"],
    queryFn: listVisibilityRules,
  });
}

export function useUpdateVisibility() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      category,
      key,
      enabled,
    }: {
      category: string;
      key: string;
      enabled: boolean;
    }) => updateVisibility(category, key, enabled),
    onSuccess() {
      void queryClient.invalidateQueries({
        queryKey: ["admin", "visibility"],
      });
    },
  });
}

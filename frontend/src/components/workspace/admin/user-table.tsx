"use client";

import { KeyRound, UserX } from "lucide-react";
import { useCallback, useState } from "react";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { useDisableUser, useResetPassword } from "@/core/admin/hooks";
import type { AdminUser } from "@/core/admin/types";

export function UserTable({ users }: { users: AdminUser[] }) {
  const { mutate: disableUser } = useDisableUser();
  const { mutate: resetPw } = useResetPassword();
  const [resetDialogOpen, setResetDialogOpen] = useState(false);
  const [resetUserId, setResetUserId] = useState<string | null>(null);
  const [newPassword, setNewPassword] = useState("");

  const handleDisable = useCallback(
    (userId: string) => {
      disableUser(
        { userId },
        {
          onSuccess: () => toast.success("User disabled"),
          onError: (e) => toast.error(e.message),
        },
      );
    },
    [disableUser],
  );

  const handleResetOpen = useCallback((userId: string) => {
    setResetUserId(userId);
    setNewPassword("");
    setResetDialogOpen(true);
  }, []);

  const handleResetSubmit = useCallback(() => {
    if (!resetUserId || newPassword.length < 8) {
      toast.error("Password must be at least 8 characters");
      return;
    }
    resetPw(
      { userId: resetUserId, password: newPassword },
      {
        onSuccess: () => {
          toast.success("Password reset successfully");
          setResetDialogOpen(false);
        },
        onError: (e) => toast.error(e.message),
      },
    );
  }, [resetPw, resetUserId, newPassword]);

  if (users.length === 0) {
    return (
      <p className="text-muted-foreground py-8 text-center text-sm">
        No users found.
      </p>
    );
  }

  return (
    <>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="text-muted-foreground border-b text-xs uppercase">
              <th className="px-3 py-2">Username</th>
              <th className="px-3 py-2">Display Name</th>
              <th className="px-3 py-2">Provider</th>
              <th className="px-3 py-2">Role</th>
              <th className="px-3 py-2">Status</th>
              <th className="px-3 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-b last:border-0">
                <td className="px-3 py-2 font-medium">{user.identifier}</td>
                <td className="px-3 py-2">{user.display_name}</td>
                <td className="px-3 py-2">{user.provider}</td>
                <td className="px-3 py-2">
                  <Badge variant={user.role === "admin" ? "default" : "outline"}>
                    {user.role}
                  </Badge>
                </td>
                <td className="px-3 py-2">
                  <Badge
                    variant={
                      user.status === "active" ? "default" : "destructive"
                    }
                  >
                    {user.status}
                  </Badge>
                </td>
                <td className="flex gap-1 px-3 py-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleResetOpen(user.id)}
                    title="Reset password"
                  >
                    <KeyRound className="size-4" />
                  </Button>
                  {user.status === "active" && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDisable(user.id)}
                      title="Disable user"
                    >
                      <UserX className="size-4" />
                    </Button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Dialog open={resetDialogOpen} onOpenChange={setResetDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Reset Password</DialogTitle>
          </DialogHeader>
          <div className="py-4">
            <Input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="New password (min 8 characters)"
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  handleResetSubmit();
                }
              }}
            />
          </div>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setResetDialogOpen(false)}
            >
              Cancel
            </Button>
            <Button onClick={handleResetSubmit}>Reset Password</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}

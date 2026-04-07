"use client";

import { useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { AdminShell } from "@/components/workspace/admin/admin-shell";
import { UserTable } from "@/components/workspace/admin/user-table";
import { useAdminUsers, useCreateUser } from "@/core/admin/hooks";

export default function AdminUsersPage() {
  const { data } = useAdminUsers();
  const { mutate: createUser } = useCreateUser();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [form, setForm] = useState({
    username: "",
    password: "",
    display_name: "",
    role: "user",
  });

  const handleCreate = () => {
    if (!form.username || form.password.length < 8 || !form.display_name) {
      toast.error(
        "All fields required. Password must be at least 8 characters.",
      );
      return;
    }
    createUser(form, {
      onSuccess: () => {
        toast.success("User created");
        setDialogOpen(false);
        setForm({ username: "", password: "", display_name: "", role: "user" });
      },
      onError: (e) => toast.error(e.message),
    });
  };

  return (
    <AdminShell title="User Management" description="Create and manage user accounts.">
      <div className="mb-4 flex justify-end">
        <Button onClick={() => setDialogOpen(true)}>Create User</Button>
      </div>
      <UserTable users={data?.users ?? []} />

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Create User</DialogTitle>
          </DialogHeader>
          <div className="flex flex-col gap-3 py-4">
            <Input
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              placeholder="Username"
            />
            <Input
              value={form.display_name}
              onChange={(e) =>
                setForm({ ...form, display_name: e.target.value })
              }
              placeholder="Display name"
            />
            <Input
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              placeholder="Password (min 8 characters)"
            />
            <select
              value={form.role}
              onChange={(e) => setForm({ ...form, role: e.target.value })}
              className="border-input bg-background h-9 rounded-md border px-3 text-sm"
            >
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleCreate}>Create</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </AdminShell>
  );
}

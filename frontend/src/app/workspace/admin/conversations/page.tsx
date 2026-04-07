"use client";

import { AdminShell } from "@/components/workspace/admin/admin-shell";
import { ConversationTable } from "@/components/workspace/admin/conversation-table";
import { useAdminConversations } from "@/core/admin/hooks";

export default function AdminConversationsPage() {
  const { data } = useAdminConversations();
  return (
    <AdminShell
      title="Conversation Review"
      description="Review all conversations across the workspace."
    >
      <ConversationTable conversations={data?.threads ?? []} />
    </AdminShell>
  );
}

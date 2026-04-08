"use client";

import { Badge } from "@/components/ui/badge";
import { formatTimeAgo } from "@/core/utils/datetime";

interface ConversationThread {
  thread_id: string;
  status: string;
  created_at: string;
  updated_at: string;
  metadata: Record<string, unknown>;
  values: Record<string, unknown>;
}

export function ConversationTable({
  conversations,
}: {
  conversations: ConversationThread[];
}) {
  if (conversations.length === 0) {
    return (
      <p className="text-muted-foreground py-8 text-center text-sm">
        No conversations found.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="text-muted-foreground border-b text-xs uppercase">
            <th className="px-3 py-2">Title</th>
            <th className="px-3 py-2">Thread ID</th>
            <th className="px-3 py-2">Status</th>
            <th className="px-3 py-2">Updated</th>
          </tr>
        </thead>
        <tbody>
          {conversations.map((thread) => (
            <tr key={thread.thread_id} className="border-b last:border-0">
              <td className="max-w-xs truncate px-3 py-2 font-medium">
                {(thread.values?.title as string) || "Untitled"}
              </td>
              <td className="text-muted-foreground px-3 py-2 font-mono text-xs">
                {thread.thread_id.slice(0, 8)}...
              </td>
              <td className="px-3 py-2">
                <Badge variant="outline">{thread.status}</Badge>
              </td>
              <td className="text-muted-foreground px-3 py-2">
                {thread.updated_at ? formatTimeAgo(new Date(Number(thread.updated_at) * 1000)) : "—"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

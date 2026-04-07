"use client";

import { AdminShell } from "@/components/workspace/admin/admin-shell";
import { CapabilityVisibilityPanel } from "@/components/workspace/admin/capability-visibility-panel";
import { useVisibilityRules } from "@/core/admin/hooks";

export default function AdminCapabilitiesPage() {
  const { data } = useVisibilityRules();
  return (
    <AdminShell
      title="Capability Visibility"
      description="Toggle profiles, skills, and MCP servers available to users."
    >
      <CapabilityVisibilityPanel rules={data?.rules ?? []} />
    </AdminShell>
  );
}

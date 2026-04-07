"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import {
  WorkspaceBody,
  WorkspaceContainer,
  WorkspaceHeader,
} from "@/components/workspace/workspace-container";
import { cn } from "@/lib/utils";

const adminTabs = [
  { label: "Users", href: "/workspace/admin/users" },
  { label: "Conversations", href: "/workspace/admin/conversations" },
  { label: "Capabilities", href: "/workspace/admin/capabilities" },
] as const;

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  return (
    <WorkspaceContainer>
      <WorkspaceHeader />
      <WorkspaceBody>
        <div className="flex size-full flex-col">
          <nav className="flex shrink-0 gap-1 border-b px-6 pt-2">
            {adminTabs.map((tab) => (
              <Link
                key={tab.href}
                href={tab.href}
                className={cn(
                  "border-b-2 px-4 py-2 text-sm font-medium transition-colors",
                  pathname === tab.href
                    ? "border-primary text-primary"
                    : "text-muted-foreground hover:text-foreground border-transparent",
                )}
              >
                {tab.label}
              </Link>
            ))}
          </nav>
          <div className="min-h-0 flex-1 overflow-y-auto">{children}</div>
        </div>
      </WorkspaceBody>
    </WorkspaceContainer>
  );
}

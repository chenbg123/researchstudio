"use client";

import { cn } from "@/lib/utils";

export function AdminShell({
  title,
  description,
  className,
  children,
}: {
  title: string;
  description?: string;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div
      className={cn(
        "mx-auto flex w-full max-w-7xl flex-col gap-6 px-6 py-6",
        className,
      )}
    >
      <div>
        <h1 className="text-2xl font-semibold">{title}</h1>
        {description && (
          <p className="text-muted-foreground mt-1 text-sm">{description}</p>
        )}
      </div>
      <div className="rounded-2xl border p-4 shadow-sm">{children}</div>
    </div>
  );
}

"use client";

import { useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { useUpdateVisibility } from "@/core/admin/hooks";
import type { VisibilityRule } from "@/core/admin/types";

export function CapabilityVisibilityPanel({
  rules,
}: {
  rules: VisibilityRule[];
}) {
  const { mutate: updateVisibility } = useUpdateVisibility();
  const [newCategory, setNewCategory] = useState("skills");
  const [newKey, setNewKey] = useState("");

  const handleToggle = (rule: VisibilityRule) => {
    updateVisibility(
      { category: rule.category, key: rule.key, enabled: !rule.enabled },
      {
        onError: (e) => toast.error(e.message),
      },
    );
  };

  const handleAdd = () => {
    if (!newKey.trim()) return;
    updateVisibility(
      { category: newCategory, key: newKey.trim(), enabled: true },
      {
        onSuccess: () => {
          setNewKey("");
          toast.success("Rule added");
        },
        onError: (e) => toast.error(e.message),
      },
    );
  };

  return (
    <div className="flex flex-col gap-4">
      {rules.length === 0 ? (
        <p className="text-muted-foreground py-4 text-center text-sm">
          No visibility rules configured.
        </p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="text-muted-foreground border-b text-xs uppercase">
                <th className="px-3 py-2">Category</th>
                <th className="px-3 py-2">Key</th>
                <th className="px-3 py-2">Enabled</th>
              </tr>
            </thead>
            <tbody>
              {rules.map((rule) => (
                <tr
                  key={`${rule.category}-${rule.key}`}
                  className="border-b last:border-0"
                >
                  <td className="px-3 py-2 font-medium">{rule.category}</td>
                  <td className="px-3 py-2">{rule.key}</td>
                  <td className="px-3 py-2">
                    <Switch
                      checked={rule.enabled}
                      onCheckedChange={() => handleToggle(rule)}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="flex items-center gap-2 border-t pt-4">
        <select
          value={newCategory}
          onChange={(e) => setNewCategory(e.target.value)}
          className="border-input bg-background h-9 rounded-md border px-3 text-sm"
        >
          <option value="skills">skills</option>
          <option value="profiles">profiles</option>
          <option value="mcp">mcp</option>
        </select>
        <Input
          value={newKey}
          onChange={(e) => setNewKey(e.target.value)}
          placeholder="Key name"
          className="max-w-xs"
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              handleAdd();
            }
          }}
        />
        <Button variant="outline" size="sm" onClick={handleAdd}>
          Add Rule
        </Button>
      </div>
    </div>
  );
}

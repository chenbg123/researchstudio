export interface AdminUser {
  id: string;
  provider: string;
  identifier: string;
  display_name: string;
  role: "admin" | "user";
  status: "active" | "disabled";
}

export interface VisibilityRule {
  category: "profiles" | "skills" | "mcp";
  key: string;
  enabled: boolean;
}

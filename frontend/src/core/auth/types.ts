export interface AuthSession {
  user: {
    id: string;
    identifier: string;
    display_name: string;
    role: "admin" | "user";
    email?: string;
  };
  token?: string;
}

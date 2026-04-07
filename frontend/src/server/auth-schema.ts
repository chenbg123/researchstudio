import { z } from "zod";

export const loginSchema = z.object({
  username: z.string().min(1),
  password: z.string().min(8),
});

export type LoginPayload = z.infer<typeof loginSchema>;

export function assertLoginPayload(payload: unknown) {
  const result = loginSchema.safeParse(payload);
  if (!result.success) {
    throw new Error("invalid payload");
  }
  return result.data;
}

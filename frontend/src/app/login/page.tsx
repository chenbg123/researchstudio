"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { useLogin } from "@/core/auth/hooks";

export default function LoginPage() {
  const router = useRouter();
  const login = useLogin();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6">
      <form
        className="w-full max-w-md rounded-2xl border border-white/10 bg-white p-8 shadow-2xl"
        onSubmit={(e) => {
          e.preventDefault();
          setError("");
          login.mutate(
            { username, password },
            {
              onSuccess: () => router.push("/workspace"),
              onError: () => setError("Invalid username or password"),
            },
          );
        }}
      >
        <h1 className="text-2xl font-semibold text-slate-900">
          DiResearchStudio
        </h1>
        <p className="mt-2 text-sm text-slate-600">
          Sign in to continue to the research workspace.
        </p>

        {error && (
          <p className="mt-4 text-sm text-red-600">{error}</p>
        )}

        <div className="mt-6 flex flex-col gap-4">
          <div>
            <label
              htmlFor="username"
              className="mb-1 block text-sm font-medium text-slate-700"
            >
              Username
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
              required
            />
          </div>
          <div>
            <label
              htmlFor="password"
              className="mb-1 block text-sm font-medium text-slate-700"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
              required
              minLength={8}
            />
          </div>
          <button
            type="submit"
            disabled={login.isPending}
            className="mt-2 w-full rounded-lg bg-slate-900 py-2.5 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-50"
          >
            {login.isPending ? "Signing in..." : "Sign in"}
          </button>
        </div>
      </form>
    </main>
  );
}

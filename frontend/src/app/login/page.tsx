"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { apiFetch, setAccessToken } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await apiFetch("/api/v1/auth/login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });
      setAccessToken(data.access_token);
      router.push("/members");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex">
      <div className="hidden md:flex w-1/2 bg-brand-sky text-white flex-col justify-center items-center p-12 text-center">
        <div className="w-20 h-20 rounded-full bg-white/10 flex items-center justify-center text-2xl font-bold mb-6">
          PGBMS
        </div>
        <h1 className="text-2xl font-bold mb-2">PCEA Gateway Parish</h1>
        <p className="text-white/80 mb-8">Boys&apos; &amp; Girls&apos; Brigade</p>
        <p className="italic text-white/70">&ldquo;Sure &amp; Stedfast&rdquo;</p>
      </div>

      <div className="w-full md:w-1/2 flex items-center justify-center p-8">
        <form onSubmit={handleSubmit} className="w-full max-w-sm space-y-4">
          <div className="mb-6">
            <h2 className="text-xl font-bold">Welcome back</h2>
            <p className="text-sm text-gray-500">Sign in to your staff profile</p>
          </div>

          {error && <div className="bg-red-50 text-brand-red text-sm p-2 rounded-lg">{error}</div>}

          <div>
            <label className="block text-sm font-medium mb-1">Username / Staff ID</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full border rounded-lg px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-brand-sky"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full border rounded-lg px-3 py-2.5 pr-10 focus:outline-none focus:ring-2 focus:ring-brand-sky"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword((v) => !v)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm"
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          <p className="text-xs text-gray-400">
            Your assigned department and permissions are applied automatically after sign-in.
          </p>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-brand-sky text-white py-2.5 rounded-lg font-medium hover:opacity-90 disabled:opacity-50"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}
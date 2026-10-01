"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { apiFetch, getAccessToken, clearAccessToken } from "@/lib/api";

interface CurrentUser {
  id: string;
  username: string;
  role: string;
  must_change_password: boolean;
  program_branch: string | null;
}

interface AuthContextValue {
  user: CurrentUser | null;
  loading: boolean;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue>({ user: null, loading: true, logout: () => {} });

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getAccessToken();
    if (!token) {
      setLoading(false);
      return;
    }
    apiFetch("/api/v1/auth/me")
      .then((data) => setUser(data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  function logout() {
    clearAccessToken();
    setUser(null);
    window.location.href = "/login";
  }

  return <AuthContext.Provider value={{ user, loading, logout }}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
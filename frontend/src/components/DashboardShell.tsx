"use client";

import { useEffect, type ReactNode } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { canAccessModule } from "@/lib/permissions";
import Sidebar from "./Sidebar";
import Header from "./Header";

interface DashboardShellProps {
  children: ReactNode;
  requiredModule?: string;
}

export default function DashboardShell({ children, requiredModule }: DashboardShellProps) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (loading) return;
    if (!user) {
      router.replace("/login");
      return;
    }
    if (requiredModule && !canAccessModule(user.role, requiredModule)) {
      router.replace("/forbidden");
    }
  }, [loading, user, requiredModule, router]);

  if (loading || !user) {
    return <div className="min-h-screen flex items-center justify-center text-gray-400">Loading...</div>;
  }

  if (requiredModule && !canAccessModule(user.role, requiredModule)) {
    return null;
  }

  return (
    <div className="min-h-screen flex bg-canvas">
      <Sidebar role={user.role} />
      <div className="flex-1 flex flex-col">
        <Header user={user} />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
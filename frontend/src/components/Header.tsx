"use client";

import { useAuth } from "@/lib/auth-context";

interface HeaderUser {
  username: string;
  role: string;
  program_branch: string | null;
}

export default function Header({ user }: { user: HeaderUser }) {
  const { logout } = useAuth();

  const logoLabel =
    user.program_branch === "girls_brigade" ? "GB" : user.program_branch === "boys_brigade" ? "BB" : "PGBMS";

  return (
    <header className="h-16 bg-white border-b flex items-center justify-between px-6 shrink-0">
      <div className="w-10 h-10 rounded-full bg-brand-sky-light text-brand-sky flex items-center justify-center font-bold text-xs">
        {logoLabel}
      </div>

      <div className="flex items-center gap-4">
        <button className="relative w-9 h-9 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center">
          <span className="text-sm">🔔</span>
          <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-brand-red" />
        </button>
        <div className="text-right">
          <p className="text-sm font-medium">{user.username}</p>
          <p className="text-xs text-gray-400 capitalize">{user.role.toLowerCase().replace("_", " ")}</p>
        </div>
        <button onClick={logout} className="text-sm text-gray-500 hover:text-brand-red">
          Logout
        </button>
      </div>
    </header>
  );
}
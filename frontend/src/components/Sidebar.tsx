"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { canAccessModule } from "@/lib/permissions";

const NAV_ITEMS = [
  { label: "Members", href: "/members", module: "members", builtYet: true },
  { label: "Attendance", href: "/attendance", module: "attendance", builtYet: true },
  { label: "Training", href: "/training", module: "training", builtYet: true },
  { label: "Finance", href: "/finance", module: "finance", builtYet: false },
  { label: "Welfare", href: "/welfare", module: "welfare", builtYet: false },
  { label: "Inventory", href: "/inventory", module: "inventory", builtYet: false },
  { label: "Meetings", href: "/meetings", module: "meetings", builtYet: false },
  { label: "Documents", href: "/documents", module: "documents", builtYet: false },
  { label: "Reports", href: "/reports", module: "reports", builtYet: false },
];

export default function Sidebar({ role }: { role: string }) {
  const pathname = usePathname();
  const visibleItems = NAV_ITEMS.filter((item) => canAccessModule(role, item.module));

  return (
    <aside className="w-64 bg-brand-sky text-white flex flex-col shrink-0">
      <div className="p-5 border-b border-white/10">
        <p className="font-bold text-lg leading-tight">PGBMS</p>
        <p className="text-xs text-white/70">PCEA Gateway Brigade</p>
      </div>
      <nav className="flex-1 overflow-y-auto py-3">
        {visibleItems.map((item) => {
          const active = pathname.startsWith(item.href);
          if (!item.builtYet) {
            return (
              <div
                key={item.href}
                className="flex items-center justify-between px-5 py-2.5 text-sm mx-2 mb-1 text-white/40 cursor-not-allowed"
              >
                {item.label}
                <span className="text-[10px] bg-white/10 px-1.5 py-0.5 rounded">soon</span>
              </div>
            );
          }
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`block px-5 py-2.5 text-sm rounded-lg mx-2 mb-1 transition ${
                active ? "bg-white text-brand-sky font-semibold" : "text-white/85 hover:bg-white/10"
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
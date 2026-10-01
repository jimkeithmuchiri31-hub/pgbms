"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import DashboardShell from "@/components/DashboardShell";

interface Member {
  id: string;
  brigade_number: string;
  first_name: string;
  last_name: string;
  member_category: string;
  status: string;
  phone: string | null;
}

export default function MembersPage() {
  const [search, setSearch] = useState("");

  const { data: members, isLoading, error } = useQuery<Member[]>({
    queryKey: ["members", search],
    queryFn: () => apiFetch(`/api/v1/members?search=${encodeURIComponent(search)}`),
  });

  return (
    <DashboardShell requiredModule="members">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Members</h1>
        <Link href="/members/new" className="bg-brand-sky text-white px-4 py-2 rounded-lg hover:opacity-90">
          + Add Member
        </Link>
      </div>

      <input
        type="text"
        placeholder="Search by name or brigade number..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full border rounded-lg px-3 py-2.5 mb-4"
      />

      {isLoading && <p className="text-gray-500">Loading members...</p>}
      {error && <p className="text-brand-red">Could not load members.</p>}

      {members && (
        <div className="bg-white rounded-xl shadow overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-left text-gray-500">
              <tr>
                <th className="p-3">Brigade No.</th>
                <th className="p-3">Name</th>
                <th className="p-3">Category</th>
                <th className="p-3">Status</th>
                <th className="p-3">Phone</th>
              </tr>
            </thead>
            <tbody>
              {members.length === 0 && (
                <tr>
                  <td colSpan={5} className="p-4 text-center text-gray-400">
                    No members found.
                  </td>
                </tr>
              )}
              {members.map((m) => (
                <tr key={m.id} className="border-t">
                  <td className="p-3">{m.brigade_number}</td>
                  <td className="p-3">{m.first_name} {m.last_name}</td>
                  <td className="p-3 capitalize">{m.member_category}</td>
                  <td className="p-3 capitalize">{m.status}</td>
                  <td className="p-3">{m.phone || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </DashboardShell>
  );
}
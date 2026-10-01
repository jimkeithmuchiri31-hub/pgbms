"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import DashboardShell from "@/components/DashboardShell";

export default function NewMemberPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    brigade_number: "",
    first_name: "",
    last_name: "",
    member_category: "brigadier",
    phone: "",
  });

  function update(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await apiFetch("/api/v1/members", {
        method: "POST",
        body: JSON.stringify(form),
      });
      router.push("/members");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create member");
    } finally {
      setLoading(false);
    }
  }

  return (
    <DashboardShell requiredModule="members">
      <h1 className="text-2xl font-bold mb-6">Add Member</h1>

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow space-y-4 max-w-lg">
        {error && <div className="bg-red-50 text-brand-red text-sm p-2 rounded-lg">{error}</div>}

        <div>
          <label className="block text-sm font-medium mb-1">Brigade Number</label>
          <input
            required
            value={form.brigade_number}
            onChange={(e) => update("brigade_number", e.target.value)}
            className="w-full border rounded-lg px-3 py-2.5"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">First Name</label>
            <input
              required
              value={form.first_name}
              onChange={(e) => update("first_name", e.target.value)}
              className="w-full border rounded-lg px-3 py-2.5"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Last Name</label>
            <input
              required
              value={form.last_name}
              onChange={(e) => update("last_name", e.target.value)}
              className="w-full border rounded-lg px-3 py-2.5"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Category</label>
          <select
            value={form.member_category}
            onChange={(e) => update("member_category", e.target.value)}
            className="w-full border rounded-lg px-3 py-2.5"
          >
            <option value="brigadier">Brigadier (child)</option>
            <option value="officer">Officer</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Phone</label>
          <input
            value={form.phone}
            onChange={(e) => update("phone", e.target.value)}
            className="w-full border rounded-lg px-3 py-2.5"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-brand-sky text-white py-2.5 rounded-lg font-medium hover:opacity-90 disabled:opacity-50"
        >
          {loading ? "Saving..." : "Save Member"}
        </button>
      </form>
    </DashboardShell>
  );
}
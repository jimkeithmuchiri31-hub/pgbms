"use client";

import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import DashboardShell from "@/components/DashboardShell";

interface Member {
  id: string;
  brigade_number: string;
  first_name: string;
  last_name: string;
}

interface MeetingType {
  id: string;
  name: string;
}

const STATUS_OPTIONS = ["Present", "Late", "Absent", "Excused"];

export default function AttendancePage() {
  const queryClient = useQueryClient();
  const today = new Date().toISOString().slice(0, 10);

  const [meetingTypeId, setMeetingTypeId] = useState("");
  const [date, setDate] = useState(today);
  const [statuses, setStatuses] = useState<Record<string, string>>({});
  const [saved, setSaved] = useState(false);

  const { data: meetingTypes } = useQuery<MeetingType[]>({
    queryKey: ["meeting-types"],
    queryFn: () => apiFetch("/api/v1/attendance/meeting-types"),
  });

  const { data: members } = useQuery<Member[]>({
    queryKey: ["members", "all"],
    queryFn: () => apiFetch("/api/v1/members?page_size=100"),
  });

  useEffect(() => {
    if (meetingTypes && meetingTypes.length > 0 && !meetingTypeId) {
      setMeetingTypeId(meetingTypes[0].id);
    }
  }, [meetingTypes, meetingTypeId]);

  function setStatus(memberId: string, status: string) {
    setStatuses((prev) => ({ ...prev, [memberId]: status }));
    setSaved(false);
  }

  const mutation = useMutation({
    mutationFn: () =>
      apiFetch("/api/v1/attendance/bulk", {
        method: "POST",
        body: JSON.stringify({
          meeting_type_id: meetingTypeId,
          date,
          records: (members || []).map((m) => ({
            member_id: m.id,
            status: statuses[m.id] || "Present",
          })),
        }),
      }),
    onSuccess: () => {
      setSaved(true);
      queryClient.invalidateQueries({ queryKey: ["attendance"] });
    },
  });

  return (
    <DashboardShell requiredModule="attendance">
      <h1 className="text-2xl font-bold mb-6">Attendance</h1>

      <div className="bg-white rounded-xl shadow p-4 mb-4 flex gap-4 items-end flex-wrap">
        <div>
          <label className="block text-sm font-medium mb-1">Meeting Type</label>
          <select
            value={meetingTypeId}
            onChange={(e) => setMeetingTypeId(e.target.value)}
            className="border rounded-lg px-3 py-2"
          >
            {meetingTypes?.map((mt) => (
              <option key={mt.id} value={mt.id}>{mt.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Date</label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="border rounded-lg px-3 py-2"
          />
        </div>
        <button
          onClick={() => mutation.mutate()}
          disabled={mutation.isPending || !members?.length}
          className="bg-brand-sky text-white px-5 py-2 rounded-lg font-medium hover:opacity-90 disabled:opacity-50"
        >
          {mutation.isPending ? "Saving..." : "Save Attendance"}
        </button>
        {saved && <span className="text-sm text-green-600">Saved ✓</span>}
      </div>

      <div className="bg-white rounded-xl shadow overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-left text-gray-500">
            <tr>
              <th className="p-3">Brigade No.</th>
              <th className="p-3">Name</th>
              <th className="p-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {members?.map((m) => (
              <tr key={m.id} className="border-t">
                <td className="p-3">{m.brigade_number}</td>
                <td className="p-3">{m.first_name} {m.last_name}</td>
                <td className="p-3">
                  <div className="flex gap-2">
                    {STATUS_OPTIONS.map((opt) => (
                      <button
                        key={opt}
                        type="button"
                        onClick={() => setStatus(m.id, opt)}
                        className={`px-2.5 py-1 rounded-full text-xs border ${
                          (statuses[m.id] || "Present") === opt
                            ? "bg-brand-sky text-white border-brand-sky"
                            : "text-gray-500 border-gray-200"
                        }`}
                      >
                        {opt}
                      </button>
                    ))}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DashboardShell>
  );
}
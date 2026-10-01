"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import DashboardShell from "@/components/DashboardShell";

interface Course {
  id: string;
  name: string;
}

interface Member {
  id: string;
  brigade_number: string;
  first_name: string;
  last_name: string;
}

interface TrainingRecord {
  id: string;
  member_id: string;
  course_id: string;
  status: string;
  start_date: string | null;
}

export default function TrainingPage() {
  const queryClient = useQueryClient();
  const [newCourseName, setNewCourseName] = useState("");
  const [enrollMemberId, setEnrollMemberId] = useState("");
  const [enrollCourseId, setEnrollCourseId] = useState("");

  const { data: courses } = useQuery<Course[]>({
    queryKey: ["courses"],
    queryFn: () => apiFetch("/api/v1/training/courses"),
  });

  const { data: members } = useQuery<Member[]>({
    queryKey: ["members", "all"],
    queryFn: () => apiFetch("/api/v1/members?page_size=100"),
  });

  const { data: records } = useQuery<TrainingRecord[]>({
    queryKey: ["training-records"],
    queryFn: () => apiFetch("/api/v1/training/records"),
  });

  const createCourse = useMutation({
    mutationFn: () =>
      apiFetch("/api/v1/training/courses", {
        method: "POST",
        body: JSON.stringify({ name: newCourseName }),
      }),
    onSuccess: () => {
      setNewCourseName("");
      queryClient.invalidateQueries({ queryKey: ["courses"] });
    },
  });

  const enrollMember = useMutation({
    mutationFn: () =>
      apiFetch("/api/v1/training/records", {
        method: "POST",
        body: JSON.stringify({ member_id: enrollMemberId, course_id: enrollCourseId }),
      }),
    onSuccess: () => {
      setEnrollMemberId("");
      setEnrollCourseId("");
      queryClient.invalidateQueries({ queryKey: ["training-records"] });
    },
  });

  function memberName(id: string) {
    const m = members?.find((mm) => mm.id === id);
    return m ? `${m.first_name} ${m.last_name}` : "—";
  }

  function courseName(id: string) {
    return courses?.find((c) => c.id === id)?.name || "—";
  }

  return (
    <DashboardShell requiredModule="training">
      <h1 className="text-2xl font-bold mb-6">Training</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-white rounded-xl shadow p-4">
          <h2 className="font-semibold mb-3">Courses</h2>
          <div className="flex gap-2 mb-3">
            <input
              value={newCourseName}
              onChange={(e) => setNewCourseName(e.target.value)}
              placeholder="New course name"
              className="flex-1 border rounded-lg px-3 py-2 text-sm"
            />
            <button
              onClick={() => newCourseName && createCourse.mutate()}
              className="bg-brand-sky text-white px-4 py-2 rounded-lg text-sm hover:opacity-90"
            >
              Add
            </button>
          </div>
          <ul className="text-sm divide-y">
            {courses?.map((c) => (
              <li key={c.id} className="py-2">{c.name}</li>
            ))}
            {courses?.length === 0 && <li className="py-2 text-gray-400">No courses yet.</li>}
          </ul>
        </div>

        <div className="bg-white rounded-xl shadow p-4">
          <h2 className="font-semibold mb-3">Enroll Member in Course</h2>
          <div className="space-y-2">
            <select
              value={enrollMemberId}
              onChange={(e) => setEnrollMemberId(e.target.value)}
              className="w-full border rounded-lg px-3 py-2 text-sm"
            >
              <option value="">Select member...</option>
              {members?.map((m) => (
                <option key={m.id} value={m.id}>{m.first_name} {m.last_name} ({m.brigade_number})</option>
              ))}
            </select>
            <select
              value={enrollCourseId}
              onChange={(e) => setEnrollCourseId(e.target.value)}
              className="w-full border rounded-lg px-3 py-2 text-sm"
            >
              <option value="">Select course...</option>
              {courses?.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
            <button
              onClick={() => enrollMemberId && enrollCourseId && enrollMember.mutate()}
              disabled={!enrollMemberId || !enrollCourseId}
              className="w-full bg-brand-sky text-white py-2 rounded-lg text-sm hover:opacity-90 disabled:opacity-50"
            >
              Enroll
            </button>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-left text-gray-500">
            <tr>
              <th className="p-3">Member</th>
              <th className="p-3">Course</th>
              <th className="p-3">Status</th>
              <th className="p-3">Started</th>
            </tr>
          </thead>
          <tbody>
            {records?.length === 0 && (
              <tr><td colSpan={4} className="p-4 text-center text-gray-400">No training records yet.</td></tr>
            )}
            {records?.map((r) => (
              <tr key={r.id} className="border-t">
                <td className="p-3">{memberName(r.member_id)}</td>
                <td className="p-3">{courseName(r.course_id)}</td>
                <td className="p-3 capitalize">{r.status.replace("_", " ")}</td>
                <td className="p-3">{r.start_date || "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DashboardShell>
  );
}
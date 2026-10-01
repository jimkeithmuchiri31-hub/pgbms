import Link from "next/link";

export default function ForbiddenPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-canvas">
      <div className="text-center bg-white rounded-xl shadow p-10 max-w-sm">
        <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-red-50 text-brand-red flex items-center justify-center text-2xl font-bold">
          403
        </div>
        <h1 className="text-lg font-bold mb-1">Access Forbidden</h1>
        <p className="text-sm text-gray-500 mb-6">
          Your account doesn&apos;t have permission to view this workspace.
        </p>
        <Link href="/members" className="text-brand-sky font-medium text-sm">
          Return to your workspace
        </Link>
      </div>
    </div>
  );
}
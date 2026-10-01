import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-2">PGBMS</h1>
        <p className="text-gray-500 mb-6">PCEA Gateway Brigade Management System</p>
        <Link href="/login" className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
          Sign In
        </Link>
      </div>
    </div>
  );
}
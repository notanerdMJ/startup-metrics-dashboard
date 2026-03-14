"use client";

import Sidebar from "@/components/layout/Sidebar";
import ProtectedRoute from "@/components/auth/ProtectedRoute";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-dashboard-bg">
        <Sidebar />
        <main className="ml-64 min-h-screen">
          <div className="p-8">{children}</div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
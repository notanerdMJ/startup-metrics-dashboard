// frontend/src/components/layout/Sidebar.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useAuth } from "@/hooks/useAuth";
import {
  BarChart3,
  LayoutDashboard,
  DollarSign,
  TrendingUp,
  Flame,
  Clock,
  Sparkles,
  LogOut,
  User,
  Home,
  ChevronLeft,
} from "lucide-react";

const menuItems = [
  {
    label: "Overview",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    label: "CAC Analysis",
    href: "/dashboard/cac",
    icon: DollarSign,
  },
  {
    label: "LTV Analysis",
    href: "/dashboard/ltv",
    icon: TrendingUp,
  },
  {
    label: "Burn Rate",
    href: "/dashboard/burn-rate",
    icon: Flame,
  },
  {
    label: "Runway",
    href: "/dashboard/runway",
    icon: Clock,
  },
  {
    label: "AI Advisor",
    href: "/dashboard/ai-advisor",
    icon: Sparkles,
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  return (
    <aside className="fixed left-0 top-0 bottom-0 w-64 bg-dashboard-bg border-r border-dashboard-border z-40 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-dashboard-border">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <BarChart3 className="w-5 h-5 text-white" />
          </div>
          <span className="text-lg font-bold text-white">
            Startup<span className="text-primary-400">Metrics</span>
          </span>
        </Link>
      </div>

      {/* Back to Home */}
      <div className="px-4 pt-4">
        <Link
          href="/"
          className="flex items-center gap-2 px-3 py-2 text-sm text-gray-500 hover:text-gray-300 transition-colors"
        >
          <ChevronLeft className="w-4 h-4" />
          Back to Home
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-4 space-y-1 overflow-y-auto">
        <p className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Analytics
        </p>
        {menuItems.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium",
                "transition-all duration-200",
                isActive
                  ? "bg-primary-600/10 text-primary-400 border border-primary-500/20"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              )}
            >
              <Icon className={cn("w-5 h-5", isActive && "text-primary-400")} />
              {item.label}
              {isActive && (
                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-primary-400" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* User Section */}
      <div className="p-4 border-t border-dashboard-border">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-8 h-8 rounded-full bg-primary-600/20 flex items-center justify-center">
            <User className="w-4 h-4 text-primary-400" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white truncate">
              {user?.full_name || "Guest"}
            </p>
            <p className="text-xs text-gray-500 truncate">
              {user?.email || "Not logged in"}
            </p>
          </div>
          <button
            onClick={logout}
            className="text-gray-500 hover:text-red-400 transition-colors"
            title="Logout"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}
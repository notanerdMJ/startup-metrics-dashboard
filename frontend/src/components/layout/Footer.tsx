// frontend/src/components/layout/Footer.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3 } from "lucide-react";

export default function Footer() {
  const pathname = usePathname();

  // Don't show footer on dashboard pages
  if (pathname?.startsWith("/dashboard")) return null;

  return (
    <footer className="bg-dashboard-bg border-t border-dashboard-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-white" />
              </div>
              <span className="text-lg font-bold text-white">
                Startup<span className="text-primary-400">Metrics</span>
              </span>
            </div>
            <p className="text-gray-400 text-sm max-w-md">
              Helping startup founders understand their financial health through
              AI-powered unit economics analysis and beautiful dashboards.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-sm font-semibold text-white mb-3">Product</h3>
            <div className="space-y-2">
              <Link href="/dashboard" className="block text-sm text-gray-400 hover:text-white transition-colors">
                Dashboard
              </Link>
              <Link href="/dashboard/ai-advisor" className="block text-sm text-gray-400 hover:text-white transition-colors">
                AI Advisor
              </Link>
              <Link href="/home" className="block text-sm text-gray-400 hover:text-white transition-colors">
                Overview
              </Link>
            </div>
          </div>

          {/* More Links */}
          <div>
            <h3 className="text-sm font-semibold text-white mb-3">Metrics</h3>
            <div className="space-y-2">
              <Link href="/dashboard/cac" className="block text-sm text-gray-400 hover:text-white transition-colors">
                CAC Analysis
              </Link>
              <Link href="/dashboard/ltv" className="block text-sm text-gray-400 hover:text-white transition-colors">
                LTV Analysis
              </Link>
              <Link href="/dashboard/burn-rate" className="block text-sm text-gray-400 hover:text-white transition-colors">
                Burn Rate
              </Link>
              <Link href="/dashboard/runway" className="block text-sm text-gray-400 hover:text-white transition-colors">
                Runway
              </Link>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-8 pt-8 border-t border-dashboard-border flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-sm text-gray-500">
            © 2024 StartupMetrics. Built for startup founders.
          </p>
          <p className="text-sm text-gray-500">
            Powered by AI · Built with Next.js & FastAPI
          </p>
        </div>
      </div>
    </footer>
  );
}
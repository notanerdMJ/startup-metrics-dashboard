// frontend/src/app/home/page.tsx
"use client";

import { useMetrics } from "@/hooks/useMetrics";
import { motion } from "framer-motion";
import Link from "next/link";
import Loading from "@/components/ui/Loading";
import {
  DollarSign,
  TrendingUp,
  Flame,
  Clock,
  Users,
  ArrowRight,
  Sparkles,
  AlertTriangle,
  CheckCircle,
} from "lucide-react";

export default function HomePage() {
  const { data: overview, loading, error } = useMetrics("/api/v1/dashboard/overview");
  const { data: insights } = useMetrics("/api/v1/ai/insights");

  if (loading) {
    return (
      <div className="min-h-screen bg-dashboard-bg flex items-center justify-center pt-16">
        <Loading size="lg" text="Loading metrics..." />
      </div>
    );
  }

  const cards = overview?.cards || [];
  const health = overview?.health || { score: 0, grade: "N/A" };
  const insightsList = insights?.insights || [];

  return (
    <div className="min-h-screen bg-dashboard-bg pt-24 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-12"
        >
          <h1 className="text-3xl sm:text-4xl font-bold text-white mb-3">
            Financial Overview
          </h1>
          <p className="text-gray-400 text-lg">
            Your startup&apos;s unit economics at a glance
          </p>
        </motion.div>

        {/* Health Score Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="mb-8"
        >
          <div className="bg-dashboard-card border border-dashboard-border rounded-2xl p-8">
            <div className="flex flex-col sm:flex-row items-center gap-8">
              {/* Score Circle */}
              <div className="relative w-32 h-32">
                <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 120 120">
                  <circle cx="60" cy="60" r="50" stroke="#2a2d3e" strokeWidth="8" fill="none" />
                  <circle
                    cx="60" cy="60" r="50"
                    stroke={health.score >= 70 ? "#10b981" : health.score >= 40 ? "#f59e0b" : "#ef4444"}
                    strokeWidth="8"
                    fill="none"
                    strokeDasharray={`${(health.score / 100) * 314} 314`}
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-3xl font-bold text-white">{health.score}</span>
                  <span className="text-xs text-gray-400">/ 100</span>
                </div>
              </div>

              <div className="flex-1 text-center sm:text-left">
                <h2 className="text-xl font-bold text-white mb-2">
                  Startup Health Score: Grade {health.grade}
                </h2>
                <p className="text-gray-400 mb-4">
                  {health.score >= 70
                    ? "Your startup is in good financial shape. Keep up the momentum!"
                    : health.score >= 40
                    ? "Some metrics need attention. Review the insights below."
                    : "Critical issues detected. Immediate action recommended."}
                </p>
                <Link
                  href="/dashboard"
                  className="inline-flex items-center gap-2 text-primary-400 hover:text-primary-300 font-medium text-sm"
                >
                  View Detailed Dashboard
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Metrics Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
          {cards.map((card: any, index: number) => {
            const icons: any = {
              "Customer Acquisition Cost": DollarSign,
              "Lifetime Value": TrendingUp,
              "LTV:CAC Ratio": TrendingUp,
              "Monthly Burn Rate": Flame,
              "Runway": Clock,
              "Total Conversions": Users,
            };
            const Icon = icons[card.title] || DollarSign;

            return (
              <motion.div
                key={card.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 + index * 0.1 }}
                className="bg-dashboard-card border border-dashboard-border rounded-xl p-6 hover:border-primary-500/30 transition-all duration-300"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="w-10 h-10 bg-primary-500/10 rounded-lg flex items-center justify-center">
                    <Icon className="w-5 h-5 text-primary-400" />
                  </div>
                  <span
                    className={`text-xs font-medium px-2 py-1 rounded-full ${
                      card.trend === "up"
                        ? "bg-emerald-500/10 text-emerald-400"
                        : card.trend === "down"
                        ? "bg-red-500/10 text-red-400"
                        : "bg-gray-500/10 text-gray-400"
                    }`}
                  >
                    {card.change > 0 ? "+" : ""}{card.change}%
                  </span>
                </div>
                <h3 className="text-sm text-gray-400 mb-1">{card.title}</h3>
                <p className="text-2xl font-bold text-white">{card.value}</p>
                <p className="text-xs text-gray-500 mt-2">{card.description}</p>
              </motion.div>
            );
          })}
        </div>

        {/* AI Insights */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <div className="flex items-center gap-3 mb-6">
            <Sparkles className="w-6 h-6 text-primary-400" />
            <h2 className="text-xl font-bold text-white">AI Insights</h2>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {insightsList.slice(0, 6).map((insight: any, index: number) => (
              <div
                key={index}
                className="bg-dashboard-card border border-dashboard-border rounded-xl p-5 hover:border-primary-500/30 transition-all duration-300"
              >
                <div className="flex items-start gap-3">
                  <div className={`mt-0.5 ${
                    insight.severity === "good"
                      ? "text-emerald-400"
                      : insight.severity === "warning"
                      ? "text-amber-400"
                      : "text-red-400"
                  }`}>
                    {insight.severity === "good" ? (
                      <CheckCircle className="w-5 h-5" />
                    ) : (
                      <AlertTriangle className="w-5 h-5" />
                    )}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                        insight.severity === "good"
                          ? "bg-emerald-500/10 text-emerald-400"
                          : insight.severity === "warning"
                          ? "bg-amber-500/10 text-amber-400"
                          : "bg-red-500/10 text-red-400"
                      }`}>
                        {insight.severity}
                      </span>
                      <span className="text-xs text-gray-500">{insight.insight_type}</span>
                    </div>
                    <p className="text-sm text-gray-300 leading-relaxed mb-2">
                      {insight.insight_text}
                    </p>
                    {insight.recommendation && (
                      <p className="text-xs text-primary-400 leading-relaxed">
                        💡 {insight.recommendation}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* CTA to Dashboard */}
          <div className="mt-8 text-center">
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-xl font-medium transition-all duration-300 shadow-lg shadow-primary-600/20"
            >
              Go to Full Dashboard
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
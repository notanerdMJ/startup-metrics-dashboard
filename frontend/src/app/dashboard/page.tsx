// frontend/src/app/dashboard/page.tsx
"use client";

import { useState, useEffect } from "react";
import Loading from "@/components/ui/Loading";
import {
  DollarSign,
  TrendingUp,
  Flame,
  Clock,
  Users,
  Target,
  Sparkles,
  RefreshCw,
  CheckCircle,
  AlertTriangle,
  Lightbulb,
} from "lucide-react";
import { motion } from "framer-motion";
import api from "@/lib/api";

export default function DashboardPage() {
  const [overview, setOverview] = useState<any>(null);
  const [insights, setInsights] = useState<any>(null);
  const [roi, setRoi] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [overviewRes, insightsRes, roiRes] = await Promise.all([
        api.get("/api/v1/dashboard/overview"),
        api.get("/api/v1/ai/insights"),
        api.get("/api/v1/metrics/roi"),
      ]);
      setOverview(overviewRes.data);
      setInsights(insightsRes.data);
      setRoi(roiRes.data || []);
    } catch (err) {
      console.error("Failed to fetch dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loading size="lg" text="Loading dashboard..." />
      </div>
    );
  }

  const cards = overview?.cards || [];
  const health = overview?.health || { score: 0, grade: "N/A", factors: [] };
  const insightsList = insights?.insights || [];

  // Icon and color helpers
  function getIcon(title: string) {
    if (title.includes("Acquisition")) return <DollarSign className="w-5 h-5 text-emerald-400" />;
    if (title.includes("Lifetime")) return <TrendingUp className="w-5 h-5 text-blue-400" />;
    if (title.includes("LTV")) return <Target className="w-5 h-5 text-purple-400" />;
    if (title.includes("Burn")) return <Flame className="w-5 h-5 text-amber-400" />;
    if (title.includes("Runway")) return <Clock className="w-5 h-5 text-cyan-400" />;
    if (title.includes("Conversion")) return <Users className="w-5 h-5 text-pink-400" />;
    return <DollarSign className="w-5 h-5 text-primary-400" />;
  }

  // Health score color
  const healthColor = health.score >= 70 ? "#10b981" : health.score >= 40 ? "#f59e0b" : "#ef4444";

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard Overview</h1>
          <p className="text-gray-400 mt-1">Your startup&apos;s financial metrics at a glance</p>
        </div>
        <button
          onClick={fetchData}
          className="flex items-center gap-2 px-4 py-2 bg-dashboard-card border border-dashboard-border rounded-lg text-gray-400 hover:text-white hover:border-primary-500/30 transition-all"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {cards.map((card: any, index: number) => (
          <motion.div
            key={card.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.1 }}
            className="bg-dashboard-card border border-dashboard-border rounded-xl p-6 hover:border-primary-500/30 transition-all duration-300"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-primary-500/10">
                {getIcon(card.title)}
              </div>
              {card.change !== undefined && (
                <span
                  className={`text-xs font-medium px-2.5 py-1 rounded-full ${
                    card.trend === "up"
                      ? "bg-emerald-500/10 text-emerald-400"
                      : card.trend === "down"
                      ? "bg-red-500/10 text-red-400"
                      : "bg-gray-500/10 text-gray-400"
                  }`}
                >
                  {card.change > 0 ? "+" : ""}{card.change}%
                </span>
              )}
            </div>
            <p className="text-sm text-gray-400 mb-1">{card.title}</p>
            <p className="text-2xl font-bold text-white tracking-tight">{card.value}</p>
            {card.description && (
              <p className="text-xs text-gray-500 mt-2">{card.description}</p>
            )}
          </motion.div>
        ))}
      </div>

      {/* Health Score + ROI Table */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Health Score */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-dashboard-card border border-dashboard-border rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold text-white mb-6">Startup Health Score</h3>
          <div className="flex items-center gap-8">
            <div className="relative w-28 h-28 flex-shrink-0">
              <svg className="w-28 h-28 transform -rotate-90" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" stroke="#2a2d3e" strokeWidth="8" fill="none" />
                <circle
                  cx="60" cy="60" r="50"
                  stroke={healthColor}
                  strokeWidth="8"
                  fill="none"
                  strokeDasharray={`${(health.score / 100) * 314} 314`}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-2xl font-bold text-white">{health.score}</span>
                <span className="text-xs text-gray-400">Grade {health.grade}</span>
              </div>
            </div>
            <div className="flex-1 space-y-3">
              {(health.factors || []).map((factor: any) => (
                <div key={factor.name}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs text-gray-400">{factor.name}</span>
                    <span className="text-xs text-gray-500">{factor.score}/30</span>
                  </div>
                  <div className="w-full h-1.5 bg-dashboard-border rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-1000"
                      style={{
                        width: `${(factor.score / 30) * 100}%`,
                        backgroundColor:
                          factor.status === "excellent" ? "#10b981" :
                          factor.status === "good" ? "#3b82f6" :
                          factor.status === "warning" ? "#f59e0b" : "#ef4444",
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* ROI Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="bg-dashboard-card border border-dashboard-border rounded-xl overflow-hidden"
        >
          <div className="px-6 py-4 border-b border-dashboard-border">
            <h3 className="text-lg font-semibold text-white">Channel ROI</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-dashboard-border">
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Channel</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ROI</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Spend</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Conv.</th>
                </tr>
              </thead>
              <tbody>
                {roi.map((row: any, i: number) => (
                  <tr key={i} className="border-b border-dashboard-border/50 hover:bg-dashboard-hover transition-colors">
                    <td className="px-6 py-4 text-sm text-gray-300">{row.channel}</td>
                    <td className={`px-6 py-4 text-sm font-medium ${row.roi_percentage > 0 ? "text-emerald-400" : "text-red-400"}`}>
                      {row.roi_percentage > 0 ? "+" : ""}{row.roi_percentage}%
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-300">${row.total_spend?.toLocaleString()}</td>
                    <td className="px-6 py-4 text-sm text-gray-300">{row.conversions?.toLocaleString()}</td>
                  </tr>
                ))}
                {roi.length === 0 && (
                  <tr>
                    <td colSpan={4} className="px-6 py-8 text-center text-gray-500">No data available</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </motion.div>
      </div>

      {/* AI Insights */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-5 h-5 text-primary-400" />
          <h2 className="text-lg font-semibold text-white">AI Insights</h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {insightsList.slice(0, 4).map((insight: any, index: number) => {
            const severityColor =
              insight.severity === "good" ? "text-emerald-400" :
              insight.severity === "critical" ? "text-red-400" : "text-amber-400";

            const severityBg =
              insight.severity === "good" ? "bg-emerald-500/10" :
              insight.severity === "critical" ? "bg-red-500/10" : "bg-amber-500/10";

            const severityBorder =
              insight.severity === "good" ? "border-emerald-500/20" :
              insight.severity === "critical" ? "border-red-500/20" : "border-amber-500/20";

            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className={`bg-dashboard-card border rounded-xl p-5 hover:border-primary-500/30 transition-all duration-300 ${severityBorder}`}
              >
                <div className="flex items-start gap-3">
                  <div className={`mt-0.5 flex-shrink-0 ${severityColor}`}>
                    {insight.severity === "good" ? (
                      <CheckCircle className="w-5 h-5" />
                    ) : (
                      <AlertTriangle className="w-5 h-5" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-2 flex-wrap">
                      <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${severityBg} ${severityColor}`}>
                        {insight.severity === "good" ? "Healthy" : insight.severity === "critical" ? "Critical" : "Warning"}
                      </span>
                      <span className="text-xs text-gray-500 uppercase">{insight.insight_type}</span>
                    </div>
                    <p className="text-sm text-gray-300 leading-relaxed mb-2">
                      {insight.insight_text}
                    </p>
                    {insight.recommendation && (
                      <div className="flex items-start gap-2 mt-3 p-3 bg-primary-500/5 rounded-lg border border-primary-500/10">
                        <Lightbulb className="w-4 h-4 text-primary-400 mt-0.5 flex-shrink-0" />
                        <p className="text-xs text-primary-300 leading-relaxed">
                          {insight.recommendation}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            );
          })}

          {insightsList.length === 0 && (
            <div className="col-span-2 bg-dashboard-card border border-dashboard-border rounded-xl p-8 text-center">
              <p className="text-gray-500">No insights yet. Run the ETL pipeline to generate AI insights.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
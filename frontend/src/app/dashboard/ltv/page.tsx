// frontend/src/app/dashboard/ltv/page.tsx
"use client";

import { useState, useEffect } from "react";
import Loading from "@/components/ui/Loading";
import api from "@/lib/api";
import { TrendingUp, Users, Target, DollarSign } from "lucide-react";
import { motion } from "framer-motion";

export default function LTVPage() {
  const [data, setData] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [ltvRes, summaryRes] = await Promise.all([
          api.get("/api/v1/metrics/ltv"),
          api.get("/api/v1/metrics/summary"),
        ]);
        setData(ltvRes.data);
        setSummary(summaryRes.data);
      } catch (err) {
        console.error("Failed to fetch LTV data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loading size="lg" text="Loading LTV data..." />
      </div>
    );
  }

  const segments = data?.by_income_segment || [];
  const ageGroups = data?.by_age_group || [];
  const ltvCac = data?.ltv_cac_ratio || [];
  const maxLtv = Math.max(...segments.map((s: any) => s.ltv), 1);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">LTV Analysis</h1>
        <p className="text-gray-400 mt-1">Customer Lifetime Value across segments</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: "Average LTV", value: `$${summary?.average_ltv?.toFixed(2) || "0"}`, icon: <TrendingUp className="w-5 h-5 text-blue-400" /> },
          { title: "LTV:CAC Ratio", value: `${summary?.ltv_cac_ratio?.toFixed(1) || "0"}x`, icon: <Target className={`w-5 h-5 ${summary?.ltv_cac_ratio >= 3 ? "text-emerald-400" : "text-amber-400"}`} /> },
          { title: "Segments", value: String(segments.length), icon: <Users className="w-5 h-5 text-purple-400" /> },
          { title: "Conversions", value: (summary?.total_conversions || 0).toLocaleString(), icon: <DollarSign className="w-5 h-5 text-pink-400" /> },
        ].map((card, index) => (
          <motion.div
            key={card.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.1 }}
            className="bg-dashboard-card border border-dashboard-border rounded-xl p-6"
          >
            <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-primary-500/10 mb-4">
              {card.icon}
            </div>
            <p className="text-sm text-gray-400 mb-1">{card.title}</p>
            <p className="text-2xl font-bold text-white">{card.value}</p>
          </motion.div>
        ))}
      </div>

      {/* LTV by Segment — Bar Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="bg-dashboard-card border border-dashboard-border rounded-xl p-6"
      >
        <h3 className="text-lg font-semibold text-white mb-6">LTV by Income Segment</h3>
        <div className="space-y-4">
          {segments.map((seg: any, index: number) => {
            const width = (seg.ltv / maxLtv) * 100;
            const colors = ["bg-emerald-500", "bg-blue-500", "bg-purple-500", "bg-amber-500"];
            return (
              <div key={seg.segment} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-300">{seg.segment}</span>
                  <div className="flex items-center gap-4">
                    <span className="text-sm font-semibold text-white">${seg.ltv.toFixed(2)}</span>
                    <span className="text-xs text-gray-500">{seg.total_customers} customers</span>
                  </div>
                </div>
                <div className="w-full h-3 bg-dashboard-border rounded-full overflow-hidden">
                  <motion.div
                    className={`h-full rounded-full ${colors[index % colors.length]}`}
                    initial={{ width: 0 }}
                    animate={{ width: `${width}%` }}
                    transition={{ duration: 0.8, delay: 0.3 + index * 0.1 }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </motion.div>

      {/* Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* LTV:CAC by Channel */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="bg-dashboard-card border border-dashboard-border rounded-xl overflow-hidden"
        >
          <div className="px-6 py-4 border-b border-dashboard-border">
            <h3 className="text-lg font-semibold text-white">LTV:CAC Ratio by Channel</h3>
          </div>
          <table className="w-full">
            <thead>
              <tr className="border-b border-dashboard-border">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Channel</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">LTV</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">CAC</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ratio</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody>
              {ltvCac.map((row: any, i: number) => (
                <tr key={i} className="border-b border-dashboard-border/50 hover:bg-dashboard-hover transition-colors">
                  <td className="px-6 py-4 text-sm text-gray-300">{row.channel}</td>
                  <td className="px-6 py-4 text-sm text-gray-300">${row.ltv.toFixed(2)}</td>
                  <td className="px-6 py-4 text-sm text-gray-300">${row.cac.toFixed(2)}</td>
                  <td className={`px-6 py-4 text-sm font-medium ${row.ltv_cac_ratio >= 3 ? "text-emerald-400" : row.ltv_cac_ratio >= 1 ? "text-amber-400" : "text-red-400"}`}>
                    {row.ltv_cac_ratio.toFixed(1)}x
                  </td>
                  <td className={`px-6 py-4 text-sm ${row.health === "Excellent" ? "text-emerald-400" : row.health === "Healthy" ? "text-blue-400" : row.health === "Warning" ? "text-amber-400" : "text-red-400"}`}>
                    {row.health}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>

        {/* LTV by Age Group */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="bg-dashboard-card border border-dashboard-border rounded-xl overflow-hidden"
        >
          <div className="px-6 py-4 border-b border-dashboard-border">
            <h3 className="text-lg font-semibold text-white">LTV by Age Group</h3>
          </div>
          <table className="w-full">
            <thead>
              <tr className="border-b border-dashboard-border">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Age</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">LTV</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Avg Income</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customers</th>
              </tr>
            </thead>
            <tbody>
              {ageGroups.map((row: any, i: number) => (
                <tr key={i} className="border-b border-dashboard-border/50 hover:bg-dashboard-hover transition-colors">
                  <td className="px-6 py-4 text-sm text-gray-300">{row.age_group}</td>
                  <td className={`px-6 py-4 text-sm font-medium ${row.ltv > 100 ? "text-emerald-400" : "text-gray-300"}`}>
                    ${row.ltv.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-300">${row.avg_income.toLocaleString()}</td>
                  <td className="px-6 py-4 text-sm text-gray-300">{row.customer_count.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>
      </div>
    </div>
  );
}
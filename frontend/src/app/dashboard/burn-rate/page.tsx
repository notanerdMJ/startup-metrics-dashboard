// frontend/src/app/dashboard/burn-rate/page.tsx
"use client";

import { useState, useEffect } from "react";
import Loading from "@/components/ui/Loading";
import api from "@/lib/api";
import { Flame, TrendingDown, DollarSign, AlertTriangle } from "lucide-react";
import { motion } from "framer-motion";

export default function BurnRatePage() {
  const [data, setData] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [burnRes, summaryRes] = await Promise.all([
          api.get("/api/v1/metrics/burn-rate"),
          api.get("/api/v1/metrics/summary"),
        ]);
        setData(burnRes.data);
        setSummary(summaryRes.data);
      } catch (err) {
        console.error("Failed to fetch burn rate data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loading size="lg" text="Loading burn rate data..." />
      </div>
    );
  }

  const channelBurn = data?.by_channel || [];
  const monthlyTrend = data?.monthly_trend || [];
  const maxExpense = Math.max(...monthlyTrend.map((m: any) => m.expenses), 1);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Burn Rate Analysis</h1>
        <p className="text-gray-400 mt-1">Monthly cash outflow and revenue trends</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: "Monthly Burn Rate", value: `$${(summary?.estimated_burn_rate || 0).toLocaleString()}`, icon: <Flame className="w-5 h-5 text-amber-400" /> },
          { title: "Total Ad Spend", value: `$${(summary?.total_ad_spend || 0).toLocaleString()}`, icon: <DollarSign className="w-5 h-5 text-red-400" /> },
          { title: "Runway Left", value: `${summary?.estimated_runway_months?.toFixed(0) || 0} mo`, icon: <AlertTriangle className="w-5 h-5 text-cyan-400" /> },
          { title: "Burn Channels", value: String(channelBurn.length), icon: <TrendingDown className="w-5 h-5 text-purple-400" /> },
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

      {/* Monthly Trend — Visual Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="bg-dashboard-card border border-dashboard-border rounded-xl p-6"
      >
        <h3 className="text-lg font-semibold text-white mb-2">Monthly Revenue vs Expenses</h3>
        <div className="flex items-center gap-6 mb-6">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-emerald-500" />
            <span className="text-xs text-gray-400">Revenue</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <span className="text-xs text-gray-400">Expenses</span>
          </div>
        </div>
        <div className="flex items-end gap-2 h-64">
          {monthlyTrend.map((month: any, i: number) => {
            const revHeight = (month.revenue / maxExpense) * 100;
            const expHeight = (month.expenses / maxExpense) * 100;

            return (
              <div key={month.month} className="flex-1 flex flex-col items-center gap-1">
                <div className="w-full flex gap-0.5 items-end" style={{ height: "200px" }}>
                  <motion.div
                    className="flex-1 bg-emerald-500/70 rounded-t"
                    initial={{ height: 0 }}
                    animate={{ height: `${revHeight}%` }}
                    transition={{ duration: 0.5, delay: 0.3 + i * 0.05 }}
                  />
                  <motion.div
                    className="flex-1 bg-red-500/70 rounded-t"
                    initial={{ height: 0 }}
                    animate={{ height: `${expHeight}%` }}
                    transition={{ duration: 0.5, delay: 0.3 + i * 0.05 }}
                  />
                </div>
                <span className="text-xs text-gray-500">{month.month}</span>
              </div>
            );
          })}
        </div>
      </motion.div>

      {/* Channel Burn Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="bg-dashboard-card border border-dashboard-border rounded-xl overflow-hidden"
      >
        <div className="px-6 py-4 border-b border-dashboard-border">
          <h3 className="text-lg font-semibold text-white">Burn Rate by Channel</h3>
        </div>
        <table className="w-full">
          <thead>
            <tr className="border-b border-dashboard-border">
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Channel</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Revenue</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Expenses</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Burn Rate</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody>
            {channelBurn.map((row: any, i: number) => (
              <tr key={i} className="border-b border-dashboard-border/50 hover:bg-dashboard-hover transition-colors">
                <td className="px-6 py-4 text-sm text-gray-300">{row.channel}</td>
                <td className="px-6 py-4 text-sm text-emerald-400">${row.monthly_revenue.toLocaleString()}</td>
                <td className="px-6 py-4 text-sm text-red-400">${row.monthly_expenses.toLocaleString()}</td>
                <td className={`px-6 py-4 text-sm font-medium ${row.burn_rate > 0 ? "text-red-400" : "text-emerald-400"}`}>
                  ${row.burn_rate.toLocaleString()}
                </td>
                <td className={`px-6 py-4 text-sm ${row.is_profitable ? "text-emerald-400" : "text-red-400"}`}>
                  {row.is_profitable ? "✅ Profitable" : "🔥 Burning"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </motion.div>
    </div>
  );
}
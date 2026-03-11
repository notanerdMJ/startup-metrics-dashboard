// frontend/src/app/dashboard/runway/page.tsx
"use client";

import { useState, useEffect } from "react";
import Loading from "@/components/ui/Loading";
import api from "@/lib/api";
import { Clock, AlertTriangle, TrendingUp, Shield } from "lucide-react";
import { motion } from "framer-motion";

export default function RunwayPage() {
  const [data, setData] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [runwayRes, summaryRes] = await Promise.all([
          api.get("/api/v1/metrics/runway"),
          api.get("/api/v1/metrics/summary"),
        ]);
        setData(runwayRes.data);
        setSummary(summaryRes.data);
      } catch (err) {
        console.error("Failed to fetch runway data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loading size="lg" text="Loading runway data..." />
      </div>
    );
  }

  const scenarios = data?.scenarios || [];
  const timeline = data?.timeline || [];

  // Find the max balance for scaling
  let maxBalance = 0;
  for (let i = 0; i < timeline.length; i++) {
    if (timeline[i].bank_balance > maxBalance) {
      maxBalance = timeline[i].bank_balance;
    }
  }
  if (maxBalance === 0) maxBalance = 1000000;

  // Find when cash runs out
  let cashOutMonth = timeline.length;
  for (let i = 0; i < timeline.length; i++) {
    if (!timeline[i].is_alive) {
      cashOutMonth = i + 1;
      break;
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Runway Prediction</h1>
        <p className="text-gray-400 mt-1">How long until your startup runs out of cash</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: "Current Runway", value: `${summary?.estimated_runway_months?.toFixed(0) || 0} months`, icon: <Clock className="w-5 h-5 text-cyan-400" /> },
          { title: "Monthly Burn", value: `$${(summary?.estimated_burn_rate || 0).toLocaleString()}`, icon: <AlertTriangle className="w-5 h-5 text-amber-400" /> },
          { title: "Bank Balance", value: "$1,000,000", icon: <Shield className="w-5 h-5 text-emerald-400" /> },
          { title: "Cash Out Month", value: `Month ${cashOutMonth}`, icon: <TrendingUp className="w-5 h-5 text-red-400" /> },
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

      {/* Bank Balance Timeline */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="bg-dashboard-card border border-dashboard-border rounded-xl p-6"
      >
        <h3 className="text-lg font-semibold text-white mb-2">Bank Balance Over Time</h3>
        <p className="text-sm text-gray-500 mb-6">
          Starting with $1,000,000 — showing month-by-month cash position
        </p>

        {/* Chart Container */}
        <div className="relative">
          {/* Y-axis labels */}
          <div className="absolute left-0 top-0 bottom-8 w-16 flex flex-col justify-between text-right pr-2">
            <span className="text-xs text-gray-500">${(maxBalance / 1000).toFixed(0)}K</span>
            <span className="text-xs text-gray-500">${(maxBalance / 2000).toFixed(0)}K</span>
            <span className="text-xs text-red-400">$0</span>
          </div>

          {/* Chart Area */}
          <div className="ml-16">
            {/* Horizontal grid lines */}
            <div className="relative" style={{ height: "250px" }}>
              <div className="absolute inset-0 flex flex-col justify-between">
                <div className="border-b border-dashboard-border/30" />
                <div className="border-b border-dashboard-border/30" />
                <div className="border-b border-dashboard-border/30" />
                <div className="border-b border-dashboard-border/30" />
                <div className="border-b border-red-500/30" />
              </div>

              {/* Bars */}
              <div className="absolute inset-0 flex items-end gap-1 px-1">
                {timeline.map((month: any, i: number) => {
                  const heightPercent = Math.max((month.bank_balance / maxBalance) * 100, 0);
                  const isAlive = month.bank_balance > 0;

                  return (
                    <div
                      key={i}
                      className="flex-1 flex flex-col items-center justify-end"
                      style={{ height: "100%" }}
                    >
                      {/* Tooltip on hover */}
                      <div className="group relative w-full">
                        <motion.div
                          className={`w-full rounded-t cursor-pointer ${
                            isAlive
                              ? heightPercent > 50
                                ? "bg-primary-500"
                                : heightPercent > 25
                                ? "bg-amber-500"
                                : "bg-red-400"
                              : "bg-red-600"
                          }`}
                          style={{ minHeight: isAlive ? "4px" : "4px" }}
                          initial={{ height: 0 }}
                          animate={{ height: `${Math.max(heightPercent, 1)}%` }}
                          transition={{ duration: 0.6, delay: 0.2 + i * 0.04 }}
                        />

                        {/* Hover tooltip */}
                        <div className="hidden group-hover:block absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-10">
                          <div className="bg-dashboard-bg border border-dashboard-border rounded-lg p-2 shadow-xl whitespace-nowrap">
                            <p className="text-xs text-white font-medium">Month {month.month}</p>
                            <p className="text-xs text-gray-400">
                              Balance: ${month.bank_balance.toLocaleString()}
                            </p>
                            <p className="text-xs text-red-400">
                              Burn: ${month.monthly_burn.toLocaleString()}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* X-axis labels */}
            <div className="flex gap-1 px-1 mt-2">
              {timeline.map((month: any, i: number) => (
                <div key={i} className="flex-1 text-center">
                  <span className="text-xs text-gray-500">
                    {i % 3 === 0 ? `M${month.month}` : ""}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Legend */}
        <div className="flex items-center justify-center gap-6 mt-6">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-primary-500" />
            <span className="text-xs text-gray-400">Healthy Balance</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-amber-500" />
            <span className="text-xs text-gray-400">Warning Zone</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-red-500" />
            <span className="text-xs text-gray-400">Danger / Out of Cash</span>
          </div>
        </div>
      </motion.div>

      {/* Monthly Details Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="bg-dashboard-card border border-dashboard-border rounded-xl overflow-hidden"
      >
        <div className="px-6 py-4 border-b border-dashboard-border">
          <h3 className="text-lg font-semibold text-white">Monthly Breakdown</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-dashboard-border">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Month</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bank Balance</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Revenue</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Expenses</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Burn</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody>
              {timeline.map((month: any, i: number) => (
                <tr key={i} className="border-b border-dashboard-border/50 hover:bg-dashboard-hover transition-colors">
                  <td className="px-6 py-3 text-sm text-gray-300">Month {month.month}</td>
                  <td className={`px-6 py-3 text-sm font-medium ${month.bank_balance > 500000 ? "text-emerald-400" : month.bank_balance > 100000 ? "text-amber-400" : "text-red-400"}`}>
                    ${month.bank_balance.toLocaleString()}
                  </td>
                  <td className="px-6 py-3 text-sm text-emerald-400">${month.monthly_revenue.toLocaleString()}</td>
                  <td className="px-6 py-3 text-sm text-red-400">${month.monthly_expenses.toLocaleString()}</td>
                  <td className="px-6 py-3 text-sm text-amber-400">${month.monthly_burn.toLocaleString()}</td>
                  <td className="px-6 py-3 text-sm">
                    {month.is_alive ? (
                      <span className="text-emerald-400">✅ Alive</span>
                    ) : (
                      <span className="text-red-400">💀 Out of Cash</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>

      {/* Scenario Cards */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-4">What-If Scenarios</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {scenarios.map((scenario: any, index: number) => (
            <motion.div
              key={scenario.scenario}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
              className={`bg-dashboard-card border rounded-xl p-6 ${
                scenario.risk_level === "low" ? "border-emerald-500/20" :
                scenario.risk_level === "medium" ? "border-amber-500/20" :
                "border-red-500/20"
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold text-white">{scenario.scenario}</h4>
                <span className={`text-xs font-medium px-2 py-1 rounded-full ${
                  scenario.risk_level === "low" ? "bg-emerald-500/10 text-emerald-400" :
                  scenario.risk_level === "medium" ? "bg-amber-500/10 text-amber-400" :
                  "bg-red-500/10 text-red-400"
                }`}>
                  {scenario.risk_level} risk
                </span>
              </div>
              <p className="text-xs text-gray-500 mb-4">{scenario.description}</p>

              {/* Runway visual bar */}
              <div className="mb-4">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-gray-400">Runway</span>
                  <span className="text-xs font-medium text-white">{scenario.runway_months} months</span>
                </div>
                <div className="w-full h-2 bg-dashboard-border rounded-full overflow-hidden">
                  <motion.div
                    className={`h-full rounded-full ${
                      scenario.runway_months > 18 ? "bg-emerald-500" :
                      scenario.runway_months > 12 ? "bg-blue-500" :
                      scenario.runway_months > 6 ? "bg-amber-500" :
                      "bg-red-500"
                    }`}
                    initial={{ width: 0 }}
                    animate={{ width: `${Math.min((scenario.runway_months / 36) * 100, 100)}%` }}
                    transition={{ duration: 0.8, delay: 0.5 + index * 0.1 }}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Monthly Burn</span>
                  <span className="text-red-400">${scenario.monthly_burn?.toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Revenue</span>
                  <span className="text-emerald-400">${scenario.monthly_revenue?.toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Expenses</span>
                  <span className="text-gray-300">${scenario.monthly_expenses?.toLocaleString()}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
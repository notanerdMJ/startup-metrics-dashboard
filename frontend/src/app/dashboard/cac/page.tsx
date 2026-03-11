// frontend/src/app/dashboard/cac/page.tsx
"use client";

import { useState, useEffect } from "react";
import Loading from "@/components/ui/Loading";
import api from "@/lib/api";
import { DollarSign, TrendingDown, BarChart3, Target } from "lucide-react";
import { motion } from "framer-motion";

export default function CACPage() {
  const [data, setData] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [cacRes, summaryRes] = await Promise.all([
          api.get("/api/v1/metrics/cac"),
          api.get("/api/v1/metrics/summary"),
        ]);
        setData(cacRes.data);
        setSummary(summaryRes.data);
      } catch (err) {
        console.error("Failed to fetch CAC data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loading size="lg" text="Loading CAC data..." />
      </div>
    );
  }

  const channelData = data?.by_channel || [];
  const campaignData = data?.by_campaign || [];
  const platformData = data?.by_platform || [];

  const bestChannel = channelData.length > 0 ? channelData[0] : null;
  const worstChannel = channelData.length > 0 ? channelData[channelData.length - 1] : null;
  const maxCac = Math.max(...channelData.map((c: any) => c.cac), 1);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">CAC Analysis</h1>
        <p className="text-gray-400 mt-1">Customer Acquisition Cost breakdown across channels</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          {
            title: "Overall CAC",
            value: `$${summary?.overall_cac?.toFixed(2) || "0"}`,
            icon: <DollarSign className="w-5 h-5 text-primary-400" />,
            desc: "Average cost per customer",
          },
          {
            title: "Best Channel CAC",
            value: bestChannel ? `$${bestChannel.cac.toFixed(2)}` : "N/A",
            icon: <TrendingDown className="w-5 h-5 text-emerald-400" />,
            desc: bestChannel ? bestChannel.channel : "",
          },
          {
            title: "Worst Channel CAC",
            value: worstChannel ? `$${worstChannel.cac.toFixed(2)}` : "N/A",
            icon: <BarChart3 className="w-5 h-5 text-red-400" />,
            desc: worstChannel ? worstChannel.channel : "",
          },
          {
            title: "Total Ad Spend",
            value: `$${(summary?.total_ad_spend || 0).toLocaleString()}`,
            icon: <Target className="w-5 h-5 text-amber-400" />,
            desc: "Across all channels",
          },
        ].map((card, index) => (
          <motion.div
            key={card.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.1 }}
            className="bg-dashboard-card border border-dashboard-border rounded-xl p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-primary-500/10">
                {card.icon}
              </div>
            </div>
            <p className="text-sm text-gray-400 mb-1">{card.title}</p>
            <p className="text-2xl font-bold text-white">{card.value}</p>
            <p className="text-xs text-gray-500 mt-2">{card.desc}</p>
          </motion.div>
        ))}
      </div>

      {/* CAC by Channel — Bar Chart using CSS */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="bg-dashboard-card border border-dashboard-border rounded-xl p-6"
      >
        <h3 className="text-lg font-semibold text-white mb-6">CAC by Channel</h3>
        <div className="space-y-4">
          {channelData.map((ch: any, index: number) => {
            const width = (ch.cac / maxCac) * 100;
            const colors = ["bg-primary-500", "bg-purple-500", "bg-blue-500", "bg-cyan-500", "bg-pink-500", "bg-amber-500"];
            const color = colors[index % colors.length];

            return (
              <div key={ch.channel} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-300">{ch.channel}</span>
                  <div className="flex items-center gap-4">
                    <span className="text-sm font-semibold text-white">${ch.cac.toFixed(2)}</span>
                    <span className="text-xs text-gray-500">{ch.customers_acquired} conv.</span>
                  </div>
                </div>
                <div className="w-full h-3 bg-dashboard-border rounded-full overflow-hidden">
                  <motion.div
                    className={`h-full rounded-full ${color}`}
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
        {/* Campaign Type Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="bg-dashboard-card border border-dashboard-border rounded-xl overflow-hidden"
        >
          <div className="px-6 py-4 border-b border-dashboard-border">
            <h3 className="text-lg font-semibold text-white">CAC by Campaign Type</h3>
          </div>
          <table className="w-full">
            <thead>
              <tr className="border-b border-dashboard-border">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Campaign</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">CAC</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Conversions</th>
              </tr>
            </thead>
            <tbody>
              {campaignData.map((row: any, i: number) => (
                <tr key={i} className="border-b border-dashboard-border/50 hover:bg-dashboard-hover transition-colors">
                  <td className="px-6 py-4 text-sm text-gray-300">{row.campaign_type}</td>
                  <td className={`px-6 py-4 text-sm font-medium ${row.cac < 100 ? "text-emerald-400" : row.cac < 200 ? "text-amber-400" : "text-red-400"}`}>
                    ${row.cac.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-300">{row.customers_acquired.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>

        {/* Platform Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="bg-dashboard-card border border-dashboard-border rounded-xl overflow-hidden"
        >
          <div className="px-6 py-4 border-b border-dashboard-border">
            <h3 className="text-lg font-semibold text-white">CAC by Platform</h3>
          </div>
          <table className="w-full">
            <thead>
              <tr className="border-b border-dashboard-border">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Platform</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">CAC</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">CTR</th>
              </tr>
            </thead>
            <tbody>
              {platformData.map((row: any, i: number) => (
                <tr key={i} className="border-b border-dashboard-border/50 hover:bg-dashboard-hover transition-colors">
                  <td className="px-6 py-4 text-sm text-gray-300">{row.platform}</td>
                  <td className={`px-6 py-4 text-sm font-medium ${row.cac < 100 ? "text-emerald-400" : row.cac < 200 ? "text-amber-400" : "text-red-400"}`}>
                    ${row.cac.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-300">{(row.avg_ctr * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>
      </div>
    </div>
  );
}
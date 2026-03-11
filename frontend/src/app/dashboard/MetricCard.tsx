// frontend/src/components/dashboard/MetricCard.tsx
"use client";

import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";
import { motion } from "framer-motion";

interface MetricCardProps {
  title: string;
  value: string;
  change?: number;
  trend?: "up" | "down" | "neutral";
  description?: string;
  icon: LucideIcon;
  color?: string;
  delay?: number;
}

export default function MetricCard({
  title,
  value,
  change,
  trend = "neutral",
  description,
  icon: Icon,
  color = "text-primary-400",
  delay = 0,
}: MetricCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className="bg-dashboard-card border border-dashboard-border rounded-xl p-6 hover:border-primary-500/30 transition-all duration-300"
    >
      <div className="flex items-center justify-between mb-4">
        <div className={cn("w-10 h-10 rounded-lg flex items-center justify-center bg-opacity-10", `bg-primary-500/10`)}>
          <Icon className={cn("w-5 h-5", color)} />
        </div>
        {change !== undefined && (
          <span
            className={cn(
              "text-xs font-medium px-2.5 py-1 rounded-full",
              trend === "up" && "bg-emerald-500/10 text-emerald-400",
              trend === "down" && "bg-red-500/10 text-red-400",
              trend === "neutral" && "bg-gray-500/10 text-gray-400"
            )}
          >
            {change > 0 ? "+" : ""}
            {change}%
          </span>
        )}
      </div>
      <p className="text-sm text-gray-400 mb-1">{title}</p>
      <p className="text-2xl font-bold text-white tracking-tight">{value}</p>
      {description && (
        <p className="text-xs text-gray-500 mt-2">{description}</p>
      )}
    </motion.div>
  );
}
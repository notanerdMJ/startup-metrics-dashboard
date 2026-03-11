// frontend/src/components/dashboard/InsightCard.tsx
"use client";

import { cn } from "@/lib/utils";
import { CheckCircle, AlertTriangle, XCircle, Lightbulb } from "lucide-react";
import { motion } from "framer-motion";

interface InsightCardProps {
  type: string;
  text: string;
  severity: "good" | "warning" | "critical";
  recommendation?: string;
  metricValue?: string;
  delay?: number;
}

export default function InsightCard({
  type,
  text,
  severity,
  recommendation,
  metricValue,
  delay = 0,
}: InsightCardProps) {
  const severityConfig = {
    good: {
      icon: CheckCircle,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10",
      border: "border-emerald-500/20",
      label: "Healthy",
    },
    warning: {
      icon: AlertTriangle,
      color: "text-amber-400",
      bg: "bg-amber-500/10",
      border: "border-amber-500/20",
      label: "Warning",
    },
    critical: {
      icon: XCircle,
      color: "text-red-400",
      bg: "bg-red-500/10",
      border: "border-red-500/20",
      label: "Critical",
    },
  };

  const config = severityConfig[severity] || severityConfig.warning;
  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className={cn(
        "bg-dashboard-card border rounded-xl p-5",
        "hover:border-primary-500/30 transition-all duration-300",
        config.border
      )}
    >
      <div className="flex items-start gap-3">
        <div className={cn("mt-0.5 flex-shrink-0", config.color)}>
          <Icon className="w-5 h-5" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <span className={cn("text-xs font-medium px-2 py-0.5 rounded-full", config.bg, config.color)}>
              {config.label}
            </span>
            <span className="text-xs text-gray-500 uppercase">{type}</span>
            {metricValue && (
              <span className="text-xs text-gray-400 font-mono">{metricValue}</span>
            )}
          </div>
          <p className="text-sm text-gray-300 leading-relaxed mb-2">{text}</p>
          {recommendation && (
            <div className="flex items-start gap-2 mt-3 p-3 bg-primary-500/5 rounded-lg border border-primary-500/10">
              <Lightbulb className="w-4 h-4 text-primary-400 mt-0.5 flex-shrink-0" />
              <p className="text-xs text-primary-300 leading-relaxed">{recommendation}</p>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
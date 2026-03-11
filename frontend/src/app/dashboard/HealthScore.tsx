// frontend/src/components/dashboard/HealthScore.tsx
"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface HealthScoreProps {
  score: number;
  grade: string;
  factors?: Array<{
    name: string;
    score: number;
    status: string;
  }>;
}

export default function HealthScore({ score, grade, factors = [] }: HealthScoreProps) {
  const getColor = (score: number) => {
    if (score >= 70) return "#10b981";
    if (score >= 40) return "#f59e0b";
    return "#ef4444";
  };

  const color = getColor(score);
  const circumference = 2 * Math.PI * 50;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-dashboard-card border border-dashboard-border rounded-xl p-6"
    >
      <h3 className="text-lg font-semibold text-white mb-6">Startup Health Score</h3>

      <div className="flex items-center gap-8">
        {/* Score Circle */}
        <div className="relative w-28 h-28 flex-shrink-0">
          <svg className="w-28 h-28 transform -rotate-90" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="50" stroke="#2a2d3e" strokeWidth="8" fill="none" />
            <motion.circle
              cx="60" cy="60" r="50"
              stroke={color}
              strokeWidth="8"
              fill="none"
              strokeLinecap="round"
              strokeDasharray={circumference}
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset }}
              transition={{ duration: 1.5, ease: "easeOut" }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-2xl font-bold text-white">{score}</span>
            <span className="text-xs text-gray-400">Grade {grade}</span>
          </div>
        </div>

        {/* Factors */}
        <div className="flex-1 space-y-3">
          {factors.map((factor) => (
            <div key={factor.name} className="flex items-center gap-3">
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-gray-400">{factor.name}</span>
                  <span className="text-xs text-gray-500">{factor.score}/30</span>
                </div>
                <div className="w-full h-1.5 bg-dashboard-border rounded-full overflow-hidden">
                  <motion.div
                    className="h-full rounded-full"
                    style={{
                      backgroundColor:
                        factor.status === "excellent" ? "#10b981" :
                        factor.status === "good" ? "#3b82f6" :
                        factor.status === "warning" ? "#f59e0b" : "#ef4444",
                    }}
                    initial={{ width: 0 }}
                    animate={{ width: `${(factor.score / 30) * 100}%` }}
                    transition={{ duration: 1, delay: 0.5 }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
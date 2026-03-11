// frontend/src/components/landing/Hero.tsx
"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { BarChart3, ArrowRight, Sparkles, TrendingUp, Shield } from "lucide-react";

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-dashboard-bg" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-600/20 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary-500/5 rounded-full blur-3xl" />

      {/* Grid Pattern */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                           linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)`,
          backgroundSize: "60px 60px",
        }}
      />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20">
        <div className="text-center">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-500/10 border border-primary-500/20 mb-8"
          >
            <Sparkles className="w-4 h-4 text-primary-400" />
            <span className="text-sm text-primary-300">AI-Powered Financial Analytics</span>
          </motion.div>

          {/* Main Heading */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight mb-6"
          >
            <span className="text-white">Know Your</span>
            <br />
            <span className="gradient-text">Unit Economics</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto mb-10"
          >
            Track CAC, LTV, Burn Rate, and Runway in real time.
            Let AI analyze your startup&apos;s financial health and guide
            you to profitability.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16"
          >
            <Link
              href="/register"
              className="group inline-flex items-center gap-2 px-8 py-3.5 bg-primary-600 hover:bg-primary-700 text-white rounded-xl font-semibold text-lg transition-all duration-300 shadow-lg shadow-primary-600/25 hover:shadow-primary-600/40"
            >
              Get Started Free
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 px-8 py-3.5 bg-white/5 hover:bg-white/10 text-white rounded-xl font-semibold text-lg transition-all duration-300 border border-white/10 hover:border-white/20"
            >
              <BarChart3 className="w-5 h-5" />
              View Dashboard
            </Link>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="grid grid-cols-3 gap-8 max-w-lg mx-auto mb-16"
          >
            {[
              { value: "6+", label: "Key Metrics" },
              { value: "AI", label: "Powered Insights" },
              { value: "Real-time", label: "Analytics" },
            ].map((stat) => (
              <div key={stat.label} className="text-center">
                <p className="text-2xl font-bold text-white">{stat.value}</p>
                <p className="text-sm text-gray-500">{stat.label}</p>
              </div>
            ))}
          </motion.div>

          {/* Preview Card */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.5 }}
            className="relative max-w-4xl mx-auto"
          >
            <div className="absolute -inset-1 bg-gradient-to-r from-primary-600 to-purple-600 rounded-2xl blur-lg opacity-20" />
            <div className="relative bg-dashboard-card border border-dashboard-border rounded-2xl p-8 shadow-2xl">
              {/* Mock Dashboard Preview */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
                {[
                  { label: "CAC", value: "$42.50", color: "text-emerald-400", icon: TrendingUp },
                  { label: "LTV", value: "$380.00", color: "text-blue-400", icon: BarChart3 },
                  { label: "Burn Rate", value: "$12.5K", color: "text-amber-400", icon: TrendingUp },
                  { label: "Runway", value: "18 mo", color: "text-purple-400", icon: Shield },
                ].map((metric) => (
                  <div key={metric.label} className="bg-white/5 rounded-xl p-4 border border-white/5">
                    <div className="flex items-center gap-2 mb-2">
                      <metric.icon className={`w-4 h-4 ${metric.color}`} />
                      <p className="text-xs text-gray-500">{metric.label}</p>
                    </div>
                    <p className={`text-xl font-bold ${metric.color}`}>{metric.value}</p>
                  </div>
                ))}
              </div>

              {/* Mock Chart Area */}
              <div className="bg-white/5 rounded-xl p-6 border border-white/5">
                <div className="flex items-center justify-between mb-4">
                  <p className="text-sm font-medium text-gray-400">Revenue vs Expenses</p>
                  <span className="text-xs text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded-full">
                    +12.5%
                  </span>
                </div>
                {/* Simple chart bars */}
                <div className="flex items-end gap-2 h-32">
                  {[40, 55, 45, 65, 50, 70, 60, 80, 75, 90, 85, 95].map((h, i) => (
                    <div key={i} className="flex-1 flex flex-col gap-1">
                      <div
                        className="bg-primary-500/30 rounded-t"
                        style={{ height: `${h}%` }}
                      />
                      <div
                        className="bg-primary-600 rounded-t"
                        style={{ height: `${h * 0.7}%` }}
                      />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
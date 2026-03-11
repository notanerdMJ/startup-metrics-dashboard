// frontend/src/components/landing/Features.tsx
"use client";

import { motion } from "framer-motion";
import {
  DollarSign,
  TrendingUp,
  Flame,
  Clock,
  Sparkles,
  BarChart3,
} from "lucide-react";

const features = [
  {
    icon: DollarSign,
    title: "CAC Tracking",
    description: "Monitor Customer Acquisition Cost across all channels. Know exactly how much each customer costs you.",
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
    border: "border-emerald-500/20",
  },
  {
    icon: TrendingUp,
    title: "LTV Analysis",
    description: "Calculate Customer Lifetime Value by segments. Understand which customers are most valuable.",
    color: "text-blue-400",
    bg: "bg-blue-500/10",
    border: "border-blue-500/20",
  },
  {
    icon: Flame,
    title: "Burn Rate Monitor",
    description: "Track monthly cash outflow vs revenue. See burn trends and identify cost-saving opportunities.",
    color: "text-amber-400",
    bg: "bg-amber-500/10",
    border: "border-amber-500/20",
  },
  {
    icon: Clock,
    title: "Runway Prediction",
    description: "Know exactly how many months until cash runs out. Model different scenarios for planning.",
    color: "text-purple-400",
    bg: "bg-purple-500/10",
    border: "border-purple-500/20",
  },
  {
    icon: Sparkles,
    title: "AI Financial Advisor",
    description: "Get AI-powered insights and recommendations. Chat with an advisor that understands your metrics.",
    color: "text-pink-400",
    bg: "bg-pink-500/10",
    border: "border-pink-500/20",
  },
  {
    icon: BarChart3,
    title: "Visual Analytics",
    description: "Beautiful charts and graphs that make complex financial data easy to understand at a glance.",
    color: "text-cyan-400",
    bg: "bg-cyan-500/10",
    border: "border-cyan-500/20",
  },
];

export default function Features() {
  return (
    <section className="py-24 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <p className="text-sm font-semibold text-primary-400 uppercase tracking-wider mb-3">
            Features
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Everything You Need to
            <span className="gradient-text"> Understand Your Finances</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            From acquisition costs to runway predictions, get a complete picture
            of your startup&apos;s financial health.
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="group relative bg-dashboard-card border border-dashboard-border rounded-xl p-6 hover:border-primary-500/30 transition-all duration-300"
            >
              <div className={`w-12 h-12 ${feature.bg} ${feature.border} border rounded-xl flex items-center justify-center mb-4`}>
                <feature.icon className={`w-6 h-6 ${feature.color}`} />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">
                {feature.title}
              </h3>
              <p className="text-sm text-gray-400 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
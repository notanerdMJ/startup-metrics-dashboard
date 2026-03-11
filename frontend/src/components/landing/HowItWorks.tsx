// frontend/src/components/landing/HowItWorks.tsx
"use client";

import { motion } from "framer-motion";
import { Upload, Cpu, BarChart3, Sparkles } from "lucide-react";

const steps = [
  {
    step: "01",
    icon: Upload,
    title: "Load Your Data",
    description: "Upload your startup's financial dataset. We support CSV files with marketing spend, revenue, and customer data.",
    color: "text-blue-400",
  },
  {
    step: "02",
    icon: Cpu,
    title: "ETL Processing",
    description: "Our pipeline cleans, transforms, and processes your data automatically. No manual work needed.",
    color: "text-purple-400",
  },
  {
    step: "03",
    icon: BarChart3,
    title: "View Metrics",
    description: "See CAC, LTV, Burn Rate, and Runway visualized on a beautiful dashboard with interactive charts.",
    color: "text-emerald-400",
  },
  {
    step: "04",
    icon: Sparkles,
    title: "Get AI Insights",
    description: "AI analyzes your metrics and provides actionable recommendations to improve your financial health.",
    color: "text-amber-400",
  },
];

export default function HowItWorks() {
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
            How It Works
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            From Data to
            <span className="gradient-text"> Decisions in Minutes</span>
          </h2>
        </motion.div>

        {/* Steps */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={step.step}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.15 }}
              className="relative"
            >
              {/* Connector line */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-12 left-full w-full h-[2px] bg-gradient-to-r from-dashboard-border to-transparent z-0" />
              )}

              <div className="relative z-10">
                <div className="text-6xl font-bold text-white/5 mb-4">{step.step}</div>
                <div className={`w-12 h-12 bg-white/5 border border-white/10 rounded-xl flex items-center justify-center mb-4`}>
                  <step.icon className={`w-6 h-6 ${step.color}`} />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  {step.title}
                </h3>
                <p className="text-sm text-gray-400 leading-relaxed">
                  {step.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
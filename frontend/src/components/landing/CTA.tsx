// frontend/src/components/landing/CTA.tsx
"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";

export default function CTA() {
  return (
    <section className="py-24 relative">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="relative"
        >
          {/* Glow */}
          <div className="absolute -inset-1 bg-gradient-to-r from-primary-600 to-purple-600 rounded-3xl blur-xl opacity-20" />

          <div className="relative bg-dashboard-card border border-dashboard-border rounded-2xl p-12 text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-500/10 border border-primary-500/20 mb-6">
              <Sparkles className="w-4 h-4 text-primary-400" />
              <span className="text-sm text-primary-300">Start for Free</span>
            </div>

            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              Ready to Understand Your
              <br />
              <span className="gradient-text">Startup&apos;s Financial Health?</span>
            </h2>

            <p className="text-gray-400 max-w-xl mx-auto mb-8">
              Join founders who use AI-powered analytics to make better financial
              decisions. No credit card required.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                href="/register"
                className="group inline-flex items-center gap-2 px-8 py-3.5 bg-primary-600 hover:bg-primary-700 text-white rounded-xl font-semibold transition-all duration-300 shadow-lg shadow-primary-600/25"
              >
                Get Started Now
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/dashboard"
                className="inline-flex items-center gap-2 px-8 py-3.5 bg-white/5 hover:bg-white/10 text-white rounded-xl font-semibold transition-all duration-300 border border-white/10"
              >
                View Demo Dashboard
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
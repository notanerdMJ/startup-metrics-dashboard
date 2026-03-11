// frontend/src/app/dashboard/ai-advisor/page.tsx
"use client";

import { useState, useEffect, useCallback } from "react";
import ChatWindow from "@/components/ai/ChatWindow";
import ChatInput from "@/components/ai/ChatInput";
import Loading from "@/components/ui/Loading";
import api from "@/lib/api";
import { motion } from "framer-motion";
import {
  Sparkles,
  Trash2,
  MessageSquare,
  AlertTriangle,
  CheckCircle,
  Lightbulb,
  Zap,
} from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export default function AIAdvisorPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [insights, setInsights] = useState<any[]>([]);
  const [insightsLoading, setInsightsLoading] = useState(true);
  const [aiStatus, setAiStatus] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Load AI status
  useEffect(() => {
    async function checkAI() {
      try {
        const res = await api.get("/api/v1/ai/status");
        setAiStatus(res.data);
      } catch (err) {
        console.error("Failed to check AI status:", err);
      }
    }
    checkAI();
  }, []);

  // Load insights
  useEffect(() => {
    async function loadInsights() {
      try {
        const res = await api.get("/api/v1/ai/insights");
        setInsights(res.data.insights || []);
      } catch (err) {
        console.error("Failed to load insights:", err);
      } finally {
        setInsightsLoading(false);
      }
    }
    loadInsights();
  }, []);

  // Load chat history
  useEffect(() => {
    async function loadHistory() {
      try {
        const res = await api.get("/api/v1/ai/chat/history");
        const history = (res.data.messages || []).map((msg: any) => ({
          id: String(msg.id),
          role: msg.role,
          content: msg.content,
          timestamp: msg.created_at,
        }));
        setMessages(history);
      } catch (err) {
        // User might not be logged in — that's okay
        console.log("Chat history not available (login required)");
      }
    }
    loadHistory();
  }, []);

  // Send message
  const sendMessage = useCallback(async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.post("/api/v1/ai/chat", {
        message: content,
      });

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.data.content,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || "Failed to send message. Please make sure you are logged in.";
      setError(errorMsg);

      // Add error as AI message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `⚠️ ${errorMsg}\n\nPlease log in first to use the AI chat feature. Go to /login to create an account.`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Clear history
  const clearHistory = async () => {
    try {
      await api.delete("/api/v1/ai/chat/history");
      setMessages([]);
    } catch (err) {
      console.error("Failed to clear history:", err);
    }
  };

  // Quick question handler
  const askQuestion = (question: string) => {
    sendMessage(question);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Sparkles className="w-7 h-7 text-primary-400" />
            AI Financial Advisor
          </h1>
          <p className="text-gray-400 mt-1">
            Ask questions about your startup&apos;s financial health
          </p>
        </div>
        <div className="flex items-center gap-3">
          {/* AI Status Badge */}
          <div
            className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium ${
              aiStatus?.ollama_available
                ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
            }`}
          >
            <div
              className={`w-2 h-2 rounded-full ${
                aiStatus?.ollama_available ? "bg-emerald-400" : "bg-amber-400"
              }`}
            />
            {aiStatus?.ollama_available ? "AI Online" : "Rule-Based Mode"}
          </div>

          {/* Clear History */}
          {messages.length > 0 && (
            <button
              onClick={clearHistory}
              className="flex items-center gap-2 px-3 py-1.5 bg-dashboard-card border border-dashboard-border rounded-lg text-gray-400 hover:text-red-400 hover:border-red-500/30 transition-all text-sm"
            >
              <Trash2 className="w-4 h-4" />
              Clear
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chat Section — Takes 2 columns */}
        <div className="lg:col-span-2">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-dashboard-bg border border-dashboard-border rounded-xl overflow-hidden flex flex-col"
            style={{ height: "600px" }}
          >
            {/* Chat Window */}
            <ChatWindow messages={messages} isLoading={isLoading} />

            {/* Chat Input */}
            <ChatInput onSend={sendMessage} isLoading={isLoading} />
          </motion.div>

          {/* Quick Questions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="mt-4"
          >
            <p className="text-xs text-gray-500 mb-2">Quick Questions:</p>
            <div className="flex flex-wrap gap-2">
              {[
                "Is my CAC too high?",
                "Analyze my LTV:CAC ratio",
                "How can I reduce burn rate?",
                "What's my runway looking like?",
                "Which channel has best ROI?",
                "Am I profitable?",
                "How to improve conversions?",
                "Give me a financial summary",
              ].map((question) => (
                <button
                  key={question}
                  onClick={() => askQuestion(question)}
                  disabled={isLoading}
                  className="px-3 py-1.5 bg-dashboard-card border border-dashboard-border rounded-lg text-xs text-gray-400 hover:text-white hover:border-primary-500/30 transition-all disabled:opacity-50"
                >
                  {question}
                </button>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Insights Sidebar — Takes 1 column */}
        <div className="lg:col-span-1">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bg-dashboard-card border border-dashboard-border rounded-xl overflow-hidden"
            style={{ height: "600px" }}
          >
            <div className="px-4 py-3 border-b border-dashboard-border flex items-center gap-2">
              <Lightbulb className="w-4 h-4 text-amber-400" />
              <h3 className="text-sm font-semibold text-white">AI Insights</h3>
            </div>

            <div className="overflow-y-auto p-4 space-y-3" style={{ height: "calc(100% - 48px)" }}>
              {insightsLoading ? (
                <div className="flex items-center justify-center py-8">
                  <Loading size="sm" text="Loading insights..." />
                </div>
              ) : insights.length > 0 ? (
                insights.map((insight: any, index: number) => {
                  const severityColor =
                    insight.severity === "good"
                      ? "text-emerald-400"
                      : insight.severity === "critical"
                      ? "text-red-400"
                      : "text-amber-400";

                  const severityBg =
                    insight.severity === "good"
                      ? "bg-emerald-500/10"
                      : insight.severity === "critical"
                      ? "bg-red-500/10"
                      : "bg-amber-500/10";

                  return (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                      className="p-3 bg-white/5 border border-white/5 rounded-lg hover:border-primary-500/20 transition-all"
                    >
                      <div className="flex items-center gap-2 mb-2">
                        {insight.severity === "good" ? (
                          <CheckCircle className={`w-3.5 h-3.5 ${severityColor}`} />
                        ) : (
                          <AlertTriangle className={`w-3.5 h-3.5 ${severityColor}`} />
                        )}
                        <span
                          className={`text-xs font-medium px-1.5 py-0.5 rounded ${severityBg} ${severityColor}`}
                        >
                          {insight.severity}
                        </span>
                        <span className="text-xs text-gray-600">{insight.insight_type}</span>
                      </div>
                      <p className="text-xs text-gray-300 leading-relaxed">
                        {insight.insight_text.length > 150
                          ? insight.insight_text.substring(0, 150) + "..."
                          : insight.insight_text}
                      </p>
                      {insight.recommendation && (
                        <p className="text-xs text-primary-400 mt-2 leading-relaxed">
                          💡 {insight.recommendation.length > 100
                            ? insight.recommendation.substring(0, 100) + "..."
                            : insight.recommendation}
                        </p>
                      )}
                    </motion.div>
                  );
                })
              ) : (
                <div className="text-center py-8">
                  <Zap className="w-8 h-8 text-gray-600 mx-auto mb-3" />
                  <p className="text-sm text-gray-500">
                    No insights yet. Run the ETL pipeline to generate insights.
                  </p>
                </div>
              )}
            </div>
          </motion.div>

          {/* Generate Insights Button */}
          <motion.button
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            onClick={async () => {
              setInsightsLoading(true);
              try {
                const res = await api.post("/api/v1/ai/insights/generate");
                setInsights(res.data.insights || []);
              } catch (err) {
                console.error("Failed to generate insights:", err);
              } finally {
                setInsightsLoading(false);
              }
            }}
            className="w-full mt-4 flex items-center justify-center gap-2 px-4 py-2.5 bg-primary-600 hover:bg-primary-700 text-white rounded-xl font-medium transition-all text-sm"
          >
            <Sparkles className="w-4 h-4" />
            Generate Fresh Insights
          </motion.button>
        </div>
      </div>
    </div>
  );
}